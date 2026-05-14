from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.state_policy import MutableRuntimeSurface


class DayPhaseState(StrEnum):
    """Approved day-phase states for Gate 69 policy law."""

    OPENING_DISORDER = "opening_disorder"
    OPENING_RESOLUTION = "opening_resolution"
    TREND_WINDOW = "trend_window"
    MIDDAY_COMPRESSION = "midday_compression"
    LATE_SESSION = "late_session"
    CLOSE_AUCTION = "close_auction"
    POST_CLOSE = "post_close"


class CarryHorizonState(StrEnum):
    """Carry-sensitive states that may alter posture lawfully."""

    INTRADAY_ONLY = "intraday_only"
    OVERNIGHT_SETUP = "overnight_setup"
    WEEKEND_SETUP = "weekend_setup"
    EVENT_CARRY_SETUP = "event_carry_setup"


class PhaseBehaviourClass(StrEnum):
    """Bounded policy behaviours allowed by the phase/carry matrix."""

    NORMAL_OPERATION = "normal_operation"
    TIGHTENED_THRESHOLDS = "tightened_thresholds"
    COMPRESSED_DEPLOYMENT = "compressed_deployment"
    CARRY_PREPARATION = "carry_preparation"
    NO_ACTION_PREFERRED = "no_action_preferred"


class PhaseNoActionBias(StrEnum):
    """Whether the matrix simply allows, prefers, or requires no-action."""

    NEUTRAL = "neutral"
    PREFERRED = "preferred"
    REQUIRED = "required"


class PhaseCarryPolicyRecord(BaseModel):
    """One deterministic phase/carry posture policy record."""

    model_config = ConfigDict(extra="forbid")

    day_phase: DayPhaseState
    carry_horizon: CarryHorizonState
    behaviour_class: PhaseBehaviourClass
    no_action_bias: PhaseNoActionBias = PhaseNoActionBias.NEUTRAL
    mutable_surface_targets: list[MutableRuntimeSurface] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PhaseCarryoverPolicyAuthorityPacket(BaseModel):
    """Frozen Gate 69 authority for phase-of-day and carryover policy."""

    model_config = ConfigDict(extra="forbid")

    day_phases: list[DayPhaseState] = Field(default_factory=list)
    carry_horizon_states: list[CarryHorizonState] = Field(default_factory=list)
    behaviour_classes: list[PhaseBehaviourClass] = Field(default_factory=list)
    no_action_biases: list[PhaseNoActionBias] = Field(default_factory=list)
    policy_records: list[PhaseCarryPolicyRecord] = Field(default_factory=list)


class RiskAction(StrEnum):
    ALLOW = "allow"
    DERISK = "derisk"
    BLOCK = "block"


class RiskPolicyInput(BaseModel):
    symbol: str = Field(default="NVDA", min_length=1)
    module_id: str = Field(min_length=1)
    requested_at: datetime
    session_phase: SessionClockPhase
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    vix_change_pct_15m: float = Field(ge=-1000, le=1000, default=0.0)
    vvix_change_pct_15m: float = Field(ge=-1000, le=1000, default=0.0)
    data_age_seconds: int = Field(ge=0, default=0)
    gross_exposure_pct: float = Field(ge=0, le=100)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0, default=0)
    conflict_tags: list[str] = Field(default_factory=list)
    vix_caution_threshold: float = Field(default=24.0, gt=0, le=200)
    vix_hot_threshold: float = Field(default=32.0, gt=0, le=200)


class RiskDecision(BaseModel):
    action: RiskAction
    reasons: list[str]
    confidence_scalar: float = Field(ge=0, le=1)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    vix_change_pct_15m: float
    vvix_change_pct_15m: float


class RiskDecisionPayload(BaseModel):
    decision_id: int
    created_at: datetime
    symbol: str
    module_id: str
    requested_at: datetime
    action: RiskAction
    reasons: list[str]
    confidence_scalar: float = Field(ge=0, le=1)
    input_payload: dict[str, object]
    output_payload: dict[str, object]


class RiskDecisionListResponse(BaseModel):
    decisions: list[RiskDecisionPayload]
