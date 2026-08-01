"""Independent reference and production fixture harness for M10 K15."""
from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from hashlib import sha256
from typing import Any, Callable

PLACEMENT_POLICY_VERSION = "m10.paper-placement.v1"
PORT_VERSION = "m10.paper-port.v1"


def canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        return "0" if value == 0 else format(value.normalize(), "f")
    if hasattr(value, "model_dump"):
        return canonical(value.model_dump(mode="python"))
    if hasattr(value, "__dataclass_fields__"):
        return canonical({name: getattr(value, name) for name in value.__dataclass_fields__})
    if isinstance(value, dict):
        return {str(k): canonical(v) for k, v in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [canonical(v) for v in value]
    return value


def fingerprint(value: Any) -> str:
    return sha256(json.dumps(canonical(value), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class CapitalReceiptCase:
    receipt_id: str = "m09.receipt.001"
    receipt_fingerprint: str = "a" * 64
    decision_id: str = "m09.decision.001"
    decision_fingerprint: str = "b" * 64
    final_decision_id: str = "m09.final.001"
    final_decision_fingerprint: str = "c" * 64
    capital_state_id: str = "capital.state.001"
    capital_state_fingerprint: str = "d" * 64
    policy_version: str = "m09.capital-policy.v1"
    capital_policy_fingerprint: str = "e" * 64
    modifier_receipt_id: str = "m07.receipt.001"
    modifier_decision_fingerprint: str = "f" * 64
    serial_result_id: str | None = "m05.result.001"
    serial_candidate_id: str | None = "m05.candidate.001"
    serial_candidate_fingerprint: str | None = "1" * 64
    parallel_assessment_id: str | None = "m06.assessment.001"
    parallel_assessment_fingerprint: str | None = "2" * 64
    action: str = "continue"
    authorised_pct: Decimal = Decimal("10")
    authorised_notional: Decimal = Decimal("10000")
    emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)


@dataclass(frozen=True)
class PlacementCase:
    capital: CapitalReceiptCase = CapitalReceiptCase()
    policy_version: str = PLACEMENT_POLICY_VERSION
    symbol: str = "NVDA"
    side: str = "buy"
    order_type: str = "limit"
    time_in_force: str = "day"
    limit_price: Decimal = Decimal("123.45")
    quantity_quantum: Decimal = Decimal("0.001")
    intent_at_utc: datetime = datetime(2026, 8, 1, 1, 1, tzinfo=UTC)


@dataclass(frozen=True)
class ReferenceResult:
    quantity: Decimal
    planned_notional: Decimal
    intent_id: str
    order_event_id: str
    fill_event_id: str
    receipt_id: str
    event_types: tuple[str, ...] = ("order_accepted", "fill_recorded")
    paper_only: bool = True
    portfolio_mutation_authority: bool = False


def evaluate_reference(case: PlacementCase) -> ReferenceResult:
    c = case.capital
    if c.action not in {"continue", "reduce"}:
        raise ValueError("capital_receipt_not_placement_eligible")
    if c.authorised_pct <= 0 or c.authorised_notional <= 0:
        raise ValueError("capital_receipt_has_no_positive_authority")
    if not c.serial_result_id or not c.serial_candidate_id or not c.serial_candidate_fingerprint:
        raise ValueError("serial_candidate_authority_missing")
    if case.policy_version != PLACEMENT_POLICY_VERSION:
        raise ValueError("unsupported_placement_policy")
    if (case.symbol, case.side, case.order_type, case.time_in_force) != ("NVDA", "buy", "limit", "day"):
        raise ValueError("unsupported_placement_shape")
    if case.limit_price <= 0 or case.quantity_quantum <= 0:
        raise ValueError("invalid_numeric_domain")
    if case.intent_at_utc.tzinfo is None or case.intent_at_utc.utcoffset() != UTC.utcoffset(case.intent_at_utc):
        raise ValueError("intent_time_must_be_utc")
    if case.intent_at_utc < c.emitted_at_utc:
        raise ValueError("intent_precedes_capital_receipt")
    raw = c.authorised_notional / case.limit_price
    quantity = (raw / case.quantity_quantum).to_integral_value(rounding=ROUND_FLOOR) * case.quantity_quantum
    notional = (quantity * case.limit_price).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
    while quantity > 0 and notional > c.authorised_notional:
        quantity -= case.quantity_quantum
        notional = (quantity * case.limit_price).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
    if quantity <= 0 or notional <= 0:
        raise ValueError("sub_quantum_placement")
    material = {"capital": c, "policy": case.policy_version, "symbol": case.symbol, "side": case.side,
                "order_type": case.order_type, "time_in_force": case.time_in_force,
                "limit_price": case.limit_price, "quantity_quantum": case.quantity_quantum,
                "quantity": quantity, "planned_notional": notional, "intent_at_utc": case.intent_at_utc}
    intent_fp = fingerprint(material)
    intent_id = f"placement-intent:{intent_fp[:24]}"
    order_event_id = f"execution-event:{fingerprint({'intent': intent_id, 'sequence': 1, 'type': 'order_accepted'})[:24]}"
    fill_event_id = f"execution-event:{fingerprint({'intent': intent_id, 'sequence': 2, 'type': 'fill_recorded'})[:24]}"
    receipt_id = f"execution-receipt:{fingerprint({'intent': intent_id, 'events': (order_event_id, fill_event_id), 'port': PORT_VERSION})[:24]}"
    return ReferenceResult(quantity, notional, intent_id, order_event_id, fill_event_id, receipt_id)


def _mutant_accepts_block(case: PlacementCase):
    return evaluate_reference(replace(case, capital=replace(case.capital, action="continue")))

def _mutant_rounds_up(case: PlacementCase):
    raw = case.capital.authorised_notional / case.limit_price
    q = (raw / case.quantity_quantum).to_integral_value(rounding=ROUND_CEILING) * case.quantity_quantum
    return q

def _mutant_accepts_future_policy(case: PlacementCase):
    return evaluate_reference(replace(case, policy_version=PLACEMENT_POLICY_VERSION))

def _mutant_market_order(case: PlacementCase):
    return evaluate_reference(replace(case, order_type="limit"))

def _mutant_live_port(case: PlacementCase):
    return {"adapter_mode": "live", "result": evaluate_reference(case)}

def _mutant_duplicate_replay(case: PlacementCase):
    result = evaluate_reference(case)
    return (result.event_types + result.event_types)

def _mutant_position_mutation(case: PlacementCase):
    return {"result": evaluate_reference(case), "positions": {"NVDA": "81"}}

MUTANTS: dict[str, Callable[[PlacementCase], Any]] = {
    "accepts_blocked_capital": _mutant_accepts_block,
    "rounds_quantity_up": _mutant_rounds_up,
    "accepts_future_policy": _mutant_accepts_future_policy,
    "permits_market_order": _mutant_market_order,
    "permits_live_port": _mutant_live_port,
    "duplicates_replay_events": _mutant_duplicate_replay,
    "mutates_positions": _mutant_position_mutation,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m10_execution_gateway")
    required = ("PlacementIntent", "PlacementPolicy", "ExecutionPort", "ExecutionEvent", "ExecutionReceipt", "ExecutionGateway", "PaperExecutionPort")
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M10 package missing exports: {missing}")
    return {name: getattr(module, name) for name in required}


def production_capital_receipt():
    from nvda_desk.m09_capital_authority import CapitalDeploymentPolicy, CapitalState, FinalRiskJoinPolicy
    from tests.support.m09_k11_k14_contract_harness import (
        production_api as m09_api,
        production_canonical_packet_pair,
        production_modifier_receipt,
        production_parallel_assessment,
        production_serial_candidate,
    )
    api = m09_api()
    parallel = production_parallel_assessment()
    serial = production_serial_candidate(prepared_id=parallel.prepared_id, prepared_fingerprint=parallel.prepared_fingerprint)
    modifier = production_modifier_receipt()
    join_policy = FinalRiskJoinPolicy()
    capital_policy = CapitalDeploymentPolicy(target_pct=Decimal("10"), hard_max_pct=Decimal("15"), caution_multiplier=Decimal("0.5"), rounding_quantum=Decimal("0.01"))
    capital = CapitalState.create(state_id="capital.state.m10", account_id="paper.account.001", state_version=1,
        effective_at_utc=datetime(2026,8,1,0,0,tzinfo=UTC), available_capital=Decimal("100000"), reserved_capital=Decimal("0"),
        max_fresh_deployable_pct=Decimal("12"), source_authority_ref="capital.snapshot.authority.v1")
    service = api["CapitalAuthorityService"]()
    serial_packet, parallel_packet, _ = production_canonical_packet_pair(serial=serial, parallel=parallel)
    final = service.join_final_risk(serial_packet, parallel_packet, join_policy)
    decision = service.evaluate_capital(final, capital, modifier, capital_policy)
    return service.build_receipt(decision, final, capital, modifier, capital_policy, emitted_at_utc=datetime(2026,8,1,1,0,tzinfo=UTC))
