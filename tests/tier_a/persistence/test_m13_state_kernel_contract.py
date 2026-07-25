from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

_FINGERPRINT_A = "a" * 64
_FINGERPRINT_B = "b" * 64


def _contracts() -> tuple[Any, ...]:
    try:
        from nvda_desk.m13_state_kernel import (
            AtomicReceipt,
            IdempotencyConflictError,
            IdempotencyKey,
            InMemoryUnitOfWork,
            RepositoryPort,
            StateVersionConflictError,
            TransactionCommand,
            UnitOfWork,
        )
    except ModuleNotFoundError as exc:
        pytest.fail(f"M13 target package is not implemented: {exc}")
    return (
        AtomicReceipt,
        IdempotencyConflictError,
        IdempotencyKey,
        InMemoryUnitOfWork,
        RepositoryPort,
        StateVersionConflictError,
        TransactionCommand,
        UnitOfWork,
    )


def _key(
    key_type: Any,
    *,
    value: str = "idem-1",
    command_type: str = "position_reconciliation",
    consistency_unit_id: str = "position-1",
) -> Any:
    return key_type(
        value=value,
        command_type=command_type,
        consistency_unit_id=consistency_unit_id,
    )


def _command(
    command_type: Any,
    key_type: Any,
    *,
    key: Any | None = None,
    command_id: str = "command-1",
    fingerprint: str = _FINGERPRINT_A,
    expected_state_version: int = 0,
    policy_version: str = "transaction-v1",
) -> Any:
    return command_type(
        command_id=command_id,
        idempotency_key=key or _key(key_type),
        input_fingerprint=fingerprint,
        expected_state_version=expected_state_version,
        policy_version=policy_version,
    )


def _mutation(*, increment: int = 1, receipt_id: str = "receipt-1", result_id: str = "result-1"):
    def mutate(state: dict[str, Any]) -> dict[str, str]:
        state["count"] += increment
        return {"receipt_id": receipt_id, "result_id": result_id}

    return mutate


def test_m13_exports_the_accepted_public_contract_and_labels_memory_as_non_durable() -> None:
    (
        atomic_receipt,
        _,
        _,
        in_memory_uow,
        repository_port,
        _,
        _,
        unit_of_work,
    ) = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})

    assert isinstance(boundary, unit_of_work)
    assert isinstance(atomic_receipt, type)
    assert isinstance(repository_port, type)
    assert boundary.durability == "non_durable_in_memory"
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()


def test_m13_success_atomically_binds_command_result_state_version_sequence_and_receipt() -> None:
    atomic_receipt, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    key = _key(key_type)
    command = _command(command_type, key_type, key=key)

    receipt = boundary.execute(command=command, mutation=_mutation())

    assert isinstance(receipt, atomic_receipt)
    assert receipt.receipt_id == "receipt-1"
    assert receipt.result_id == "result-1"
    assert receipt.command_id == "command-1"
    assert receipt.command_type == "position_reconciliation"
    assert receipt.consistency_unit_id == "position-1"
    assert receipt.idempotency_key == key
    assert receipt.input_fingerprint == _FINGERPRINT_A
    assert receipt.policy_version == "transaction-v1"
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.sequence == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)


def test_m13_exact_duplicate_returns_original_identity_without_repeating_mutation() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    command = _command(command_type, key_type)
    calls = {"count": 0}

    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    first = boundary.execute(command=command, mutation=mutate)
    second = boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 1
    assert second.receipt_id == first.receipt_id
    assert second.result_id == first.result_id
    assert second.resulting_state_version == first.resulting_state_version == 1
    assert second.sequence == first.sequence == 1
    assert first.duplicate_replay is False
    assert second.duplicate_replay is True
    assert boundary.snapshot_state() == {"count": 1}
    assert len(boundary.list_receipts()) == 1


def test_m13_same_scoped_key_with_different_input_or_command_identity_is_conflict() -> None:
    _, conflict, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    base = _command(command_type, key_type)
    boundary.execute(command=base, mutation=_mutation())

    with pytest.raises(conflict):
        boundary.execute(
            command=_command(
                command_type,
                key_type,
                fingerprint=_FINGERPRINT_B,
                expected_state_version=1,
            ),
            mutation=_mutation(receipt_id="receipt-2", result_id="result-2"),
        )
    with pytest.raises(conflict):
        boundary.execute(
            command=_command(
                command_type,
                key_type,
                command_id="different-command",
                expected_state_version=1,
            ),
            mutation=_mutation(receipt_id="receipt-3", result_id="result-3"),
        )
    with pytest.raises(conflict):
        boundary.execute(
            command=_command(
                command_type,
                key_type,
                expected_state_version=1,
                policy_version="transaction-v2",
            ),
            mutation=_mutation(receipt_id="receipt-4", result_id="result-4"),
        )

    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert len(boundary.list_receipts()) == 1


def test_m13_idempotency_key_is_scoped_by_command_type_and_consistency_unit() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    first = _command(command_type, key_type)
    second_key = _key(key_type, consistency_unit_id="position-2")
    second = _command(
        command_type,
        key_type,
        key=second_key,
        command_id="command-2",
        expected_state_version=1,
    )
    third_key = _key(
        key_type,
        command_type="capital_state_transition",
        consistency_unit_id="position-1",
    )
    third = _command(
        command_type,
        key_type,
        key=third_key,
        command_id="command-3",
        expected_state_version=2,
    )

    boundary.execute(command=first, mutation=_mutation())
    boundary.execute(
        command=second,
        mutation=_mutation(increment=10, receipt_id="receipt-2", result_id="result-2"),
    )
    boundary.execute(
        command=third,
        mutation=_mutation(increment=100, receipt_id="receipt-3", result_id="result-3"),
    )

    assert boundary.state_version == 3
    assert boundary.snapshot_state() == {"count": 111}
    assert [receipt.sequence for receipt in boundary.list_receipts()] == [1, 2, 3]


def test_m13_stale_expected_version_fails_before_mutation_and_emits_no_receipt() -> None:
    _, _, key_type, in_memory_uow, _, state_conflict, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    first = _command(command_type, key_type)
    boundary.execute(command=first, mutation=_mutation())
    calls = {"count": 0}

    def should_not_run(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] = 99
        return {"receipt_id": "receipt-2", "result_id": "result-2"}

    with pytest.raises(state_conflict):
        boundary.execute(
            command=_command(
                command_type,
                key_type,
                key=_key(key_type, value="idem-2"),
                command_id="command-2",
                expected_state_version=0,
            ),
            mutation=should_not_run,
        )

    assert calls["count"] == 0
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert len(boundary.list_receipts()) == 1


def test_m13_mutation_failure_rolls_back_state_version_and_success_receipt() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    command = _command(command_type, key_type)

    def fail_after_mutation(state: dict[str, Any]) -> dict[str, str]:
        state["count"] = 99
        raise RuntimeError("mutation failed")

    with pytest.raises(RuntimeError, match="mutation failed"):
        boundary.execute(command=command, mutation=fail_after_mutation)

    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()


def test_m13_invalid_receipt_result_rolls_back_the_working_state() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()

    for invalid_field in ("receipt_id", "result_id"):
        boundary = in_memory_uow(initial_state={"count": 0})
        command = _command(command_type, key_type)

        def invalid_receipt(state: dict[str, Any]) -> dict[str, str]:
            state["count"] = 99
            result = {"receipt_id": "receipt-1", "result_id": "result-1"}
            result[invalid_field] = ""
            return result

        with pytest.raises((TypeError, ValueError), match="receipt"):
            boundary.execute(command=command, mutation=invalid_receipt)

        assert boundary.state_version == 0
        assert boundary.snapshot_state() == {"count": 0}
        assert boundary.list_receipts() == ()


def test_m13_state_and_receipt_readbacks_are_detached_copies() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    initial = {"count": 0, "nested": {"value": 1}}
    boundary = in_memory_uow(initial_state=initial)
    command = _command(command_type, key_type)
    receipt = boundary.execute(command=command, mutation=_mutation())

    initial["nested"]["value"] = 999
    state = boundary.snapshot_state()
    state["nested"]["value"] = 888
    receipts = list(boundary.list_receipts())
    receipt_copy = deepcopy(receipts[0])

    assert boundary.snapshot_state() == {"count": 1, "nested": {"value": 1}}
    assert receipt_copy == receipt
    assert boundary.list_receipts() == (receipt,)
