from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LadderDecision(StrEnum):
    ACCEPT = "accept"
    REVISE = "revise"
    REJECT = "reject"


class LadderConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LadderRungInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rung_id: str = Field(min_length=1)
    limit_price: Decimal
    notional_usd: Decimal
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def _detach_tags(cls, value: Any) -> list[str]:
        return [str(item) for item in list(value or [])]


class StrategicLadderObservationContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(min_length=1)
    spot_price: Decimal
    negative_gamma_active: bool = False
    event_risk_active: bool = False
    liquidity_state: str = "normal"


class StrategicLadderValidationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=1)
    rungs: list[LadderRungInput] = Field(default_factory=list)
    observation_context: StrategicLadderObservationContext | None = None

    @model_validator(mode="after")
    def _validate_unique_rungs(self) -> "StrategicLadderValidationRequest":
        rung_ids = [rung.rung_id for rung in self.rungs]
        duplicates = sorted({rung_id for rung_id in rung_ids if rung_ids.count(rung_id) > 1})
        if duplicates:
            raise ValueError(f"duplicate strategic ladder rung ids: {duplicates}")
        return self


class LadderMarketEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str | None = None
    spot_price: Decimal | None = None
    distance_from_spot: Decimal | None = None
    market_state: str = "not_evaluated"
    reasons: list[str] = Field(default_factory=list)


class LadderRungResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rung_id: str = Field(min_length=1)
    rung_decision: LadderDecision
    confidence: LadderConfidence
    market_evidence: LadderMarketEvidence = Field(default_factory=LadderMarketEvidence)


class StrikeZoneSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1)
    score: Decimal
    reasons: list[str] = Field(default_factory=list)


class SupervisoryOverlay(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overlay_state: str = "clear"
    reasons: list[str] = Field(default_factory=list)


class StrategicLadderValidationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=1)
    overall_decision: LadderDecision
    rung_results: list[LadderRungResult] = Field(default_factory=list)
    execution_authority: str = "not_authorised"


class StrategicLadderMarketValidationOutput(StrategicLadderValidationOutput):
    strike_zone_signals: list[StrikeZoneSignal] = Field(default_factory=list)
    supervisory_overlay: SupervisoryOverlay = Field(default_factory=SupervisoryOverlay)
