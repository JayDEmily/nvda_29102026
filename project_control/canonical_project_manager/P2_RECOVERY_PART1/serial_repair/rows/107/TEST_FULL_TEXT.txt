from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentDecision,
)
from nvda_desk.contracts.downstream import (
    PlacementHandoffMaterial,
    PlacementReadinessInputTrace,
    PlacementReadinessResult,
)
from nvda_desk.downstream.opening import DownstreamOpeningService


def _trace() -> PlacementReadinessInputTrace:
    return PlacementReadinessInputTrace(
        capital_deployment_receipt_id="capital-receipt-row041",
        serial_candidate_id="serial-candidate-row041",
        placement_constraint_ids=["limit-only"],
    )


def _decision() -> CapitalDeploymentDecision:
    return CapitalDeploymentDecision(
        action=CapitalDeploymentAuthorityAction.CONTINUE,
        authorised_deployable_pct=10.0,
        authorised_notional_usd=10_000.0,
        consumed_inputs=["capital_state", "bounded_deployment_policy"],
        rationale=["row041"],
        capital_deployment_receipt_id="capital-receipt-row041",
    )


def test_placement_trace_contract_rejects_non_protocol_broker_boundary_mode() -> None:
    with pytest.raises(ValidationError, match="protocol_only"):
        PlacementReadinessInputTrace(
            capital_deployment_receipt_id="capital-receipt-row041",
            serial_candidate_id="serial-candidate-row041",
            broker_boundary_mode="live_broker_adapter",
        )


def test_placement_handoff_contract_cannot_enable_execution() -> None:
    with pytest.raises(ValidationError, match="execution_allowed"):
        PlacementHandoffMaterial(
            handoff_id="handoff-execution-row041",
            order_intent_preview={"serial_candidate_id": "serial-candidate-row041"},
            execution_allowed=True,
        )


def test_placement_handoff_contract_must_remain_protocol_only() -> None:
    with pytest.raises(ValidationError, match="broker_protocol_only"):
        PlacementHandoffMaterial(
            handoff_id="handoff-protocol-row041",
            order_intent_preview={"serial_candidate_id": "serial-candidate-row041"},
            broker_protocol_only=False,
        )


def test_placement_readiness_result_cannot_claim_broker_execution_or_resizing() -> None:
    handoff = PlacementHandoffMaterial(
        handoff_id="handoff-result-row041",
        order_intent_preview={"serial_candidate_id": "serial-candidate-row041"},
    )

    with pytest.raises(ValidationError, match="broker_execution_opened"):
        PlacementReadinessResult(
            readiness_id="result-broker-opened-row041",
            readiness_state="ready_for_protocol_handoff",
            input_trace=_trace(),
            placement_handoff=handoff,
            broker_execution_opened=True,
        )

    with pytest.raises(ValidationError, match="capital_sizing_recomputed"):
        PlacementReadinessResult(
            readiness_id="result-resized-row041",
            readiness_state="ready_for_protocol_handoff",
            input_trace=_trace(),
            placement_handoff=handoff,
            capital_sizing_recomputed=True,
        )


def test_opening_service_emits_protocol_only_non_executing_readiness_material() -> None:
    result = DownstreamOpeningService().evaluate_placement_readiness(
        decision=_decision(),
        serial_candidate_id="serial-candidate-row041",
        placement_constraint_ids=["limit-only"],
        readiness_id="service-row041",
    )

    assert result.input_trace.broker_boundary_mode == "protocol_only"
    assert result.broker_execution_opened is False
    assert result.capital_sizing_recomputed is False
    assert result.placement_handoff is not None
    assert result.placement_handoff.broker_protocol_only is True
    assert result.placement_handoff.execution_allowed is False
