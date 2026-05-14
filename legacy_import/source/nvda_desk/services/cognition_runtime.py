"""Deterministic Desk Cognition Grammar runtime orchestrator.

This service executes the binding runtime order:
1) temporal context
2) market regime context
3) options and flow context
4) posture and risk permission
5) playbook eligibility
6) expression and execution
7) review and explanation
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.db.session import create_session_factory
from nvda_desk.schemas.calibration import ParallelRiskLaneEvaluationPreparationPacket
from nvda_desk.schemas.cognition import (
    BindingStageName,
    CapitalDeploymentAuthorityDecision,
    CapitalDeploymentAuthorityInput,
    ExecutionExpressionInput,
    ExecutionExpressionOutput,
    InventoryState,
    LifecycleAction,
    MarketRegimeContextInput,
    MarketRegimeContextOutput,
    OptionsFlowContextInput,
    OptionsFlowContextOutput,
    PacketLineageSurface,
    PlaybookEligibilityInput,
    PlaybookEligibilityOutput,
    PositionContextInput,
    PostureRiskInput,
    PostureRiskOutput,
    ReviewExplanationInput,
    ReviewExplanationOutput,
    StageLocalHandoffSurface,
    TemporalContextInput,
    TemporalContextOutput,
    TradableExpressionFamily,
)
from nvda_desk.schemas.dmp import (
    CognitionStagePayload,
    DeskModulePacketV3,
    DmpBehaviourClass,
    DmpGrammarRole,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.dmp_envelope import DmpV3Envelope, build_dmp_v3_envelope_kwargs
from nvda_desk.schemas.downstream import (
    DownstreamArchitectureReceipt,
    DownstreamLiveInventorySnapshot,
    DownstreamOpeningSnapshot,
)
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    ContractComputationMode,
    ContractDependencyStatus,
    ConvictionTierAllocatorContractOutput,
    EntryGateContractOutput,
    LadderConstructorContractOutput,
    ModelConfidenceScorerContractOutput,
    SignalConflictDetectorContractOutput,
    TrancheASelectorContext,
    TrancheAUpstreamContext,
)
from nvda_desk.schemas.parallel_risk import ParallelRiskLanePacket
from nvda_desk.schemas.review import (
    ImportedModuleDependencySurface,
    ImportedModuleMaturityState,
    ImportedModuleReviewCitation,
)
from nvda_desk.services.capital_deployment_authority import CapitalDeploymentAuthorityService
from nvda_desk.services.execution_expression import ExecutionExpressionService
from nvda_desk.services.execution_records import ExecutionRecordsService
from nvda_desk.services.downstream_live_inventory import DownstreamLiveInventoryService
from nvda_desk.services.downstream_opening import DownstreamOpeningService
from nvda_desk.services.downstream_review import DownstreamReviewService
from nvda_desk.services.downstream_state import DownstreamStateService
from nvda_desk.services.imported_modules.tranche_a import (
    TrancheAContractEmission,
    TrancheASelectorContractService,
    TrancheAUpstreamContractService,
)
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.options_flow_history import (
    OptionsFlowHistoryBuilder,
    OptionsFlowHistoryStore,
    build_and_persist_options_flow_history,
)
from nvda_desk.services.parallel_risk_lane import ParallelRiskLaneService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.review_explanation import ReviewExplanationService
from nvda_desk.services.risk_gateway import RiskGatewayService
from nvda_desk.services.state_conditioned_modifier import (
    StateConditionedModifierService,
)
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.schemas.options_flow_history import (
    OptionsFlowHistoryObservationRecord,
    OptionsFlowHistoryWriteResult,
)


@dataclass(frozen=True)
class DeskCognitionRuntimeResult:
    """Structured result packet for one full desk-cognition runtime pass."""

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    review: ReviewExplanationOutput
    stage_local_handoff: StageLocalHandoffSurface
    downstream_opening_snapshot: DownstreamOpeningSnapshot
    downstream_live_inventory_snapshot: DownstreamLiveInventorySnapshot
    downstream_architecture_receipt: DownstreamArchitectureReceipt
    parallel_risk_lane: ParallelRiskLanePacket | None = None
    parallel_risk_calibration: ParallelRiskLaneEvaluationPreparationPacket | None = None
    capital_deployment_authority: CapitalDeploymentAuthorityDecision | None = None
    stage_packets: tuple[DeskModulePacketV3, ...] = ()
    packet_lineage: tuple[str, ...] = ()
    stage_packet_ids: dict[str, str] = field(default_factory=dict)
    contract_packets: tuple[DeskModulePacketV3, ...] = ()
    contract_packet_ids: dict[str, str] = field(default_factory=dict)
    options_flow_history_observation: OptionsFlowHistoryObservationRecord | None = None
    options_flow_history_write_result: OptionsFlowHistoryWriteResult | None = None


class DeskCognitionRuntime:
    """Execute the deterministic Desk Cognition Grammar for one snapshot."""

    _STAGE_SPECS: tuple[tuple[BindingStageName, DmpGrammarRole, str, str], ...] = (
        (
            BindingStageName.TEMPORAL,
            DmpGrammarRole.TEMPORAL_CONTEXT,
            "TemporalContextInput",
            "TemporalContextOutput",
        ),
        (
            BindingStageName.REGIME,
            DmpGrammarRole.MARKET_REGIME_CONTEXT,
            "MarketRegimeContextInput",
            "MarketRegimeContextOutput",
        ),
        (
            BindingStageName.OPTIONS_FLOW,
            DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
            "OptionsFlowContextInput",
            "OptionsFlowContextOutput",
        ),
        (
            BindingStageName.POSTURE,
            DmpGrammarRole.POSTURE_RISK_PERMISSION,
            "PostureRiskInput",
            "PostureRiskOutput",
        ),
        (
            BindingStageName.ELIGIBILITY,
            DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
            "PlaybookEligibilityInput",
            "PlaybookEligibilityOutput",
        ),
        (
            BindingStageName.EXECUTION,
            DmpGrammarRole.EXPRESSION_EXECUTION,
            "ExecutionExpressionInput",
            "ExecutionExpressionOutput",
        ),
        (
            BindingStageName.REVIEW,
            DmpGrammarRole.REVIEW_EXPLANATION,
            "ReviewExplanationInput",
            "ReviewExplanationOutput",
        ),
    )

    def __init__(self, settings: Settings):
        self._temporal = TemporalContextService(settings)
        self._regime = MarketRegimeContextService()
        self._options_flow = OptionsFlowContextService()
        self._parallel_risk_lane = ParallelRiskLaneService()
        self._posture = PostureRiskService()
        self._eligibility = PlaybookEligibilityService()
        self._execution = ExecutionExpressionService()
        self._session_factory = create_session_factory(settings.database_url)
        self._execution_records = ExecutionRecordsService(self._session_factory)
        self._capital_deployment_authority = CapitalDeploymentAuthorityService()
        self._downstream_opening = DownstreamOpeningService()
        self._downstream_live_inventory = DownstreamLiveInventoryService()
        self._downstream_review = DownstreamReviewService()
        self._downstream_state = DownstreamStateService(self._execution_records)
        self._review = ReviewExplanationService()
        self._risk_gateway = RiskGatewayService()
        self._modifiers = StateConditionedModifierService()
        self._tranche_a_upstream = TrancheAUpstreamContractService()
        self._tranche_a_selector = TrancheASelectorContractService()
        self._settings = settings
        self._options_flow_history_builder = OptionsFlowHistoryBuilder(self._session_factory)
        self._options_flow_history_store = OptionsFlowHistoryStore(self._session_factory)

    def _imported_module_maturity(
        self,
        emission: TrancheAContractEmission,
    ) -> ImportedModuleMaturityState:
        if emission.output.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY:
            return ImportedModuleMaturityState.CONCEPT_CONTRACT_ONLY
        if any(
            fence.status is ContractDependencyStatus.FENCED_MISSING_SOURCE
            for fence in emission.output.dependency_fences
        ):
            return ImportedModuleMaturityState.CONCEPT_CONTRACT_ONLY
        return ImportedModuleMaturityState.IMPLEMENTED_RUNTIME_PROXY

    def _build_imported_module_citations(
        self,
        emissions: tuple[TrancheAContractEmission, ...],
    ) -> tuple[list[ImportedModuleReviewCitation], dict[str, int]]:
        citations = [
            ImportedModuleReviewCitation(
                canonical_id=emission.output.canonical_id,
                canonical_slug=emission.output.canonical_slug,
                packet_id=emission.packet.packet_id,
                grammar_role=emission.output.grammar_role,
                computation_mode=emission.output.computation_mode.value,
                maturity_state=self._imported_module_maturity(emission),
                dependency_fences=[
                    ImportedModuleDependencySurface(
                        dependency=fence.dependency,
                        status=fence.status.value,
                        note=fence.note,
                    )
                    for fence in emission.output.dependency_fences
                ],
                contract_notes=emission.output.contract_notes,
            )
            for emission in emissions
        ]
        maturity_counts = dict(
            sorted(Counter(citation.maturity_state.value for citation in citations).items())
        )
        return citations, maturity_counts

    def run(
        self,
        *,
        temporal_input: TemporalContextInput,
        regime_input: MarketRegimeContextInput,
        options_flow_input: OptionsFlowContextInput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        capital_state_snapshot: CapitalStateSnapshotPayload | None = None,
        stack_id: str | None = None,
        coefficient_set_id: str | None = None,
        symbol: str = "NVDA",
    ) -> DeskCognitionRuntimeResult:
        """Run the full deterministic desk-cognition runtime for one snapshot."""

        temporal = self._temporal.evaluate(temporal_input)
        regime = self._regime.evaluate(regime_input)
        options_flow = self._options_flow.evaluate(options_flow_input)
        options_flow_history_observation = None
        options_flow_history_write_result = None
        if self._settings.options_flow_history_lane_enabled:
            try:
                options_flow_history_write_result = build_and_persist_options_flow_history(
                    builder=self._options_flow_history_builder,
                    store=self._options_flow_history_store,
                    symbol=symbol,
                    observed_at=temporal_input.ts,
                    options_flow_input=options_flow_input,
                    options_flow_output=options_flow,
                )
                if options_flow_history_write_result.persisted is not None:
                    options_flow_history_observation = options_flow_history_write_result.persisted.record
            except Exception as exc:
                options_flow_history_write_result = OptionsFlowHistoryWriteResult(
                    status="write_failed", note=str(exc)
                )
        stage_packet_ids = {
            stage_name.value: self._packet_id(
                emitted_at=temporal_input.ts,
                stage_name=stage_name,
                stack_id=stack_id,
                coefficient_set_id=coefficient_set_id,
            )
            for stage_name, _, _, _ in self._STAGE_SPECS
        }
        trace_id, run_id = self._runtime_trace_ids(
            emitted_at=temporal_input.ts,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets: dict[BindingStageName, DeskModulePacketV3] = {}
        upstream_packet_ids: list[str] = []
        temporal_input_packet = self._build_parallel_risk_temporal_input_packet(
            emitted_at=temporal_input.ts,
            temporal_input=temporal_input,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        temporal_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.TEMPORAL,
            stage_output=temporal,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.TEMPORAL] = temporal_packet
        upstream_packet_ids.append(temporal_packet.packet_id)
        regime_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.REGIME,
            stage_output=regime,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.REGIME] = regime_packet
        upstream_packet_ids.append(regime_packet.packet_id)
        options_flow_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.OPTIONS_FLOW,
            stage_output=options_flow,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.OPTIONS_FLOW] = options_flow_packet
        upstream_packet_ids.append(options_flow_packet.packet_id)
        parallel_risk_lane = self._parallel_risk_lane.evaluate(
            temporal_input_packet=temporal_input_packet,
            temporal_packet=temporal_packet,
        )
        parallel_risk_lane = self._parallel_risk_lane.enrich_market_translation(
            packet=parallel_risk_lane,
            regime_packet=regime_packet,
            options_flow_packet=options_flow_packet,
        )
        upstream_contract_emissions = self._tranche_a_upstream.evaluate(
            TrancheAUpstreamContext(
                emitted_at=temporal_input.ts,
                temporal_input=temporal_input,
                regime_input=regime_input,
                options_flow_input=options_flow_input,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                stack_id=stack_id,
                coefficient_set_id=coefficient_set_id,
            )
        )
        posture = self._posture.evaluate(
            PostureRiskInput(
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                inventory=inventory_state,
                risk_budget_remaining_pct=risk_budget_remaining_pct,
            )
        )
        selector_contract_emissions = self._tranche_a_selector.evaluate(
            TrancheASelectorContext(
                emitted_at=temporal_input.ts,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                stack_id=stack_id,
                coefficient_set_id=coefficient_set_id,
            )
        )
        posture = self._posture_with_contract_citations(posture, selector_contract_emissions)
        cited_posture_pre_modifier = posture
        modifier_runtime_packet = self._modifiers.evaluate(
            temporal_input=temporal_input,
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
        posture = self._modifiers.apply_to_posture(posture, modifier_runtime_packet)
        posture_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.POSTURE,
            stage_output=posture,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.POSTURE] = posture_packet
        upstream_packet_ids.append(posture_packet.packet_id)
        eligibility = self._eligibility.evaluate(
            PlaybookEligibilityInput(
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
            )
        )
        eligibility = self._eligibility_with_contract_citations(
            eligibility, selector_contract_emissions
        )
        cited_eligibility = eligibility
        eligibility_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.ELIGIBILITY,
            stage_output=eligibility,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.ELIGIBILITY] = eligibility_packet
        upstream_packet_ids.append(eligibility_packet.packet_id)
        execution = self._execution.evaluate(
            ExecutionExpressionInput(
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                eligibility=eligibility,
                modifier_runtime_packet=modifier_runtime_packet,
                parallel_risk_lane_packet=parallel_risk_lane,
                position_context=self._build_execution_position_context(
                    temporal=temporal,
                    posture=posture,
                    inventory_state=inventory_state,
                    eligibility=eligibility,
                ),
            )
        )
        execution_pre_modifier = execution
        execution = self._modifiers.apply_to_execution(execution, modifier_runtime_packet)
        execution_post_modifier_pre_final_risk = execution
        execution_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.EXECUTION,
            stage_output=execution_post_modifier_pre_final_risk,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.EXECUTION] = execution_packet
        upstream_packet_ids.append(execution_packet.packet_id)
        overlay_risk_decision = self._risk_gateway.evaluate_overlay(
            requested_at=temporal_input.ts,
            temporal_input=temporal_input,
            temporal=temporal,
            regime_input=regime_input,
            options_flow_input=options_flow_input,
            posture=posture,
            execution=execution,
            inventory_state=inventory_state,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
        )
        terminal_risk_application = self._risk_gateway.build_terminal_risk_application(
            overlay_decision=overlay_risk_decision,
            posture=posture,
        )
        final_risk_decision = terminal_risk_application.final_decision
        parallel_risk_lane = self._parallel_risk_lane.enrich_candidate_semantics(
            packet=parallel_risk_lane,
            posture_packet=posture_packet,
            eligibility_packet=eligibility_packet,
            execution_packet=execution_packet,
        )
        parallel_risk_calibration = self._parallel_risk_lane.build_evaluation_preparation_packet(
            packet=parallel_risk_lane,
        )
        posture = posture.model_copy(update={"parallel_risk_lane_packet": parallel_risk_lane})
        execution = execution.model_copy(update={"parallel_risk_lane_packet": parallel_risk_lane})
        stage_local_handoff = StageLocalHandoffSurface(
            cited_posture_pre_modifier=cited_posture_pre_modifier,
            cited_eligibility=cited_eligibility,
            execution_pre_modifier=execution_pre_modifier,
            execution_post_modifier_pre_final_risk=execution_post_modifier_pre_final_risk,
            overlay_risk_decision=overlay_risk_decision,
            terminal_risk_application=terminal_risk_application,
            terminal_risk_decision=final_risk_decision,
            notes=[
                "additive_preserved_handoff_only",
                "terminal_behavior_unchanged_in_gate_143",
            ],
        )
        execution = self._risk_gateway.apply_final_join(execution, final_risk_decision)
        capital_deployment_authority = None
        if capital_state_snapshot is not None:
            capital_deployment_authority = self._capital_deployment_authority.evaluate(
                CapitalDeploymentAuthorityInput(
                    posture=posture,
                    eligibility=eligibility,
                    execution=execution_post_modifier_pre_final_risk,
                    stage_local_handoff=stage_local_handoff,
                    parallel_risk_lane_packet=parallel_risk_lane,
                    capital_state=capital_state_snapshot,
                )
            )
        try:
            downstream_state_result = self._downstream_state.read(symbol=symbol)
        except Exception as error:
            downstream_state_result = self._downstream_state.degraded(error=error)
        downstream_opening_snapshot = self._downstream_opening.build_snapshot(
            execution=execution_post_modifier_pre_final_risk,
            stage_local_handoff=stage_local_handoff,
            parallel_risk_lane_packet=parallel_risk_lane,
            capital_deployment_authority=capital_deployment_authority,
            state_read_result=downstream_state_result,
        )
        downstream_live_inventory_snapshot = self._downstream_live_inventory.build_snapshot(
            state_read_result=downstream_state_result,
        )
        downstream_architecture_receipt = self._downstream_review.build_receipt(
            opening_snapshot=downstream_opening_snapshot,
            live_inventory_snapshot=downstream_live_inventory_snapshot,
        )
        review = self._review.evaluate(
            ReviewExplanationInput(
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                eligibility=eligibility,
                execution=execution,
                modifier_runtime_packet=modifier_runtime_packet,
                parallel_risk_lane_packet=parallel_risk_lane,
                stage_local_handoff=stage_local_handoff,
                capital_deployment_authority=capital_deployment_authority,
                downstream_architecture_receipt=downstream_architecture_receipt,
                temporal_input=temporal_input,
            )
        )
        packet_lineage = tuple(
            stage_packet_ids[stage_name.value] for stage_name, _, _, _ in self._STAGE_SPECS
        )
        review_packet_id = stage_packet_ids[BindingStageName.REVIEW.value]
        decision_packet_id = stage_packet_ids[BindingStageName.EXECUTION.value]
        review_lineage = PacketLineageSurface(
            review_packet_id=review_packet_id,
            decision_packet_id=decision_packet_id,
            packet_lineage=list(packet_lineage),
            stage_packet_ids=stage_packet_ids,
        )
        imported_module_citations, imported_module_maturity_counts = (
            self._build_imported_module_citations(
                tuple((*upstream_contract_emissions, *selector_contract_emissions))
            )
        )
        review = review.model_copy(
            update={
                "packet_lineage": review_lineage,
                "imported_module_citations": imported_module_citations,
                "imported_module_maturity_counts": imported_module_maturity_counts,
                "review_packet": {
                    **review.review_packet,
                    "packet_lineage": review_lineage.model_dump(mode="json"),
                    "dmp_lineage": review_lineage.model_dump(mode="json"),
                    "imported_module_citations": [
                        citation.model_dump(mode="json") for citation in imported_module_citations
                    ],
                    "imported_module_maturity_counts": imported_module_maturity_counts,
                },
            }
        )
        review_packet = self._build_stage_packet(
            emitted_at=temporal_input.ts,
            stage_name=BindingStageName.REVIEW,
            stage_output=review,
            stage_packet_ids=stage_packet_ids,
            upstream_packet_ids=upstream_packet_ids,
            trace_id=trace_id,
            run_id=run_id,
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
        )
        stage_packets[BindingStageName.REVIEW] = review_packet
        ordered_packets = tuple(
            stage_packets[stage_name] for stage_name, _, _, _ in self._STAGE_SPECS
        )
        return DeskCognitionRuntimeResult(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
            eligibility=eligibility,
            execution=execution,
            review=review,
            parallel_risk_lane=parallel_risk_lane,
            capital_deployment_authority=capital_deployment_authority,
            downstream_opening_snapshot=downstream_opening_snapshot,
            downstream_live_inventory_snapshot=downstream_live_inventory_snapshot,
            downstream_architecture_receipt=downstream_architecture_receipt,
            parallel_risk_calibration=parallel_risk_calibration,
            stage_local_handoff=stage_local_handoff,
            stage_packets=ordered_packets,
            packet_lineage=tuple(packet.packet_id for packet in ordered_packets),
            stage_packet_ids=stage_packet_ids,
            contract_packets=tuple(
                emission.packet
                for emission in (
                    *upstream_contract_emissions,
                    *selector_contract_emissions,
                )
            ),
            contract_packet_ids={
                emission.output.canonical_slug: emission.packet.packet_id
                for emission in (
                    *upstream_contract_emissions,
                    *selector_contract_emissions,
                )
            },
            options_flow_history_observation=options_flow_history_observation,
            options_flow_history_write_result=options_flow_history_write_result,
        )

    def _posture_with_contract_citations(
        self,
        posture: PostureRiskOutput,
        selector_emissions: list[TrancheAContractEmission],
    ) -> PostureRiskOutput:
        citation_map = {
            emission.output.canonical_slug: emission.output for emission in selector_emissions
        }
        signal_conflict = cast(
            SignalConflictDetectorContractOutput,
            citation_map["signal_conflict_detector"],
        )
        confidence = cast(
            ModelConfidenceScorerContractOutput, citation_map["model_confidence_scorer"]
        )
        conviction = cast(
            ConvictionTierAllocatorContractOutput,
            citation_map["conviction_tier_allocator"],
        )
        extra_reasons = [
            f"contract:signal_conflict_detector:{signal_conflict.conflict_state}",
            f"contract:model_confidence_scorer:{confidence.confidence_band}",
            f"contract:conviction_tier_allocator:{conviction.conviction_tier}",
        ]
        return posture.model_copy(
            update={
                "reasons": [*posture.reasons, *extra_reasons],
                "downstream_annotations": [*posture.downstream_annotations, *extra_reasons],
            }
        )

    def _eligibility_with_contract_citations(
        self,
        eligibility: PlaybookEligibilityOutput,
        selector_emissions: list[TrancheAContractEmission],
    ) -> PlaybookEligibilityOutput:
        citation_map = {
            emission.output.canonical_slug: emission.output for emission in selector_emissions
        }
        entry_gate = cast(EntryGateContractOutput, citation_map["entry_gate"])
        ladder = cast(LadderConstructorContractOutput, citation_map["ladder_constructor"])
        archetype = cast(ArchetypeMatcherContractOutput, citation_map["archetype_matcher"])
        reasons = [
            *eligibility.reasons,
            f"contract:entry_gate:{entry_gate.suppression_tag}",
            f"contract:ladder_constructor:{ladder.constructor_state}",
            f"contract:archetype_matcher:{archetype.pattern_tag}",
        ]
        updated_candidates = []
        for candidate in eligibility.candidates:
            candidate_reasons = list(candidate.reasons)
            if archetype.matched_playbook == candidate.playbook_id:
                candidate_reasons.append(f"contract:archetype_matcher:{archetype.pattern_tag}")
            if entry_gate.suppression_tag != "clear":
                candidate_reasons.append(f"contract:entry_gate:{entry_gate.suppression_tag}")
            updated_candidates.append(candidate.model_copy(update={"reasons": candidate_reasons}))
        return eligibility.model_copy(update={"reasons": reasons, "candidates": updated_candidates})

    def _build_execution_position_context(
        self,
        *,
        temporal: TemporalContextOutput,
        posture: PostureRiskOutput,
        inventory_state: InventoryState,
        eligibility: PlaybookEligibilityOutput,
    ) -> PositionContextInput | None:
        if "opening_drive_continuation" not in set(
            eligibility.active_setup_variant_ids + eligibility.watch_setup_variant_ids
        ):
            return None
        current_position_size_pct = round(
            inventory_state.existing_inventory_pct + inventory_state.overnight_inventory_pct,
            4,
        )
        position_active = current_position_size_pct > 0.0
        carry_state_eligible = (
            position_active
            and temporal.desk_window == "late_session"
            and temporal.event_window_state in {"clear", "clear_window"}
            and posture.permission_state.value == "allow"
            and posture.thesis_state == "valid"
        )
        hard_flat_required = bool(
            posture.time_stop_state == "time_stop_near"
            or posture.permission_state.value == "derisk"
            or (temporal.minutes_to_close is not None and temporal.minutes_to_close <= 5)
        )
        return PositionContextInput(
            setup_variant_id="opening_drive_continuation",
            execution_expression_id="continuation_ladder_exec",
            tradable_expression_family=TradableExpressionFamily.SINGLE_LEG_CALL_DEBIT,
            legal_lifecycle_actions=[
                LifecycleAction.ADD,
                LifecycleAction.TRIM,
                LifecycleAction.FLATTEN,
                LifecycleAction.HOLD_SMALL_OVERNIGHT,
                LifecycleAction.BLOCK_CARRY,
            ],
            position_active=position_active,
            current_position_size_pct=current_position_size_pct,
            carry_state_eligible=carry_state_eligible,
            hard_flat_required=hard_flat_required,
        )

    def _build_parallel_risk_temporal_input_packet(
        self,
        *,
        emitted_at: datetime,
        temporal_input: TemporalContextInput,
        trace_id: str,
        run_id: str,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> DmpV3Envelope[TemporalContextInput]:
        packet_id = f"dmp::temporal_input::{self._packet_id(emitted_at=emitted_at, stage_name=BindingStageName.TEMPORAL, stack_id=stack_id, coefficient_set_id=coefficient_set_id).split('dmp::', 1)[1]}"
        return DmpV3Envelope[TemporalContextInput](
            **build_dmp_v3_envelope_kwargs(
                packet_id=packet_id,
                emitted_at=emitted_at,
                grammar_role="temporal_context",
                behaviour_class="input_surface",
                payload=temporal_input,
                trader_summary="temporal context input surface for canonical parallel-risk lane reads",
                stack_id=stack_id,
                coefficient_set_id=coefficient_set_id,
                dependencies=["desk_calendar_authority", "live_event_snapshot", "next_event_at", "next_expiry"],
                input_model_name="TemporalContextInput",
                output_model_name="TemporalContextInput",
                trace_id=trace_id,
                run_id=run_id,
                scenario_id="live",
                module_id="temporal_context_input",
                module_instance_id="temporal_input::runtime",
                stage_name="temporal_input",
                registry_version="dmp_v3_live",
                environment_tag="research",
                dataschema="urn:nvda:schema:temporal_context.input:1.0.0",
                packet_type="urn:nvda:packet:temporal_context.input_surface",
                packetrole="input_surface",
                summary_keyflags=["live_event_snapshot", "desk_calendar_authority"],
            )
        )

    def _runtime_trace_ids(
        self,
        *,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> tuple[str, str]:
        token = emitted_at.isoformat()
        suffix = f"::{stack_id or 'no_stack'}::{coefficient_set_id or 'no_coeffs'}"
        return (f"trace::{token}{suffix}", f"run::{token}{suffix}")

    def _build_stage_packet(
        self,
        *,
        emitted_at: datetime,
        stage_name: BindingStageName,
        stage_output: CognitionStagePayload,
        stage_packet_ids: dict[str, str],
        upstream_packet_ids: list[str],
        trace_id: str,
        run_id: str,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> DeskModulePacketV3:
        stage_spec = next(
            spec for spec in self._STAGE_SPECS if spec[0] is stage_name
        )
        _, grammar_role, input_model_name, output_model_name = stage_spec
        packet_id = stage_packet_ids[stage_name.value]
        return build_dmp_v3_packet_from_payload(
            packet_id=packet_id,
            emitted_at=emitted_at,
            grammar_role=grammar_role,
            behaviour_class=DmpBehaviourClass.STAGE_OUTPUT,
            payload=stage_output,
            trader_summary=self._packet_summary(stage_name, stage_output),
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=self._dependencies_for_stage(stage_name),
            input_model_name=input_model_name,
            output_model_name=output_model_name,
            parent_packet_ids=([upstream_packet_ids[-1]] if upstream_packet_ids else []),
            dependency_packet_ids=list(upstream_packet_ids),
            review_trace_id=(f"review-trace::{packet_id}" if stage_name is BindingStageName.REVIEW else None),
            trace_id=trace_id,
            run_id=run_id,
            scenario_id="live",
            module_instance_id=f"{stage_name.value}::runtime",
            stage_name=stage_name.value,
            registry_version="dmp_v3_live",
            environment_tag="research",
        )

    def _packet_id(
        self,
        *,
        emitted_at: datetime,
        stage_name: BindingStageName,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> str:
        token = emitted_at.isoformat().replace("+00:00", "Z").replace(":", "").replace("-", "")
        parts = [stage_name.value, token]
        if stack_id:
            parts.append(stack_id)
        if coefficient_set_id:
            parts.append(coefficient_set_id)
        return "dmp::" + "::".join(parts)

    def _dependencies_for_stage(self, stage_name: BindingStageName) -> list[str]:
        return {
            BindingStageName.TEMPORAL: ["temporal_state_v1"],
            BindingStageName.REGIME: [],
            BindingStageName.OPTIONS_FLOW: [],
            BindingStageName.POSTURE: [
                DmpGrammarRole.TEMPORAL_CONTEXT.value,
                DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
                DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            ],
            BindingStageName.ELIGIBILITY: [
                DmpGrammarRole.TEMPORAL_CONTEXT.value,
                DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
                DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
                DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
            ],
            BindingStageName.EXECUTION: [
                DmpGrammarRole.TEMPORAL_CONTEXT.value,
                DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
                DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
                DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
                DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
            ],
            BindingStageName.REVIEW: [
                DmpGrammarRole.TEMPORAL_CONTEXT.value,
                DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
                DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
                DmpGrammarRole.POSTURE_RISK_PERMISSION.value,
                DmpGrammarRole.PLAYBOOK_ELIGIBILITY.value,
                DmpGrammarRole.EXPRESSION_EXECUTION.value,
            ],
        }[stage_name]

    def _packet_summary(self, stage_name: BindingStageName, payload: CognitionStagePayload) -> str:
        if stage_name is BindingStageName.TEMPORAL:
            if isinstance(payload, TemporalContextOutput):
                return f"{payload.desk_window} / {payload.session_phase.value}"
            raise TypeError("Temporal DMP payload drifted away from TemporalContextOutput")
        if stage_name is BindingStageName.REGIME:
            if isinstance(payload, MarketRegimeContextOutput):
                return f"{payload.volatility_regime.value} / {payload.signal_conflict_state}"
            raise TypeError("Regime DMP payload drifted away from MarketRegimeContextOutput")
        if stage_name is BindingStageName.OPTIONS_FLOW:
            if isinstance(payload, OptionsFlowContextOutput):
                return f"{payload.options_behavior_cluster} / {payload.gamma_state.value}"
            raise TypeError("Options-flow DMP payload drifted away from OptionsFlowContextOutput")
        if stage_name is BindingStageName.POSTURE:
            if isinstance(payload, PostureRiskOutput):
                return f"{payload.permission_state.value} / {payload.posture_label}"
            raise TypeError("Posture DMP payload drifted away from PostureRiskOutput")
        if stage_name is BindingStageName.ELIGIBILITY:
            if isinstance(payload, PlaybookEligibilityOutput):
                return (
                    f"adds={payload.add_candidates or ['none']} / "
                    f"watch={payload.watch_only_candidates or ['none']}"
                )
            raise TypeError("Eligibility DMP payload drifted away from PlaybookEligibilityOutput")
        if stage_name is BindingStageName.EXECUTION:
            if isinstance(payload, ExecutionExpressionOutput):
                return f"{payload.entry_style} / active={payload.active_playbook_ids or ['none']}"
            raise TypeError("Execution DMP payload drifted away from ExecutionExpressionOutput")
        if isinstance(payload, ReviewExplanationOutput):
            return payload.summary
        raise TypeError("Review DMP payload drifted away from ReviewExplanationOutput")
