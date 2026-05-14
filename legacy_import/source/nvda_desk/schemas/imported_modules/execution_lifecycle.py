"""Typed Gate 22 execution-state, exit, and lifecycle contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    InventoryState,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.execution_planning import (
    BrokerAdapterContractOutput,
    EntryPlannerContractOutput,
    OrderSimulatorContractOutput,
    PositionAllocatorContractOutput,
    RunTradingBotContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    SpotDataCaptureContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    EntryGateContractOutput,
)


class ExecutionLifecycleContractBase(BaseModel):
    """Common metadata shared by every Gate-22 lifecycle contract."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    advisory_only: bool = True
    contract_notes: list[str] = Field(default_factory=list)


class DynamicPartialExitModelContractOutput(ExecutionLifecycleContractBase):
    partial_exit_levels: list[float] = Field(default_factory=list)
    partial_exit_fracs: list[float] = Field(default_factory=list)
    model_state: str


class TakeProfitContractOutput(ExecutionLifecycleContractBase):
    profit_targets: list[float] = Field(default_factory=list)
    target_basis: str
    take_profit_state: str


class TrailingStopContractOutput(ExecutionLifecycleContractBase):
    trailing_stop_pct: float | None = Field(default=None, ge=0.0, le=1.0)
    trail_anchor: float | None = None
    stop_state: str


class UnrealizedTrackerContractOutput(ExecutionLifecycleContractBase):
    mark_price: float
    unrealized_pnl_pct: float
    tracker_state: str


class PositionBookContractOutput(ExecutionLifecycleContractBase):
    open_position_state: str
    live_position_pct: float = Field(ge=0.0, le=100.0)
    open_order_count: int = Field(ge=0)
    book_state: str


class TradeReentryMarkerContractOutput(ExecutionLifecycleContractBase):
    reentry_allowed: bool
    cooldown_minutes: int | None = Field(default=None, ge=0)
    reentry_state: str


class LadderContinuityTrackerContractOutput(ExecutionLifecycleContractBase):
    continuity_state: str
    continuity_score: float = Field(ge=0.0, le=1.0)
    ladder_hash: str | None = None


class FillFeedbackRouterContractOutput(ExecutionLifecycleContractBase):
    feedback_route: str
    route_confidence: float = Field(ge=0.0, le=1.0)
    router_state: str


class ExecutionLogWriterContractOutput(ExecutionLifecycleContractBase):
    log_state: str
    event_count: int = Field(ge=0)
    missing_surfaces: list[str] = Field(default_factory=list)


class ExecutionTagsContractOutput(ExecutionLifecycleContractBase):
    tags: list[str] = Field(default_factory=list)
    tagging_state: str


class TradeLoggerContractOutput(ExecutionLifecycleContractBase):
    trade_log_state: str
    record_count: int = Field(ge=0)
    last_event_tag: str | None = None


ExecutionLifecyclePayload = (
    DynamicPartialExitModelContractOutput
    | TakeProfitContractOutput
    | TrailingStopContractOutput
    | UnrealizedTrackerContractOutput
    | PositionBookContractOutput
    | TradeReentryMarkerContractOutput
    | LadderContinuityTrackerContractOutput
    | FillFeedbackRouterContractOutput
    | ExecutionLogWriterContractOutput
    | ExecutionTagsContractOutput
    | TradeLoggerContractOutput
)


class ExecutionLifecycleContext(BaseModel):
    """Context required to evaluate Gate-22 lifecycle contracts."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    inventory: InventoryState
    entry_gate: EntryGateContractOutput
    spot_data_capture: SpotDataCaptureContractOutput
    broker_adapter: BrokerAdapterContractOutput
    entry_planner: EntryPlannerContractOutput
    position_allocator: PositionAllocatorContractOutput
    order_simulator: OrderSimulatorContractOutput
    run_trading_bot: RunTradingBotContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
