from __future__ import annotations

import inspect

import pytest
from tests.product.raw_signal._support import (
    ASSESSMENT_CONCEPT,
    ASSESSMENT_CONTRACT,
    CAPTURE_CONCEPT,
    CAPTURE_CONTRACT,
    OBSERVATION_CONCEPT,
    OBSERVATION_CONTRACT,
    POLICY_CONCEPT,
    POLICY_CONTRACT,
    RELATION_CONCEPT,
    RELATION_CONTRACT,
    build_owner,
    policy,
    required_symbol,
)

from nvda_desk.raw_signal_occurrence_truth import api


def _as_mapping(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    pytest.fail(f"proof cannot inspect contract payload for {type(value)!r}")


def test_exact_five_v1_contract_symbols_are_public_and_distinct() -> None:
    expected = {
        "CaptureScopePolicyV1": (POLICY_CONCEPT, POLICY_CONTRACT),
        "ScheduledCaptureOccurrenceV1": (CAPTURE_CONCEPT, CAPTURE_CONTRACT),
        "RawObservationOccurrenceV1": (OBSERVATION_CONCEPT, OBSERVATION_CONTRACT),
        "CaptureReceiptEvidenceRelationV1": (RELATION_CONCEPT, RELATION_CONTRACT),
        "CaptureReceiptPresenceAssessmentV1": (ASSESSMENT_CONCEPT, ASSESSMENT_CONTRACT),
    }
    classes = {name: required_symbol(name) for name in expected}
    assert all(isinstance(cls, type) for cls in classes.values())
    assert len(set(classes.values())) == 5
    assert len({concept for concept, _ in expected.values()}) == 5
    assert len({contract for _, contract in expected.values()}) == 5


def test_policy_payload_keeps_concept_contract_and_occurrence_identity_separate() -> None:
    value = policy()
    assert value.concept_id == POLICY_CONCEPT
    assert value.contract_id == POLICY_CONTRACT
    assert value.scope_policy_id == "scope-policy-001"
    assert value.concept_id != value.contract_id != value.scope_policy_id
    assert value.units == "not_applicable"


def test_owner_exposes_separate_command_and_read_facets() -> None:
    owner = build_owner()
    assert owner.commands is not owner.reads
    for name in (
        "register_capture_scope_policy",
        "realise_scheduled_capture_occurrence",
        "admit_raw_observation_occurrence",
        "derive_capture_receipt_evidence_relation",
        "append_capture_receipt_presence_assessment",
        "reconcile_owed_slots",
    ):
        assert callable(getattr(owner.commands, name, None)), name
    for name in (
        "get_capture_scope_policy",
        "get_scheduled_capture_occurrence",
        "get_raw_observation_occurrence",
        "get_receipt_presence_assessment",
        "list_receipt_presence_assessments",
    ):
        assert callable(getattr(owner.reads, name, None)), name


def test_mandatory_structural_identity_cannot_be_null() -> None:
    cls = required_symbol("CaptureScopePolicyV1")
    with pytest.raises((TypeError, ValueError)):
        cls(
            concept_id=POLICY_CONCEPT,
            contract_id=POLICY_CONTRACT,
            units="not_applicable",
            scope_policy_id=None,
            scope_policy_version=1,
            activation_ts_utc="2026-09-20T12:00:00Z",
            deactivation_ts_utc=None,
            eligibility_policy_ref="eligibility:v1",
        )


def test_v1_contract_rejects_unadmitted_authority_fields() -> None:
    cls = required_symbol("CaptureScopePolicyV1")
    kwargs = _as_mapping(policy())
    kwargs["dmpv3_packet_id"] = "packet-1"
    kwargs["universal_id"] = "all-meanings-1"
    with pytest.raises((TypeError, ValueError)):
        cls(**kwargs)


def test_current_v1_payload_cannot_silently_drop_or_retype_required_semantics() -> None:
    cls = required_symbol("CaptureScopePolicyV1")
    baseline = _as_mapping(policy())
    for field, invalid in (
        ("scope_policy_version", None),
        ("activation_ts_utc", None),
        ("eligibility_policy_ref", None),
    ):
        mutated = {**baseline, field: invalid}
        with pytest.raises((TypeError, ValueError)):
            cls(**mutated)


def test_public_seam_does_not_activate_packet_kernel_or_downstream_consumer() -> None:
    source = inspect.getsource(api).lower()
    for forbidden in ("dmpv3", "p01", "k01", "downstream_consumer"):
        assert forbidden not in source
