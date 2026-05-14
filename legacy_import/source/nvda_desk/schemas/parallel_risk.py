"""Typed contracts for the co-resident independent parallel risk lane.

These contracts preserve the planning-law distinction that the lane is
co-resident with the serial seven-stage desk grammar without becoming an eighth
stage. The lane may read approved invariants from session start and may add
lawful reads of serial-stage outputs once those outputs exist.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.dmp_envelope import DmpV3Envelope, build_dmp_v3_envelope_kwargs

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.events import DeskEventClass


class ParallelRiskReadableStage(StrEnum):
    """Bounded serial-stage names the lane may lawfully read."""

    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"


class ParallelRiskStageReadStatus(StrEnum):
    """Availability and use status for one serial-stage read surface."""

    USED = "used"
    AVAILABLE_NOT_USED = "available_not_used"
    NOT_YET_AVAILABLE = "not_yet_available"


class ParallelRiskGovernanceStatus(StrEnum):
    """Governance status carried for one lane surface or source."""

    INVARIANT_DIRECT_READ = "invariant_direct_read"
    GOVERNED_LIVE_THRESHOLD = "governed_live_threshold"
    FIXED_STRUCTURAL_HEURISTIC = "fixed_structural_heuristic"
    COMPATIBILITY_TIMESTAMP = "compatibility_timestamp"
    DEFERRED_NOT_ADMITTED = "deferred_not_admitted"
    LAWFUL_STAGE_OUTPUT = "lawful_stage_output"


class ParallelRiskInvariantSurface(StrEnum):
    """Approved invariant surfaces readable from session start."""

    SERIAL_GRAMMAR_ORDER = "serial_grammar_order"
    STAGE_OWNERSHIP = "stage_ownership"
    DESK_CALENDAR_CONTRACT = "desk_calendar_contract"
    CALENDAR_HORIZON_ROUTING = "calendar_horizon_routing"
    FINANCIAL_CALENDAR_SCHEDULED_FACT_AUTHORITY = "financial_calendar_scheduled_fact_authority"
    EVENT_IDENTITY = "event_identity"
    RAW_MARKET_FACTS = "raw_market_facts"
    RELEASED_COEFFICIENT_AUTHORITY = "released_coefficient_authority"


class ParallelRiskDependencyActivationState(StrEnum):
    """Bounded dependency activation states for the lane."""

    BACKGROUND_ONLY = "background_only"
    ACTIVE_ENOUGH_TO_MATTER_NOW = "active_enough_to_matter_now"


class ParallelRiskDislocationState(StrEnum):
    """Translation/dislocation classifications preserved by the lane."""

    NEUTRAL = "neutral"
    DISLOCATION_RISK = "dislocation_risk"
    JUSTIFIED_REPRICING = "justified_repricing"
    IMPAIRMENT_RISK = "impairment_risk"


class ParallelRiskEnvironmentalWeatherState(StrEnum):
    """High-level environmental weather labels for the lane."""

    SUPPORTIVE_BACKGROUND = "supportive_background"
    MIXED_TRANSLATION_PRESSURE = "mixed_translation_pressure"
    ELEVATED_TRANSLATION_PRESSURE = "elevated_translation_pressure"
    IMPAIRED_BACKGROUND = "impaired_background"


class ParallelRiskCandidateAuditState(StrEnum):
    """Bounded candidate-audit activation states."""

    INACTIVE_NO_CANDIDATE = "inactive_no_candidate"
    ACTIVE_CANDIDATE = "active_candidate"


class ParallelRiskConsequenceClass(StrEnum):
    """Bounded expression-posture consequence classes."""

    NOT_AT_ALL = "not_at_all"
    WAIT_OR_DEFER = "wait_or_defer"
    SMALLER = "smaller"
    NORMAL = "normal"
    MORE_ASSERTIVE = "more_assertive"
    RESHAPE = "reshape"
    HEDGE_REQUIRED = "hedge_required"
    NO_CARRY = "no_carry"


class ParallelRiskInvariantReadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: ParallelRiskInvariantSurface
    governance_status: ParallelRiskGovernanceStatus
    used: bool = True
    note: str | None = None


class ParallelRiskStageReadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage: ParallelRiskReadableStage
    status: ParallelRiskStageReadStatus
    note: str | None = None


class ParallelRiskTemporalSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_phase: SessionClockPhase
    behavioural_phase: SessionClockPhase | None = None
    desk_window: str
    clock_envelope: str
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    calendar_closure_classes: list[str] = Field(default_factory=list)
    session_bridge_rules: list[str] = Field(default_factory=list)
    next_session_open_hint: datetime | None = None
    event_minutes_remaining: int | None = None
    event_window_state: str
    event_overlap_class: str
    event_risk_timing_class: str
    event_carry_sensitivity: str
    event_timing_profile: str | None = None
    active_event_family: str | None = None
    active_event_class: DeskEventClass | None = None
    expiry_days_remaining: int | None = None
    expiry_cycle_state: str
    session_clock_governance: ParallelRiskGovernanceStatus
    behavioural_phase_governance: ParallelRiskGovernanceStatus
    event_source_governance: ParallelRiskGovernanceStatus
    expiry_source_governance: ParallelRiskGovernanceStatus
    calendar_source_governance: ParallelRiskGovernanceStatus
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ParallelRiskMarketTranslationSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")

    volatility_regime: str
    breadth_state: str
    sector_leadership_state: str
    signal_conflict_state: str
    cross_asset_pressure_score: float
    beta_leadership_score: float
    term_structure_state: str
    gamma_state: str
    dealer_pressure_state: str
    pin_risk_state: str
    options_behavior_cluster: str
    flow_tension_score: float
    strike_cluster_state: str
    repeated_snapshot_state: str
    skew_evolution_state: str
    pin_progression_state: str
    dependency_activation_state: ParallelRiskDependencyActivationState
    active_enough_to_matter_now: bool
    dislocation_state: ParallelRiskDislocationState
    environmental_weather_state: ParallelRiskEnvironmentalWeatherState
    slower_background_context: list[str] = Field(default_factory=list)
    fast_translation_context: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ParallelRiskFragilityDimension(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: str
    state: str
    reasons: list[str] = Field(default_factory=list)


class ParallelRiskCandidateAuditSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_state: ParallelRiskCandidateAuditState
    active_family_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    lead_family_id: str | None = None
    lead_setup_variant_id: str | None = None
    lead_playbook_id: str | None = None
    environmental_weather_state: ParallelRiskEnvironmentalWeatherState
    fragility_dimensions: list[ParallelRiskFragilityDimension] = Field(default_factory=list)
    consequence_class: ParallelRiskConsequenceClass
    anti_duplication_primary_binding_point: str
    descriptive_secondary_reads: list[str] = Field(default_factory=list)
    duplicate_caution_suppressed: bool = True
    notes: list[str] = Field(default_factory=list)


class ParallelRiskLanePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lane_id: str = "independent_parallel_risk_lane"
    serial_spine_preserved: bool = True
    co_resident_from_session_start: bool = True
    arbiter_active: bool = False
    invariant_reads: list[ParallelRiskInvariantReadRecord] = Field(default_factory=list)
    stage_output_reads: list[ParallelRiskStageReadRecord] = Field(default_factory=list)
    temporal_surface: ParallelRiskTemporalSurface
    market_translation_surface: ParallelRiskMarketTranslationSurface | None = None
    candidate_audit_surface: ParallelRiskCandidateAuditSurface | None = None
    notes: list[str] = Field(default_factory=list)


class ParallelRiskLanePacket(DmpV3Envelope[ParallelRiskLanePayload]):
    @property
    def lane_id(self) -> str:
        return self.data.lane_id

    @property
    def serial_spine_preserved(self) -> bool:
        return self.data.serial_spine_preserved

    @property
    def co_resident_from_session_start(self) -> bool:
        return self.data.co_resident_from_session_start

    @property
    def arbiter_active(self) -> bool:
        return self.data.arbiter_active

    @property
    def invariant_reads(self) -> list[ParallelRiskInvariantReadRecord]:
        return self.data.invariant_reads

    @property
    def stage_output_reads(self) -> list[ParallelRiskStageReadRecord]:
        return self.data.stage_output_reads

    @property
    def temporal_surface(self) -> ParallelRiskTemporalSurface:
        return self.data.temporal_surface

    @property
    def market_translation_surface(self) -> ParallelRiskMarketTranslationSurface | None:
        return self.data.market_translation_surface

    @property
    def candidate_audit_surface(self) -> ParallelRiskCandidateAuditSurface | None:
        return self.data.candidate_audit_surface

    def required_market_translation_surface(self) -> ParallelRiskMarketTranslationSurface:
        surface = self.data.market_translation_surface
        if surface is None:
            raise ValueError("parallel risk lane market_translation_surface is required")
        return surface

    def required_candidate_audit_surface(self) -> ParallelRiskCandidateAuditSurface:
        surface = self.data.candidate_audit_surface
        if surface is None:
            raise ValueError("parallel risk lane candidate_audit_surface is required")
        return surface

    @property
    def notes(self) -> list[str]:
        return self.data.notes


PARALLEL_RISK_LANE_MODULE_ID = "independent_parallel_risk_lane"
PARALLEL_RISK_LANE_GRAMMAR_ROLE = "parallel_risk_lane"
PARALLEL_RISK_LANE_DATASCHEMA = "urn:nvda:schema:parallel_risk_lane.output:1.0.0"


def build_parallel_risk_lane_packet(
    *,
    packet_id: str,
    emitted_at: datetime,
    payload: ParallelRiskLanePayload,
    parent_packet_ids: list[str] | None = None,
    dependency_packet_ids: list[str] | None = None,
    source_artifact_ids: list[str] | None = None,
    trace_id: str | None = None,
    run_id: str | None = None,
    scenario_id: str = "live",
) -> ParallelRiskLanePacket:
    keyflags = [
        f"stage_reads={len(payload.stage_output_reads)}",
        f"market_surface={'yes' if payload.market_translation_surface is not None else 'no'}",
        f"candidate_surface={'yes' if payload.candidate_audit_surface is not None else 'no'}",
    ]
    summary = (
        f"parallel-risk lane / market={'set' if payload.market_translation_surface is not None else 'unset'} / "
        f"candidate={'set' if payload.candidate_audit_surface is not None else 'unset'}"
    )
    return ParallelRiskLanePacket(
        **build_dmp_v3_envelope_kwargs(
            packet_id=packet_id,
            emitted_at=emitted_at,
            grammar_role=PARALLEL_RISK_LANE_GRAMMAR_ROLE,
            behaviour_class="module_output",
            payload=payload,
            trader_summary=summary,
            dataschema=PARALLEL_RISK_LANE_DATASCHEMA,
            packetrole="module_output",
            source=f"urn:nvda:producer:{PARALLEL_RISK_LANE_MODULE_ID}",
            packet_type="urn:nvda:packet:parallel_risk_lane.module_output",
            module_id=PARALLEL_RISK_LANE_MODULE_ID,
            module_version="1.0.0",
            module_instance_id=f"{PARALLEL_RISK_LANE_MODULE_ID}::default",
            stage_name=PARALLEL_RISK_LANE_MODULE_ID,
            parent_packet_ids=parent_packet_ids,
            dependency_packet_ids=dependency_packet_ids,
            source_artifact_ids=source_artifact_ids,
            trace_id=trace_id,
            run_id=run_id or f"run::{PARALLEL_RISK_LANE_MODULE_ID}::{emitted_at.isoformat()}",
            scenario_id=scenario_id,
            registry_version="parallel_risk_lane@2.0.0",
            environment_tag="live_runtime",
            dependencies=keyflags,
            summary_keyflags=keyflags,
        )
    )
