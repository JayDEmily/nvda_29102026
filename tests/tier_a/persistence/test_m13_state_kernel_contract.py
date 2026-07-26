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


def _repository_participant(
    repository_port: Any,
    *,
    capture: str,
    fail_on_commit: bool = False,
    failure_message: str = "repository participant commit failed",
) -> Any:
    class Participant(repository_port):
        def __init__(self) -> None:
            self.capture = capture
            self.fail_on_commit = fail_on_commit
            self.failure_message = failure_message
            self.visible: list[Any] = []
            self.prepare_calls = 0
            self.commit_calls = 0
            self.rollback_calls = 0
            self._before: list[Any] | None = None
            self._pending: Any = None

        def prepare(
            self,
            *,
            command: Any,
            working_state: Any,
            receipt: Any,
        ) -> None:
            self.prepare_calls += 1
            self._before = deepcopy(self.visible)
            if self.capture == "state":
                self._pending = {
                    "command_id": command.command_id,
                    "state": deepcopy(working_state),
                    "state_version": receipt.resulting_state_version,
                    "sequence": receipt.sequence,
                }
            elif self.capture == "receipt":
                self._pending = deepcopy(receipt)
            else:
                raise ValueError(f"unsupported participant capture: {self.capture}")

        def commit(self) -> None:
            self.commit_calls += 1
            self.visible.append(deepcopy(self._pending))
            if self.fail_on_commit:
                raise RuntimeError(self.failure_message)

        def rollback(self) -> None:
            self.rollback_calls += 1
            if self._before is not None:
                self.visible = deepcopy(self._before)
            self._pending = None

        # Preserve compatibility with the earlier read-only RepositoryPort shape so
        # the repaired tests still falsify the original six mutants on their own
        # behavioural defects rather than failing during test-fixture construction.
        def snapshot_state(self) -> Any:
            return deepcopy(self.visible)

        def list_receipts(self) -> tuple[Any, ...]:
            return tuple(deepcopy(self.visible))

    return Participant()


def test_m13_receipt_write_failure_rolls_back_every_visible_change_and_allows_clean_retry() -> None:
    _, _, key_type, in_memory_uow, repository_port, _, command_type, _ = _contracts()
    state_participant = _repository_participant(repository_port, capture="state")
    receipt_writer = _repository_participant(
        repository_port,
        capture="receipt",
        fail_on_commit=True,
        failure_message="receipt write failed",
    )
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=(state_participant, receipt_writer),
    )
    command = _command(command_type, key_type)
    calls = {"count": 0}

    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    with pytest.raises(RuntimeError, match="receipt write failed"):
        boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 1
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()
    assert state_participant.visible == []
    assert receipt_writer.visible == []
    assert state_participant.rollback_calls >= 1
    assert receipt_writer.rollback_calls >= 1

    receipt_writer.fail_on_commit = False
    receipt = boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 2
    assert receipt.sequence == 1
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert state_participant.visible == [
        {
            "command_id": "command-1",
            "state": {"count": 1},
            "state_version": 1,
            "sequence": 1,
        }
    ]
    assert receipt_writer.visible == [receipt]


def test_m13_repository_participant_failure_rolls_back_participant_and_internal_truth() -> None:
    _, _, key_type, in_memory_uow, repository_port, _, command_type, _ = _contracts()
    failing_participant = _repository_participant(
        repository_port,
        capture="state",
        fail_on_commit=True,
        failure_message="repository participant failed",
    )
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=(failing_participant,),
    )
    command = _command(command_type, key_type)

    with pytest.raises(RuntimeError, match="repository participant failed"):
        boundary.execute(command=command, mutation=_mutation())

    assert failing_participant.prepare_calls == 1
    assert failing_participant.commit_calls == 1
    assert failing_participant.rollback_calls >= 1
    assert failing_participant.visible == []
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()

    failing_participant.fail_on_commit = False
    receipt = boundary.execute(command=command, mutation=_mutation())

    assert receipt.sequence == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert failing_participant.visible == [
        {
            "command_id": "command-1",
            "state": {"count": 1},
            "state_version": 1,
            "sequence": 1,
        }
    ]


def _prepare_failure_participant(repository_port: Any) -> Any:
    class Participant(repository_port):
        def __init__(self) -> None:
            self.visible: list[Any] = []
            self.pending: Any = None
            self.fail_on_prepare = True
            self.prepare_calls = 0
            self.commit_calls = 0
            self.rollback_calls = 0

        def prepare(
            self,
            *,
            command: Any,
            working_state: Any,
            receipt: Any,
        ) -> None:
            self.prepare_calls += 1
            if self.pending is not None:
                raise RuntimeError("stale pending transaction survived failed prepare")
            self.pending = {
                "command_id": command.command_id,
                "state": deepcopy(working_state),
                "state_version": receipt.resulting_state_version,
                "sequence": receipt.sequence,
            }
            if self.fail_on_prepare:
                raise RuntimeError("participant prepare failed")

        def commit(self) -> None:
            self.commit_calls += 1
            self.visible.append(deepcopy(self.pending))
            self.pending = None

        def rollback(self) -> None:
            self.rollback_calls += 1
            self.pending = None

        def snapshot_state(self) -> Any:
            return deepcopy(self.visible)

        def list_receipts(self) -> tuple[Any, ...]:
            return ()

    return Participant()


def test_m13_prepare_failure_rolls_back_failing_participant_and_allows_uncontaminated_retry() -> None:
    _, _, key_type, in_memory_uow, repository_port, _, command_type, _ = _contracts()
    participant = _prepare_failure_participant(repository_port)
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=(participant,),
    )
    command = _command(command_type, key_type)
    calls = {"count": 0}

    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    with pytest.raises(RuntimeError, match="participant prepare failed"):
        boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 1
    assert participant.prepare_calls == 1
    assert participant.commit_calls == 0
    assert participant.rollback_calls >= 1
    assert participant.pending is None
    assert participant.visible == []
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()

    participant.fail_on_prepare = False
    receipt = boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 2
    assert participant.prepare_calls == 2
    assert participant.commit_calls == 1
    assert participant.rollback_calls >= 1
    assert participant.pending is None
    assert receipt.sequence == 1
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert participant.visible == [
        {
            "command_id": "command-1",
            "state": {"count": 1},
            "state_version": 1,
            "sequence": 1,
        }
    ]


def test_m13_later_prepare_failure_rolls_back_every_prepared_participant_and_allows_clean_retry() -> None:
    _, _, key_type, in_memory_uow, repository_port, _, command_type, _ = _contracts()
    participant_a = _prepare_failure_participant(repository_port)
    participant_a.fail_on_prepare = False
    participant_b = _prepare_failure_participant(repository_port)
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=(participant_a, participant_b),
    )
    command = _command(command_type, key_type)
    calls = {"count": 0}

    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-1", "result_id": "result-1"}

    with pytest.raises(RuntimeError, match="participant prepare failed"):
        boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 1
    assert participant_a.prepare_calls == 1
    assert participant_b.prepare_calls == 1
    assert participant_a.commit_calls == 0
    assert participant_b.commit_calls == 0
    assert participant_a.rollback_calls >= 1
    assert participant_b.rollback_calls >= 1
    assert participant_a.pending is None
    assert participant_b.pending is None
    assert participant_a.visible == []
    assert participant_b.visible == []
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()

    participant_b.fail_on_prepare = False
    receipt = boundary.execute(command=command, mutation=mutate)

    assert calls["count"] == 2
    assert participant_a.prepare_calls == 2
    assert participant_b.prepare_calls == 2
    assert participant_a.commit_calls == 1
    assert participant_b.commit_calls == 1
    assert participant_a.pending is None
    assert participant_b.pending is None
    assert receipt.sequence == 1
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    expected_visible = [
        {
            "command_id": "command-1",
            "state": {"count": 1},
            "state_version": 1,
            "sequence": 1,
        }
    ]
    assert participant_a.visible == expected_visible
    assert participant_b.visible == expected_visible


def test_m13_failed_transaction_does_not_bind_idempotency_key_and_fresh_reuse_commits_once() -> None:
    _, _, key_type, in_memory_uow, repository_port, _, command_type, _ = _contracts()
    participant = _prepare_failure_participant(repository_port)
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=(participant,),
    )
    shared_key = _key(key_type)
    failed_command = _command(command_type, key_type, key=shared_key)
    fresh_command = _command(
        command_type,
        key_type,
        key=shared_key,
        command_id="command-2",
        fingerprint=_FINGERPRINT_B,
        expected_state_version=0,
    )
    calls = {"count": 0}

    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-2", "result_id": "result-2"}

    with pytest.raises(RuntimeError, match="participant prepare failed"):
        boundary.execute(command=failed_command, mutation=mutate)

    assert calls["count"] == 1
    assert participant.rollback_calls >= 1
    assert participant.pending is None
    assert participant.visible == []
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()

    participant.fail_on_prepare = False
    receipt = boundary.execute(command=fresh_command, mutation=mutate)

    assert calls["count"] == 2
    assert receipt.command_id == "command-2"
    assert receipt.input_fingerprint == _FINGERPRINT_B
    assert receipt.sequence == 1
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert participant.pending is None
    assert participant.visible == [
        {
            "command_id": "command-2",
            "state": {"count": 1},
            "state_version": 1,
            "sequence": 1,
        }
    ]

    replay = boundary.execute(command=fresh_command, mutation=mutate)

    assert calls["count"] == 2
    assert replay.receipt_id == receipt.receipt_id
    assert replay.result_id == receipt.result_id
    assert replay.sequence == receipt.sequence == 1
    assert replay.resulting_state_version == receipt.resulting_state_version == 1
    assert replay.duplicate_replay is True
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert len(participant.visible) == 1


def _matrix_participant(
    repository_port: Any,
    *,
    name: str,
    role: str,
    fail_phase: str | None = None,
) -> Any:
    class Participant(repository_port):
        def __init__(self) -> None:
            self.name = name
            self.role = role
            self.fail_phase = fail_phase
            self.pending: dict[str, Any] | None = None
            self.visible: list[dict[str, Any]] = []
            self.prepare_calls = 0
            self.commit_calls = 0
            self.rollback_calls = 0
            self._visible_before: list[dict[str, Any]] = []

        def prepare(self, *, command: Any, working_state: Any, receipt: Any) -> None:
            self.prepare_calls += 1
            self._visible_before = deepcopy(self.visible)
            self.pending = {
                "role": self.role,
                "command_id": command.command_id,
                "input_fingerprint": command.input_fingerprint,
                "policy_version": command.policy_version,
                "state": deepcopy(working_state),
                "state_version": receipt.resulting_state_version,
                "sequence": receipt.sequence,
                "receipt_id": receipt.receipt_id,
            }
            if self.fail_phase == "prepare":
                raise RuntimeError(f"{self.name} prepare failed")

        def commit(self) -> None:
            self.commit_calls += 1
            assert self.pending is not None
            self.visible.append(deepcopy(self.pending))
            if self.fail_phase == "commit":
                raise RuntimeError(f"{self.name} commit failed")
            self.pending = None

        def rollback(self) -> None:
            self.rollback_calls += 1
            self.visible = deepcopy(self._visible_before)
            self.pending = None

    return Participant()


_M13_FAILURE_BINDING_MATRIX = (
    pytest.param(
        "stale_expected_state_version",
        "same_command_id_different_fingerprint",
        id="stale-expected-state-version--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "stale_expected_state_version",
        "different_command_id_same_fingerprint",
        id="stale-expected-state-version--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "stale_expected_state_version",
        "same_command_id_fingerprint_different_policy_version",
        id="stale-expected-state-version--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "stale_expected_state_version",
        "complete_command_identity",
        id="stale-expected-state-version--complete-command-identity-corrected-version",
    ),
    pytest.param(
        "owner_mutation_exception",
        "same_command_id_different_fingerprint",
        id="owner-mutation-exception--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "owner_mutation_exception",
        "different_command_id_same_fingerprint",
        id="owner-mutation-exception--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "owner_mutation_exception",
        "same_command_id_fingerprint_different_policy_version",
        id="owner-mutation-exception--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "owner_mutation_exception",
        "complete_command_identity",
        id="owner-mutation-exception--complete-command-identity",
    ),
    pytest.param(
        "invalid_mutation_result_mapping",
        "same_command_id_different_fingerprint",
        id="invalid-mutation-result-mapping--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "invalid_mutation_result_mapping",
        "different_command_id_same_fingerprint",
        id="invalid-mutation-result-mapping--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "invalid_mutation_result_mapping",
        "same_command_id_fingerprint_different_policy_version",
        id="invalid-mutation-result-mapping--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "invalid_mutation_result_mapping",
        "complete_command_identity",
        id="invalid-mutation-result-mapping--complete-command-identity",
    ),
    pytest.param(
        "invalid_or_empty_receipt_id",
        "same_command_id_different_fingerprint",
        id="invalid-or-empty-receipt-id--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "invalid_or_empty_receipt_id",
        "different_command_id_same_fingerprint",
        id="invalid-or-empty-receipt-id--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "invalid_or_empty_receipt_id",
        "same_command_id_fingerprint_different_policy_version",
        id="invalid-or-empty-receipt-id--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "invalid_or_empty_receipt_id",
        "complete_command_identity",
        id="invalid-or-empty-receipt-id--complete-command-identity",
    ),
    pytest.param(
        "invalid_or_empty_result_id",
        "same_command_id_different_fingerprint",
        id="invalid-or-empty-result-id--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "invalid_or_empty_result_id",
        "different_command_id_same_fingerprint",
        id="invalid-or-empty-result-id--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "invalid_or_empty_result_id",
        "same_command_id_fingerprint_different_policy_version",
        id="invalid-or-empty-result-id--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "invalid_or_empty_result_id",
        "complete_command_identity",
        id="invalid-or-empty-result-id--complete-command-identity",
    ),
    pytest.param(
        "repository_participant_prepare_failure",
        "same_command_id_different_fingerprint",
        id="repository-participant-prepare-failure--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "repository_participant_prepare_failure",
        "different_command_id_same_fingerprint",
        id="repository-participant-prepare-failure--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "repository_participant_prepare_failure",
        "same_command_id_fingerprint_different_policy_version",
        id="repository-participant-prepare-failure--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "repository_participant_prepare_failure",
        "complete_command_identity",
        id="repository-participant-prepare-failure--complete-command-identity",
    ),
    pytest.param(
        "repository_participant_commit_failure",
        "same_command_id_different_fingerprint",
        id="repository-participant-commit-failure--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "repository_participant_commit_failure",
        "different_command_id_same_fingerprint",
        id="repository-participant-commit-failure--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "repository_participant_commit_failure",
        "same_command_id_fingerprint_different_policy_version",
        id="repository-participant-commit-failure--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "repository_participant_commit_failure",
        "complete_command_identity",
        id="repository-participant-commit-failure--complete-command-identity",
    ),
    pytest.param(
        "attesting_receipt_writer_failure",
        "same_command_id_different_fingerprint",
        id="attesting-receipt-writer-failure--same-command-id-different-fingerprint",
    ),
    pytest.param(
        "attesting_receipt_writer_failure",
        "different_command_id_same_fingerprint",
        id="attesting-receipt-writer-failure--different-command-id-same-fingerprint",
    ),
    pytest.param(
        "attesting_receipt_writer_failure",
        "same_command_id_fingerprint_different_policy_version",
        id="attesting-receipt-writer-failure--same-command-id-fingerprint-different-policy-version",
    ),
    pytest.param(
        "attesting_receipt_writer_failure",
        "complete_command_identity",
        id="attesting-receipt-writer-failure--complete-command-identity",
    ),
)


@pytest.mark.parametrize("failure_boundary,identity_dimension", _M13_FAILURE_BINDING_MATRIX)
def test_m13_unsuccessful_execute_attempt_leaves_no_binding_matrix(
    failure_boundary: str,
    identity_dimension: str,
) -> None:
    (
        _,
        _,
        key_type,
        in_memory_uow,
        repository_port,
        state_version_conflict,
        command_type,
        _,
    ) = _contracts()
    participant_a = _matrix_participant(
        repository_port,
        name="participant-a",
        role="state-participant",
    )
    participant_b = _matrix_participant(
        repository_port,
        name="participant-b",
        role="state-participant",
        fail_phase=(
            "prepare"
            if failure_boundary == "repository_participant_prepare_failure"
            else "commit"
            if failure_boundary == "repository_participant_commit_failure"
            else None
        ),
    )
    receipt_writer = _matrix_participant(
        repository_port,
        name="attesting-receipt-writer",
        role="attesting-receipt-writer",
        fail_phase="commit" if failure_boundary == "attesting_receipt_writer_failure" else None,
    )
    participants = (participant_a, participant_b, receipt_writer)
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=participants,
    )
    shared_key = _key(key_type)
    failed_command = _command(
        command_type,
        key_type,
        key=shared_key,
        command_id="command-failed",
        fingerprint=_FINGERPRINT_A,
        expected_state_version=1 if failure_boundary == "stale_expected_state_version" else 0,
        policy_version="transaction-v1",
    )
    corrected_identity = {
        "command_id": failed_command.command_id,
        "fingerprint": failed_command.input_fingerprint,
        "policy_version": failed_command.policy_version,
    }
    if identity_dimension == "same_command_id_different_fingerprint":
        corrected_identity["fingerprint"] = _FINGERPRINT_B
    elif identity_dimension == "different_command_id_same_fingerprint":
        corrected_identity["command_id"] = "command-corrected"
    elif identity_dimension == "same_command_id_fingerprint_different_policy_version":
        corrected_identity["policy_version"] = "transaction-v2"
    else:
        assert identity_dimension == "complete_command_identity"
    corrected_command = _command(
        command_type,
        key_type,
        key=shared_key,
        command_id=corrected_identity["command_id"],
        fingerprint=corrected_identity["fingerprint"],
        expected_state_version=0,
        policy_version=corrected_identity["policy_version"],
    )
    calls = {"count": 0}

    def attempted_mutation(state: dict[str, Any]) -> Any:
        calls["count"] += 1
        state["count"] += 1
        if failure_boundary == "owner_mutation_exception":
            raise RuntimeError("matrix owner mutation failed")
        if failure_boundary == "invalid_mutation_result_mapping":
            return ["not", "a", "mapping"]
        if failure_boundary == "invalid_or_empty_receipt_id":
            return {"receipt_id": "", "result_id": "failed-result"}
        if failure_boundary == "invalid_or_empty_result_id":
            return {"receipt_id": "failed-receipt", "result_id": ""}
        return {"receipt_id": "failed-receipt", "result_id": "failed-result"}

    if failure_boundary == "stale_expected_state_version":
        failure_type: Any = state_version_conflict
        failure_message = "stale expected state version"
    elif failure_boundary == "owner_mutation_exception":
        failure_type = RuntimeError
        failure_message = "matrix owner mutation failed"
    elif failure_boundary == "invalid_mutation_result_mapping":
        failure_type = TypeError
        failure_message = "mapping"
    elif failure_boundary == "invalid_or_empty_receipt_id":
        failure_type = ValueError
        failure_message = "receipt_id"
    elif failure_boundary == "invalid_or_empty_result_id":
        failure_type = ValueError
        failure_message = "result_id"
    elif failure_boundary == "repository_participant_prepare_failure":
        failure_type = RuntimeError
        failure_message = "participant-b prepare failed"
    elif failure_boundary == "repository_participant_commit_failure":
        failure_type = RuntimeError
        failure_message = "participant-b commit failed"
    else:
        assert failure_boundary == "attesting_receipt_writer_failure"
        failure_type = RuntimeError
        failure_message = "attesting-receipt-writer commit failed"

    with pytest.raises(failure_type, match=failure_message):
        boundary.execute(command=failed_command, mutation=attempted_mutation)

    expected_failed_calls = 0 if failure_boundary == "stale_expected_state_version" else 1
    assert calls["count"] == expected_failed_calls
    assert boundary.state_version == 0
    assert boundary.snapshot_state() == {"count": 0}
    assert boundary.list_receipts() == ()
    for participant in participants:
        assert participant.pending is None
        assert participant.visible == []

    for participant in participants:
        participant.fail_phase = None

    def corrected_mutation(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "corrected-receipt", "result_id": "corrected-result"}

    receipt = boundary.execute(command=corrected_command, mutation=corrected_mutation)

    assert calls["count"] == expected_failed_calls + 1
    assert receipt.command_id == corrected_command.command_id
    assert receipt.input_fingerprint == corrected_command.input_fingerprint
    assert receipt.policy_version == corrected_command.policy_version
    assert receipt.sequence == 1
    assert receipt.prior_state_version == 0
    assert receipt.resulting_state_version == 1
    assert receipt.duplicate_replay is False
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    expected_participant_truth = {
        "command_id": corrected_command.command_id,
        "input_fingerprint": corrected_command.input_fingerprint,
        "policy_version": corrected_command.policy_version,
        "state": {"count": 1},
        "state_version": 1,
        "sequence": 1,
        "receipt_id": "corrected-receipt",
    }
    for participant in participants:
        assert participant.pending is None
        assert participant.visible == [
            {
                "role": participant.role,
                **expected_participant_truth,
            }
        ]

    participant_counts = tuple(
        (participant.prepare_calls, participant.commit_calls, participant.rollback_calls)
        for participant in participants
    )
    replay = boundary.execute(command=corrected_command, mutation=corrected_mutation)

    assert calls["count"] == expected_failed_calls + 1
    assert replay.receipt_id == receipt.receipt_id == "corrected-receipt"
    assert replay.result_id == receipt.result_id == "corrected-result"
    assert replay.sequence == receipt.sequence == 1
    assert replay.resulting_state_version == receipt.resulting_state_version == 1
    assert replay.duplicate_replay is True
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}
    assert boundary.list_receipts() == (receipt,)
    assert participant_counts == tuple(
        (participant.prepare_calls, participant.commit_calls, participant.rollback_calls)
        for participant in participants
    )
    for participant in participants:
        assert participant.pending is None
        assert len(participant.visible) == 1
