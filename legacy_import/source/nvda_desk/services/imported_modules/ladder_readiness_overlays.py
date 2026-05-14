"""Gate 33 ladder-readiness overlay contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.ladder_readiness_overlays import (
    LadderReadinessContext,
    LadderReadinessPayload,
    VvixLadderShaperContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class LadderReadinessContractEmission:
    """One typed ladder-readiness overlay output plus its DMP packets."""

    output: LadderReadinessPayload
    packet: DeskModulePacketV3


def _dependency_fences(
    dependencies: list[str],
    *,
    satisfied: set[str] | None = None,
    proxied: dict[str, str] | None = None,
) -> list[ContractDependencyFence]:
    satisfied = satisfied or set()
    proxied = proxied or {}
    fences: list[ContractDependencyFence] = []
    for dependency in dependencies:
        if dependency in proxied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.PROXIED_FROM_RUNTIME,
                    note=proxied[dependency],
                )
            )
        elif dependency in satisfied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.SATISFIED,
                    note="available directly inside the deterministic runtime or prior contract surface",
                )
            )
        else:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.FENCED_MISSING_SOURCE,
                    note="not available in the current deterministic runtime; kept as an explicit contract fence",
                )
            )
    return fences


class LadderReadinessContractService:
    """Emit Gate-33 ladder-readiness overlays in frozen order."""

    def evaluate(self, context: LadderReadinessContext) -> list[LadderReadinessContractEmission]:
        outputs: list[LadderReadinessPayload] = [self._vvix_ladder_shaper(context)]
        return [
            self._emit_packet(
                output=output,
                emitted_at=context.emitted_at,
                stack_id=context.stack_id,
                coefficient_set_id=context.coefficient_set_id,
            )
            for output in outputs
        ]

    def _emit_packet(
        self,
        *,
        output: LadderReadinessPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> LadderReadinessContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::ladder_readiness_overlays::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="LadderReadinessContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::ladder_readiness_overlays::{emitted_at.isoformat()}",
            run_id=f"run::ladder_readiness_overlays::{emitted_at.isoformat()}",
            module_instance_id=f"ladder_readiness_overlays::{output.canonical_slug}",
            registry_version="ladder_readiness_overlays_v1",
            environment_tag="research",
        )
        return LadderReadinessContractEmission(output=output, packet=packet)

    def _vvix_ladder_shaper(
        self, context: LadderReadinessContext
    ) -> VvixLadderShaperContractOutput:
        ladder = context.ladder_constructor.ladder_strikes
        vix_spread_state = context.options_flow.vix_spread_state
        vix_level = context.macro_data_capture.vix_level
        if vix_spread_state == "vvix_dislocation":
            vvix_regime = "vvix_spike"
            multiplier = 1.35
            state = "widen_for_vol_of_vol"
        elif vix_spread_state == "vvix_elevated":
            vvix_regime = "vvix_elevated"
            multiplier = 1.15
            state = "modestly_widened"
        elif vix_spread_state == "spread_calm" and (vix_level is None or vix_level <= 20.0):
            vvix_regime = "vvix_calm"
            multiplier = 0.9
            state = "compressed_for_calm_regime"
        else:
            vvix_regime = "vvix_neutral"
            multiplier = 1.0
            state = "ladder_unchanged"

        if ladder:
            anchor = ladder[0]
            reshaped_ladder = [
                round(anchor + ((strike - anchor) * multiplier), 2) for strike in ladder
            ]
        else:
            reshaped_ladder = []
            state = "no_ladder_available"

        return VvixLadderShaperContractOutput(
            canonical_id="archive-module-044",
            canonical_slug="vvix_ladder_shaper",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["ladder_constructor", "macro_metrics"],
                satisfied={"ladder_constructor"},
                proxied={
                    "macro_metrics": "proxied from the current options-flow VVIX plus market-substrate macro metrics already present in the deterministic runtime",
                },
            ),
            upstream_contract_slugs=["ladder_constructor", "macro_data_capture"],
            contract_notes=[
                "VVIX ladder shaping remains an advisory overlay that only reshapes the current preview ladder.",
                "No broker route, order mutation, or hidden named-playbook widening is implied by this surface.",
            ],
            vvix_regime=vvix_regime,
            ladder_width_multiplier=multiplier,
            reshaped_ladder=reshaped_ladder,
            shaper_state=state,
        )
