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


def test_serial_execution_boundary_is_separate_from_capital_authority() -> None:
    contracts = _require_module("nvda_desk.contracts.execution")
    assert contracts.__name__ == "nvda_desk.contracts.execution"
    assert _require_module("nvda_desk.capital.authority").__name__ == "nvda_desk.capital.authority"
    assert _require_module("nvda_desk.risk.join.final_join").__name__ == "nvda_desk.risk.join.final_join"

    output_model = _require_attr(contracts, "ExecutionExpressionOutput")
    assert output_model is getattr(contracts, "ExecutionExpressionOutput")

    assert hasattr(output_model, "model_fields")
    assert "capital_deployment_authority" not in output_model.model_fields
