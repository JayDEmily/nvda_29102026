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


def test_checkpoint_helper_surface_is_present_for_prepared_ingress_boundaries() -> None:
    checkpoints = _require_module("nvda_desk.downstream.checkpoints")
    assert checkpoints.__name__ == "nvda_desk.downstream.checkpoints"
    assert _require_attr(checkpoints, "CheckpointObservation") is getattr(
        checkpoints, "CheckpointObservation"
    )
