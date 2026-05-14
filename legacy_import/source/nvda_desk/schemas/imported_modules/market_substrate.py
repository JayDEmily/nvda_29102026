"""Typed shared market-data substrate contracts for Gate 18.

These contracts preserve the raw/shared capture layer as explicit DMP-emitting
surfaces without pretending the repo already owns live market-feed ingestion.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    MarketRegimeContextInput,
    MarketRegimeContextOutput,
    OptionsFlowContextInput,
    OptionsFlowContextOutput,
    TemporalContextInput,
    TemporalContextOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
)


class MarketSubstrateContractBase(BaseModel):
    """Common metadata shared by every shared-substrate contract output."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    contract_notes: list[str] = Field(default_factory=list)


class SpotDataCaptureContractOutput(MarketSubstrateContractBase):
    spot_price: float | None = None
    capture_state: str
    proxy_basis: list[str] = Field(default_factory=list)


class PeerEquityCaptureContractOutput(MarketSubstrateContractBase):
    peer_symbols: list[str] = Field(default_factory=list)
    peer_returns: dict[str, float] = Field(default_factory=dict)
    capture_state: str


class OptionsDataCaptureContractOutput(MarketSubstrateContractBase):
    snapshot_count: int | None = Field(default=None, ge=0)
    front_atm_iv: float | None = None
    next_atm_iv: float | None = None
    capture_state: str


class OptionsMetadataCaptureContractOutput(MarketSubstrateContractBase):
    front_dte: int | None = Field(default=None, ge=0)
    next_dte: int | None = Field(default=None, ge=0)
    dominant_strike: float | None = None
    metadata_state: str


class MacroDataCaptureContractOutput(MarketSubstrateContractBase):
    vix_level: float | None = None
    vvix_level: float | None = None
    curve_10s2s: float | None = None
    usdjpy: float | None = None
    capture_state: str


class VwapAccumulatorContractOutput(MarketSubstrateContractBase):
    spot_vwap_10s: float | None = None
    observation_count: int | None = Field(default=None, ge=0)
    accumulation_state: str


class VwapRocContractOutput(MarketSubstrateContractBase):
    vwap_roc: float | None = None
    slope_flag: str
    derivation_state: str


MarketSubstratePayload = (
    SpotDataCaptureContractOutput
    | PeerEquityCaptureContractOutput
    | OptionsDataCaptureContractOutput
    | OptionsMetadataCaptureContractOutput
    | MacroDataCaptureContractOutput
    | VwapAccumulatorContractOutput
    | VwapRocContractOutput
)


class MarketSubstrateContext(BaseModel):
    """Context required to evaluate the shared market-data substrate contracts."""

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
