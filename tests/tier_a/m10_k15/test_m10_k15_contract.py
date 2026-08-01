"""M10 K15 proof for offline placement and execution evidence."""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from tests.support.m10_k15_contract_harness import (
    MUTANTS, PLACEMENT_POLICY_VERSION, PlacementCase, evaluate_reference,
    production_api, production_capital_receipt,
)


def test_reference_forms_downward_bounded_limit_placement() -> None:
    result = evaluate_reference(PlacementCase())
    assert result.quantity == Decimal("81.004")
    assert result.planned_notional == Decimal("9999.94")
    assert result.planned_notional <= PlacementCase().capital.authorised_notional
    assert result.event_types == ("order_accepted", "fill_recorded")
    assert result.portfolio_mutation_authority is False


def test_reference_rejects_nonpositive_or_ineligible_capital() -> None:
    for capital in (
        replace(PlacementCase().capital, action="block", authorised_pct=Decimal("0"), authorised_notional=Decimal("0")),
        replace(PlacementCase().capital, action="no_trade", authorised_pct=Decimal("0"), authorised_notional=Decimal("0")),
        replace(PlacementCase().capital, serial_candidate_id=None),
    ):
        with pytest.raises(ValueError): evaluate_reference(replace(PlacementCase(), capital=capital))


def test_reference_rejects_foreign_policy_shape_and_time() -> None:
    cases = (
        replace(PlacementCase(), policy_version="m10.future.v999"),
        replace(PlacementCase(), symbol="AAPL"),
        replace(PlacementCase(), side="sell"),
        replace(PlacementCase(), order_type="market"),
        replace(PlacementCase(), intent_at_utc=datetime(2026,8,1,0,59,tzinfo=UTC)),
    )
    for case in cases:
        with pytest.raises(ValueError): evaluate_reference(case)


def test_reference_rejects_sub_quantum_result() -> None:
    with pytest.raises(ValueError, match="sub_quantum"):
        evaluate_reference(replace(PlacementCase(), limit_price=Decimal("20000"), quantity_quantum=Decimal("1")))


def test_reference_identity_is_deterministic_and_binds_time() -> None:
    first = evaluate_reference(PlacementCase())
    second = evaluate_reference(PlacementCase())
    changed = evaluate_reference(replace(PlacementCase(), intent_at_utc=PlacementCase().intent_at_utc + timedelta(seconds=1)))
    assert first == second
    assert first.intent_id != changed.intent_id


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_named_mutants_are_detectable(name: str) -> None:
    case = PlacementCase()
    output = MUTANTS[name](case)
    expected = evaluate_reference(case)
    if name == "rounds_quantity_up":
        assert output * case.limit_price > case.capital.authorised_notional
    elif name == "duplicates_replay_events":
        assert output != expected.event_types
    elif name == "mutates_positions":
        assert "positions" in output
    elif name == "permits_live_port":
        assert output["adapter_mode"] == "live"
    else:
        # These mutants demonstrate a forbidden input being normalised into the lawful case.
        assert output == expected


def _valid_production():
    api = production_api()
    receipt = production_capital_receipt()
    policy = api["PlacementPolicy"](quantity_quantum=Decimal("0.001"))
    gateway = api["ExecutionGateway"]()
    intent = gateway.create_intent(receipt, policy, limit_price=Decimal("123.45"), intent_at_utc=datetime(2026,8,1,1,1,tzinfo=UTC))
    return api, receipt, policy, gateway, intent


def test_production_exports_frozen_contracts_and_protocol() -> None:
    api = production_api()
    for name in ("PlacementIntent", "ExecutionEvent", "ExecutionReceipt"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"
    assert api["ExecutionPort"]


def test_production_intent_preserves_exact_m09_lineage_and_rounds_down() -> None:
    _, receipt, _, _, intent = _valid_production()
    assert intent.capital_receipt_id == receipt.receipt_id
    assert intent.capital_receipt_fingerprint == receipt.semantic_fingerprint
    assert intent.serial_candidate_id == receipt.serial_candidate_id
    assert intent.quantity * intent.limit_price >= intent.planned_notional
    assert intent.planned_notional <= receipt.authorised_notional
    assert intent.paper_only is True
    assert intent.live_execution_allowed is False


def test_production_rejects_ineligible_receipt_and_unsupported_policy() -> None:
    api = production_api()
    receipt = production_capital_receipt()
    gateway = api["ExecutionGateway"]()
    with pytest.raises(ValueError):
        gateway.create_intent(receipt.model_copy(update={"action":"block"}), api["PlacementPolicy"](quantity_quantum=Decimal("0.001")), limit_price=Decimal("100"), intent_at_utc=datetime(2026,8,1,1,1,tzinfo=UTC))
    with pytest.raises(ValueError):
        api["PlacementPolicy"].model_validate({"policy_version":"m10.future.v999","quantity_quantum":"0.001"})


def test_production_rejects_wrong_shape_time_and_subquantum() -> None:
    api = production_api(); receipt = production_capital_receipt(); gateway = api["ExecutionGateway"]()
    for kwargs in (
        {"symbol":"AAPL"}, {"side":"sell"}, {"order_type":"market"}, {"time_in_force":"gtc"},
    ):
        policy = api["PlacementPolicy"].model_validate({"quantity_quantum":"0.001", **kwargs})
        with pytest.raises(ValueError): gateway.create_intent(receipt, policy, limit_price=Decimal("100"), intent_at_utc=datetime(2026,8,1,1,1,tzinfo=UTC))
    with pytest.raises(ValueError): gateway.create_intent(receipt, api["PlacementPolicy"](quantity_quantum=Decimal("1")), limit_price=Decimal("20000"), intent_at_utc=datetime(2026,8,1,1,1,tzinfo=UTC))
    with pytest.raises(ValueError): gateway.create_intent(receipt, api["PlacementPolicy"](quantity_quantum=Decimal("0.001")), limit_price=Decimal("100"), intent_at_utc=datetime(2026,8,1,0,59,tzinfo=UTC))


def test_production_paper_execution_emits_exact_ordered_events_and_receipt() -> None:
    api, _, _, gateway, intent = _valid_production()
    port = api["PaperExecutionPort"]()
    receipt = gateway.execute(intent, port, executed_at_utc=datetime(2026,8,1,1,2,tzinfo=UTC))
    events = port.list_events()
    assert [e.event_type for e in events] == ["order_accepted", "fill_recorded"]
    assert [e.sequence for e in events] == [1,2]
    assert receipt.order_event_id == events[0].event_id
    assert receipt.fill_event_id == events[1].event_id
    assert receipt.executed_quantity == intent.quantity
    assert receipt.executed_price == intent.limit_price
    assert receipt.executed_notional == intent.planned_notional
    assert receipt.live_execution_proven is False
    assert receipt.position_mutation_proven is False


def test_production_exact_replay_is_idempotent_without_duplicate_events() -> None:
    api, _, _, gateway, intent = _valid_production(); port = api["PaperExecutionPort"]()
    first = gateway.execute(intent, port, executed_at_utc=datetime(2026,8,1,1,2,tzinfo=UTC))
    second = gateway.execute(intent, port, executed_at_utc=datetime(2026,8,1,1,3,tzinfo=UTC))
    assert first.receipt_id == second.receipt_id
    assert len(port.list_events()) == 2
    assert len(port.list_receipts()) == 1


def test_production_forged_copies_and_conflicting_scope_fail_closed() -> None:
    api, _, _, gateway, intent = _valid_production(); port = api["PaperExecutionPort"]()
    gateway.execute(intent, port, executed_at_utc=datetime(2026,8,1,1,2,tzinfo=UTC))
    forged = intent.model_copy(update={"planned_notional": intent.planned_notional + Decimal("1")})
    with pytest.raises(ValueError): gateway.execute(forged, port, executed_at_utc=datetime(2026,8,1,1,3,tzinfo=UTC))


def test_production_port_has_no_position_or_portfolio_authority() -> None:
    api, _, _, _, _ = _valid_production(); port = api["PaperExecutionPort"]()
    assert not hasattr(port, "positions")
    assert not hasattr(port, "portfolio")
    assert not hasattr(port, "average_cost")
    assert port.durability == "non_durable_in_memory"
    assert port.adapter_mode == "paper"
