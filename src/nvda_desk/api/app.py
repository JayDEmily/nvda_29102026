"""Expose the benchmark-owned API app cut without widening the current web shell."""

from __future__ import annotations

from typing import Any

from nvda_desk.adapters.egress.api_dto_adapter import ApiDtoAdapter
from nvda_desk.api.deps import get_api_dto_adapter, get_config_surface, get_runtime_orchestrator
from nvda_desk.config import ConfigSurface
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator


class HttpApp:
    """Small boundary app shell around bounded dependency and runtime composition."""

    def __init__(
        self,
        *,
        orchestrator: DeskRuntimeOrchestrator | None = None,
        config_surface: ConfigSurface | None = None,
        dto_adapter: ApiDtoAdapter | None = None,
    ) -> None:
        self.orchestrator = orchestrator or get_runtime_orchestrator()
        self.config_surface = config_surface or get_config_surface()
        self.dto_adapter = dto_adapter or get_api_dto_adapter()
        self.route_handlers: dict[str, Any] = {}

    def healthcheck(self) -> dict[str, str]:
        """Return the bounded health surface supported by the rebuild-phase shell."""

        return self.dto_adapter.to_state_dto({"status": "ok"})

    def run_once(self, stage_inputs: dict[str, Any]) -> dict[str, Any]:
        """Run one bounded runtime pass from already-typed stage inputs."""

        return self.dto_adapter.to_runtime_dto(self.orchestrator.run_once(stage_inputs))


def register_routes(app: HttpApp) -> HttpApp:
    """Attach the minimal bounded route table supported by the current shell."""

    app.route_handlers = {
        "healthcheck": app.healthcheck,
        "run_once": app.run_once,
    }
    return app


def create_app(
    *,
    orchestrator: DeskRuntimeOrchestrator | None = None,
    config_surface: ConfigSurface | None = None,
    dto_adapter: ApiDtoAdapter | None = None,
) -> HttpApp:
    """Create the minimal boundary app shell for entry/bootstrap callers."""

    app = HttpApp(orchestrator=orchestrator, config_surface=config_surface, dto_adapter=dto_adapter)
    return register_routes(app)
