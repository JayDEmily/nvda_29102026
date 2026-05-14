"""Bounded API dependency composition for the rebuild-phase boundary shell."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.adapters.egress.api_dto_adapter import ApiDtoAdapter
from nvda_desk.config import ConfigSurface
from nvda_desk.config.bundle_loader import DEFAULT_CONFIG_DIR
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator


def get_config_surface(config_dir: Path | str = DEFAULT_CONFIG_DIR) -> ConfigSurface:
    """Return the bounded config surface used by boundary bootstrap shells."""

    return ConfigSurface(config_dir)


def get_runtime_orchestrator() -> DeskRuntimeOrchestrator:
    """Return the bounded runtime orchestrator used by the boundary app shell."""

    return DeskRuntimeOrchestrator()


def get_api_dto_adapter() -> ApiDtoAdapter:
    """Return the admitted DTO projection owner used by the bounded API shell."""

    return ApiDtoAdapter()
