"""Bounded implementation checks not duplicated in the frozen M13 proof."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import nvda_desk.m13_state_kernel as public_api
from nvda_desk.m13_state_kernel import (
    AtomicReceipt,
    IdempotencyKey,
    InMemoryUnitOfWork,
    RepositoryPort,
    TransactionCommand,
)

EXPECTED_EXPORTS = {
    "AtomicReceipt",
    "IdempotencyConflictError",
    "IdempotencyKey",
    "InMemoryUnitOfWork",
    "RepositoryPort",
    "StateVersionConflictError",
    "TransactionCommand",
    "UnitOfWork",
}


def _key() -> IdempotencyKey:
    return IdempotencyKey(
        value="key-1",
        command_type="synthetic_command",
        consistency_unit_id="synthetic-unit-1",
    )


def _command() -> TransactionCommand:
    return TransactionCommand(
        command_id="command-1",
        idempotency_key=_key(),
        input_fingerprint=" fingerprint-kept-exactly ",
        expected_state_version=0,
        policy_version=" policy-kept-exactly ",
    )


class _PrimaryAndRollbackFailureParticipant(RepositoryPort):
    def prepare(
        self,
        *,
        command: TransactionCommand,
        working_state: Any,
        receipt: AtomicReceipt,
    ) -> None:
        raise RuntimeError("primary participant failure")

    def commit(self) -> None:
        raise AssertionError("commit must not run")

    def rollback(self) -> None:
        raise ValueError("secondary rollback failure")


def _expect_value_error(factory: Any, field_name: str) -> None:
    try:
        factory()
    except ValueError:
        return
    raise AssertionError(f"{field_name} accepted an empty identifier")


def main() -> None:
    assert set(public_api.__all__) == EXPECTED_EXPORTS

    for field_name, factory in (
        (
            "IdempotencyKey.value",
            lambda: IdempotencyKey("", "command", "unit"),
        ),
        (
            "IdempotencyKey.command_type",
            lambda: IdempotencyKey("key", "   ", "unit"),
        ),
        (
            "IdempotencyKey.consistency_unit_id",
            lambda: IdempotencyKey("key", "command", ""),
        ),
        (
            "TransactionCommand.command_id",
            lambda: TransactionCommand("", _key(), "fingerprint", 0, "policy"),
        ),
        (
            "TransactionCommand.input_fingerprint",
            lambda: TransactionCommand("command", _key(), "", 0, "policy"),
        ),
        (
            "TransactionCommand.policy_version",
            lambda: TransactionCommand("command", _key(), "fingerprint", 0, ""),
        ),
    ):
        _expect_value_error(factory, field_name)

    key = _key()
    command = _command()
    for immutable, field_name, replacement in (
        (key, "value", "mutated-key"),
        (command, "command_id", "mutated-command"),
    ):
        try:
            setattr(immutable, field_name, replacement)
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError(f"{type(immutable).__name__} is mutable")

    initial = {"count": 0, "nested": {"value": 1}}
    boundary = InMemoryUnitOfWork(initial_state=initial)
    initial["nested"]["value"] = 99

    def mutation(state: dict[str, Any]) -> dict[str, str]:
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    receipt = boundary.execute(command=command, mutation=mutation)
    assert receipt.input_fingerprint == " fingerprint-kept-exactly "
    assert receipt.policy_version == " policy-kept-exactly "
    assert boundary.committed_sequence == 1
    assert boundary.snapshot_state() == {"count": 1, "nested": {"value": 1}}

    try:
        receipt.result_id = "mutated-result"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("AtomicReceipt is mutable")

    returned = boundary.snapshot_state()
    returned["nested"]["value"] = 500
    assert boundary.snapshot_state()["nested"]["value"] == 1

    failing = InMemoryUnitOfWork(
        initial_state={"count": 0},
        repository_ports=(_PrimaryAndRollbackFailureParticipant(),),
    )
    try:
        failing.execute(command=_command(), mutation=mutation)
    except RuntimeError as primary:
        assert str(primary) == "primary participant failure"
        assert any("secondary rollback failure" in note for note in primary.__notes__)
    else:
        raise AssertionError("participant failure did not propagate")
    assert failing.state_version == 0
    assert failing.committed_sequence == 0
    assert failing.snapshot_state() == {"count": 0}
    assert failing.list_receipts() == ()

    print("public_exports=PASS")
    print("immutable_contract_values=PASS")
    print("required_identifier_validation=PASS")
    print("exact_fingerprint_and_policy_retention=PASS")
    print("initial_and_readback_detachment=PASS")
    print("failed_sequence_preservation=PASS")
    print("primary_failure_preservation=PASS")


if __name__ == "__main__":
    main()
