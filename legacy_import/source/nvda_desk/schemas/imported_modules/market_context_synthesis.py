"""Typed Gate 29 market-context synthesis contracts.

These contracts sit above the ingress substrate and existing context scanners.
They preserve higher-level scan orchestration surfaces without pretending the
repo already owns a hidden scheduler or live runtime-config service.
"""

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
    EngineScoreContractOutput,
    MacroSignalScoreContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
)


class MarketContextSynthesisContractBase(BaseModel):
    """Common metadata shared by Gate-29 synthesis contracts."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class RunSignalScanContractOutput(MarketContextSynthesisContractBase):
    scan_state: str
    configured_scan_window: str
    enabled_passes: list[str] = Field(default_factory=list)
    candidate_count: int = Field(ge=0)


MarketContextSynthesisPayload = RunSignalScanContractOutput


class MarketContextSynthesisContext(BaseModel):
    """Context required to evaluate the Gate-29 synthesis wrapper contracts."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    regime: MarketRegimeContextOutput
    options_flow: OptionsFlowContextOutput
    posture: PostureRiskOutput
    eligibility: PlaybookEligibilityOutput
    macro_signal_score: MacroSignalScoreContractOutput
    engine_score: EngineScoreContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
