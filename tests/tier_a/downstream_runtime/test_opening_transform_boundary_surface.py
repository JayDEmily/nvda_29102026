from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentDecision,
)
from nvda_desk.contracts.downstream import PlacementHandoffMaterial
from nvda_desk.downstream.opening import DownstreamOpeningService

FORBIDDEN_EXECUTION_RECORD_KEYS = {
    "execution_record_id",
    "ExecutionRecord",
    "execution_fill_id",
    "broker_execution_record",
    "fill_price_usd",
}
ALLOWED_SERVICE_PREVIEW_KEYS = {
    "serial_candidate_id",
    "capital_deployment_receipt_id",
    "authorised_deployable_pct",
    "authorised_notional_usd",
    "placement_constraint_ids",
}


def _decision() -> CapitalDeploymentDecision:
    return CapitalDeploymentDecision(
        action=CapitalDeploymentAuthorityAction.CONTINUE,
        authorised_deployable_pct=8.0,
        authorised_notional_usd=8_000.0,
        consumed_inputs=["capital_state", "bounded_deployment_policy"],
        rationale=["row042"],
        capital_deployment_receipt_id="capital-receipt-row042",
    )


def _payload_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _payload_keys(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _payload_keys(child)


def test_placement_handoff_rejects_execution_record_donor_payload_shape() -> None:
    with pytest.raises(ValidationError, match="execution record"):
        PlacementHandoffMaterial(
            handoff_id="handoff-execution-record-row042",
            order_intent_preview={
                "serial_candidate_id": "serial-candidate-row042",
                "donor_execution_record": {
                    "ExecutionRecord": {
                        "execution_record_id": "exec-record-row042",
                        "execution_fill_id": "fill-row042",
                        "fill_price_usd": 712.34,
                    }
                },
            },
        )


def test_opening_service_preview_stays_in_native_handoff_shape() -> None:
    result = DownstreamOpeningService().evaluate_placement_readiness(
        decision=_decision(),
        serial_candidate_id="serial-candidate-row042",
        placement_constraint_ids=["limit-only"],
        readiness_id="transform-row042",
    )

    assert result.placement_handoff is not None
    preview = result.placement_handoff.order_intent_preview
    assert set(preview) == ALLOWED_SERVICE_PREVIEW_KEYS
    assert not (set(_payload_keys(preview)) & FORBIDDEN_EXECUTION_RECORD_KEYS)


def test_opening_transform_boundary_does_not_import_execution_record_contracts() -> None:
    source = Path("src/nvda_desk/downstream/opening.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)

    assert "ExecutionRecord" not in imported_names
    assert "broker_execution_record" not in source
