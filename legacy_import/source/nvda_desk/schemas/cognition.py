"""Typed runtime contracts for the Desk Cognition Grammar.

Gate C defines the binding schema surface for the desk runtime. These models
make inventory state, repeated options context, playbook actions, review
packets, and runtime-contract metadata explicit so later module imports do not
smuggle in hidden state.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.events import LiveEventSnapshot
from nvda_desk.schemas.checkpoints import CheckpointObservation
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.schemas.downstream import DownstreamArchitectureReceipt
from nvda_desk.schemas.market import PrecursorRuntimePacket
from nvda_desk.schemas.options_units import VolFraction
from nvda_desk.schemas.parallel_risk import ParallelRiskLanePacket
from nvda_desk.schemas.review import (
    CandidateGovernanceSurface,
    EconomicContributionPacket,
    EventOptionsStressPolicySurface,
    ImportedModuleReviewCitation,
    ModifierControlLawSurface,
    PhaseCarryoverPolicySurface,
    PrecursorGovernanceSurface,
    PrecursorRuntimeBindingSurface,
    PromotionEvidencePacket,
    ReviewEligibilitySurface,
    ReviewFailurePacket,
    ReviewGovernanceSurface,
    ReviewLineagePacket,
    TemporalEventWindowSurface,
)
from nvda_desk.schemas.risk import CarryHorizonState, DayPhaseState, RiskAction, RiskDecision
from nvda_desk.schemas.session_clock import DeskCalendarAuthorityPacket
from nvda_desk.schemas.state_policy import (
    DegradationStep,
    EffectiveCoefficientLineage,
    ModifierRuntimePacket,
    NonActionClass,
    OverrideDisposition,
    ResolvedRuntimeSurfaceValue,
    SignalConflictClass,
    SurfaceStabilityScorecard,
)


class VolatilityRegime(StrEnum):
    """Bounded volatility-regime labels for desk-context evaluation."""

    CALM = "calm"
    CAUTION = "caution"
    STRESSED = "stressed"


class BreadthState(StrEnum):
    """Breadth-state labels used by regime and posture services."""

    SUPPORTIVE = "supportive"
    MIXED = "mixed"
    WEAK = "weak"


class TermStructureState(StrEnum):
    """Options term-structure states."""

    FRONT_PREMIUM = "front_premium"
    FLAT = "flat"
    BACK_PREMIUM = "back_premium"


class SkewState(StrEnum):
    """Options skew states."""

    DOWNSIDE_HEAVY = "downside_heavy"
    BALANCED = "balanced"
    UPSIDE_CHASE = "upside_chase"


class GammaState(StrEnum):
    """Gamma-pressure states used in options-context analysis."""

    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    DESTABILISING = "destabilising"


class PermissionState(StrEnum):
    """Binding posture/risk permission states."""

    BLOCK = "block"
    DERISK = "derisk"
    ALLOW = "allow"


class PlaybookDecision(StrEnum):
    """Eligibility outcomes for candidate playbooks."""

    ELIGIBLE = "eligible"
    WATCH_ONLY = "watch_only"
    INELIGIBLE = "ineligible"


class PlaybookAction(StrEnum):
    """Explicit per-playbook action surface required by Gate C."""

    ADD = "add"
    HOLD = "hold"
    TRIM = "trim"
    REDUCE = "reduce"
    HEDGE = "hedge"


class TradableExpressionFamily(StrEnum):
    """Bounded tradable expression families admitted to lifecycle carriage."""

    SINGLE_LEG_CALL_DEBIT = "single_leg_call_debit"


class LifecycleAction(StrEnum):
    """Bounded lifecycle actions admitted before broad lifecycle compilation exists."""

    ADD = "add"
    TRIM = "trim"
    FLATTEN = "flatten"
    HOLD_SMALL_OVERNIGHT = "hold_small_overnight"
    BLOCK_CARRY = "block_carry"


class BindingStageName(StrEnum):
    """Deterministic names for the seven binding desk-runtime stages."""

    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    REVIEW = "review"


class TemporalContextInput(BaseModel):
    """Inputs required to classify temporal context for a market snapshot."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    next_expiry: datetime | None = None
    next_event_at: datetime | None = None
    live_event_snapshot: LiveEventSnapshot | None = None
    precursor_runtime_packet: PrecursorRuntimePacket | None = None
    desk_calendar_authority: DeskCalendarAuthorityPacket | None = None
    prior_session_return_pct: float = 0.0
    intraday_move_pct: float = 0.0
    prior_close_price: float | None = None
    official_open_price: float | None = None
    last_price: float | None = None
    interval_volume_shares: float | None = None
    cumulative_session_volume: float | None = None
    session_vwap: float | None = None
    distance_to_vwap_pct: float | None = None
    vwap_slope_5m_pct: float | None = None
    opening_range_high_5m: float | None = None
    opening_range_low_5m: float | None = None
    opening_range_break_count: int | None = None
    price_realised_vol_5m_pct: float | None = None
    price_realised_vol_15m_pct: float | None = None
    relative_volume_ratio: float | None = None
    session_bucket_label: str | None = None
    same_bucket_interval_volume_share: float | None = None
    same_bucket_interval_volume_share_baseline: float | None = None
    same_bucket_baseline_available: bool = False
    rolling_range_5m_pct: float | None = None
    impulse_age_bars: int | None = None


class TemporalContextOutput(BaseModel):
    """Deterministic temporal-context output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    session_phase: SessionClockPhase
    desk_window: str
    phase_confidence: float
    clock_envelope: str = "closed"
    behavioural_phase: SessionClockPhase | None = None
    signal_coverage_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    minutes_since_open: int | None = None
    minutes_to_close: int | None = None
    expiry_days_remaining: int | None = None
    expiry_cycle_state: str
    event_minutes_remaining: int | None = None
    event_proximity_state: str
    event_window_state: str
    event_overlap_class: str = "single_event"
    event_risk_timing_class: str = "priced_risk"
    event_carry_sensitivity: str = "intraday_only"
    event_timing_profile: str | None = None
    active_event_family: str | None = None
    calendar_closure_classes: list[str] = Field(default_factory=list)
    session_bridge_rules: list[str] = Field(default_factory=list)
    next_session_open_hint: datetime | None = None
    recent_path_tag: str
    carryover_state: str
    reasons: list[str] = Field(default_factory=list)


class MarketRegimeContextInput(BaseModel):
    """Inputs required to classify market-regime context."""

    model_config = ConfigDict(extra="forbid")

    nvda_return_pct: float
    nq_return_pct: float
    es_return_pct: float
    sox_return_pct: float
    breadth_score: float = Field(ge=0.0, le=1.0)
    concentration_score: float = Field(ge=0.0, le=1.0)
    vix_level: float
    vvix_level: float
    us10y: float
    us2y: float
    usdjpy: float


class MarketRegimeContextOutput(BaseModel):
    """Deterministic market-regime output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    nvda_vs_nq_residual_pct: float
    nvda_vs_es_residual_pct: float
    beta_leadership_score: float
    volatility_regime: VolatilityRegime
    vol_of_vol_state: str
    breadth_state: BreadthState
    breadth_concentration_state: str
    sector_leadership_state: str
    rates_regime_state: str
    fx_stress_state: str
    signal_conflict_state: str
    curve_10s2s: float
    vix_vvix_spread: float
    cross_asset_pressure_score: float
    reasons: list[str] = Field(default_factory=list)


class StrikeClusterObservation(BaseModel):
    """One nearby strike cluster used to enrich options context."""

    model_config = ConfigDict(extra="forbid")

    strike: float
    side: str
    open_interest: float = Field(ge=0.0)
    volume: float = Field(ge=0.0)
    distance_to_spot_pct: float


class OptionsFlowMicroSnapshot(BaseModel):
    """One repeated intraday options snapshot for state progression."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    front_atm_iv: VolFraction
    next_atm_iv: VolFraction
    put_call_skew: float
    gamma_pressure_score: float
    spot_to_pin_distance_pct: float = 0.0


class TenorCurvePoint(BaseModel):
    """One tenor-point observation for the intraday IV curve."""

    model_config = ConfigDict(extra="forbid")

    tenor_dte: int = Field(ge=0)
    atm_iv: VolFraction = Field(ge=0.0)


class PinProgressionPoint(BaseModel):
    """One point tracking distance to a live pin cluster over time."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    distance_to_pin_pct: float


class OptionsFlowContextInput(BaseModel):
    """Inputs required to classify options and flow context."""

    model_config = ConfigDict(extra="forbid")

    spot_price: float
    front_dte: int
    next_dte: int
    front_atm_iv: VolFraction
    next_atm_iv: VolFraction
    put_call_skew: float
    gamma_pressure_score: float
    call_put_imbalance: float
    oi_concentration: float
    atm_straddle_value: float
    front_realised_vol: VolFraction = 0.0
    next_realised_vol: VolFraction = 0.0
    vix_level: float = 0.0
    vvix_level: float = 0.0
    spot_to_pin_distance_pct: float = 0.0
    call_oi_near_spot: float = 0.0
    put_oi_near_spot: float = 0.0
    front_volume_near_spot: float = 0.0
    next_volume_near_spot: float = 0.0
    same_bucket_spread_bps: float | None = None
    same_bucket_spread_baseline_bps: float | None = None
    same_bucket_trade_count: int | None = None
    same_bucket_trade_count_baseline: float | None = None
    vanna_proxy: float = 0.0
    charm_proxy: float = 0.0
    nearby_strike_clusters: list[StrikeClusterObservation] = Field(default_factory=list)
    repeated_snapshot_sequence: list[OptionsFlowMicroSnapshot] = Field(default_factory=list)
    tenor_iv_curve: list[TenorCurvePoint] = Field(default_factory=list)
    pin_progression_sequence: list[PinProgressionPoint] = Field(default_factory=list)
    surface_anchor_to_spot_pct: float | None = None


class OptionsFlowContextOutput(BaseModel):
    """Deterministic options-and-flow output for downstream layers."""

    model_config = ConfigDict(extra="forbid")

    term_structure_state: TermStructureState
    skew_state: SkewState
    gamma_state: GammaState
    implied_move_envelope_pct: float
    iv_rv_front_state: str
    iv_rv_next_state: str
    iv_rv_curve_state: str
    pin_risk_state: str
    dealer_pressure_state: str
    vix_spread_state: str
    options_behavior_cluster: str
    flow_tension_score: float
    strike_cluster_state: str
    dominant_strike: float | None = None
    surface_anchor_state: str
    repeated_snapshot_state: str
    skew_evolution_state: str
    tenor_curve_state: str
    pin_progression_state: str
    pin_progression_velocity: float | None = None
    reasons: list[str] = Field(default_factory=list)


class InventoryState(BaseModel):
    """Held exposure, thesis lifecycle, and deployment-control inputs."""

    model_config = ConfigDict(extra="forbid")

    existing_inventory_pct: float = Field(ge=0.0, le=100.0)
    fresh_cash_pct: float = Field(ge=0.0, le=100.0)
    overnight_inventory_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    open_orders_count: int = Field(ge=0, default=0)
    capital_lockup_pct: float = Field(ge=0.0, le=100.0, default=0.0)
    cost_basis_gap_pct: float = 0.0
    thesis_state_input: str = "valid"
    adverse_excursion_pct: float = 0.0
    time_stop_minutes_remaining: int | None = Field(default=None, ge=0)
    thesis_age_minutes: int | None = Field(default=None, ge=0)


class PostureRiskInput(BaseModel):
    """Inputs required for posture and risk permission."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    inventory: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


class PostureHardInvariantsSurface(BaseModel):
    """Posture-owned hard-stop surface preserved apart from later annotations."""

    model_config = ConfigDict(extra="forbid")

    block_active: bool
    hard_block_reasons: list[str] = Field(default_factory=list)
    zero_deployable_required: bool


class PostureLocalEnvelopeSurface(BaseModel):
    """Posture-owned local envelope preserved before later modifier consequences.

    Numeric deployable-capital and inventory-bias fields remain compatibility
    echoes while downstream readers migrate to the bounded permission envelope.
    """

    model_config = ConfigDict(extra="forbid")

    base_permission_state: PermissionState
    base_posture_label: str
    inventory_posture_state: str
    fresh_vs_inventory_state: str
    thesis_state: str
    capital_lockup_state: str
    adverse_excursion_state: str
    time_stop_state: str
    signal_conflict_state: str
    base_fresh_deployable_capital_pct: float
    base_overnight_deployable_capital_pct: float
    base_inventory_action_bias: str
    time_stop_minutes_remaining: int | None = None
    thesis_pressure_score: float
    derisk_reasons: list[str] = Field(default_factory=list)


class ModifierCompatibilityBridgeSurface(BaseModel):
    """Explicit compatibility bridge showing packet-authoritative field consequences."""

    model_config = ConfigDict(extra="forbid")

    authority_source: str = "modifier_runtime_packet"
    compatibility_bridge_active: bool = False
    applied_policy_ids: list[str] = Field(default_factory=list)
    overridden_fields: list[str] = Field(default_factory=list)
    target_fresh_deployable_capital_pct: float | None = None
    entry_gate_score_floor: float | None = None
    zone_score_threshold: float | None = None
    max_risk_per_trade: float | None = None
    hedge_required: bool | None = None
    notes: list[str] = Field(default_factory=list)


class PostureRiskOutput(BaseModel):
    """Binding posture and permission output.

    Flat deployable-capital and inventory-bias fields remain compatibility
    echoes. The bounded permission envelope is the active Step 4 serial
    authority for downstream readers.
    """

    model_config = ConfigDict(extra="forbid")

    permission_state: PermissionState
    posture_label: str
    inventory_posture_state: str
    fresh_deployable_capital_pct: float
    overnight_deployable_capital_pct: float
    inventory_action_bias: str
    fresh_vs_inventory_state: str
    thesis_state: str
    capital_lockup_state: str
    adverse_excursion_state: str
    time_stop_state: str
    signal_conflict_state: str
    time_stop_minutes_remaining: int | None = None
    thesis_pressure_score: float
    hard_invariants: PostureHardInvariantsSurface | None = None
    local_envelope: PostureLocalEnvelopeSurface | None = None
    downstream_annotations: list[str] = Field(default_factory=list)
    modifier_compatibility_bridge: ModifierCompatibilityBridgeSurface | None = None
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    parallel_risk_lane_packet: ParallelRiskLanePacket | None = None
    stand_down_class: NonActionClass | None = None
    conflict_classes: list[SignalConflictClass] = Field(default_factory=list)
    degradation_step: DegradationStep = DegradationStep.NORMAL
    override_disposition: OverrideDisposition = OverrideDisposition.NOT_APPLICABLE
    reasons: list[str] = Field(default_factory=list)


class PlaybookFamilyCandidate(BaseModel):
    """Candidate playbook-family status inside the desk-cognition runtime."""

    model_config = ConfigDict(extra="forbid")

    family_id: str
    decision: PlaybookDecision
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    watch_setup_variant_ids: list[str] = Field(default_factory=list)
    active_playbook_ids: list[str] = Field(default_factory=list)
    watch_playbook_ids: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class SetupVariantCandidate(BaseModel):
    """Candidate setup-variant status inside the desk-cognition runtime."""

    model_config = ConfigDict(extra="forbid")

    setup_variant_id: str
    family_id: str
    execution_expression_id: str | None = None
    horizon: str | None = None
    legacy_playbook_id: str | None = None
    decision: PlaybookDecision
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False
    reasons: list[str] = Field(default_factory=list)


class PlaybookCandidate(BaseModel):
    """Legacy-compatible playbook candidate derived from native setup-variant selection."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    family_id: str | None = None
    setup_variant_id: str | None = None
    execution_expression_id: str | None = None
    horizon: str | None = None
    decision: PlaybookDecision
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False
    reasons: list[str] = Field(default_factory=list)


class CandidateAdjudicationRecord(BaseModel):
    """Deterministic record of how one eligible playbook candidate was ranked."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    family_id: str | None = None
    setup_variant_id: str | None = None
    action_bias: PlaybookAction = PlaybookAction.HOLD
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    score: float
    registry_priority: int = Field(ge=1)
    contradiction_tags: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class PlaybookEligibilityInput(BaseModel):
    """Inputs required to classify playbook eligibility."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput


class PlaybookEligibilityOutput(BaseModel):
    """Eligibility output for the current desk-cognition snapshot."""

    model_config = ConfigDict(extra="forbid")

    family_candidates: list[PlaybookFamilyCandidate] = Field(default_factory=list)
    setup_variant_candidates: list[SetupVariantCandidate] = Field(default_factory=list)
    candidates: list[PlaybookCandidate] = Field(default_factory=list)
    active_family_ids: list[str] = Field(default_factory=list)
    watch_family_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    watch_setup_variant_ids: list[str] = Field(default_factory=list)
    add_candidates: list[str] = Field(default_factory=list)
    hold_candidates: list[str] = Field(default_factory=list)
    trim_candidates: list[str] = Field(default_factory=list)
    reduce_candidates: list[str] = Field(default_factory=list)
    hedge_candidates: list[str] = Field(default_factory=list)
    probe_candidates: list[str] = Field(default_factory=list)
    watch_only_candidates: list[str] = Field(default_factory=list)
    no_trade_reasons: list[str] = Field(default_factory=list)
    rejected_playbook_reasons: dict[str, list[str]] = Field(default_factory=dict)
    admissibility_surface: EligibilityAdmissibilitySurface
    reasons: list[str] = Field(default_factory=list)


class EligibilityAdmissibilitySurface(BaseModel):
    """Bounded Stage 5 admissibility surface preserved apart from Stage 6 ranking."""

    model_config = ConfigDict(extra="forbid")

    admissibility_version: str = "eligibility_admissibility.v1"
    permission_state: PermissionState
    no_trade_reasons: list[str] = Field(default_factory=list)
    admissible_family_ids: list[str] = Field(default_factory=list)
    watch_family_ids: list[str] = Field(default_factory=list)
    admissible_setup_variant_ids: list[str] = Field(default_factory=list)
    watch_setup_variant_ids: list[str] = Field(default_factory=list)
    admissible_playbook_ids: list[str] = Field(default_factory=list)
    watch_only_playbook_ids: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PositionContextInput(BaseModel):
    """Bounded managed-position context carried into the execution stage."""

    model_config = ConfigDict(extra="forbid")

    position_context_version: str = "position_context.v1"
    setup_variant_id: str | None = None
    execution_expression_id: str | None = None
    tradable_expression_family: TradableExpressionFamily | None = None
    legal_lifecycle_actions: list[LifecycleAction] = Field(default_factory=list)
    position_active: bool | None = None
    current_position_size_pct: float | None = Field(default=None, ge=0.0, le=100.0)
    remaining_ladder_steps: int | None = Field(default=None, ge=0)
    carry_state_eligible: bool | None = None
    hard_flat_required: bool | None = None


class ExecutionExpressionInput(BaseModel):
    """Inputs required to derive deterministic expression and execution."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    parallel_risk_lane_packet: ParallelRiskLanePacket | None = None
    position_context: PositionContextInput | None = None


class FinalRiskJoinSurface(BaseModel):
    """Structured record of the final risk authority join after execution synthesis."""

    model_config = ConfigDict(extra="forbid")

    action: RiskAction
    confidence_scalar: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    joined_after_stage: str = "execution_synthesis"
    source_service: str = "risk_gateway"
    lineage_tags: list[str] = Field(default_factory=list)
    execution_effect: str


class TerminalRiskOverlapClass(StrEnum):
    """Observed overlap classes between overlay evaluation and terminal application."""

    OVERLAY_ALLOW_NO_TERMINAL_OVERRIDE = "overlay_allow_no_terminal_override"
    OVERLAY_DERISK_NO_TERMINAL_OVERRIDE = "overlay_derisk_no_terminal_override"
    OVERLAY_BLOCK_NO_TERMINAL_OVERRIDE = "overlay_block_no_terminal_override"
    POSTURE_DERISK_SUPERSEDES_OVERLAY_ALLOW = "posture_derisk_supersedes_overlay_allow"
    POSTURE_BLOCK_SUPERSEDES_OVERLAY_ALLOW = "posture_block_supersedes_overlay_allow"
    POSTURE_BLOCK_SUPERSEDES_OVERLAY_DERISK = "posture_block_supersedes_overlay_derisk"
    POSTURE_BLOCK_ALIGNS_WITH_OVERLAY_BLOCK = "posture_block_aligns_with_overlay_block"


class TerminalRiskApplicationSurface(BaseModel):
    """Bounded additive seam between overlay evaluation and final-risk application."""

    model_config = ConfigDict(extra="forbid")

    application_version: str = "terminal_risk_application.v1"
    posture_permission_state: PermissionState
    overlay_decision: RiskDecision
    final_decision: RiskDecision
    overlap_classes: list[TerminalRiskOverlapClass] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class LifecyclePlanOutput(BaseModel):
    """Bounded second-half lifecycle plan emitted by the execution stage."""

    model_config = ConfigDict(extra="forbid")

    lifecycle_plan_version: str = "lifecycle_plan.v1"
    setup_variant_id: str | None = None
    execution_expression_id: str | None = None
    tradable_expression_family: TradableExpressionFamily | None = None
    legal_lifecycle_actions: list[LifecycleAction] = Field(default_factory=list)
    lifecycle_state: str = "not_applicable"
    next_action: LifecycleAction | None = None
    allowed_actions: list[LifecycleAction] = Field(default_factory=list)
    carry_candidate: bool = False
    must_flatten_by_close: bool = False
    fired_rules: list[str] = Field(default_factory=list)
    blocked_rules: list[str] = Field(default_factory=list)
    rationale_codes: list[str] = Field(default_factory=list)


class ExecutionExpressionOutput(BaseModel):
    """Deterministic execution-expression output.

    The serial contract carries recommendation identity, execution character,
    and ladder geometry only. A compatibility accessor still derives
    `target_fresh_deployable_pct` from `scaling_plan`, but that value is only
    the summed ladder shape, not a serialized contract field and not
    fresh-capital allocation authority.
    """

    model_config = ConfigDict(extra="forbid")

    active_playbook_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    active_family_ids: list[str] = Field(default_factory=list)
    pre_final_risk_active_playbook_ids: list[str] = Field(default_factory=list)
    pre_final_risk_lead_playbook_id: str | None = None
    pre_final_risk_entry_style: str | None = None
    lead_playbook_id: str | None = None
    lead_setup_variant_id: str | None = None
    lead_family_id: str | None = None
    adjudication_method: str = "candidate_score_v1"
    contradiction_resolution: str | None = None
    lead_selection_score: float | None = None
    lead_selection_reasons: list[str] = Field(default_factory=list)
    candidate_adjudication: list[CandidateAdjudicationRecord] = Field(default_factory=list)
    entry_style: str
    playbook_execution_styles: dict[str, str] = Field(default_factory=dict)
    setup_variant_execution_styles: dict[str, str] = Field(default_factory=dict)
    entry_gate_score_floor: float = 0.65
    zone_score_threshold: float = 0.50
    distance_to_vwap_soft_limit_pct: float = 1.50
    risk_vix_caution_threshold: float = 24.0
    risk_vix_hot_threshold: float = 32.0
    max_risk_per_trade: float = 0.35
    passive_aggressive_bias: str = "balanced"
    ladder_spacing_bps: float = 0.0
    max_chase_distance_bps: float = 0.0
    stop_distance_bps: float = 0.0
    take_profit_distance_bps: float = 0.0
    hedge_ratio: float = 0.0
    per_slice_risk_pct: float = 0.0
    geometry_notes: list[str] = Field(default_factory=list)
    hedge_required: bool
    inventory_action: str
    fresh_capital_action: str
    thesis_invalidation_state: str
    scaling_plan: list[float] = Field(default_factory=list)
    invalidation_reasons: list[str] = Field(default_factory=list)
    exit_reasons: list[str] = Field(default_factory=list)
    exit_plan: list[str] = Field(default_factory=list)
    lifecycle_plan: LifecyclePlanOutput | None = None
    candidate_ownership: ExecutionCandidateOwnershipSurface
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    parallel_risk_lane_packet: ParallelRiskLanePacket | None = None
    modifier_compatibility_bridge: ModifierCompatibilityBridgeSurface | None = None
    final_risk_join: FinalRiskJoinSurface | None = None
    reasons: list[str] = Field(default_factory=list)

    @property
    def target_fresh_deployable_pct(self) -> float:
        """Return the compatibility-only sum implied by `scaling_plan`."""

        if not self.scaling_plan:
            return 0.0
        return round(sum(self.scaling_plan), 4)


class ExecutionCandidateOwnershipSurface(BaseModel):
    """Bounded Stage 6 candidate-ownership surface preserved apart from later risk joins."""

    model_config = ConfigDict(extra="forbid")

    ownership_version: str = "execution_candidate_ownership.v1"
    admitted_playbook_ids: list[str] = Field(default_factory=list)
    watch_only_playbook_ids: list[str] = Field(default_factory=list)
    adjudicated_playbook_ids: list[str] = Field(default_factory=list)
    lead_playbook_id: str | None = None
    contradiction_resolution: str | None = None
    notes: list[str] = Field(default_factory=list)


class StageLocalHandoffSurface(BaseModel):
    """Additive preserved handoff surface carried without changing stage order."""

    model_config = ConfigDict(extra="forbid")

    handoff_version: str = "stage_local_handoff.v1"
    cited_posture_pre_modifier: PostureRiskOutput
    cited_eligibility: PlaybookEligibilityOutput
    execution_pre_modifier: ExecutionExpressionOutput
    execution_post_modifier_pre_final_risk: ExecutionExpressionOutput
    overlay_risk_decision: RiskDecision
    terminal_risk_application: TerminalRiskApplicationSurface
    terminal_risk_decision: RiskDecision
    notes: list[str] = Field(default_factory=list)


class CapitalDeploymentAuthorityAction(StrEnum):
    """Bounded actions for downstream fresh-capital authorisation."""

    DEPLOY = "deploy"
    STAND_DOWN = "stand_down"


class CapitalDeploymentAuthorityInput(BaseModel):
    """Minimum lawful inputs for capital-deployment authorisation."""

    model_config = ConfigDict(extra="forbid")

    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    stage_local_handoff: StageLocalHandoffSurface
    parallel_risk_lane_packet: ParallelRiskLanePacket
    capital_state: CapitalStateSnapshotPayload


class CapitalDeploymentAuthorityDecision(BaseModel):
    """Bounded downstream decision stating whether fresh capital should be deployed now.

    Upstream serial stages recommend and preserve seam context. This downstream
    service alone authorises bounded fresh-capital deployment.
    """

    model_config = ConfigDict(extra="forbid")

    decision_version: str = "capital_deployment_authority.v1"
    service_id: str = "capital_deployment_authority_service"
    deployment_action: CapitalDeploymentAuthorityAction
    lead_playbook_id: str | None = None
    opportunity_target_pct: float = Field(ge=0.0, le=100.0)
    posture_cap_pct: float = Field(ge=0.0, le=100.0)
    authorised_deployable_pct: float = Field(ge=0.0, le=100.0)
    authorised_notional_usd: float = Field(ge=0.0)
    available_buying_power_usd: float = Field(ge=0.0)
    capital_source: str = Field(min_length=1)
    terminal_risk_action: RiskAction
    environmental_weather_state: str
    consequence_class: str
    rationale_codes: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class RuntimeStateVector(BaseModel):
    """Approved state-vector slice readable by Gate 60 modifier policy."""

    model_config = ConfigDict(extra="forbid")

    desk_window: str
    clock_envelope: str
    day_phase_state: DayPhaseState
    carry_horizon_state: CarryHorizonState
    carryover_state: str
    expiry_cycle_state: str
    event_proximity_state: str
    event_window_state: str
    volatility_regime: VolatilityRegime
    breadth_state: BreadthState
    sector_leadership_state: str
    rates_regime_state: str
    fx_stress_state: str
    signal_conflict_state: str
    term_structure_state: TermStructureState
    skew_state: SkewState
    gamma_state: GammaState
    dealer_pressure_state: str
    options_behavior_cluster: str
    inventory_posture_state: str
    fresh_vs_inventory_state: str
    thesis_state: str
    capital_lockup_state: str
    time_stop_state: str
    permission_state: PermissionState


class EffectivePolicySnapshot(BaseModel):
    """Review-visible snapshot of effective policy surfaces for one decision."""

    model_config = ConfigDict(extra="forbid")

    active_lineage: list[EffectiveCoefficientLineage] = Field(default_factory=list)
    resolved_surfaces: list[ResolvedRuntimeSurfaceValue] = Field(default_factory=list)


class ReviewExplanationInput(BaseModel):
    """Inputs required to reconstruct a deterministic reasoning packet."""

    model_config = ConfigDict(extra="forbid")

    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    modifier_runtime_packet: ModifierRuntimePacket | None = None
    parallel_risk_lane_packet: ParallelRiskLanePacket
    stage_local_handoff: StageLocalHandoffSurface
    capital_deployment_authority: CapitalDeploymentAuthorityDecision | None = None
    downstream_architecture_receipt: DownstreamArchitectureReceipt
    temporal_input: TemporalContextInput | None = None


class StageReasonPacket(BaseModel):
    """Stage-by-stage reason packet for deterministic review output."""

    model_config = ConfigDict(extra="forbid")

    stage: str
    summary: str
    reasons: list[str] = Field(default_factory=list)


class RejectedPlaybookReason(BaseModel):
    """Explicit rejected-playbook surface required by Gate C review packets."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    decision: PlaybookDecision
    action_bias: PlaybookAction
    reasons: list[str] = Field(default_factory=list)


class ContradictionSurface(BaseModel):
    """One contradiction or tension the review layer must expose."""

    model_config = ConfigDict(extra="forbid")

    contradiction_id: str
    description: str
    implicated_stages: list[str] = Field(default_factory=list)


class PacketLineageSurface(BaseModel):
    """Typed lineage surface for review and replay provenance."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: Literal["dmp.v3"] = "dmp.v3"
    review_packet_id: str
    decision_packet_id: str
    packet_lineage: list[str] = Field(default_factory=list)
    stage_packet_ids: dict[str, str] = Field(default_factory=dict)


class ReviewExplanationOutput(BaseModel):
    """Structured review and explanation packet for one snapshot."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    conflict_tags: list[str] = Field(default_factory=list)
    signal_conflict_density: float = 0.0
    stage_reason_packets: list[StageReasonPacket] = Field(default_factory=list)
    rejected_playbooks: list[RejectedPlaybookReason] = Field(default_factory=list)
    contradictions: list[ContradictionSurface] = Field(default_factory=list)
    module_attribution: dict[str, float] = Field(default_factory=dict)
    imported_module_citations: list[ImportedModuleReviewCitation] = Field(default_factory=list)
    imported_module_maturity_counts: dict[str, int] = Field(default_factory=dict)
    effective_policy: EffectivePolicySnapshot | None = None
    stability_scorecards: list[SurfaceStabilityScorecard] = Field(default_factory=list)
    review_governance: ReviewGovernanceSurface | None = None
    event_window_governance: TemporalEventWindowSurface | None = None
    precursor_governance: PrecursorGovernanceSurface | None = None
    precursor_runtime_binding: PrecursorRuntimeBindingSurface | None = None
    phase_carry_policy: PhaseCarryoverPolicySurface | None = None
    event_options_stress_policy: EventOptionsStressPolicySurface | None = None
    modifier_control_law: ModifierControlLawSurface | None = None
    review_eligibility: ReviewEligibilitySurface | None = None
    candidate_governance: CandidateGovernanceSurface | None = None
    review_lineage: ReviewLineagePacket | None = None
    failure_taxonomy: ReviewFailurePacket | None = None
    economic_accountability: EconomicContributionPacket | None = None
    promotion_evidence: PromotionEvidencePacket | None = None
    packet_lineage: PacketLineageSurface | None = None
    stage_local_handoff: StageLocalHandoffSurface
    capital_deployment_authority: CapitalDeploymentAuthorityDecision | None = None
    downstream_architecture_receipt: DownstreamArchitectureReceipt
    review_packet: dict[str, object]
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class ModuleDocstringContractTemplate(BaseModel):
    """Required docstring sections for imported desk-runtime services."""

    model_config = ConfigDict(extra="forbid")

    template_id: str
    required_sections: list[str] = Field(default_factory=list)


class RuntimeLayerContract(BaseModel):
    """Deterministic contract for one binding Desk Cognition Grammar layer."""

    model_config = ConfigDict(extra="forbid")

    grammar_role: str
    service_path: str
    service_class_name: str
    input_model_name: str
    output_model_name: str
    required_input_fields: list[str] = Field(default_factory=list)
    optional_input_fields: list[str] = Field(default_factory=list)
    required_output_fields: list[str] = Field(default_factory=list)
    optional_output_fields: list[str] = Field(default_factory=list)
    docstring_required: bool = True
    docstring_contract_sections: list[str] = Field(default_factory=list)


class TraceStagePacket(BaseModel):
    """Trace contract for one executed runtime layer."""

    model_config = ConfigDict(extra="forbid")

    grammar_role: str
    service_path: str
    input_model_name: str
    output_model_name: str
    required_input_fields: list[str] = Field(default_factory=list)
    required_output_fields: list[str] = Field(default_factory=list)
    summary: str


ReviewExplanationOutput.model_rebuild()
