"""Expose the benchmark-owned ASGI/bootstrap entry surface for the bounded app shell."""

from __future__ import annotations

from nvda_desk.api.app import HttpApp
from nvda_desk.api.app import create_app as create_boundary_app
from nvda_desk.config import ConfigSurface
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator


def configure_middlewares(app: HttpApp) -> HttpApp:
    """Return the current app shell unchanged until middleware work is lawfully admitted."""

    return app


def create_app(
    *,
    orchestrator: DeskRuntimeOrchestrator | None = None,
    config_surface: ConfigSurface | None = None,
) -> HttpApp:
    """Create the bounded app shell through the benchmark-owned entry surface."""

    app = create_boundary_app(orchestrator=orchestrator, config_surface=config_surface)
    return configure_middlewares(app)
