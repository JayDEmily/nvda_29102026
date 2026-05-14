"""Gate 20 posture and eligibility enricher contract services."""

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
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    ArchetypeTaggerContractOutput,
    CompressionRegimeDetectorContractOutput,
    FillBiasAdjusterContractOutput,
    ObvViFlowConfirmationContractOutput,
    PostureEnricherContext,
    PostureEnricherPayload,
    TailHedgeInjectorContractOutput,
    VolatilitySentimentIndexContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class PostureEnricherContractEmission:
    """One typed posture-enricher contract output plus its DMP packets."""

    output: PostureEnricherPayload
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


class PostureEnricherContractService:
    """Emit Gate-20 enrichers in frozen order."""

    def evaluate(self, context: PostureEnricherContext) -> list[PostureEnricherContractEmission]:
        outputs: list[PostureEnricherPayload] = [
            self._fill_bias_adjuster(context),
            self._archetype_tagger(context),
            self._compression_regime_detector(context),
            self._obv_vi_flow_confirmation(context),
            self._tail_hedge_injector(context),
            self._volatility_sentiment_index(context),
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
        output: PostureEnricherPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> PostureEnricherContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::posture_enrichers::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="PostureEnricherContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::posture_enrichers::{emitted_at.isoformat()}",
            run_id=f"run::posture_enrichers::{emitted_at.isoformat()}",
            module_instance_id=f"posture_enrichers::{output.canonical_slug}",
            registry_version="posture_enrichers_v1",
            environment_tag="research",
        )
        return PostureEnricherContractEmission(output=output, packet=packet)

    def _fill_bias_adjuster(
        self, context: PostureEnricherContext
    ) -> FillBiasAdjusterContractOutput:
        base = (
            context.execution_context_score.context_score
            * context.macro_adaptive_weighting_filter.weight_multiplier
        )
        if context.posture.permission_state.value == "block":
            base *= 0.25
            bias_tag = "do_not_work_orders"
            fill_bias = "stand_down"
        elif context.posture.permission_state.value == "derisk":
            base *= 0.6
            bias_tag = "lean_passive_reduction"
            fill_bias = "reduce_only"
        else:
            bias_tag = "lean_passive_bid"
            fill_bias = "passive_improve"
        adjustment_score = round(max(0.0, min(1.0, base)), 4)
        return FillBiasAdjusterContractOutput(
            canonical_id="archive-module-026",
            canonical_slug="fill_bias_adjuster",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:execution_context_score",
                    "context_scanner:macro_adaptive_weighting_filter",
                    "context_scanner:engine_score",
                    "runtime:posture_risk",
                ],
                satisfied={
                    "context_scanner:execution_context_score",
                    "context_scanner:macro_adaptive_weighting_filter",
                    "context_scanner:engine_score",
                },
                proxied={
                    "runtime:posture_risk": "proxied from the current posture permission and inventory-action-bias surface rather than a live execution router",
                },
            ),
            upstream_contract_slugs=[
                "execution_context_score",
                "macro_adaptive_weighting_filter",
                "engine_score",
            ],
            contract_notes=[
                "This enricher remains advisory-only; it shapes suggested fill bias without routing or placing orders.",
            ],
            bias_tag=bias_tag,
            adjustment_score=adjustment_score,
            fill_bias=fill_bias,
        )

    def _archetype_tagger(self, context: PostureEnricherContext) -> ArchetypeTaggerContractOutput:
        if (
            context.engine_score.conviction_band == "constructive"
            and context.temporal.desk_window in {"trend_window", "late_session"}
        ):
            archetype_tag = "trend_constructive"
            confidence = 0.78
        elif context.posture.permission_state.value == "block":
            archetype_tag = "defensive_stress"
            confidence = 0.82
        else:
            archetype_tag = "balanced_rotation"
            confidence = 0.56
        return ArchetypeTaggerContractOutput(
            canonical_id="archive-module-048",
            canonical_slug="archetype_tagger",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:engine_score",
                    "context_scanner:options_behaviour_cluster",
                    "runtime:temporal_context",
                ],
                satisfied={
                    "context_scanner:engine_score",
                    "context_scanner:options_behaviour_cluster",
                },
                proxied={
                    "runtime:temporal_context": "proxied from the current desk-window classification rather than a separate archetype history engine",
                },
            ),
            upstream_contract_slugs=["engine_score", "options_behaviour_cluster"],
            contract_notes=[
                "Archetype tagging stays descriptive and advisory; it does not rewrite playbook registry behaviour.",
            ],
            archetype_tag=archetype_tag,
            confidence=confidence,
        )

    def _compression_regime_detector(
        self, context: PostureEnricherContext
    ) -> CompressionRegimeDetectorContractOutput:
        if (
            context.vol_corridor.compression_flag == "tight_corridor"
            and context.execution_context_score.context_score >= 0.6
        ):
            compression_state = "compression_ready"
            signal_score = 0.82
        elif context.vol_corridor.compression_flag == "wide_corridor":
            compression_state = "compression_absent"
            signal_score = 0.18
        else:
            compression_state = "compression_mixed"
            signal_score = 0.45
        return CompressionRegimeDetectorContractOutput(
            canonical_id="legacy-module-004",
            canonical_slug="compression_regime_detector",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:vol_corridor",
                    "context_scanner:execution_context_score",
                    "context_scanner:options_behaviour_cluster",
                ],
                satisfied={
                    "context_scanner:vol_corridor",
                    "context_scanner:execution_context_score",
                    "context_scanner:options_behaviour_cluster",
                },
            ),
            upstream_contract_slugs=[
                "vol_corridor",
                "execution_context_score",
                "options_behaviour_cluster",
            ],
            contract_notes=[
                "Compression regime detection remains a bounded qualifier only and does not create a new playbook family.",
            ],
            compression_state=compression_state,
            signal_score=signal_score,
        )

    def _obv_vi_flow_confirmation(
        self, context: PostureEnricherContext
    ) -> ObvViFlowConfirmationContractOutput:
        return ObvViFlowConfirmationContractOutput(
            canonical_id="legacy-module-003",
            canonical_slug="obv_vi_flow_confirmation",
            grammar_role=DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            computation_mode=ContractComputationMode.FENCED_CONTRACT_ONLY,
            dependency_fences=_dependency_fences(
                [
                    "market_volume_series",
                    "intraday_obv_curve",
                    "context_scanner:engine_score",
                ],
                satisfied={"context_scanner:engine_score"},
            ),
            upstream_contract_slugs=["engine_score"],
            contract_notes=[
                "OBV and volume-intensity confirmation remain fenced because the deterministic runtime still lacks the raw market-volume tape needed to compute them honestly.",
            ],
            confirmation_state="dependency_fenced",
            confirmation_score=0.0,
        )

    def _tail_hedge_injector(
        self, context: PostureEnricherContext
    ) -> TailHedgeInjectorContractOutput:
        hostile_pressure = fmean(
            [
                1.0 - context.macro_signal_score.macro_score,
                context.vix_spread_detector.signal_score,
                1.0 - context.engine_score.engine_score,
            ]
        )
        if context.posture.permission_state.value == "block" or hostile_pressure >= 0.7:
            hedge_overlay_tag = "deploy_tail_hedge"
            hedge_ratio = 0.25
            injector_state = "hedge_advised"
        elif hostile_pressure >= 0.45:
            hedge_overlay_tag = "monitor_tail_risk"
            hedge_ratio = 0.1
            injector_state = "hedge_watch"
        else:
            hedge_overlay_tag = "no_tail_hedge_needed"
            hedge_ratio = 0.0
            injector_state = "hedge_clear"
        return TailHedgeInjectorContractOutput(
            canonical_id="archive-module-049",
            canonical_slug="tail_hedge_injector",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:macro_signal_score",
                    "context_scanner:vix_spread_detector",
                    "context_scanner:engine_score",
                    "runtime:posture_risk",
                ],
                satisfied={
                    "context_scanner:macro_signal_score",
                    "context_scanner:vix_spread_detector",
                    "context_scanner:engine_score",
                },
                proxied={
                    "runtime:posture_risk": "proxied from the current permission state so the overlay stays advisory rather than becoming an automated hedge engine",
                },
            ),
            upstream_contract_slugs=[
                "macro_signal_score",
                "vix_spread_detector",
                "engine_score",
            ],
            contract_notes=[
                "Tail hedge injection remains advisory-only; it suggests overlay intensity without placing hedges or mutating live positions.",
            ],
            hedge_overlay_tag=hedge_overlay_tag,
            hedge_ratio=hedge_ratio,
            injector_state=injector_state,
        )

    def _volatility_sentiment_index(
        self, context: PostureEnricherContext
    ) -> VolatilitySentimentIndexContractOutput:
        supportive = fmean(
            [
                context.macro_signal_score.macro_score,
                1.0 - context.vix_spread_detector.signal_score,
                context.engine_score.engine_score,
            ]
        )
        sentiment_index = round(max(0.0, min(1.0, supportive)), 4)
        if sentiment_index >= 0.65:
            sentiment_state = "supportive_volatility_sentiment"
        elif sentiment_index <= 0.35:
            sentiment_state = "hostile_volatility_sentiment"
        else:
            sentiment_state = "mixed_volatility_sentiment"
        return VolatilitySentimentIndexContractOutput(
            canonical_id="legacy-module-002",
            canonical_slug="volatility_sentiment_index",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                [
                    "context_scanner:macro_signal_score",
                    "context_scanner:vix_spread_detector",
                    "context_scanner:options_behaviour_cluster",
                    "context_scanner:engine_score",
                ],
                satisfied={
                    "context_scanner:macro_signal_score",
                    "context_scanner:vix_spread_detector",
                    "context_scanner:options_behaviour_cluster",
                    "context_scanner:engine_score",
                },
            ),
            upstream_contract_slugs=[
                "macro_signal_score",
                "vix_spread_detector",
                "options_behaviour_cluster",
                "engine_score",
            ],
            contract_notes=[
                "Volatility sentiment is preserved as an advisory posture overlay only; it does not alter the live posture service directly.",
            ],
            sentiment_index=sentiment_index,
            sentiment_state=sentiment_state,
        )
