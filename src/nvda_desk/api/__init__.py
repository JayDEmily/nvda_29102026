"""API boundary package for bounded app wiring and dependency composition."""

from nvda_desk.api.app import HttpApp, create_app, register_routes
from nvda_desk.api.deps import get_config_surface, get_runtime_orchestrator

__all__ = [
    "HttpApp",
    "create_app",
    "get_config_surface",
    "get_runtime_orchestrator",
    "register_routes",
]
