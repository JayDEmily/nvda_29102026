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


def test_options_flow_contract_models_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.options_flow")
    assert contracts.__name__ == "nvda_desk.contracts.options_flow"
    history_contracts = _require_module("nvda_desk.contracts.options_flow_history")
    assert history_contracts.__name__ == "nvda_desk.contracts.options_flow_history"

    assert _require_attr(contracts, "OptionsFlowContextInput") is getattr(
        contracts, "OptionsFlowContextInput"
    )
    assert _require_attr(contracts, "OptionsFlowContextOutput") is getattr(
        contracts, "OptionsFlowContextOutput"
    )
    assert _require_attr(history_contracts, "OptionsFlowHistoryObservationRecord") is getattr(
        history_contracts, "OptionsFlowHistoryObservationRecord"
    )
    assert _require_attr(history_contracts, "OptionsFlowHistoryWriteResult") is getattr(
        history_contracts, "OptionsFlowHistoryWriteResult"
    )
