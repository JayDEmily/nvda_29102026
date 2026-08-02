"""Options-flow ingress and output contracts for the bounded runtime rebuild."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OptionsEvidenceEnvelope(BaseModel):
    """Typed options evidence retained above preparation and cognition."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    evidence_id: str
    source_artifact_id: str
    capture_id: str
    input_schema_version: str
    adapter_policy_version: str
    effective_at_utc: datetime
    observed_at_utc: datetime
    captured_at_utc: datetime
    semantic_fingerprint: str
    completeness_state: Literal["complete", "degraded", "unavailable"]
    spot_price: float | None = None
    front_dte: int | None = None
    next_dte: int | None = None
    missing_fields: tuple[str, ...] = ()


class OptionsFlowContextInput(BaseModel):
    """Typed options-flow input with explicit completeness state."""

    model_config = ConfigDict(extra="forbid")
    common_context_ref: str | None = None
    options_evidence_ref: str | None = None
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
