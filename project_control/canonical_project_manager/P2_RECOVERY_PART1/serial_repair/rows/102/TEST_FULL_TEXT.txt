from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.api.app import create_app
from nvda_desk.contracts.broker_execution import BrokerOrderIntent
from nvda_desk.downstream.broker_execution import PaperBrokerExecutionService


def test_paper_broker_order_contract_records_order_event_fill_position_and_account_state() -> None:
    service = PaperBrokerExecutionService(starting_cash=100_000.0)
    intent = BrokerOrderIntent(
        order_id="order-1",
        symbol="NVDA",
        side="buy",
        quantity=2,
        order_type="limit",
        limit_price=125.5,
        time_in_force="day",
        source_handoff_id="handoff-1",
    )

    result = service.place_paper_order(intent)

    assert result.order_id == "order-1"
    assert result.status == "accepted"
    assert result.broker_protocol_only is True
    assert result.execution_allowed is False
    assert service.list_order_events().events[0].event_type == "paper_order_accepted"
    assert service.list_fill_events().fills[0].fill_price == 125.5
    assert service.list_positions().positions[0].quantity == 2
    assert service.get_account_state().cash_balance == 99_749.0


def test_broker_order_side_is_closed_and_execution_payloads_stay_offline() -> None:
    with pytest.raises(ValidationError):
        BrokerOrderIntent(
            order_id="order-bad",
            symbol="NVDA",
            side="short",  # type: ignore[arg-type]
            quantity=1,
            order_type="market",
            time_in_force="day",
        )

    with pytest.raises(ValidationError, match="live_broker"):
        BrokerOrderIntent(
            order_id="order-live",
            symbol="NVDA",
            side="buy",
            quantity=1,
            order_type="market",
            time_in_force="day",
            metadata={"live_broker_adapter": "forbidden"},
        )


def test_api_exposes_paper_broker_lifecycle_without_network_execution() -> None:
    app = create_app()
    expected = {
        "place_paper_order",
        "list_broker_order_events",
        "list_broker_fill_events",
        "list_broker_positions",
        "get_broker_account_state",
    }
    assert expected.issubset(app.route_handlers)

    result = app.place_paper_order(
        {
            "order_id": "api-order-1",
            "symbol": "NVDA",
            "side": "sell",
            "quantity": 1,
            "order_type": "market",
            "time_in_force": "day",
        }
    )

    assert result["status"] == "accepted"
    assert result["execution_allowed"] is False
    assert app.list_broker_order_events()[0]["order_id"] == "api-order-1"
    assert app.list_broker_fill_events()[0]["order_id"] == "api-order-1"
    assert app.list_broker_positions()[0]["symbol"] == "NVDA"
    assert app.get_broker_account_state()["account_id"] == "paper-account"
