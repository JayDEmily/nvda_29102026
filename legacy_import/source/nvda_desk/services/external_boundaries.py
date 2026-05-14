from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any, Protocol

from pydantic import BaseModel, Field


class AccountState(BaseModel):
    cash: float = Field(ge=0)
    equity: float = Field(ge=0)
    buying_power: float = Field(ge=0)


class Position(BaseModel):
    symbol: str = Field(min_length=1)
    quantity: float
    average_price: float = Field(gt=0)


class OrderIntent(BaseModel):
    symbol: str = Field(min_length=1)
    side: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    order_type: str = Field(default="limit", min_length=1)
    limit_price: float | None = Field(default=None, gt=0)


class BrokerOrderRef(BaseModel):
    order_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    submitted_at: datetime


class OrderEvent(BaseModel):
    order_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    detail: str = Field(min_length=1)
    event_ts: datetime


class OpenAIResponseRequest(BaseModel):
    prompt: str = Field(min_length=1)
    conversation_id: str | None = None
    tool_names: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OpenAIResponseArtifact(BaseModel):
    response_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    structured_output: dict[str, Any] = Field(default_factory=dict)
    referenced_tools: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class BrokerAdapter(Protocol):
    async def get_account_state(self) -> AccountState: ...
    async def get_positions(self) -> list[Position]: ...
    async def place_order(self, order: OrderIntent) -> BrokerOrderRef: ...
    async def cancel_order(self, order_id: str) -> None: ...
    async def stream_order_events(self) -> AsyncIterator[OrderEvent]: ...


class OpenAIOrchestrator(Protocol):
    async def respond(self, request: OpenAIResponseRequest) -> OpenAIResponseArtifact: ...


class InMemoryBrokerAdapter:
    def __init__(self) -> None:
        self._account = AccountState(cash=100000.0, equity=100000.0, buying_power=100000.0)
        self._positions: list[Position] = []
        self._events: list[OrderEvent] = []

    async def get_account_state(self) -> AccountState:
        return self._account

    async def get_positions(self) -> list[Position]:
        return list(self._positions)

    async def place_order(self, order: OrderIntent) -> BrokerOrderRef:
        order_id = f"paper-{len(self._events) + 1}"
        submitted_at = datetime.now(tz=UTC)
        notional = order.quantity * (order.limit_price or 0.0)
        if order.side.lower() == "buy":
            self._account = self._account.model_copy(
                update={
                    "cash": round(max(self._account.cash - notional, 0.0), 4),
                    "equity": round(self._account.equity, 4),
                    "buying_power": round(max(self._account.buying_power - notional, 0.0), 4),
                }
            )
        self._positions.append(
            Position(
                symbol=order.symbol,
                quantity=order.quantity,
                average_price=order.limit_price or 0.0,
            )
        )
        self._events.append(
            OrderEvent(
                order_id=order_id,
                status="filled",
                detail="offline_stub_fill",
                event_ts=submitted_at,
            )
        )
        return BrokerOrderRef(order_id=order_id, status="filled", submitted_at=submitted_at)

    async def cancel_order(self, order_id: str) -> None:
        self._events.append(
            OrderEvent(
                order_id=order_id,
                status="cancelled",
                detail="offline_stub_cancel",
                event_ts=datetime.now(tz=UTC),
            )
        )

    async def stream_order_events(self) -> AsyncIterator[OrderEvent]:
        for event in list(self._events):
            yield event


class NullOpenAIOrchestrator:
    async def respond(self, request: OpenAIResponseRequest) -> OpenAIResponseArtifact:
        return OpenAIResponseArtifact(
            response_id="unverified-openai-boundary",
            status="unverified_stub",
            structured_output={
                "prompt_length": len(request.prompt),
                "tool_count": len(request.tool_names),
            },
            referenced_tools=request.tool_names,
            notes=[
                "Sandbox boundary only.",
                "No live OpenAI Responses API call was attempted.",
            ],
        )
