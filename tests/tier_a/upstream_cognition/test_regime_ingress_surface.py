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


def test_regime_ingress_mapper_and_service_surfaces_are_present() -> None:
    mapper = _require_module("nvda_desk.cognition.ingress.regime_mapper")
    assert mapper.__name__ == "nvda_desk.cognition.ingress.regime_mapper"
    service = _require_module("nvda_desk.services.regime_context_service")
    assert service.__name__ == "nvda_desk.services.regime_context_service"

    assert _require_attr(mapper, "build_regime_input") is getattr(mapper, "build_regime_input")
    assert _require_attr(service, "RegimeContextService") is getattr(service, "RegimeContextService")
