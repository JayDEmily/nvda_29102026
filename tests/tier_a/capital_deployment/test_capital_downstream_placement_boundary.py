from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def test_capital_authority_is_downstream_not_a_serial_stage_module() -> None:
    assert _require_module("nvda_desk.capital.authority").__name__ == "nvda_desk.capital.authority"
    assert _require_module("nvda_desk.services.final_risk_service").__name__ == "nvda_desk.services.final_risk_service"
    assert _require_module("nvda_desk.downstream.opening").__name__ == "nvda_desk.downstream.opening"
