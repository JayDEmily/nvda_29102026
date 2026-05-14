"""Co-resident independent parallel risk-lane service.

This service materialises the bounded Gate 174-177 runtime surface only:
- lawful invariant reads from session start
- lawful temporal/calendar/event/multi-clock surface after temporal evaluation
- bounded market/options/dependency/dislocation translation surfaces
- descriptive candidate-aware anti-duplication semantics

It does not implement final arbitration, playbook-internal logic, or a second
caution engine.
"""

from __future__ import annotations

from nvda_desk.schemas.calibration import (
    ParallelRiskLaneEvaluationPreparationPacket,
    ParallelRiskLanePolicyCalibrationMetadata,
    ParallelRiskLaneSurfaceCalibrationMetadata,
)
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextInput,
    TemporalContextOutput,
)
from nvda_desk.schemas.dmp_envelope import DmpV3Envelope
from nvda_desk.schemas.parallel_risk import (
    ParallelRiskCandidateAuditState,
    ParallelRiskCandidateAuditSurface,
    ParallelRiskConsequenceClass,
    ParallelRiskDependencyActivationState,
    ParallelRiskDislocationState,
    ParallelRiskEnvironmentalWeatherState,
    ParallelRiskFragilityDimension,
    ParallelRiskGovernanceStatus,
    ParallelRiskInvariantReadRecord,
    ParallelRiskInvariantSurface,
    ParallelRiskLanePacket,
    ParallelRiskLanePayload,
    ParallelRiskMarketTranslationSurface,
    ParallelRiskReadableStage,
    ParallelRiskStageReadRecord,
    ParallelRiskStageReadStatus,
    ParallelRiskTemporalSurface,
    build_parallel_risk_lane_packet,
)


class ParallelRiskLaneService:
    def evaluate(
        self,
        *,
        temporal_input_packet: DmpV3Envelope[TemporalContextInput],
        temporal_packet: DmpV3Envelope[TemporalContextOutput],
    ) -> ParallelRiskLanePacket:
        temporal_input = temporal_input_packet.data
        temporal = temporal_packet.data
        event_governance = (
            ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ
            if temporal_input.live_event_snapshot is not None
            else ParallelRiskGovernanceStatus.COMPATIBILITY_TIMESTAMP
            if temporal_input.next_event_at is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        expiry_governance = (
            ParallelRiskGovernanceStatus.COMPATIBILITY_TIMESTAMP
            if temporal_input.next_expiry is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        calendar_governance = (
            ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ
            if temporal_input.desk_calendar_authority is not None
            else ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED
        )
        lineage_keys: list[str] = []
        active_event_class = None
        if temporal_input.live_event_snapshot is not None:
            lineage_keys.extend(temporal_input.live_event_snapshot.lineage_keys)
            next_event = temporal_input.live_event_snapshot.next_event
            active_event_class = None if next_event is None else next_event.event_class
            if next_event is not None:
                lineage_keys.extend(next_event.lineage_keys)
        invariants = [
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.SERIAL_GRAMMAR_ORDER, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="seven-stage serial spine remains binding"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.STAGE_OWNERSHIP, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="parallel lane is co-resident and additive only"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.DESK_CALENDAR_CONTRACT, governance_status=calendar_governance, used=temporal_input.desk_calendar_authority is not None, note="direct read allowed from session start when desk calendar packet is present"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.CALENDAR_HORIZON_ROUTING, governance_status=calendar_governance, used=temporal_input.desk_calendar_authority is not None, note="calendar horizon routing read remains descriptive in Gate 174-175"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.FINANCIAL_CALENDAR_SCHEDULED_FACT_AUTHORITY, governance_status=event_governance, used=temporal_input.live_event_snapshot is not None or temporal_input.next_event_at is not None, note="live event snapshot wins; compatibility timestamp remains subordinate fallback"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.EVENT_IDENTITY, governance_status=event_governance, used=temporal_input.live_event_snapshot is not None or temporal_input.next_event_at is not None, note="event identity is read, not rewritten, by the lane"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.RAW_MARKET_FACTS, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, note="raw market facts remain serial-spine facts, not lane inventions"),
            ParallelRiskInvariantReadRecord(surface=ParallelRiskInvariantSurface.RELEASED_COEFFICIENT_AUTHORITY, governance_status=ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, used=False, note="baseline authority remains released and immutable; active coefficient reads are deferred in Gate 174-177"),
        ]
        stage_reads = [
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.TEMPORAL, status=ParallelRiskStageReadStatus.USED, note="temporal output is the first lawful stage output the lane may consume"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.REGIME, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175 bootstrap packet"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.OPTIONS_FLOW, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175 bootstrap packet"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.POSTURE, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175 bootstrap packet"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.ELIGIBILITY, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175 bootstrap packet"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.EXECUTION, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="not read in Gate 174-175 bootstrap packet"),
            ParallelRiskStageReadRecord(stage=ParallelRiskReadableStage.REVIEW, status=ParallelRiskStageReadStatus.NOT_YET_AVAILABLE, note="review remains downstream of lane creation"),
        ]
        temporal_surface = ParallelRiskTemporalSurface(
            session_phase=temporal.session_phase,
            behavioural_phase=temporal.behavioural_phase,
            desk_window=temporal.desk_window,
            clock_envelope=temporal.clock_envelope,
            minutes_since_open=temporal.minutes_since_open,
            minutes_to_close=temporal.minutes_to_close,
            calendar_closure_classes=list(temporal.calendar_closure_classes),
            session_bridge_rules=list(temporal.session_bridge_rules),
            next_session_open_hint=temporal.next_session_open_hint,
            event_minutes_remaining=temporal.event_minutes_remaining,
            event_window_state=temporal.event_window_state,
            event_overlap_class=temporal.event_overlap_class,
            event_risk_timing_class=temporal.event_risk_timing_class,
            event_carry_sensitivity=temporal.event_carry_sensitivity,
            event_timing_profile=temporal.event_timing_profile,
            active_event_family=temporal.active_event_family,
            active_event_class=active_event_class,
            expiry_days_remaining=temporal.expiry_days_remaining,
            expiry_cycle_state=temporal.expiry_cycle_state,
            session_clock_governance=ParallelRiskGovernanceStatus.FIXED_STRUCTURAL_HEURISTIC,
            behavioural_phase_governance=ParallelRiskGovernanceStatus.GOVERNED_LIVE_THRESHOLD,
            event_source_governance=event_governance,
            expiry_source_governance=expiry_governance,
            calendar_source_governance=calendar_governance,
            lineage_keys=lineage_keys,
            notes=[
                "co_resident_lane_created_after_temporal_stage_only",
                "no_arbiter_behavior_in_gate_174_175",
                "live_event_snapshot_subordinates_next_event_at_when_both_are_present" if temporal_input.live_event_snapshot is not None and temporal_input.next_event_at is not None else "event_source_selection_is_single_surface",
            ],
        )
        return build_parallel_risk_lane_packet(
            packet_id=f"parallel-risk::temporal::{temporal_input.ts.isoformat()}",
            emitted_at=temporal_input.ts,
            payload=ParallelRiskLanePayload(
                invariant_reads=invariants,
                stage_output_reads=stage_reads,
                temporal_surface=temporal_surface,
                notes=[
                    "co_resident_from_session_start",
                    "not_step_1_1",
                    "not_step_8",
                    "not_eighth_stage",
                    "descriptive_and_diagnostic_only_in_gate_174_177",
                ],
            ),
            dependency_packet_ids=[temporal_input_packet.packet_id, temporal_packet.packet_id],
            source_artifact_ids=[
                *list(temporal_input_packet.lineage.sourceartifactids),
                *list(temporal_packet.lineage.sourceartifactids),
            ],
            trace_id=temporal_packet.traceid,
            run_id=temporal_packet.runid,
            scenario_id=temporal_packet.scenarioid,
        )

    def enrich_market_translation(
        self,
        *,
        packet: ParallelRiskLanePacket,
        regime_packet: DmpV3Envelope[MarketRegimeContextOutput],
        options_flow_packet: DmpV3Envelope[OptionsFlowContextOutput],
    ) -> ParallelRiskLanePacket:
        regime = regime_packet.data
        options_flow = options_flow_packet.data
        active_enough_to_matter_now = bool(
            packet.temporal_surface.active_event_family
            or options_flow.gamma_state.value == "destabilising"
            or options_flow.flow_tension_score >= 0.30
            or regime.signal_conflict_state != "aligned_regime"
            or abs(regime.cross_asset_pressure_score) >= 0.50
        )
        dependency_activation_state = (
            ParallelRiskDependencyActivationState.ACTIVE_ENOUGH_TO_MATTER_NOW
            if active_enough_to_matter_now
            else ParallelRiskDependencyActivationState.BACKGROUND_ONLY
        )
        dislocation_state = self._dislocation_state(regime, options_flow)
        weather_state = self._environmental_weather_state(regime, options_flow, dislocation_state)
        surface = ParallelRiskMarketTranslationSurface(
            volatility_regime=regime.volatility_regime.value,
            breadth_state=regime.breadth_state.value,
            sector_leadership_state=regime.sector_leadership_state,
            signal_conflict_state=regime.signal_conflict_state,
            cross_asset_pressure_score=regime.cross_asset_pressure_score,
            beta_leadership_score=regime.beta_leadership_score,
            term_structure_state=options_flow.term_structure_state.value,
            gamma_state=options_flow.gamma_state.value,
            dealer_pressure_state=options_flow.dealer_pressure_state,
            pin_risk_state=options_flow.pin_risk_state,
            options_behavior_cluster=options_flow.options_behavior_cluster,
            flow_tension_score=options_flow.flow_tension_score,
            strike_cluster_state=options_flow.strike_cluster_state,
            repeated_snapshot_state=options_flow.repeated_snapshot_state,
            skew_evolution_state=options_flow.skew_evolution_state,
            pin_progression_state=options_flow.pin_progression_state,
            dependency_activation_state=dependency_activation_state,
            active_enough_to_matter_now=active_enough_to_matter_now,
            dislocation_state=dislocation_state,
            environmental_weather_state=weather_state,
            slower_background_context=[
                f"volatility_regime:{regime.volatility_regime.value}",
                f"breadth_state:{regime.breadth_state.value}",
                f"sector_leadership_state:{regime.sector_leadership_state}",
                f"rates_regime_state:{regime.rates_regime_state}",
                f"fx_stress_state:{regime.fx_stress_state}",
            ],
            fast_translation_context=[
                f"gamma_state:{options_flow.gamma_state.value}",
                f"dealer_pressure_state:{options_flow.dealer_pressure_state}",
                f"options_behavior_cluster:{options_flow.options_behavior_cluster}",
                f"repeated_snapshot_state:{options_flow.repeated_snapshot_state}",
                f"pin_progression_state:{options_flow.pin_progression_state}",
            ],
            notes=[
                "options_table_used_as_translation_surface",
                "dependency_filter_bounded_to_active_enough_to_matter_now",
                "market_translation_surface_is_descriptive_not_arbiter",
            ],
        )
        return build_parallel_risk_lane_packet(
            packet_id=f"parallel-risk::market_translation::{packet.time.isoformat()}",
            emitted_at=packet.time,
            payload=packet.data.model_copy(
                update={
                    "market_translation_surface": surface,
                    "stage_output_reads": self._updated_stage_reads(
                        packet.stage_output_reads,
                        {
                            ParallelRiskReadableStage.REGIME: ParallelRiskStageReadStatus.USED,
                            ParallelRiskReadableStage.OPTIONS_FLOW: ParallelRiskStageReadStatus.USED,
                        },
                        {
                            ParallelRiskReadableStage.REGIME: "market weather read used in Gate 176",
                            ParallelRiskReadableStage.OPTIONS_FLOW: "options translation read used in Gate 176",
                        },
                    ),
                    "notes": [*packet.notes, "market_and_options_translation_surface_added_in_gate_176"],
                }
            ),
            parent_packet_ids=[packet.packet_id],
            dependency_packet_ids=[packet.packet_id, regime_packet.packet_id, options_flow_packet.packet_id],
            source_artifact_ids=list(packet.lineage.sourceartifactids),
            trace_id=packet.traceid,
            run_id=packet.runid,
            scenario_id=packet.scenarioid,
        )

    def enrich_candidate_semantics(
        self,
        *,
        packet: ParallelRiskLanePacket,
        posture_packet: DmpV3Envelope[PostureRiskOutput],
        eligibility_packet: DmpV3Envelope[PlaybookEligibilityOutput],
        execution_packet: DmpV3Envelope[ExecutionExpressionOutput],
    ) -> ParallelRiskLanePacket:
        posture = posture_packet.data
        eligibility = eligibility_packet.data
        execution = execution_packet.data
        market_surface = packet.market_translation_surface
        weather_state = (
            market_surface.environmental_weather_state
            if market_surface is not None
            else ParallelRiskEnvironmentalWeatherState.MIXED_TRANSLATION_PRESSURE
        )
        candidate_present = bool(execution.active_playbook_ids or execution.active_setup_variant_ids or execution.active_family_ids)
        fragility_dimensions = self._fragility_dimensions(packet, posture, execution)
        consequence = self._consequence_class(posture, execution, candidate_present)
        if candidate_present:
            primary_binding = self._primary_binding_point(posture, execution)
            secondary_reads = [
                "parallel_risk_environmental_weather",
                "execution_expression_output",
            ]
            candidate_state = ParallelRiskCandidateAuditState.ACTIVE_CANDIDATE
            notes = [
                "candidate_specific_audit_active",
                "lane_describes_action_shape_without_arbiter_authority",
            ]
        else:
            primary_binding = "not_applicable_no_candidate"
            secondary_reads = ["environmental_weather_only"]
            candidate_state = ParallelRiskCandidateAuditState.INACTIVE_NO_CANDIDATE
            notes = [
                "no_candidate_specific_audit_without_execution_candidate",
                "environmental_weather_preserved_without_second_caution_engine",
            ]
        candidate_surface = ParallelRiskCandidateAuditSurface(
            candidate_state=candidate_state,
            active_family_ids=list(execution.active_family_ids),
            active_setup_variant_ids=list(execution.active_setup_variant_ids),
            lead_family_id=execution.lead_family_id,
            lead_setup_variant_id=execution.lead_setup_variant_id,
            lead_playbook_id=execution.lead_playbook_id,
            environmental_weather_state=weather_state,
            fragility_dimensions=fragility_dimensions,
            consequence_class=consequence,
            anti_duplication_primary_binding_point=primary_binding,
            descriptive_secondary_reads=secondary_reads,
            duplicate_caution_suppressed=True,
            notes=notes,
        )
        return build_parallel_risk_lane_packet(
            packet_id=f"parallel-risk::candidate_semantics::{packet.time.isoformat()}",
            emitted_at=packet.time,
            payload=packet.data.model_copy(
                update={
                    "candidate_audit_surface": candidate_surface,
                    "stage_output_reads": self._updated_stage_reads(
                        packet.stage_output_reads,
                        {
                            ParallelRiskReadableStage.POSTURE: ParallelRiskStageReadStatus.USED,
                            ParallelRiskReadableStage.ELIGIBILITY: ParallelRiskStageReadStatus.USED,
                            ParallelRiskReadableStage.EXECUTION: ParallelRiskStageReadStatus.USED,
                        },
                        {
                            ParallelRiskReadableStage.POSTURE: "posture read used for descriptive consequence classes in Gate 177",
                            ParallelRiskReadableStage.ELIGIBILITY: "eligibility read used to preserve candidate-aware semantics in Gate 177",
                            ParallelRiskReadableStage.EXECUTION: "execution read used to preserve candidate-specific action-shape semantics in Gate 177",
                        },
                    ),
                    "notes": [*packet.notes, "candidate_semantics_added_in_gate_177", "no_distributed_caution_fog"],
                }
            ),
            parent_packet_ids=[packet.packet_id],
            dependency_packet_ids=[packet.packet_id, posture_packet.packet_id, eligibility_packet.packet_id, execution_packet.packet_id],
            source_artifact_ids=list(packet.lineage.sourceartifactids),
            trace_id=packet.traceid,
            run_id=packet.runid,
            scenario_id=packet.scenarioid,
        )

    def build_evaluation_preparation_packet(
        self,
        *,
        packet: ParallelRiskLanePacket,
    ) -> ParallelRiskLaneEvaluationPreparationPacket:
        """Build the lean Gate 178 evaluation-prep packet for implemented lane slices."""

        implemented_surfaces = ["temporal_surface"]
        surface_metadata = [
            ParallelRiskLaneSurfaceCalibrationMetadata(
                surface_id="temporal_surface",
                behavioural_purpose="Preserve session-phase, calendar, event, and expiry timing semantics for the co-resident lane without mutating serial-stage truth.",
                expected_directionality="Richer timing/event detail should improve risk-read timing sensitivity rather than widen authority.",
                anti_goal="Do not let timing metadata become a hidden arbiter or duplicate the temporal stage.",
                owner_stage="temporal_context",
                surface_family="timing_governance",
                review_cadence="per implementation tranche and before later paper-testing",
                activation_state="active_runtime",
                evidence_sources=[
                    "parallel_risk_lane.temporal_surface",
                    "temporal_context_output",
                    "desk_calendar_authority",
                ],
            )
        ]
        policy_metadata = [
            ParallelRiskLanePolicyCalibrationMetadata(
                policy_id="parallel_risk:temporal_calendar_multi_clock",
                policy_family="timing_governance",
                primary_target_surface="temporal_surface",
                behavioural_purpose="Keep the lane anchored to lawful session/event/expiry clocks and calendar-source governance.",
                expected_effect="The lane should become more timing-aware without changing coefficient authority or serial grammar order.",
                anti_goal="Do not let timing reads manufacture new runtime permission states.",
                over_tightening_signs=["event timing labels appear to suppress candidates without candidate-specific evidence"],
                redundancy_signs=["the lane restates temporal stage facts without adding any distinct timing interpretation"],
                danger_signs=["compatibility timestamps override live scheduled-fact authority"],
                review_cadence="per implementation tranche and before later paper-testing",
                evidence_sources=["parallel_risk_lane.temporal_surface", "review.parallel_risk_lane"],
            )
        ]
        if packet.market_translation_surface is not None:
            implemented_surfaces.append("market_translation_surface")
            surface_metadata.append(
                ParallelRiskLaneSurfaceCalibrationMetadata(
                    surface_id="market_translation_surface",
                    behavioural_purpose="Translate regime and options-flow context into dependency activation, dislocation, and environmental-weather semantics.",
                    expected_directionality="When translation pressure rises, the lane should describe more impairment or dislocation risk without becoming a second caution engine.",
                    anti_goal="Do not convert options-table interpretation into automatic veto or duplicate serial-stage market logic.",
                    owner_stage="independent_parallel_risk_lane",
                    surface_family="translation_semantics",
                    review_cadence="per implementation tranche and before later paper-testing",
                    activation_state="active_runtime",
                    evidence_sources=[
                        "parallel_risk_lane.market_translation_surface",
                        "market_regime_context_output",
                        "options_flow_context_output",
                    ],
                )
            )
            policy_metadata.append(
                ParallelRiskLanePolicyCalibrationMetadata(
                    policy_id="parallel_risk:market_options_dependency_translation",
                    policy_family="translation_semantics",
                    primary_target_surface="market_translation_surface",
                    behavioural_purpose="Classify whether options and cross-asset conditions are active enough to matter now and whether the resulting pressure is dislocation, justified repricing, or impairment.",
                    expected_effect="The lane should become more descriptive about translation pressure and environmental weather without taking arbiter authority.",
                    anti_goal="Do not treat every stressed options state as the same thing or smuggle extra risk caps into the serial spine.",
                    over_tightening_signs=["translation labels always collapse to impairment regardless of breadth or volatility context"],
                    redundancy_signs=["the lane repeats regime/options summaries without changing the descriptive classification"],
                    danger_signs=["dislocation and impairment classifications stop staying distinct"],
                    review_cadence="per implementation tranche and before later paper-testing",
                    evidence_sources=["parallel_risk_lane.market_translation_surface", "review.parallel_risk_lane_summary"],
                )
            )
        if packet.candidate_audit_surface is not None:
            implemented_surfaces.append("candidate_audit_surface")
            surface_metadata.append(
                ParallelRiskLaneSurfaceCalibrationMetadata(
                    surface_id="candidate_audit_surface",
                    behavioural_purpose="Separate environmental weather from candidate-specific fragility and preserve one descriptive primary binding point per active candidate shape.",
                    expected_directionality="As fragility rises, the lane should describe reshaping, waiting, or hedge-required consequences without duplicating serial-stage caution ownership.",
                    anti_goal="Do not create distributed caution fog or a silent second owner for vetoes and deployable-capital clamps.",
                    owner_stage="independent_parallel_risk_lane",
                    surface_family="candidate_audit",
                    review_cadence="per implementation tranche and before later paper-testing",
                    activation_state="active_runtime",
                    evidence_sources=[
                        "parallel_risk_lane.candidate_audit_surface",
                        "execution_expression_output",
                        "review.parallel_risk_lane_summary",
                    ],
                )
            )
            policy_metadata.append(
                ParallelRiskLanePolicyCalibrationMetadata(
                    policy_id="parallel_risk:candidate_fragility_anti_duplication",
                    policy_family="candidate_audit",
                    primary_target_surface="candidate_audit_surface",
                    behavioural_purpose="Keep candidate-aware fragility, consequence, and anti-duplication semantics inspectable while preserving the serial spine as the only primary caution owner.",
                    expected_effect="Candidate-specific audits should explain shape changes and suppressed duplicate caution rather than widen runtime authority.",
                    anti_goal="Do not let candidate fragility labels become a hidden arbiter or second caution stack.",
                    over_tightening_signs=["candidate audits always imply smaller or no-carry regardless of execution shape"],
                    redundancy_signs=["candidate audit mirrors execution output with no distinct fragility information"],
                    danger_signs=["anti_duplication_primary_binding_point drifts away from the serial owner actually binding the decision"],
                    review_cadence="per implementation tranche and before later paper-testing",
                    evidence_sources=["parallel_risk_lane.candidate_audit_surface", "review.parallel_risk_lane"],
                )
            )
        return ParallelRiskLaneEvaluationPreparationPacket(
            lane_id=packet.lane_id,
            implemented_surfaces=implemented_surfaces,
            surface_metadata=surface_metadata,
            policy_metadata=policy_metadata,
            notes=[
                "gate_178_preparatory_only",
                "selective_proof_order_is_bounded",
                "calibration_has_not_started",
            ],
        )

    def _updated_stage_reads(
        self,
        records: list[ParallelRiskStageReadRecord],
        statuses: dict[ParallelRiskReadableStage, ParallelRiskStageReadStatus],
        notes: dict[ParallelRiskReadableStage, str],
    ) -> list[ParallelRiskStageReadRecord]:
        updated: list[ParallelRiskStageReadRecord] = []
        for record in records:
            stage = record.stage
            updated.append(
                record.model_copy(
                    update={
                        "status": statuses.get(stage, record.status),
                        "note": notes.get(stage, record.note),
                    }
                )
            )
        return updated

    def _dislocation_state(
        self,
        regime: MarketRegimeContextOutput,
        options_flow: OptionsFlowContextOutput,
    ) -> ParallelRiskDislocationState:
        if regime.volatility_regime.value == "stressed" and regime.breadth_state.value == "weak":
            return ParallelRiskDislocationState.IMPAIRMENT_RISK
        if options_flow.gamma_state.value == "destabilising" and regime.signal_conflict_state == "aligned_regime" and regime.breadth_state.value == "supportive":
            return ParallelRiskDislocationState.DISLOCATION_RISK
        if abs(regime.cross_asset_pressure_score) >= 0.50 or regime.signal_conflict_state != "aligned_regime":
            return ParallelRiskDislocationState.JUSTIFIED_REPRICING
        return ParallelRiskDislocationState.NEUTRAL

    def _environmental_weather_state(
        self,
        regime: MarketRegimeContextOutput,
        options_flow: OptionsFlowContextOutput,
        dislocation_state: ParallelRiskDislocationState,
    ) -> ParallelRiskEnvironmentalWeatherState:
        if dislocation_state is ParallelRiskDislocationState.IMPAIRMENT_RISK:
            return ParallelRiskEnvironmentalWeatherState.IMPAIRED_BACKGROUND
        if regime.volatility_regime.value == "calm" and regime.breadth_state.value == "supportive" and options_flow.gamma_state.value != "destabilising":
            return ParallelRiskEnvironmentalWeatherState.SUPPORTIVE_BACKGROUND
        if dislocation_state is ParallelRiskDislocationState.DISLOCATION_RISK:
            return ParallelRiskEnvironmentalWeatherState.ELEVATED_TRANSLATION_PRESSURE
        return ParallelRiskEnvironmentalWeatherState.MIXED_TRANSLATION_PRESSURE

    def _fragility_dimensions(
        self,
        packet: ParallelRiskLanePacket,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
    ) -> list[ParallelRiskFragilityDimension]:
        market_surface = packet.market_translation_surface
        translation_state = "elevated" if market_surface and market_surface.dislocation_state is not ParallelRiskDislocationState.NEUTRAL else "contained"
        timing_state = "elevated" if packet.temporal_surface.event_window_state != "no_event_window" else "contained"
        carry_state = "restricted" if packet.temporal_surface.event_carry_sensitivity != "carry_neutral" else "contained"
        execution_state = "elevated" if execution.hedge_required or execution.entry_style == "stand_aside" else "contained"
        structural_state = "elevated" if posture.permission_state.value in {"block", "derisk"} else "contained"
        dependency_state = "elevated" if market_surface and market_surface.active_enough_to_matter_now else "background"
        event_state = "elevated" if packet.temporal_surface.active_event_family is not None else "contained"
        return [
            ParallelRiskFragilityDimension(dimension="structural_fragility", state=structural_state, reasons=[f"permission_state:{posture.permission_state.value}"]),
            ParallelRiskFragilityDimension(dimension="dependency_fragility", state=dependency_state, reasons=[f"dependency_active:{market_surface.active_enough_to_matter_now if market_surface else False}"]),
            ParallelRiskFragilityDimension(dimension="event_fragility", state=event_state, reasons=[f"event_window_state:{packet.temporal_surface.event_window_state}"]),
            ParallelRiskFragilityDimension(dimension="translation_fragility", state=translation_state, reasons=[f"gamma_state:{market_surface.gamma_state if market_surface else 'unset'}"]),
            ParallelRiskFragilityDimension(dimension="timing_fragility", state=timing_state, reasons=[f"event_overlap_class:{packet.temporal_surface.event_overlap_class}"]),
            ParallelRiskFragilityDimension(dimension="carry_fragility", state=carry_state, reasons=[f"event_carry_sensitivity:{packet.temporal_surface.event_carry_sensitivity}"]),
            ParallelRiskFragilityDimension(dimension="execution_fragility", state=execution_state, reasons=[f"entry_style:{execution.entry_style}", f"hedge_required:{execution.hedge_required}"]),
        ]

    def _consequence_class(
        self,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
        candidate_present: bool,
    ) -> ParallelRiskConsequenceClass:
        if not candidate_present:
            return ParallelRiskConsequenceClass.NO_CARRY
        if posture.permission_state.value == "block":
            return ParallelRiskConsequenceClass.NOT_AT_ALL
        if execution.entry_style == "stand_aside":
            return ParallelRiskConsequenceClass.WAIT_OR_DEFER
        if execution.hedge_required:
            return ParallelRiskConsequenceClass.HEDGE_REQUIRED
        recommendation_target_pct = self._recommendation_target_pct(posture, execution)
        if execution.inventory_action == "reduce" or recommendation_target_pct < 50.0:
            return ParallelRiskConsequenceClass.SMALLER
        if execution.fresh_capital_action == "probe":
            return ParallelRiskConsequenceClass.RESHAPE
        return ParallelRiskConsequenceClass.NORMAL

    def _primary_binding_point(
        self,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
    ) -> str:
        if posture.permission_state.value in {"block", "derisk"}:
            return "posture_risk_output"
        if execution.hedge_required:
            return "execution_expression_output"
        recommendation_target_pct = self._recommendation_target_pct(posture, execution)
        if recommendation_target_pct < 100.0 or execution.inventory_action in {"trim", "reduce"}:
            return "execution_expression_output"
        return "candidate_shape_descriptive_only"

    def _recommendation_target_pct(
        self,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
    ) -> float:
        """Return the bounded recommendation total from posture and lawful serial shape."""

        shape_sum = round(sum(execution.scaling_plan), 4) if execution.scaling_plan else 0.0
        if shape_sum <= 0.0 or shape_sum > 1.0:
            return 0.0
        return round(max(0.0, min(100.0, posture.fresh_deployable_capital_pct * shape_sum)), 4)
