"""Review and daily packet contracts.

The review layer reconstructs deterministic decisions, imported-module lineage,
recent execution records, and the Gate 61 non-action/conflict vocabulary that
later review packets must expose explicitly.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.schemas.events import MarketEventPayload
from nvda_desk.schemas.execution_records import (
    CapitalStateSnapshotPayload,
    DailyPnlReportPayload,
    PositionSnapshotPayload,
)
from nvda_desk.schemas.market import (
    DerivedPrecursorField,
    PrecursorContradictionClass,
    PrecursorFallbackDisposition,
    PrecursorPostureState,
    PrecursorVenueUniverse,
    RawPrecursorField,
    SessionAlignmentExpectation,
)
from nvda_desk.schemas.risk import (
    CarryHorizonState,
    DayPhaseState,
    PhaseBehaviourClass,
    PhaseNoActionBias,
)
from nvda_desk.schemas.state_policy import (
    AdjudicationDisposition,
    CandidateComparisonOutcome,
    CandidateSetShape,
    CombinationLaw,
    DegradationStep,
    EventOptionsBehaviourClass,
    EventOptionsStressState,
    KillSwitchCondition,
    ModifierPriorityBand,
    NonActionClass,
    OverrideDisposition,
    PolicyEffectType,
    ResolvedRuntimeSurfaceValue,
    ReviewChangeBudget,
    ReviewEvidenceBlock,
    ReviewOutcome,
    ReviewTriggerClass,
    SignalConflictClass,
)
from nvda_desk.schemas.temporal_surface import (
    EventCarrySensitivity,
    EventOverlapClass,
    EventProximityState,
    EventRiskTimingClass,
    EventWindowState,
)


class ImportedModuleMaturityState(StrEnum):
    """Honest maturity states for imported module review and replay surfaces."""

    CONCEPT_CONTRACT_ONLY = "concept_contract_only"
    IMPLEMENTED_RUNTIME_PROXY = "implemented_runtime_proxy"


class ImportedModuleApprovalState(StrEnum):
    """Explicit non-theatrical approval state for imported modules."""

    NOT_APPROVED = "not_approved"


class ImportedModuleDependencySurface(BaseModel):
    """Review-safe rendering of one imported-module dependency fence."""

    dependency: str = Field(min_length=1)
    status: str = Field(min_length=1)
    note: str = Field(min_length=1)


class ImportedModuleReviewCitation(BaseModel):
    """Review/replay citation for one imported module contract packet."""

    canonical_id: str = Field(min_length=1)
    canonical_slug: str = Field(min_length=1)
    packet_id: str = Field(min_length=1)
    grammar_role: str = Field(min_length=1)
    computation_mode: str = Field(min_length=1)
    maturity_state: ImportedModuleMaturityState
    approval_state: ImportedModuleApprovalState = ImportedModuleApprovalState.NOT_APPROVED
    dependency_fences: list[ImportedModuleDependencySurface] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)




class DownstreamArchitectureReviewSurface(BaseModel):
    """Review-safe downstream architecture receipt surface."""

    policy_freeze_state: str = Field(min_length=1)
    deferred_domains: list[str] = Field(default_factory=list)
    opening_policy_status: str = Field(min_length=1)
    live_inventory_policy_status: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)


class RecordCountSummary(BaseModel):
    """Daily record-count summary for the review surface."""

    signal_event_count: int = Field(ge=0)
    veto_event_count: int = Field(ge=0)
    risk_block_event_count: int = Field(ge=0)
    order_event_count: int = Field(ge=0)
    fill_event_count: int = Field(ge=0)
    position_snapshot_count: int = Field(ge=0)


class ModuleHealthPacket(BaseModel):
    """Per-module health packet shown in daily review."""

    module_id: str = Field(min_length=1)
    evaluation_count: int = Field(ge=0)
    experiment_count: int = Field(ge=0)
    latest_daily_pnl: DailyPnlReportPayload | None = None
    record_counts: RecordCountSummary
    last_signal_at: datetime | None = None
    last_fill_at: datetime | None = None
    open_position_symbols: list[str] = Field(default_factory=list)


class DailyReviewPacket(BaseModel):
    """Top-level daily review packet for capital, positions, and events."""

    requested_at: datetime
    report_date: date
    trade_count: int = Field(ge=0)
    realized_pnl: float
    unrealized_pnl: float
    account_state: CapitalStateSnapshotPayload
    positions: list[PositionSnapshotPayload]
    module_health: list[ModuleHealthPacket]
    recent_events: list[MarketEventPayload]


class ReviewGovernanceSurface(BaseModel):
    """Gate 61 review vocabulary for non-action, conflict, and overrides."""

    stand_down_class: NonActionClass | None = None
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_step: DegradationStep = DegradationStep.NORMAL
    override_disposition: OverrideDisposition = OverrideDisposition.NOT_APPLICABLE
    override_audit_notes: list[str] = Field(default_factory=list)


class TemporalEventWindowSurface(BaseModel):
    """Gate 67 hook exposing bounded event-window semantics to review packets."""

    proximity_state: EventProximityState
    window_state: EventWindowState
    overlap_class: EventOverlapClass = EventOverlapClass.SINGLE_EVENT
    risk_timing_class: EventRiskTimingClass
    carry_sensitivity: EventCarrySensitivity
    timing_profile: str | None = None
    event_family: str = Field(min_length=1)


class PrecursorGovernanceSurface(BaseModel):
    """Gate 68 hook exposing bounded precursor-universe selection to review."""

    active_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment: list[SessionAlignmentExpectation] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PrecursorRuntimeBindingSurface(BaseModel):
    """Gate 76 hook exposing the actual precursor packet seen by runtime and review."""

    requested_at: datetime
    stitched_order: list[PrecursorVenueUniverse] = Field(default_factory=list)
    active_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    missing_venues: list[PrecursorVenueUniverse] = Field(default_factory=list)
    raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    derived_values: dict[DerivedPrecursorField, float] = Field(default_factory=dict)
    contradiction_class: PrecursorContradictionClass = PrecursorContradictionClass.NONE
    posture_state: PrecursorPostureState = PrecursorPostureState.NORMAL_CONFIDENCE
    fallback_dispositions: list[PrecursorFallbackDisposition] = Field(default_factory=list)
    lineage_keys: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PhaseCarryoverPolicySurface(BaseModel):
    """Gate 69 hook exposing bounded phase/carry posture meaning to review."""

    day_phase_state: DayPhaseState
    carry_horizon_state: CarryHorizonState
    behaviour_class: PhaseBehaviourClass
    no_action_bias: PhaseNoActionBias = PhaseNoActionBias.NEUTRAL
    notes: list[str] = Field(default_factory=list)


class EventOptionsStressPolicySurface(BaseModel):
    """Gate 70 hook exposing event/options-stress posture law to review."""

    active_states: list[EventOptionsStressState] = Field(default_factory=list)
    behaviour_class: EventOptionsBehaviourClass
    effect_types: list[PolicyEffectType] = Field(default_factory=list)
    hard_block: bool = False
    notes: list[str] = Field(default_factory=list)


class ModifierControlLawSurface(BaseModel):
    """Gate 71 hook exposing precedence, veto, and kill-switch outcomes."""

    active_precedence_bands: list[ModifierPriorityBand] = Field(default_factory=list)
    applied_combination_laws: list[CombinationLaw] = Field(default_factory=list)
    triggered_kill_switch: KillSwitchCondition | None = None
    suppressed_state_labels: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ReviewEligibilitySurface(BaseModel):
    """Gate 63 hook exposing evidence, triggers, and governed review outcome."""

    evidence_block: ReviewEvidenceBlock
    trigger_classes: list[ReviewTriggerClass] = Field(default_factory=list)
    eligible: bool = False
    governed_outcome: ReviewOutcome = ReviewOutcome.REVIEW_NOT_ELIGIBLE
    change_budget: ReviewChangeBudget = ReviewChangeBudget.NONE


class CandidateGovernanceSurface(BaseModel):
    """Gate 64 hook exposing candidate roles and adjudication state."""

    candidate_shape: CandidateSetShape
    champion_candidate_id: str | None = None
    shadow_challenger_ids: list[str] = Field(default_factory=list)
    dormant_candidate_ids: list[str] = Field(default_factory=list)
    retired_candidate_ids: list[str] = Field(default_factory=list)
    comparison_outcome: CandidateComparisonOutcome | None = None
    adjudication_disposition: AdjudicationDisposition = AdjudicationDisposition.RESERVED_UNTOUCHED


class CandidateComparisonContext(BaseModel):
    """Explicit bounded comparison context required before releasing candidate adjudication."""

    candidate_shape: CandidateSetShape
    champion_candidate_id: str = Field(min_length=1)
    shadow_challenger_ids: list[str] = Field(default_factory=list)
    dormant_candidate_ids: list[str] = Field(default_factory=list)
    retired_candidate_ids: list[str] = Field(default_factory=list)
    comparison_outcome: CandidateComparisonOutcome
    adjudication_disposition: AdjudicationDisposition = (
        AdjudicationDisposition.RELEASED_FOR_FINAL_COMPARISON
    )


class ReviewFailureClass(StrEnum):
    """Trader-grade failure classes frozen by Gate 77."""

    DIAGNOSIS_FAILURE = "diagnosis_failure"
    POSTURE_POLICY_FAILURE = "posture_policy_failure"
    ELIGIBILITY_FAILURE = "eligibility_failure"
    EXECUTION_EXPRESSION_FAILURE = "execution_expression_failure"
    SIZING_FAILURE = "sizing_failure"
    DATA_PROVENANCE_FAILURE = "data_provenance_failure"
    ONTOLOGY_FAILURE = "ontology_failure"


class ReviewResolutionClass(StrEnum):
    """Bounded review outputs for action, non-action, ambiguity, and structural failure."""

    ACTION_TAKEN = "action_taken"
    NON_ACTION = "non_action"
    BLOCKED_TRADE = "blocked_trade"
    UNKNOWN = "unknown"
    UNRESOLVED = "unresolved"
    BAD_LUCK = "bad_luck"
    ONTOLOGY_FAILURE = "ontology_failure"


class EconomicContributionTag(StrEnum):
    """Directional economic-accountability labels used by Gate 77 review packets."""

    VALUE_ADD = "value_add"
    CAPITAL_PRESERVATION = "capital_preservation"
    NEUTRAL = "neutral"
    VALUE_LEAK = "value_leak"
    UNKNOWN = "unknown"


class ReviewLineagePacket(BaseModel):
    """Review-visible lineage needed to reconstruct event, precursor, and modifier truth."""

    event_lineage_keys: list[str] = Field(default_factory=list)
    precursor_lineage_keys: list[str] = Field(default_factory=list)
    modifier_policy_ids: list[str] = Field(default_factory=list)
    effective_coefficient_targets: list[str] = Field(default_factory=list)
    resolved_surfaces: list[ResolvedRuntimeSurfaceValue] = Field(default_factory=list)
    posture_change_reasons: list[str] = Field(default_factory=list)


class ReviewFailurePacket(BaseModel):
    """Bounded failure-taxonomy packet for one runtime decision or non-decision."""

    primary_failure_class: ReviewFailureClass | None = None
    resolution: ReviewResolutionClass
    blocked_trade: bool = False
    non_action: bool = False
    evidence_floor: ReviewEvidenceBlock | None = None
    rationale: list[str] = Field(default_factory=list)


class EconomicContributionPacket(BaseModel):
    """Economic-accountability fields kept separate from raw P&L narration."""

    diagnosis: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    posture: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    timing: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    execution: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    sizing: EconomicContributionTag = EconomicContributionTag.UNKNOWN
    non_action: EconomicContributionTag = EconomicContributionTag.NEUTRAL


class PromotionEvidencePacket(BaseModel):
    """Minimum trader-grade review packet required before later candidate adjudication."""

    ready_for_candidate_review: bool = False
    required_sections: list[str] = Field(default_factory=list)
    missing_sections: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
