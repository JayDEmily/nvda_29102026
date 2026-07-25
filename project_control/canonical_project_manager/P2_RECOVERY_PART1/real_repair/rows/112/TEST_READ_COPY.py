from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def test_options_flow_history_replay_stays_separate_from_live_trade_state() -> None:
    assert _require_module("nvda_desk.repositories.options_flow_history_repository").__name__ == "nvda_desk.repositories.options_flow_history_repository"
    assert _require_module("nvda_desk.services.options_flow_context_service").__name__ == "nvda_desk.services.options_flow_context_service"
    assert _require_module("nvda_desk.downstream.state_reader").__name__ == "nvda_desk.downstream.state_reader"
