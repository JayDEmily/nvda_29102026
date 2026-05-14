"""Tier A behavioural proof for capital and downstream opening seams."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.capital.authority import evaluate_capital_deployment
from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityInput,
    CapitalDeploymentDecision,
    CapitalDeploymentReceipt,
)
from nvda_desk.contracts.downstream import (
    DownstreamOpeningSnapshot,
    DownstreamRecommendationHistoryReservation,
    OpeningAuthorisationResult,
)


def _input(**overrides: object) -> CapitalDeploymentAuthorityInput:
    payload = {
        "final_risk_action": "proceed",
        "final_risk_receipt_id": "final-risk-receipt-001",
        "serial_candidate_id": "candidate-001",
        "serial_candidate_eligible": True,
        "serial_confidence": 0.72,
        "downstream_pre_deployment_allowed": True,
        "downstream_pre_deployment_receipt_id": "pre-deployment-allow-001",
        "parallel_risk_packet_id": "parallel-risk-packet-001",
        "parallel_risk_envelope_state": "broad",
        "capital_state_snapshot_id": "capital-snapshot-001",
        "available_capital_usd": 250_000.0,
        "bounded_policy_id": "bounded-policy-001",
        "requested_deployable_pct": 40.0,
        "max_deployable_pct": 12.5,
        "inventory_pct": 75.0,
    }
    payload.update(overrides)
    return CapitalDeploymentAuthorityInput(**payload)


def test_capital_contract_models_enforce_explicit_capital_state_and_policy_bounds() -> None:
    """Capital authority input requires bounded capital state and deployment policy."""
    input_model = _input()
    decision = CapitalDeploymentDecision(
        action=CapitalDeploymentAuthorityAction.REDUCE,
        authorised_deployable_pct=12.5,
        authorised_notional_usd=31_250.0,
        consumed_inputs=[
            "serial_candidate",
            "downstream_pre_deployment_result",
            "parallel_risk_envelope",
            "final_risk_product",
            "capital_state",
            "bounded_deployment_policy",
            "coefficient_modifier_authority",
            "temporal_context",
        ],
        rationale=["bounded capital authority"],
    )
    assert input_model.capital_state_snapshot_id == "capital-snapshot-001"
    assert input_model.available_capital_usd == 250_000.0
    assert input_model.requested_deployable_pct == 40.0
    assert input_model.max_deployable_pct == 12.5
    assert input_model.inventory_pct == 75.0
    assert decision.action is CapitalDeploymentAuthorityAction.REDUCE
    assert decision.authorised_deployable_pct == 12.5
    assert decision.authorised_notional_usd == 31_250.0
    with pytest.raises(ValidationError):
        _input(available_capital_usd=-1.0)
    with pytest.raises(ValidationError):
        _input(requested_deployable_pct=101.0, max_deployable_pct=10.0)
    with pytest.raises(ValidationError):
        CapitalDeploymentDecision(
            action=CapitalDeploymentAuthorityAction.CONTINUE,
            authorised_deployable_pct=10.0,
            authorised_notional_usd=-1.0,
        )


def test_capital_input_requires_traceable_preconditions() -> None:
    """Fresh-capital authority may not evaluate anonymous preconditions."""
    with pytest.raises(ValidationError):
        _input(serial_candidate_id="unknown")
    with pytest.raises(ValidationError):
        _input(downstream_pre_deployment_receipt_id="")
    with pytest.raises(ValidationError):
        _input(final_risk_receipt_id="unknown")
    with pytest.raises(ValidationError):
        _input(capital_state_snapshot_id="")
    with pytest.raises(ValidationError):
        _input(bounded_policy_id="unknown")


def test_capital_authority_sizes_from_explicit_capital_state_not_constant_notional() -> None:
    """Capital authority sizes from supplied capital state and bounded policy."""
    first = evaluate_capital_deployment(
        _input(
            capital_state_snapshot_id="capital-snapshot-large",
            available_capital_usd=250_000.0,
            requested_deployable_pct=12.0,
            max_deployable_pct=12.0,
        )
    )
    second = evaluate_capital_deployment(
        _input(
            capital_state_snapshot_id="capital-snapshot-small",
            available_capital_usd=40_000.0,
            requested_deployable_pct=12.0,
            max_deployable_pct=12.0,
        )
    )
    assert first.action is CapitalDeploymentAuthorityAction.CONTINUE
    assert first.authorised_deployable_pct == 12.0
    assert first.authorised_notional_usd == 30_000.0
    assert second.action is CapitalDeploymentAuthorityAction.CONTINUE
    assert second.authorised_deployable_pct == 12.0
    assert second.authorised_notional_usd == 4_800.0
    assert first.authorised_notional_usd != second.authorised_notional_usd


def test_capital_authority_blocks_when_final_risk_does_not_proceed() -> None:
    """Final risk non-proceed action blocks deployment regardless of capital state."""
    decision = evaluate_capital_deployment(
        _input(final_risk_action="block", requested_deployable_pct=50.0, max_deployable_pct=12.0)
    )
    assert decision.action is CapitalDeploymentAuthorityAction.BLOCK
    assert decision.authorised_deployable_pct == 0.0
    assert decision.authorised_notional_usd == 0.0
    assert "parallel_or_final_risk_block_dominates" in decision.rationale


def test_capital_authority_blocks_when_pre_deployment_disallows_candidate() -> None:
    """Downstream pre-deployment allow/block truth dominates fresh-capital sizing."""
    decision = evaluate_capital_deployment(_input(downstream_pre_deployment_allowed=False))
    assert decision.action is CapitalDeploymentAuthorityAction.BLOCK
    assert decision.authorised_deployable_pct == 0.0
    assert decision.authorised_notional_usd == 0.0
    assert decision.rationale == ["downstream_pre_deployment_blocked_candidate"]


def test_capital_decision_carries_input_trace_without_opening_placement() -> None:
    """Capital decision receipt identifies inputs and does not carry placement authority."""
    context = _input()
    decision = evaluate_capital_deployment(context, receipt_id="capital-receipt-001")
    receipt = CapitalDeploymentReceipt(
        receipt_id="capital-receipt-001",
        decision=decision,
        input_trace=decision.input_trace,
        emitted_output=decision.model_dump(mode="json"),
    )
    assert decision.capital_deployment_receipt_id == "capital-receipt-001"
    assert decision.input_trace is not None
    assert decision.input_trace.serial_candidate_id == "candidate-001"
    assert decision.input_trace.downstream_pre_deployment_receipt_id == "pre-deployment-allow-001"
    assert decision.input_trace.final_risk_receipt_id == "final-risk-receipt-001"
    assert decision.input_trace.capital_state_snapshot_id == "capital-snapshot-001"
    assert decision.input_trace.bounded_policy_id == "bounded-policy-001"
    assert receipt.placement_authority_opened is False


def test_downstream_opening_authorisation_shell_round_trips_without_capital_sizing() -> None:
    """Downstream opening carries authorisation shape without owning notional sizing."""
    reservation = DownstreamRecommendationHistoryReservation(
        reservation_id="reservation-001",
        source_candidate_id="candidate-001",
        reserved_entry_count=2,
    )
    authorisation = OpeningAuthorisationResult(
        recommendation_history_reservation=reservation,
        authorised_deployable_pct=40.0,
        immediate_opening_slice_pct=10.0,
        serial_ladder_shape_sum=30.0,
    )
    snapshot = DownstreamOpeningSnapshot(
        opening_ids=["opening-001"], opening_authorisation=authorisation
    )
    dumped = snapshot.model_dump()
    assert (
        dumped["opening_authorisation"]["recommendation_history_reservation"]["reservation_id"]
        == "reservation-001"
    )
    assert dumped["opening_authorisation"]["authorised_deployable_pct"] == 40.0
    assert "authorised_notional_usd" not in dumped["opening_authorisation"]


def test_capital_contract_rejects_downstream_opening_shell_fields() -> None:
    """Capital contracts must not absorb downstream opening-authorisation ownership."""
    with pytest.raises(ValidationError):
        CapitalDeploymentDecision(
            action=CapitalDeploymentAuthorityAction.CONTINUE,
            authorised_deployable_pct=10.0,
            authorised_notional_usd=1000.0,
            opening_authorisation={"authorised_deployable_pct": 40.0},
        )


def test_capital_authority_input_rejects_hidden_broker_or_placement_fields() -> None:
    with pytest.raises(ValidationError):
        _input(broker_order_id="hidden-broker-authority")

    with pytest.raises(ValidationError):
        _input(placement_authority_opened=True)


def test_capital_optional_parallel_risk_trace_token_is_normalised() -> None:
    input_model = _input(parallel_risk_packet_id=" parallel-risk-packet-001 ")

    assert input_model.parallel_risk_packet_id == "parallel-risk-packet-001"


def test_capital_deployment_receipt_builder_keeps_placement_authority_closed() -> None:
    context = _input()
    decision = evaluate_capital_deployment(context, receipt_id="capital-receipt-builder-001")
    receipt = CapitalDeploymentReceipt(
        receipt_id="capital-receipt-builder-001",
        decision=decision,
        input_trace=decision.input_trace,
        emitted_output={
            "action": decision.action.value,
            "authorised_deployable_pct": decision.authorised_deployable_pct,
            "authorised_notional_usd": decision.authorised_notional_usd,
            "rationale": list(decision.rationale),
        },
    )

    assert receipt.placement_authority_opened is False


def test_capital_deployment_receipt_rejects_hidden_broker_execution_fields() -> None:
    context = _input()
    decision = evaluate_capital_deployment(context, receipt_id="capital-receipt-extra-001")

    with pytest.raises(ValidationError):
        CapitalDeploymentReceipt(
            receipt_id="capital-receipt-extra-001",
            decision=decision,
            input_trace=decision.input_trace,
            emitted_output={"action": decision.action.value},
            broker_order_id="hidden-broker-authority",
        )


def test_capital_deployment_receipt_rejects_opening_authorisation_payload_in_emitted_output() -> (
    None
):
    context = _input()
    decision = evaluate_capital_deployment(
        context, receipt_id="capital-receipt-opening-smuggle-001"
    )

    with pytest.raises(ValidationError, match="opening or broker authority"):
        CapitalDeploymentReceipt(
            receipt_id="capital-receipt-opening-smuggle-001",
            decision=decision,
            input_trace=decision.input_trace,
            emitted_output={
                "action": decision.action.value,
                "opening_authorisation": {
                    "order_intent_preview": {"broker_order_id": "hidden-broker"}
                },
            },
        )
