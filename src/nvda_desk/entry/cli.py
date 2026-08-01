"""Translate bounded CLI JSON into the accepted M00 application contracts."""

from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

from nvda_desk.m00_application_shell import (
    ApplicationCommand,
    ApplicationQuery,
    RunCoordinator,
)


def run_command(
    payload: Mapping[str, Any], *, coordinator: RunCoordinator
) -> dict[str, Any]:
    """Validate one exact application command and return its M00 receipt."""

    command = ApplicationCommand.model_validate(payload)
    return coordinator.run(command).model_dump(mode="json")


def query_command(
    payload: Mapping[str, Any], *, coordinator: RunCoordinator
) -> dict[str, Any]:
    """Validate one exact read-only application query and return its M12 projection."""

    query = ApplicationQuery.model_validate(payload)
    return coordinator.query(query).model_dump(mode="json")


def _json_object(raw: str) -> Mapping[str, Any]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("cli_payload_must_be_json_object")
    return value


def build_cli(*, coordinator: RunCoordinator) -> argparse.ArgumentParser:
    """Build the canonical CLI with one command and one read-only query route."""

    parser = argparse.ArgumentParser(prog="nvda-desk")
    subparsers = parser.add_subparsers(dest="operation", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--payload-json", required=True)
    run_parser.set_defaults(
        handler=lambda args: run_command(
            _json_object(args.payload_json),
            coordinator=coordinator,
        )
    )

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--payload-json", required=True)
    query_parser.set_defaults(
        handler=lambda args: query_command(
            _json_object(args.payload_json),
            coordinator=coordinator,
        )
    )

    return parser


def run_cli(
    argv: Sequence[str] | None = None, *, coordinator: RunCoordinator
) -> dict[str, Any]:
    """Parse arguments and execute one explicitly injected M00 operation."""

    parser = build_cli(coordinator=coordinator)
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.handler(args)
