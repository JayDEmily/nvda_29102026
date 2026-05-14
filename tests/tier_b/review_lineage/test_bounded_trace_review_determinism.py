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


def test_bounded_trace_review_surfaces_are_present() -> None:
    review_module = _require_module("nvda_desk.testing.bounded_trace_review")
    contracts = _require_module("nvda_desk.contracts.review")

    _require_attr(review_module, "BoundedTraceReviewService")
    _require_attr(review_module, "BoundedTraceReviewReport")
    _require_attr(review_module, "BoundedTraceRunResult")
    _require_attr(contracts, "ReviewPacket")


def test_bounded_trace_review_report_stays_deterministic_and_review_facing() -> None:
    review_module = _require_module("nvda_desk.testing.bounded_trace_review")
    report_model = _require_attr(review_module, "BoundedTraceReviewReport")
    run_model = _require_attr(review_module, "BoundedTraceRunResult")

    assert hasattr(report_model, "model_fields")
    assert hasattr(run_model, "model_fields")
    assert "runs" in report_model.model_fields
    assert "narrative_summary" in report_model.model_fields
    assert "scenario_id" in run_model.model_fields
    assert "summary" in run_model.model_fields
