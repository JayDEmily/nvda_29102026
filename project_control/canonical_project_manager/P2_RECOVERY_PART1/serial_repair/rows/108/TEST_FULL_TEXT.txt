from __future__ import annotations

import pytest

from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentDecision,
)
from nvda_desk.downstream.opening import DownstreamOpeningService


def _decision(
    *,
    action: CapitalDeploymentAuthorityAction = CapitalDeploymentAuthorityAction.CONTINUE,
    pct: float = 12.5,
    notional: float = 12500.0,
) -> CapitalDeploymentDecision:
    return CapitalDeploymentDecision(
        action=action,
        authorised_deployable_pct=pct,
        authorised_notional_usd=notional,
        consumed_inputs=["capital_state", "parallel_risk_envelope"],
        rationale=["test"],
        capital_deployment_receipt_id="cap-receipt-001",
    )


def test_opening_readiness_consumes_capital_decision_without_broker_execution() -> None:
    service = DownstreamOpeningService()

    result = service.evaluate_placement_readiness(
        decision=_decision(),
        serial_candidate_id="serial-candidate-001",
        placement_constraint_ids=["limit-only", "day-session"],
        readiness_id="ready-001",
    )

    assert result.readiness_state == "ready_for_protocol_handoff"
    assert result.input_trace.capital_deployment_receipt_id == "cap-receipt-001"
    assert result.input_trace.serial_candidate_id == "serial-candidate-001"
    assert result.input_trace.broker_boundary_mode == "protocol_only"
    assert result.broker_execution_opened is False
    assert result.capital_sizing_recomputed is False
    assert result.placement_handoff is not None
    assert result.placement_handoff.broker_protocol_only is True
    assert result.placement_handoff.execution_allowed is False
    assert result.placement_handoff.order_intent_preview["authorised_deployable_pct"] == 12.5


def test_opening_readiness_blocks_non_continue_capital_decisions() -> None:
    service = DownstreamOpeningService()

    result = service.evaluate_placement_readiness(
        decision=_decision(action=CapitalDeploymentAuthorityAction.BLOCK, pct=0.0, notional=0.0),
        serial_candidate_id="serial-candidate-002",
        readiness_id="blocked-001",
    )

    assert result.readiness_state == "blocked"
    assert result.placement_handoff is None
    assert "capital_deployment_action_block" in result.blocked_reasons
    assert "no_authorised_deployable_percentage" in result.blocked_reasons


def test_opening_readiness_rejects_concrete_broker_boundary() -> None:
    service = DownstreamOpeningService()

    with pytest.raises(ValueError, match="protocol_only"):
        service.evaluate_placement_readiness(
            decision=_decision(),
            serial_candidate_id="serial-candidate-003",
            broker_boundary_mode="live_broker_adapter",
        )


def test_opening_readiness_requires_capital_deployment_receipt_id() -> None:
    service = DownstreamOpeningService()

    with pytest.raises(ValueError) as exc_info:
        service.evaluate_placement_readiness(
            decision=_decision().model_copy(update={"capital_deployment_receipt_id": None}),
            serial_candidate_id="serial-candidate-004",
        )
    assert str(exc_info.value) == "placement readiness requires capital_deployment_receipt_id"


def test_opening_readiness_rejects_blank_serial_candidate_id() -> None:
    service = DownstreamOpeningService()

    with pytest.raises(ValueError) as exc_info:
        service.evaluate_placement_readiness(
            decision=_decision(),
            serial_candidate_id="   ",
        )
    assert str(exc_info.value) == "placement readiness requires serial_candidate_id"


def test_opening_readiness_blocks_continue_decision_with_zero_notional() -> None:
    service = DownstreamOpeningService()

    result = service.evaluate_placement_readiness(
        decision=_decision(
            action=CapitalDeploymentAuthorityAction.CONTINUE, pct=12.5, notional=0.0
        ),
        serial_candidate_id="serial-candidate-005",
        readiness_id="zero-notional-001",
    )

    assert result.readiness_state == "blocked"
    assert result.placement_handoff is None
    assert result.broker_execution_opened is False
    assert result.capital_sizing_recomputed is False
    assert result.blocked_reasons == ["no_authorised_notional"]


def test_opening_readiness_detaches_placement_constraints_from_caller_list() -> None:
    service = DownstreamOpeningService()
    constraints = ["limit-only", "day-session"]

    result = service.evaluate_placement_readiness(
        decision=_decision(),
        serial_candidate_id="serial-candidate-006",
        placement_constraint_ids=constraints,
        readiness_id="copy-boundary-001",
    )
    constraints.append("mutated-after-call")

    assert result.input_trace.placement_constraint_ids == ["limit-only", "day-session"]
    assert result.placement_handoff is not None
    assert result.placement_handoff.order_intent_preview["placement_constraint_ids"] == [
        "limit-only",
        "day-session",
    ]


def test_opening_readiness_protocol_handoff_rejects_broker_execution_fields() -> None:
    from pydantic import ValidationError

    from nvda_desk.contracts.downstream import PlacementHandoffMaterial

    with pytest.raises(ValidationError):
        PlacementHandoffMaterial(
            handoff_id="handoff-001",
            order_intent_preview={"serial_candidate_id": "serial-candidate-007"},
            broker_order_id="broker-order-should-not-enter-readiness",
        )


def test_opening_readiness_protocol_handoff_rejects_nested_broker_execution_preview() -> None:
    from pydantic import ValidationError

    from nvda_desk.contracts.downstream import PlacementHandoffMaterial

    with pytest.raises(ValidationError, match="broker execution"):
        PlacementHandoffMaterial(
            handoff_id="handoff-nested-broker-001",
            order_intent_preview={
                "serial_candidate_id": "serial-candidate-008",
                "broker_preview": {"broker_order_id": "hidden-broker-order"},
            },
        )
