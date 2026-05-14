"""Architecture-only downstream opening shells.

These shells reserve the lawful downstream homes that sit after serial candidate
formation and before any later behavioural opening-policy pack is written.
"""
from __future__ import annotations

from nvda_desk.schemas.cognition import (
    CapitalDeploymentAuthorityDecision,
    ExecutionExpressionOutput,
    StageLocalHandoffSurface,
)
from nvda_desk.schemas.downstream import (
    DownstreamOpeningSnapshot,
    DownstreamPolicyStatus,
    DownstreamReadSurface,
    DownstreamRecommendationHistoryReservation,
    DownstreamStateReadResult,
    OpeningAuthorisationResult,
    PlacementHandoffResult,
    PlacementReadinessResult,
)
from nvda_desk.schemas.parallel_risk import ParallelRiskLanePacket
from nvda_desk.services.downstream_seam_checkpointing import (
    CHECKPOINT_OPENING_AUTHORISATION_OBSERVED,
    CHECKPOINT_PLACEMENT_HANDOFF_OBSERVED,
    checkpoint_observation,
)


class DownstreamOpeningService:
    """Build architecture-only opening snapshots without deciding policy."""

    service_id = "downstream_opening_service"

    def build_snapshot(
        self,
        *,
        execution: ExecutionExpressionOutput,
        stage_local_handoff: StageLocalHandoffSurface,
        parallel_risk_lane_packet: ParallelRiskLanePacket,
        capital_deployment_authority: CapitalDeploymentAuthorityDecision | None,
        state_read_result: DownstreamStateReadResult | None = None,
    ) -> DownstreamOpeningSnapshot:
        """Return the downstream opening shell snapshot for one runtime pass."""

        return DownstreamOpeningSnapshot(
            opening_authorisation=self._opening_authorisation(
                stage_local_handoff=stage_local_handoff,
                parallel_risk_lane_packet=parallel_risk_lane_packet,
                capital_deployment_authority=capital_deployment_authority,
                state_read_result=state_read_result,
            ),
            placement_readiness=self._placement_readiness(
                execution=execution,
                state_read_result=state_read_result,
            ),
            placement_handoff=self._placement_handoff(
                execution=execution,
                stage_local_handoff=stage_local_handoff,
                state_read_result=state_read_result,
            ),
            notes=[
                "architecture_only_downstream_opening_snapshot",
                "behavioural_policy_deferred_to_later_pack",
            ],
        )

    def _opening_authorisation(
        self,
        *,
        stage_local_handoff: StageLocalHandoffSurface,
        parallel_risk_lane_packet: ParallelRiskLanePacket,
        capital_deployment_authority: CapitalDeploymentAuthorityDecision | None,
        state_read_result: DownstreamStateReadResult | None,
    ) -> OpeningAuthorisationResult:
        reservation = self._reservation(state_read_result)
        local_state_reads = self._local_state_reads(state_read_result)
        recommendation = stage_local_handoff.execution_post_modifier_pre_final_risk
        serial_ladder_shape_sum = round(sum(recommendation.scaling_plan), 4) if recommendation.scaling_plan else 0.0
        market_translation_surface = parallel_risk_lane_packet.required_market_translation_surface()
        candidate_audit_surface = parallel_risk_lane_packet.required_candidate_audit_surface()
        immediate_opening_slice_pct = self._immediate_opening_slice_pct(
            recommendation=recommendation,
            capital_deployment_authority=capital_deployment_authority,
        )
        result = OpeningAuthorisationResult(
            service_id=self.service_id,
            shell_name="opening_authorisation",
            policy_status=(
                DownstreamPolicyStatus.DELEGATED_TO_EXISTING_OWNER
                if capital_deployment_authority is not None
                else DownstreamPolicyStatus.RESERVED_HOME_ONLY
            ),
            decision_owner=(
                "capital_deployment_authority_service"
                if capital_deployment_authority is not None
                else None
            ),
            reads_from=self._reads(
                DownstreamReadSurface.SERIAL_CANDIDATE,
                DownstreamReadSurface.STAGE_LOCAL_HANDOFF,
                DownstreamReadSurface.PARALLEL_RISK_LANE,
                *(
                    [DownstreamReadSurface.CAPITAL_DEPLOYMENT_AUTHORITY_DECISION]
                    if capital_deployment_authority is not None
                    else []
                ),
                *local_state_reads,
                *(
                    [DownstreamReadSurface.RECOMMENDATION_HISTORY_RESERVATION]
                    if reservation is not None
                    else []
                ),
            ),
            not_read=[
                "duplicate_or_recent_open_policy_deferred",
                "placement_formula_deferred",
                "paper_order_receipt_reader_deferred",
                "no_local_opening_policy_authored_in_gate_267",
            ],
            state_snapshot=None if state_read_result is None else state_read_result.state_snapshot,
            recommendation_history_reservation=reservation,
            authorised_deployable_pct=(
                None if capital_deployment_authority is None else capital_deployment_authority.authorised_deployable_pct
            ),
            immediate_opening_slice_pct=immediate_opening_slice_pct,
            serial_ladder_shape_sum=(serial_ladder_shape_sum if serial_ladder_shape_sum > 0.0 else None),
            notes=[
                f"lead_playbook_id:{recommendation.lead_playbook_id or 'none'}",
                f"parallel_weather_state:{market_translation_surface.environmental_weather_state.value}",
                f"parallel_consequence_class:{candidate_audit_surface.consequence_class.value}",
                "fresh_capital_authority_stays_bounded_to_existing_owner",
                "opening_authorisation_receipt_names_parallel_and_local_state_reads_explicitly",
                *(
                    [f"immediate_opening_slice_pct:{immediate_opening_slice_pct:.4f}"]
                    if immediate_opening_slice_pct is not None
                    else []
                ),
            ],
        )
        result.checkpoint_observations.append(
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_OPENING_AUTHORISATION_OBSERVED,
                input_snapshot={
                    "lead_playbook_id": recommendation.lead_playbook_id,
                    "parallel_weather_state": market_translation_surface.environmental_weather_state.value,
                    "parallel_consequence_class": candidate_audit_surface.consequence_class.value,
                    "capital_decision_present": capital_deployment_authority is not None,
                    "serial_ladder_shape_sum": serial_ladder_shape_sum,
                },
                output_snapshot={
                    "policy_status": result.policy_status.value,
                    "decision_owner": result.decision_owner,
                    "authorised_deployable_pct": result.authorised_deployable_pct,
                    "immediate_opening_slice_pct": result.immediate_opening_slice_pct,
                    "reads_from": [surface.value for surface in result.reads_from],
                },
            )
        )
        return result

    def _placement_readiness(
        self,
        *,
        execution: ExecutionExpressionOutput,
        state_read_result: DownstreamStateReadResult | None,
    ) -> PlacementReadinessResult:
        return PlacementReadinessResult(
            service_id=self.service_id,
            shell_name="placement_readiness",
            policy_status=(
                DownstreamPolicyStatus.STATE_ATTACHED_NO_POLICY
                if state_read_result is not None
                else DownstreamPolicyStatus.RESERVED_HOME_ONLY
            ),
            decision_owner=None,
            reads_from=self._reads(
                DownstreamReadSurface.SERIAL_CANDIDATE,
                *(
                    [DownstreamReadSurface.CAPITAL_STATE]
                    if state_read_result is not None
                    else []
                ),
                *(
                    [DownstreamReadSurface.POSITIONS, DownstreamReadSurface.POSITION_INSTANCES]
                    if state_read_result is not None
                    else []
                ),
            ),
            not_read=[
                "broker_submission_rules_deferred",
                "ladder_placement_timing_deferred",
                "duplicate_or_recent_open_policy_deferred",
                "no_readiness_policy_authored_in_gate_267",
            ],
            state_snapshot=None if state_read_result is None else state_read_result.state_snapshot,
            recommendation_history_reservation=None,
            notes=[
                f"entry_style:{execution.entry_style}",
                "placement_readiness_home_reserved_only",
            ],
        )

    def _placement_handoff(
        self,
        *,
        execution: ExecutionExpressionOutput,
        stage_local_handoff: StageLocalHandoffSurface,
        state_read_result: DownstreamStateReadResult | None,
    ) -> PlacementHandoffResult:
        result = PlacementHandoffResult(
            service_id=self.service_id,
            shell_name="placement_handoff",
            policy_status=(
                DownstreamPolicyStatus.STATE_ATTACHED_NO_POLICY
                if state_read_result is not None
                else DownstreamPolicyStatus.RESERVED_HOME_ONLY
            ),
            decision_owner=None,
            reads_from=self._reads(
                DownstreamReadSurface.SERIAL_CANDIDATE,
                DownstreamReadSurface.STAGE_LOCAL_HANDOFF,
            ),
            not_read=[
                "order_staging_policy_deferred",
                "broker_handoff_policy_deferred",
                "no_handoff_decisioning_in_gate_267",
            ],
            state_snapshot=None if state_read_result is None else state_read_result.state_snapshot,
            recommendation_history_reservation=self._reservation(state_read_result),
            notes=[
                f"lead_setup_variant_id:{execution.lead_setup_variant_id or 'none'}",
                "placement_handoff_home_reserved_only",
            ],
        )
        result.checkpoint_observations.append(
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_PLACEMENT_HANDOFF_OBSERVED,
                input_snapshot={
                    "lead_setup_variant_id": execution.lead_setup_variant_id,
                    "lead_playbook_id": stage_local_handoff.execution_post_modifier_pre_final_risk.lead_playbook_id,
                },
                output_snapshot={
                    "policy_status": result.policy_status.value,
                    "reservation_future_home": result.recommendation_history_reservation.future_home,
                    "reads_from": [surface.value for surface in result.reads_from],
                },
            )
        )
        return result

    @staticmethod
    def _immediate_opening_slice_pct(
        *,
        recommendation: ExecutionExpressionOutput,
        capital_deployment_authority: CapitalDeploymentAuthorityDecision | None,
    ) -> float | None:
        if capital_deployment_authority is None or not recommendation.scaling_plan:
            return None
        authorised_total = capital_deployment_authority.authorised_deployable_pct
        if authorised_total <= 0.0:
            return 0.0
        shape_sum = round(sum(recommendation.scaling_plan), 4)
        if shape_sum <= 0.0 or shape_sum > 1.0:
            return None
        first_step = round(float(recommendation.scaling_plan[0]), 4)
        return round(authorised_total * (first_step / shape_sum), 4)

    def _reservation(
        self,
        state_read_result: DownstreamStateReadResult | None,
    ) -> DownstreamRecommendationHistoryReservation | None:
        if state_read_result is None:
            return DownstreamRecommendationHistoryReservation(
                existing_receipt_tables=[],
                future_home="downstream_recommendation_history_reader",
                notes=[
                    "recommendation_history_home_reserved",
                    "repo_native_receipt_attachment_deferred_until_gate_268",
                ],
            )
        return state_read_result.recommendation_history_reservation

    @staticmethod
    def _local_state_reads(
        state_read_result: DownstreamStateReadResult | None,
    ) -> list[DownstreamReadSurface]:
        if state_read_result is None:
            return []
        return [
            DownstreamReadSurface.CAPITAL_STATE,
            DownstreamReadSurface.POSITIONS,
            DownstreamReadSurface.POSITION_INSTANCES,
            DownstreamReadSurface.SIGNAL_RECEIPTS,
            DownstreamReadSurface.VETO_RECEIPTS,
            DownstreamReadSurface.RISK_BLOCK_RECEIPTS,
            DownstreamReadSurface.ORDER_EVENT_RECEIPTS,
            DownstreamReadSurface.FILL_EVENT_RECEIPTS,
        ]

    @staticmethod
    def _reads(*reads: DownstreamReadSurface) -> list[DownstreamReadSurface]:
        deduped: list[DownstreamReadSurface] = []
        for read in reads:
            if read not in deduped:
                deduped.append(read)
        return deduped
