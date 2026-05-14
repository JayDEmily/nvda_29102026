from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_playbook_eligibility_contract_and_service_surfaces_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.eligibility")
    serial_module = _require_module("nvda_desk.cognition.serial.eligibility")
    service_module = _require_module("nvda_desk.services." + "playbook_eligibility" + "_service")

    _require_attr(contracts, "EligibilityAdmissibilitySurface")
    output_model = _require_attr(contracts, "PlaybookEligibilityOutput")
    _require_attr(serial_module, "evaluate_" "playbook_eligibility")
    _require_attr(service_module, "PlaybookEligibilityService")

    assert hasattr(output_model, "model_fields")


def test_playbook_eligibility_output_stays_free_of_step4_capital_echoes() -> None:
    contracts = _require_module("nvda_desk.contracts.eligibility")

    output_model = _require_attr(contracts, "PlaybookEligibilityOutput")
    admissibility_surface = _require_attr(contracts, "EligibilityAdmissibilitySurface")

    assert "admissibility_surface" in output_model.model_fields
    assert "active_family_ids" in output_model.model_fields
    assert "active_setup_variant_ids" in output_model.model_fields
    assert "permission_state" in admissibility_surface.model_fields
    assert "no_trade_reasons" in admissibility_surface.model_fields
    assert "fresh_deployable_capital_pct" not in output_model.model_fields
    assert "inventory_action_bias" not in output_model.model_fields
