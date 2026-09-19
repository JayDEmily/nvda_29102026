from __future__ import annotations

import importlib
import os
from datetime import UTC, datetime

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    observation,
    realise_capture,
    register_policy,
    required_symbol,
)


def _dsn() -> str:
    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for real PostgreSQL product proof")
    return value


def _psycopg():
    try:
        module = importlib.import_module("psycopg")
    except ModuleNotFoundError as exc:
        pytest.fail(f"psycopg 3.3.4 proof dependency is missing: {exc}")
    assert module.__version__ == "3.3.4"
    return module


def _assessment(*, assessment_id: str, capture_id: str, outcome: str, supersedes=None):
    cls = required_symbol("CaptureReceiptPresenceAssessmentV1")
    return cls(
        concept_id="raw_signal.capture_receipt_presence_assessment",
        contract_id="nvda.raw_signal.CaptureReceiptPresenceAssessment.v1",
        units="not_applicable",
        assessment_occurrence_id=assessment_id,
        capture_occurrence_ref=capture_id,
        outcome=outcome,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, tzinfo=UTC),
        supersedes_assessment_ref=supersedes,
    )


def test_proof_environment_is_real_postgresql_17_9() -> None:
    psycopg = _psycopg()
    with psycopg.connect(_dsn()) as connection, connection.cursor() as cursor:
        cursor.execute("show server_version")
        version = cursor.fetchone()[0]
    assert version.startswith("17.9")


def test_committed_facts_survive_fresh_owner_and_read_back_by_domain_identity() -> None:
    dsn = _dsn()
    first = build_owner(postgres_dsn=dsn)
    policy = register_policy(first)
    capture = realise_capture(first)
    obs = admit_observation(first, observation())

    second = build_owner(postgres_dsn=dsn)
    assert (
        second.reads.get_capture_scope_policy(policy.scope_policy_id, policy.scope_policy_version)
        == policy
    )
    assert second.reads.get_scheduled_capture_occurrence(capture.capture_occurrence_id) == capture
    assert second.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_assessment_history_is_append_only_and_durable_across_fresh_owner() -> None:
    dsn = _dsn()
    first = build_owner(postgres_dsn=dsn)
    register_policy(first)
    capture = realise_capture(first)
    initial = first.commands.append_capture_receipt_presence_assessment(
        _assessment(
            assessment_id="pg-assessment-zero",
            capture_id=capture.capture_occurrence_id,
            outcome="zero_received",
        )
    )
    later = first.commands.append_capture_receipt_presence_assessment(
        _assessment(
            assessment_id="pg-assessment-one-plus",
            capture_id=capture.capture_occurrence_id,
            outcome="one_or_more_received",
            supersedes=initial.assessment_occurrence_id,
        )
    )

    fresh = build_owner(postgres_dsn=dsn)
    chain = fresh.reads.list_receipt_presence_assessments(capture.capture_occurrence_id)
    assert [item.assessment_occurrence_id for item in chain] == [
        initial.assessment_occurrence_id,
        later.assessment_occurrence_id,
    ]
    assert fresh.reads.get_receipt_presence_assessment(initial.assessment_occurrence_id) == initial
    assert fresh.reads.get_receipt_presence_assessment(later.assessment_occurrence_id) == later


def test_durable_retry_is_idempotent_and_conflicting_same_id_fails_closed() -> None:
    dsn = _dsn()
    owner = build_owner(postgres_dsn=dsn)
    value = observation(observation_occurrence_id="pg-observation-retry")
    first = admit_observation(owner, value)
    fresh = build_owner(postgres_dsn=dsn)
    assert admit_observation(fresh, value) == first
    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            fresh,
            observation(
                observation_occurrence_id="pg-observation-retry",
                native_record={"Bid Price": "999.00"},
            ),
        )


def test_failed_commit_produces_no_durable_fact_or_semantic_fallback() -> None:
    dsn = _dsn()
    faulted = build_owner(postgres_dsn=dsn, fault_mode="fail_before_commit")
    # Exact technical exception type is intentionally not product-semantic authority.
    with pytest.raises(Exception):  # noqa: B017
        admit_observation(
            faulted,
            observation(observation_occurrence_id="pg-observation-failed-write"),
        )
    fresh = build_owner(postgres_dsn=dsn)
    assert fresh.reads.get_raw_observation_occurrence("pg-observation-failed-write") is None


def test_restart_reconciliation_creates_missing_owed_slot_as_unknown_not_zero() -> None:
    dsn = _dsn()
    first = build_owner(postgres_dsn=dsn)
    register_policy(first)

    restarted = build_owner(postgres_dsn=dsn)
    result = restarted.commands.reconcile_owed_slots(
        scope_policy_ref="scope-policy-001@1",
        slot_starts_utc=[datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        capture_occurrence_ids=["pg-recovered-capture-001"],
        assessment_occurrence_ids=["pg-recovered-assessment-001"],
    )
    assert len(result) == 1
    capture = restarted.reads.get_scheduled_capture_occurrence("pg-recovered-capture-001")
    chain = restarted.reads.list_receipt_presence_assessments(capture.capture_occurrence_id)
    assert chain[0].outcome == "unknown_not_established"
    assert all(item.outcome != "zero_received" for item in chain)

    fresh = build_owner(postgres_dsn=dsn)
    assert fresh.reads.get_scheduled_capture_occurrence(capture.capture_occurrence_id) == capture
    assert fresh.reads.get_receipt_presence_assessment(
        "pg-recovered-assessment-001"
    ).outcome == "unknown_not_established"


def test_persistence_proof_does_not_claim_cross_kind_atomicity_or_replay_sla() -> None:
    owner = build_owner(postgres_dsn=_dsn())
    for forbidden in (
        "cross_kind_atomic",
        "replay_equivalent",
        "rto",
        "rpo",
        "retention_duration",
        "recovery_deadline",
    ):
        assert not hasattr(owner, forbidden)
