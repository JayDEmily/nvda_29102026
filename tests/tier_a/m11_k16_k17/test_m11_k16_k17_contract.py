from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from pydantic import ValidationError

from tests.support.m11_k16_k17_contract_harness import (
    lifecycle_quantity,
    production_api,
    production_execution_receipt,
    weighted_position,
)


def test_reference_weighted_average_preserves_cost_basis():
    qty, cost, avg = weighted_position(Decimal("2"), Decimal("200"), Decimal("1"), Decimal("130"))
    assert (qty, cost, avg) == (Decimal("3"), Decimal("330"), Decimal("110"))


def test_reference_rejects_invalid_fill_arithmetic():
    for args in ((Decimal("0"), Decimal("0"), Decimal("0"), Decimal("100")), (Decimal("0"), Decimal("0"), Decimal("1"), Decimal("0"))):
        with pytest.raises(ValueError): weighted_position(*args)


def test_reference_lifecycle_actions_are_closed_and_bounded():
    assert lifecycle_quantity("hold", Decimal("5"), None) == Decimal("5")
    assert lifecycle_quantity("trim", Decimal("5"), Decimal("2")) == Decimal("3")
    assert lifecycle_quantity("close", Decimal("5"), Decimal("5")) == Decimal("0")
    for action, requested in (("trim", Decimal("5")), ("trim", Decimal("0")), ("close", Decimal("4")), ("hold", Decimal("1")), ("sell", Decimal("1"))):
        with pytest.raises(ValueError): lifecycle_quantity(action, Decimal("5"), requested)


def _service_and_fill(price=Decimal("100")):
    api = production_api(); service = api["PortfolioLifecycleService"]()
    receipt = production_execution_receipt(limit_price=price)
    return api, service, receipt


def test_production_exports_frozen_contracts():
    api = production_api()
    for name in ("PositionState", "PortfolioSnapshot", "LifecycleDecision", "CloseReceipt", "FillReconciliationReceipt"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"


def test_production_reconciles_exact_m10_fill_into_canonical_position():
    _, service, receipt = _service_and_fill()
    result = service.reconcile_fill(receipt)
    position = result.snapshot.positions[0]
    assert position.symbol == "NVDA"
    assert position.quantity == receipt.executed_quantity
    assert position.average_cost == receipt.executed_price
    assert position.cost_basis == receipt.executed_notional
    assert position.fill_ids == (receipt.fill_id,)
    assert result.execution_receipt_id == receipt.receipt_id
    assert result.atomic_resulting_state_version == 1


def test_production_exact_fill_replay_is_idempotent():
    _, service, receipt = _service_and_fill()
    first = service.reconcile_fill(receipt)
    second = service.reconcile_fill(receipt)
    assert second.receipt_id == first.receipt_id
    assert second.snapshot == first.snapshot
    assert service.snapshot() == first.snapshot


def test_production_second_fill_uses_weighted_average_and_append_only_lineage():
    api, service, first_receipt = _service_and_fill(Decimal("100"))
    first = service.reconcile_fill(first_receipt)
    second_receipt = production_execution_receipt(limit_price=Decimal("130"), when=datetime(2026,8,1,2,10,tzinfo=UTC))
    second = service.reconcile_fill(second_receipt)
    p = second.snapshot.positions[0]
    expected_cost = first_receipt.executed_notional + second_receipt.executed_notional
    expected_qty = first_receipt.executed_quantity + second_receipt.executed_quantity
    assert p.quantity == expected_qty
    assert p.cost_basis == expected_cost
    assert p.average_cost == expected_cost / expected_qty
    assert p.fill_ids == (first_receipt.fill_id, second_receipt.fill_id)
    assert second.atomic_resulting_state_version == first.atomic_resulting_state_version + 1


def test_production_rejects_forged_or_nonfilled_execution_receipt():
    _, service, receipt = _service_and_fill()
    forged = receipt.model_copy(update={"executed_quantity": receipt.executed_quantity + Decimal("1")})
    with pytest.raises(ValueError): service.reconcile_fill(forged)
    with pytest.raises(ValueError): service.reconcile_fill(receipt.model_copy(update={"status":"accepted"}))


def test_production_decision_binds_exact_snapshot_and_position():
    _, service, receipt = _service_and_fill(); result = service.reconcile_fill(receipt)
    decision = service.decide_lifecycle(snapshot=result.snapshot, position_id=result.snapshot.position_ids[0], action="trim", quantity=result.snapshot.positions[0].quantity / 2, reasons=("risk_reduction",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))
    assert decision.snapshot_fingerprint == result.snapshot.semantic_fingerprint
    assert decision.position_fingerprint == result.snapshot.positions[0].semantic_fingerprint
    assert decision.action == "trim"


def test_production_rejects_invalid_hold_trim_close_shapes():
    _, service, receipt = _service_and_fill(); snapshot = service.reconcile_fill(receipt).snapshot; pid=snapshot.position_ids[0]; qty=snapshot.positions[0].quantity
    cases=(("hold",Decimal("1")),("trim",qty),("trim",Decimal("0")),("close",qty-Decimal("0.001")))
    for action, amount in cases:
        with pytest.raises(ValueError): service.decide_lifecycle(snapshot=snapshot, position_id=pid, action=action, quantity=amount, reasons=("x",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))


def test_production_trim_is_atomic_and_preserves_average_cost():
    _, service, receipt = _service_and_fill(); before=service.reconcile_fill(receipt).snapshot; p=before.positions[0]
    decision=service.decide_lifecycle(snapshot=before, position_id=p.position_id, action="trim", quantity=p.quantity/2, reasons=("de_risk",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))
    closed=service.apply_lifecycle(decision)
    after=closed.snapshot.positions[0]
    assert after.quantity == p.quantity/2
    assert after.average_cost == p.average_cost
    assert after.cost_basis == p.cost_basis/2
    assert closed.atomic_resulting_state_version == closed.atomic_prior_state_version + 1


def test_production_close_removes_position_and_replay_does_not_mutate_twice():
    _, service, receipt = _service_and_fill(); before=service.reconcile_fill(receipt).snapshot; p=before.positions[0]
    decision=service.decide_lifecycle(snapshot=before, position_id=p.position_id, action="close", quantity=p.quantity, reasons=("exit",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))
    first=service.apply_lifecycle(decision); second=service.apply_lifecycle(decision)
    assert first.snapshot.positions == ()
    assert second.receipt_id == first.receipt_id
    assert service.snapshot().positions == ()


def test_production_rejects_stale_decision_after_intervening_fill():
    _, service, receipt = _service_and_fill(); before=service.reconcile_fill(receipt).snapshot; p=before.positions[0]
    decision=service.decide_lifecycle(snapshot=before, position_id=p.position_id, action="close", quantity=p.quantity, reasons=("exit",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))
    service.reconcile_fill(production_execution_receipt(limit_price=Decimal("110"), when=datetime(2026,8,1,2,30,tzinfo=UTC)))
    with pytest.raises(ValueError): service.apply_lifecycle(decision)


def test_production_hold_is_evidence_only_and_cannot_mutate():
    _, service, receipt = _service_and_fill(); snap=service.reconcile_fill(receipt).snapshot; p=snap.positions[0]
    decision=service.decide_lifecycle(snapshot=snap, position_id=p.position_id, action="hold", quantity=None, reasons=("carry",), decided_at_utc=datetime(2026,8,1,2,20,tzinfo=UTC))
    with pytest.raises(ValueError): service.apply_lifecycle(decision)
    assert service.snapshot() == snap


def test_production_rejects_non_utc_and_future_policy():
    api, service, receipt = _service_and_fill(); snap=service.reconcile_fill(receipt).snapshot; p=snap.positions[0]
    with pytest.raises(ValueError): service.decide_lifecycle(snapshot=snap, position_id=p.position_id, action="hold", quantity=None, reasons=("x",), decided_at_utc=datetime(2026,8,1,2,20))
    with pytest.raises(ValidationError): api["LifecycleDecision"].model_validate({"policy_version":"m11.future.v2"})
