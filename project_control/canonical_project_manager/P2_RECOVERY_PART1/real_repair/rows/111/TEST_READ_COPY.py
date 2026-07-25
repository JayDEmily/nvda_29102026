from __future__ import annotations

import importlib
from pathlib import Path

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


def test_options_flow_history_persistence_surfaces_are_present() -> None:
    repository = _require_module("nvda_desk.repositories.options_flow_history_repository")
    assert repository.__name__ == "nvda_desk.repositories.options_flow_history_repository"
    assert _require_attr(repository, "OptionsFlowHistoryRepository") is getattr(repository, "OptionsFlowHistoryRepository")

    versions_dir = Path("alembic/versions")
    if not versions_dir.exists():
        pytest.fail("Required migration directory is not implemented: alembic/versions")
