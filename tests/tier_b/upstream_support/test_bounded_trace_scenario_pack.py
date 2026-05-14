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


def test_bounded_trace_pack_contract_surfaces_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.trace_review")

    _require_attr(contracts, "BoundedTraceFixturePack")
    _require_attr(contracts, "BoundedTraceScenario")
    _require_attr(contracts, "BoundedTraceReviewReport")


def test_bounded_trace_pack_stays_bounded_and_fixture_root_exists() -> None:
    contracts = _require_module("nvda_desk.contracts.trace_review")
    pack_model = _require_attr(contracts, "BoundedTraceFixturePack")

    assert hasattr(pack_model, "model_fields")
    assert "scenario_ids" in pack_model.model_fields
    assert "scenarios" in pack_model.model_fields

    fixture_root = Path("fixtures/trace_review")
    if not fixture_root.exists():
        pytest.fail("Required fixture root is not implemented: fixtures/trace_review")
