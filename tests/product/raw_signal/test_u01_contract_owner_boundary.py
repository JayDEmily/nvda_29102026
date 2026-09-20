from __future__ import annotations

import inspect
from dataclasses import MISSING, fields, is_dataclass
from datetime import datetime
from typing import Any

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
    as_mapping,
    assessment_contract,
    build_owner,
    capture_contract,
    observation,
    policy,
    relation_contract,
    required_symbol,
)

from nvda_desk.raw_signal_occurrence_truth import api

CONTRACT_SHAPES: dict[str, dict[str, bool]] = {
    "CaptureScopePolicyV1": {
        "concept_id": True,
        "contract_id": True,
        "units": True,
        "scope_policy_id": True,
        "scope_policy_version": True,
        "activation_ts_utc": True,
        "deactivation_ts_utc": False,
        "eligibility_policy_ref": True,
    },
    "ScheduledCaptureOccurrenceV1": {
        "concept_id": True,
        "contract_id": True,
        "units": True,
        "capture_occurrence_id": True,
        "scope_policy_ref": True,
        "slot_start_utc": True,
        "slot_end_utc": True,
    },
    "RawObservationOccurrenceV1": {
        "concept_id": True,
        "contract_id": True,
        "observation_occurrence_id": True,
        "delivery_artifact_ref": True,
        "source_provider": True,
        "native_record": True,
        "source_product_api": False,
        "source_endpoint_callback": False,
        "native_identifier": False,
        "native_tick_series_identifier": False,
        "source_variant": False,
        "subject_instrument": False,
        "native_units": False,
        "availability_session": False,
        "source_status_native": False,
        "revision_vintage_native": False,
        "received_ts_utc": True,
        "received_epoch_ns": False,
        "ingestion_sequence": True,
        "ingestion_sequence_scope": True,
        "source_temporal_kind": True,
        "source_timestamp_raw": False,
        "source_timezone_native": False,
        "market_timezone_iana": False,
        "market_session_native": False,
    },
    "CaptureReceiptEvidenceRelationV1": {
        "concept_id": True,
        "contract_id": True,
        "units": True,
        "observation_occurrence_ref": True,
        "capture_occurrence_ref": True,
        "scope_policy_ref": True,
        "received_ts_utc": True,
        "relation_role": True,
    },
    "CaptureReceiptPresenceAssessmentV1": {
        "concept_id": True,
        "contract_id": True,
        "units": True,
        "assessment_occurrence_id": True,
        "capture_occurrence_ref": True,
        "outcome": True,
        "evidence_as_of_ts_utc": True,
        "supersedes_assessment_ref": False,
    },
}


REQUIRED_FIELD_CASES = [
    (name, field)
    for name, shape in CONTRACT_SHAPES.items()
    for field, required in shape.items()
    if required
]

UTC_FIELD_CASES = [
    ("CaptureScopePolicyV1", "activation_ts_utc"),
    ("ScheduledCaptureOccurrenceV1", "slot_start_utc"),
    ("ScheduledCaptureOccurrenceV1", "slot_end_utc"),
    ("RawObservationOccurrenceV1", "received_ts_utc"),
    ("CaptureReceiptEvidenceRelationV1", "received_ts_utc"),
    ("CaptureReceiptPresenceAssessmentV1", "evidence_as_of_ts_utc"),
]


def _constructor_shape(cls: type[Any]) -> dict[str, bool]:
    model_fields = getattr(cls, "model_fields", None)
    if model_fields is not None:
        return {name: bool(field.is_required()) for name, field in model_fields.items()}
    if is_dataclass(cls):
        return {
            field.name: field.default is MISSING and field.default_factory is MISSING
            for field in fields(cls)
        }
    shape: dict[str, bool] = {}
    for name, parameter in inspect.signature(cls).parameters.items():
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        shape[name] = parameter.default is parameter.empty
    return shape


def _compatibility_violations(
    baseline: dict[str, bool], candidate: dict[str, bool]
) -> tuple[str, ...]:
    violations: list[str] = []
    for name, required in baseline.items():
        if name not in candidate:
            violations.append(f"removed:{name}")
        elif candidate[name] is not required:
            violations.append(f"requiredness:{name}")
    for name, required in candidate.items():
        if name not in baseline and required:
            violations.append(f"new-required:{name}")
    return tuple(violations)


def _specimens() -> dict[str, Any]:
    return {
        "CaptureScopePolicyV1": policy(),
        "ScheduledCaptureOccurrenceV1": capture_contract(),
        "RawObservationOccurrenceV1": observation(),
        "CaptureReceiptEvidenceRelationV1": relation_contract(),
        "CaptureReceiptPresenceAssessmentV1": assessment_contract(),
    }


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


@pytest.mark.parametrize("name", list(CONTRACT_SHAPES))
def test_each_v1_contract_preserves_requiredness_and_only_adds_optional_fields(name: str) -> None:
    baseline = CONTRACT_SHAPES[name]
    actual = _constructor_shape(required_symbol(name))
    assert _compatibility_violations(baseline, actual) == (), (name, baseline, actual)


def test_compatibility_rule_accepts_only_genuinely_optional_addition() -> None:
    baseline = {"required": True, "optional": False}
    assert _compatibility_violations(baseline, {**baseline, "new_optional": False}) == ()
    assert _compatibility_violations(baseline, {**baseline, "new_required": True}) == (
        "new-required:new_required",
    )
    assert _compatibility_violations(baseline, {"required": True}) == ("removed:optional",)
    assert _compatibility_violations(baseline, {"required": False, "optional": False}) == (
        "requiredness:required",
    )
    assert _compatibility_violations(baseline, {"required": True, "optional": True}) == (
        "requiredness:optional",
    )


@pytest.mark.parametrize(("name", "field"), REQUIRED_FIELD_CASES)
def test_required_field_rejects_null(name: str, field: str) -> None:
    cls = required_symbol(name)
    baseline = as_mapping(_specimens()[name])
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, field: None})


@pytest.mark.parametrize(("name", "field"), UTC_FIELD_CASES)
def test_utc_time_field_rejects_naive_datetime(name: str, field: str) -> None:
    cls = required_symbol(name)
    baseline = as_mapping(_specimens()[name])
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, field: datetime(2026, 9, 20, 12, 0)})


def test_lawful_optional_absence_remains_explicit() -> None:
    assert policy(deactivation_ts_utc=None).deactivation_ts_utc is None
    observed = observation(native_identifier=None, native_units=None, source_timezone_native=None)
    assert observed.native_identifier is None
    assert observed.native_units is None
    assert observed.source_timezone_native is None
    assert assessment_contract(supersedes_assessment_ref=None).supersedes_assessment_ref is None


@pytest.mark.parametrize(
    ("name", "mutations"),
    [
        ("CaptureScopePolicyV1", {"scope_policy_version": 0}),
        ("CaptureScopePolicyV1", {"units": "USD"}),
        ("ScheduledCaptureOccurrenceV1", {"units": "USD"}),
        ("RawObservationOccurrenceV1", {"source_temporal_kind": "fabricated"}),
        ("CaptureReceiptEvidenceRelationV1", {"relation_role": "contains_member"}),
        ("CaptureReceiptEvidenceRelationV1", {"units": "USD"}),
        ("CaptureReceiptPresenceAssessmentV1", {"outcome": "exactly_one"}),
        ("CaptureReceiptPresenceAssessmentV1", {"units": "USD"}),
    ],
)
def test_v1_discriminants_and_allowed_values_fail_closed(
    name: str, mutations: dict[str, Any]
) -> None:
    cls = required_symbol(name)
    with pytest.raises((TypeError, ValueError)):
        cls(**{**as_mapping(_specimens()[name]), **mutations})


@pytest.mark.parametrize(
    "field",
    [
        "delivery_artifact_ref",
        "source_provider",
        "native_record",
        "received_ts_utc",
        "ingestion_sequence",
        "ingestion_sequence_scope",
        "source_temporal_kind",
    ],
)
def test_observation_provenance_requiredness_cannot_be_weakened(field: str) -> None:
    cls = required_symbol("RawObservationOccurrenceV1")
    baseline = as_mapping(observation())
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, field: None})


@pytest.mark.parametrize(
    ("name", "field", "substitute"),
    [
        ("CaptureScopePolicyV1", "concept_id", POLICY_CONTRACT),
        ("CaptureScopePolicyV1", "contract_id", POLICY_CONCEPT),
        ("CaptureScopePolicyV1", "scope_policy_id", "capture-001"),
        ("ScheduledCaptureOccurrenceV1", "capture_occurrence_id", "scope-policy-001"),
        ("ScheduledCaptureOccurrenceV1", "scope_policy_ref", "capture-001"),
        ("RawObservationOccurrenceV1", "observation_occurrence_id", "delivery-001"),
        ("RawObservationOccurrenceV1", "delivery_artifact_ref", "observation-001"),
        ("RawObservationOccurrenceV1", "source_provider", "provider-native-001"),
        ("RawObservationOccurrenceV1", "native_identifier", "provider.fixture"),
        ("CaptureReceiptEvidenceRelationV1", "observation_occurrence_ref", "capture-001"),
        ("CaptureReceiptEvidenceRelationV1", "capture_occurrence_ref", "observation-001"),
        ("CaptureReceiptEvidenceRelationV1", "scope_policy_ref", "capture-001"),
        ("CaptureReceiptPresenceAssessmentV1", "assessment_occurrence_id", "capture-001"),
        ("CaptureReceiptPresenceAssessmentV1", "capture_occurrence_ref", "assessment-001"),
        ("CaptureReceiptPresenceAssessmentV1", "supersedes_assessment_ref", "capture-001"),
    ],
)
def test_identity_layers_reject_cross_layer_substitution(
    name: str, field: str, substitute: str
) -> None:
    cls = required_symbol(name)
    with pytest.raises((TypeError, ValueError)):
        cls(**{**as_mapping(_specimens()[name]), field: substitute})


@pytest.mark.parametrize(
    "field",
    [
        "workbook_alias",
        "run_id",
        "replay_id",
        "lineage_id",
        "packet_occurrence_id",
        "universal_id",
    ],
)
def test_unadmitted_identity_authority_fields_are_rejected(field: str) -> None:
    cls = required_symbol("CaptureScopePolicyV1")
    with pytest.raises((TypeError, ValueError)):
        cls(**{**as_mapping(policy()), field: f"unadmitted-{field}"})


def test_owner_uses_public_production_factory_with_separate_command_and_read_facets() -> None:
    assert not hasattr(api, "_build_test_owner")
    builder = required_symbol("create_owner")
    source = inspect.getsource(builder).lower()
    for forbidden in ("_build_test_owner", "test_mode", "proof_mode"):
        assert forbidden not in source

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


def test_policy_payload_keeps_concept_contract_and_occurrence_identity_separate() -> None:
    value = policy()
    assert value.concept_id == POLICY_CONCEPT
    assert value.contract_id == POLICY_CONTRACT
    assert value.scope_policy_id == "scope-policy-001"
    assert value.concept_id != value.contract_id != value.scope_policy_id
    assert value.units == "not_applicable"


def test_public_seam_does_not_activate_packet_kernel_or_downstream_consumer() -> None:
    source = inspect.getsource(api).lower()
    for forbidden in ("dmpv3", "p01", "k01", "downstream_consumer"):
        assert forbidden not in source
