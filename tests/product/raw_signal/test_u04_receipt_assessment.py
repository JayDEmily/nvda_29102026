from __future__ import annotations

from datetime import UTC, datetime

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    eligible,
    ineligible,
    observation,
    realise_capture,
    register_policy,
    required_symbol,
)


def _fixture(*, eligibility_resolver=eligible, observed=None):
    owner = build_owner(eligibility_resolver=eligibility_resolver)
    register_policy(owner)
    capture = realise_capture(owner)
    obs = admit_observation(owner, observed or observation())
    return owner, capture, obs


def _derive(owner, capture, obs):
    return owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=obs.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )


def test_relation_requires_eligibility_active_policy_and_in_slot_receipt() -> None:
    owner, capture, obs = _fixture()
    relation = _derive(owner, capture, obs)
    assert relation.relation_role == "evidences_receipt_presence_only"
    assert relation.received_ts_utc == obs.received_ts_utc
    assert relation.observation_occurrence_ref == obs.observation_occurrence_id
    assert relation.capture_occurrence_ref == capture.capture_occurrence_id
    assert relation.scope_policy_ref == capture.scope_policy_ref


def test_ineligible_observation_has_lawful_no_relation_state() -> None:
    owner, capture, obs = _fixture(eligibility_resolver=ineligible)
    assert _derive(owner, capture, obs) is None
    assert owner.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_out_of_slot_receipt_has_lawful_no_relation_state() -> None:
    observed = observation(received_ts_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC))
    owner, capture, obs = _fixture(observed=observed)
    assert _derive(owner, capture, obs) is None
    assert owner.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_relation_does_not_expose_membership_count_validity_or_finality() -> None:
    owner, capture, obs = _fixture()
    relation = _derive(owner, capture, obs)
    forbidden_fields = (
        "contains",
        "member",
        "members",
        "count",
        "counted",
        "snapshot",
        "valid",
        "complete",
        "final",
        "owned_by_capture",
    )
    for forbidden in forbidden_fields:
        assert not hasattr(relation, forbidden)


def _assessment(outcome: str, *, assessment_id: str, capture_id: str, supersedes=None):
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


@pytest.mark.parametrize(
    "outcome", ["unknown_not_established", "zero_received", "one_or_more_received"]
)
def test_all_three_assessment_outcomes_are_exact(outcome: str) -> None:
    owner, capture, _ = _fixture()
    stored = owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            outcome,
            assessment_id=f"assessment-{outcome}",
            capture_id=capture.capture_occurrence_id,
        )
    )
    assert stored.outcome == outcome


def test_late_evidence_appends_superseding_one_or_more_without_overwrite() -> None:
    owner, capture, _ = _fixture()
    zero = owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            "zero_received",
            assessment_id="assessment-zero",
            capture_id=capture.capture_occurrence_id,
        )
    )
    later = owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            "one_or_more_received",
            assessment_id="assessment-one-plus",
            capture_id=capture.capture_occurrence_id,
            supersedes=zero.assessment_occurrence_id,
        )
    )
    chain = owner.reads.list_receipt_presence_assessments(capture.capture_occurrence_id)
    assert [item.assessment_occurrence_id for item in chain] == [
        "assessment-zero",
        "assessment-one-plus",
    ]
    assert later.supersedes_assessment_ref == zero.assessment_occurrence_id
    assert owner.reads.get_receipt_presence_assessment("assessment-zero").outcome == "zero_received"


def test_assessment_same_id_retry_is_idempotent_but_conflicting_reuse_fails() -> None:
    owner, capture, _ = _fixture()
    value = _assessment(
        "unknown_not_established",
        assessment_id="assessment-retry",
        capture_id=capture.capture_occurrence_id,
    )
    first = owner.commands.append_capture_receipt_presence_assessment(value)
    assert owner.commands.append_capture_receipt_presence_assessment(value) == first
    with pytest.raises((TypeError, ValueError)):
        owner.commands.append_capture_receipt_presence_assessment(
            _assessment(
                "zero_received",
                assessment_id="assessment-retry",
                capture_id=capture.capture_occurrence_id,
            )
        )


def test_unknown_is_not_zero_and_one_or_more_is_not_exact_count_or_finality() -> None:
    owner, capture, _ = _fixture()
    unknown = owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            "unknown_not_established",
            assessment_id="assessment-unknown",
            capture_id=capture.capture_occurrence_id,
        )
    )
    assert unknown.outcome != "zero_received"
    for forbidden in ("exact_count", "final", "outage", "provider_event_absence", "healthy"):
        assert not hasattr(unknown, forbidden)


@pytest.mark.parametrize("supersedes", ["missing-assessment", "assessment-self"])
def test_broken_or_self_supersession_fails_closed(supersedes: str) -> None:
    owner, capture, _ = _fixture()
    with pytest.raises((TypeError, ValueError, KeyError)):
        owner.commands.append_capture_receipt_presence_assessment(
            _assessment(
                "one_or_more_received",
                assessment_id="assessment-self",
                capture_id=capture.capture_occurrence_id,
                supersedes=supersedes,
            )
        )


def test_non_immediate_supersession_fails_closed() -> None:
    owner, capture, _ = _fixture()
    first = owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            "unknown_not_established",
            assessment_id="assessment-first",
            capture_id=capture.capture_occurrence_id,
        )
    )
    owner.commands.append_capture_receipt_presence_assessment(
        _assessment(
            "zero_received",
            assessment_id="assessment-second",
            capture_id=capture.capture_occurrence_id,
            supersedes=first.assessment_occurrence_id,
        )
    )
    with pytest.raises((TypeError, ValueError, KeyError)):
        owner.commands.append_capture_receipt_presence_assessment(
            _assessment(
                "one_or_more_received",
                assessment_id="assessment-third",
                capture_id=capture.capture_occurrence_id,
                supersedes=first.assessment_occurrence_id,
            )
        )
