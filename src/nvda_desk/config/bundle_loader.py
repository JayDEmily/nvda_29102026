"""Typed config-bundle loader for the benchmark-owned config home."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.config.coefficient_authority import CoefficientAuthorityService
from nvda_desk.config.playbook_registry import PlaybookRegistryDocument, load_playbook_registry
from nvda_desk.config.runtime_settings import RuntimeSettingsDocument, load_runtime_settings

DEFAULT_CONFIG_DIR = Path("config")


class ConfigBundle(BaseModel):
    """Bounded typed bundle of repo-owned config authority documents."""

    model_config = ConfigDict(extra="forbid")
    runtime_settings: RuntimeSettingsDocument
    coefficient_authority: dict[str, Any] = Field(default_factory=dict)
    playbook_registry: PlaybookRegistryDocument
    evaluation_config: dict[str, Any] = Field(default_factory=dict)
    coefficients_registry: dict[str, Any] = Field(default_factory=dict)
    strategy_variants: dict[str, Any] = Field(default_factory=dict)


def _optional_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_config_bundle(config_dir: Path | str = DEFAULT_CONFIG_DIR) -> ConfigBundle:
    """Load the repo-owned config example bundle without widening runtime scope."""

    config_path = Path(config_dir)
    runtime_settings = load_runtime_settings(config_path / "runtime_settings.example.yaml")
    coefficient_authority = (
        CoefficientAuthorityService(config_path / "coefficient_authority.v1.yaml")
        .load_document()
        .model_dump()
    )
    playbook_registry = load_playbook_registry(config_path / "playbook_registry.example.yaml")
    return ConfigBundle(
        runtime_settings=runtime_settings,
        coefficient_authority=coefficient_authority,
        playbook_registry=playbook_registry,
        evaluation_config=_optional_yaml(config_path / "evaluation_config.example.yaml"),
        coefficients_registry=_optional_yaml(config_path / "coefficients_registry.example.yaml"),
        strategy_variants=_optional_yaml(config_path / "strategy_variants.example.yaml"),
    )
