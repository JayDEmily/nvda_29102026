"""Gate 23 review, P&L, attribution, and variant-tracking contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.review_attribution import (
    ConfidenceDivergenceLoggerContractOutput,
    DailySummaryContractOutput,
    FeedbackSummaryWriterContractOutput,
    MacroAlignmentCheckerContractOutput,
    ModuleScoreAttributorContractOutput,
    ModuleTraceAttributionContractOutput,
    ProfitLossLedgerContractOutput,
    ReviewAttributionContext,
    ReviewAttributionPayload,
    VariantPerformanceTrackerContractOutput,
    VariantTraceLoggerContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class ReviewAttributionContractEmission:
    """One typed Gate-23 review-chain contract output plus its DMP packets."""

    output: ReviewAttributionPayload
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


class ReviewAttributionContractService:
    """Emit Gate-23 review-chain contracts in frozen order."""

    def evaluate(
        self, context: ReviewAttributionContext
    ) -> list[ReviewAttributionContractEmission]:
        profit_loss_ledger = self._profit_loss_ledger(context)
        module_trace_attribution = self._module_trace_attribution(context, profit_loss_ledger)
        daily_summary = self._daily_summary(context, profit_loss_ledger)
        feedback_summary = self._feedback_summary_writer(context, profit_loss_ledger)
        module_scores = self._module_score_attributor(context, profit_loss_ledger)
        variant_trace = self._variant_trace_logger(context)
        variant_performance = self._variant_performance_tracker(context, profit_loss_ledger)
        confidence_divergence = self._confidence_divergence_logger(context, profit_loss_ledger)
        macro_alignment = self._macro_alignment_checker(context)
        outputs: list[ReviewAttributionPayload] = [
            profit_loss_ledger,
            module_trace_attribution,
            daily_summary,
            feedback_summary,
            module_scores,
            variant_trace,
            variant_performance,
            confidence_divergence,
            macro_alignment,
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
        output: ReviewAttributionPayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> ReviewAttributionContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::review_attribution::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="ReviewAttributionContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::review_attribution::{emitted_at.isoformat()}",
            run_id=f"run::review_attribution::{emitted_at.isoformat()}",
            module_instance_id=f"review_attribution::{output.canonical_slug}",
            registry_version="review_attribution_v1",
            environment_tag="research",
        )
        return ReviewAttributionContractEmission(output=output, packet=packet)

    def _profit_loss_ledger(
        self, context: ReviewAttributionContext
    ) -> ProfitLossLedgerContractOutput:
        realized = round(0.35 if context.execution.active_playbook_ids else 0.0, 4)
        if context.trade_logger.trade_log_state != "preview_trade_log_ready":
            realized = 0.0
        return ProfitLossLedgerContractOutput(
            canonical_id="archive-module-039",
            canonical_slug="profit_loss_ledger",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["closed_positions"],
                proxied={
                    "closed_positions": "proxied from the advisory trade-log surface and current mark-to-market preview"
                },
            ),
            upstream_contract_slugs=[
                "unrealized_tracker",
                "trade_logger",
                "position_book",
            ],
            contract_notes=[
                "P&L remains a deterministic preview ledger rather than a booked statement."
            ],
            realized_pnl_pct=realized,
            unrealized_pnl_pct=context.unrealized_tracker.unrealized_pnl_pct,
            gross_exposure_pct=context.position_book.live_position_pct,
            ledger_state=(
                "preview_pnl_ready" if context.position_book.live_position_pct > 0.0 else "flat"
            ),
        )

    def _module_trace_attribution(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> ModuleTraceAttributionContractOutput:
        leading_modules = [
            "engine_score",
            "entry_planner",
            "unrealized_tracker",
        ]
        confidence = 0.8 if profit_loss_ledger.gross_exposure_pct > 0.0 else 0.35
        return ModuleTraceAttributionContractOutput(
            canonical_id="archive-module-038",
            canonical_slug="module_trace_attribution",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["execution_decisions", "signal_outputs"],
                proxied={
                    "signal_outputs": "proxied from the review packet and execution-tag surfaces"
                },
            ),
            upstream_contract_slugs=["execution_tags", "trade_logger"],
            contract_notes=[
                "Attribution stays bounded to the deterministic packet chain already present in review output."
            ],
            leading_modules=leading_modules,
            attribution_confidence=confidence,
            attribution_state=("coherent" if confidence >= 0.75 else "thin"),
        )

    def _daily_summary(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> DailySummaryContractOutput:
        headline = (
            "preview day green and orderly"
            if profit_loss_ledger.unrealized_pnl_pct >= 0.0
            else "preview day under pressure"
        )
        key_points = [
            context.review.summary,
            f"gross_exposure_pct:{profit_loss_ledger.gross_exposure_pct}",
            f"unrealized_pnl_pct:{profit_loss_ledger.unrealized_pnl_pct}",
        ]
        return DailySummaryContractOutput(
            canonical_id="archive-module-041",
            canonical_slug="daily_summary",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["profit_loss_ledger", "trade_log"],
                satisfied={"profit_loss_ledger", "trade_log"},
            ),
            upstream_contract_slugs=["profit_loss_ledger", "trade_logger"],
            contract_notes=[
                "The daily summary is an operator artefact derived only from preview execution state."
            ],
            summary_headline=headline,
            day_state=(
                "positive_preview"
                if profit_loss_ledger.unrealized_pnl_pct >= 0.0
                else "negative_preview"
            ),
            key_points=key_points,
        )

    def _feedback_summary_writer(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> FeedbackSummaryWriterContractOutput:
        grade = (
            "A"
            if profit_loss_ledger.unrealized_pnl_pct >= 0.5
            else "B" if profit_loss_ledger.unrealized_pnl_pct >= 0.0 else "C"
        )
        actions = [
            "keep preview chain deterministic",
            "inspect broker fences before widening scope",
        ]
        if context.position_book.book_state == "flat_or_locked":
            actions.append("do not force entries under permission lock")
        return FeedbackSummaryWriterContractOutput(
            canonical_id="archive-evaluator-eval06",
            canonical_slug="feedback_summary_writer",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["evaluator_outputs"],
                proxied={
                    "evaluator_outputs": "proxied from review packet, execution tags, and preview P&L state"
                },
            ),
            upstream_contract_slugs=["profit_loss_ledger", "execution_tags"],
            contract_notes=[
                "Feedback remains an operator-facing summary rather than an optimisation loop."
            ],
            feedback_grade=grade,
            feedback_actions=actions,
            summary_state="feedback_written",
        )

    def _module_score_attributor(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> ModuleScoreAttributorContractOutput:
        exposure_weight = min(1.0, profit_loss_ledger.gross_exposure_pct / 100.0)
        scores = {
            "engine_score": round(context.engine_score.engine_score, 4),
            "macro_signal_score": round(context.macro_signal_score.macro_score, 4),
            "execution_tags": round(0.45 + (0.2 * exposure_weight), 4),
            "trade_logger": round(0.4 + (0.2 * exposure_weight), 4),
        }
        return ModuleScoreAttributorContractOutput(
            canonical_id="archive-evaluator-eval01",
            canonical_slug="module_score_attributor",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["module_attribution_log", "profit_loss_ledger"],
                satisfied={"profit_loss_ledger"},
                proxied={
                    "module_attribution_log": "proxied from the deterministic review packet and execution-tag surfaces"
                },
            ),
            upstream_contract_slugs=["profit_loss_ledger", "module_trace_attribution"],
            contract_notes=[
                "Scores remain bounded to preview evidence and do not imply promotion state."
            ],
            module_scores=scores,
            score_state="scored",
        )

    def _variant_trace_logger(
        self, context: ReviewAttributionContext
    ) -> VariantTraceLoggerContractOutput:
        variant_id = f"{context.execution.entry_style}::{context.temporal.desk_window}"
        return VariantTraceLoggerContractOutput(
            canonical_id="archive-module-040",
            canonical_slug="variant_trace_logger",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["execution_outcomes", "runtime_config"],
                proxied={
                    "execution_outcomes": "proxied from the preview trade-log surface",
                    "runtime_config": "proxied from the deterministic settings surface",
                },
            ),
            upstream_contract_slugs=["trade_logger", "execution_tags"],
            contract_notes=[
                "Variant tracing remains a preview ledger keyed to the live deterministic entry style only."
            ],
            variant_id=variant_id,
            active_playbooks=list(context.execution.active_playbook_ids),
            trace_state="variant_traced",
        )

    def _variant_performance_tracker(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> VariantPerformanceTrackerContractOutput:
        performance_score = round(
            max(
                0.0,
                min(1.0, 0.5 + (profit_loss_ledger.unrealized_pnl_pct / 10.0)),
            ),
            4,
        )
        band = (
            "strong"
            if performance_score >= 0.65
            else "mixed" if performance_score >= 0.45 else "weak"
        )
        return VariantPerformanceTrackerContractOutput(
            canonical_id="archive-evaluator-eval04",
            canonical_slug="variant_performance_tracker",
            grammar_role=DmpGrammarRole.REVIEW_EXPLANATION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["profit_loss_ledger", "variant_trace"],
                satisfied={"profit_loss_ledger"},
                proxied={"variant_trace": "proxied from the deterministic variant-trace logger"},
            ),
            upstream_contract_slugs=["profit_loss_ledger", "variant_trace_logger"],
            contract_notes=["Variant performance stays descriptive and preview-only."],
            performance_score=performance_score,
            performance_band=band,
            tracker_state="variant_scored",
        )

    def _confidence_divergence_logger(
        self,
        context: ReviewAttributionContext,
        profit_loss_ledger: ProfitLossLedgerContractOutput,
    ) -> ConfidenceDivergenceLoggerContractOutput:
        if profit_loss_ledger.unrealized_pnl_pct >= 0.0:
            observed_confidence = 0.75
        elif profit_loss_ledger.unrealized_pnl_pct <= -5.0:
            observed_confidence = 0.35
        else:
            observed_confidence = 0.45
        divergence_score = round(abs(context.engine_score.engine_score - observed_confidence), 4)
        return ConfidenceDivergenceLoggerContractOutput(
            canonical_id="archive-evaluator-eval05",
            canonical_slug="confidence_divergence_logger",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["engine_score", "profit_loss_ledger"],
                satisfied={"engine_score", "profit_loss_ledger"},
            ),
            upstream_contract_slugs=["engine_score", "profit_loss_ledger"],
            contract_notes=[
                "Confidence divergence compares preview P&L with the current engine-score surface only."
            ],
            divergence_score=divergence_score,
            divergence_state=("aligned" if divergence_score <= 0.1 else "divergent"),
            compared_fields=["engine_score", "unrealized_pnl_pct"],
        )

    def _macro_alignment_checker(
        self, context: ReviewAttributionContext
    ) -> MacroAlignmentCheckerContractOutput:
        macro_flags: list[str] = []
        if context.regime.fx_stress_state != "fx_neutral":
            macro_flags.append("fx_stress")
        if context.regime.rates_regime_state == "curve_inversion_pressure":
            macro_flags.append("rates_pressure")
        if context.macro_signal_score.macro_bias == "macro_hostile":
            macro_flags.append("macro_hostile")
        alignment_score = round(max(0.0, min(1.0, 1.0 - (0.25 * len(macro_flags)))), 4)
        return MacroAlignmentCheckerContractOutput(
            canonical_id="archive-evaluator-eval03",
            canonical_slug="macro_alignment_checker",
            grammar_role=DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["macro_metrics", "trade_log"],
                proxied={
                    "macro_metrics": "proxied from the current regime and macro-signal contract surfaces"
                },
                satisfied={"trade_log"},
            ),
            upstream_contract_slugs=["macro_signal_score", "trade_logger"],
            contract_notes=[
                "Macro alignment stays descriptive and must not masquerade as a live veto beyond current posture logic."
            ],
            macro_alignment_state=("aligned" if not macro_flags else "cautious"),
            alignment_score=alignment_score,
            macro_flags=macro_flags,
        )
