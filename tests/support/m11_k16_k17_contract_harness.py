from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
import importlib

from tests.support.m10_k15_contract_harness import production_api as m10_api, production_capital_receipt


def weighted_position(existing_qty: Decimal, existing_cost: Decimal, fill_qty: Decimal, fill_price: Decimal):
    if fill_qty <= 0 or fill_price <= 0 or existing_qty < 0 or existing_cost < 0:
        raise ValueError("invalid_position_arithmetic")
    qty = existing_qty + fill_qty
    cost = existing_cost + fill_qty * fill_price
    return qty, cost, cost / qty


def lifecycle_quantity(action: str, current: Decimal, requested: Decimal | None) -> Decimal:
    if action == "hold":
        if requested is not None:
            raise ValueError("hold_carries_no_quantity")
        return current
    if action == "trim":
        if requested is None or requested <= 0 or requested >= current:
            raise ValueError("trim_quantity_invalid")
        return current - requested
    if action == "close":
        if requested != current:
            raise ValueError("close_quantity_must_equal_position")
        return Decimal("0")
    raise ValueError("unsupported_lifecycle_action")


def production_api():
    module = importlib.import_module("nvda_desk.m11_portfolio_lifecycle")
    names = ("PositionState", "PortfolioSnapshot", "LifecycleDecision", "CloseReceipt", "FillReconciliationReceipt", "PortfolioLifecycleService")
    return {name: getattr(module, name) for name in names}


def production_execution_receipt(*, limit_price: Decimal = Decimal("100"), when: datetime = datetime(2026, 8, 1, 2, 0, tzinfo=UTC)):
    api = m10_api(); capital = production_capital_receipt()
    policy = api["PlacementPolicy"](quantity_quantum=Decimal("0.001"))
    gateway = api["ExecutionGateway"]()
    intent = gateway.create_intent(capital, policy, limit_price=limit_price, intent_at_utc=when)
    return gateway.execute(intent, api["PaperExecutionPort"](), executed_at_utc=when)
