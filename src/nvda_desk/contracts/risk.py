from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FinalRiskJoinReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str
    confidence_scalar: float = 0.0
    reasons: list[str] = Field(default_factory=list)
