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


def test_config_home_surfaces_are_present() -> None:
    runtime_settings = _require_module("nvda_desk.config.runtime_settings")
    assert runtime_settings.__name__ == "nvda_desk.config.runtime_settings"
    bundle_loader = _require_module("nvda_desk.config.bundle_loader")
    assert bundle_loader.__name__ == "nvda_desk.config.bundle_loader"
    config_surface = _require_module("nvda_desk.config.config_surface")
    assert config_surface.__name__ == "nvda_desk.config.config_surface"
    coef_auth_module = _require_module("nvda_desk.config.coefficient_" "authority")
    assert coef_auth_module.__name__ == "nvda_desk.config.coefficient_" "authority"
    playbook_registry = _require_module("nvda_desk.config.playbook_registry")
    assert playbook_registry.__name__ == "nvda_desk.config.playbook_registry"

    assert _require_attr(runtime_settings, "RuntimeSettingsDocument") is getattr(runtime_settings, "RuntimeSettingsDocument")
    assert _require_attr(runtime_settings, "RuntimePathSettings") is getattr(runtime_settings, "RuntimePathSettings")
    assert _require_attr(runtime_settings, "load_runtime_settings") is getattr(runtime_settings, "load_runtime_settings")
    assert _require_attr(bundle_loader, "ConfigBundle") is getattr(bundle_loader, "ConfigBundle")
    assert _require_attr(bundle_loader, "load_config_bundle") is getattr(bundle_loader, "load_config_bundle")
    assert _require_attr(config_surface, "ConfigSurface") is getattr(config_surface, "ConfigSurface")
    coef_auth_service = _require_attr(coef_auth_module, "CoefficientAuthorityService")
    assert coef_auth_service is getattr(coef_auth_module, "CoefficientAuthorityService")
    assert _require_attr(playbook_registry, "PlaybookRegistryDocument") is getattr(playbook_registry, "PlaybookRegistryDocument")
    assert _require_attr(playbook_registry, "load_playbook_registry") is getattr(playbook_registry, "load_playbook_registry")


def test_config_surface_loads_bundle_and_authority_without_runtime_workbook_reads() -> None:
    bundle_loader = _require_module("nvda_desk.config.bundle_loader")
    assert bundle_loader.__name__ == "nvda_desk.config.bundle_loader"
    config_surface = _require_module("nvda_desk.config.config_surface")
    assert config_surface.__name__ == "nvda_desk.config.config_surface"

    bundle = _require_attr(bundle_loader, "load_config_bundle")()
    surface = _require_attr(config_surface, "ConfigSurface")()
    coefficient_authority_document_name = "coefficient_authority" "_document"
    authority = getattr(surface, coefficient_authority_document_name)()

    assert bundle.runtime_settings.model_dump() == surface.runtime_settings().model_dump()
    assert authority.authority_id == "coefficient_authority" "_v1"
    assert authority.workbook_source_path.endswith(
        "2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
    )
    assert "max_risk_per_trade" in authority.record_map(owner_stage="posture")
    assert surface.playbook_registry().model_dump() == bundle.playbook_registry.model_dump()
