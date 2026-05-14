"""Thin accessor over the benchmark-owned config bundle and authority surfaces."""

from __future__ import annotations

from functools import cached_property
from pathlib import Path

from nvda_desk.config.bundle_loader import DEFAULT_CONFIG_DIR, ConfigBundle, load_config_bundle
from nvda_desk.config.coefficient_authority import CoefficientAuthorityService


class ConfigSurface:
    """Provide bounded access to the repo-owned config authority bundle."""

    def __init__(self, config_dir: Path | str = DEFAULT_CONFIG_DIR) -> None:
        self.config_dir = Path(config_dir)

    @cached_property
    def bundle(self) -> ConfigBundle:
        """Load the typed config bundle once per surface instance."""

        return load_config_bundle(self.config_dir)

    def runtime_settings(self):
        """Return the typed runtime-settings document from the bundle."""

        return self.bundle.runtime_settings

    def coefficient_authority_service(self) -> CoefficientAuthorityService:
        """Return the bounded coefficient-authority access surface."""

        return CoefficientAuthorityService(self.config_dir / "coefficient_authority.v1.yaml")

    def coefficient_authority_document(self):
        """Return the typed coefficient-authority document from the config home."""

        return self.coefficient_authority_service().load_document()

    def playbook_registry(self):
        """Return the typed playbook registry from the bundle."""

        return self.bundle.playbook_registry
