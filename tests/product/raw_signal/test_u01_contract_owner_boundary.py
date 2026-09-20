from __future__ import annotations

import inspect
from dataclasses import MISSING, dataclass, fields, is_dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from itertools import permutations
from typing import Any, Literal, get_args, get_origin

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
    field_annotation,
    identity_type,
    observation,
    policy,
    relation_contract,
    required_symbol,
    typed_identity,
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
    ("CaptureScopePolicyV1", "deactivation_ts_utc"),
    ("ScheduledCaptureOccurrenceV1", "slot_start_utc"),
    ("ScheduledCaptureOccurrenceV1", "slot_end_utc"),
    ("RawObservationOccurrenceV1", "received_ts_utc"),
    ("CaptureReceiptEvidenceRelationV1", "received_ts_utc"),
    ("CaptureReceiptPresenceAssessmentV1", "evidence_as_of_ts_utc"),
]

LITERAL_LAW: dict[tuple[str, str], frozenset[str]] = {
    ("CaptureScopePolicyV1", "units"): frozenset({"not_applicable"}),
    ("ScheduledCaptureOccurrenceV1", "units"): frozenset({"not_applicable"}),
    ("RawObservationOccurrenceV1", "source_temporal_kind"): frozenset(
        {"true_instant", "date_only", "receipt_only"}
    ),
    ("CaptureReceiptEvidenceRelationV1", "units"): frozenset({"not_applicable"}),
    ("CaptureReceiptEvidenceRelationV1", "relation_role"): frozenset(
        {"evidences_receipt_presence_only"}
    ),
    ("CaptureReceiptPresenceAssessmentV1", "units"): frozenset({"not_applicable"}),
    ("CaptureReceiptPresenceAssessmentV1", "outcome"): frozenset(
        {"unknown_not_established", "zero_received", "one_or_more_received"}
    ),
}

IDENTITY_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {
    "concept": tuple((name, "concept_id") for name in CONTRACT_SHAPES),
    "contract": tuple((name, "contract_id") for name in CONTRACT_SHAPES),
    "policy_id": (("CaptureScopePolicyV1", "scope_policy_id"),),
    "eligibility_policy": (("CaptureScopePolicyV1", "eligibility_policy_ref"),),
    "policy_ref": (
        ("ScheduledCaptureOccurrenceV1", "scope_policy_ref"),
        ("CaptureReceiptEvidenceRelationV1", "scope_policy_ref"),
    ),
    "capture": (
        ("ScheduledCaptureOccurrenceV1", "capture_occurrence_id"),
        ("CaptureReceiptEvidenceRelationV1", "capture_occurrence_ref"),
        ("CaptureReceiptPresenceAssessmentV1", "capture_occurrence_ref"),
    ),
    "observation": (
        ("RawObservationOccurrenceV1", "observation_occurrence_id"),
        ("CaptureReceiptEvidenceRelationV1", "observation_occurrence_ref"),
    ),
    "assessment": (
        ("CaptureReceiptPresenceAssessmentV1", "assessment_occurrence_id"),
        ("CaptureReceiptPresenceAssessmentV1", "supersedes_assessment_ref"),
    ),
    "provider": (("RawObservationOccurrenceV1", "source_provider"),),
    "delivery": (("RawObservationOccurrenceV1", "delivery_artifact_ref"),),
    "ingestion_scope": (("RawObservationOccurrenceV1", "ingestion_sequence_scope"),),
}

ACTIVE_IDENTITY_TARGETS = tuple(
    (group, symbol, field)
    for group, members in IDENTITY_GROUPS.items()
    for symbol, field in members[:1]
)


@dataclass(frozen=True)
class _ForeignRunId:
    value: str


@dataclass(frozen=True)
class _ForeignReplayId:
    value: str


@dataclass(frozen=True)
class _ForeignPacketOccurrenceId:
    value: str


@dataclass(frozen=True)
class _ForeignWorkbookAlias:
    value: str


@dataclass(frozen=True)
class _ForeignLineageId:
    value: str


FOREIGN_IDENTITY_TYPES = (
    _ForeignRunId,
    _ForeignReplayId,
    _ForeignPacketOccurrenceId,
    _ForeignWorkbookAlias,
    _ForeignLineageId,
)


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
    for name in candidate:
        if name not in baseline:
            violations.append(f"unproved-extra:{name}")
    return tuple(violations)


def _specimens() -> dict[str, Any]:
    return {
        "CaptureScopePolicyV1": policy(),
        "ScheduledCaptureOccurrenceV1": capture_contract(),
        "RawObservationOccurrenceV1": observation(),
        "CaptureReceiptEvidenceRelationV1": relation_contract(),
        "CaptureReceiptPresenceAssessmentV1": assessment_contract(),
    }


def _declared_finite_values(symbol: str, field: str) -> frozenset[str]:
    annotation = field_annotation(symbol, field)
    origin = get_origin(annotation)
    if origin is Literal:
        return frozenset(str(value) for value in get_args(annotation))
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return frozenset(str(item.value) for item in annotation)
    pytest.fail(
        f"{symbol}.{field} must expose its finite v1 allowed set through Literal/Enum typing"
    )


def _construct(symbol: str, field: str, value: Any) -> Any:
    cls = required_symbol(symbol)
    payload = as_mapping(_specimens()[symbol])
    payload[field] = value
    return cls(**payload)


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
def test_each_v1_contract_preserves_exact_v1_field_set_and_requiredness(name: str) -> None:
    baseline = CONTRACT_SHAPES[name]
    actual = _constructor_shape(required_symbol(name))
    assert _compatibility_violations(baseline, actual) == (), (name, baseline, actual)


def test_compatibility_rule_fails_closed_on_unproved_v1_additions() -> None:
    baseline = {"required": True, "optional": False}
    assert _compatibility_violations(baseline, baseline.copy()) == ()
    assert _compatibility_violations(baseline, {**baseline, "new_optional": False}) == (
        "unproved-extra:new_optional",
    )
    assert _compatibility_violations(baseline, {**baseline, "new_required": True}) == (
        "unproved-extra:new_required",
    )
    assert _compatibility_violations(baseline, {"required": True}) == ("removed:optional",)
    assert _compatibility_violations(baseline, {"required": False, "optional": False}) == (
        "requiredness:required",
    )
    assert _compatibility_violations(baseline, {"required": True, "optional": True}) == (
        "requiredness:optional",
    )


@pytest.mark.parametrize("name", tuple(CONTRACT_SHAPES))
def test_every_v1_contract_rejects_unproved_extra_keyword_material(name: str) -> None:
    cls = required_symbol(name)
    baseline = as_mapping(_specimens()[name])
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, "__unproved_v1_extension__": "must-not-be-accepted"})


@pytest.mark.parametrize(("name", "field"), REQUIRED_FIELD_CASES)
def test_required_field_rejects_null(name: str, field: str) -> None:
    cls = required_symbol(name)
    baseline = as_mapping(_specimens()[name])
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, field: None})


@pytest.mark.parametrize(("name", "field"), UTC_FIELD_CASES)
def test_every_v1_utc_field_rejects_naive_datetime(name: str, field: str) -> None:
    baseline = as_mapping(_specimens()[name])
    if field == "deactivation_ts_utc":
        assert baseline[field] is not None
    with pytest.raises((TypeError, ValueError)):
        required_symbol(name)(**{**baseline, field: datetime(2026, 9, 20, 12, 0)})


@pytest.mark.parametrize(("name", "field"), UTC_FIELD_CASES)
def test_every_v1_utc_field_rejects_aware_non_utc_offset(name: str, field: str) -> None:
    baseline = as_mapping(_specimens()[name])
    if field == "deactivation_ts_utc":
        assert baseline[field] is not None
    non_utc = datetime(
        2026,
        9,
        20,
        22,
        0,
        tzinfo=timezone(timedelta(hours=10)),
    )
    with pytest.raises((TypeError, ValueError)):
        required_symbol(name)(**{**baseline, field: non_utc})


@pytest.mark.parametrize(("symbol", "field", "expected"), [
    (symbol, field, expected) for (symbol, field), expected in LITERAL_LAW.items()
])
def test_finite_v1_discriminant_sets_are_exact(
    symbol: str, field: str, expected: frozenset[str]
) -> None:
    assert _declared_finite_values(symbol, field) == expected


@pytest.mark.parametrize(("symbol", "field", "expected"), [
    (symbol, field, expected)
    for (symbol, field), values in LITERAL_LAW.items()
    for expected in sorted(values)
])
def test_every_allowed_v1_discriminant_value_is_accepted(
    symbol: str, field: str, expected: str
) -> None:
    assert str(getattr(_construct(symbol, field, expected), field)) == expected


@pytest.mark.parametrize(
    ("name", "field", "invalid"),
    [
        ("CaptureScopePolicyV1", "units", "USD"),
        ("ScheduledCaptureOccurrenceV1", "units", "USD"),
        ("RawObservationOccurrenceV1", "source_temporal_kind", "fabricated"),
        ("CaptureReceiptEvidenceRelationV1", "units", "USD"),
        ("CaptureReceiptEvidenceRelationV1", "relation_role", "contains_member"),
        ("CaptureReceiptPresenceAssessmentV1", "units", "USD"),
        ("CaptureReceiptPresenceAssessmentV1", "outcome", "exactly_one"),
    ],
)
def test_values_outside_v1_discriminant_sets_fail_closed(
    name: str, field: str, invalid: str
) -> None:
    with pytest.raises((TypeError, ValueError)):
        _construct(name, field, invalid)


def test_policy_version_must_be_positive() -> None:
    with pytest.raises((TypeError, ValueError)):
        _construct("CaptureScopePolicyV1", "scope_policy_version", 0)


@pytest.mark.parametrize(
    ("symbol", "field", "exact_value"),
    [
        ("CaptureScopePolicyV1", "concept_id", POLICY_CONCEPT),
        ("CaptureScopePolicyV1", "contract_id", POLICY_CONTRACT),
        ("ScheduledCaptureOccurrenceV1", "concept_id", CAPTURE_CONCEPT),
        ("ScheduledCaptureOccurrenceV1", "contract_id", CAPTURE_CONTRACT),
        ("RawObservationOccurrenceV1", "concept_id", OBSERVATION_CONCEPT),
        ("RawObservationOccurrenceV1", "contract_id", OBSERVATION_CONTRACT),
        ("CaptureReceiptEvidenceRelationV1", "concept_id", RELATION_CONCEPT),
        ("CaptureReceiptEvidenceRelationV1", "contract_id", RELATION_CONTRACT),
        ("CaptureReceiptPresenceAssessmentV1", "concept_id", ASSESSMENT_CONCEPT),
        ("CaptureReceiptPresenceAssessmentV1", "contract_id", ASSESSMENT_CONTRACT),
    ],
)
def test_concept_and_contract_discriminants_reject_same_type_wrong_value(
    symbol: str, field: str, exact_value: str
) -> None:
    wrong = typed_identity(symbol, field, f"wrong::{exact_value}")
    with pytest.raises((TypeError, ValueError)):
        _construct(symbol, field, wrong)


def test_all_active_identity_layers_use_runtime_distinct_opaque_types() -> None:
    representative_types: dict[str, type[Any]] = {}
    for group, members in IDENTITY_GROUPS.items():
        member_types = {identity_type(symbol, field) for symbol, field in members}
        assert len(member_types) == 1, (group, member_types)
        identity_cls = next(iter(member_types))
        assert identity_cls is not str
        representative_types[group] = identity_cls
    assert len(set(representative_types.values())) == len(representative_types)


@pytest.mark.parametrize(
    (
        "target_group",
        "target_symbol",
        "target_field",
        "source_group",
        "source_symbol",
        "source_field",
    ),
    [
        (*target, *source)
        for target, source in permutations(ACTIVE_IDENTITY_TARGETS, 2)
        if target[0] != source[0]
    ],
)
def test_same_opaque_payload_rejects_every_active_cross_layer_identity_substitution(
    target_group: str,
    target_symbol: str,
    target_field: str,
    source_group: str,
    source_symbol: str,
    source_field: str,
) -> None:
    del target_group, source_group
    substitute = typed_identity(source_symbol, source_field, "same-opaque-payload")
    with pytest.raises((TypeError, ValueError)):
        _construct(target_symbol, target_field, substitute)


@pytest.mark.parametrize(("target_group", "target_symbol", "target_field"), ACTIVE_IDENTITY_TARGETS)
@pytest.mark.parametrize("foreign_type", FOREIGN_IDENTITY_TYPES)
def test_inactive_identity_layer_value_cannot_substitute_for_active_identity(
    target_group: str,
    target_symbol: str,
    target_field: str,
    foreign_type: type[Any],
) -> None:
    del target_group
    with pytest.raises((TypeError, ValueError)):
        _construct(target_symbol, target_field, foreign_type("same-opaque-payload"))


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


def test_lawful_optional_absence_and_conditional_null_law_are_explicit() -> None:
    assert policy(deactivation_ts_utc=None).deactivation_ts_utc is None
    observed = observation(
        native_identifier=None,
        native_units=None,
        source_product_api=None,
        source_endpoint_callback=None,
        native_tick_series_identifier=None,
        source_variant=None,
        subject_instrument=None,
        availability_session=None,
        source_status_native=None,
        revision_vintage_native=None,
        received_epoch_ns=None,
        source_temporal_kind="receipt_only",
        source_timestamp_raw=None,
        source_timezone_native=None,
        market_timezone_iana=None,
        market_session_native=None,
    )
    for field in CONTRACT_SHAPES["RawObservationOccurrenceV1"]:
        if CONTRACT_SHAPES["RawObservationOccurrenceV1"][field] is False:
            assert getattr(observed, field) is None
    assert assessment_contract(supersedes_assessment_ref=None).supersedes_assessment_ref is None


@pytest.mark.parametrize(
    ("kind", "raw"),
    [("true_instant", None), ("date_only", None), ("receipt_only", "not-absent")],
)
def test_temporal_discriminant_controls_source_timestamp_null_law(
    kind: str, raw: str | None
) -> None:
    with pytest.raises((TypeError, ValueError)):
        observation(source_temporal_kind=kind, source_timestamp_raw=raw)


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
    assert str(value.concept_id) == POLICY_CONCEPT
    assert str(value.contract_id) == POLICY_CONTRACT
    assert str(value.scope_policy_id) == "scope-policy-001"
    assert type(value.concept_id) is not type(value.contract_id)
    assert type(value.contract_id) is not type(value.scope_policy_id)
    assert value.units == "not_applicable"


def test_public_seam_does_not_activate_packet_kernel_or_downstream_consumer() -> None:
    source = inspect.getsource(api).lower()
    for forbidden in ("dmpv3", "p01", "k01", "downstream_consumer"):
        assert forbidden not in source
