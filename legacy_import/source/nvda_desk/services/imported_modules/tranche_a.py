"""Tranche-A imported module services.

This module imports a bounded set of archive modules as typed, DMP-emitting
contract surfaces. The services preserve missing live-data dependencies as
explicit fences rather than hidden stubs.
"""

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
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
    ConvictionTierAllocatorContractOutput,
    EntryGateContractOutput,
    EventFlagCaptureContractOutput,
    GammaPressureContractOutput,
    IvVsRvAnalysisContractOutput,
    LadderConstructorContractOutput,
    ModelConfidenceScorerContractOutput,
    PeerDivergenceContractOutput,
    RealizedVolatilityEngineContractOutput,
    SignalConflictDetectorContractOutput,
    SkewInflectionContractOutput,
    TrancheAImportedPayload,
    TrancheASelectorContext,
    TrancheAUpstreamContext,
    VolumeSpikeFilterContractOutput,
)


@dataclass(frozen=True)
class TrancheAContractEmission:
    """One typed contract output plus its DMP packets."""

    output: TrancheAImportedPayload
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
                    note="available directly inside the deterministic runtime surface",
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


class TrancheAUpstreamContractService:
    """Import tranche-A temporal, regime, and options detectors as typed contracts."""

    def evaluate(self, context: TrancheAUpstreamContext) -> list[TrancheAContractEmission]:
        """Emit the seven upstream tranche-A contract surfaces in grammar order."""

        outputs: list[TrancheAImportedPayload] = [
            self._event_flag_capture(context),
            self._realized_volatility_engine(context),
            self._volume_spike_filter(context),
            self._peer_divergence(context),
            self._gamma_pressure(context),
            self._iv_vs_rv_analysis(context),
            self._skew_inflection(context),
        ]
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
        output: TrancheAImportedPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> TrancheAContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::tranche_a::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=self._summary(output),
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="TrancheAUpstreamContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::tranche_a::{emitted_at.isoformat()}",
            run_id=f"run::tranche_a::{emitted_at.isoformat()}",
            module_instance_id=f"tranche_a::{output.canonical_slug}",
            registry_version="tranche_a_v1",
            environment_tag="research",
        )
        return TrancheAContractEmission(output=output, packet=packet)

    def _summary(self, output: TrancheAImportedPayload) -> str:
        return f"{output.canonical_slug} / {output.computation_mode.value}"

    def _event_flag_capture(
        self, context: TrancheAUpstreamContext
    ) -> EventFlagCaptureContractOutput:
        event_flags: list[str] = []
        if context.temporal_input.next_event_at is not None:
            event_flags.append("scheduled_event")
        if context.temporal.event_window_state not in {"clear_window", "event_clear"}:
            event_flags.append(context.temporal.event_window_state)
        return EventFlagCaptureContractOutput(
            canonical_id="archive-module-006",
            canonical_slug="event_flag_capture",
            grammar_role=DmpGrammarRole.TEMPORAL_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["manual_or_api_events"],
                proxied={
                    "manual_or_api_events": "proxied from TemporalContextInput.next_event_at and TemporalContextOutput.event_window_state",
                },
            ),
            contract_notes=[
                "Event feed remains external; this contract only preserves the runtime-facing event flag surface."
            ],
            event_flags=event_flags,
            next_event_minutes=context.temporal.event_minutes_remaining,
            event_window_state=context.temporal.event_window_state,
            capture_state=("event_flags_present" if event_flags else "no_known_event_flags"),
        )

    def _realized_volatility_engine(
        self, context: TrancheAUpstreamContext
    ) -> RealizedVolatilityEngineContractOutput:
        rv_5d = context.options_flow_input.front_realised_vol or None
        rv_10d = context.options_flow_input.next_realised_vol or None
        score = 0.0
        if rv_5d is not None and rv_10d is not None:
            score = round(min(1.0, abs(rv_5d - rv_10d) / 25.0), 4)
        vol_direction = "rising" if (rv_5d or 0.0) >= (rv_10d or 0.0) else "easing"
        vol_compression = (
            "compressed" if abs((rv_5d or 0.0) - (rv_10d or 0.0)) <= 2.0 else "expanded"
        )
        return RealizedVolatilityEngineContractOutput(
            canonical_id="archive-module-009",
            canonical_slug="realized_volatility_engine",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["spot_prices"],
                proxied={
                    "spot_prices": "proxied from existing realised-volatility fields already passed into OptionsFlowContextInput"
                },
            ),
            contract_notes=[
                "Direct spot-price history remains outside the current runtime; the contract uses existing realised-volatility proxies only."
            ],
            rv_5d=rv_5d,
            rv_10d=rv_10d,
            vol_compression=vol_compression,
            vol_direction=vol_direction,
            signal_score=score,
            proxy_basis=["front_realised_vol", "next_realised_vol"],
        )

    def _volume_spike_filter(
        self, context: TrancheAUpstreamContext
    ) -> VolumeSpikeFilterContractOutput:
        return VolumeSpikeFilterContractOutput(
            canonical_id="archive-module-018",
            canonical_slug="volume_spike_filter",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.FENCED_CONTRACT_ONLY,
            dependency_fences=_dependency_fences(["spot_prices", "spot_volume_series"]),
            contract_notes=[
                "The current runtime has no volume-series surface, so the detector remains an honest contract fence."
            ],
            signal_score=0.0,
            spike_count=None,
            trap_flag=None,
            detection_state="dependency_fenced",
        )

    def _peer_divergence(self, context: TrancheAUpstreamContext) -> PeerDivergenceContractOutput:
        peer_proxy_returns = [
            context.regime_input.nq_return_pct,
            context.regime_input.es_return_pct,
            context.regime_input.sox_return_pct,
        ]
        peer_mean = fmean(peer_proxy_returns)
        residual = round(context.regime_input.nvda_return_pct - peer_mean, 4)
        correlation = round(max(-1.0, min(1.0, 1.0 - abs(residual))), 4)
        coherence_flag = "divergent" if abs(residual) >= 0.75 else "coherent"
        return PeerDivergenceContractOutput(
            canonical_id="archive-module-014",
            canonical_slug="peer_divergence",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["peer_equities", "spot_prices"],
                proxied={
                    "peer_equities": "proxied from existing NQ, ES, and SOX regime inputs",
                    "spot_prices": "proxied from NVDA return already present in MarketRegimeContextInput",
                },
            ),
            contract_notes=[
                "Peer-equity granularity remains fenced; this contract uses current cross-asset proxies only."
            ],
            coherence_flag=coherence_flag,
            correlation=correlation,
            signal_score=round(min(1.0, abs(residual) / 2.0), 4),
            peer_basis=["nq_return_pct", "es_return_pct", "sox_return_pct"],
        )

    def _gamma_pressure(self, context: TrancheAUpstreamContext) -> GammaPressureContractOutput:
        signal_score = round(min(1.0, abs(context.options_flow_input.gamma_pressure_score)), 4)
        return GammaPressureContractOutput(
            canonical_id="archive-module-011",
            canonical_slug="gamma_pressure",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["options_chain", "options_metadata", "spot_prices"],
                proxied={
                    "spot_prices": "proxied from OptionsFlowContextInput.spot_price",
                    "options_chain": "proxied from existing gamma_pressure_score and nearby options-context state",
                },
            ),
            contract_notes=[
                "Full chain and metadata remain fenced; the contract relies on the existing gamma-pressure runtime surface."
            ],
            signal_score=signal_score,
            tag=context.options_flow.dealer_pressure_state,
            zone_gamma=context.options_flow.gamma_state.value,
        )

    def _iv_vs_rv_analysis(self, context: TrancheAUpstreamContext) -> IvVsRvAnalysisContractOutput:
        rv = context.options_flow_input.front_realised_vol
        iv = context.options_flow_input.front_atm_iv
        ratio = round(iv / rv, 4) if rv > 0 else None
        anomaly = ratio is not None and ratio >= 1.2
        return IvVsRvAnalysisContractOutput(
            canonical_id="archive-module-010",
            canonical_slug="iv_vs_rv_analysis",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["options_chain", "rv_metrics"],
                satisfied={"rv_metrics"},
                proxied={
                    "options_chain": "proxied from existing ATM-IV inputs already passed into OptionsFlowContextInput",
                },
            ),
            contract_notes=[
                "The contract uses current ATM-IV and realised-volatility inputs rather than a fresh live chain pull."
            ],
            anomaly_flag=anomaly,
            ivrv_ratio=ratio,
            signal_score=round(min(1.0, abs((ratio or 1.0) - 1.0)), 4),
        )

    def _skew_inflection(self, context: TrancheAUpstreamContext) -> SkewInflectionContractOutput:
        snapshots = context.options_flow_input.repeated_snapshot_sequence
        skew_change = None
        if len(snapshots) >= 2:
            skew_change = round(snapshots[-1].put_call_skew - snapshots[0].put_call_skew, 4)
        if skew_change is None:
            inflection_tag = "single_snapshot_only"
            signal_score = 0.0
        elif skew_change >= 0.08:
            inflection_tag = "downside_skew_accelerating"
            signal_score = round(min(1.0, abs(skew_change) * 4.0), 4)
        elif skew_change <= -0.08:
            inflection_tag = "skew_relaxing"
            signal_score = round(min(1.0, abs(skew_change) * 4.0), 4)
        else:
            inflection_tag = "skew_stable"
            signal_score = round(min(1.0, abs(skew_change) * 4.0), 4)
        return SkewInflectionContractOutput(
            canonical_id="archive-module-016",
            canonical_slug="skew_inflection",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["options_chain"],
                proxied={
                    "options_chain": "proxied from repeated put_call_skew snapshots already carried by OptionsFlowContextInput"
                },
            ),
            contract_notes=[
                "Skew inflection is reconstructed from existing repeated snapshots; a full live chain still remains out of scope."
            ],
            inflection_tag=inflection_tag,
            signal_score=signal_score,
            skew_change=skew_change,
        )


class TrancheASelectorContractService:
    """Import tranche-A posture and eligibility selectors as typed contracts."""

    def evaluate(self, context: TrancheASelectorContext) -> list[TrancheAContractEmission]:
        """Emit the six posture and eligibility selectors in grammar order."""

        outputs: list[TrancheAImportedPayload] = [
            self._signal_conflict_detector(context),
            self._model_confidence_scorer(context),
            self._conviction_tier_allocator(context),
            self._entry_gate(context),
            self._ladder_constructor(context),
            self._archetype_matcher(context),
        ]
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
        output: TrancheAImportedPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> TrancheAContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::tranche_a::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="TrancheASelectorContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::tranche_a::{emitted_at.isoformat()}",
            run_id=f"run::tranche_a::{emitted_at.isoformat()}",
            module_instance_id=f"tranche_a::{output.canonical_slug}",
            registry_version="tranche_a_v1",
            environment_tag="research",
        )
        return TrancheAContractEmission(output=output, packet=packet)

    def _signal_conflict_detector(
        self, context: TrancheASelectorContext
    ) -> SignalConflictDetectorContractOutput:
        conflicts: list[str] = []
        if context.regime.signal_conflict_state != "aligned_regime":
            conflicts.append("regime_signal_conflict")
        if context.posture.signal_conflict_state != "aligned_signals":
            conflicts.append("posture_signal_conflict")
        if (
            context.options_flow.gamma_state.value == "destabilising"
            and context.posture.permission_state.value != "block"
        ):
            conflicts.append("destabilising_gamma_under_open_permission")
        return SignalConflictDetectorContractOutput(
            canonical_id="archive-evaluator-eval02",
            canonical_slug="signal_conflict_detector",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["execution_decisions", "signal_outputs"],
                proxied={
                    "signal_outputs": "proxied from existing regime/options/posture outputs",
                },
            ),
            contract_notes=[
                "Execution decisions remain partially fenced until the selector is bound into a richer decision trace."
            ],
            signal_conflicts=conflicts,
            conflict_score=round(min(1.0, len(conflicts) / 3.0), 4),
            conflict_state="aligned" if not conflicts else "conflicted",
        )

    def _model_confidence_scorer(
        self, context: TrancheASelectorContext
    ) -> ModelConfidenceScorerContractOutput:
        signal_bonus = 0.15 if context.regime.signal_conflict_state == "aligned_regime" else 0.0
        gamma_penalty = 0.25 if context.options_flow.gamma_state.value == "destabilising" else 0.0
        permission_bonus = 0.20 if context.posture.permission_state.value == "allow" else 0.05
        confidence = round(
            max(0.0, min(1.0, 0.45 + signal_bonus + permission_bonus - gamma_penalty)),
            4,
        )
        band = "high" if confidence >= 0.75 else "medium" if confidence >= 0.5 else "low"
        return ModelConfidenceScorerContractOutput(
            canonical_id="archive-module-051",
            canonical_slug="model_confidence_scorer",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["engine_score", "signal_conflicts"],
                proxied={
                    "signal_conflicts": "derived from the imported signal_conflict_detector contract",
                },
            ),
            contract_notes=[
                "Engine score remains fenced; confidence uses current stage outputs plus explicit conflict state."
            ],
            model_confidence=confidence,
            confidence_band=band,
        )

    def _conviction_tier_allocator(
        self, context: TrancheASelectorContext
    ) -> ConvictionTierAllocatorContractOutput:
        score = (
            0.65
            if context.posture.permission_state.value == "allow"
            else 0.45 if context.posture.permission_state.value == "derisk" else 0.1
        )
        if context.regime.volatility_regime.value == "stressed":
            score -= 0.2
        if context.options_flow.options_behavior_cluster == "compression_breakout_ready":
            score += 0.1
        score = round(max(0.0, min(1.0, score)), 4)
        tier = "tier_1" if score >= 0.75 else "tier_2" if score >= 0.5 else "tier_3"
        return ConvictionTierAllocatorContractOutput(
            canonical_id="archive-module-043",
            canonical_slug="conviction_tier_allocator",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["engine_score", "macro_signal_score"],
                proxied={
                    "engine_score": "proxied from current permission, volatility, and options cluster surfaces"
                },
            ),
            contract_notes=[
                "Macro signal score remains fenced; conviction is advisory only inside tranche A."
            ],
            conviction_tier=tier,
            conviction_score=score,
        )

    def _entry_gate(self, context: TrancheASelectorContext) -> EntryGateContractOutput:
        entry_allowed = context.posture.permission_state.value == "allow"
        suppression_tag = "clear" if entry_allowed else "permission_blocked"
        if context.temporal.event_window_state not in {"clear_window", "event_clear"}:
            entry_allowed = False
            suppression_tag = "event_window_veto"
        if context.posture.permission_state.value == "derisk" and suppression_tag == "clear":
            suppression_tag = "derisk_only"
        confidence = 0.75 if entry_allowed else 0.25 if suppression_tag == "derisk_only" else 0.0
        return EntryGateContractOutput(
            canonical_id="archive-module-023",
            canonical_slug="entry_gate",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["engine_score", "macro_signal_score"],
                proxied={
                    "engine_score": "proxied from current posture permission and temporal veto surfaces"
                },
            ),
            contract_notes=["Entry gate remains advisory until a richer score stack exists."],
            entry_allowed=entry_allowed,
            entry_confidence=confidence,
            suppression_tag=suppression_tag,
        )

    def _ladder_constructor(
        self, context: TrancheASelectorContext
    ) -> LadderConstructorContractOutput:
        if context.posture.permission_state.value == "block":
            return LadderConstructorContractOutput(
                canonical_id="archive-module-024",
                canonical_slug="ladder_constructor",
                grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
                computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
                dependency_fences=_dependency_fences(
                    ["options_metadata", "spot_prices"],
                    proxied={
                        "spot_prices": "proxied from current options-flow spot price and pin-distance surfaces",
                    },
                ),
                contract_notes=[
                    "No ladder is proposed while permission is blocked; metadata dependency remains fenced."
                ],
                expiry=None,
                ladder_span=None,
                ladder_strikes=[],
                constructor_state="suppressed",
            )
        spot = context.options_flow.dominant_strike or 0.0
        if spot == 0.0:
            spot = 100.0
        span = round(max(1.0, abs(context.options_flow.implied_move_envelope_pct) * 0.5), 2)
        ladder = [round(spot - span, 2), round(spot, 2), round(spot + span, 2)]
        return LadderConstructorContractOutput(
            canonical_id="archive-module-024",
            canonical_slug="ladder_constructor",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["options_metadata", "spot_prices"],
                proxied={
                    "spot_prices": "proxied from current options-flow spot and strike-cluster surfaces",
                },
            ),
            contract_notes=[
                "Metadata remains fenced; ladder levels are advisory and derived from the current implied-move envelope."
            ],
            expiry=None,
            ladder_span=span,
            ladder_strikes=ladder,
            constructor_state="advisory_ladder_ready",
        )

    def _archetype_matcher(
        self, context: TrancheASelectorContext
    ) -> ArchetypeMatcherContractOutput:
        cluster = context.options_flow.options_behavior_cluster
        pattern_tag = cluster
        matched_playbook: str | None
        if cluster == "pin_reversion_ready":
            matched_playbook = "pin_reversion"
        elif cluster == "negative_gamma_flush":
            matched_playbook = "negative_gamma_flush"
        elif cluster == "compression_breakout_ready":
            matched_playbook = "compression_breakout"
        elif context.posture.permission_state.value == "allow":
            matched_playbook = "continuation_ladder"
            pattern_tag = "continuation_ramp"
        else:
            matched_playbook = None
        score = 0.9 if matched_playbook is not None else 0.35
        return ArchetypeMatcherContractOutput(
            canonical_id="archive-module-020",
            canonical_slug="archetype_matcher",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["optional_context_signals", "spot_prices"],
                proxied={
                    "spot_prices": "proxied from current options-flow spot and pattern surfaces"
                },
            ),
            contract_notes=[
                "Optional context signals remain fenced; this archetype match only reflects the current deterministic runtime surface."
            ],
            pattern_tag=pattern_tag,
            signal_score=score,
            matched_playbook=matched_playbook,
        )
