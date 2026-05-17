from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class BrokerOrderSide(StrEnum):
    BUY = "buy"
    SELL = "sell"


class BrokerOrderType(StrEnum):
    MARKET = "market"
    LIMIT = "limit"


class BrokerOrderStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


_FORBIDDEN_EXECUTION_KEYS = frozenset(
    {
        "account_credentials",
        "broker_session_token",
        "live_broker",
        "live_broker_adapter",
        "network_endpoint",
        "order_submitted",
        "wire_broker_submit",
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


def _reject_live_execution_payload(value: dict[str, Any]) -> dict[str, Any]:
    forbidden = set(_payload_keys(value)) & _FORBIDDEN_EXECUTION_KEYS
    if forbidden:
        raise ValueError(
            "live_broker execution payload is forbidden: " + ", ".join(sorted(forbidden))
        )
    return value


class BrokerOrderIntent(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    order_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    side: BrokerOrderSide
    quantity: float = Field(gt=0.0)
    order_type: BrokerOrderType
    time_in_force: str = Field(min_length=1)
    limit_price: float | None = Field(default=None, gt=0.0)
    source_handoff_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    broker_protocol_only: bool = True
    execution_allowed: bool = False

    @field_validator("symbol")
    @classmethod
    def _normalise_symbol(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("metadata")
    @classmethod
    def _validate_metadata(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _reject_live_execution_payload(value)

    @model_validator(mode="after")
    def _validate_boundary(self) -> "BrokerOrderIntent":
        if self.broker_protocol_only is not True:
            raise ValueError("broker order intent must remain protocol-only")
        if self.execution_allowed is not False:
            raise ValueError("broker order intent must not allow live execution")
        if self.order_type == BrokerOrderType.LIMIT and self.limit_price is None:
            raise ValueError("limit broker order intent requires limit_price")
        return self


class PaperOrderResult(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    order_id: str
    status: BrokerOrderStatus
    accepted_quantity: float = Field(ge=0.0)
    accepted_price: float | None = None
    broker_protocol_only: bool = True
    execution_allowed: bool = False

    @model_validator(mode="after")
    def _validate_boundary(self) -> "PaperOrderResult":
        if self.broker_protocol_only is not True or self.execution_allowed is not False:
            raise ValueError("paper order result must remain non-executing")
        return self


class BrokerOrderEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    order_id: str
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class BrokerFillEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fill_id: str
    order_id: str
    symbol: str
    side: BrokerOrderSide
    quantity: float
    fill_price: float
    paper_only: bool = True


class BrokerPositionSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position_id: str
    symbol: str
    quantity: float
    average_price: float
    source_order_ids: tuple[str, ...] = Field(default_factory=tuple)


class BrokerAccountState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = "paper-account"
    cash_balance: float = 0.0
    equity_value: float = 0.0
    buying_power: float = 0.0
    paper_only: bool = True
    network_execution_opened: bool = False


class BrokerOrderEventCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    events: tuple[BrokerOrderEvent, ...] = Field(default_factory=tuple)


class BrokerFillEventCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fills: tuple[BrokerFillEvent, ...] = Field(default_factory=tuple)


class BrokerPositionCollection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    positions: tuple[BrokerPositionSnapshot, ...] = Field(default_factory=tuple)
