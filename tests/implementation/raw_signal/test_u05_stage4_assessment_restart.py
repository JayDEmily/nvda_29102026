from __future__ import annotations

import contextlib
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Barrier
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    append_assessment,
    build_owner,
    observation,
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
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for Stage-4 real PostgreSQL proof")
    return value


def _fresh_owner(
    *, eligibility_resolver: Any | None = None, durability_port: Any | None = None
) -> Any:
    port = durability_port or create_postgres_persistence(_dsn())
    return build_owner(
        eligibility_resolver=eligibility_resolver,
        durability_port=port,
        utc_now=lambda: _FIXED_NOW,
    )


@pytest.fixture(autouse=True)
def _clean_stage4_tables() -> None:
    psycopg = pytest.importorskip("psycopg")
    assert psycopg.__version__ == "3.3.4"
    create_postgres_persistence(_dsn())
    with psycopg.connect(_dsn()) as connection:
        connection.execute(
            "TRUNCATE rsot_capture_receipt_presence_assessment_v1, "
            "rsot_raw_observation_occurrence_v1, "
            "rsot_scheduled_capture_occurrence_v1, "
            "rsot_capture_scope_policy_v1 CASCADE"
        )
        connection.commit()


def _capture_id(value: str) -> Any:
    return required_symbol("capture_occurrence_id")(value)


def _assessment_id(value: str) -> Any:
    return required_symbol("assessment_occurrence_id")(value)


def _policy_ref(value: str) -> Any:
    return required_symbol("scope_policy_ref")(value)


class _RecordingEligibilityAuthority:
    def __init__(self, *, result: bool) -> None:
        self.result = result
        self.calls: list[tuple[Any, Any]] = []

    def __call__(self, observed: Any, effective_policy: Any) -> bool:
        self.calls.append((observed, effective_policy))
        return self.result


def _durable_capture(
    *, policy_id: str = "stage4-policy", capture_id: str = "stage4-capture"
) -> Any:
    first = _fresh_owner()
    register_policy(
        first,
        policy(
            scope_policy_id=policy_id,
            activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
    )
    return realise_capture(
        first,
        scope_policy_ref=f"{policy_id}@1",
        capture_occurrence_id=capture_id,
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )


def test_stage4_fresh_owner_rederives_optional_relation_from_durable_facts() -> None:
    capture = _durable_capture()
    observed = observation(
        observation_occurrence_id="stage4-relation-observation",
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
    )
    admit_observation(_fresh_owner(), observed)

    resolver = _RecordingEligibilityAuthority(result=True)
    restarted = _fresh_owner(eligibility_resolver=resolver)
    relation = restarted.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=observed.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )

    assert relation is not None
    assert relation.observation_occurrence_ref == observed.observation_occurrence_id
    assert relation.capture_occurrence_ref == capture.capture_occurrence_id
    assert relation.scope_policy_ref == capture.scope_policy_ref
    assert relation.received_ts_utc == observed.received_ts_utc
    assert relation.relation_role == "evidences_receipt_presence_only"
    assert len(resolver.calls) == 1


def test_stage4_fresh_owner_relation_preserves_no_relation_and_policy_lineage_law() -> None:
    capture = _durable_capture()
    in_slot = observation(
        observation_occurrence_id="stage4-ineligible-observation",
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
    )
    out_of_slot = observation(
        observation_occurrence_id="stage4-out-of-slot-observation",
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        ingestion_sequence=2,
    )
    admit_observation(_fresh_owner(), in_slot)
    admit_observation(_fresh_owner(), out_of_slot)

    resolver = _RecordingEligibilityAuthority(result=False)
    restarted = _fresh_owner(eligibility_resolver=resolver)
    assert (
        restarted.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=in_slot.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=capture.scope_policy_ref,
        )
        is None
    )
    assert (
        restarted.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=out_of_slot.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=capture.scope_policy_ref,
        )
        is None
    )
    with pytest.raises(ValueError, match="does not match"):
        restarted.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=in_slot.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=_policy_ref("different-policy@1"),
        )


def test_stage4_assessment_uses_durable_evidence_without_relation_or_receipt_time_proxy() -> None:
    capture = _durable_capture()
    observed = observation(
        observation_occurrence_id="stage4-assessment-observation",
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
    )
    admit_observation(_fresh_owner(), observed)

    resolver = _RecordingEligibilityAuthority(result=True)
    restarted = _fresh_owner(eligibility_resolver=resolver)
    stored = append_assessment(
        restarted,
        assessment_occurrence_id="stage4-assessment-one",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )

    assert stored.outcome == "one_or_more_received"
    assert len(resolver.calls) == 1
    assert resolver.calls[0][0].observation_occurrence_id == observed.observation_occurrence_id
    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id("stage4-assessment-one")
        )
        == stored
    )


def test_stage4_assessment_fails_closed_without_eligibility_authority() -> None:
    capture = _durable_capture()
    admit_observation(
        _fresh_owner(),
        observation(observation_occurrence_id="stage4-missing-eligibility"),
    )

    with pytest.raises(ValueError, match="eligibility resolver"):
        append_assessment(
            _fresh_owner(),
            assessment_occurrence_id="stage4-no-authority-assessment",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        )

    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id("stage4-no-authority-assessment")
        )
        is None
    )


def test_stage4_ineligible_durable_evidence_produces_zero() -> None:
    capture = _durable_capture()
    admit_observation(
        _fresh_owner(),
        observation(observation_occurrence_id="stage4-ineligible-for-assessment"),
    )
    resolver = _RecordingEligibilityAuthority(result=False)
    stored = append_assessment(
        _fresh_owner(eligibility_resolver=resolver),
        assessment_occurrence_id="stage4-assessment-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    assert stored.outcome == "zero_received"
    assert len(resolver.calls) == 1


def test_stage4_same_id_retry_stays_stable_and_new_assessment_supersedes_predecessor() -> None:
    capture = _durable_capture()
    first = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage4-stable-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    assert first.outcome == "zero_received"

    admit_observation(
        _fresh_owner(),
        observation(observation_occurrence_id="stage4-late-evidence"),
    )
    resolver = _RecordingEligibilityAuthority(result=True)
    restarted = _fresh_owner(eligibility_resolver=resolver)

    retried = append_assessment(
        restarted,
        assessment_occurrence_id="stage4-stable-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    assert retried == first
    assert resolver.calls == []

    second = append_assessment(
        restarted,
        assessment_occurrence_id="stage4-later-one",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, tzinfo=UTC),
        supersedes_assessment_ref=first.assessment_occurrence_id,
    )
    assert second.outcome == "one_or_more_received"
    assert second.supersedes_assessment_ref == first.assessment_occurrence_id
    assert len(resolver.calls) == 1

    chain = _fresh_owner().reads.list_receipt_presence_assessments(
        capture.capture_occurrence_id
    )
    assert tuple(item.assessment_occurrence_id for item in chain) == (
        first.assessment_occurrence_id,
        second.assessment_occurrence_id,
    )
    assert tuple(item.outcome for item in chain) == (
        "zero_received",
        "one_or_more_received",
    )


def test_stage4_conflicting_retry_and_non_immediate_supersession_fail_closed() -> None:
    capture = _durable_capture()
    first = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage4-chain-first",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    second = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage4-chain-second",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
        supersedes_assessment_ref=first.assessment_occurrence_id,
    )

    with pytest.raises(ValueError, match="different content"):
        append_assessment(
            _fresh_owner(),
            assessment_occurrence_id="stage4-chain-first",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 11, tzinfo=UTC),
        )

    with pytest.raises(ValueError, match="immediately prior"):
        append_assessment(
            _fresh_owner(),
            assessment_occurrence_id="stage4-chain-third",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
            supersedes_assessment_ref=first.assessment_occurrence_id,
        )

    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id("stage4-chain-third")
        )
        is None
    )
    assert second.supersedes_assessment_ref == first.assessment_occurrence_id


def test_stage4_reconciliation_unknown_is_durable_immediate_predecessor() -> None:
    first_owner = _fresh_owner()
    register_policy(first_owner)
    reconciled = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("scope-policy-001@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage4-reconciled-capture")],
        [_assessment_id("stage4-reconciled-unknown")],
    )[0]
    assert reconciled.outcome == "unknown_not_established"

    successor = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage4-after-unknown",
        capture_occurrence_ref=reconciled.capture_occurrence_ref,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        supersedes_assessment_ref=reconciled.assessment_occurrence_id,
    )
    assert successor.outcome == "zero_received"
    assert successor.supersedes_assessment_ref == reconciled.assessment_occurrence_id


def test_stage4_concurrent_assessment_writers_preserve_one_append_only_chain() -> None:
    capture = _durable_capture()
    root_barrier = Barrier(2)

    def append_same_root() -> Any:
        root_barrier.wait()
        return append_assessment(
            _fresh_owner(),
            assessment_occurrence_id="stage4-concurrent-root",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        roots = tuple(executor.map(lambda _: append_same_root(), range(2)))

    assert roots[0] == roots[1]
    root = roots[0]
    assert (
        len(
            _fresh_owner().reads.list_receipt_presence_assessments(
                capture.capture_occurrence_id
            )
        )
        == 1
    )

    successor_barrier = Barrier(2)

    def append_competing_successor(assessment_id: str) -> tuple[str, Any]:
        successor_barrier.wait()
        try:
            result = append_assessment(
                _fresh_owner(),
                assessment_occurrence_id=assessment_id,
                capture_occurrence_ref=capture.capture_occurrence_id,
                evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
                supersedes_assessment_ref=root.assessment_occurrence_id,
            )
        except ValueError as exc:
            return ("rejected", exc)
        return ("stored", result)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(
            executor.map(
                append_competing_successor,
                ("stage4-successor-a", "stage4-successor-b"),
            )
        )

    assert sorted(result[0] for result in results) == ["rejected", "stored"]
    rejected = next(result[1] for result in results if result[0] == "rejected")
    assert "immediately prior" in str(rejected)

    chain = _fresh_owner().reads.list_receipt_presence_assessments(
        capture.capture_occurrence_id
    )
    assert len(chain) == 2
    assert chain[0] == root
    assert chain[1].supersedes_assessment_ref == root.assessment_occurrence_id


class _FaultingTransaction:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def append_assessment(self, value: Any) -> None:
        self._inner.append_assessment(value)
        if self._fail_after == "assessment":
            raise RuntimeError("stage4 injected assessment write failure")


class _FaultingPort:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    @contextlib.contextmanager
    def transaction(self, *, write: bool) -> Any:
        with self._inner.transaction(write=write) as transaction:
            yield _FaultingTransaction(transaction, self._fail_after)
            if self._fail_after == "transaction_exit":
                raise RuntimeError("stage4 injected transaction exit failure")


@pytest.mark.parametrize(
    ("fail_after", "message"),
    [
        ("assessment", "assessment write failure"),
        ("transaction_exit", "transaction exit failure"),
    ],
)
def test_stage4_failed_assessment_transaction_fabricates_no_outcome(
    fail_after: str, message: str
) -> None:
    capture = _durable_capture()
    faulting_owner = _fresh_owner(
        durability_port=_FaultingPort(create_postgres_persistence(_dsn()), fail_after)
    )

    with pytest.raises(RuntimeError, match=message):
        append_assessment(
            faulting_owner,
            assessment_occurrence_id=f"stage4-failed-{fail_after}",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        )

    assert (
        _fresh_owner().reads.get_receipt_presence_assessment(
            _assessment_id(f"stage4-failed-{fail_after}")
        )
        is None
    )


def test_stage4_assessment_list_for_missing_capture_stays_fail_closed_after_restart() -> None:
    with pytest.raises(KeyError, match="not realised"):
        _fresh_owner().reads.list_receipt_presence_assessments(
            _capture_id("stage4-missing-capture")
        )
