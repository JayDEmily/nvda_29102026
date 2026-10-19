"""RSQL-P02/P06/P07/P08/P10: schedule, relations and durable assessment law."""

from contextlib import contextmanager
from dataclasses import replace
from datetime import timedelta

import pytest
from _support import T0, fresh_record, mechanism, observation, owner, policy

from nvda_desk.raw_signal_occurrence_truth import api


def test_sqlite_owed_slot_and_policy_boundary_law(tmp_path):
    o = owner(tmp_path / "raw.db", create=True)
    p = policy(deactivation_ts_utc=T0 + timedelta(minutes=2))
    o.commands.register_capture_scope_policy(p)
    ref = api.scope_policy_ref("policy@1")
    for second in (0, 30, 60, 90):
        start = T0 + timedelta(seconds=second)
        capture = o.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=ref,
            slot_start_utc=start,
            capture_occurrence_id=api.capture_occurrence_id(str(second)),
        )
        assert capture.slot_start_utc == start
        assert capture.slot_end_utc == start + timedelta(seconds=30)
    for start in (
        T0 - timedelta(seconds=30),
        T0 + timedelta(minutes=2),
        T0 + timedelta(microseconds=1),
    ):
        with pytest.raises(ValueError):
            o.commands.realise_scheduled_capture_occurrence(
                scope_policy_ref=ref,
                slot_start_utc=start,
                capture_occurrence_id=api.capture_occurrence_id("invalid"),
            )
    with pytest.raises(ValueError):
        o.commands.register_capture_scope_policy(
            replace(p, eligibility_policy_ref=api.eligibility_policy_ref("changed"))
        )
    with pytest.raises(ValueError):
        o.commands.register_capture_scope_policy(policy(scope_policy_version=2))
    successor = policy(scope_policy_version=2, activation_ts_utc=p.deactivation_ts_utc)
    assert o.commands.register_capture_scope_policy(successor) == successor
    retry = o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=ref,
        slot_start_utc=T0,
        capture_occurrence_id=api.capture_occurrence_id("0"),
    )
    assert retry.capture_occurrence_id == api.capture_occurrence_id("0")
    with pytest.raises(ValueError):
        o.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=ref,
            slot_start_utc=T0,
            capture_occurrence_id=api.capture_occurrence_id("different-retry-id"),
        )
    with pytest.raises(ValueError):
        o.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=ref,
            slot_start_utc=T0.replace(second=30),
            capture_occurrence_id=api.capture_occurrence_id("0"),
        )
    with pytest.raises(KeyError):
        o.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=api.scope_policy_ref("absent@1"),
            slot_start_utc=T0,
            capture_occurrence_id=api.capture_occurrence_id("absent"),
        )


def test_sqlite_receipt_relation_and_assessment_chain(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    o.commands.register_capture_scope_policy(policy())
    ref = api.scope_policy_ref("policy@1")
    c = o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=ref,
        slot_start_utc=T0,
        capture_occurrence_id=api.capture_occurrence_id("capture"),
    )
    zero = o.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=api.assessment_occurrence_id("zero"),
        capture_occurrence_ref=c.capture_occurrence_id,
        evidence_as_of_ts_utc=T0,
        supersedes_assessment_ref=None,
    )
    assert zero.outcome == "zero_received"
    for identity, seconds in (("start", 0), ("end", 30)):
        raw = observation(identity, seconds, received_ts_utc=T0 + timedelta(seconds=seconds))
        o.commands.admit_raw_observation_occurrence(raw)
        relation = o.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=raw.observation_occurrence_id,
            capture_occurrence_ref=c.capture_occurrence_id,
            scope_policy_ref=ref,
        )
        if seconds == 0:
            assert relation.relation_role == "evidences_receipt_presence_only"
            assert relation.received_ts_utc == T0
        else:
            assert relation is None
    reopened = owner(path)
    one = reopened.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=api.assessment_occurrence_id("one"),
        capture_occurrence_ref=c.capture_occurrence_id,
        evidence_as_of_ts_utc=T0 + timedelta(minutes=1),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    assert one.outcome == "one_or_more_received"
    assert tuple(reopened.reads.list_receipt_presence_assessments(c.capture_occurrence_id)) == (
        zero,
        one,
    )
    with pytest.raises(ValueError):
        reopened.commands.append_capture_receipt_presence_assessment(
            assessment_occurrence_id=api.assessment_occurrence_id("fork"),
            capture_occurrence_ref=c.capture_occurrence_id,
            evidence_as_of_ts_utc=T0,
            supersedes_assessment_ref=zero.assessment_occurrence_id,
        )
    opposing = owner(path, eligible=False)
    assert (
        opposing.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=api.observation_occurrence_id("start"),
            capture_occurrence_ref=c.capture_occurrence_id,
            scope_policy_ref=ref,
        )
        is None
    )
    assert opposing.reads.get_raw_observation_occurrence(api.observation_occurrence_id("start"))
    missing = api.create_owner(durability_port=mechanism().create_sqlite_persistence(str(path)))
    with pytest.raises(ValueError):
        missing.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=api.observation_occurrence_id("start"),
            capture_occurrence_ref=c.capture_occurrence_id,
            scope_policy_ref=ref,
        )


def test_sqlite_scope_high_water_and_restart_unknown(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    for identity, sequence, scope in (("a-high", 10**90, "A"), ("b-low", -(10**90), "B")):
        o.commands.admit_raw_observation_occurrence(observation(identity, sequence, scope))
    o = owner(path)
    with pytest.raises(ValueError):
        o.commands.admit_raw_observation_occurrence(observation("a-low", 10**90 - 1, "A"))
    o.commands.admit_raw_observation_occurrence(observation("a-higher", 10**90 + 1, "A"))
    o.commands.register_capture_scope_policy(policy())
    # Deliberate transaction failure: the capture command must commit independently.
    port = mechanism().create_sqlite_persistence(str(path))

    class AssessmentFailure:
        @contextmanager
        def transaction(self, *, write):
            with port.transaction(write=write) as tx:

                class Proxy:
                    def __getattr__(self, name):
                        return getattr(tx, name)

                    def append_assessment(self, value):
                        raise RuntimeError("deliberate assessment failure")

                yield Proxy()

    failing = api.create_owner(durability_port=AssessmentFailure(), utc_now=lambda: T0)
    kwargs = dict(
        scope_policy_ref=api.scope_policy_ref("policy@1"),
        slot_starts_utc=(T0,),
        capture_occurrence_ids=(api.capture_occurrence_id("restart"),),
        assessment_occurrence_ids=(api.assessment_occurrence_id("unknown"),),
    )
    with pytest.raises(RuntimeError, match="deliberate assessment failure"):
        failing.commands.reconcile_owed_slots(**kwargs)
    restarted = owner(path)
    assert restarted.reads.get_scheduled_capture_occurrence(api.capture_occurrence_id("restart"))
    assert (
        restarted.reads.get_receipt_presence_assessment(api.assessment_occurrence_id("unknown"))
        is None
    )
    result = restarted.commands.reconcile_owed_slots(**kwargs)
    assert result[0].outcome == "unknown_not_established"
    assert result[0].supersedes_assessment_ref is None
    assert tuple(fresh_record(path, "chain", "restart")) == tuple(result)


def test_sqlite_assessment_without_relation_capture_isolation_and_missing_authority(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    o.commands.register_capture_scope_policy(policy())
    ref = api.scope_policy_ref("policy@1")
    a = o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=ref,
        slot_start_utc=T0,
        capture_occurrence_id=api.capture_occurrence_id("A"),
    )
    b = o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=ref,
        slot_start_utc=T0 + timedelta(seconds=30),
        capture_occurrence_id=api.capture_occurrence_id("B"),
    )
    zero_kwargs = dict(
        assessment_occurrence_id=api.assessment_occurrence_id("a-zero"),
        capture_occurrence_ref=a.capture_occurrence_id,
        evidence_as_of_ts_utc=T0,
        supersedes_assessment_ref=None,
    )
    zero = o.commands.append_capture_receipt_presence_assessment(**zero_kwargs)
    raw = observation("late", received_ts_utc=T0 + timedelta(seconds=1))
    o.commands.admit_raw_observation_occurrence(raw)
    # No relation derivation precedes this assessment. Receipt truth is not relation storage.
    one = o.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=api.assessment_occurrence_id("a-one"),
        capture_occurrence_ref=a.capture_occurrence_id,
        evidence_as_of_ts_utc=T0 + timedelta(seconds=2),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    assert one.outcome == "one_or_more_received"
    assert o.commands.append_capture_receipt_presence_assessment(**zero_kwargs) == zero
    no_b = o.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=api.assessment_occurrence_id("b-zero"),
        capture_occurrence_ref=b.capture_occurrence_id,
        evidence_as_of_ts_utc=T0 + timedelta(minutes=1),
        supersedes_assessment_ref=None,
    )
    assert no_b.outcome == "zero_received"
    assert tuple(fresh_record(path, "chain", "A")) == (zero, one)
    assert tuple(fresh_record(path, "chain", "B")) == (no_b,)
    for capture, predecessor in (
        (api.capture_occurrence_id("missing"), None),
        (a.capture_occurrence_id, api.assessment_occurrence_id("missing")),
        (a.capture_occurrence_id, no_b.assessment_occurrence_id),
    ):
        with pytest.raises((KeyError, ValueError)):
            o.commands.append_capture_receipt_presence_assessment(
                assessment_occurrence_id=api.assessment_occurrence_id("invalid"),
                capture_occurrence_ref=capture,
                evidence_as_of_ts_utc=T0,
                supersedes_assessment_ref=predecessor,
            )
    missing = api.create_owner(durability_port=mechanism().create_sqlite_persistence(str(path)))
    with pytest.raises(ValueError):
        missing.commands.append_capture_receipt_presence_assessment(
            assessment_occurrence_id=api.assessment_occurrence_id("missing-eligibility"),
            capture_occurrence_ref=a.capture_occurrence_id,
            evidence_as_of_ts_utc=T0,
            supersedes_assessment_ref=one.assessment_occurrence_id,
        )
