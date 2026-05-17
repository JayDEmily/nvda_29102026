from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator

_FORBIDDEN_TRADING_KEYS = frozenset(
    {
        "broker_order_id",
        "capital_sizing",
        "execution_allowed",
        "live_order_placement",
        "order_submitted",
        "position_mutation",
        "trade_decision",
    }
)


def _payload_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _payload_keys(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _payload_keys(child)


class DailyPnlReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    trade_date: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    realised_pnl_usd: float = 0.0
    unrealised_pnl_usd: float = 0.0
    fees_usd: float = 0.0
    evidence_ids: tuple[str, ...] = Field(default_factory=tuple)
    context: dict[str, Any] = Field(default_factory=dict)
    trading_decision_mutated: bool = False

    @field_validator("symbol")
    @classmethod
    def _normalise_symbol(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("context")
    @classmethod
    def _reject_trading_authority(cls, value: dict[str, Any]) -> dict[str, Any]:
        forbidden = set(_payload_keys(value)) & _FORBIDDEN_TRADING_KEYS
        if forbidden:
            raise ValueError(
                "daily pnl context contains trading authority keys: " + ", ".join(sorted(forbidden))
            )
        return value

    @model_validator(mode="after")
    def _validate_reporting_only(self) -> "DailyPnlReport":
        if self.trading_decision_mutated:
            raise ValueError("daily pnl report must not mutate trading decisions")
        return self

    @computed_field
    @property
    def total_pnl_usd(self) -> float:
        return self.realised_pnl_usd + self.unrealised_pnl_usd - self.fees_usd


class DailyPnlReportCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reports: tuple[DailyPnlReport, ...] = Field(default_factory=tuple)
