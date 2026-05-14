"""Typed runtime-settings loader for the benchmark-owned config home."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

DEFAULT_RUNTIME_SETTINGS_PATH = Path("config/runtime_settings.example.yaml")


class RuntimePathSettings(BaseModel):
    """Path-bearing subset of the runtime settings surface."""

    model_config = ConfigDict(extra="allow")
    coefficient_authority_path: str | None = None
    coefficients_registry_path: str | None = None
    strategy_variants_path: str | None = None
    playbook_registry_path: str | None = None


class RuntimeSettingsDocument(BaseModel):
    """Typed runtime settings document loaded from the governed example YAML."""

    model_config = ConfigDict(extra="allow")
    schema_version: str | None = None
    paths: RuntimePathSettings = Field(default_factory=RuntimePathSettings)


def load_runtime_settings(
    path: Path | str = DEFAULT_RUNTIME_SETTINGS_PATH,
) -> RuntimeSettingsDocument:
    """Load and validate the repo-owned runtime settings example document."""

    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return RuntimeSettingsDocument.model_validate(payload)
