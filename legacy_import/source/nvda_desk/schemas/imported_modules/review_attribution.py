"""Typed Gate 23 review, P&L, attribution, and variant-tracking contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    ReviewExplanationOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    EngineScoreContractOutput,
    MacroSignalScoreContractOutput,
)
from nvda_desk.schemas.imported_modules.execution_lifecycle import (
    ExecutionTagsContractOutput,
    PositionBookContractOutput,
    TradeLoggerContractOutput,
    UnrealizedTrackerContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
)


class ReviewAttributionContractBase(BaseModel):
    """Common metadata shared by every Gate-23 review-chain contract."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    advisory_only: bool = True
    contract_notes: list[str] = Field(default_factory=list)


class ProfitLossLedgerContractOutput(ReviewAttributionContractBase):
    realized_pnl_pct: float
    unrealized_pnl_pct: float
    gross_exposure_pct: float = Field(ge=0.0, le=100.0)
    ledger_state: str


class ModuleTraceAttributionContractOutput(ReviewAttributionContractBase):
    leading_modules: list[str] = Field(default_factory=list)
    attribution_confidence: float = Field(ge=0.0, le=1.0)
    attribution_state: str


class DailySummaryContractOutput(ReviewAttributionContractBase):
    summary_headline: str
    day_state: str
    key_points: list[str] = Field(default_factory=list)


class FeedbackSummaryWriterContractOutput(ReviewAttributionContractBase):
    feedback_grade: str
    feedback_actions: list[str] = Field(default_factory=list)
    summary_state: str


class ModuleScoreAttributorContractOutput(ReviewAttributionContractBase):
    module_scores: dict[str, float] = Field(default_factory=dict)
    score_state: str


class VariantTraceLoggerContractOutput(ReviewAttributionContractBase):
    variant_id: str
    active_playbooks: list[str] = Field(default_factory=list)
    trace_state: str


class VariantPerformanceTrackerContractOutput(ReviewAttributionContractBase):
    performance_score: float = Field(ge=0.0, le=1.0)
    performance_band: str
    tracker_state: str


class ConfidenceDivergenceLoggerContractOutput(ReviewAttributionContractBase):
    divergence_score: float = Field(ge=0.0, le=1.0)
    divergence_state: str
    compared_fields: list[str] = Field(default_factory=list)


class MacroAlignmentCheckerContractOutput(ReviewAttributionContractBase):
    macro_alignment_state: str
    alignment_score: float = Field(ge=0.0, le=1.0)
    macro_flags: list[str] = Field(default_factory=list)


ReviewAttributionPayload = (
    ProfitLossLedgerContractOutput
    | ModuleTraceAttributionContractOutput
    | DailySummaryContractOutput
    | FeedbackSummaryWriterContractOutput
    | ModuleScoreAttributorContractOutput
    | VariantTraceLoggerContractOutput
    | VariantPerformanceTrackerContractOutput
    | ConfidenceDivergenceLoggerContractOutput
    | MacroAlignmentCheckerContractOutput
)


class ReviewAttributionContext(BaseModel):
    """Context required to evaluate Gate-23 review-chain contracts."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    execution: ExecutionExpressionOutput
    review: ReviewExplanationOutput
    engine_score: EngineScoreContractOutput
    macro_signal_score: MacroSignalScoreContractOutput
    unrealized_tracker: UnrealizedTrackerContractOutput
    position_book: PositionBookContractOutput
    execution_tags: ExecutionTagsContractOutput
    trade_logger: TradeLoggerContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
