"""Typed Gate 20 eligibility and posture enricher contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    MarketRegimeContextOutput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.context_scanners import (
    AsiaPrecursorContextFilterContractOutput,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    MacroAdaptiveWeightingFilterContractOutput,
    MacroSignalScoreContractOutput,
    OptionsBehaviourClusterContractOutput,
    VixSpreadDetectorContractOutput,
    VolCorridorContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
)


class PostureEnricherContractBase(BaseModel):
    """Common metadata shared by every Gate-20 enricher contract."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    advisory_only: bool = True
    contract_notes: list[str] = Field(default_factory=list)


class FillBiasAdjusterContractOutput(PostureEnricherContractBase):
    bias_tag: str
    adjustment_score: float = Field(ge=0.0, le=1.0)
    fill_bias: str


class ArchetypeTaggerContractOutput(PostureEnricherContractBase):
    archetype_tag: str
    confidence: float = Field(ge=0.0, le=1.0)


class CompressionRegimeDetectorContractOutput(PostureEnricherContractBase):
    compression_state: str
    signal_score: float = Field(ge=0.0, le=1.0)


class ObvViFlowConfirmationContractOutput(PostureEnricherContractBase):
    confirmation_state: str
    confirmation_score: float = Field(ge=0.0, le=1.0)


class TailHedgeInjectorContractOutput(PostureEnricherContractBase):
    hedge_overlay_tag: str
    hedge_ratio: float = Field(ge=0.0, le=1.0)
    injector_state: str


class VolatilitySentimentIndexContractOutput(PostureEnricherContractBase):
    sentiment_index: float = Field(ge=0.0, le=1.0)
    sentiment_state: str


PostureEnricherPayload = (
    FillBiasAdjusterContractOutput
    | ArchetypeTaggerContractOutput
    | CompressionRegimeDetectorContractOutput
    | ObvViFlowConfirmationContractOutput
    | TailHedgeInjectorContractOutput
    | VolatilitySentimentIndexContractOutput
)


class PostureEnricherContext(BaseModel):
    """Context required to evaluate Gate-20 posture enrichers."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    macro_signal_score: MacroSignalScoreContractOutput
    execution_context_score: ExecutionContextScoreContractOutput
    vix_spread_detector: VixSpreadDetectorContractOutput
    vol_corridor: VolCorridorContractOutput
    options_behaviour_cluster: OptionsBehaviourClusterContractOutput
    asia_precursor_context_filter: AsiaPrecursorContextFilterContractOutput
    macro_adaptive_weighting_filter: MacroAdaptiveWeightingFilterContractOutput
    engine_score: EngineScoreContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
