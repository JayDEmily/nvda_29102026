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


def test_review_stage_surface_is_present() -> None:
    review_stage = _require_module("nvda_desk.downstream.review_stage")
    assert review_stage.__name__ == "nvda_desk.downstream.review_stage"
    assert _require_attr(review_stage, "ReviewStageService") is getattr(review_stage, "ReviewStageService")
    for attr_name in ("build_review_packet", "attach_lineage", "attach_imported_citations"):
        assert _require_attr(review_stage, attr_name) is getattr(review_stage, attr_name)
