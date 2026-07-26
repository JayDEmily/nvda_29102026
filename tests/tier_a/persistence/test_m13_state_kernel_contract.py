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


def test_m13_prepare_failure_rolls_back_failing_participant_and_allows_uncontaminated_retry() -> (
    None
):
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


def test_m13_later_prepare_failure_rolls_back_every_prepared_participant_and_allows_clean_retry() -> (
    None
):
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


def test_m13_failed_transaction_does_not_bind_idempotency_key_and_fresh_reuse_commits_once() -> (
    None
):
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
            else "commit" if failure_boundary == "repository_participant_commit_failure" else None
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


_M13_V6_REENTRANT_PHASES = (
    "owner_mutation",
    "participant_prepare",
    "participant_commit",
    "participant_rollback",
    "attesting_receipt_writer",
)
_M13_V6_NESTED_SCOPE_RELATIONSHIPS = (
    "same_scoped_idempotency_key",
    "different_key_same_command_type_and_unit",
    "different_consistency_unit",
    "different_command_type",
)
_M13_V6_REENTRANT_MATRIX = tuple(
    pytest.param(
        phase,
        scope_relationship,
        outer_outcome,
        id=(
            f"phase-{phase.replace('_', '-')}--"
            f"scope-{scope_relationship.replace('_', '-')}--"
            f"outer-{outer_outcome.replace('_', '-')}--"
            "nested-runtime-rejection"
        ),
    )
    for phase in _M13_V6_REENTRANT_PHASES
    for scope_relationship in _M13_V6_NESTED_SCOPE_RELATIONSHIPS
    for outer_outcome in (
        ("outer_fails_primary",)
        if phase == "participant_rollback"
        else ("outer_commits_caught", "outer_fails_unhandled")
    )
)


def _v6_nested_command(
    command_type: Any,
    key_type: Any,
    *,
    outer_key: Any,
    scope_relationship: str,
    expected_state_version: int,
) -> Any:
    if scope_relationship == "same_scoped_idempotency_key":
        nested_key = outer_key
    elif scope_relationship == "different_key_same_command_type_and_unit":
        nested_key = _key(
            key_type,
            value="idem-nested",
            command_type=outer_key.command_type,
            consistency_unit_id=outer_key.consistency_unit_id,
        )
    elif scope_relationship == "different_consistency_unit":
        nested_key = _key(
            key_type,
            value=outer_key.value,
            command_type=outer_key.command_type,
            consistency_unit_id="position-nested",
        )
    else:
        assert scope_relationship == "different_command_type"
        nested_key = _key(
            key_type,
            value=outer_key.value,
            command_type="capital_state_transition",
            consistency_unit_id=outer_key.consistency_unit_id,
        )
    return _command(
        command_type,
        key_type,
        key=nested_key,
        command_id="command-nested",
        fingerprint=_FINGERPRINT_B,
        expected_state_version=expected_state_version,
        policy_version="transaction-v2",
    )


def _v6_reentrant_participant(
    repository_port: Any,
    *,
    callback_phase: str,
    outer_outcome: str,
) -> Any:
    class Participant(repository_port):
        def __init__(self) -> None:
            self.boundary: Any = None
            self.nested_command: Any = None
            self.callback_phase = callback_phase
            self.outer_outcome = outer_outcome
            self.armed = True
            self.pending: dict[str, Any] | None = None
            self.visible: list[dict[str, Any]] = []
            self._visible_before: list[dict[str, Any]] = []
            self.prepare_calls = 0
            self.commit_calls = 0
            self.rollback_calls = 0
            self.nested_mutation_calls = 0
            self.nested_returns = 0
            self.nested_errors: list[BaseException] = []

        def _attempt_nested(self) -> None:
            if not self.armed:
                return
            self.armed = False

            def nested_mutation(state: dict[str, Any]) -> dict[str, str]:
                self.nested_mutation_calls += 1
                state["nested"] += 1
                return {
                    "receipt_id": "receipt-nested",
                    "result_id": "result-nested",
                }

            try:
                self.boundary.execute(
                    command=self.nested_command,
                    mutation=nested_mutation,
                )
            except BaseException as exc:
                self.nested_errors.append(exc)
                if self.outer_outcome == "outer_fails_unhandled":
                    raise
            else:
                self.nested_returns += 1

        def prepare(self, *, command: Any, working_state: Any, receipt: Any) -> None:
            self.prepare_calls += 1
            self._visible_before = deepcopy(self.visible)
            self.pending = {
                "command_id": command.command_id,
                "state": deepcopy(working_state),
                "receipt_id": receipt.receipt_id,
                "sequence": receipt.sequence,
                "state_version": receipt.resulting_state_version,
            }
            if self.callback_phase == "participant_prepare":
                self._attempt_nested()
            if self.callback_phase == "participant_rollback":
                raise RuntimeError("outer rollback trigger")

        def commit(self) -> None:
            self.commit_calls += 1
            assert self.pending is not None
            self.visible.append(deepcopy(self.pending))
            if self.callback_phase in ("participant_commit", "attesting_receipt_writer"):
                self._attempt_nested()
            self.pending = None

        def rollback(self) -> None:
            self.rollback_calls += 1
            self.visible = deepcopy(self._visible_before)
            self.pending = None
            if self.callback_phase == "participant_rollback":
                self._attempt_nested()

    return Participant()


@pytest.mark.parametrize(
    "phase,scope_relationship,outer_outcome",
    _M13_V6_REENTRANT_MATRIX,
)
def test_m13_v6_single_active_attempt_excludes_nested_execute_matrix(
    phase: str,
    scope_relationship: str,
    outer_outcome: str,
) -> None:
    (
        _,
        _,
        key_type,
        in_memory_uow,
        repository_port,
        _,
        command_type,
        _,
    ) = _contracts()
    participant_phase = "participant_commit" if phase == "attesting_receipt_writer" else phase
    participant = _v6_reentrant_participant(
        repository_port,
        callback_phase=participant_phase,
        outer_outcome=outer_outcome,
    )
    boundary = in_memory_uow(
        initial_state={"outer": 0, "nested": 0},
        repository_ports=(participant,),
    )
    participant.boundary = boundary
    outer_key = _key(key_type, value="idem-outer")
    outer_command = _command(
        command_type,
        key_type,
        key=outer_key,
        command_id="command-outer",
    )
    nested_command = _v6_nested_command(
        command_type,
        key_type,
        outer_key=outer_key,
        scope_relationship=scope_relationship,
        expected_state_version=0,
    )
    participant.nested_command = nested_command
    owner_attempted = {"value": False}

    def outer_mutation(state: dict[str, Any]) -> dict[str, str]:
        state["outer"] += 1
        if phase == "owner_mutation":
            owner_attempted["value"] = True
            participant._attempt_nested()
        return {"receipt_id": "receipt-outer", "result_id": "result-outer"}

    outer_commits = outer_outcome == "outer_commits_caught"
    if outer_commits:
        outer_receipt = boundary.execute(
            command=outer_command,
            mutation=outer_mutation,
        )
        assert outer_receipt.receipt_id == "receipt-outer"
        assert outer_receipt.sequence == 1
        assert outer_receipt.prior_state_version == 0
        assert outer_receipt.resulting_state_version == 1
        assert boundary.state_version == 1
        assert boundary.snapshot_state() == {"outer": 1, "nested": 0}
        assert boundary.list_receipts() == (outer_receipt,)
        assert participant.visible == [
            {
                "command_id": "command-outer",
                "state": {"outer": 1, "nested": 0},
                "receipt_id": "receipt-outer",
                "sequence": 1,
                "state_version": 1,
            }
        ]
    else:
        expected_message = "outer rollback trigger" if phase == "participant_rollback" else None
        if expected_message is None:
            with pytest.raises(RuntimeError):
                boundary.execute(
                    command=outer_command,
                    mutation=outer_mutation,
                )
        else:
            with pytest.raises(RuntimeError, match=expected_message):
                boundary.execute(
                    command=outer_command,
                    mutation=outer_mutation,
                )
        assert boundary.state_version == 0
        assert boundary.snapshot_state() == {"outer": 0, "nested": 0}
        assert boundary.list_receipts() == ()
        assert participant.visible == []

    assert participant.nested_returns == 0
    assert participant.nested_mutation_calls == 0
    assert len(participant.nested_errors) == 1
    assert type(participant.nested_errors[0]) is RuntimeError
    assert participant.pending is None
    if phase == "owner_mutation":
        assert owner_attempted["value"] is True

    participant.callback_phase = "disabled"
    corrected_nested = _v6_nested_command(
        command_type,
        key_type,
        outer_key=outer_key,
        scope_relationship=scope_relationship,
        expected_state_version=boundary.state_version,
    )
    if outer_commits and scope_relationship == "same_scoped_idempotency_key":
        replay_calls = {"count": 0}

        def replay_mutation(state: dict[str, Any]) -> dict[str, str]:
            replay_calls["count"] += 1
            return {"receipt_id": "wrong", "result_id": "wrong"}

        replay = boundary.execute(command=outer_command, mutation=replay_mutation)
        assert replay_calls["count"] == 0
        assert replay.receipt_id == "receipt-outer"
        assert replay.sequence == 1
        assert replay.duplicate_replay is True
        assert len(boundary.list_receipts()) == 1
    else:
        later_calls = {"count": 0}

        def later_mutation(state: dict[str, Any]) -> dict[str, str]:
            later_calls["count"] += 1
            state["nested"] += 1
            return {"receipt_id": "receipt-later", "result_id": "result-later"}

        later = boundary.execute(
            command=corrected_nested,
            mutation=later_mutation,
        )
        expected_sequence = 2 if outer_commits else 1
        assert later_calls["count"] == 1
        assert later.sequence == expected_sequence
        assert later.prior_state_version == expected_sequence - 1
        assert later.resulting_state_version == expected_sequence
        assert boundary.state_version == expected_sequence
        assert len(boundary.list_receipts()) == expected_sequence
        assert boundary.snapshot_state()["nested"] == 1


_M13_V6_ACTIVE_LIFECYCLE_MATRIX = (
    pytest.param("successful_commit", id="terminal-successful-commit--fresh-admitted"),
    pytest.param("exact_duplicate_replay", id="terminal-exact-duplicate-replay--fresh-admitted"),
    pytest.param("stale_version", id="terminal-stale-version-rejection--fresh-admitted"),
    pytest.param("mutation_exception", id="terminal-mutation-exception--fresh-admitted"),
    pytest.param(
        "non_mapping_mutation_result",
        id="terminal-non-mapping-mutation-result--fresh-admitted",
    ),
    pytest.param("invalid_receipt_id", id="terminal-invalid-receipt-id--fresh-admitted"),
    pytest.param("invalid_result_id", id="terminal-invalid-result-id--fresh-admitted"),
    pytest.param(
        "participant_prepare_failure",
        id="terminal-participant-prepare-failure--fresh-admitted",
    ),
    pytest.param(
        "participant_commit_failure",
        id="terminal-participant-commit-failure--fresh-admitted",
    ),
    pytest.param(
        "receipt_writer_failure",
        id="terminal-receipt-writer-failure--fresh-admitted",
    ),
    pytest.param(
        "nested_execution_rejection",
        id="terminal-nested-execution-rejection--fresh-admitted",
    ),
)


@pytest.mark.parametrize("terminal_outcome", _M13_V6_ACTIVE_LIFECYCLE_MATRIX)
def test_m13_v6_active_attempt_state_clears_after_every_terminal_outcome(
    terminal_outcome: str,
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
            if terminal_outcome == "participant_prepare_failure"
            else "commit" if terminal_outcome == "participant_commit_failure" else None
        ),
    )
    receipt_writer = _matrix_participant(
        repository_port,
        name="attesting-receipt-writer",
        role="attesting-receipt-writer",
        fail_phase="commit" if terminal_outcome == "receipt_writer_failure" else None,
    )
    participants = (participant_a, participant_b, receipt_writer)
    boundary = in_memory_uow(
        initial_state={"count": 0},
        repository_ports=participants,
    )
    attempted_key = _key(key_type, value="idem-attempt")
    attempted_command = _command(
        command_type,
        key_type,
        key=attempted_key,
        command_id="command-attempt",
        expected_state_version=1 if terminal_outcome == "stale_version" else 0,
    )
    mutation_calls = {"count": 0}

    def attempted_mutation(state: dict[str, Any]) -> Any:
        mutation_calls["count"] += 1
        state["count"] += 1
        if terminal_outcome == "mutation_exception":
            raise RuntimeError("lifecycle mutation failed")
        if terminal_outcome == "non_mapping_mutation_result":
            return ("not", "a", "mapping")
        if terminal_outcome == "invalid_receipt_id":
            return {"receipt_id": "", "result_id": "result-attempt"}
        if terminal_outcome == "invalid_result_id":
            return {"receipt_id": "receipt-attempt", "result_id": ""}
        if terminal_outcome == "nested_execution_rejection":
            nested_command = _command(
                command_type,
                key_type,
                key=_key(key_type, value="idem-nested-lifecycle"),
                command_id="command-nested-lifecycle",
                fingerprint=_FINGERPRINT_B,
                expected_state_version=0,
            )
            boundary.execute(
                command=nested_command,
                mutation=_mutation(
                    receipt_id="receipt-nested-lifecycle",
                    result_id="result-nested-lifecycle",
                ),
            )
        return {"receipt_id": "receipt-attempt", "result_id": "result-attempt"}

    committed_before_fresh = terminal_outcome in (
        "successful_commit",
        "exact_duplicate_replay",
    )
    if terminal_outcome == "successful_commit":
        first = boundary.execute(
            command=attempted_command,
            mutation=attempted_mutation,
        )
        assert first.sequence == 1
    elif terminal_outcome == "exact_duplicate_replay":
        first = boundary.execute(
            command=attempted_command,
            mutation=attempted_mutation,
        )
        replay = boundary.execute(
            command=attempted_command,
            mutation=attempted_mutation,
        )
        assert replay.receipt_id == first.receipt_id
        assert replay.duplicate_replay is True
        assert mutation_calls["count"] == 1
    elif terminal_outcome == "stale_version":
        with pytest.raises(state_version_conflict, match="stale expected state version"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "mutation_exception":
        with pytest.raises(RuntimeError, match="lifecycle mutation failed"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "non_mapping_mutation_result":
        with pytest.raises(TypeError, match="mapping"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "invalid_receipt_id":
        with pytest.raises(ValueError, match="receipt_id"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "invalid_result_id":
        with pytest.raises(ValueError, match="result_id"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "participant_prepare_failure":
        with pytest.raises(RuntimeError, match="participant-b prepare failed"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "participant_commit_failure":
        with pytest.raises(RuntimeError, match="participant-b commit failed"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    elif terminal_outcome == "receipt_writer_failure":
        with pytest.raises(RuntimeError, match="attesting-receipt-writer commit failed"):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )
    else:
        assert terminal_outcome == "nested_execution_rejection"
        with pytest.raises(RuntimeError):
            boundary.execute(
                command=attempted_command,
                mutation=attempted_mutation,
            )

    expected_commits = 1 if committed_before_fresh else 0
    assert boundary.state_version == expected_commits
    assert len(boundary.list_receipts()) == expected_commits
    assert boundary.snapshot_state() == {"count": expected_commits}
    for participant in participants:
        assert participant.pending is None
        assert len(participant.visible) == expected_commits

    participant_b.fail_phase = None
    receipt_writer.fail_phase = None
    fresh_key = _key(key_type, value="idem-fresh") if committed_before_fresh else attempted_key
    fresh_command = _command(
        command_type,
        key_type,
        key=fresh_key,
        command_id="command-fresh",
        fingerprint=_FINGERPRINT_B,
        expected_state_version=expected_commits,
        policy_version="transaction-v2",
    )
    fresh_calls = {"count": 0}

    def fresh_mutation(state: dict[str, Any]) -> dict[str, str]:
        fresh_calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-fresh", "result_id": "result-fresh"}

    fresh = boundary.execute(command=fresh_command, mutation=fresh_mutation)
    expected_next = expected_commits + 1
    assert fresh_calls["count"] == 1
    assert fresh.sequence == expected_next
    assert fresh.prior_state_version == expected_commits
    assert fresh.resulting_state_version == expected_next
    assert boundary.state_version == expected_next
    assert len(boundary.list_receipts()) == expected_next
    assert boundary.snapshot_state() == {"count": expected_next}
    for participant in participants:
        assert participant.pending is None
        assert len(participant.visible) == expected_next

    participant_counts = tuple(
        (item.prepare_calls, item.commit_calls, item.rollback_calls) for item in participants
    )
    fresh_replay = boundary.execute(
        command=fresh_command,
        mutation=fresh_mutation,
    )
    assert fresh_calls["count"] == 1
    assert fresh_replay.receipt_id == fresh.receipt_id == "receipt-fresh"
    assert fresh_replay.result_id == fresh.result_id == "result-fresh"
    assert fresh_replay.sequence == fresh.sequence == expected_next
    assert fresh_replay.prior_state_version == fresh.prior_state_version
    assert fresh_replay.resulting_state_version == fresh.resulting_state_version
    assert fresh_replay.duplicate_replay is True
    assert boundary.state_version == expected_next
    assert len(boundary.list_receipts()) == expected_next
    assert participant_counts == tuple(
        (item.prepare_calls, item.commit_calls, item.rollback_calls) for item in participants
    )


class _V6CoercibleNumeric:
    def __int__(self) -> int:
        return 1


_M13_V6_INVALID_TYPE_ERRORS = (TypeError, ValueError)
_M13_V6_INVALID_RECEIPT_MATRIX = (
    pytest.param(
        {"command_type": "different-command-type"},
        ValueError,
        id="scope-command-type-mismatches-embedded-key",
    ),
    pytest.param(
        {"consistency_unit_id": "different-consistency-unit"},
        ValueError,
        id="scope-consistency-unit-mismatches-embedded-key",
    ),
    pytest.param(
        {"prior_state_version": True},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="prior-state-version-bool-is-not-exact-int",
    ),
    pytest.param(
        {"prior_state_version": 0.0},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="prior-state-version-float-is-not-exact-int",
    ),
    pytest.param(
        {"prior_state_version": "0"},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="prior-state-version-string-is-not-exact-int",
    ),
    pytest.param(
        {"prior_state_version": _V6CoercibleNumeric()},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="prior-state-version-coercible-numeric-is-not-exact-int",
    ),
    pytest.param(
        {"resulting_state_version": True},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="resulting-state-version-bool-is-not-exact-int",
    ),
    pytest.param(
        {"resulting_state_version": 1.0},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="resulting-state-version-float-is-not-exact-int",
    ),
    pytest.param(
        {"resulting_state_version": "1"},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="resulting-state-version-string-is-not-exact-int",
    ),
    pytest.param(
        {"resulting_state_version": _V6CoercibleNumeric()},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="resulting-state-version-coercible-numeric-is-not-exact-int",
    ),
    pytest.param(
        {"sequence": True},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="sequence-bool-is-not-exact-int",
    ),
    pytest.param(
        {"sequence": 1.0},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="sequence-float-is-not-exact-int",
    ),
    pytest.param(
        {"sequence": "1"},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="sequence-string-is-not-exact-int",
    ),
    pytest.param(
        {"sequence": _V6CoercibleNumeric()},
        _M13_V6_INVALID_TYPE_ERRORS,
        id="sequence-coercible-numeric-is-not-exact-int",
    ),
    pytest.param(
        {"prior_state_version": -1, "resulting_state_version": 0},
        ValueError,
        id="prior-state-version-negative",
    ),
    pytest.param(
        {"resulting_state_version": 0},
        ValueError,
        id="resulting-state-version-zero",
    ),
    pytest.param(
        {"resulting_state_version": -1},
        ValueError,
        id="resulting-state-version-negative",
    ),
    pytest.param(
        {"prior_state_version": 1, "resulting_state_version": 1},
        ValueError,
        id="resulting-state-version-equals-prior",
    ),
    pytest.param(
        {"prior_state_version": 0, "resulting_state_version": 2},
        ValueError,
        id="resulting-state-version-skips-next-version",
    ),
    pytest.param(
        {"sequence": 0},
        ValueError,
        id="sequence-zero",
    ),
    pytest.param(
        {"sequence": -1},
        ValueError,
        id="sequence-negative",
    ),
    pytest.param({"receipt_id": ""}, ValueError, id="receipt-id-empty"),
    pytest.param({"result_id": ""}, ValueError, id="result-id-empty"),
    pytest.param({"command_id": ""}, ValueError, id="command-id-empty"),
    pytest.param({"command_type": ""}, ValueError, id="command-type-empty"),
    pytest.param(
        {"consistency_unit_id": ""},
        ValueError,
        id="consistency-unit-id-empty",
    ),
    pytest.param(
        {"input_fingerprint": ""},
        ValueError,
        id="semantic-input-fingerprint-empty",
    ),
    pytest.param({"policy_version": ""}, ValueError, id="policy-version-empty"),
)


def _v6_receipt_kwargs(key: Any) -> dict[str, Any]:
    return {
        "receipt_id": "receipt-v6",
        "result_id": "result-v6",
        "command_id": "command-v6",
        "command_type": key.command_type,
        "consistency_unit_id": key.consistency_unit_id,
        "idempotency_key": key,
        "input_fingerprint": _FINGERPRINT_A,
        "policy_version": "transaction-v1",
        "prior_state_version": 0,
        "resulting_state_version": 1,
        "sequence": 1,
    }


@pytest.mark.parametrize(
    "overrides,error_type",
    _M13_V6_INVALID_RECEIPT_MATRIX,
)
def test_m13_v6_atomic_receipt_rejects_contradictory_or_invalid_truth_matrix(
    overrides: dict[str, Any],
    error_type: Any,
) -> None:
    atomic_receipt, _, key_type, _, _, _, _, _ = _contracts()
    key = _key(key_type, value="idem-v6-receipt")
    arguments = _v6_receipt_kwargs(key)
    arguments.update(overrides)

    with pytest.raises(error_type):
        atomic_receipt(**arguments)


_M13_V6_INVALID_KEY_MATRIX = (
    pytest.param("value", id="idempotency-key-value-empty"),
    pytest.param("command_type", id="idempotency-key-command-type-empty"),
    pytest.param(
        "consistency_unit_id",
        id="idempotency-key-consistency-unit-id-empty",
    ),
)


@pytest.mark.parametrize("empty_field", _M13_V6_INVALID_KEY_MATRIX)
def test_m13_v6_atomic_receipt_scope_key_retains_non_empty_identity_contract(
    empty_field: str,
) -> None:
    _, _, key_type, _, _, _, _, _ = _contracts()
    arguments = {
        "value": "idem-v6",
        "command_type": "position_reconciliation",
        "consistency_unit_id": "position-v6",
    }
    arguments[empty_field] = ""
    with pytest.raises(ValueError):
        key_type(**arguments)


_M13_V6_VALID_RECEIPT_MATRIX = (
    pytest.param(0, 1, 1, id="initial-commit-boundary"),
    pytest.param(1, 2, 1, id="next-version-independent-sequence-one"),
    pytest.param(5, 6, 17, id="later-version-positive-sequence"),
)


@pytest.mark.parametrize(
    "prior_state_version,resulting_state_version,sequence",
    _M13_V6_VALID_RECEIPT_MATRIX,
)
def test_m13_v6_atomic_receipt_accepts_exact_valid_boundaries(
    prior_state_version: int,
    resulting_state_version: int,
    sequence: int,
) -> None:
    atomic_receipt, _, key_type, _, _, _, _, _ = _contracts()
    key = _key(key_type, value="idem-v6-valid")
    arguments = _v6_receipt_kwargs(key)
    arguments.update(
        {
            "prior_state_version": prior_state_version,
            "resulting_state_version": resulting_state_version,
            "sequence": sequence,
        }
    )
    receipt = atomic_receipt(**arguments)
    assert receipt.prior_state_version == prior_state_version
    assert receipt.resulting_state_version == resulting_state_version
    assert receipt.sequence == sequence
    assert type(receipt.prior_state_version) is int
    assert type(receipt.resulting_state_version) is int
    assert type(receipt.sequence) is int


def test_m13_v6_duplicate_replay_preserves_every_committed_receipt_truth_field() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    command = _command(
        command_type,
        key_type,
        key=_key(
            key_type,
            value="idem-v6-replay",
            command_type="capital_state_transition",
            consistency_unit_id="capital-unit-v6",
        ),
        command_id="command-v6-replay",
        fingerprint=_FINGERPRINT_B,
        policy_version="policy-v6",
    )
    calls = {"count": 0}

    def mutation(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "receipt-v6-replay", "result_id": "result-v6-replay"}

    committed = boundary.execute(command=command, mutation=mutation)
    stored_before = deepcopy(boundary.list_receipts())
    replay = boundary.execute(command=command, mutation=mutation)

    assert calls["count"] == 1
    for field in (
        "receipt_id",
        "result_id",
        "command_id",
        "command_type",
        "consistency_unit_id",
        "idempotency_key",
        "input_fingerprint",
        "policy_version",
        "prior_state_version",
        "resulting_state_version",
        "sequence",
    ):
        assert getattr(replay, field) == getattr(committed, field)
    assert committed.duplicate_replay is False
    assert replay.duplicate_replay is True
    assert boundary.list_receipts() == stored_before == (committed,)
    assert boundary.state_version == 1
    assert boundary.snapshot_state() == {"count": 1}


def test_m13_v6_new_successes_publish_exact_next_state_version_and_sequence() -> None:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"count": 0})
    receipts = []
    for index in range(1, 4):
        command = _command(
            command_type,
            key_type,
            key=_key(key_type, value=f"idem-v6-sequence-{index}"),
            command_id=f"command-v6-sequence-{index}",
            expected_state_version=index - 1,
        )
        receipts.append(
            boundary.execute(
                command=command,
                mutation=_mutation(
                    receipt_id=f"receipt-v6-sequence-{index}",
                    result_id=f"result-v6-sequence-{index}",
                ),
            )
        )

    assert [receipt.prior_state_version for receipt in receipts] == [0, 1, 2]
    assert [receipt.resulting_state_version for receipt in receipts] == [1, 2, 3]
    assert [receipt.sequence for receipt in receipts] == [1, 2, 3]
    assert boundary.state_version == 3
    assert boundary.snapshot_state() == {"count": 3}
    assert boundary.list_receipts() == tuple(receipts)


def _v6_caught_owner_nested_scenario() -> tuple[Any, list[BaseException]]:
    _, _, key_type, in_memory_uow, _, _, command_type, _ = _contracts()
    boundary = in_memory_uow(initial_state={"outer": 0, "nested": 0})
    nested_errors: list[BaseException] = []
    nested_command = _command(
        command_type,
        key_type,
        key=_key(key_type, value="idem-v6-combined-inner"),
        command_id="command-v6-combined-inner",
        fingerprint=_FINGERPRINT_B,
        expected_state_version=0,
    )

    def nested_mutation(state: dict[str, Any]) -> dict[str, str]:
        state["nested"] += 1
        return {
            "receipt_id": "receipt-v6-combined-inner",
            "result_id": "result-v6-combined-inner",
        }

    def outer_mutation(state: dict[str, Any]) -> dict[str, str]:
        state["outer"] += 1
        try:
            boundary.execute(
                command=nested_command,
                mutation=nested_mutation,
            )
        except BaseException as exc:
            nested_errors.append(exc)
        return {
            "receipt_id": "receipt-v6-combined-outer",
            "result_id": "result-v6-combined-outer",
        }

    boundary.execute(
        command=_command(
            command_type,
            key_type,
            key=_key(key_type, value="idem-v6-combined-outer"),
            command_id="command-v6-combined-outer",
        ),
        mutation=outer_mutation,
    )
    return boundary, nested_errors


def test_m13_v6_nested_state_and_receipt_truth_cannot_be_orphaned() -> None:
    boundary, nested_errors = _v6_caught_owner_nested_scenario()
    receipts = boundary.list_receipts()
    receipt_ids = {receipt.receipt_id for receipt in receipts}
    nested_state_committed = boundary.snapshot_state()["nested"] == 1
    nested_receipt_committed = "receipt-v6-combined-inner" in receipt_ids

    assert nested_state_committed is nested_receipt_committed
    assert nested_state_committed is False
    assert receipt_ids == {"receipt-v6-combined-outer"}
    assert boundary.snapshot_state() == {"outer": 1, "nested": 0}
    assert boundary.state_version == 1
    assert len(nested_errors) == 1
    assert type(nested_errors[0]) is RuntimeError


def test_m13_v6_nested_and_outer_cannot_reuse_sequence_or_resulting_version() -> None:
    boundary, nested_errors = _v6_caught_owner_nested_scenario()
    receipts = boundary.list_receipts()

    assert len({receipt.sequence for receipt in receipts}) == len(receipts)
    assert len({receipt.resulting_state_version for receipt in receipts}) == len(receipts)
    assert [receipt.sequence for receipt in receipts] == [1]
    assert [receipt.resulting_state_version for receipt in receipts] == [1]
    assert len(nested_errors) == 1
    assert type(nested_errors[0]) is RuntimeError
