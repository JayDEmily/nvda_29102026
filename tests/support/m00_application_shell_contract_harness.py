"""Reference-only M00 composition contract and production API loader.

The reference functions encode the admitted C-NORM ordering and fail-closed
properties without providing the production composition root.  Production
conformance is exercised only through ``production_api``.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable


@dataclass(frozen=True)
class ReferenceCommand:
    command_id: str = "m00.command.001"
    prepared_id: str = "prepared.001"
    prepared_fingerprint: str = "a" * 64
    trace_id: str = "trace.001"
    run_id: str = "run.001"
    scenario_id: str = "paper.alpha.001"
    prepared_packet_id: str = "packet.prepared.001"
    serial_packet_id: str = "packet.serial.001"
    parallel_packet_id: str = "packet.parallel.001"
    serial_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)
    parallel_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)
    capital_emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 1, tzinfo=UTC)
    intent_at_utc: datetime = datetime(2026, 8, 1, 1, 2, tzinfo=UTC)
    executed_at_utc: datetime = datetime(2026, 8, 1, 1, 3, tzinfo=UTC)


@dataclass(frozen=True)
class ReferenceRunReceipt:
    command_id: str
    run_id: str
    outcome: str
    owner_steps: tuple[str, ...]
    scope_id: str | None
    replay_class: None = None
    live_execution_proven: bool = False
    durable_state_proven: bool = False


class RecordingOwners:
    """Deterministic owner-seam specimen used only by the C-PROOF reference tests."""

    def __init__(self, *, capital_action: str = "continue") -> None:
        self.capital_action = capital_action
        self.calls: list[str] = []
        self.scope_counter = 0

    def call(self, name: str) -> dict[str, Any]:
        self.calls.append(name)
        if name == "capital":
            return {"action": self.capital_action}
        return {"owner": name}

    def new_scope(self) -> str:
        self.scope_counter += 1
        scope_id = f"scope.{self.scope_counter}"
        self.calls.append(f"scope:{scope_id}")
        return scope_id


def _require_nonempty(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing_{field}")


def _require_utc(value: datetime, field: str) -> None:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(f"{field}_must_be_utc")


def evaluate_reference(command: ReferenceCommand, owners: RecordingOwners) -> ReferenceRunReceipt:
    """Evaluate the minimal admitted M00 order with no production implementation."""

    for field in (
        "command_id",
        "prepared_id",
        "prepared_fingerprint",
        "trace_id",
        "run_id",
        "scenario_id",
        "prepared_packet_id",
        "serial_packet_id",
        "parallel_packet_id",
    ):
        _require_nonempty(getattr(command, field), field)
    if len(command.prepared_fingerprint) != 64:
        raise ValueError("invalid_prepared_fingerprint")

    times = (
        ("serial_emitted_at_utc", command.serial_emitted_at_utc),
        ("parallel_emitted_at_utc", command.parallel_emitted_at_utc),
        ("capital_emitted_at_utc", command.capital_emitted_at_utc),
        ("intent_at_utc", command.intent_at_utc),
        ("executed_at_utc", command.executed_at_utc),
    )
    for field, value in times:
        _require_utc(value, field)
    if command.capital_emitted_at_utc < max(
        command.serial_emitted_at_utc, command.parallel_emitted_at_utc
    ):
        raise ValueError("capital_time_precedes_owner_packets")
    if not (command.capital_emitted_at_utc <= command.intent_at_utc <= command.executed_at_utc):
        raise ValueError("execution_time_order_invalid")

    for name in (
        "prepared_context_packet",
        "serial",
        "parallel",
        "serial_packet",
        "parallel_packet",
        "final_risk",
    ):
        owners.call(name)
    capital = owners.call("capital")
    action = capital["action"]
    if action in {"block", "no_trade"}:
        return ReferenceRunReceipt(
            command_id=command.command_id,
            run_id=command.run_id,
            outcome=action,
            owner_steps=tuple(owners.calls),
            scope_id=None,
        )
    if action not in {"continue", "reduce"}:
        raise ValueError("unsupported_capital_action")

    scope_id = owners.new_scope()
    owners.call("paper_execution")
    owners.call("portfolio_reconciliation")
    return ReferenceRunReceipt(
        command_id=command.command_id,
        run_id=command.run_id,
        outcome="paper_filled",
        owner_steps=tuple(owners.calls),
        scope_id=scope_id,
    )


def evaluate_query_reference(*, run_calls: list[str], replay_calls: list[str]) -> str:
    """Prove that the M12 query path is separate from runtime execution."""

    replay_calls.extend(("assess", "project"))
    if run_calls:
        raise AssertionError("application_query_invoked_runtime")
    return "review_projection"


def _mutant_places_after_block(command: ReferenceCommand) -> ReferenceRunReceipt:
    owners = RecordingOwners(capital_action="block")
    receipt = evaluate_reference(command, owners)
    owners.new_scope()
    owners.call("paper_execution")
    return ReferenceRunReceipt(
        command_id=receipt.command_id,
        run_id=receipt.run_id,
        outcome="paper_filled",
        owner_steps=tuple(owners.calls),
        scope_id="scope.1",
    )


def _mutant_reuses_scope(command: ReferenceCommand) -> tuple[str | None, str | None]:
    owners = RecordingOwners()
    first = evaluate_reference(command, owners)
    # Deliberately returns the prior scope rather than creating another run scope.
    return first.scope_id, first.scope_id


def _mutant_promotes_runtime_to_replay(command: ReferenceCommand) -> dict[str, Any]:
    receipt = evaluate_reference(command, RecordingOwners())
    return {"receipt": receipt, "replay_class": "preserved_occurrence_replay"}


MUTANTS: dict[str, Callable[[ReferenceCommand], Any]] = {
    "places_after_block": _mutant_places_after_block,
    "reuses_scope": _mutant_reuses_scope,
    "promotes_runtime_to_replay": _mutant_promotes_runtime_to_replay,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m00_application_shell")
    required = (
        "ApplicationCommand",
        "ApplicationQuery",
        "ApplicationRunReceipt",
        "RunCoordinator",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M00 package missing exports: {missing}")
    prohibited = ("DeskRuntimeOrchestrator", "HttpApp")
    leaked = [name for name in prohibited if hasattr(module, name)]
    if leaked:
        raise AssertionError(f"canonical M00 package leaked compatibility owners: {leaked}")
    return {name: getattr(module, name) for name in required}
