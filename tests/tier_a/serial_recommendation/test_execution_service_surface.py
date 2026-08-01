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


def test_execution_service_and_domain_surfaces_are_present() -> None:
    service = _require_module("nvda_desk.services.execution_service")
    assert service.__name__ == "nvda_desk.services.execution_service"
    candidate_expression = _require_module("nvda_desk.domain.execution.candidate_expression")
    assert candidate_expression.__name__ == "nvda_desk.domain.execution.candidate_expression"
    lifecycle_plan = _require_module("nvda_desk.domain.execution.lifecycle_plan")
    assert lifecycle_plan.__name__ == "nvda_desk.domain.execution.lifecycle_plan"

    assert _require_attr(service, "ExecutionService") is getattr(service, "ExecutionService")
    assert _require_attr(candidate_expression, "evaluate_execution_expression") is getattr(
        candidate_expression, "evaluate_execution_expression"
    )
    assert _require_attr(lifecycle_plan, "build_lifecycle_plan") is getattr(
        lifecycle_plan, "build_lifecycle_plan"
    )
