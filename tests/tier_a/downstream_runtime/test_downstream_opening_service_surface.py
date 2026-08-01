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


def test_downstream_opening_service_surface_is_present() -> None:
    opening = _require_module("nvda_desk.downstream.opening")
    assert opening.__name__ == "nvda_desk.downstream.opening"
    assert _require_attr(opening, "DownstreamOpeningService") is getattr(
        opening, "DownstreamOpeningService"
    )
