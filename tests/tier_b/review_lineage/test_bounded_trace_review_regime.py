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


def test_bounded_trace_review_regime_surfaces_are_present() -> None:
    review_module = _require_module("nvda_desk.testing.bounded_trace_review")
    contracts = _require_module("nvda_desk.contracts.trace_review")

    _require_attr(review_module, "BoundedTraceReviewService")
    run_model = _require_attr(contracts, "BoundedTraceRunResult")
    assert hasattr(run_model, "model_fields")


def test_bounded_trace_review_run_result_keeps_human_sanity_outputs_visible() -> None:
    contracts = _require_module("nvda_desk.contracts.trace_review")
    run_model = _require_attr(contracts, "BoundedTraceRunResult")

    assert "scenario_id" in run_model.model_fields
    assert "permission_state" in run_model.model_fields
    assert "active_playbook_ids" in run_model.model_fields
    assert "final_risk_action" in run_model.model_fields
    assert "capital_deployment_action" in run_model.model_fields
