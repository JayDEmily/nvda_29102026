from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class MarketSubstrateObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observation_id: str = Field(min_length=1)
    signal_family_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    value: Decimal
    units: str = Field(min_length=1)
    source_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source_ids", "tags", mode="before")
    @classmethod
    def _detach_string_lists(cls, value: Any) -> list[str]:
        return [str(item) for item in list(value or [])]


class MarketSubstrateSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    substrate_id: str = Field(min_length=1)
    observations: list[MarketSubstrateObservation] = Field(default_factory=list)
    decision_authority: str = "trace_only_market_substrate"
    trade_decision_side_effects: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _reject_trade_decision_side_effects(self) -> "MarketSubstrateSnapshot":
        if self.trade_decision_side_effects:
            raise ValueError("market_substrate_trade_decision_side_effects_not_admitted")
        self.observations = [observation.model_copy(deep=True) for observation in self.observations]
        return self

    @property
    def signal_family_ids(self) -> list[str]:
        return sorted({observation.signal_family_id for observation in self.observations})

    def by_signal_family(self, signal_family_id: str) -> list[MarketSubstrateObservation]:
        return [
            observation.model_copy(deep=True)
            for observation in self.observations
            if observation.signal_family_id == signal_family_id
        ]
