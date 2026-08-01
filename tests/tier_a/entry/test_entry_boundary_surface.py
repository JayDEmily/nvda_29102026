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


def test_entry_boundary_surfaces_are_present() -> None:
    asgi_module = _require_module("nvda_desk.entry.asgi")
    assert asgi_module.__name__ == "nvda_desk.entry.asgi"
    cli_module = _require_module("nvda_desk.entry.cli")
    assert cli_module.__name__ == "nvda_desk.entry.cli"

    assert _require_attr(asgi_module, "create_app") is getattr(asgi_module, "create_app")
    assert _require_attr(asgi_module, "configure_middlewares") is getattr(
        asgi_module, "configure_middlewares"
    )
    assert _require_attr(cli_module, "build_cli") is getattr(cli_module, "build_cli")
    assert _require_attr(cli_module, "inspect_config_command") is getattr(
        cli_module, "inspect_config_command"
    )
    assert _require_attr(cli_module, "run_cli") is getattr(cli_module, "run_cli")
    assert _require_attr(cli_module, "run_once_command") is getattr(cli_module, "run_once_command")


def test_entry_boundary_bootstrap_exposes_only_bounded_cli_and_app_shells() -> None:
    asgi_module = _require_module("nvda_desk.entry.asgi")
    assert asgi_module.__name__ == "nvda_desk.entry.asgi"
    cli_module = _require_module("nvda_desk.entry.cli")
    assert cli_module.__name__ == "nvda_desk.entry.cli"

    create_app = _require_attr(asgi_module, "create_app")
    assert create_app is getattr(asgi_module, "create_app")
    configure_middlewares = _require_attr(asgi_module, "configure_middlewares")
    assert configure_middlewares is getattr(asgi_module, "configure_middlewares")
    run_cli = _require_attr(cli_module, "run_cli")
    assert run_cli is getattr(cli_module, "run_cli")

    app = create_app()
    assert configure_middlewares(app) is app
    assert app.healthcheck() == {"status": "ok"}

    config_view = run_cli(["inspect-config"])
    assert "paths" in config_view

    receipt = run_cli(["run-once", "--stage-inputs-json", '{"temporal": {"present": true}}'])
    assert receipt["executed_stages"] == ["temporal"]
