"""Typed Gate 21 execution-planning and broker-abstraction contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    EngineScoreContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
)
from nvda_desk.schemas.imported_modules.posture_enrichers import (
    FillBiasAdjusterContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    EntryGateContractOutput,
    LadderConstructorContractOutput,
)


class ExecutionPlanningContractBase(BaseModel):
    """Common metadata shared by every Gate-21 planning contract."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    advisory_only: bool = True
    contract_notes: list[str] = Field(default_factory=list)


class BrokerAdapterContractOutput(ExecutionPlanningContractBase):
    adapter_mode: str
    supported_actions: list[str] = Field(default_factory=list)
    routing_state: str


class EntryPlannerContractOutput(ExecutionPlanningContractBase):
    planned_playbook: str | None = None
    order_style: str
    planned_limit_price: float | None = None
    planned_scale_steps: list[float] = Field(default_factory=list)
    planned_ladder_strikes: list[float] = Field(default_factory=list)
    planner_state: str


class PositionAllocatorContractOutput(ExecutionPlanningContractBase):
    target_position_pct: float = Field(ge=0.0, le=100.0)
    tranche_sizes: list[float] = Field(default_factory=list)
    conviction_band: str
    allocation_state: str


class OrderSimulatorContractOutput(ExecutionPlanningContractBase):
    simulated_fill_price: float | None = None
    slippage_bps: float | None = None
    fill_probability: float = Field(ge=0.0, le=1.0)
    simulation_state: str


class RunTradingBotContractOutput(ExecutionPlanningContractBase):
    run_mode: str
    active_dispatches: int = Field(ge=0)
    dispatch_state: str
    start_reason: str


ExecutionPlanningPayload = (
    BrokerAdapterContractOutput
    | EntryPlannerContractOutput
    | PositionAllocatorContractOutput
    | OrderSimulatorContractOutput
    | RunTradingBotContractOutput
)


class ExecutionPlanningContext(BaseModel):
    """Context required to evaluate Gate-21 planning contracts."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    engine_score: EngineScoreContractOutput
    entry_gate: EntryGateContractOutput
    ladder_constructor: LadderConstructorContractOutput
    fill_bias_adjuster: FillBiasAdjusterContractOutput
    spot_data_capture: SpotDataCaptureContractOutput
    vwap_accumulator: VwapAccumulatorContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
