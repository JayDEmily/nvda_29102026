"""Review and explanation service for the Desk Cognition Grammar.

This service builds machine-readable review packets that reconstruct how the
runtime reached a posture, playbook, and execution decision.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    ContradictionSurface,
    EffectivePolicySnapshot,
    PlaybookDecision,
    RejectedPlaybookReason,
    ReviewExplanationInput,
    ReviewExplanationOutput,
    StageReasonPacket,
)
from nvda_desk.schemas.market import SessionAlignmentExpectation
from nvda_desk.schemas.review import (
    CandidateComparisonContext,
    CandidateGovernanceSurface,
    EconomicContributionPacket,
    EconomicContributionTag,
    EventOptionsStressPolicySurface,
    ModifierControlLawSurface,
    PhaseCarryoverPolicySurface,
    PrecursorGovernanceSurface,
    PrecursorRuntimeBindingSurface,
    PromotionEvidencePacket,
    ReviewEligibilitySurface,
    ReviewFailureClass,
    ReviewFailurePacket,
    ReviewGovernanceSurface,
    ReviewLineagePacket,
    ReviewResolutionClass,
    TemporalEventWindowSurface,
)
from nvda_desk.schemas.risk import (
    CarryHorizonState,
    PhaseBehaviourClass,
    PhaseNoActionBias,
)
from nvda_desk.services.review_packets import ReviewPacketService
from nvda_desk.services.downstream_seam_checkpointing import (
    CHECKPOINT_REVIEW_PACKET_PRESERVED_SEAM_OBSERVED,
    checkpoint_observation,
)
from nvda_desk.schemas.state_policy import (
    AdjudicationDisposition,
    BehaviourStabilityState,
    CandidateSetShape,
    CorridorBounds,
    CorridorBreachSeverity,
    CoverageSliceClass,
    CoverageSliceScore,
    EventOptionsBehaviourClass,
    EventOptionsStressState,
    MetricTriggerMode,
    PersistenceHysteresisSpec,
    PolicyEffectType,
    ReviewChangeBudget,
    ReviewEvidenceBlock,
    ReviewOutcome,
    ReviewSurfaceClass,
    ReviewTriggerClass,
    RuntimeSurfaceClass,
    ScorecardAxis,
    StabilityMetricFamily,
    StabilityMetricObservation,
    SurfaceStabilityScorecard,
)
from nvda_desk.schemas.temporal_surface import (
    EventCarrySensitivity,
    EventOverlapClass,
    EventProximityState,
    EventRiskTimingClass,
    EventWindowState,
)
from nvda_desk.services.state_conditioned_modifier import (
    project_carry_horizon_state,
    project_day_phase_state,
    project_event_option_state_labels,
)


class ReviewExplanationService:
    """Build deterministic review and explanation packets.

    Purpose:
        Reconstruct the runtime decision as a structured stage-by-stage review.
    Inputs:
        `ReviewExplanationInput` containing the outputs from all prior runtime
        layers, including explicit playbook action buckets.
    Outputs:
        `ReviewExplanationOutput` with stage packets, rejected playbooks,
        contradiction surfaces, conflict density, and module attribution hooks.
    Determinism:
        Produces ordered packets from live model payloads with fixed rules.
    """

    def evaluate(self, payload: ReviewExplanationInput) -> ReviewExplanationOutput:
        """Create a structured review packet for one runtime snapshot."""

        conflict_tags = self._conflict_tags(payload)
        signal_conflict_density = round(min(1.0, len(conflict_tags) / 5.0), 4)
        final_risk_join = self._final_risk_join(payload)
        final_risk_action = final_risk_join.action.value
        summary = (
            f"window={payload.temporal.desk_window}; "
            f"permission={payload.posture.permission_state.value}; "
            f"families={payload.execution.active_family_ids or ['none']}; "
            f"setups={payload.execution.active_setup_variant_ids or ['none']}; "
            f"playbooks={payload.execution.active_playbook_ids or ['none']}; "
            f"final_risk={final_risk_action}"
        )
        stage_reason_packets = [
            StageReasonPacket(
                stage="temporal",
                summary=payload.temporal.desk_window,
                reasons=payload.temporal.reasons,
            ),
            StageReasonPacket(
                stage="regime",
                summary=payload.regime.signal_conflict_state,
                reasons=payload.regime.reasons,
            ),
            StageReasonPacket(
                stage="options_flow",
                summary=payload.options_flow.options_behavior_cluster,
                reasons=payload.options_flow.reasons,
            ),
            StageReasonPacket(
                stage="posture",
                summary=payload.posture.permission_state.value,
                reasons=payload.posture.reasons,
            ),
            StageReasonPacket(
                stage="eligibility",
                summary=(
                    f"families={payload.eligibility.active_family_ids or ['none']} / "
                    f"setups={payload.eligibility.active_setup_variant_ids or ['none']} / "
                    f"eligible={payload.eligibility.add_candidates or payload.eligibility.trim_candidates or ['none']}"
                ),
                reasons=payload.eligibility.reasons,
            ),
            StageReasonPacket(
                stage="execution",
                summary=(
                    f"{payload.execution.entry_style} / "
                    f"family={payload.execution.lead_family_id or 'none'} / "
                    f"setup={payload.execution.lead_setup_variant_id or 'none'}"
                ),
                reasons=payload.execution.reasons,
            ),
        ]
        stage_reason_packets.append(
            StageReasonPacket(
                stage="final_risk_join",
                summary=final_risk_join.action.value,
                reasons=final_risk_join.reasons,
            )
        )
        rejected_playbooks = [
            RejectedPlaybookReason(
                playbook_id=candidate.playbook_id,
                decision=candidate.decision,
                action_bias=candidate.action_bias,
                reasons=candidate.reasons,
            )
            for candidate in payload.eligibility.candidates
            if candidate.decision is not PlaybookDecision.ELIGIBLE
        ]
        contradictions = [
            ContradictionSurface(
                contradiction_id=tag,
                description=self._contradiction_description(tag),
                implicated_stages=self._contradiction_stages(tag),
            )
            for tag in conflict_tags
        ]
        module_attribution = self._module_attribution(stage_reason_packets)
        stage_summaries = {
            packet.stage: "; ".join(packet.reasons) for packet in stage_reason_packets
        }
        desk_readout = self._desk_readout(payload)
        event_window_governance = self._event_window_governance(payload)
        precursor_governance = self._precursor_governance(payload)
        precursor_runtime_binding = self._precursor_runtime_binding(payload)
        review_governance = self._review_governance(payload)
        phase_carry_policy = self._phase_carry_policy(payload)
        event_options_stress_policy = self._event_options_stress_policy(payload)
        modifier_control_law = self._modifier_control_law(payload)
        effective_policy = self._effective_policy(payload)
        review_lineage = self._review_lineage(payload)
        promotion_evidence = self._promotion_evidence(review_lineage)
        review_eligibility = self._review_eligibility(payload, promotion_evidence)
        stability_scorecards = self._stability_scorecards(review_eligibility)
        candidate_governance = self._candidate_governance(promotion_evidence)
        failure_taxonomy = self._failure_taxonomy(
            payload,
            conflict_tags,
            review_eligibility,
        )
        economic_accountability = self._economic_accountability(failure_taxonomy)

        review_packet: dict[str, object] = {
            "temporal": payload.temporal.model_dump(mode="json"),
            "regime": payload.regime.model_dump(mode="json"),
            "options_flow": payload.options_flow.model_dump(mode="json"),
            "posture": payload.posture.model_dump(mode="json"),
            "eligibility": payload.eligibility.model_dump(mode="json"),
            "execution": payload.execution.model_dump(mode="json"),
            "hierarchy_summary": {
                "active_family_ids": list(payload.execution.active_family_ids),
                "active_setup_variant_ids": list(payload.execution.active_setup_variant_ids),
                "lead_family_id": payload.execution.lead_family_id,
                "lead_setup_variant_id": payload.execution.lead_setup_variant_id,
                "lead_playbook_id": payload.execution.lead_playbook_id,
            },
            "stage_summaries": stage_summaries,
            "stage_reason_packets": [
                packet.model_dump(mode="json") for packet in stage_reason_packets
            ],
            "rejected_playbooks": [packet.model_dump(mode="json") for packet in rejected_playbooks],
            "contradictions": [surface.model_dump(mode="json") for surface in contradictions],
            "module_attribution": module_attribution,
            "signal_conflict_density": signal_conflict_density,
            "desk_readout": desk_readout,
            "conflicts": conflict_tags,
            "final_risk_join": final_risk_join.model_dump(mode="json"),
            "review_lineage": review_lineage.model_dump(mode="json"),
            "failure_taxonomy": failure_taxonomy.model_dump(mode="json"),
            "economic_accountability": economic_accountability.model_dump(mode="json"),
            "promotion_evidence": promotion_evidence.model_dump(mode="json"),
        }
        if event_window_governance is not None:
            review_packet["event_window_governance"] = event_window_governance.model_dump(
                mode="json"
            )
        if precursor_governance is not None:
            review_packet["precursor_governance"] = precursor_governance.model_dump(mode="json")
        if precursor_runtime_binding is not None:
            review_packet["precursor_runtime_binding"] = precursor_runtime_binding.model_dump(
                mode="json"
            )
        if review_governance is not None:
            review_packet["review_governance"] = review_governance.model_dump(mode="json")
        if phase_carry_policy is not None:
            review_packet["phase_carry_policy"] = phase_carry_policy.model_dump(mode="json")
        if event_options_stress_policy is not None:
            review_packet["event_options_stress_policy"] = event_options_stress_policy.model_dump(
                mode="json"
            )
        if modifier_control_law is not None:
            review_packet["modifier_control_law"] = modifier_control_law.model_dump(mode="json")
        if effective_policy is not None:
            review_packet["effective_policy"] = effective_policy.model_dump(mode="json")
        review_packet["stage_local_handoff"] = payload.stage_local_handoff.model_dump(mode="json")
        review_packet["execution_recommendation"] = payload.stage_local_handoff.execution_post_modifier_pre_final_risk.model_dump(mode="json")
        review_packet["overlay_risk_decision"] = payload.stage_local_handoff.overlay_risk_decision.model_dump(mode="json")
        review_packet["terminal_risk_application"] = payload.stage_local_handoff.terminal_risk_application.model_dump(mode="json")
        review_packet["terminal_risk_decision"] = payload.stage_local_handoff.terminal_risk_decision.model_dump(mode="json")
        review_packet["admissibility_surface"] = payload.eligibility.admissibility_surface.model_dump(mode="json")
        review_packet["candidate_ownership"] = payload.execution.candidate_ownership.model_dump(mode="json")
        if review_eligibility is not None:
            review_packet["review_eligibility"] = review_eligibility.model_dump(mode="json")
        if stability_scorecards:
            review_packet["stability_scorecards"] = [
                scorecard.model_dump(mode="json") for scorecard in stability_scorecards
            ]
        if candidate_governance is not None:
            review_packet["candidate_governance"] = candidate_governance.model_dump(mode="json")
        review_packet["parallel_risk_lane"] = payload.parallel_risk_lane_packet.model_dump(mode="json")
        market_translation_surface = payload.parallel_risk_lane_packet.required_market_translation_surface()
        candidate_audit_surface = payload.parallel_risk_lane_packet.required_candidate_audit_surface()
        summary_bits = [
            f"weather={market_translation_surface.environmental_weather_state.value}",
            f"candidate_state={candidate_audit_surface.candidate_state.value}",
            f"consequence_class={candidate_audit_surface.consequence_class.value}",
        ]
        review_packet["parallel_risk_lane_summary"] = {
            "lane_id": payload.parallel_risk_lane_packet.lane_id,
            "packet_id": payload.parallel_risk_lane_packet.packet_id,
            "protocol_version": payload.parallel_risk_lane_packet.protocol_version,
            "dataschema": payload.parallel_risk_lane_packet.dataschema,
            "summary": " / ".join(summary_bits),
        }
        if payload.capital_deployment_authority is not None:
            review_packet["capital_deployment_authority"] = payload.capital_deployment_authority.model_dump(mode="json")
        downstream_review_surface = ReviewPacketService.render_downstream_architecture_receipt(
            payload.downstream_architecture_receipt
        )
        if downstream_review_surface is None:
            raise ValueError('downstream architecture receipt review surface is required')
        review_packet["downstream_architecture_receipt"] = downstream_review_surface.model_dump(mode="json")

        output = ReviewExplanationOutput(
            summary=summary,
            conflict_tags=conflict_tags,
            signal_conflict_density=signal_conflict_density,
            stage_reason_packets=stage_reason_packets,
            rejected_playbooks=rejected_playbooks,
            contradictions=contradictions,
            module_attribution=module_attribution,
            effective_policy=effective_policy,
            stability_scorecards=stability_scorecards,
            review_governance=review_governance,
            event_window_governance=event_window_governance,
            precursor_governance=precursor_governance,
            precursor_runtime_binding=precursor_runtime_binding,
            phase_carry_policy=phase_carry_policy,
            event_options_stress_policy=event_options_stress_policy,
            modifier_control_law=modifier_control_law,
            review_eligibility=review_eligibility,
            candidate_governance=candidate_governance,
            review_lineage=review_lineage,
            failure_taxonomy=failure_taxonomy,
            economic_accountability=economic_accountability,
            promotion_evidence=promotion_evidence,
            stage_local_handoff=payload.stage_local_handoff,
            capital_deployment_authority=payload.capital_deployment_authority,
            downstream_architecture_receipt=payload.downstream_architecture_receipt,
            review_packet=review_packet,
        )
        output.checkpoint_observations.append(
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_REVIEW_PACKET_PRESERVED_SEAM_OBSERVED,
                input_snapshot={
                    "lead_playbook_id": payload.execution.lead_playbook_id,
                    "parallel_lane_id": payload.parallel_risk_lane_packet.lane_id,
                    "parallel_weather_state": market_translation_surface.environmental_weather_state.value,
                    "parallel_consequence_class": candidate_audit_surface.consequence_class.value,
                    "terminal_risk_action": payload.stage_local_handoff.terminal_risk_application.final_decision.action.value,
                },
                output_snapshot={
                    "review_packet_keys": sorted(review_packet.keys()),
                    "downstream_policy_freeze_state": payload.downstream_architecture_receipt.policy_freeze_state,
                    "capital_decision_present": payload.capital_deployment_authority is not None,
                },
            )
        )
        return output

    @staticmethod
    def _final_risk_join(payload: ReviewExplanationInput):
        final_risk_join = payload.execution.final_risk_join
        if final_risk_join is None:
            raise ValueError('review explanation requires execution.final_risk_join')
        return final_risk_join

    def _conflict_tags(self, payload: ReviewExplanationInput) -> list[str]:
        conflict_tags: list[str] = []
        if payload.regime.signal_conflict_state != "aligned_regime":
            conflict_tags.append("regime_signal_conflict")
        if payload.posture.signal_conflict_state != "aligned_signals":
            conflict_tags.append("posture_signal_conflict")
        if payload.eligibility.no_trade_reasons and payload.execution.active_playbook_ids:
            conflict_tags.append("event_veto_breached")
        if (
            payload.options_flow.gamma_state.value == "destabilising"
            and payload.posture.permission_state.value != "block"
            and not payload.execution.hedge_required
        ):
            conflict_tags.append("missing_hedge_under_destabilising_gamma")
        if (
            payload.posture.inventory_posture_state in {"trapped", "capital_locked"}
            and payload.execution.inventory_action == "add"
        ):
            conflict_tags.append("adding_into_locked_inventory")
        return conflict_tags

    def _module_attribution(
        self, stage_reason_packets: list[StageReasonPacket]
    ) -> dict[str, float]:
        raw_scores = {
            packet.stage: max(1.0, float(len(packet.reasons))) for packet in stage_reason_packets
        }
        total = sum(raw_scores.values())
        return {stage: round(score / total, 4) for stage, score in raw_scores.items()}

    def _desk_readout(self, payload: ReviewExplanationInput) -> str:
        return (
            f"{payload.temporal.desk_window} | "
            f"{payload.regime.volatility_regime.value} / {payload.regime.breadth_concentration_state} | "
            f"{payload.options_flow.options_behavior_cluster} | "
            f"permission={payload.posture.permission_state.value} | "
            f"family={payload.execution.lead_family_id or 'none'} | "
            f"setup={payload.execution.lead_setup_variant_id or 'none'} | "
            f"inventory={payload.execution.inventory_action}"
        )

    def _contradiction_description(self, tag: str) -> str:
        descriptions = {
            "regime_signal_conflict": "The regime layer still shows unresolved cross-signal conflict.",
            "posture_signal_conflict": "Posture remained conflicted after options and inventory checks.",
            "event_veto_breached": "Execution stayed active despite an explicit no-trade event veto.",
            "missing_hedge_under_destabilising_gamma": "Destabilising gamma was present without a hedge overlay.",
            "adding_into_locked_inventory": "Execution proposed adding into trapped or locked inventory.",
        }
        return descriptions.get(tag, "Runtime contradiction detected.")

    def _contradiction_stages(self, tag: str) -> list[str]:
        stage_map = {
            "regime_signal_conflict": ["regime", "posture", "review_explanation"],
            "posture_signal_conflict": [
                "options_flow",
                "posture",
                "review_explanation",
            ],
            "event_veto_breached": ["temporal", "eligibility", "execution"],
            "missing_hedge_under_destabilising_gamma": ["options_flow", "execution"],
            "adding_into_locked_inventory": ["posture", "execution"],
        }
        return stage_map.get(tag, ["review_explanation"])

    def _event_window_governance(
        self, payload: ReviewExplanationInput
    ) -> TemporalEventWindowSurface | None:
        snapshot = (
            None if payload.temporal_input is None else payload.temporal_input.live_event_snapshot
        )
        next_event = None if snapshot is None else snapshot.next_event
        if next_event is None and payload.temporal.active_event_family is None:
            return None
        event_family = payload.temporal.active_event_family or (
            next_event.event_subclass
            if next_event is not None and next_event.event_subclass is not None
            else (
                next_event.event_class.value
                if next_event is not None and next_event.event_class is not None
                else (None if next_event is None else next_event.event_type)
            )
        )
        if event_family is None:
            return None
        return TemporalEventWindowSurface(
            proximity_state=EventProximityState(payload.temporal.event_proximity_state),
            window_state=EventWindowState(payload.temporal.event_window_state),
            overlap_class=EventOverlapClass(payload.temporal.event_overlap_class),
            risk_timing_class=EventRiskTimingClass(payload.temporal.event_risk_timing_class),
            carry_sensitivity=EventCarrySensitivity(payload.temporal.event_carry_sensitivity),
            timing_profile=payload.temporal.event_timing_profile,
            event_family=event_family,
        )

    def _precursor_governance(
        self, payload: ReviewExplanationInput
    ) -> PrecursorGovernanceSurface | None:
        packet = (
            None
            if payload.temporal_input is None
            else payload.temporal_input.precursor_runtime_packet
        )
        if packet is None:
            return None
        return PrecursorGovernanceSurface(
            active_venues=list(packet.active_venues),
            derived_fields=list(packet.derived_fields),
            session_alignment=[
                SessionAlignmentExpectation.USE_LAST_COMPLETE_SESSION,
                SessionAlignmentExpectation.NO_PARTIAL_SESSION_PROJECTION,
                SessionAlignmentExpectation.MAP_TO_NEXT_US_CASH_OPEN,
                SessionAlignmentExpectation.WEEKEND_AND_HOLIDAY_GAPS_MUST_STAY_EXPLICIT,
            ],
            notes=list(packet.notes),
        )

    def _precursor_runtime_binding(
        self, payload: ReviewExplanationInput
    ) -> PrecursorRuntimeBindingSurface | None:
        packet = (
            None
            if payload.temporal_input is None
            else payload.temporal_input.precursor_runtime_packet
        )
        if packet is None:
            return None
        return PrecursorRuntimeBindingSurface(
            requested_at=packet.requested_at,
            stitched_order=list(packet.stitched_order),
            active_venues=list(packet.active_venues),
            missing_venues=list(packet.missing_venues),
            raw_fields=list(packet.raw_fields),
            derived_fields=list(packet.derived_fields),
            derived_values=dict(packet.derived_values),
            contradiction_class=packet.contradiction_class,
            posture_state=packet.posture_state,
            fallback_dispositions=list(packet.fallback_dispositions),
            lineage_keys=list(packet.lineage_keys),
            notes=list(packet.notes),
        )

    def _review_governance(self, payload: ReviewExplanationInput) -> ReviewGovernanceSurface | None:
        packet = payload.modifier_runtime_packet
        if packet is None:
            return None
        return ReviewGovernanceSurface(
            stand_down_class=packet.stand_down_class,
            conflict_classes=list(packet.conflict_classes),
            degradation_step=packet.degradation_step,
            override_disposition=packet.override_disposition,
            override_audit_notes=list(packet.notes),
        )

    def _phase_carry_policy(
        self, payload: ReviewExplanationInput
    ) -> PhaseCarryoverPolicySurface | None:
        day_phase_state = project_day_phase_state(payload.temporal)
        carry_horizon_state = project_carry_horizon_state(payload.temporal)
        active_policy_ids = set()
        if payload.modifier_runtime_packet is not None:
            active_policy_ids = set(payload.modifier_runtime_packet.active_policy_ids)
        phase_policy_active = any(
            policy_id.startswith("phase_carry:") for policy_id in active_policy_ids
        )
        behaviour_class = PhaseBehaviourClass.NORMAL_OPERATION
        no_action_bias = PhaseNoActionBias.NEUTRAL
        if carry_horizon_state is not CarryHorizonState.INTRADAY_ONLY:
            behaviour_class = PhaseBehaviourClass.CARRY_PREPARATION
            no_action_bias = PhaseNoActionBias.PREFERRED
        elif phase_policy_active:
            behaviour_class = PhaseBehaviourClass.COMPRESSED_DEPLOYMENT
            no_action_bias = PhaseNoActionBias.PREFERRED
        return PhaseCarryoverPolicySurface(
            day_phase_state=day_phase_state,
            carry_horizon_state=carry_horizon_state,
            behaviour_class=behaviour_class,
            no_action_bias=no_action_bias,
            notes=list(payload.temporal.reasons)
            + (["phase_carry_policy_emitted_from_modifier_runtime"] if phase_policy_active else []),
        )

    def _event_options_stress_policy(
        self, payload: ReviewExplanationInput
    ) -> EventOptionsStressPolicySurface | None:
        active_labels = project_event_option_state_labels(payload.temporal, payload.options_flow)
        active_states: list[EventOptionsStressState] = []
        if "event_imminent" in active_labels:
            active_states.append(EventOptionsStressState.EVENT_IMMINENT)
        if "event_live" in active_labels:
            active_states.append(EventOptionsStressState.EVENT_LIVE)
        if "event_suppressed" in active_labels:
            active_states.append(EventOptionsStressState.EVENT_SUPPRESSED)
        if "negative_gamma_stress" in active_labels:
            active_states.append(EventOptionsStressState.NEGATIVE_GAMMA_STRESS)
        if "pin_risk" in active_labels:
            active_states.append(EventOptionsStressState.PIN_RISK)
        if "expiry_distortion" in active_labels:
            active_states.append(EventOptionsStressState.EXPIRY_DISTORTION)
        if not active_states:
            return None
        packet = payload.modifier_runtime_packet
        active_policy_ids = set() if packet is None else set(packet.active_policy_ids)
        hard_block = packet is not None and packet.triggered_kill_switch is not None
        if hard_block:
            behaviour_class = EventOptionsBehaviourClass.HARD_BLOCK
        elif "event_options:negative_gamma_stress" in active_policy_ids:
            behaviour_class = EventOptionsBehaviourClass.HEDGED_ONLY
        elif "event_options:pin_risk" in active_policy_ids:
            behaviour_class = EventOptionsBehaviourClass.SIZE_CAPPED
        else:
            behaviour_class = EventOptionsBehaviourClass.TIGHTENED_THRESHOLDS
        effect_types: list[PolicyEffectType] = []
        if hard_block:
            effect_types.append(PolicyEffectType.BLOCK)
        if "event_options:negative_gamma_stress" in active_policy_ids:
            effect_types.append(PolicyEffectType.HEDGE)
            effect_types.append(PolicyEffectType.CAP)
        if "event_options:pin_risk" in active_policy_ids:
            effect_types.append(PolicyEffectType.CAP)
        if "event_options:event_imminent" in active_policy_ids:
            effect_types.append(PolicyEffectType.DEGRADE)
        if not effect_types:
            effect_types.append(PolicyEffectType.SUPPRESS)
        return EventOptionsStressPolicySurface(
            active_states=active_states,
            behaviour_class=behaviour_class,
            effect_types=effect_types,
            hard_block=hard_block,
            notes=list(payload.options_flow.reasons)
            + (
                ["event_options_policy_emitted_from_modifier_runtime"] if packet is not None else []
            ),
        )

    def _modifier_control_law(
        self, payload: ReviewExplanationInput
    ) -> ModifierControlLawSurface | None:
        packet = payload.modifier_runtime_packet
        if packet is None:
            return None
        return ModifierControlLawSurface(
            active_precedence_bands=list(packet.active_precedence_bands),
            applied_combination_laws=list(packet.applied_combination_laws),
            triggered_kill_switch=packet.triggered_kill_switch,
            suppressed_state_labels=list(packet.suppressed_state_labels),
            notes=list(packet.notes),
        )

    def _effective_policy(self, payload: ReviewExplanationInput) -> EffectivePolicySnapshot | None:
        packet = payload.modifier_runtime_packet
        if packet is None:
            return None
        return EffectivePolicySnapshot(
            active_lineage=list(packet.effective_lineage),
            resolved_surfaces=list(packet.resolved_surfaces),
        )

    def _review_lineage(self, payload: ReviewExplanationInput) -> ReviewLineagePacket:
        event_lineage_keys = []
        precursor_lineage_keys = []
        if (
            payload.temporal_input is not None
            and payload.temporal_input.live_event_snapshot is not None
        ):
            event_lineage_keys = list(payload.temporal_input.live_event_snapshot.lineage_keys)
        if (
            payload.temporal_input is not None
            and payload.temporal_input.precursor_runtime_packet is not None
        ):
            precursor_lineage_keys = list(
                payload.temporal_input.precursor_runtime_packet.lineage_keys
            )
        modifier_policy_ids = []
        effective_targets = []
        resolved_surfaces = []
        if payload.modifier_runtime_packet is not None:
            modifier_policy_ids = list(payload.modifier_runtime_packet.active_policy_ids)
            effective_targets = [
                lineage.target_surface.value
                for lineage in payload.modifier_runtime_packet.effective_lineage
            ]
            resolved_surfaces = list(payload.modifier_runtime_packet.resolved_surfaces)
        return ReviewLineagePacket(
            event_lineage_keys=event_lineage_keys,
            precursor_lineage_keys=precursor_lineage_keys,
            modifier_policy_ids=modifier_policy_ids,
            effective_coefficient_targets=effective_targets,
            resolved_surfaces=resolved_surfaces,
            posture_change_reasons=list(payload.posture.reasons),
        )

    def _review_eligibility(
        self,
        payload: ReviewExplanationInput,
        promotion_evidence: PromotionEvidencePacket,
    ) -> ReviewEligibilitySurface:
        sample_count = (
            len(promotion_evidence.required_sections) - len(promotion_evidence.missing_sections)
        ) + len(payload.execution.active_playbook_ids)
        event_slice_count = 1 if payload.temporal.event_proximity_state != "no_event_context" else 0
        regime_slice_count = 1 if payload.regime.reasons else 0
        coverage_ratio = min(1.0, max(0.2, sample_count / 5.0))
        breach_severity = CorridorBreachSeverity.NONE
        if payload.posture.permission_state.value == "block":
            breach_severity = CorridorBreachSeverity.MATERIAL
        if len(promotion_evidence.missing_sections) >= 2:
            breach_severity = CorridorBreachSeverity.SEVERE
        evidence_block = ReviewEvidenceBlock(
            surface_class=ReviewSurfaceClass.POLICY_SURFACE,
            surface_id="review_reconstruction_runtime",
            sample_count=sample_count,
            session_count=1,
            event_slice_count=event_slice_count,
            regime_slice_count=regime_slice_count,
            coverage_ratio=coverage_ratio,
            breach_severity=breach_severity,
            persistence_blocks=max(1, len(payload.execution.active_playbook_ids) or 1),
            hysteresis_passed=coverage_ratio >= 0.6,
        )
        trigger_classes: list[ReviewTriggerClass] = []
        if breach_severity in {
            CorridorBreachSeverity.MATERIAL,
            CorridorBreachSeverity.SEVERE,
        }:
            trigger_classes.append(ReviewTriggerClass.MATERIAL_CORRIDOR_BREACH)
        if breach_severity is CorridorBreachSeverity.SEVERE:
            trigger_classes.append(ReviewTriggerClass.SEVERE_CORRIDOR_BREACH)
        if not evidence_block.hysteresis_passed:
            trigger_classes.append(ReviewTriggerClass.PERSISTENCE_FAILURE)
        if coverage_ratio < 0.5:
            trigger_classes.append(ReviewTriggerClass.COVERAGE_COLLAPSE)
        eligible = bool(trigger_classes)
        governed_outcome = ReviewOutcome.REVIEW_NOT_ELIGIBLE
        change_budget = ReviewChangeBudget.NONE
        if eligible and promotion_evidence.ready_for_candidate_review:
            governed_outcome = ReviewOutcome.CANDIDATE_REPLACEMENT_REQUEST
            change_budget = ReviewChangeBudget.CANDIDATE_SWAP_ONLY
        elif eligible:
            governed_outcome = ReviewOutcome.BOUNDED_ADJUSTMENT_REQUEST
            change_budget = ReviewChangeBudget.BOUNDED_SINGLE_SURFACE
        return ReviewEligibilitySurface(
            evidence_block=evidence_block,
            trigger_classes=trigger_classes,
            eligible=eligible,
            governed_outcome=governed_outcome,
            change_budget=change_budget,
        )

    def _stability_scorecards(
        self, review_eligibility: ReviewEligibilitySurface | None
    ) -> list[SurfaceStabilityScorecard]:
        if review_eligibility is None:
            return []
        evidence = review_eligibility.evidence_block
        behaviour_state = (
            BehaviourStabilityState.BREATHING
            if evidence.breach_severity is CorridorBreachSeverity.NONE
            else BehaviourStabilityState.DRIFTING
        )
        return [
            SurfaceStabilityScorecard(
                surface_id=evidence.surface_id,
                surface_class=RuntimeSurfaceClass.REVIEW_ONLY_METRIC,
                metric_observations=[
                    StabilityMetricObservation(
                        axis=ScorecardAxis.ECONOMIC_QUALITY,
                        metric_family=StabilityMetricFamily.COVERAGE,
                        trigger_mode=MetricTriggerMode.REVIEW_TRIGGER,
                        value=evidence.coverage_ratio,
                        notes=["bounded_gate83_review_eligibility_binding"],
                    )
                ],
                corridor=CorridorBounds(
                    central_tendency=evidence.coverage_ratio,
                    tolerated_spread=0.1,
                    target_low=0.8,
                    target_high=1.0,
                    drift_low=0.6,
                    drift_high=1.0,
                    breach_low=0.0,
                    breach_high=1.0,
                ),
                breach_severity=evidence.breach_severity,
                behaviour_state=behaviour_state,
                persistence=PersistenceHysteresisSpec(
                    minimum_blocks=1,
                    confirmation_blocks=1,
                    recovery_blocks=1,
                    cooldown_blocks=0,
                ),
                coverage_slices=[
                    CoverageSliceScore(
                        slice_class=CoverageSliceClass.EVENT_CLASS,
                        slice_label="event_context",
                        observation_count=evidence.event_slice_count,
                        coverage_ratio=1.0 if evidence.event_slice_count else 0.0,
                    ),
                    CoverageSliceScore(
                        slice_class=CoverageSliceClass.REGIME_SLICE,
                        slice_label="regime_context",
                        observation_count=evidence.regime_slice_count,
                        coverage_ratio=1.0 if evidence.regime_slice_count else 0.0,
                    ),
                    CoverageSliceScore(
                        slice_class=CoverageSliceClass.SESSION_SLICE,
                        slice_label="runtime_snapshot",
                        observation_count=evidence.session_count,
                        coverage_ratio=1.0 if evidence.session_count else 0.0,
                    ),
                ],
            )
        ]

    def _candidate_governance(
        self,
        promotion_evidence: PromotionEvidencePacket,
        comparison_context: CandidateComparisonContext | None = None,
    ) -> CandidateGovernanceSurface:
        if promotion_evidence.ready_for_candidate_review and comparison_context is not None:
            return CandidateGovernanceSurface(
                candidate_shape=comparison_context.candidate_shape,
                champion_candidate_id=comparison_context.champion_candidate_id,
                shadow_challenger_ids=list(comparison_context.shadow_challenger_ids),
                dormant_candidate_ids=list(comparison_context.dormant_candidate_ids),
                retired_candidate_ids=list(comparison_context.retired_candidate_ids),
                comparison_outcome=comparison_context.comparison_outcome,
                adjudication_disposition=comparison_context.adjudication_disposition,
            )
        return CandidateGovernanceSurface(
            candidate_shape=CandidateSetShape(
                max_candidate_count=2,
                max_shadow_challengers=0,
                allow_dormant_candidates=True,
                allow_retired_candidates=True,
                reserved_adjudication_spans=1,
            ),
            comparison_outcome=None,
            adjudication_disposition=AdjudicationDisposition.RESERVED_UNTOUCHED,
        )

    def _failure_taxonomy(
        self,
        payload: ReviewExplanationInput,
        conflict_tags: list[str],
        review_eligibility: ReviewEligibilitySurface | None,
    ) -> ReviewFailurePacket:
        runtime_precursor = (
            None
            if payload.temporal_input is None
            else payload.temporal_input.precursor_runtime_packet
        )
        rationale: list[str] = []
        primary_failure_class: ReviewFailureClass | None = None

        if (
            runtime_precursor is not None
            and runtime_precursor.posture_state.value == "unresolved_context"
        ):
            primary_failure_class = ReviewFailureClass.DATA_PROVENANCE_FAILURE
            rationale.append("precursor_runtime_packet_signalled_unresolved_context")

        modifier_kill_switch = None
        if (
            payload.modifier_runtime_packet is not None
            and payload.modifier_runtime_packet.triggered_kill_switch is not None
        ):
            modifier_kill_switch = payload.modifier_runtime_packet.triggered_kill_switch
            rationale.append(f"modifier_kill_switch:{modifier_kill_switch.value}")

        if (
            payload.execution.active_playbook_ids
            and payload.execution.lead_family_id is None
            and payload.eligibility.candidates
        ):
            primary_failure_class = ReviewFailureClass.ONTOLOGY_FAILURE
            rationale.append("active_playbook_without_lead_family")
        if (
            payload.execution.active_playbook_ids
            and payload.execution.inventory_action in {"trim", "hold"}
            and payload.posture.permission_state.value != "block"
        ):
            primary_failure_class = ReviewFailureClass.SIZING_FAILURE
            rationale.append("execution_inventory_action_signalled_sizing_failure")
        if "regime_signal_conflict" in conflict_tags or "posture_signal_conflict" in conflict_tags:
            primary_failure_class = ReviewFailureClass.DIAGNOSIS_FAILURE
            rationale.append("cross_signal_conflict_visible_in_review")
        if "event_veto_breached" in conflict_tags:
            primary_failure_class = ReviewFailureClass.ELIGIBILITY_FAILURE
            rationale.append("event_veto_breach_visible_in_review")
        if any(
            tag in conflict_tags
            for tag in {
                "missing_hedge_under_destabilising_gamma",
                "adding_into_locked_inventory",
            }
        ):
            primary_failure_class = ReviewFailureClass.EXECUTION_EXPRESSION_FAILURE
            rationale.append("execution_expression_conflict_visible_in_review")
        if modifier_kill_switch is not None:
            primary_failure_class = ReviewFailureClass.POSTURE_POLICY_FAILURE

        if payload.execution.active_playbook_ids:
            resolution = ReviewResolutionClass.UNRESOLVED
        elif payload.posture.permission_state.value == "block":
            resolution = ReviewResolutionClass.BLOCKED_TRADE
        elif payload.eligibility.no_trade_reasons:
            resolution = ReviewResolutionClass.NON_ACTION
        else:
            resolution = ReviewResolutionClass.UNKNOWN
        if (
            primary_failure_class is None
            and review_eligibility is not None
            and review_eligibility.evidence_block.breach_severity
            in {CorridorBreachSeverity.MATERIAL, CorridorBreachSeverity.SEVERE}
            and not payload.execution.active_playbook_ids
            and payload.posture.permission_state.value != "block"
        ):
            resolution = ReviewResolutionClass.BAD_LUCK
            rationale.append("bounded_review_surface_lost_without_policy_failure")
        if (
            resolution is ReviewResolutionClass.UNKNOWN
            and primary_failure_class is ReviewFailureClass.ONTOLOGY_FAILURE
        ):
            rationale.append("ontology_failure_selected")

        evidence_floor = None if review_eligibility is None else review_eligibility.evidence_block
        return ReviewFailurePacket(
            primary_failure_class=primary_failure_class,
            resolution=resolution,
            blocked_trade=resolution is ReviewResolutionClass.BLOCKED_TRADE,
            non_action=resolution is ReviewResolutionClass.NON_ACTION,
            evidence_floor=evidence_floor,
            rationale=rationale,
        )

    def _economic_accountability(self, packet: ReviewFailurePacket) -> EconomicContributionPacket:
        diagnosis = EconomicContributionTag.UNKNOWN
        posture = EconomicContributionTag.UNKNOWN
        execution = EconomicContributionTag.UNKNOWN
        non_action = EconomicContributionTag.NEUTRAL
        sizing = EconomicContributionTag.UNKNOWN

        if packet.primary_failure_class is ReviewFailureClass.DIAGNOSIS_FAILURE:
            diagnosis = EconomicContributionTag.VALUE_LEAK
        if packet.primary_failure_class is ReviewFailureClass.EXECUTION_EXPRESSION_FAILURE:
            execution = EconomicContributionTag.VALUE_LEAK
        if packet.primary_failure_class is ReviewFailureClass.SIZING_FAILURE:
            sizing = EconomicContributionTag.VALUE_LEAK
        if packet.resolution in {
            ReviewResolutionClass.NON_ACTION,
            ReviewResolutionClass.BLOCKED_TRADE,
        }:
            posture = EconomicContributionTag.CAPITAL_PRESERVATION
            non_action = EconomicContributionTag.CAPITAL_PRESERVATION
        if packet.resolution is ReviewResolutionClass.BAD_LUCK:
            diagnosis = EconomicContributionTag.NEUTRAL

        return EconomicContributionPacket(
            diagnosis=diagnosis,
            posture=posture,
            timing=EconomicContributionTag.UNKNOWN,
            execution=execution,
            sizing=sizing,
            non_action=non_action,
        )

    def _promotion_evidence(self, lineage: ReviewLineagePacket) -> PromotionEvidencePacket:
        required_sections = [
            "event_lineage_keys",
            "precursor_lineage_keys",
            "modifier_policy_ids",
            "effective_coefficient_targets",
            "posture_change_reasons",
        ]
        missing_sections = [
            section
            for section, values in {
                "event_lineage_keys": lineage.event_lineage_keys,
                "precursor_lineage_keys": lineage.precursor_lineage_keys,
                "modifier_policy_ids": lineage.modifier_policy_ids,
                "effective_coefficient_targets": lineage.effective_coefficient_targets,
                "posture_change_reasons": lineage.posture_change_reasons,
            }.items()
            if not values
        ]
        return PromotionEvidencePacket(
            ready_for_candidate_review=not missing_sections,
            required_sections=required_sections,
            missing_sections=missing_sections,
            notes=["gate77_review_packet_requires_lineage_before_later_candidate_adjudication"],
        )
