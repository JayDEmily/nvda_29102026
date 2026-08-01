"""Canonical transport adapters for the accepted M00 application shell."""

from nvda_desk.entry.asgi import configure_middlewares, create_app
from nvda_desk.entry.cli import build_cli, query_command, run_cli, run_command

__all__ = [
    "build_cli",
    "configure_middlewares",
    "create_app",
    "query_command",
    "run_cli",
    "run_command",
]
