"""Config authority package for typed runtime configuration and governed access surfaces."""

from nvda_desk.config.bundle_loader import ConfigBundle, load_config_bundle
from nvda_desk.config.coefficient_authority import (
    DEFAULT_COEFFICIENT_AUTHORITY_PATH,
    CoefficientAuthorityService,
)
from nvda_desk.config.config_surface import ConfigSurface
from nvda_desk.config.playbook_registry import (
    DEFAULT_PLAYBOOK_REGISTRY_PATH,
    PlaybookRegistryDocument,
    build_playbook_metadata_receipts,
    load_playbook_registry,
)
from nvda_desk.config.runtime_settings import (
    DEFAULT_RUNTIME_SETTINGS_PATH,
    RuntimePathSettings,
    RuntimeSettingsDocument,
    load_runtime_settings,
)

__all__ = [
    "DEFAULT_COEFFICIENT_AUTHORITY_PATH",
    "DEFAULT_PLAYBOOK_REGISTRY_PATH",
    "DEFAULT_RUNTIME_SETTINGS_PATH",
    "CoefficientAuthorityService",
    "ConfigBundle",
    "ConfigSurface",
    "PlaybookRegistryDocument",
    "build_playbook_metadata_receipts",
    "RuntimePathSettings",
    "RuntimeSettingsDocument",
    "load_config_bundle",
    "load_playbook_registry",
    "load_runtime_settings",
]
