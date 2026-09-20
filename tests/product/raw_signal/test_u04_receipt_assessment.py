from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    append_assessment,
    assessment_contract,
    build_owner,
    observation,
    policy,
    policy_ref,
    realise_capture,
    register_policy,
    typed_identity,
)


class _RecordingEligibilityAuthority:
    def __init__(self, *, result: bool = True) -> None:
        self.result = result
        self.expected_observation: Any | None = None
        self.expected_policy: Any | None = None
        self.calls: list[tuple[Any, Any]] = []

    def __call__(self, observed: Any, effective_policy: Any) -> bool:
        self.calls.append((observed, effective_policy))
        assert observed is self.expected_observation
        assert effective_policy is self.expected_policy
        return self.result


class _TechnicalPersistencePort:
    """Proof technical port: stores owner-decided facts and has no decision methods."""

    def __init__(self) -> None:
        self.policies: dict[tuple[Any, int], Any] = {}
        self.captures: dict[Any, Any] = {}
        self.observations: dict[Any, Any] = {}
        self.assessments: dict[Any, Any] = {}
        self.assessment_order: dict[Any, list[Any]] = {}
        self.appended_assessments: list[Any] = []

    def append_policy(self, value: Any) -> Any:
        self.policies[(value.scope_policy_id, value.scope_policy_version)] = value
        return value

    def get_policy(self, policy_id: Any, version: int) -> Any | None:
        return self.policies.get((policy_id, version))

    def append_capture(self, value: Any) -> Any:
        self.captures[value.capture_occurrence_id] = value
        return value

    def get_capture(self, capture_id: Any) -> Any | None:
        return self.captures.get(capture_id)

    def append_observation(self, value: Any) -> Any:
        self.observations[value.observation_occurrence_id] = value
        return value

    def get_observation(self, observation_id: Any) -> Any | None:
        return self.observations.get(observation_id)

    def append_assessment(self, value: Any) -> Any:
        self.appended_assessments.append(value)
        self.assessments[value.assessment_occurrence_id] = value
        self.assessment_order.setdefault(value.capture_occurrence_ref, []).append(
            value.assessment_occurrence_id
        )
        return value

    def get_assessment(self, assessment_id: Any) -> Any | None:
        return self.assessments.get(assessment_id)

    def list_assessments(self, capture_id: Any) -> list[Any]:
        return [self.assessments[item] for item in self.assessment_order.get(capture_id, [])]


def _capture_fixture(
    *, result: bool = True, persistence_port: Any | None = None
) -> tuple[Any, Any, Any, _RecordingEligibilityAuthority]:
    resolver = _RecordingEligibilityAuthority(result=result)
    owner = build_owner(
        eligibility_resolver=resolver,
        **({"persistence_port": persistence_port} if persistence_port is not None else {}),
    )
    stored_policy = register_policy(owner)
    capture = realise_capture(owner)
    resolver.expected_policy = stored_policy
    return owner, capture, stored_policy, resolver


def _add_observation(
    owner: Any,
    capture: Any,
    resolver: _RecordingEligibilityAuthority,
    *,
    observed: Any | None = None,
    scope_policy_ref: Any | None = None,
) -> tuple[Any, Any]:
    obs = admit_observation(owner, observed or observation())
    resolver.expected_observation = obs
    relation = owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=obs.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref if scope_policy_ref is None else scope_policy_ref,
    )
    return obs, relation


def test_relation_requires_exact_observation_effective_policy_and_in_slot_receipt() -> None:
    owner, capture, stored_policy, resolver = _capture_fixture()
    obs, relation = _add_observation(owner, capture, resolver)
    assert resolver.calls == [(obs, stored_policy)]
    assert relation.relation_role == "evidences_receipt_presence_only"
    assert relation.received_ts_utc == obs.received_ts_utc
    assert relation.observation_occurrence_ref == obs.observation_occurrence_id
    assert relation.capture_occurrence_ref == capture.capture_occurrence_id
    assert relation.scope_policy_ref == capture.scope_policy_ref


def test_ineligible_observation_has_lawful_no_relation_state() -> None:
    owner, capture, stored_policy, resolver = _capture_fixture(result=False)
    obs, relation = _add_observation(owner, capture, resolver)
    assert resolver.calls == [(obs, stored_policy)]
    assert relation is None
    assert owner.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_out_of_slot_receipt_has_lawful_no_relation_state() -> None:
    owner, capture, _, resolver = _capture_fixture()
    observed = observation(received_ts_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC))
    obs, relation = _add_observation(owner, capture, resolver, observed=observed)
    assert relation is None
    assert owner.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_receipt_immediately_before_slot_start_has_lawful_no_relation_state() -> None:
    owner, capture, _, resolver = _capture_fixture()
    observed = observation(
        observation_occurrence_id="observation-pre-start",
        received_ts_utc=datetime(2026, 9, 20, 11, 59, 59, 999999, tzinfo=UTC),
    )
    obs, relation = _add_observation(owner, capture, resolver, observed=observed)
    assert relation is None
    assert owner.reads.get_raw_observation_occurrence(obs.observation_occurrence_id) == obs


def test_mismatched_existing_policy_reference_cannot_authorise_or_mislineage_relation() -> None:
    owner, capture, _, resolver = _capture_fixture()
    register_policy(
        owner,
        policy(
            scope_policy_version=2,
            activation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
            deactivation_ts_utc=None,
        ),
    )
    obs = admit_observation(owner, observation())
    resolver.expected_observation = obs
    with pytest.raises((TypeError, ValueError, KeyError, AssertionError)):
        owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=obs.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=policy_ref("scope-policy-001", 2),
        )
    assert resolver.calls == [] or all(
        call[1] is resolver.expected_policy for call in resolver.calls
    )


def test_typed_but_nonexistent_observation_authority_cannot_create_relation() -> None:
    owner, capture, _, resolver = _capture_fixture()
    missing_observation = typed_identity(
        "RawObservationOccurrenceV1",
        "observation_occurrence_id",
        "missing-observation",
    )
    with pytest.raises((TypeError, ValueError, KeyError)):
        owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=missing_observation,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=capture.scope_policy_ref,
        )
    assert resolver.calls == []


def test_missing_capture_authority_cannot_create_relation() -> None:
    owner, _, _, _ = _capture_fixture()
    obs = admit_observation(owner)
    missing_capture = typed_identity(
        "ScheduledCaptureOccurrenceV1", "capture_occurrence_id", "missing-capture"
    )
    with pytest.raises((TypeError, ValueError, KeyError)):
        owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=obs.observation_occurrence_id,
            capture_occurrence_ref=missing_capture,
            scope_policy_ref=policy_ref(),
        )


@pytest.mark.parametrize(
    ("received_ts_utc", "expect_relation"),
    [
        (datetime(2026, 9, 20, 11, 59, 59, 999999, tzinfo=UTC), False),
        (datetime(2026, 9, 20, 12, 0, 0, 0, tzinfo=UTC), True),
        (datetime(2026, 9, 20, 12, 0, 29, 999999, tzinfo=UTC), True),
        (datetime(2026, 9, 20, 12, 0, 30, 0, tzinfo=UTC), False),
    ],
)
def test_receipt_presence_uses_exact_microsecond_half_open_interval_edges(
    received_ts_utc: datetime, expect_relation: bool
) -> None:
    owner, capture, _, resolver = _capture_fixture()
    observed = observation(
        observation_occurrence_id=f"observation-edge-{received_ts_utc.isoformat()}",
        received_ts_utc=received_ts_utc,
    )
    _, relation = _add_observation(owner, capture, resolver, observed=observed)
    assert (relation is not None) is expect_relation


def test_relation_does_not_expose_membership_count_validity_or_finality() -> None:
    owner, capture, _, resolver = _capture_fixture()
    _, relation = _add_observation(owner, capture, resolver)
    for forbidden in (
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
    ):
        assert not hasattr(relation, forbidden)


@pytest.mark.parametrize(
    "outcome", ["unknown_not_established", "zero_received", "one_or_more_received"]
)
def test_assessment_contract_discriminant_accepts_exact_three_outcomes(outcome: str) -> None:
    assert assessment_contract(outcome=outcome).outcome == outcome


def test_zero_is_derived_when_no_eligible_committed_receipt_is_visible() -> None:
    owner, capture, _, _ = _capture_fixture()
    stored = append_assessment(
        owner,
        assessment_occurrence_id="assessment-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    assert stored.outcome == "zero_received"


@pytest.mark.parametrize(
    ("eligibility", "received_ts", "observation_id"),
    [
        (False, datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC), "observation-ineligible"),
        (True, datetime(2026, 9, 20, 11, 59, 59, tzinfo=UTC), "observation-pre-slot"),
        (True, datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC), "observation-at-end"),
    ],
)
def test_ineligible_or_out_of_slot_raw_observation_does_not_make_one_or_more(
    eligibility: bool, received_ts: datetime, observation_id: str
) -> None:
    owner, capture, _, resolver = _capture_fixture(result=eligibility)
    _, relation = _add_observation(
        owner,
        capture,
        resolver,
        observed=observation(
            observation_occurrence_id=observation_id,
            received_ts_utc=received_ts,
        ),
    )
    assert relation is None
    assessment = append_assessment(
        owner,
        assessment_occurrence_id=f"assessment-{observation_id}",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 40, tzinfo=UTC),
    )
    assert assessment.outcome == "zero_received"


def test_assessment_receipt_evidence_is_capture_local_not_owner_global() -> None:
    resolver = _RecordingEligibilityAuthority(result=True)
    owner = build_owner(eligibility_resolver=resolver)
    stored_policy = register_policy(owner)
    capture_a = realise_capture(
        owner,
        capture_occurrence_id="capture-local-a",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC),
    )
    capture_b = realise_capture(
        owner,
        capture_occurrence_id="capture-local-b",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
    )
    resolver.expected_policy = stored_policy
    observed = admit_observation(
        owner,
        observation(
            observation_occurrence_id="observation-capture-a-only",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
        ),
    )
    resolver.expected_observation = observed
    relation = owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=observed.observation_occurrence_id,
        capture_occurrence_ref=capture_a.capture_occurrence_id,
        scope_policy_ref=capture_a.scope_policy_ref,
    )
    assert relation is not None

    as_of = datetime(2026, 9, 20, 12, 0, 45, tzinfo=UTC)
    assessment_a = append_assessment(
        owner,
        assessment_occurrence_id="assessment-capture-a",
        capture_occurrence_ref=capture_a.capture_occurrence_id,
        evidence_as_of_ts_utc=as_of,
    )
    assessment_b = append_assessment(
        owner,
        assessment_occurrence_id="assessment-capture-b",
        capture_occurrence_ref=capture_b.capture_occurrence_id,
        evidence_as_of_ts_utc=as_of,
    )
    assert assessment_a.outcome == "one_or_more_received"
    assert assessment_b.outcome == "zero_received"


def test_one_or_more_is_derived_when_eligible_committed_receipt_is_visible() -> None:
    owner, capture, _, resolver = _capture_fixture()
    _add_observation(owner, capture, resolver)
    stored = append_assessment(
        owner,
        assessment_occurrence_id="assessment-one-plus",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    assert stored.outcome == "one_or_more_received"


def test_persistence_port_receives_already_decided_semantics_and_has_no_decision_capability(
) -> None:
    port = _TechnicalPersistencePort()
    owner, capture, _, resolver = _capture_fixture(persistence_port=port)
    zero = append_assessment(
        owner,
        assessment_occurrence_id="assessment-zero-port",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    _add_observation(owner, capture, resolver)
    one = append_assessment(
        owner,
        assessment_occurrence_id="assessment-one-port",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    assert [zero.outcome, one.outcome] == ["zero_received", "one_or_more_received"]
    assert [item.outcome for item in port.appended_assessments] == [
        "zero_received",
        "one_or_more_received",
    ]
    for semantic_method in (
        "derive_relation",
        "decide_relation",
        "assess_outcome",
        "decide_outcome",
        "is_eligible",
        "classify",
    ):
        assert not hasattr(port, semantic_method)


def test_caller_cannot_supply_assessment_outcome() -> None:
    owner, capture, _, _ = _capture_fixture()
    with pytest.raises((TypeError, ValueError)):
        append_assessment(
            owner,
            assessment_occurrence_id="assessment-forged",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
            outcome="one_or_more_received",
        )


def test_late_evidence_appends_superseding_one_or_more_without_overwrite() -> None:
    owner, capture, _, resolver = _capture_fixture()
    zero = append_assessment(
        owner,
        assessment_occurrence_id="assessment-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    _add_observation(
        owner,
        capture,
        resolver,
        observed=observation(
            observation_occurrence_id="observation-late",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
            ingestion_sequence=2,
        ),
    )
    later = append_assessment(
        owner,
        assessment_occurrence_id="assessment-one-plus",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    chain = owner.reads.list_receipt_presence_assessments(capture.capture_occurrence_id)
    assert [str(item.assessment_occurrence_id) for item in chain] == [
        "assessment-zero",
        "assessment-one-plus",
    ]
    assert [item.outcome for item in chain] == ["zero_received", "one_or_more_received"]
    assert later.supersedes_assessment_ref == zero.assessment_occurrence_id
    assert owner.reads.get_receipt_presence_assessment(zero.assessment_occurrence_id).outcome == (
        "zero_received"
    )


def test_assessment_same_id_retry_is_idempotent_but_evidence_change_conflicts() -> None:
    owner, capture, _, resolver = _capture_fixture()
    kwargs = {
        "assessment_occurrence_id": "assessment-retry",
        "capture_occurrence_ref": capture.capture_occurrence_id,
        "evidence_as_of_ts_utc": datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    }
    first = append_assessment(owner, **kwargs)
    assert append_assessment(owner, **kwargs) == first
    _add_observation(owner, capture, resolver)
    with pytest.raises((TypeError, ValueError)):
        append_assessment(
            owner,
            assessment_occurrence_id="assessment-retry",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
        )


def test_assessment_does_not_claim_exact_count_finality_health_or_provider_absence() -> None:
    owner, capture, _, _ = _capture_fixture()
    stored = append_assessment(
        owner,
        assessment_occurrence_id="assessment-nonclaims",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    for forbidden in ("exact_count", "final", "outage", "provider_event_absence", "healthy"):
        assert not hasattr(stored, forbidden)


@pytest.mark.parametrize("supersedes", ["missing-assessment", "assessment-self"])
def test_broken_or_self_supersession_fails_closed(supersedes: str) -> None:
    owner, capture, _, _ = _capture_fixture()
    with pytest.raises((TypeError, ValueError, KeyError)):
        append_assessment(
            owner,
            assessment_occurrence_id="assessment-self",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
            supersedes_assessment_ref=supersedes,
        )


def test_non_immediate_supersession_fails_closed() -> None:
    owner, capture, _, resolver = _capture_fixture()
    first = append_assessment(
        owner,
        assessment_occurrence_id="assessment-first",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    _add_observation(owner, capture, resolver)
    append_assessment(
        owner,
        assessment_occurrence_id="assessment-second",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
        supersedes_assessment_ref=first.assessment_occurrence_id,
    )
    with pytest.raises((TypeError, ValueError, KeyError)):
        append_assessment(
            owner,
            assessment_occurrence_id="assessment-third",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, tzinfo=UTC),
            supersedes_assessment_ref=first.assessment_occurrence_id,
        )
