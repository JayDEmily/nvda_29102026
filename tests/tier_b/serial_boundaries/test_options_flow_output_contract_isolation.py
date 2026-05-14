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


def test_options_flow_contract_and_service_surfaces_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow")
    serial_module = _require_module("nvda_desk.cognition.serial.options_flow")
    service_module = _require_module("nvda_desk.services.options_flow_context_service")

    _require_attr(contracts, "OptionsFlowContextInput")
    output_model = _require_attr(contracts, "OptionsFlowContextOutput")
    _require_attr(serial_module, "evaluate_options_flow_context")
    _require_attr(service_module, "OptionsFlowContextService")

    assert hasattr(output_model, "model_fields")


def test_options_flow_output_fields_remain_descriptive_only() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow")
    output_model = _require_attr(contracts, "OptionsFlowContextOutput")

    forbidden_tokens = ("permission", "deploy", "capital", "inventory_action", "authorised")
    for field_name in output_model.model_fields.keys():
        assert not any(token in field_name for token in forbidden_tokens), field_name
