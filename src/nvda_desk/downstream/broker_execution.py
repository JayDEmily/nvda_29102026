from __future__ import annotations

from copy import deepcopy

from nvda_desk.contracts.broker_execution import (
    BrokerAccountState,
    BrokerFillEvent,
    BrokerFillEventCollection,
    BrokerOrderEvent,
    BrokerOrderEventCollection,
    BrokerOrderIntent,
    BrokerOrderSide,
    BrokerOrderStatus,
    BrokerPositionCollection,
    BrokerPositionSnapshot,
    PaperOrderResult,
)
from nvda_desk.persistence.execution_records import ExecutionRecordsRepository


class PaperBrokerExecutionService:
    def __init__(
        self,
        *,
        starting_cash: float = 0.0,
        execution_records: ExecutionRecordsRepository | None = None,
    ) -> None:
        self._cash = float(starting_cash)
        self._orders: list[BrokerOrderEvent] = []
        self._fills: list[BrokerFillEvent] = []
        self._positions: dict[str, BrokerPositionSnapshot] = {}
        self._records = execution_records

    def place_paper_order(self, intent: BrokerOrderIntent) -> PaperOrderResult:
        price = intent.limit_price if intent.limit_price is not None else 0.0
        result = PaperOrderResult(
            order_id=intent.order_id,
            status=BrokerOrderStatus.ACCEPTED,
            accepted_quantity=intent.quantity,
            accepted_price=price,
        )
        event = BrokerOrderEvent(
            event_id=f"{intent.order_id}::accepted",
            order_id=intent.order_id,
            event_type="paper_order_accepted",
            payload=intent.model_dump(mode="json"),
        )
        signed_quantity = (
            intent.quantity if intent.side == BrokerOrderSide.BUY else -intent.quantity
        )
        fill = BrokerFillEvent(
            fill_id=f"{intent.order_id}::fill",
            order_id=intent.order_id,
            symbol=intent.symbol,
            side=intent.side,
            quantity=signed_quantity,
            fill_price=price,
        )
        self._orders.append(event)
        self._fills.append(fill)
        self._cash -= signed_quantity * price
        self._apply_position(intent=intent, fill=fill)
        if self._records is not None:
            self._records.append_record(
                {"record_type": "order_event", **event.model_dump(mode="json")}
            )
            self._records.append_record(
                {"record_type": "fill_event", **fill.model_dump(mode="json")}
            )
        return result

    def list_order_events(self) -> BrokerOrderEventCollection:
        return BrokerOrderEventCollection(events=tuple(deepcopy(self._orders)))

    def list_fill_events(self) -> BrokerFillEventCollection:
        return BrokerFillEventCollection(fills=tuple(deepcopy(self._fills)))

    def list_positions(self) -> BrokerPositionCollection:
        return BrokerPositionCollection(positions=tuple(deepcopy(list(self._positions.values()))))

    def get_account_state(self) -> BrokerAccountState:
        market_value = sum(
            position.quantity * position.average_price for position in self._positions.values()
        )
        equity = self._cash + market_value
        return BrokerAccountState(
            cash_balance=self._cash, equity_value=equity, buying_power=max(self._cash, 0.0)
        )

    def _apply_position(self, *, intent: BrokerOrderIntent, fill: BrokerFillEvent) -> None:
        position_id = f"paper::{intent.symbol}"
        existing = self._positions.get(position_id)
        if existing is None:
            self._positions[position_id] = BrokerPositionSnapshot(
                position_id=position_id,
                symbol=intent.symbol,
                quantity=fill.quantity,
                average_price=fill.fill_price,
                source_order_ids=(intent.order_id,),
            )
            return
        new_quantity = existing.quantity + fill.quantity
        if new_quantity == 0:
            avg = fill.fill_price
        else:
            avg = (
                (existing.quantity * existing.average_price) + (fill.quantity * fill.fill_price)
            ) / new_quantity
        self._positions[position_id] = BrokerPositionSnapshot(
            position_id=position_id,
            symbol=intent.symbol,
            quantity=new_quantity,
            average_price=avg,
            source_order_ids=existing.source_order_ids + (intent.order_id,),
        )
