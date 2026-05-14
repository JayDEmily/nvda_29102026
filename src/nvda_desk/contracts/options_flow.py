"""Options-flow ingress and output contracts for the bounded runtime rebuild."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OptionsFlowContextInput(BaseModel):
    """Typed options-flow input with explicit completeness state."""

    model_config = ConfigDict(extra="forbid")
    spot_price: float | None = None
    front_dte: int | None = None
    next_dte: int | None = None
    missing_fields: list[str] = Field(default_factory=list)


class OptionsFlowContextOutput(BaseModel):
    """Typed options-flow output from the bounded options stage."""

    model_config = ConfigDict(extra="forbid")
    term_structure_state: str = "unknown"
    skew_state: str = "unknown"
    gamma_state: str = "unknown"
    reasons: list[str] = Field(default_factory=list)
