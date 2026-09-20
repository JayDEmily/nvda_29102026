from __future__ import annotations

from datetime import UTC, datetime

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    copy_with,
    observation,
)


def test_two_separable_records_share_delivery_but_remain_two_observations() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(observation_occurrence_id="obs-1"))
    second = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-2",
            native_record={"Bid Price": "123.46"},
            ingestion_sequence=2,
        ),
    )
    assert first.delivery_artifact_ref == second.delivery_artifact_ref == "delivery-001"
    assert first.observation_occurrence_id != second.observation_occurrence_id


def test_one_provider_record_with_multiple_fields_remains_one_observation() -> None:
    owner = build_owner()
    native = {"Bid Price": "123.4500", "Ask Price": "123.4600", "Provider Null": None}
    stored = admit_observation(owner, observation(native_record=native))
    assert stored.native_record == native
    assert not hasattr(stored, "field_occurrences")


def test_native_record_names_values_and_provider_null_round_trip_unchanged() -> None:
    owner = build_owner()
    native = {"Bid Price": "123.4500", "Provider Null": None, "Calc Value": "7.5"}
    stored = admit_observation(owner, observation(native_record=native))
    assert stored.native_record == native
    assert stored.native_units == "USD"


@pytest.mark.parametrize(
    ("kind", "raw", "timezone"),
    [
        ("true_instant", "2026-09-20T12:00:04.900000Z", "UTC"),
        ("date_only", "2026-09-20", None),
        ("receipt_only", None, None),
    ],
)
def test_temporal_kind_preserves_only_authorised_source_time(
    kind: str, raw: str | None, timezone: str | None
) -> None:
    owner = build_owner()
    stored = admit_observation(
        owner,
        observation(
            source_temporal_kind=kind,
            source_timestamp_raw=raw,
            source_timezone_native=timezone,
        ),
    )
    assert stored.source_temporal_kind == kind
    assert stored.source_timestamp_raw == raw
    assert stored.source_timezone_native == timezone
    assert not hasattr(stored, "event_ts_utc")


@pytest.mark.parametrize(
    ("kind", "raw"),
    [
        ("true_instant", None),
        ("date_only", None),
        ("receipt_only", "2026-09-20T12:00:04Z"),
    ],
)
def test_impossible_temporal_discriminant_fails_closed(kind: str, raw: str | None) -> None:
    owner = build_owner()
    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(
                source_temporal_kind=kind,
                source_timestamp_raw=raw,
                source_timezone_native=None,
            ),
        )


def test_receipt_time_does_not_fill_missing_provider_time_or_timezone() -> None:
    owner = build_owner()
    stored = admit_observation(
        owner,
        observation(
            source_temporal_kind="receipt_only",
            source_timestamp_raw=None,
            source_timezone_native=None,
        ),
    )
    assert stored.source_timestamp_raw is None
    assert stored.source_timezone_native is None
    assert stored.received_ts_utc == datetime(2026, 9, 20, 12, 0, 5, 123456, tzinfo=UTC)


def test_optional_provider_metadata_remains_absent_when_not_applicable() -> None:
    owner = build_owner()
    stored = admit_observation(owner, observation(native_identifier=None, native_units=None))
    assert stored.native_identifier is None
    assert stored.native_units is None
    assert getattr(stored, "revision_vintage_native", None) is None
    assert not hasattr(stored, "is_original_revision")


def test_genuine_nanosecond_evidence_is_not_synthesised_from_microseconds() -> None:
    owner = build_owner()
    no_ns = admit_observation(owner, observation(observation_occurrence_id="obs-no-ns"))
    with_ns = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-ns",
            ingestion_sequence=2,
            received_epoch_ns=1_758_369_605_123_456_789,
        ),
    )
    assert no_ns.received_epoch_ns is None
    assert with_ns.received_epoch_ns == 1_758_369_605_123_456_789


def test_missing_required_receipt_order_or_provenance_fails_closed() -> None:
    owner = build_owner()
    base = observation()
    for field in ("received_ts_utc", "ingestion_sequence", "ingestion_sequence_scope"):
        with pytest.raises((TypeError, ValueError)):
            admit_observation(owner, copy_with(base, **{field: None}))


def test_same_observation_identity_is_idempotent_only_for_identical_content() -> None:
    owner = build_owner()
    value = observation()
    first = admit_observation(owner, value)
    second = admit_observation(owner, value)
    assert second == first
    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, copy_with(value, native_record={"Bid Price": "999.00"}))


def test_newly_received_retransmission_keeps_new_observation_identity() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(observation_occurrence_id="obs-1"))
    second = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-2",
            ingestion_sequence=2,
        ),
    )
    assert first.native_identifier == second.native_identifier
    assert first.native_record == second.native_record
    assert first.observation_occurrence_id != second.observation_occurrence_id


def test_no_scope_observation_remains_valid_without_capture_relation() -> None:
    owner = build_owner()
    stored = admit_observation(owner)
    assert owner.reads.get_raw_observation_occurrence(stored.observation_occurrence_id) == stored
    assert getattr(stored, "capture_occurrence_ref", None) is None


@pytest.mark.parametrize(
    ("field", "substitute"),
    [
        ("observation_occurrence_id", "delivery-001"),
        ("delivery_artifact_ref", "observation-001"),
        ("source_provider", "observation-001"),
        ("native_identifier", "provider.fixture"),
        ("ingestion_sequence_scope", "delivery-001"),
    ],
)
def test_observation_command_boundary_rejects_cross_layer_identity_substitution(
    field: str, substitute: str
) -> None:
    owner = build_owner()
    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, copy_with(observation(), **{field: substitute}))
