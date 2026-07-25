from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def test_options_flow_history_repository_is_separate_from_runtime_authority() -> None:
    assert _require_module("nvda_desk.repositories.options_flow_history_repository").__name__ == "nvda_desk.repositories.options_flow_history_repository"
    assert _require_module("nvda_desk.repositories.position_repository").__name__ == "nvda_desk.repositories.position_repository"
    assert _require_module("nvda_desk.repositories.capital_state_repository").__name__ == "nvda_desk.repositories.capital_state_repository"
    assert _require_module("nvda_desk.repositories.review_repository").__name__ == "nvda_desk.repositories.review_repository"
