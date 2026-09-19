"""Proof-only fixtures for Raw Signal Occurrence Truth.

This module constructs authority-fixed specimen inputs and locates the production public seam.
It must not decide Raw Signal outcomes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import is_dataclass, replace
from datetime import UTC, datetime
from typing import Any

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
    builder = required_symbol("_build_test_owner")
    owner = builder(**kwargs)
    if not hasattr(owner, "commands") or not hasattr(owner, "reads"):
        pytest.fail("_build_test_owner must return separate commands and reads facets")
    return owner


def copy_with(value: Any, **changes: Any) -> Any:
    if hasattr(value, "model_copy"):
        return value.model_copy(update=changes)
    if is_dataclass(value):
        return replace(value, **changes)
    pytest.fail(f"proof fixture cannot create a modified copy of {type(value)!r}")


def policy(
    *,
    scope_policy_id: str = "scope-policy-001",
    scope_policy_version: int = 1,
    activation_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    deactivation_ts_utc: datetime | None = datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
    eligibility_policy_ref: str = "eligibility-policy:fixture:v1",
) -> Any:
    cls = required_symbol("CaptureScopePolicyV1")
    return cls(
        concept_id=POLICY_CONCEPT,
        contract_id=POLICY_CONTRACT,
        units="not_applicable",
        scope_policy_id=scope_policy_id,
        scope_policy_version=scope_policy_version,
        activation_ts_utc=activation_ts_utc,
        deactivation_ts_utc=deactivation_ts_utc,
        eligibility_policy_ref=eligibility_policy_ref,
    )


def observation(
    *,
    observation_occurrence_id: str = "observation-001",
    delivery_artifact_ref: str = "delivery-001",
    native_identifier: str | None = "provider-native-001",
    native_record: dict[str, Any] | None = None,
    received_ts_utc: datetime = datetime(2026, 9, 20, 12, 0, 5, 123456, tzinfo=UTC),
    received_epoch_ns: int | None = None,
    ingestion_sequence: int = 1,
    source_temporal_kind: str = "true_instant",
    source_timestamp_raw: str | None = "2026-09-20T12:00:04.900000Z",
    source_timezone_native: str | None = "UTC",
    native_units: str | None = "USD",
) -> Any:
    cls = required_symbol("RawObservationOccurrenceV1")
    return cls(
        concept_id=OBSERVATION_CONCEPT,
        contract_id=OBSERVATION_CONTRACT,
        observation_occurrence_id=observation_occurrence_id,
        delivery_artifact_ref=delivery_artifact_ref,
        source_provider="provider.fixture",
        native_record=native_record
        if native_record is not None
        else {"Bid Price": "123.45", "Provider Null": None},
        source_product_api=None,
        source_endpoint_callback=None,
        native_identifier=native_identifier,
        native_tick_series_identifier=None,
        source_variant=None,
        subject_instrument="NVDA",
        native_units=native_units,
        availability_session=None,
        source_status_native=None,
        revision_vintage_native=None,
        received_ts_utc=received_ts_utc,
        received_epoch_ns=received_epoch_ns,
        ingestion_sequence=ingestion_sequence,
        ingestion_sequence_scope="collector.fixture",
        source_temporal_kind=source_temporal_kind,
        source_timestamp_raw=source_timestamp_raw,
        source_timezone_native=source_timezone_native,
        market_timezone_iana=None,
        market_session_native=None,
    )


def register_policy(owner: Any, value: Any | None = None) -> Any:
    return owner.commands.register_capture_scope_policy(value or policy())


def realise_capture(
    owner: Any,
    *,
    scope_policy_ref: str = "scope-policy-001@1",
    slot_start_utc: datetime = datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    capture_occurrence_id: str = "capture-001",
    **unexpected: Any,
) -> Any:
    return owner.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=scope_policy_ref,
        slot_start_utc=slot_start_utc,
        capture_occurrence_id=capture_occurrence_id,
        **unexpected,
    )


def admit_observation(owner: Any, value: Any | None = None) -> Any:
    return owner.commands.admit_raw_observation_occurrence(value or observation())


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
