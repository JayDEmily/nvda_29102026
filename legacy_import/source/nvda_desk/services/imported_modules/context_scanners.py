"""Gate 19 context and scanner contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from statistics import fmean

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    AsiaPrecursorContextFilterContractOutput,
    ContextScannerContext,
    ContextScannerPayload,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    MacroAdaptiveWeightingFilterContractOutput,
    MacroSignalScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
    VixSpreadDetectorContractOutput,
    VolCorridorContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class ContextScannerContractEmission:
    """One typed context/scanner contract output plus its DMP packets."""

    output: ContextScannerPayload
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


class ContextScannerContractService:
    """Emit Gate-19 context/scanner contracts in frozen order."""

    def evaluate(self, context: ContextScannerContext) -> list[ContextScannerContractEmission]:
        outputs: list[ContextScannerPayload] = []
        macro_signal = self._macro_signal_score(context)
        execution_context = self._execution_context_score(context)
        vix_spread = self._vix_spread_detector(context)
        vol_corridor = self._vol_corridor(context)
        options_behaviour = self._options_behaviour_cluster(context)
        asia_precursor = self._asia_precursor_context_filter(context)
        macro_weighting = self._macro_adaptive_weighting_filter(context, macro_signal)
        engine_score = self._engine_score(
            context, macro_signal, execution_context, options_behaviour
        )
        outputs.extend(
            [
                macro_signal,
                execution_context,
                vix_spread,
                vol_corridor,
                options_behaviour,
                asia_precursor,
                macro_weighting,
                engine_score,
            ]
        )
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
        output: ContextScannerPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> ContextScannerContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::context_scanners::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="ContextScannerContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::context_scanners::{emitted_at.isoformat()}",
            run_id=f"run::context_scanners::{emitted_at.isoformat()}",
            module_instance_id=f"context_scanners::{output.canonical_slug}",
            registry_version="context_scanners_v1",
            environment_tag="research",
        )
        return ContextScannerContractEmission(output=output, packet=packet)

    def _macro_signal_score(self, context: ContextScannerContext) -> MacroSignalScoreContractOutput:
        macro_pressure = 0.0
        if (
            context.macro_data_capture.vix_level is not None
            and context.macro_data_capture.vix_level >= 25.0
        ):
            macro_pressure += 0.45
        if (
            context.macro_data_capture.curve_10s2s is not None
            and context.macro_data_capture.curve_10s2s <= 0.0
        ):
            macro_pressure += 0.25
        if context.temporal.event_window_state != "clear_window":
            macro_pressure += 0.15
        if context.regime.fx_stress_state != "fx_neutral":
            macro_pressure += 0.15
        macro_score = round(max(0.0, 1.0 - min(1.0, macro_pressure)), 4)
        if macro_score >= 0.7:
            macro_bias = "macro_supportive"
        elif macro_score <= 0.35:
            macro_bias = "macro_hostile"
        else:
            macro_bias = "macro_mixed"
        return MacroSignalScoreContractOutput(
            canonical_id="archive-module-013",
            canonical_slug="macro_signal_score",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:macro_data_capture",
                    "runtime:temporal_context",
                    "runtime:market_regime_context",
                ],
                satisfied={"market_substrate:macro_data_capture"},
                proxied={
                    "runtime:temporal_context": "proxied from the current temporal-context output event-window surface",
                    "runtime:market_regime_context": "proxied from the current regime output including FX and volatility states",
                },
            ),
            upstream_contract_slugs=["macro_data_capture"],
            contract_notes=[
                "This contract preserves the macro veto/scoring surface using the current macro substrate plus runtime regime context; it does not imply a separate live macro engine already exists.",
            ],
            macro_score=macro_score,
            macro_bias=macro_bias,
            event_sensitivity=context.temporal.event_window_state,
        )

    def _execution_context_score(
        self, context: ContextScannerContext
    ) -> ExecutionContextScoreContractOutput:
        raw_score = 0.45
        if context.posture.permission_state.value == "allow":
            raw_score += 0.2
        elif context.posture.permission_state.value == "block":
            raw_score -= 0.25
        if context.regime.volatility_regime.value == "stressed":
            raw_score -= 0.2
        if context.options_flow.gamma_state.value == "supportive":
            raw_score += 0.1
        elif context.options_flow.gamma_state.value == "destabilising":
            raw_score -= 0.1
        if context.temporal.desk_window in {"trend_window", "late_session"}:
            raw_score += 0.05
        score = round(max(0.0, min(1.0, raw_score)), 4)
        if score >= 0.65:
            execution_state = "deployable_context"
        elif score <= 0.25:
            execution_state = "do_not_press"
        else:
            execution_state = "mixed_context"
        upstream_contract_slugs = [
            "spot_data_capture",
            "options_data_capture",
            "options_metadata_capture",
            "macro_data_capture",
        ]
        return ExecutionContextScoreContractOutput(
            canonical_id="archive-module-021",
            canonical_slug="execution_context_score",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:spot_data_capture",
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                    "market_substrate:macro_data_capture",
                    "runtime:temporal_context",
                    "runtime:posture_risk",
                ],
                satisfied={
                    "market_substrate:spot_data_capture",
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                    "market_substrate:macro_data_capture",
                },
                proxied={
                    "runtime:temporal_context": "proxied from the current temporal-context desk-window classification",
                    "runtime:posture_risk": "proxied from the current posture permission surface rather than a separate execution-state engine",
                },
            ),
            upstream_contract_slugs=upstream_contract_slugs,
            contract_notes=[
                "Execution context remains an advisory contract surface only; provenance is explicit and no imported score is treated as approved execution logic.",
            ],
            context_score=score,
            execution_state=execution_state,
            desk_window=context.temporal.desk_window,
        )

    def _vix_spread_detector(
        self, context: ContextScannerContext
    ) -> VixSpreadDetectorContractOutput:
        spread = None
        if (
            context.macro_data_capture.vix_level is not None
            and context.macro_data_capture.vvix_level is not None
        ):
            spread = round(
                context.macro_data_capture.vvix_level - context.macro_data_capture.vix_level,
                4,
            )
        if spread is None:
            risk_tag = "spread_unavailable"
            signal_score = 0.0
        elif spread >= 80.0:
            risk_tag = "vvix_dislocation"
            signal_score = 1.0
        elif spread >= 70.0:
            risk_tag = "spread_elevated"
            signal_score = 0.7
        else:
            risk_tag = "spread_stable"
            signal_score = round(max(0.0, spread / 100.0), 4)
        return VixSpreadDetectorContractOutput(
            canonical_id="archive-module-019",
            canonical_slug="vix_spread_detector",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:macro_data_capture",
                    "runtime:options_flow_context",
                ],
                satisfied={"market_substrate:macro_data_capture"},
                proxied={
                    "runtime:options_flow_context": "proxied from the current options-flow vix_spread_state for tag alignment",
                },
            ),
            upstream_contract_slugs=["macro_data_capture"],
            contract_notes=[
                "The spread detector is rebuilt from the current macro substrate rather than a second hidden volatility-feed adapter.",
            ],
            spread=spread,
            risk_tag=risk_tag,
            signal_score=signal_score,
        )

    def _vol_corridor(self, context: ContextScannerContext) -> VolCorridorContractOutput:
        if (
            context.options_data_capture.front_atm_iv is not None
            and context.options_data_capture.next_atm_iv is not None
        ):
            corridor_width = round(
                abs(
                    context.options_data_capture.front_atm_iv
                    - context.options_data_capture.next_atm_iv
                ),
                4,
            )
        else:
            corridor_width = None
        if corridor_width is None:
            compression_flag = "corridor_unavailable"
            signal_score = 0.0
        elif corridor_width <= 1.5:
            compression_flag = "tight_corridor"
            signal_score = 0.85
        elif corridor_width <= 3.5:
            compression_flag = "normal_corridor"
            signal_score = 0.45
        else:
            compression_flag = "wide_corridor"
            signal_score = 0.15
        return VolCorridorContractOutput(
            canonical_id="archive-module-012",
            canonical_slug="vol_corridor",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                    "runtime:options_flow_context",
                ],
                satisfied={
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                },
                proxied={
                    "runtime:options_flow_context": "proxied from the current options-flow tenor-curve state to preserve runtime alignment",
                },
            ),
            upstream_contract_slugs=[
                "options_data_capture",
                "options_metadata_capture",
            ],
            contract_notes=[
                "Vol corridor is reconstructed from the current options substrate and tenor context; no separate live corridor engine is implied.",
            ],
            corridor_width=corridor_width,
            compression_flag=compression_flag,
            signal_score=signal_score,
        )

    def _options_behaviour_cluster(
        self, context: ContextScannerContext
    ) -> OptionsBehaviourClusterContractOutput:
        if (
            context.options_flow.gamma_state.value == "destabilising"
            and context.regime.volatility_regime.value == "stressed"
        ):
            cluster_tag = "stress_transition"
            signal_score = 0.2
        elif context.options_flow.options_behavior_cluster == "balanced_options_state":
            cluster_tag = "balanced_options_state"
            signal_score = 0.65
        else:
            cluster_tag = context.options_flow.options_behavior_cluster
            signal_score = 0.5
        return OptionsBehaviourClusterContractOutput(
            canonical_id="legacy-module-005",
            canonical_slug="options_behaviour_cluster",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                    "runtime:options_flow_context",
                ],
                satisfied={
                    "market_substrate:options_data_capture",
                    "market_substrate:options_metadata_capture",
                },
                proxied={
                    "runtime:options_flow_context": "proxied from the current options-behaviour cluster and gamma-state outputs",
                },
            ),
            upstream_contract_slugs=[
                "options_data_capture",
                "options_metadata_capture",
            ],
            contract_notes=[
                "The contract deepens options-behaviour labelling without claiming a separate monolithic options-state engine is already promoted.",
            ],
            cluster_tag=cluster_tag,
            signal_score=signal_score,
        )

    def _asia_precursor_context_filter(
        self, context: ContextScannerContext
    ) -> AsiaPrecursorContextFilterContractOutput:
        precursor_score = 0.5
        if (context.macro_data_capture.usdjpy or 0.0) >= 147.0:
            precursor_score += 0.2
        if context.temporal_input.prior_session_return_pct > 0:
            precursor_score += 0.1
        if context.regime.fx_stress_state != "fx_neutral":
            precursor_score -= 0.25
        precursor_score = round(max(0.0, min(1.0, precursor_score)), 4)
        if precursor_score >= 0.7:
            asia_state = "carry_supportive"
        elif precursor_score <= 0.3:
            asia_state = "asia_headwind"
        else:
            asia_state = "asia_mixed"
        return AsiaPrecursorContextFilterContractOutput(
            canonical_id="legacy-module-008",
            canonical_slug="asia_precursor_context_filter",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "market_substrate:macro_data_capture",
                    "runtime:temporal_context",
                ],
                satisfied={"market_substrate:macro_data_capture"},
                proxied={
                    "runtime:temporal_context": "proxied from prior-session return and desk timing rather than an Asia-session tape replay",
                },
            ),
            upstream_contract_slugs=["macro_data_capture"],
            contract_notes=[
                "Asia precursor context remains an inferred proxy surface only; the repo still does not carry a dedicated Asia-session market tape.",
            ],
            precursor_score=precursor_score,
            asia_state=asia_state,
            filter_state="runtime_precursor_proxy",
        )

    def _macro_adaptive_weighting_filter(
        self,
        context: ContextScannerContext,
        macro_signal: MacroSignalScoreContractOutput,
    ) -> MacroAdaptiveWeightingFilterContractOutput:
        weight_multiplier = 1.0
        if macro_signal.macro_bias == "macro_supportive":
            weight_multiplier += 0.1
        elif macro_signal.macro_bias == "macro_hostile":
            weight_multiplier -= 0.25
        if context.regime.volatility_regime.value == "stressed":
            weight_multiplier -= 0.1
        weight_multiplier = round(max(0.5, weight_multiplier), 4)
        if weight_multiplier >= 1.05:
            weighting_regime = "upweight_supportive_macro"
        elif weight_multiplier <= 0.75:
            weighting_regime = "downweight_hostile_macro"
        else:
            weighting_regime = "neutral_macro_weighting"
        return MacroAdaptiveWeightingFilterContractOutput(
            canonical_id="legacy-module-006",
            canonical_slug="macro_adaptive_weighting_filter",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:macro_signal_score",
                    "market_substrate:macro_data_capture",
                    "runtime:market_regime_context",
                ],
                satisfied={
                    "context_scanner:macro_signal_score",
                    "market_substrate:macro_data_capture",
                },
                proxied={
                    "runtime:market_regime_context": "proxied from the current volatility-regime surface to keep weighting aligned with live runtime context",
                },
            ),
            upstream_contract_slugs=["macro_signal_score", "macro_data_capture"],
            contract_notes=[
                "Adaptive weighting remains a bounded contract overlay; it adjusts advisory weighting only and does not rewrite live playbook logic.",
            ],
            weight_multiplier=weight_multiplier,
            weighting_regime=weighting_regime,
        )

    def _engine_score(
        self,
        context: ContextScannerContext,
        macro_signal: MacroSignalScoreContractOutput,
        execution_context: ExecutionContextScoreContractOutput,
        options_behaviour: OptionsBehaviourClusterContractOutput,
    ) -> EngineScoreContractOutput:
        base = fmean(
            [
                macro_signal.macro_score,
                execution_context.context_score,
                options_behaviour.signal_score,
            ]
        )
        if context.posture.permission_state.value == "block":
            base -= 0.15
        elif context.posture.permission_state.value == "derisk":
            base -= 0.05
        if context.eligibility.no_trade_reasons:
            base -= 0.05
        score = round(max(0.0, min(1.0, base)), 4)
        if score >= 0.7:
            conviction_band = "constructive"
            engine_state = "score_supportive"
        elif score <= 0.3:
            conviction_band = "suppressed"
            engine_state = "score_hostile"
        else:
            conviction_band = "mixed"
            engine_state = "score_balanced"
        upstream_contract_slugs = [
            "macro_signal_score",
            "execution_context_score",
            "options_behaviour_cluster",
        ]
        return EngineScoreContractOutput(
            canonical_id="archive-module-022",
            canonical_slug="engine_score",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:macro_signal_score",
                    "context_scanner:execution_context_score",
                    "context_scanner:options_behaviour_cluster",
                    "runtime:posture_risk",
                    "runtime:playbook_eligibility",
                ],
                satisfied={
                    "context_scanner:macro_signal_score",
                    "context_scanner:execution_context_score",
                    "context_scanner:options_behaviour_cluster",
                },
                proxied={
                    "runtime:posture_risk": "proxied from the current permission surface rather than a promoted supervisory engine",
                    "runtime:playbook_eligibility": "proxied from the current no-trade reasons to keep engine suppression honest",
                },
            ),
            upstream_contract_slugs=upstream_contract_slugs,
            contract_notes=[
                "Engine score is an advisory aggregate over explicit upstream contracts; it is not labelled approved and does not replace the current runtime decision path.",
            ],
            engine_score=score,
            conviction_band=conviction_band,
            engine_state=engine_state,
        )
