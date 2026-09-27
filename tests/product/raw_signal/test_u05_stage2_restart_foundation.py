from __future__ import annotations

import contextlib
from datetime import UTC, datetime
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    build_owner,
    policy,
    realise_capture,
    register_policy,
    required_symbol,
)

from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence

_FIXED_NOW = datetime(2026, 9, 20, 12, 5, tzinfo=UTC)


def _dsn() -> str:
    import os

    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for Stage-2 real PostgreSQL proof")
    return value


def _fresh_owner(*, durability_port: Any | None = None) -> Any:
    port = durability_port or create_postgres_persistence(_dsn())
    return build_owner(durability_port=port, utc_now=lambda: _FIXED_NOW)


@pytest.fixture(autouse=True)
def _clean_stage2_tables() -> None:
    psycopg = pytest.importorskip("psycopg")
    assert psycopg.__version__ == "3.3.4"
    create_postgres_persistence(_dsn())
    with psycopg.connect(_dsn()) as connection:
        connection.execute(
            "TRUNCATE rsot_capture_receipt_presence_assessment_v1, "
            "rsot_scheduled_capture_occurrence_v1, rsot_capture_scope_policy_v1 CASCADE"
        )
        connection.commit()


def _policy_ref(value: str) -> Any:
    return required_symbol("scope_policy_ref")(value)


def _capture_id(value: str) -> Any:
    return required_symbol("capture_occurrence_id")(value)


def _assessment_id(value: str) -> Any:
    return required_symbol("assessment_occurrence_id")(value)


def test_stage2_fresh_owner_normalizes_timestamptz_readback_under_non_utc_database_timezone(
) -> None:
    psycopg = pytest.importorskip("psycopg")
    sql = pytest.importorskip("psycopg.sql")
    dsn = _dsn()

    with psycopg.connect(dsn) as connection:
        original_timezone = connection.execute("SHOW TimeZone").fetchone()[0]
        database_name = connection.execute("SELECT current_database()").fetchone()[0]

    def set_database_timezone(value: str) -> None:
        with psycopg.connect(dsn, autocommit=True) as connection:
            connection.execute(
                sql.SQL("ALTER DATABASE {} SET timezone TO {}").format(
                    sql.Identifier(database_name),
                    sql.Literal(value),
                )
            )

    try:
        set_database_timezone("Australia/Melbourne")
        with psycopg.connect(dsn) as connection:
            assert connection.execute("SHOW TimeZone").fetchone()[0] == "Australia/Melbourne"

        original = policy(
            scope_policy_id="stage2-non-utc-session-policy",
            activation_ts_utc=datetime(2026, 9, 27, 6, 0, tzinfo=UTC),
            deactivation_ts_utc=None,
        )
        assert register_policy(_fresh_owner(), original) == original

        restarted = _fresh_owner()
        recovered = restarted.reads.get_capture_scope_policy(
            required_symbol("scope_policy_id")("stage2-non-utc-session-policy"), 1
        )
        assert recovered == original
        assert recovered is not None
        assert recovered.activation_ts_utc == datetime(2026, 9, 27, 6, 0, tzinfo=UTC)
        assert recovered.activation_ts_utc.tzinfo is UTC
    finally:
        set_database_timezone(str(original_timezone))


def test_stage2_fresh_owner_uses_durable_policy_set_for_overlap_and_readback() -> None:
    first = _fresh_owner()
    original = policy(
        scope_policy_id="stage2-policy-a",
        activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
    )
    assert register_policy(first, original) == original

    second = _fresh_owner()
    assert second.reads.get_capture_scope_policy(
        required_symbol("scope_policy_id")("stage2-policy-a"), 1
    ) == original
    assert register_policy(second, original) == original

    overlapping = policy(
        scope_policy_id="stage2-policy-overlap",
        activation_ts_utc=datetime(2026, 9, 20, 12, 1, tzinfo=UTC),
        deactivation_ts_utc=datetime(2026, 9, 20, 12, 3, tzinfo=UTC),
    )
    with pytest.raises(ValueError, match="must not overlap"):
        register_policy(second, overlapping)

    non_overlapping = policy(
        scope_policy_id="stage2-policy-b",
        activation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        deactivation_ts_utc=datetime(2026, 9, 20, 12, 4, tzinfo=UTC),
    )
    assert register_policy(second, non_overlapping) == non_overlapping


def test_stage2_fresh_owner_recovers_stable_owed_slot_identity() -> None:
    first = _fresh_owner()
    register_policy(
        first,
        policy(
            scope_policy_id="stage2-slot-policy",
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )
    written = realise_capture(
        first,
        scope_policy_ref="stage2-slot-policy@1",
        capture_occurrence_id="stage2-capture",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )

    second = _fresh_owner()
    retry = realise_capture(
        second,
        scope_policy_ref="stage2-slot-policy@1",
        capture_occurrence_id="stage2-capture",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    assert retry == written
    assert second.reads.get_scheduled_capture_occurrence(_capture_id("stage2-capture")) == written

    with pytest.raises(ValueError, match="different capture identity"):
        realise_capture(
            second,
            scope_policy_ref="stage2-slot-policy@1",
            capture_occurrence_id="stage2-other-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )

    with pytest.raises(ValueError, match="different owed slot"):
        realise_capture(
            second,
            scope_policy_ref="stage2-slot-policy@1",
            capture_occurrence_id="stage2-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        )


def test_stage2_reconciliation_creates_durable_unknown_without_inferred_zero() -> None:
    first = _fresh_owner()
    register_policy(
        first,
        policy(
            scope_policy_id="stage2-reconcile-policy",
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )

    restarted = _fresh_owner()
    result = restarted.commands.reconcile_owed_slots(
        _policy_ref("stage2-reconcile-policy@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage2-reconciled-capture")],
        [_assessment_id("stage2-reconciled-assessment")],
    )
    assert len(result) == 1
    assert result[0].outcome == "unknown_not_established"
    assert result[0].evidence_as_of_ts_utc == _FIXED_NOW
    assert result[0].supersedes_assessment_ref is None

    fresh_reader = _fresh_owner()
    capture = fresh_reader.reads.get_scheduled_capture_occurrence(
        _capture_id("stage2-reconciled-capture")
    )
    assessment = fresh_reader.reads.get_receipt_presence_assessment(
        _assessment_id("stage2-reconciled-assessment")
    )
    assert capture is not None
    assert capture.scope_policy_ref == _policy_ref("stage2-reconcile-policy@1")
    assert assessment == result[0]
    assert assessment.outcome != "zero_received"

    retry = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("stage2-reconcile-policy@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage2-reconciled-capture")],
        [_assessment_id("stage2-reconciled-assessment")],
    )
    assert tuple(retry) == tuple(result)

    different_declared_id = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("stage2-reconcile-policy@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage2-reconciled-capture")],
        [_assessment_id("stage2-unused-assessment-id")],
    )
    assert tuple(different_declared_id) == tuple(result)
    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id("stage2-unused-assessment-id")
        )
        is None
    )


class _FaultingTransaction:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def append_capture(self, value: Any) -> None:
        self._inner.append_capture(value)
        if self._fail_after == "capture":
            raise RuntimeError("stage2 injected capture write failure")

    def append_assessment(self, value: Any) -> None:
        self._inner.append_assessment(value)
        if self._fail_after == "assessment":
            raise RuntimeError("stage2 injected assessment write failure")


class _FaultingPort:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    @contextlib.contextmanager
    def transaction(self, *, write: bool) -> Any:
        with self._inner.transaction(write=write) as transaction:
            yield _FaultingTransaction(transaction, self._fail_after)
            if self._fail_after == "transaction_exit":
                raise RuntimeError("stage2 injected transaction exit failure")


def test_stage2_public_success_waits_for_transaction_exit_commit_barrier() -> None:
    base = create_postgres_persistence(_dsn())
    first = _fresh_owner(durability_port=base)
    register_policy(
        first,
        policy(
            scope_policy_id="stage2-commit-barrier-policy",
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )

    faulting = _fresh_owner(
        durability_port=_FaultingPort(
            create_postgres_persistence(_dsn()), "transaction_exit"
        )
    )
    with pytest.raises(RuntimeError, match="transaction exit failure"):
        realise_capture(
            faulting,
            scope_policy_ref="stage2-commit-barrier-policy@1",
            capture_occurrence_id="stage2-unacknowledged-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )

    assert (
        _fresh_owner().reads.get_scheduled_capture_occurrence(
            _capture_id("stage2-unacknowledged-capture")
        )
        is None
    )


def test_stage2_failed_capture_transaction_rolls_back_without_fabricated_fact() -> None:
    base = create_postgres_persistence(_dsn())
    first = _fresh_owner(durability_port=base)
    register_policy(
        first,
        policy(
            scope_policy_id="stage2-failed-capture-policy",
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )

    faulting = _fresh_owner(
        durability_port=_FaultingPort(create_postgres_persistence(_dsn()), "capture")
    )
    with pytest.raises(RuntimeError, match="capture write failure"):
        realise_capture(
            faulting,
            scope_policy_ref="stage2-failed-capture-policy@1",
            capture_occurrence_id="stage2-failed-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )

    assert (
        _fresh_owner().reads.get_scheduled_capture_occurrence(
            _capture_id("stage2-failed-capture")
        )
        is None
    )


def test_stage2_interrupted_reconciliation_preserves_capture_and_rolls_back_assessment() -> None:
    first = _fresh_owner()
    register_policy(
        first,
        policy(
            scope_policy_id="stage2-interrupt-policy",
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )

    faulting = _fresh_owner(
        durability_port=_FaultingPort(create_postgres_persistence(_dsn()), "assessment")
    )
    with pytest.raises(RuntimeError, match="assessment write failure"):
        faulting.commands.reconcile_owed_slots(
            _policy_ref("stage2-interrupt-policy@1"),
            [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
            [_capture_id("stage2-interrupt-capture")],
            [_assessment_id("stage2-interrupt-assessment")],
        )

    after_fault = _fresh_owner()
    assert (
        after_fault.reads.get_scheduled_capture_occurrence(
            _capture_id("stage2-interrupt-capture")
        )
        is not None
    )
    assert (
        after_fault.reads.get_receipt_presence_assessment(
            _assessment_id("stage2-interrupt-assessment")
        )
        is None
    )

    recovered = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("stage2-interrupt-policy@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage2-interrupt-capture")],
        [_assessment_id("stage2-interrupt-assessment")],
    )
    assert recovered[0].outcome == "unknown_not_established"
    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id("stage2-interrupt-assessment")
        )
        == recovered[0]
    )


def test_stage2_returned_public_object_graph_does_not_expose_postgresql_capability() -> None:
    port = create_postgres_persistence(_dsn())
    owner = _fresh_owner(durability_port=port)

    assert not hasattr(owner, "persistence_port")
    assert not hasattr(owner.commands, "persistence_port")
    assert not hasattr(owner.reads, "persistence_port")
    assert not hasattr(owner, "transaction")
    assert not hasattr(owner.commands, "transaction")
    assert not hasattr(owner.reads, "transaction")

    for facet in (owner, owner.commands, owner.reads):
        for name in dir(facet):
            if name.startswith("_"):
                continue
            value = getattr(facet, name)
            assert value is not port
            assert value.__class__.__module__ != "nvda_desk.raw_signal_occurrence_truth._postgres"
