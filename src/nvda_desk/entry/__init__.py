"""Entry package for bounded ASGI and CLI bootstrap surfaces."""

from nvda_desk.entry.asgi import configure_middlewares, create_app
from nvda_desk.entry.cli import build_cli, inspect_config_command, run_cli, run_once_command

__all__ = [
    "build_cli",
    "configure_middlewares",
    "create_app",
    "inspect_config_command",
    "run_cli",
    "run_once_command",
]
