"""Canonical M10 placement formation and execution coordination."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import ROUND_FLOOR, Decimal

from nvda_desk.m09_capital_authority import CapitalDeploymentReceipt

from .contracts import PlacementIntent, PlacementPolicy, semantic_fingerprint
from .port import ExecutionPort


class ExecutionGateway:
    """Coordinate one bounded M09-to-paper-execution K15 flow."""

    def create_intent(
        self,
        capital_receipt: CapitalDeploymentReceipt,
        policy: PlacementPolicy,
        *,
        limit_price: Decimal,
        intent_at_utc: datetime,
    ) -> PlacementIntent:
        try:
            receipt = CapitalDeploymentReceipt.model_validate(
                capital_receipt.model_dump(mode="python")
            )
        except Exception as exc:
            raise ValueError("capital_deployment_receipt_contract_invalid") from exc
        try:
            policy = PlacementPolicy.model_validate(policy.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("placement_policy_contract_invalid") from exc
        limit_price = Decimal(limit_price)
        if not limit_price.is_finite() or limit_price <= 0:
            raise ValueError("limit_price_must_be_positive_finite")
        if intent_at_utc.tzinfo is None or intent_at_utc.utcoffset() != UTC.utcoffset(
            intent_at_utc
        ):
            raise ValueError("intent_time_must_be_utc")
        if intent_at_utc < receipt.emitted_at_utc:
            raise ValueError("intent_precedes_capital_receipt")
        if receipt.action not in {"continue", "reduce"}:
            raise ValueError("capital_receipt_not_placement_eligible")
        if receipt.authorised_pct <= 0 or receipt.authorised_notional <= 0:
            raise ValueError("capital_receipt_has_no_positive_authority")
        if (
            not receipt.serial_result_id
            or not receipt.serial_candidate_id
            or not receipt.serial_candidate_fingerprint
        ):
            raise ValueError("serial_candidate_authority_missing")

        raw_quantity = receipt.authorised_notional / limit_price
        quantity = (raw_quantity / policy.quantity_quantum).to_integral_value(
            rounding=ROUND_FLOOR
        ) * policy.quantity_quantum
        planned_notional = (quantity * limit_price).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
        while quantity > 0 and quantity * limit_price > receipt.authorised_notional:
            quantity -= policy.quantity_quantum
            planned_notional = (quantity * limit_price).quantize(
                Decimal("0.01"), rounding=ROUND_FLOOR
            )
        if quantity <= 0 or planned_notional <= 0:
            raise ValueError("sub_quantum_placement")

        payload = {
            "contract_version": "1.0.0",
            "capital_receipt_id": receipt.receipt_id,
            "capital_receipt_fingerprint": receipt.semantic_fingerprint,
            "capital_decision_id": receipt.decision_id,
            "capital_decision_fingerprint": receipt.decision_fingerprint,
            "final_decision_id": receipt.final_decision_id,
            "final_decision_fingerprint": receipt.final_decision_fingerprint,
            "capital_state_id": receipt.capital_state_id,
            "capital_state_fingerprint": receipt.capital_state_fingerprint,
            "modifier_receipt_id": receipt.modifier_receipt_id,
            "modifier_decision_fingerprint": receipt.modifier_decision_fingerprint,
            "m09_policy_version": receipt.policy_version,
            "m09_policy_fingerprint": receipt.capital_policy_fingerprint,
            "serial_result_id": receipt.serial_result_id,
            "serial_candidate_id": receipt.serial_candidate_id,
            "serial_candidate_fingerprint": receipt.serial_candidate_fingerprint,
            "parallel_assessment_id": receipt.parallel_assessment_id,
            "parallel_assessment_fingerprint": receipt.parallel_assessment_fingerprint,
            "capital_action": receipt.action,
            "authorised_pct": receipt.authorised_pct,
            "authorised_notional": receipt.authorised_notional,
            "capital_receipt_emitted_at_utc": receipt.emitted_at_utc,
            "placement_policy_version": policy.policy_version,
            "placement_policy_fingerprint": policy.policy_fingerprint,
            "symbol": policy.symbol,
            "side": policy.side,
            "order_type": policy.order_type,
            "time_in_force": policy.time_in_force,
            "limit_price": limit_price,
            "quantity_quantum": policy.quantity_quantum,
            "quantity": quantity,
            "planned_notional": planned_notional,
            "intent_at_utc": intent_at_utc,
            "paper_only": True,
            "live_execution_allowed": False,
            "market_price_discovery_allowed": False,
            "portfolio_mutation_authority": False,
            "lifecycle_authority": False,
            "durable_commit_proven": False,
        }
        fp = semantic_fingerprint(payload)
        return PlacementIntent.model_validate(
            {**payload, "intent_id": f"placement-intent:{fp[:24]}", "semantic_fingerprint": fp}
        )

    def execute(self, intent: PlacementIntent, port: ExecutionPort, *, executed_at_utc: datetime):
        if not isinstance(port, ExecutionPort):
            raise TypeError("port_must_implement_execution_port")
        return port.submit(intent, executed_at_utc=executed_at_utc)
