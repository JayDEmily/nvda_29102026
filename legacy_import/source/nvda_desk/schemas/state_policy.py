"""Binding state-policy and non-action authority contracts.

Gate 60 freezes what kind of runtime surface is allowed to vary, which state
fields modifiers may read, and which transform family is lawful. Gate 61 then
freezes non-action, conflict, degradation, and override law before later policy
matrices or runtime wiring can rely on informal desk language.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PolicyStageOwner(StrEnum):
    """Canonical owner stages for state-policy and conflict governance."""

    CALENDAR_HORIZON = "calendar_horizon"
    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"
    EVENT = "event"
    PRECURSOR = "precursor"


class RuntimeSurfaceClass(StrEnum):
    """Lawful ontology for surfaces mentioned by adaptation policy."""

    INVARIANT = "invariant"
    BASELINE_COEFFICIENT = "baseline_coefficient"
    STATE_CONDITIONED_MODIFIER = "state_conditioned_modifier"
    EFFECTIVE_COEFFICIENT = "effective_coefficient"
    REVIEW_ONLY_METRIC = "review_only_metric"
    PROHIBITED_RUNTIME_VARIATION = "prohibited_runtime_variation"


class ModifierTransformType(StrEnum):
    """Bounded transform family approved for state-conditioned modifiers."""

    MULTIPLICATIVE_SCALE = "multiplicative_scale"
    ADDITIVE_OFFSET = "additive_offset"
    CLAMP = "clamp"
    RANK_WEIGHT_ADJUSTMENT = "rank_weight_adjustment"
    SUPPRESSION_VETO = "suppression_veto"


class MutableRuntimeSurface(StrEnum):
    """Runtime surfaces that may lawfully receive approved modifier policy."""

    ENTRY_GATE_SCORE_FLOOR = "entry_gate_score_floor"
    ZONE_SCORE_THRESHOLD = "zone_score_threshold"
    DISTANCE_TO_VWAP_SOFT_LIMIT_PCT = "distance_to_vwap_soft_limit_pct"
    RISK_VIX_CAUTION_THRESHOLD = "risk_vix_caution_threshold"
    RISK_VIX_HOT_THRESHOLD = "risk_vix_hot_threshold"
    MAX_RISK_PER_TRADE = "max_risk_per_trade"
    TARGET_FRESH_DEPLOYABLE_PCT = "target_fresh_deployable_pct"
    HEDGE_REQUIRED = "hedge_required"


class ProhibitedRuntimeSurface(StrEnum):
    """Surfaces that must never vary through runtime state-conditioned policy."""

    DESK_COGNITION_GRAMMAR_ORDER = "desk_cognition_grammar_order"
    STAGE_OWNER_ASSIGNMENTS = "stage_owner_assignments"
    BASELINE_COEFFICIENT_VALUES = "baseline_coefficient_values"
    CALENDAR_TRUTH = "calendar_truth"
    EVENT_IDENTITY = "event_identity"
    RAW_MARKET_FACTS = "raw_market_facts"
    PLAYBOOK_REGISTRY_MEMBERSHIP = "playbook_registry_membership"
    REVIEW_PACKET_LINEAGE = "review_packet_lineage"


class CanonicalStateVectorField(StrEnum):
    """Approved state-vector fields readable by modifier policy."""

    DESK_WINDOW = "desk_window"
    CLOCK_ENVELOPE = "clock_envelope"
    DAY_PHASE_STATE = "day_phase_state"
    CARRY_HORIZON_STATE = "carry_horizon_state"
    CARRYOVER_STATE = "carryover_state"
    EXPIRY_CYCLE_STATE = "expiry_cycle_state"
    EVENT_PROXIMITY_STATE = "event_proximity_state"
    EVENT_WINDOW_STATE = "event_window_state"
    VOLATILITY_REGIME = "volatility_regime"
    BREADTH_STATE = "breadth_state"
    SECTOR_LEADERSHIP_STATE = "sector_leadership_state"
    RATES_REGIME_STATE = "rates_regime_state"
    FX_STRESS_STATE = "fx_stress_state"
    SIGNAL_CONFLICT_STATE = "signal_conflict_state"
    TERM_STRUCTURE_STATE = "term_structure_state"
    SKEW_STATE = "skew_state"
    GAMMA_STATE = "gamma_state"
    DEALER_PRESSURE_STATE = "dealer_pressure_state"
    OPTIONS_BEHAVIOR_CLUSTER = "options_behavior_cluster"
    INVENTORY_POSTURE_STATE = "inventory_posture_state"
    FRESH_VS_INVENTORY_STATE = "fresh_vs_inventory_state"
    THESIS_STATE = "thesis_state"
    CAPITAL_LOCKUP_STATE = "capital_lockup_state"
    TIME_STOP_STATE = "time_stop_state"
    PERMISSION_STATE = "permission_state"


class StateVectorFieldSpec(BaseModel):
    """One governed state-vector field specification."""

    model_config = ConfigDict(extra="forbid")

    field: CanonicalStateVectorField
    owner_stage: PolicyStageOwner
    source_contract: str = Field(min_length=1)
    posture_triggering: bool = False
    review_visible: bool = True
    notes: list[str] = Field(default_factory=list)


class ModifierPolicySpec(BaseModel):
    """Typed object model for one approved state-conditioned modifier."""

    model_config = ConfigDict(extra="forbid")

    modifier_id: str = Field(min_length=1)
    target_surface: MutableRuntimeSurface
    activation_fields: list[CanonicalStateVectorField] = Field(default_factory=list)
    target_stage_owner: PolicyStageOwner
    transform_type: ModifierTransformType
    cap: float | None = None
    floor: float | None = None
    additive_offset: float | None = None
    multiplicative_scale: float | None = None
    rank_weight_delta: float | None = None
    suppresses_output: bool = False
    precedence_hint: str = ""
    explanation_tags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class EffectiveCoefficientLineage(BaseModel):
    """Explain how baseline plus approved modifiers yielded one effective surface."""

    model_config = ConfigDict(extra="forbid")

    target_surface: MutableRuntimeSurface
    baseline_reference: str = Field(min_length=1)
    active_modifier_policy_ids: list[str] = Field(default_factory=list)
    explanation_id: str | None = None


class StatePolicyAuthorityPacket(BaseModel):
    """Frozen Gate 60 authority packet for downstream config and review hooks."""

    model_config = ConfigDict(extra="forbid")

    invariants: list[str] = Field(default_factory=list)
    mutable_surfaces: list[MutableRuntimeSurface] = Field(default_factory=list)
    prohibited_surfaces: list[ProhibitedRuntimeSurface] = Field(default_factory=list)
    readable_state_fields: list[CanonicalStateVectorField] = Field(default_factory=list)
    allowed_transform_types: list[ModifierTransformType] = Field(default_factory=list)


class NonActionClass(StrEnum):
    """First-class stand-down classes recognised by runtime and review."""

    DATA_QUALITY_STAND_DOWN = "data_quality_stand_down"
    TEMPORAL_STAND_DOWN = "temporal_stand_down"
    EVENT_RISK_STAND_DOWN = "event_risk_stand_down"
    REGIME_STAND_DOWN = "regime_stand_down"
    OPTIONS_FLOW_STAND_DOWN = "options_flow_stand_down"
    POSTURE_RISK_STAND_DOWN = "posture_risk_stand_down"
    ELIGIBILITY_STAND_DOWN = "eligibility_stand_down"
    EXECUTION_READINESS_STAND_DOWN = "execution_readiness_stand_down"


class SignalConflictClass(StrEnum):
    """Ordered conflict classes from mild divergence to hard veto."""

    OBSERVATION_DIVERGENCE = "observation_divergence"
    CONFIRMATION_CONFLICT = "confirmation_conflict"
    POSTURE_DEGRADATION = "posture_degradation"
    HARD_VETO_CONFLICT = "hard_veto_conflict"


class DegradationStep(StrEnum):
    """Ordered posture degradation ladder used before or at stand-down."""

    NORMAL = "normal"
    CONFIRMATION_TIGHTENED = "confirmation_tightened"
    CONFIDENCE_REDUCED = "confidence_reduced"
    SIZE_REDUCED = "size_reduced"
    WATCH_ONLY = "watch_only"
    STAND_DOWN = "stand_down"
    VETO = "veto"


class OverrideDisposition(StrEnum):
    """Permitted override or annotation posture for deterministic runtime review."""

    NOT_APPLICABLE = "not_applicable"
    AUDIT_ANNOTATION_ONLY = "audit_annotation_only"
    HUMAN_REVIEW_RELEASE_ONLY = "human_review_release_only"
    FORBIDDEN = "forbidden"


class ConflictResolutionPolicy(BaseModel):
    """One governed conflict-resolution rule."""

    model_config = ConfigDict(extra="forbid")

    conflict_class: SignalConflictClass
    primary_owner_stage: PolicyStageOwner
    secondary_owner_stages: list[PolicyStageOwner] = Field(default_factory=list)
    default_degradation_step: DegradationStep
    escalates_to_veto: bool = False
    visibility_required: bool = True
    notes: list[str] = Field(default_factory=list)


class NonActionAuthorityRecord(BaseModel):
    """One governed stand-down rule and its evidence requirement."""

    model_config = ConfigDict(extra="forbid")

    stand_down_class: NonActionClass
    blocking_owner_stage: PolicyStageOwner
    evidence_required: list[str] = Field(default_factory=list)
    review_note_required: bool = True
    notes: list[str] = Field(default_factory=list)


class NonActionAuthorityPacket(BaseModel):
    """Frozen Gate 61 authority packet for non-action and conflict law."""

    model_config = ConfigDict(extra="forbid")

    non_action_classes: list[NonActionClass] = Field(default_factory=list)
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_steps: list[DegradationStep] = Field(default_factory=list)
    override_dispositions: list[OverrideDisposition] = Field(default_factory=list)


class ScorecardAxis(StrEnum):
    """Canonical Gate 62 scorecard axes for governed stability review."""

    DIAGNOSIS_QUALITY = "diagnosis_quality"
    DECISION_QUALITY = "decision_quality"
    ECONOMIC_QUALITY = "economic_quality"
    EXECUTION_QUALITY = "execution_quality"
    POSTURE_LAW_FIDELITY = "posture_law_fidelity"


class StabilityMetricFamily(StrEnum):
    """Metric families that describe behaviour change and stability."""

    LEVEL = "level"
    SLOPE = "slope"
    ACCELERATION = "acceleration"
    PERSISTENCE = "persistence"
    DISPERSION = "dispersion"
    CORRIDOR_WIDTH = "corridor_width"
    BREACH_FREQUENCY = "breach_frequency"
    BREACH_SEVERITY = "breach_severity"
    COVERAGE = "coverage"


class MetricTriggerMode(StrEnum):
    """Whether one metric is descriptive only or may support review triggers."""

    DESCRIPTIVE_ONLY = "descriptive_only"
    REVIEW_TRIGGER = "review_trigger"


class CorridorZone(StrEnum):
    """Named corridor regions for governed stability assessment."""

    TARGET = "target"
    TOLERATED_DRIFT = "tolerated_drift"
    BREACH = "breach"


class CorridorBreachSeverity(StrEnum):
    """Severity labels for corridor breaches after persistence law is applied."""

    NONE = "none"
    DRIFTING = "drifting"
    MATERIAL = "material"
    SEVERE = "severe"


class BehaviourStabilityState(StrEnum):
    """Human-readable governed stability posture for one surface."""

    BREATHING = "breathing"
    DRIFTING = "drifting"
    DECAYING = "decaying"


class CoverageSliceClass(StrEnum):
    """Coverage slices that keep hidden fragility visible in scorecards."""

    EVENT_CLASS = "event_class"
    REGIME_SLICE = "regime_slice"
    SESSION_SLICE = "session_slice"


class StabilityMetricObservation(BaseModel):
    """One scorecard metric observation for a governed review surface."""

    model_config = ConfigDict(extra="forbid")

    axis: ScorecardAxis
    metric_family: StabilityMetricFamily
    trigger_mode: MetricTriggerMode = MetricTriggerMode.DESCRIPTIVE_ONLY
    value: float
    notes: list[str] = Field(default_factory=list)


class CorridorBounds(BaseModel):
    """Formal corridor algebra for one governed metric family."""

    model_config = ConfigDict(extra="forbid")

    central_tendency: float
    tolerated_spread: float = Field(ge=0.0)
    target_low: float
    target_high: float
    drift_low: float
    drift_high: float
    breach_low: float
    breach_high: float


class PersistenceHysteresisSpec(BaseModel):
    """Persistence and hysteresis rules that prevent review chatter."""

    model_config = ConfigDict(extra="forbid")

    minimum_blocks: int = Field(ge=1)
    confirmation_blocks: int = Field(ge=1)
    recovery_blocks: int = Field(ge=1)
    cooldown_blocks: int = Field(ge=0)


class CoverageSliceScore(BaseModel):
    """Coverage summary for one event, regime, or session slice."""

    model_config = ConfigDict(extra="forbid")

    slice_class: CoverageSliceClass
    slice_label: str = Field(min_length=1)
    observation_count: int = Field(ge=0)
    coverage_ratio: float = Field(ge=0.0, le=1.0)


class SurfaceStabilityScorecard(BaseModel):
    """Frozen Gate 62 scorecard shape for one governed surface."""

    model_config = ConfigDict(extra="forbid")

    surface_id: str = Field(min_length=1)
    surface_class: RuntimeSurfaceClass
    metric_observations: list[StabilityMetricObservation] = Field(default_factory=list)
    corridor: CorridorBounds
    breach_severity: CorridorBreachSeverity = CorridorBreachSeverity.NONE
    behaviour_state: BehaviourStabilityState = BehaviourStabilityState.BREATHING
    persistence: PersistenceHysteresisSpec
    coverage_slices: list[CoverageSliceScore] = Field(default_factory=list)


class StabilityAuthorityPacket(BaseModel):
    """Frozen Gate 62 metric, corridor, and scorecard authority packet."""

    model_config = ConfigDict(extra="forbid")

    scorecard_axes: list[ScorecardAxis] = Field(default_factory=list)
    metric_families: list[StabilityMetricFamily] = Field(default_factory=list)
    trigger_modes: list[MetricTriggerMode] = Field(default_factory=list)
    corridor_zones: list[CorridorZone] = Field(default_factory=list)
    breach_severities: list[CorridorBreachSeverity] = Field(default_factory=list)
    behaviour_states: list[BehaviourStabilityState] = Field(default_factory=list)
    coverage_slice_classes: list[CoverageSliceClass] = Field(default_factory=list)


class ReviewSurfaceClass(StrEnum):
    """Surface classes that may become eligible for governed review."""

    COEFFICIENT_GROUP = "coefficient_group"
    POLICY_SURFACE = "policy_surface"


class ReviewTriggerClass(StrEnum):
    """Explicit reasons a sufficiently evidenced surface becomes review-eligible."""

    MATERIAL_CORRIDOR_BREACH = "material_corridor_breach"
    SEVERE_CORRIDOR_BREACH = "severe_corridor_breach"
    PERSISTENCE_FAILURE = "persistence_failure"
    COVERAGE_COLLAPSE = "coverage_collapse"


class ReviewOutcome(StrEnum):
    """Governed outcomes emitted by review-eligibility law."""

    REVIEW_NOT_ELIGIBLE = "review_not_eligible"
    REVIEW_NO_CHANGE = "review_no_change"
    BOUNDED_ADJUSTMENT_REQUEST = "bounded_adjustment_request"
    CANDIDATE_REPLACEMENT_REQUEST = "candidate_replacement_request"
    RESEARCH_RESET = "research_reset"
    MISSING_MODULE_SUSPICION = "missing_module_suspicion"


class ReviewChangeBudget(StrEnum):
    """Bounded downstream action budget attached to a governed review outcome."""

    NONE = "none"
    BOUNDED_SINGLE_SURFACE = "bounded_single_surface"
    BOUNDED_MULTI_SURFACE = "bounded_multi_surface"
    CANDIDATE_SWAP_ONLY = "candidate_swap_only"
    RESEARCH_ONLY = "research_only"


class EvidenceFloorSpec(BaseModel):
    """Minimum evidence floor required before one surface may be judged."""

    model_config = ConfigDict(extra="forbid")

    surface_class: ReviewSurfaceClass
    minimum_samples: int = Field(ge=1)
    minimum_sessions: int = Field(ge=1)
    minimum_event_slices: int = Field(ge=0)
    minimum_regime_slices: int = Field(ge=0)
    minimum_coverage_ratio: float = Field(ge=0.0, le=1.0)


class ReviewEvidenceBlock(BaseModel):
    """Observed evidence block measured against review floors and corridors."""

    model_config = ConfigDict(extra="forbid")

    surface_class: ReviewSurfaceClass
    surface_id: str = Field(min_length=1)
    sample_count: int = Field(ge=0)
    session_count: int = Field(ge=0)
    event_slice_count: int = Field(ge=0)
    regime_slice_count: int = Field(ge=0)
    coverage_ratio: float = Field(ge=0.0, le=1.0)
    breach_severity: CorridorBreachSeverity = CorridorBreachSeverity.NONE
    persistence_blocks: int = Field(ge=0)
    hysteresis_passed: bool = False


class ReviewEligibilityAuthorityPacket(BaseModel):
    """Frozen Gate 63 review-eligibility authority packet."""

    model_config = ConfigDict(extra="forbid")

    surface_classes: list[ReviewSurfaceClass] = Field(default_factory=list)
    trigger_classes: list[ReviewTriggerClass] = Field(default_factory=list)
    outcomes: list[ReviewOutcome] = Field(default_factory=list)
    change_budgets: list[ReviewChangeBudget] = Field(default_factory=list)


class CandidateRole(StrEnum):
    """Governed candidate roles allowed after historical research lock."""

    CHAMPION = "champion"
    SHADOW_CHALLENGER = "shadow_challenger"
    DORMANT_CANDIDATE = "dormant_candidate"
    RETIRED_CANDIDATE = "retired_candidate"


class CandidateComparisonOutcome(StrEnum):
    """Governed downstream result of candidate comparison and adjudication."""

    RETAIN_CHAMPION = "retain_champion"
    PROMOTE_CHALLENGER = "promote_challenger"
    DEMOTE_TO_DORMANT = "demote_to_dormant"
    RETIRE_CANDIDATE = "retire_candidate"
    RESET_TO_RESEARCH = "reset_to_research"


class AdjudicationDisposition(StrEnum):
    """Lifecycle state for the reserved adjudication span."""

    RESERVED_UNTOUCHED = "reserved_untouched"
    RELEASED_FOR_FINAL_COMPARISON = "released_for_final_comparison"
    CONSUMED_RECORDED = "consumed_recorded"


class CandidateSetShape(BaseModel):
    """Bounded size and role-shape rules for locked candidate sets."""

    model_config = ConfigDict(extra="forbid")

    max_candidate_count: int = Field(ge=1)
    max_shadow_challengers: int = Field(ge=0)
    allow_dormant_candidates: bool = True
    allow_retired_candidates: bool = True
    reserved_adjudication_spans: int = Field(ge=1)


class CandidateLedgerRecord(BaseModel):
    """Tracking hook for one locked candidate and its adjudication state."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    role: CandidateRole
    locked_from_research: bool = True
    evidence_span_ids: list[str] = Field(default_factory=list)
    adjudication_disposition: AdjudicationDisposition = AdjudicationDisposition.RESERVED_UNTOUCHED
    notes: list[str] = Field(default_factory=list)


class CandidateGovernanceAuthorityPacket(BaseModel):
    """Frozen Gate 64 candidate-governance authority packet."""

    model_config = ConfigDict(extra="forbid")

    allowed_roles: list[CandidateRole] = Field(default_factory=list)
    comparison_outcomes: list[CandidateComparisonOutcome] = Field(default_factory=list)
    adjudication_dispositions: list[AdjudicationDisposition] = Field(default_factory=list)
    candidate_shape: CandidateSetShape


class EventOptionsStressState(StrEnum):
    """Bounded Gate 70 event and options-stress states."""

    EVENT_IMMINENT = "event_imminent"
    EVENT_LIVE = "event_live"
    EVENT_SUPPRESSED = "event_suppressed"
    NEGATIVE_GAMMA_STRESS = "negative_gamma_stress"
    PIN_RISK = "pin_risk"
    EXPIRY_DISTORTION = "expiry_distortion"


class EventOptionsStressFamily(StrEnum):
    """Event or options families that qualify Gate 70 policy examples."""

    COMPANY_EVENT = "company_event"
    MACRO_EVENT = "macro_event"
    POLICY_EVENT = "policy_event"
    VENUE_EVENT = "venue_event"
    OPTIONS_GEOMETRY = "options_geometry"


class PolicyEffectType(StrEnum):
    """Bounded posture effects allowed by the Gate 70 matrix."""

    SUPPRESS = "suppress"
    DEGRADE = "degrade"
    WIDEN = "widen"
    CAP = "cap"
    BLOCK = "block"
    HEDGE = "hedge"


class EventOptionsBehaviourClass(StrEnum):
    """Behaviour classes frozen by the event/options-stress matrix."""

    TIGHTENED_THRESHOLDS = "tightened_thresholds"
    HEDGED_ONLY = "hedged_only"
    SIZE_CAPPED = "size_capped"
    WATCH_ONLY = "watch_only"
    HARD_BLOCK = "hard_block"


class EventOptionsStressPolicyRecord(BaseModel):
    """One deterministic event/options-stress policy record."""

    model_config = ConfigDict(extra="forbid")

    state: EventOptionsStressState
    event_families: list[EventOptionsStressFamily] = Field(default_factory=list)
    mutable_surface_targets: list[MutableRuntimeSurface] = Field(default_factory=list)
    effect_types: list[PolicyEffectType] = Field(default_factory=list)
    behaviour_class: EventOptionsBehaviourClass
    hard_block: bool = False
    notes: list[str] = Field(default_factory=list)


class EventOptionsStressAuthorityPacket(BaseModel):
    """Frozen Gate 70 authority for event and options-stress posture law."""

    model_config = ConfigDict(extra="forbid")

    states: list[EventOptionsStressState] = Field(default_factory=list)
    families: list[EventOptionsStressFamily] = Field(default_factory=list)
    effect_types: list[PolicyEffectType] = Field(default_factory=list)
    behaviour_classes: list[EventOptionsBehaviourClass] = Field(default_factory=list)
    policy_records: list[EventOptionsStressPolicyRecord] = Field(default_factory=list)


class ModifierPriorityBand(StrEnum):
    """Deterministic precedence bands for Gate 71 control law."""

    KILL_SWITCH = "kill_switch"
    HARD_BLOCK = "hard_block"
    EVENT_OPTIONS_STRESS = "event_options_stress"
    PHASE_CARRY = "phase_carry"
    PRECURSOR = "precursor"
    REGIME = "regime"
    BASELINE = "baseline"


class CombinationLaw(StrEnum):
    """Bounded algebra for combining compatible modifier effects."""

    MOST_RESTRICTIVE_WINS = "most_restrictive_wins"
    MULTIPLY_THEN_CLAMP = "multiply_then_clamp"
    ADDITIVE_OFFSET_THEN_CLAMP = "additive_offset_then_clamp"
    BLOCK_OVERRIDES_SCALE = "block_overrides_scale"


class KillSwitchCondition(StrEnum):
    """Explicit hard-stop conditions frozen by Gate 71."""

    EVENT_LIVE_HARD_BLOCK = "event_live_hard_block"
    EVENT_SUPPRESSED_WITH_NEGATIVE_GAMMA = "event_suppressed_with_negative_gamma"
    PRECURSOR_CONTRADICTION_WITH_EXPIRY_DISTORTION = (
        "precursor_contradiction_with_expiry_distortion"
    )
    DATA_QUALITY_HARD_BLOCK = "data_quality_hard_block"
    OPERATOR_OR_BROKER_HARD_BLOCK = "operator_or_broker_hard_block"


class ModifierClampRule(BaseModel):
    """Hard cap and floor bounds for one effective mutable surface."""

    model_config = ConfigDict(extra="forbid")

    target_surface: MutableRuntimeSurface
    floor: float | None = None
    cap: float | None = None
    notes: list[str] = Field(default_factory=list)


class ModifierVetoRule(BaseModel):
    """When one precedence band suppresses another entirely."""

    model_config = ConfigDict(extra="forbid")

    controlling_band: ModifierPriorityBand
    suppressed_bands: list[ModifierPriorityBand] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ModifierControlLawAuthorityPacket(BaseModel):
    """Frozen Gate 71 authority for precedence, clamps, vetoes, and kill-switches."""

    model_config = ConfigDict(extra="forbid")

    precedence_bands: list[ModifierPriorityBand] = Field(default_factory=list)
    combination_laws: list[CombinationLaw] = Field(default_factory=list)
    kill_switch_conditions: list[KillSwitchCondition] = Field(default_factory=list)
    clamp_rules: list[ModifierClampRule] = Field(default_factory=list)
    veto_rules: list[ModifierVetoRule] = Field(default_factory=list)
    lineage_fields: list[str] = Field(default_factory=list)


class ResolvedRuntimeSurfaceValue(BaseModel):
    """One resolved mutable-surface value after bounded runtime modifier law."""

    model_config = ConfigDict(extra="forbid")

    target_surface: MutableRuntimeSurface
    owner_stage: PolicyStageOwner
    authority_version: str = Field(min_length=1)
    baseline_reference: str = Field(min_length=1)
    baseline_numeric_value: float | None = None
    baseline_boolean_value: bool | None = None
    minimum_numeric_value: float | None = None
    maximum_numeric_value: float | None = None
    effective_numeric_value: float | None = None
    effective_boolean_value: bool | None = None
    winning_precedence_band: ModifierPriorityBand
    source_policy_ids: list[str] = Field(default_factory=list)
    clamped: bool = False
    notes: list[str] = Field(default_factory=list)


class ModifierRuntimePacket(BaseModel):
    """Typed runtime packet freezing Gate 78 modifier application outputs."""

    model_config = ConfigDict(extra="forbid")

    active_state_fields: list[CanonicalStateVectorField] = Field(default_factory=list)
    active_policy_ids: list[str] = Field(default_factory=list)
    resolved_surfaces: list[ResolvedRuntimeSurfaceValue] = Field(default_factory=list)
    effective_lineage: list[EffectiveCoefficientLineage] = Field(default_factory=list)
    active_precedence_bands: list[ModifierPriorityBand] = Field(default_factory=list)
    applied_combination_laws: list[CombinationLaw] = Field(default_factory=list)
    triggered_kill_switch: KillSwitchCondition | None = None
    suppressed_state_labels: list[str] = Field(default_factory=list)
    stand_down_class: NonActionClass | None = None
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_step: DegradationStep = DegradationStep.NORMAL
    override_disposition: OverrideDisposition = OverrideDisposition.NOT_APPLICABLE
    notes: list[str] = Field(default_factory=list)
