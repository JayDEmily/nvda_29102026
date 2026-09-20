"""Proof-only fixtures for Raw Signal Occurrence Truth.

This module constructs authority-fixed specimen inputs and locates the production public seam.
It may inject technical proof dependencies, but it must not decide Raw Signal outcomes.
"""

from __future__ import annotations

import inspect
import types
from collections.abc import Callable
from dataclasses import fields, is_dataclass, replace
from datetime import UTC, datetime
from typing import Annotated, Any, Union, get_args, get_origin

import pytest

from nvda_desk.raw_signal_occurrence_truth import api

POLICY_CONCEPT = "raw_signal.capture_scope_policy"
POLICY_CONTRACT = "nvda.raw_signal.CaptureScopePolicy.v1"
CAPTURE_CONCEPT = "raw_signal.scheduled_capture_occurrence"
CAPTURE_CONTRACT = "nvda.raw_signal.ScheduledCaptureOccurrence.v1"
OBSERVATION_CONCEPT = "raw_signal.raw_observation_occurrence"
OBSERVATION_CONTRACT = "nvda.raw_signal.RawObservationOccurrence.v1"
RELATION_CONCEPT = "raw_signal.capture_receipt_evidence_relation"
RELATION_CONTRACT = "nvda.raw_signal.CaptureReceiptEvidenceRelation.v1"
ASSESSMENT_CONCEPT = "raw_signal.capture_receipt_presence_assessment"
ASSESSMENT_CONTRACT = "nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"


def required_symbol(name: str) -> Any:
    if not hasattr(api, name):
        pytest.fail(f"required Raw Signal public-seam symbol is not implemented: {name}")
    return getattr(api, name)


def build_owner(**kwargs: Any) -> Any:
    """Construct the real production owner through its public factory."""

    builder = required_symbol("create_owner")
    owner = builder(**kwargs)
    if not hasattr(owner, "commands") or not hasattr(owner, "reads"):
        pytest.fail("create_owner must return separate commands and reads facets")
    return owner


def as_mapping(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if is_dataclass(value):
        return {field.name: getattr(value, field.name) for field in fields(value)}
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    pytest.fail(f"proof fixture cannot inspect contract payload for {type(value)!r}")


def copy_with(value: Any, **changes: Any) -> Any:
    if hasattr(value, "model_copy"):
        return value.model_copy(update=changes)
    if is_dataclass(value):
        return replace(value, **changes)
    pytest.fail(f"proof fixture cannot create a modified copy of {type(value)!r}")


def _unwrap_optional(annotation: Any) -> Any:
    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        args = tuple(item for item in get_args(annotation) if item is not type(None))
        if len(args) == 1:
            return _unwrap_optional(args[0])
    return annotation


def field_annotation(symbol: str, field: str) -> Any:
    """Return the concrete public annotation for one contract field."""

    cls = required_symbol(symbol)
    model_fields = getattr(cls, "model_fields", None)
    if model_fields is not None and field in model_fields:
        return _unwrap_optional(model_fields[field].annotation)
    if is_dataclass(cls):
        for item in fields(cls):
            if item.name == field:
                return _unwrap_optional(item.type)
    parameter = inspect.signature(cls).parameters.get(field)
    if parameter is None or parameter.annotation is inspect.Parameter.empty:
        pytest.fail(f"{symbol}.{field} has no inspectable public type annotation")
    return _unwrap_optional(parameter.annotation)


def identity_type(symbol: str, field: str) -> type[Any]:
    """Require a runtime-distinct opaque identity type for an identity field."""

    annotation = field_annotation(symbol, field)
    if annotation in (str, Any, object) or not isinstance(annotation, type):
        pytest.fail(
            f"{symbol}.{field} must expose a concrete layer-specific identity type, "
            f"not {annotation!r}"
        )
    return annotation


def typed_identity(symbol: str, field: str, opaque_payload: str) -> Any:
    """Construct one identity through the public layer-specific type boundary."""

    identity_cls = identity_type(symbol, field)
    try:
        value = identity_cls(opaque_payload)
    except Exception as exc:  # pragma: no cover - error detail belongs to implementation
        pytest.fail(
            f"cannot construct {symbol}.{field} identity from opaque payload: {exc}"
        )
    if type(value) is str:
        pytest.fail(f"{symbol}.{field} collapses to the universal runtime str type")
    return value


def _identity(symbol: str, field: str, value: Any) -> Any:
    if isinstance(value, str):
        return typed_identity(symbol, field, value)
    return value


def policy_ref(scope_policy_id: str = "scope-policy-001", version: int = 1) -> Any:
    return typed_identity(
        "ScheduledCaptureOccurrenceV1",
        "scope_policy_ref",
        f"{scope_policy_id}@{version}",
    )


def policy(
    *,
    scope_policy_id: Any = "scope-policy-001",
    scope_policy_version: int = 1,
    activation_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    deactivation_ts_utc: datetime | None = datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
    eligibility_policy_ref: Any = "eligibility-policy:fixture:v1",
) -> Any:
    cls = required_symbol("CaptureScopePolicyV1")
    return cls(
        concept_id=_identity("CaptureScopePolicyV1", "concept_id", POLICY_CONCEPT),
        contract_id=_identity("CaptureScopePolicyV1", "contract_id", POLICY_CONTRACT),
        units="not_applicable",
        scope_policy_id=_identity("CaptureScopePolicyV1", "scope_policy_id", scope_policy_id),
        scope_policy_version=scope_policy_version,
        activation_ts_utc=activation_ts_utc,
        deactivation_ts_utc=deactivation_ts_utc,
        eligibility_policy_ref=_identity(
            "CaptureScopePolicyV1", "eligibility_policy_ref", eligibility_policy_ref
        ),
    )


def capture_contract(
    *,
    capture_occurrence_id: Any = "capture-001",
    scope_policy_ref: Any = "scope-policy-001@1",
    slot_start_utc: datetime = datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    slot_end_utc: datetime = datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
) -> Any:
    cls = required_symbol("ScheduledCaptureOccurrenceV1")
    return cls(
        concept_id=_identity("ScheduledCaptureOccurrenceV1", "concept_id", CAPTURE_CONCEPT),
        contract_id=_identity("ScheduledCaptureOccurrenceV1", "contract_id", CAPTURE_CONTRACT),
        units="not_applicable",
        capture_occurrence_id=_identity(
            "ScheduledCaptureOccurrenceV1", "capture_occurrence_id", capture_occurrence_id
        ),
        scope_policy_ref=_identity(
            "ScheduledCaptureOccurrenceV1", "scope_policy_ref", scope_policy_ref
        ),
        slot_start_utc=slot_start_utc,
        slot_end_utc=slot_end_utc,
    )


def observation(
    *,
    observation_occurrence_id: Any = "observation-001",
    delivery_artifact_ref: Any = "delivery-001",
    source_provider: Any = "provider.fixture",
    native_identifier: str | None = "provider-native-001",
    native_record: dict[str, Any] | None = None,
    source_product_api: str | None = None,
    source_endpoint_callback: str | None = None,
    native_tick_series_identifier: str | None = None,
    source_variant: str | None = None,
    subject_instrument: str | None = "NVDA",
    native_units: str | None = "USD",
    availability_session: str | None = None,
    source_status_native: str | None = None,
    revision_vintage_native: str | None = None,
    received_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, 5, 123456, tzinfo=UTC),
    received_epoch_ns: int | None = None,
    ingestion_sequence: int = 1,
    ingestion_sequence_scope: Any = "collector.fixture",
    source_temporal_kind: str = "true_instant",
    source_timestamp_raw: str | None = "2026-09-20T12:00:04.900000Z",
    source_timezone_native: str | None = "UTC",
    market_timezone_iana: str | None = None,
    market_session_native: str | None = None,
) -> Any:
    cls = required_symbol("RawObservationOccurrenceV1")
    return cls(
        concept_id=_identity("RawObservationOccurrenceV1", "concept_id", OBSERVATION_CONCEPT),
        contract_id=_identity(
            "RawObservationOccurrenceV1", "contract_id", OBSERVATION_CONTRACT
        ),
        observation_occurrence_id=_identity(
            "RawObservationOccurrenceV1", "observation_occurrence_id", observation_occurrence_id
        ),
        delivery_artifact_ref=_identity(
            "RawObservationOccurrenceV1", "delivery_artifact_ref", delivery_artifact_ref
        ),
        source_provider=_identity("RawObservationOccurrenceV1", "source_provider", source_provider),
        native_record=native_record
        if native_record is not None
        else {"Bid Price": "123.45", "Provider Null": None},
        source_product_api=source_product_api,
        source_endpoint_callback=source_endpoint_callback,
        native_identifier=native_identifier,
        native_tick_series_identifier=native_tick_series_identifier,
        source_variant=source_variant,
        subject_instrument=subject_instrument,
        native_units=native_units,
        availability_session=availability_session,
        source_status_native=source_status_native,
        revision_vintage_native=revision_vintage_native,
        received_ts_utc=received_ts_utc,
        received_epoch_ns=received_epoch_ns,
        ingestion_sequence=ingestion_sequence,
        ingestion_sequence_scope=_identity(
            "RawObservationOccurrenceV1", "ingestion_sequence_scope", ingestion_sequence_scope
        ),
        source_temporal_kind=source_temporal_kind,
        source_timestamp_raw=source_timestamp_raw,
        source_timezone_native=source_timezone_native,
        market_timezone_iana=market_timezone_iana,
        market_session_native=market_session_native,
    )


def relation_contract(
    *,
    observation_occurrence_ref: Any = "observation-001",
    capture_occurrence_ref: Any = "capture-001",
    scope_policy_ref: Any = "scope-policy-001@1",
    received_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, 5, 123456, tzinfo=UTC),
    relation_role: str = "evidences_receipt_presence_only",
) -> Any:
    cls = required_symbol("CaptureReceiptEvidenceRelationV1")
    return cls(
        concept_id=_identity(
            "CaptureReceiptEvidenceRelationV1", "concept_id", RELATION_CONCEPT
        ),
        contract_id=_identity(
            "CaptureReceiptEvidenceRelationV1", "contract_id", RELATION_CONTRACT
        ),
        units="not_applicable",
        observation_occurrence_ref=_identity(
            "CaptureReceiptEvidenceRelationV1",
            "observation_occurrence_ref",
            observation_occurrence_ref,
        ),
        capture_occurrence_ref=_identity(
            "CaptureReceiptEvidenceRelationV1", "capture_occurrence_ref", capture_occurrence_ref
        ),
        scope_policy_ref=_identity(
            "CaptureReceiptEvidenceRelationV1", "scope_policy_ref", scope_policy_ref
        ),
        received_ts_utc=received_ts_utc,
        relation_role=relation_role,
    )


def assessment_contract(
    *,
    assessment_occurrence_id: Any = "assessment-001",
    capture_occurrence_ref: Any = "capture-001",
    outcome: str = "zero_received",
    evidence_as_of_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    supersedes_assessment_ref: Any | None = None,
) -> Any:
    cls = required_symbol("CaptureReceiptPresenceAssessmentV1")
    return cls(
        concept_id=_identity(
            "CaptureReceiptPresenceAssessmentV1", "concept_id", ASSESSMENT_CONCEPT
        ),
        contract_id=_identity(
            "CaptureReceiptPresenceAssessmentV1", "contract_id", ASSESSMENT_CONTRACT
        ),
        units="not_applicable",
        assessment_occurrence_id=_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "assessment_occurrence_id",
            assessment_occurrence_id,
        ),
        capture_occurrence_ref=_identity(
            "CaptureReceiptPresenceAssessmentV1", "capture_occurrence_ref", capture_occurrence_ref
        ),
        outcome=outcome,
        evidence_as_of_ts_utc=evidence_as_of_ts_utc,
        supersedes_assessment_ref=None
        if supersedes_assessment_ref is None
        else _identity(
            "CaptureReceiptPresenceAssessmentV1",
            "supersedes_assessment_ref",
            supersedes_assessment_ref,
        ),
    )


def register_policy(owner: Any, value: Any | None = None) -> Any:
    return owner.commands.register_capture_scope_policy(value or policy())


def realise_capture(
    owner: Any,
    *,
    scope_policy_ref: Any = "scope-policy-001@1",
    slot_start_utc: datetime = datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    capture_occurrence_id: Any = "capture-001",
    **unexpected: Any,
) -> Any:
    return owner.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=_identity(
            "ScheduledCaptureOccurrenceV1", "scope_policy_ref", scope_policy_ref
        ),
        slot_start_utc=slot_start_utc,
        capture_occurrence_id=_identity(
            "ScheduledCaptureOccurrenceV1", "capture_occurrence_id", capture_occurrence_id
        ),
        **unexpected,
    )


def admit_observation(owner: Any, value: Any | None = None) -> Any:
    return owner.commands.admit_raw_observation_occurrence(value or observation())


def append_assessment(
    owner: Any,
    *,
    assessment_occurrence_id: Any,
    capture_occurrence_ref: Any,
    evidence_as_of_ts_utc: datetime,
    supersedes_assessment_ref: Any | None = None,
    **unexpected: Any,
) -> Any:
    """Ask M00 to derive and append the assessment outcome from visible evidence."""

    return owner.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "assessment_occurrence_id",
            assessment_occurrence_id,
        ),
        capture_occurrence_ref=_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "capture_occurrence_ref",
            capture_occurrence_ref,
        ),
        evidence_as_of_ts_utc=evidence_as_of_ts_utc,
        supersedes_assessment_ref=None
        if supersedes_assessment_ref is None
        else _identity(
            "CaptureReceiptPresenceAssessmentV1",
            "supersedes_assessment_ref",
            supersedes_assessment_ref,
        ),
        **unexpected,
    )


def eligible(_: Any, __: Any) -> bool:
    return True


def ineligible(_: Any, __: Any) -> bool:
    return False


def sequence_source(*values: str) -> Callable[[], str]:
    remaining = list(values)

    def next_value() -> str:
        if not remaining:
            raise AssertionError("proof opaque-ID source exhausted")
        return remaining.pop(0)

    return next_value
