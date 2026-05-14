"""Gate 29 market-context synthesis contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.market_context_synthesis import (
    MarketContextSynthesisContext,
    MarketContextSynthesisPayload,
    RunSignalScanContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class MarketContextSynthesisContractEmission:
    """One typed synthesis contract output plus its DMP packets."""

    output: MarketContextSynthesisPayload
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


class MarketContextSynthesisContractService:
    """Emit Gate-29 synthesis contracts in frozen order."""

    def evaluate(
        self, context: MarketContextSynthesisContext
    ) -> list[MarketContextSynthesisContractEmission]:
        outputs: list[MarketContextSynthesisPayload] = [self._run_signal_scan(context)]
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
        output: MarketContextSynthesisPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> MarketContextSynthesisContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::market_context_synthesis::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="MarketContextSynthesisContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::market_context_synthesis::{emitted_at.isoformat()}",
            run_id=f"run::market_context_synthesis::{emitted_at.isoformat()}",
            module_instance_id=f"market_context_synthesis::{output.canonical_slug}",
            registry_version="market_context_synthesis_v1",
            environment_tag="research",
        )
        return MarketContextSynthesisContractEmission(output=output, packet=packet)

    def _run_signal_scan(
        self, context: MarketContextSynthesisContext
    ) -> RunSignalScanContractOutput:
        allowed = context.posture.permission_state.value == "allow"
        constructive = context.engine_score.engine_score >= 0.6
        watch_mode = (
            bool(context.eligibility.watch_only_candidates)
            and not context.eligibility.add_candidates
        )
        scan_state = (
            "scan_ready"
            if allowed and constructive
            else "scan_watch_only" if watch_mode else "scan_suppressed"
        )
        enabled_passes = [
            "macro_bias",
            "options_behaviour",
            "engine_conviction",
        ]
        if context.macro_signal_score.macro_bias != "balanced":
            enabled_passes.append("macro_bias_override")
        if context.temporal.event_window_state not in {"clear_window", "event_clear"}:
            enabled_passes.append("event_window_guard")
        candidate_count = (
            len(context.eligibility.add_candidates)
            if scan_state == "scan_ready"
            else len(context.eligibility.watch_only_candidates)
        )
        return RunSignalScanContractOutput(
            canonical_id="archive-module-052",
            canonical_slug="run_signal_scan",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "runtime_config",
                    "context_scanner:macro_signal_score",
                    "context_scanner:engine_score",
                ],
                satisfied={
                    "context_scanner:macro_signal_score",
                    "context_scanner:engine_score",
                },
                proxied={
                    "runtime_config": "proxied from the current deterministic stack_id/coefficient_set_id pair and runtime permission state",
                },
            ),
            upstream_contract_slugs=["macro_signal_score", "engine_score"],
            contract_notes=[
                "Run Signal Scan remains a bounded wrapper concept only; this contract preserves scan intent and gating without inventing a hidden scheduler.",
                "No execution trigger, broker call, or named-playbook widening is implied by this surface.",
            ],
            scan_state=scan_state,
            configured_scan_window=context.temporal.desk_window,
            enabled_passes=enabled_passes,
            candidate_count=candidate_count,
        )
