"""Sequence 9 Tier A tests for downstream capital authority decisions."""

from __future__ import annotations

from nvda_desk.capital.authority import evaluate_capital_deployment
from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityInput,
)


def _input(**overrides: object) -> CapitalDeploymentAuthorityInput:
    payload = {
        "final_risk_action": "proceed",
        "final_risk_receipt_id": "final-risk-seq9",
        "serial_candidate_id": "serial-candidate-seq9",
        "serial_candidate_eligible": True,
        "serial_confidence": 0.91,
        "downstream_pre_deployment_allowed": True,
        "downstream_pre_deployment_receipt_id": "pre-deployment-seq9",
        "parallel_risk_packet_id": "parallel-risk-envelope-seq9",
        "parallel_risk_envelope_state": "broad",
        "parallel_risk_hard_blocks": [],
        "parallel_risk_caution_flags": [],
        "coefficient_min_deployable_floor_pct": 2.0,
        "temporal_event_window_active": False,
        "temporal_event_risk": "normal",
        "capital_state_snapshot_id": "capital-state-seq9",
        "available_capital_usd": 100_000.0,
        "bounded_policy_id": "bounded-policy-seq9",
        "requested_deployable_pct": 10.0,
        "max_deployable_pct": 10.0,
        "inventory_pct": 0.0,
    }
    payload.update(overrides)
    return CapitalDeploymentAuthorityInput(**payload)


def test_sequence9_downstream_pre_deployment_block_dominates() -> None:
    """Downstream pre-deployment block dominates before sizing is considered."""
    decision = evaluate_capital_deployment(_input(downstream_pre_deployment_allowed=False))
    assert decision.action is CapitalDeploymentAuthorityAction.BLOCK
    assert decision.authorised_deployable_pct == 0.0
    assert decision.authorised_notional_usd == 0.0
    assert decision.rationale == ["downstream_pre_deployment_blocked_candidate"]


def test_sequence9_parallel_risk_block_dominates_serial_candidate() -> None:
    """Parallel risk hard block dominates even when serial candidate is eligible."""
    decision = evaluate_capital_deployment(
        _input(parallel_risk_envelope_state="block", parallel_risk_hard_blocks=["vvix_extreme"])
    )
    assert decision.action is CapitalDeploymentAuthorityAction.BLOCK
    assert decision.authorised_deployable_pct == 0.0
    assert decision.authorised_notional_usd == 0.0


def test_sequence9_serial_ineligible_produces_no_trade() -> None:
    """Serial candidate ineligibility produces a no-trade downstream decision."""
    decision = evaluate_capital_deployment(_input(serial_candidate_eligible=False))
    assert decision.action is CapitalDeploymentAuthorityAction.NO_TRADE
    assert decision.rationale == ["serial_candidate_not_eligible"]


def test_sequence9_risk_cap_reduces_requested_deployment() -> None:
    """Parallel risk envelope cap reduces, rather than bypassing, deployment authority."""
    decision = evaluate_capital_deployment(
        _input(requested_deployable_pct=20.0, max_deployable_pct=8.0)
    )
    assert decision.action is CapitalDeploymentAuthorityAction.REDUCE
    assert decision.authorised_deployable_pct == 8.0
    assert decision.authorised_notional_usd == 8_000.0


def test_sequence9_temporal_elevated_event_window_reduces() -> None:
    """Temporal elevated event risk reduces otherwise clean capital deployment."""
    decision = evaluate_capital_deployment(
        _input(temporal_event_window_active=True, temporal_event_risk="elevated")
    )
    assert decision.action is CapitalDeploymentAuthorityAction.REDUCE
    assert decision.authorised_deployable_pct == 10.0


def test_sequence9_clean_context_continues() -> None:
    """Clean serial, parallel, coefficient, and temporal inputs allow continuation."""
    decision = evaluate_capital_deployment(_input())
    assert decision.action is CapitalDeploymentAuthorityAction.CONTINUE
    assert decision.consumed_inputs == [
        "serial_candidate",
        "downstream_pre_deployment_result",
        "parallel_risk_envelope",
        "final_risk_product",
        "capital_state",
        "bounded_deployment_policy",
        "coefficient_modifier_authority",
        "temporal_context",
    ]
    assert decision.input_trace is not None
    assert decision.input_trace.final_risk_receipt_id == "final-risk-seq9"


def test_sequence9_coefficient_floor_reduces_reachable_requested_deployment() -> None:
    """Coefficient floor reduction is reachable when requested pct is below the floor."""
    decision = evaluate_capital_deployment(
        _input(
            coefficient_min_deployable_floor_pct=2.0,
            requested_deployable_pct=1.0,
            max_deployable_pct=10.0,
        )
    )
    assert decision.action is CapitalDeploymentAuthorityAction.REDUCE
    assert decision.authorised_deployable_pct == 1.0
    assert decision.authorised_notional_usd == 1_000.0
    assert decision.rationale == ["coefficient_floor_not_satisfied"]


def test_sequence9_serial_confidence_is_not_position_size() -> None:
    """Serial confidence is auditable metadata and must not affect sizing."""
    low_confidence = evaluate_capital_deployment(_input(serial_confidence=0.12))
    high_confidence = evaluate_capital_deployment(_input(serial_confidence=0.98))
    assert low_confidence.action is CapitalDeploymentAuthorityAction.CONTINUE
    assert high_confidence.action is CapitalDeploymentAuthorityAction.CONTINUE
    assert low_confidence.authorised_deployable_pct == high_confidence.authorised_deployable_pct
    assert low_confidence.authorised_notional_usd == high_confidence.authorised_notional_usd
