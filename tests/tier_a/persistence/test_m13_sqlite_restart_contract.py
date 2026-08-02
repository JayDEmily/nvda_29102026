"""Tier A proof for durable M13 state/evidence and restart recovery."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest
from tests.support.m11_k16_k17_contract_harness import production_execution_receipt

from nvda_desk.contracts.review import ReviewPacket
from nvda_desk.m11_portfolio_lifecycle import PortfolioLifecycleService
from nvda_desk.m12_evidence_replay import EvidenceReplayService
from nvda_desk.m13_state_kernel import (
    IdempotencyKey,
    SqliteEvidenceRepository,
    SqliteUnitOfWork,
    TransactionCommand,
)


def _command(*, expected_state_version: int = 0, fingerprint: str = "a" * 64):
    return TransactionCommand(
        command_id="durable-command:1",
        idempotency_key=IdempotencyKey(
            value="durable-idem:1",
            command_type="durable_test",
            consistency_unit_id="durable-unit:1",
        ),
        input_fingerprint=fingerprint,
        expected_state_version=expected_state_version,
        policy_version="durable-test.v1",
    )


def _mutation(calls: dict[str, int]):
    def mutate(state: dict[str, Any]) -> dict[str, str]:
        calls["count"] += 1
        state["count"] += 1
        return {"receipt_id": "durable-receipt:1", "result_id": "durable-result:1"}

    return mutate


def test_sqlite_state_and_receipts_survive_process_restart(tmp_path) -> None:
    database = tmp_path / "state.sqlite3"
    calls = {"count": 0}
    first = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})
    receipt = first.execute(command=_command(), mutation=_mutation(calls))

    restarted = SqliteUnitOfWork(database_path=database, initial_state={"count": 999})
    assert restarted.durability == "durable_sqlite"
    assert restarted.state_version == 1
    assert restarted.snapshot_state() == {"count": 1}
    assert restarted.list_receipts() == (receipt,)


def test_sqlite_exact_duplicate_after_restart_does_not_repeat_mutation(tmp_path) -> None:
    database = tmp_path / "state.sqlite3"
    calls = {"count": 0}
    SqliteUnitOfWork(database_path=database, initial_state={"count": 0}).execute(
        command=_command(), mutation=_mutation(calls)
    )
    restarted = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})
    replay = restarted.execute(command=_command(), mutation=_mutation(calls))

    assert calls["count"] == 1
    assert replay.duplicate_replay is True
    assert restarted.snapshot_state() == {"count": 1}
    assert len(restarted.list_receipts()) == 1


def test_sqlite_failed_mutation_rolls_back_durable_state_and_receipt(tmp_path) -> None:
    database = tmp_path / "state.sqlite3"
    boundary = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})

    def fail(state: dict[str, Any]) -> dict[str, str]:
        state["count"] = 99
        raise RuntimeError("durable mutation failed")

    with pytest.raises(RuntimeError, match="durable mutation failed"):
        boundary.execute(command=_command(), mutation=fail)

    restarted = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})
    assert restarted.state_version == 0
    assert restarted.snapshot_state() == {"count": 0}
    assert restarted.list_receipts() == ()


def test_m11_portfolio_snapshot_and_duplicate_fill_recover_after_restart(tmp_path) -> None:
    database = tmp_path / "portfolio.sqlite3"
    first = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    execution = production_execution_receipt()
    original = first.reconcile_fill(execution)
    assert original.snapshot.durability == "durable_sqlite"
    assert original.snapshot.positions[0].durable_commit_proven is True

    restarted = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    assert restarted.snapshot() == original.snapshot
    replay = restarted.reconcile_fill(execution)
    assert replay.receipt_id == original.receipt_id
    assert replay.duplicate_replay is True
    assert restarted.snapshot() == original.snapshot


def test_sqlite_evidence_repository_rebuilds_typed_m12_material_after_restart(tmp_path) -> None:
    database = tmp_path / "evidence.sqlite3"
    content = ReviewPacket(packet_id="decision:1", summary="stand_down", sections=["stand_down"])
    repository = SqliteEvidenceRepository(database_path=database)
    record = repository.store(
        owner_module="M09",
        occurrence_id="decision-occurrence:1",
        content=content,
    )

    restarted = SqliteEvidenceRepository(database_path=database)
    recovered = restarted.load("decision-occurrence:1")
    assert recovered == content
    assert restarted.list_records() == (record,)

    material = EvidenceReplayService().build_material(
        owner_module="M09",
        contract_version="1.0.0",
        occurrence_id=record.occurrence_id,
        content=recovered,
        sequence=record.sequence,
        material_time_utc=None,
        material_label="durable-original-output",
    )
    assert material.content_snapshot == content.model_dump(mode="python")
    assert material.retrievable is True


def test_sqlite_conflicting_scoped_key_after_restart_is_rejected_without_mutation(tmp_path) -> None:
    database = tmp_path / "state.sqlite3"
    first = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})
    first.execute(command=_command(), mutation=_mutation({"count": 0}))
    restarted = SqliteUnitOfWork(database_path=database, initial_state={"count": 999})

    with pytest.raises(Exception) as caught:
        restarted.execute(
            command=_command(fingerprint="b" * 64),
            mutation=_mutation({"count": 0}),
        )

    assert type(caught.value).__name__ == "IdempotencyConflictError"
    assert restarted.state_version == 1
    assert restarted.snapshot_state() == {"count": 1}
    assert len(restarted.list_receipts()) == 1


def test_sqlite_codec_rejects_non_utc_and_unsupported_state_before_commit(tmp_path) -> None:
    from datetime import datetime

    database = tmp_path / "state.sqlite3"
    boundary = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})

    def invalid(state: dict[str, Any]) -> dict[str, str]:
        state["bad_time"] = datetime(2026, 8, 2, 9, 0)
        return {"receipt_id": "durable-receipt:1", "result_id": "durable-result:1"}

    with pytest.raises(ValueError, match="durable_datetime_must_be_utc"):
        boundary.execute(command=_command(), mutation=invalid)

    restarted = SqliteUnitOfWork(database_path=database, initial_state={"count": 0})
    assert restarted.state_version == 0
    assert restarted.snapshot_state() == {"count": 0}
    assert restarted.list_receipts() == ()


def test_sqlite_evidence_occurrence_is_idempotent_and_conflict_safe(tmp_path) -> None:
    from nvda_desk.m13_state_kernel import EvidenceRepositoryPort, IdempotencyConflictError

    database = tmp_path / "evidence.sqlite3"
    repository = SqliteEvidenceRepository(database_path=database)
    assert isinstance(repository, EvidenceRepositoryPort)
    first_content = ReviewPacket(
        packet_id="decision:1", summary="stand_down", sections=["stand_down"]
    )
    first = repository.store(
        owner_module="M09", occurrence_id="decision-occurrence:1", content=first_content
    )
    duplicate = repository.store(
        owner_module="M09", occurrence_id="decision-occurrence:1", content=first_content
    )
    assert duplicate == first
    assert len(repository.list_records()) == 1

    conflicting = ReviewPacket(packet_id="decision:2", summary="trade", sections=["trade"])
    with pytest.raises(IdempotencyConflictError, match="conflicting durable evidence occurrence"):
        repository.store(
            owner_module="M09", occurrence_id="decision-occurrence:1", content=conflicting
        )
    assert repository.load("decision-occurrence:1") == first_content
    assert repository.list_records() == (first,)


def test_m11_close_receipt_and_last_transition_recover_after_restart(tmp_path) -> None:
    database = tmp_path / "portfolio.sqlite3"
    first = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    execution = production_execution_receipt()
    filled = first.reconcile_fill(execution)
    position = filled.snapshot.positions[0]
    decision = first.decide_lifecycle(
        snapshot=filled.snapshot,
        position_id=position.position_id,
        action="close",
        quantity=position.quantity,
        reasons=("durable-close",),
        decided_at_utc=datetime(2026, 8, 1, 2, 20, tzinfo=UTC),
    )
    original = first.apply_lifecycle(decision)
    assert original.snapshot.positions == ()
    assert original.snapshot.durability == "durable_sqlite"

    restarted = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    assert restarted.snapshot() == original.snapshot
    replay = restarted.apply_lifecycle(decision)
    assert replay.receipt_id == original.receipt_id
    assert replay.duplicate_replay is True
    assert restarted.snapshot() == original.snapshot


def test_m11_old_fill_duplicate_after_durable_close_cannot_reopen_position(tmp_path) -> None:
    database = tmp_path / "portfolio.sqlite3"
    first = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    execution = production_execution_receipt(limit_price=Decimal("100"))
    filled = first.reconcile_fill(execution)
    position = filled.snapshot.positions[0]
    decision = first.decide_lifecycle(
        snapshot=filled.snapshot,
        position_id=position.position_id,
        action="close",
        quantity=position.quantity,
        reasons=("durable-close",),
        decided_at_utc=datetime(2026, 8, 1, 2, 20, tzinfo=UTC),
    )
    closed = first.apply_lifecycle(decision)

    restarted = PortfolioLifecycleService(
        SqliteUnitOfWork(database_path=database, initial_state={"positions": {}})
    )
    replay = restarted.reconcile_fill(execution)
    assert replay.receipt_id == filled.receipt_id
    assert replay.duplicate_replay is True
    assert restarted.snapshot() == closed.snapshot
    assert restarted.snapshot().positions == ()
