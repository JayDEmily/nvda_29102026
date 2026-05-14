"""Typed tranche-A contract surfaces for imported upstream detectors and selectors.

These contracts let the repo import bounded archive modules as explicit,
reviewable, DMP-emitting surfaces without pretending that every live dependency
is already solved.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    MarketRegimeContextInput,
    MarketRegimeContextOutput,
    OptionsFlowContextInput,
    OptionsFlowContextOutput,
    PlaybookEligibilityOutput,
    PostureRiskOutput,
    TemporalContextInput,
    TemporalContextOutput,
)


class ContractDependencyStatus(StrEnum):
    """Dependency resolution states for tranche-A imports."""

    SATISFIED = "satisfied"
    PROXIED_FROM_RUNTIME = "proxied_from_runtime"
    FENCED_MISSING_SOURCE = "fenced_missing_source"


class ContractComputationMode(StrEnum):
    """How one tranche-A contract surface was computed."""

    DERIVED_FROM_RUNTIME = "derived_from_runtime"
    DERIVED_FROM_RUNTIME_PROXY = "derived_from_runtime_proxy"
    FENCED_CONTRACT_ONLY = "fenced_contract_only"


class ContractDependencyFence(BaseModel):
    """One dependency and the honest state of that dependency."""

    model_config = ConfigDict(extra="forbid")

    dependency: str
    status: ContractDependencyStatus
    note: str


class TrancheAContractBase(BaseModel):
    """Common metadata shared by every tranche-A contract output."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class EventFlagCaptureContractOutput(TrancheAContractBase):
    event_flags: list[str] = Field(default_factory=list)
    next_event_minutes: int | None = None
    event_window_state: str
    capture_state: str


class RealizedVolatilityEngineContractOutput(TrancheAContractBase):
    rv_5d: float | None = None
    rv_10d: float | None = None
    vol_compression: str
    vol_direction: str
    signal_score: float
    proxy_basis: list[str] = Field(default_factory=list)


class VolumeSpikeFilterContractOutput(TrancheAContractBase):
    signal_score: float
    spike_count: int | None = None
    trap_flag: bool | None = None
    detection_state: str


class PeerDivergenceContractOutput(TrancheAContractBase):
    coherence_flag: str
    correlation: float | None = None
    signal_score: float
    peer_basis: list[str] = Field(default_factory=list)


class GammaPressureContractOutput(TrancheAContractBase):
    signal_score: float
    tag: str
    zone_gamma: str


class IvVsRvAnalysisContractOutput(TrancheAContractBase):
    anomaly_flag: bool
    ivrv_ratio: float | None = None
    signal_score: float


class SkewInflectionContractOutput(TrancheAContractBase):
    inflection_tag: str
    signal_score: float
    skew_change: float | None = None


class SignalConflictDetectorContractOutput(TrancheAContractBase):
    signal_conflicts: list[str] = Field(default_factory=list)
    conflict_score: float
    conflict_state: str


class ModelConfidenceScorerContractOutput(TrancheAContractBase):
    model_confidence: float
    confidence_band: str


class ConvictionTierAllocatorContractOutput(TrancheAContractBase):
    conviction_tier: str
    conviction_score: float


class EntryGateContractOutput(TrancheAContractBase):
    entry_allowed: bool
    entry_confidence: float
    suppression_tag: str


class LadderConstructorContractOutput(TrancheAContractBase):
    expiry: int | None = None
    ladder_span: float | None = None
    ladder_strikes: list[float] = Field(default_factory=list)
    constructor_state: str


class ArchetypeMatcherContractOutput(TrancheAContractBase):
    pattern_tag: str
    signal_score: float
    matched_playbook: str | None = None


TrancheAImportedPayload = (
    EventFlagCaptureContractOutput
    | RealizedVolatilityEngineContractOutput
    | VolumeSpikeFilterContractOutput
    | PeerDivergenceContractOutput
    | GammaPressureContractOutput
    | IvVsRvAnalysisContractOutput
    | SkewInflectionContractOutput
    | SignalConflictDetectorContractOutput
    | ModelConfidenceScorerContractOutput
    | ConvictionTierAllocatorContractOutput
    | EntryGateContractOutput
    | LadderConstructorContractOutput
    | ArchetypeMatcherContractOutput
)


class TrancheAUpstreamContext(BaseModel):
    """Context required to evaluate tranche-A upstream detectors."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput
    options_flow_input: OptionsFlowContextInput
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None


class TrancheASelectorContext(BaseModel):
    """Context required to evaluate tranche-A posture and eligibility selectors."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput | None = None
    execution: ExecutionExpressionOutput | None = None
    stack_id: str | None = None
    coefficient_set_id: str | None = None
