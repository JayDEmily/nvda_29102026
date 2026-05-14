"""Typed Gate 19 context and scanner contracts.

These contracts sit above the shared market-data substrate and preserve the
remaining context/scanner layer as explicit DMP-emitting surfaces without
pretending the repo already owns hidden live scoring engines.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    MarketRegimeContextInput,
    MarketRegimeContextOutput,
    OptionsFlowContextInput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextInput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
)


class ContextScannerContractBase(BaseModel):
    """Common metadata shared by every Gate-19 context/scanner contract."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class MacroSignalScoreContractOutput(ContextScannerContractBase):
    macro_score: float = Field(ge=0.0, le=1.0)
    macro_bias: str
    event_sensitivity: str


class ExecutionContextScoreContractOutput(ContextScannerContractBase):
    context_score: float = Field(ge=0.0, le=1.0)
    execution_state: str
    desk_window: str


class VixSpreadDetectorContractOutput(ContextScannerContractBase):
    spread: float | None = None
    risk_tag: str
    signal_score: float = Field(ge=0.0, le=1.0)


class VolCorridorContractOutput(ContextScannerContractBase):
    corridor_width: float | None = None
    compression_flag: str
    signal_score: float = Field(ge=0.0, le=1.0)


class OptionsBehaviourClusterContractOutput(ContextScannerContractBase):
    cluster_tag: str
    signal_score: float = Field(ge=0.0, le=1.0)


class AsiaPrecursorContextFilterContractOutput(ContextScannerContractBase):
    precursor_score: float = Field(ge=0.0, le=1.0)
    asia_state: str
    filter_state: str


class MacroAdaptiveWeightingFilterContractOutput(ContextScannerContractBase):
    weight_multiplier: float = Field(ge=0.0)
    weighting_regime: str


class EngineScoreContractOutput(ContextScannerContractBase):
    engine_score: float = Field(ge=0.0, le=1.0)
    conviction_band: str
    engine_state: str


ContextScannerPayload = (
    MacroSignalScoreContractOutput
    | ExecutionContextScoreContractOutput
    | VixSpreadDetectorContractOutput
    | VolCorridorContractOutput
    | OptionsBehaviourClusterContractOutput
    | AsiaPrecursorContextFilterContractOutput
    | MacroAdaptiveWeightingFilterContractOutput
    | EngineScoreContractOutput
)


class ContextScannerContext(BaseModel):
    """Context required to evaluate the Gate-19 context/scanner contracts."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput
    options_flow_input: OptionsFlowContextInput
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    spot_data_capture: SpotDataCaptureContractOutput
    peer_equity_capture: PeerEquityCaptureContractOutput
    options_data_capture: OptionsDataCaptureContractOutput
    options_metadata_capture: OptionsMetadataCaptureContractOutput
    macro_data_capture: MacroDataCaptureContractOutput
    vwap_accumulator: VwapAccumulatorContractOutput
    vwap_roc: VwapRocContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
