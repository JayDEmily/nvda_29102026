from __future__ import annotations

import inspect
import os
import subprocess
import sys
import types
from collections.abc import Sequence
from dataclasses import MISSING, dataclass, fields, is_dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from itertools import permutations
from pathlib import Path
from typing import Annotated, Any, Literal, Union, get_args, get_origin, get_type_hints

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
    raw_signal_catalogue_id,
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
        "raw_signal_catalogue_ids": False,
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
    if (symbol, field, value) == (
        "RawObservationOccurrenceV1",
        "source_temporal_kind",
        "receipt_only",
    ):
        payload["source_timestamp_raw"] = None
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


@pytest.mark.parametrize(
    ("symbol", "field", "expected"),
    [(symbol, field, expected) for (symbol, field), expected in LITERAL_LAW.items()],
)
def test_finite_v1_discriminant_sets_are_exact(
    symbol: str, field: str, expected: frozenset[str]
) -> None:
    assert _declared_finite_values(symbol, field) == expected


@pytest.mark.parametrize(
    ("symbol", "field", "expected"),
    [
        (symbol, field, expected)
        for (symbol, field), values in LITERAL_LAW.items()
        for expected in sorted(values)
    ],
)
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


def _annotation_leaf_types(annotation: Any) -> set[Any]:
    """Collect semantic leaf types while ignoring container/optional wrappers."""

    origin = get_origin(annotation)
    if origin is Annotated:
        return _annotation_leaf_types(get_args(annotation)[0])
    if origin in (Union, types.UnionType):
        leaves: set[Any] = set()
        for item in get_args(annotation):
            if item is not type(None):
                leaves.update(_annotation_leaf_types(item))
        return leaves
    if origin is not None:
        leaves: set[Any] = set()
        for item in get_args(annotation):
            if item not in (type(None), Ellipsis):
                leaves.update(_annotation_leaf_types(item))
        return leaves
    return {annotation}


def _assert_exact_public_annotation(actual: Any, expected: Any, *, label: str) -> None:
    assert actual == expected, (label, actual, expected)
    leaves = _annotation_leaf_types(actual)
    assert not leaves.intersection({Any, object, str}), (label, actual, leaves)


def test_every_public_facet_declares_complete_exact_parameter_and_return_types() -> None:
    owner = build_owner()
    policy_cls = required_symbol("CaptureScopePolicyV1")
    capture_cls = required_symbol("ScheduledCaptureOccurrenceV1")
    observation_cls = required_symbol("RawObservationOccurrenceV1")
    relation_cls = required_symbol("CaptureReceiptEvidenceRelationV1")
    assessment_cls = required_symbol("CaptureReceiptPresenceAssessmentV1")
    capture_policy_ref = identity_type("ScheduledCaptureOccurrenceV1", "scope_policy_ref")
    capture_id = identity_type("ScheduledCaptureOccurrenceV1", "capture_occurrence_id")
    observation_id = identity_type("RawObservationOccurrenceV1", "observation_occurrence_id")
    assessment_id = identity_type("CaptureReceiptPresenceAssessmentV1", "assessment_occurrence_id")
    policy_id = identity_type("CaptureScopePolicyV1", "scope_policy_id")

    expected: list[tuple[Any, dict[str, Any]]] = [
        (
            owner.commands.register_capture_scope_policy,
            {"value": policy_cls, "return": policy_cls},
        ),
        (
            owner.commands.realise_scheduled_capture_occurrence,
            {
                "scope_policy_ref": capture_policy_ref,
                "capture_occurrence_id": capture_id,
                "slot_start_utc": datetime,
                "return": capture_cls,
            },
        ),
        (
            owner.commands.admit_raw_observation_occurrence,
            {"value": observation_cls, "return": observation_cls},
        ),
        (
            owner.commands.derive_capture_receipt_evidence_relation,
            {
                "observation_occurrence_ref": identity_type(
                    "CaptureReceiptEvidenceRelationV1", "observation_occurrence_ref"
                ),
                "capture_occurrence_ref": identity_type(
                    "CaptureReceiptEvidenceRelationV1", "capture_occurrence_ref"
                ),
                "scope_policy_ref": identity_type(
                    "CaptureReceiptEvidenceRelationV1", "scope_policy_ref"
                ),
                "return": relation_cls | None,
            },
        ),
        (
            owner.commands.append_capture_receipt_presence_assessment,
            {
                "assessment_occurrence_id": assessment_id,
                "capture_occurrence_ref": identity_type(
                    "CaptureReceiptPresenceAssessmentV1", "capture_occurrence_ref"
                ),
                "evidence_as_of_ts_utc": datetime,
                "supersedes_assessment_ref": identity_type(
                    "CaptureReceiptPresenceAssessmentV1", "supersedes_assessment_ref"
                )
                | None,
                "return": assessment_cls,
            },
        ),
        (
            owner.commands.reconcile_owed_slots,
            {
                "scope_policy_ref": capture_policy_ref,
                "slot_starts_utc": Sequence[datetime],
                "capture_occurrence_ids": Sequence[capture_id],
                "assessment_occurrence_ids": Sequence[assessment_id],
                "return": Sequence[assessment_cls],
            },
        ),
        (
            owner.reads.get_capture_scope_policy,
            {
                "scope_policy_id": policy_id,
                "scope_policy_version": int,
                "return": policy_cls | None,
            },
        ),
        (
            owner.reads.get_scheduled_capture_occurrence,
            {"capture_occurrence_id": capture_id, "return": capture_cls | None},
        ),
        (
            owner.reads.get_raw_observation_occurrence,
            {"observation_occurrence_id": observation_id, "return": observation_cls | None},
        ),
        (
            owner.reads.get_receipt_presence_assessment,
            {"assessment_occurrence_id": assessment_id, "return": assessment_cls | None},
        ),
        (
            owner.reads.list_receipt_presence_assessments,
            {
                "capture_occurrence_id": capture_id,
                "return": Sequence[assessment_cls],
            },
        ),
    ]

    for method, expected_hints in expected:
        signature = inspect.signature(method)
        assert all(
            parameter.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
            for parameter in signature.parameters.values()
        ), (method, signature)
        hints = get_type_hints(method)
        assert set(hints) == set(expected_hints), (method, hints, expected_hints)
        assert set(signature.parameters) == set(expected_hints) - {"return"}, (
            method,
            signature,
            expected_hints,
        )
        for name, expected_annotation in expected_hints.items():
            _assert_exact_public_annotation(
                hints[name], expected_annotation, label=f"{method}.{name}"
            )


def test_catalogue_id_field_annotation_contains_only_catalogue_identity() -> None:
    annotation = field_annotation("RawObservationOccurrenceV1", "raw_signal_catalogue_ids")
    assert _annotation_leaf_types(annotation) == {required_symbol("RawSignalCatalogueId")}


def test_raw_signal_catalogue_identity_is_separately_typed_and_range_bound() -> None:
    catalogue_cls = required_symbol("RawSignalCatalogueId")
    assert isinstance(catalogue_cls, type)
    assert type(raw_signal_catalogue_id("R001")) is catalogue_cls
    assert str(raw_signal_catalogue_id("R001")) == "R001"
    assert str(raw_signal_catalogue_id("R323")) == "R323"
    assert catalogue_cls is not identity_type(
        "RawObservationOccurrenceV1", "observation_occurrence_id"
    )
    assert catalogue_cls is not identity_type("RawObservationOccurrenceV1", "source_provider")
    assert catalogue_cls is not identity_type("RawObservationOccurrenceV1", "delivery_artifact_ref")


@pytest.mark.parametrize("bad_id", ["R000", "R324", "D001", "r001", "R01", "R001 "])
def test_raw_signal_catalogue_identity_rejects_noncanonical_values(bad_id: str) -> None:
    identity_cls = required_symbol("RawSignalCatalogueId")
    with pytest.raises((TypeError, ValueError)):
        identity_cls(bad_id)


def test_observation_can_carry_multiple_catalogue_ids_without_conflating_native_identity() -> None:
    value = observation(
        raw_signal_catalogue_ids=("R033", "R034"),
        native_identifier="provider-native-book-record-001",
        native_record={"Bid Size": 0, "Bid Price": 123.45678901234567},
    )
    assert tuple(str(item) for item in value.raw_signal_catalogue_ids) == ("R033", "R034")
    assert value.native_identifier == "provider-native-book-record-001"
    assert all(
        type(item) is required_symbol("RawSignalCatalogueId")
        for item in value.raw_signal_catalogue_ids
    )
    assert type(value.raw_signal_catalogue_ids[0]) is not type(value.observation_occurrence_id)
    assert type(value.raw_signal_catalogue_ids[0]) is not type(value.delivery_artifact_ref)


def test_catalogue_id_carriage_uses_absence_not_empty_or_duplicate_collections() -> None:
    assert observation(raw_signal_catalogue_ids=None).raw_signal_catalogue_ids is None
    cls = required_symbol("RawObservationOccurrenceV1")
    baseline = as_mapping(observation())
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, "raw_signal_catalogue_ids": ()})
    duplicate = raw_signal_catalogue_id("R034")
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, "raw_signal_catalogue_ids": (duplicate, duplicate)})


def test_catalogue_identity_cannot_substitute_for_provider_or_occurrence_identity_and_reverse() -> (
    None
):
    catalogue = raw_signal_catalogue_id("R034")
    with pytest.raises((TypeError, ValueError)):
        observation(observation_occurrence_id=catalogue)
    with pytest.raises((TypeError, ValueError)):
        observation(source_provider=catalogue)
    wrong = typed_identity("RawObservationOccurrenceV1", "observation_occurrence_id", "R034")
    cls = required_symbol("RawObservationOccurrenceV1")
    baseline = as_mapping(observation())
    with pytest.raises((TypeError, ValueError)):
        cls(**{**baseline, "raw_signal_catalogue_ids": (wrong,)})


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


def test_native_record_is_alias_safe_read_only_snapshot() -> None:
    source = {
        "Bid Price": "123.45",
        "Provider Null": None,
        "Nested": {"Levels": [1, 2]},
    }
    observed = observation(native_record=source)

    source["Bid Price"] = "999.99"
    source["Injected"] = "later"
    nested_source = source["Nested"]
    assert isinstance(nested_source, dict)
    nested_source["Levels"].append(3)

    assert observed.native_record["Bid Price"] == "123.45"
    assert "Injected" not in observed.native_record
    assert observed.native_record["Nested"] == {"Levels": [1, 2]}

    nested_read = observed.native_record["Nested"]
    assert isinstance(nested_read, dict)
    nested_read["Levels"].append(99)
    assert observed.native_record["Nested"] == {"Levels": [1, 2]}

    with pytest.raises(TypeError):
        observed.native_record["Bid Price"] = "888.88"


def test_public_identity_factories_construct_every_required_identity_layer() -> None:
    cases = (
        ("concept_id", "CaptureScopePolicyV1", "concept_id", POLICY_CONCEPT),
        ("contract_id", "CaptureScopePolicyV1", "contract_id", POLICY_CONTRACT),
        ("scope_policy_id", "CaptureScopePolicyV1", "scope_policy_id", "scope-policy-001"),
        (
            "eligibility_policy_ref",
            "CaptureScopePolicyV1",
            "eligibility_policy_ref",
            "eligibility-policy:fixture:v1",
        ),
        (
            "scope_policy_ref",
            "ScheduledCaptureOccurrenceV1",
            "scope_policy_ref",
            "scope-policy-001@1",
        ),
        (
            "capture_occurrence_id",
            "ScheduledCaptureOccurrenceV1",
            "capture_occurrence_id",
            "capture-001",
        ),
        (
            "observation_occurrence_id",
            "RawObservationOccurrenceV1",
            "observation_occurrence_id",
            "observation-001",
        ),
        (
            "assessment_occurrence_id",
            "CaptureReceiptPresenceAssessmentV1",
            "assessment_occurrence_id",
            "assessment-001",
        ),
        ("provider_id", "RawObservationOccurrenceV1", "source_provider", "provider.fixture"),
        (
            "delivery_artifact_ref",
            "RawObservationOccurrenceV1",
            "delivery_artifact_ref",
            "delivery-001",
        ),
        (
            "ingestion_sequence_scope",
            "RawObservationOccurrenceV1",
            "ingestion_sequence_scope",
            "collector.fixture",
        ),
    )

    for factory_name, symbol, field, opaque_value in cases:
        factory = required_symbol(factory_name)
        value = factory(opaque_value)
        assert type(value) is identity_type(symbol, field)
        assert str(value) == opaque_value


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


TYPECHECK_DIR = Path(__file__).resolve().parent / "typecheck"
TYPECHECK_POSITIVE = TYPECHECK_DIR / "public_seam_positive.py"
TYPECHECK_NEGATIVE = TYPECHECK_DIR / "public_seam_negative.py"


def _run_public_seam_mypy(path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    root = Path(__file__).resolve().parents[3]
    env["MYPYPATH"] = str(root / "src")
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--strict",
            "--disallow-any-expr",
            "--show-error-codes",
            "--no-error-summary",
            str(path),
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_public_command_and_read_facets_are_statically_typed_without_any() -> None:
    result = _run_public_seam_mypy(TYPECHECK_POSITIVE)
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_public_facet_rejects_cross_layer_static_type_substitution() -> None:
    source_lines = TYPECHECK_NEGATIVE.read_text(encoding="utf-8").splitlines()
    expected_lines = {
        number for number, line in enumerate(source_lines, start=1) if "STATIC_NEGATIVE" in line
    }
    assert len(expected_lines) == 15

    result = _run_public_seam_mypy(TYPECHECK_NEGATIVE)
    assert result.returncode != 0, "negative static-type specimen unexpectedly type-checked"
    reported_lines: set[int] = set()
    root = Path(__file__).resolve().parents[3]
    expected_path = TYPECHECK_NEGATIVE.resolve()
    for line in (result.stdout + result.stderr).splitlines():
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        reported_path = Path(parts[0])
        if not reported_path.is_absolute():
            reported_path = root / reported_path
        if reported_path.resolve() != expected_path:
            continue
        try:
            reported_lines.add(int(parts[1]))
        except ValueError:
            continue
    missing = expected_lines - reported_lines
    assert not missing, (missing, result.stdout, result.stderr)


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
