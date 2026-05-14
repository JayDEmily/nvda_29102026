"""Typed Gate 33 ladder-readiness overlay contracts.

This module preserves the remaining ladder-shaping overlay that sits between
eligibility-time strike construction and later execution planning. It keeps the
VVIX-aware shaping logic explicit without pretending the repo owns a live broker
or hidden volatility feed beyond the existing runtime inputs.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import OptionsFlowContextOutput, TemporalContextOutput
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    LadderConstructorContractOutput,
)


class LadderReadinessContractBase(BaseModel):
    """Common metadata shared by Gate-33 ladder-readiness overlays."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: str
    computation_mode: ContractComputationMode
    dependency_fences: list[ContractDependencyFence] = Field(default_factory=list)
    upstream_contract_slugs: list[str] = Field(default_factory=list)
    advisory_only: bool = True
    contract_notes: list[str] = Field(default_factory=list)


class VvixLadderShaperContractOutput(LadderReadinessContractBase):
    vvix_regime: str
    ladder_width_multiplier: float = Field(gt=0.0)
    reshaped_ladder: list[float] = Field(default_factory=list)
    shaper_state: str


LadderReadinessPayload = VvixLadderShaperContractOutput


class LadderReadinessContext(BaseModel):
    """Context required to evaluate the Gate-33 ladder-readiness overlays."""

    model_config = ConfigDict(extra="forbid")

    emitted_at: datetime
    temporal: TemporalContextOutput
    options_flow: OptionsFlowContextOutput
    ladder_constructor: LadderConstructorContractOutput
    macro_data_capture: MacroDataCaptureContractOutput
    stack_id: str | None = None
    coefficient_set_id: str | None = None
