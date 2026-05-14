from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import LifecycleAction
from nvda_desk.schemas.module import ModuleClass, ModuleDescriptor


class CarryRecommendation(StrEnum):
    INCREASE = "increase"
    HOLD_SMALL = "hold_small"
    FLATTEN = "flatten"
    BLOCK = "block"


class CarryHorizon(StrEnum):
    OVERNIGHT = "overnight"
    WEEKEND = "weekend"
    EVENT_CARRY = "event_carry"


class CarryAction(StrEnum):
    FLATTEN = "flatten"
    HOLD_SMALL = "hold_small"
    HOLD_BASELINE = "hold_baseline"
    ADD_CARRY = "add_carry"
    BLOCK_CARRY = "block_carry"


class CloseStateCarryHandoff(BaseModel):
    """Typed intraday close-state handoff into the carry-horizon branch."""

    handoff_version: str = Field(default="carry_handoff.v2", min_length=1)
    symbol: str = Field(default="NVDA", min_length=1)
    evaluation_ts: datetime
    horizon: CarryHorizon
    next_session_open_ts: datetime | None = None
    weekend_window: bool
    event_carry_window: bool
    close_phase: SessionClockPhase
    desk_window: str
    event_window_state: str
    expiry_cycle_state: str
    permission_state: str
    fresh_deployable_capital_pct: float = Field(ge=0, le=100)
    overnight_deployable_capital_pct: float = Field(ge=0, le=100)
    existing_inventory_pct: float = Field(ge=0, le=100)
    overnight_inventory_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)
    inventory_action_bias: str
    thesis_state: str
    dealer_pressure_state: str
    pin_risk_state: str
    options_behavior_cluster: str
    active_family_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    active_playbook_ids: list[str] = Field(default_factory=list)
    lifecycle_setup_variant_id: str | None = None
    lifecycle_execution_expression_id: str | None = None
    lifecycle_state: str | None = None
    lifecycle_next_action: LifecycleAction | None = None
    lifecycle_carry_candidate: bool = False
    lifecycle_action_ceiling: CarryAction | None = None
    lifecycle_fired_rules: list[str] = Field(default_factory=list)
    lifecycle_blocked_rules: list[str] = Field(default_factory=list)
    lifecycle_rationale_codes: list[str] = Field(default_factory=list)
    recommended_action_ceiling: CarryAction
    allowed_actions: list[CarryAction] = Field(default_factory=list)
    rationale_codes: list[str] = Field(default_factory=list)


class OvernightCarryEvaluatorInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v1",
            name="Overnight Carry Evaluator",
            module_class=ModuleClass.SIZING,
            thesis="Advise whether to hold exposure overnight.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    close_distance_to_vwap_pct: float = Field(ge=-100, le=100)
    close_phase: SessionClockPhase
    realised_vol_pct: float = Field(ge=0, le=1000)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)


class OvernightCarryEvaluatorOutput(BaseModel):
    carry_recommendation: CarryRecommendation
    carry_action: CarryAction
    overnight_exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    rationale_codes: list[str]
    review_required: bool


class CarryDerivedContext(BaseModel):
    evaluation_ts: datetime
    last_bar_ts: datetime
    close_phase: SessionClockPhase
    close_distance_to_vwap_pct: float = Field(ge=-100, le=100)
    realised_vol_pct: float = Field(ge=0, le=1000)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)


class OvernightCarryMarketInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v2-market",
            name="Overnight Carry Evaluator",
            module_class=ModuleClass.SIZING,
            thesis="Advise whether to hold exposure overnight using persisted market state.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    evaluation_ts: datetime
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)
    close_state_handoff: CloseStateCarryHandoff | None = None


class OvernightCarryMarketOutput(BaseModel):
    carry_recommendation: CarryRecommendation
    carry_action: CarryAction
    overnight_exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    rationale_codes: list[str]
    review_required: bool
    derived_context: CarryDerivedContext
    applied_handoff: CloseStateCarryHandoff | None = None


class CarryReplayPathSummary(BaseModel):
    path_name: str = Field(min_length=1)
    carry_action: CarryAction
    exposure_pct: float = Field(ge=0, le=100)
    keep_orders_active: bool
    projected_open_price: float = Field(gt=0)
    projected_gap_pct: float
    projected_pnl_pct: float
    rationale_codes: list[str] = Field(default_factory=list)


class OvernightCarryReplayFromMarketInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="overnight-carry-v3-replay",
            name="Overnight Carry Replay Comparator",
            module_class=ModuleClass.SIZING,
            thesis="Compare flatten, hold, and carry-guided overnight paths from persisted market state.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    evaluation_ts: datetime
    asia_precursor_composite: float = Field(ge=-1, le=1)
    risk_budget_remaining_pct: float = Field(ge=0, le=100)
    gross_exposure_pct: float = Field(ge=0, le=100)
    open_orders_count: int = Field(ge=0)
    baseline_hold_exposure_pct: float = Field(default=10.0, ge=0, le=100)
    close_state_handoff: CloseStateCarryHandoff | None = None


class OvernightCarryReplayFromMarketOutput(BaseModel):
    module_id: str = Field(min_length=1)
    evaluation_ts: datetime
    next_session_open_ts: datetime
    next_session_reference_source: str = Field(min_length=1)
    weekend_window: bool
    event_window_open: bool
    carry_horizon: CarryHorizon
    best_path_name: str = Field(min_length=1)
    carry_recommendation: CarryRecommendation
    carry_action: CarryAction
    close_price: float = Field(gt=0)
    next_open_price_reference: float = Field(gt=0)
    path_summaries: list[CarryReplayPathSummary]
    applied_handoff: CloseStateCarryHandoff | None = None
