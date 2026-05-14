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


def test_api_boundary_surface_is_present() -> None:
    app_module = _require_module("nvda_desk.api.app")
    assert app_module.__name__ == "nvda_desk.api.app"
    deps_module = _require_module("nvda_desk.api.deps")
    assert deps_module.__name__ == "nvda_desk.api.deps"
    wrapper_module = _require_module("nvda_desk.api.http.app")
    assert wrapper_module.__name__ == "nvda_desk.api.http.app"

    assert _require_attr(app_module, "HttpApp") is getattr(app_module, "HttpApp")
    assert _require_attr(app_module, "create_app") is getattr(app_module, "create_app")
    assert _require_attr(app_module, "register_routes") is getattr(app_module, "register_routes")
    assert _require_attr(deps_module, "get_config_surface") is getattr(deps_module, "get_config_surface")
    assert _require_attr(deps_module, "get_runtime_orchestrator") is getattr(deps_module, "get_runtime_orchestrator")

    assert wrapper_module.HttpApp is app_module.HttpApp
    assert wrapper_module.create_app is app_module.create_app


def test_api_boundary_wiring_stays_bounded_to_app_shell_and_runtime_orchestrator() -> None:
    app_module = _require_module("nvda_desk.api.app")
    assert app_module.__name__ == "nvda_desk.api.app"

    create_app = _require_attr(app_module, "create_app")
    assert create_app is getattr(app_module, "create_app")
    app = create_app()

    assert app.healthcheck() == {"status": "ok"}
    assert sorted(app.route_handlers) == ["healthcheck", "run_once"]
    assert "paths" in app.config_surface.runtime_settings().model_dump()

    receipt = app.run_once({"temporal": {"present": True}})
    assert receipt["executed_stages"] == ["temporal"]
    assert receipt["missing_stages"][0] == "regime"
