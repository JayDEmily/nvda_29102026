"""Expose the benchmark-owned CLI bootstrap surface without widening into replay or evaluation flows."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

from nvda_desk.api.app import HttpApp
from nvda_desk.api.deps import get_config_surface
from nvda_desk.entry.asgi import create_app


def inspect_config_command() -> dict[str, Any]:
    """Return the bounded runtime-settings view currently exposed to CLI callers."""

    return get_config_surface().runtime_settings().model_dump()


def run_once_command(
    stage_inputs: Mapping[str, Any], *, app: HttpApp | None = None
) -> dict[str, Any]:
    """Run one bounded runtime pass from already-typed stage-input mappings."""

    boundary_app = app or create_app()
    return boundary_app.run_once(dict(stage_inputs))


def build_cli() -> argparse.ArgumentParser:
    """Build the bounded CLI surface admitted in the current tranche."""

    parser = argparse.ArgumentParser(prog="nvda-desk")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect-config")
    inspect_parser.set_defaults(handler=lambda _: inspect_config_command())

    run_once_parser = subparsers.add_parser("run-once")
    run_once_parser.add_argument("--stage-inputs-json", required=True)
    run_once_parser.set_defaults(
        handler=lambda args: run_once_command(json.loads(args.stage_inputs_json)),
    )

    return parser


def run_cli(argv: Sequence[str] | None = None) -> Any:
    """Parse arguments and execute the bounded CLI command set."""

    parser = build_cli()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.handler(args)
