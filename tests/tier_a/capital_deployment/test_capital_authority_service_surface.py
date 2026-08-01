from __future__ import annotations

import importlib

import pytest

from nvda_desk.contracts.capital import CapitalDeploymentAuthorityInput


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def _input() -> CapitalDeploymentAuthorityInput:
    return CapitalDeploymentAuthorityInput(
        final_risk_action="proceed",
        final_risk_receipt_id="final-risk-service-001",
        serial_candidate_id="candidate-service-001",
        downstream_pre_deployment_allowed=True,
        downstream_pre_deployment_receipt_id="pre-deployment-service-001",
        parallel_risk_packet_id="parallel-risk-service-001",
        capital_state_snapshot_id="capital-state-service-001",
        available_capital_usd=10_000.0,
        bounded_policy_id="bounded-policy-service-001",
        requested_deployable_pct=5.0,
        max_deployable_pct=5.0,
    )


def test_capital_authority_service_surfaces_are_present() -> None:
    authority = _require_module("nvda_desk.capital.authority")
    assert authority.__name__ == "nvda_desk.capital.authority"
    orchestration = _require_module("nvda_desk.services.capital_deployment_service")
    assert orchestration.__name__ == "nvda_desk.services.capital_deployment_service"

    assert _require_attr(authority, "CapitalDeploymentAuthorityService") is getattr(
        authority, "CapitalDeploymentAuthorityService"
    )
    assert _require_attr(authority, "evaluate_capital_deployment") is getattr(
        authority, "evaluate_capital_deployment"
    )
    assert _require_attr(authority, "build_capital_deployment_receipt") is getattr(
        authority, "build_capital_deployment_receipt"
    )
    assert _require_attr(orchestration, "CapitalDeploymentService") is getattr(
        orchestration, "CapitalDeploymentService"
    )


def test_capital_authority_service_emits_receipt_without_placement_authority() -> None:
    orchestration = _require_module("nvda_desk.services.capital_deployment_service")
    assert orchestration.__name__ == "nvda_desk.services.capital_deployment_service"
    service = orchestration.CapitalDeploymentService()
    receipt = service.evaluate_with_receipt(_input(), receipt_id="capital-service-receipt-001")

    assert receipt.receipt_id == "capital-service-receipt-001"
    assert receipt.decision.capital_deployment_receipt_id == "capital-service-receipt-001"
    assert receipt.input_trace.serial_candidate_id == "candidate-service-001"
    assert receipt.placement_authority_opened is False
    assert "authorised_notional_usd" in receipt.emitted_output
