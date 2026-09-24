from __future__ import annotations

from array import array
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    copy_with,
    observation,
    typed_identity,
)

OPTIONAL_METADATA_CASES: tuple[tuple[str, Any], ...] = (
    ("source_product_api", "product-api::distinctive"),
    ("source_endpoint_callback", "callback::distinctive"),
    ("native_identifier", "native-id::distinctive"),
    ("native_tick_series_identifier", "tick-series::distinctive"),
    ("source_variant", "variant::distinctive"),
    ("subject_instrument", "NVDA::distinctive"),
    ("native_units", "USD::native-distinctive"),
    ("availability_session", "regular::distinctive"),
    ("source_status_native", "published::distinctive"),
    ("revision_vintage_native", "rev::distinctive"),
    ("source_timezone_native", "+00:00::native"),
    ("market_timezone_iana", "America/New_York"),
    ("market_session_native", "regular-market::distinctive"),
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
    assert first.delivery_artifact_ref == second.delivery_artifact_ref
    assert str(first.delivery_artifact_ref) == "delivery-001"
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


@pytest.mark.parametrize(("field", "value"), OPTIONAL_METADATA_CASES)
def test_each_optional_provider_metadata_field_round_trips_exactly_when_present(
    field: str, value: Any
) -> None:
    owner = build_owner()
    stored = admit_observation(owner, observation(**{field: value}))
    assert getattr(stored, field) == value
    reread = owner.reads.get_raw_observation_occurrence(stored.observation_occurrence_id)
    assert getattr(reread, field) == value


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
    kwargs = {field: None for field, _ in OPTIONAL_METADATA_CASES}
    stored = admit_observation(
        owner,
        observation(
            **kwargs,
            source_temporal_kind="receipt_only",
            source_timestamp_raw=None,
        ),
    )
    for field, _ in OPTIONAL_METADATA_CASES:
        assert getattr(stored, field) is None
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


def test_same_scope_ingestion_sequence_must_be_monotonic() -> None:
    owner = build_owner()
    scope = typed_identity("RawObservationOccurrenceV1", "ingestion_sequence_scope", "scope-A")
    admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-seq-2",
            ingestion_sequence=2,
            ingestion_sequence_scope=scope,
        ),
    )
    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(
                observation_occurrence_id="obs-seq-1-late",
                ingestion_sequence=1,
                ingestion_sequence_scope=scope,
            ),
        )


def test_ingestion_sequence_is_local_to_scope_not_global() -> None:
    owner = build_owner()
    scope_a = typed_identity("RawObservationOccurrenceV1", "ingestion_sequence_scope", "scope-A")
    scope_b = typed_identity("RawObservationOccurrenceV1", "ingestion_sequence_scope", "scope-B")
    first = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-scope-a-10",
            ingestion_sequence=10,
            ingestion_sequence_scope=scope_a,
        ),
    )
    second = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-scope-b-1",
            ingestion_sequence=1,
            ingestion_sequence_scope=scope_b,
        ),
    )
    assert first.ingestion_sequence == 10
    assert second.ingestion_sequence == 1
    assert first.ingestion_sequence_scope != second.ingestion_sequence_scope


def test_ingestion_sequence_high_water_survives_scope_interleaving() -> None:
    owner = build_owner()
    scope_a = typed_identity("RawObservationOccurrenceV1", "ingestion_sequence_scope", "scope-A")
    scope_b = typed_identity("RawObservationOccurrenceV1", "ingestion_sequence_scope", "scope-B")
    admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-a-10",
            ingestion_sequence=10,
            ingestion_sequence_scope=scope_a,
        ),
    )
    admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-b-1",
            ingestion_sequence=1,
            ingestion_sequence_scope=scope_b,
        ),
    )
    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(
                observation_occurrence_id="obs-a-9-after-b",
                ingestion_sequence=9,
                ingestion_sequence_scope=scope_a,
            ),
        )
    accepted = admit_observation(
        owner,
        observation(
            observation_occurrence_id="obs-a-11-after-b",
            ingestion_sequence=11,
            ingestion_sequence_scope=scope_a,
        ),
    )
    assert accepted.ingestion_sequence == 11
    assert accepted.ingestion_sequence_scope == scope_a


def test_same_observation_identity_is_idempotent_only_for_identical_content() -> None:
    owner = build_owner()
    value = observation()
    first = admit_observation(owner, value)
    second = admit_observation(owner, value)
    assert second == first
    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, copy_with(value, native_record={"Bid Price": "999.00"}))


@pytest.mark.parametrize(
    ("first_native", "retry_native"),
    [
        ({"Native": 1}, {"Native": 1.0}),
        ({"Native": Decimal("1.0")}, {"Native": Decimal("1.00")}),
    ],
)
def test_same_observation_identity_rejects_native_numeric_representation_change(
    first_native: dict[str, Any], retry_native: dict[str, Any]
) -> None:
    owner = build_owner()
    value = observation(native_record=first_native)
    first = admit_observation(owner, value)
    reconstructed = observation(native_record=dict(first_native))
    assert admit_observation(owner, reconstructed) is first

    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, copy_with(value, native_record=retry_native))

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    stored_value = reread.native_record["Native"]
    original_value = first_native["Native"]
    assert type(stored_value) is type(original_value)
    if isinstance(original_value, Decimal):
        assert isinstance(stored_value, Decimal)
        assert stored_value.as_tuple() == original_value.as_tuple()
    else:
        assert stored_value == original_value


@pytest.mark.parametrize("native_kind", ["float_nan", "decimal_nan"])
def test_same_observation_identity_accepts_reconstructed_identical_nan(
    native_kind: str,
) -> None:
    owner = build_owner()
    first_native: object
    retry_native: object
    if native_kind == "float_nan":
        first_native = float("nan")
        retry_native = float("nan")
    else:
        first_native = Decimal("NaN")
        retry_native = Decimal("NaN")

    first = admit_observation(owner, observation(native_record={"Native": first_native}))
    retry = observation(native_record={"Native": retry_native})

    assert admit_observation(owner, retry) is first
    assert owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id) is first


def test_same_observation_identity_rejects_complex_signed_zero_change() -> None:
    owner = build_owner()
    first = admit_observation(
        owner, observation(native_record={"Native": complex(-0.0, 0.0)})
    )

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": complex(0.0, 0.0)}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    stored_value = reread.native_record["Native"]
    assert isinstance(stored_value, complex)
    assert stored_value.real.hex() == "-0x0.0p+0"
    assert stored_value.imag.hex() == "0x0.0p+0"


def test_same_observation_identity_rejects_bytes_to_bytearray_change() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(native_record={"Native": b"abc"}))

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": bytearray(b"abc")}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    assert type(reread.native_record["Native"]) is bytes
    assert reread.native_record["Native"] == b"abc"


def test_same_observation_identity_rejects_nested_mapping_key_type_change() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(native_record={"Native": {1: "x"}}))

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": {1.0: "x"}}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    nested = reread.native_record["Native"]
    assert isinstance(nested, dict)
    key = next(iter(nested))
    assert type(key) is int
    assert key == 1


def test_same_observation_identity_rejects_array_typecode_change() -> None:
    owner = build_owner()
    first = admit_observation(
        owner, observation(native_record={"Native": array("b", [1])})
    )

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": array("B", [1])}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    stored_value = reread.native_record["Native"]
    assert isinstance(stored_value, array)
    assert stored_value.typecode == "b"
    assert stored_value.tolist() == [1]


def test_same_observation_identity_rejects_range_bound_change() -> None:
    owner = build_owner()
    first = admit_observation(
        owner, observation(native_record={"Native": range(0, 3, 2)})
    )

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": range(0, 4, 2)}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    stored_value = reread.native_record["Native"]
    assert isinstance(stored_value, range)
    assert (stored_value.start, stored_value.stop, stored_value.step) == (0, 3, 2)


def test_newly_received_retransmission_keeps_new_observation_identity() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(observation_occurrence_id="obs-1"))
    second = admit_observation(
        owner,
        observation(observation_occurrence_id="obs-2", ingestion_sequence=2),
    )
    assert first.native_identifier == second.native_identifier
    assert first.native_record == second.native_record
    assert first.observation_occurrence_id != second.observation_occurrence_id


def test_no_scope_observation_remains_valid_without_capture_relation() -> None:
    owner = build_owner()
    stored = admit_observation(owner)
    assert owner.reads.get_raw_observation_occurrence(stored.observation_occurrence_id) == stored
    assert getattr(stored, "capture_occurrence_ref", None) is None


def test_observation_command_rejects_typed_cross_layer_identity_substitution() -> None:
    owner = build_owner()
    observation_id = typed_identity(
        "RawObservationOccurrenceV1", "observation_occurrence_id", "same-opaque-payload"
    )
    delivery_id = typed_identity(
        "RawObservationOccurrenceV1", "delivery_artifact_ref", "same-opaque-payload"
    )
    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, observation(observation_occurrence_id=delivery_id))
    with pytest.raises((TypeError, ValueError)):
        admit_observation(owner, observation(delivery_artifact_ref=observation_id))


@pytest.mark.parametrize(
    ("catalogue_id", "field", "value", "units"),
    [
        ("R033", "Bid Size", 0, "contracts/shares"),
        ("R034", "Bid Price", 123.45678901234567, "price"),
        ("R038", "Last Size", Decimal("0.00100"), "contracts/shares"),
        (
            "R084",
            "Bid Option Computation.impliedVolatility",
            -0.000000000123456789,
            "volatility",
        ),
        ("R246", "DGS3MO", -0.375, "Percent"),
    ],
)
def test_catalogue_backed_native_numeric_values_preserve_exact_value_and_runtime_type(
    catalogue_id: str, field: str, value: int | float | Decimal, units: str
) -> None:
    """Numeric specimens are fidelity canaries, not admitted range/bounds validation."""

    owner = build_owner()
    stored = admit_observation(
        owner,
        observation(
            raw_signal_catalogue_ids=(catalogue_id,),
            native_record={field: value, "Provider Null": None},
            native_units=units,
        ),
    )
    reread = owner.reads.get_raw_observation_occurrence(stored.observation_occurrence_id)
    assert tuple(str(item) for item in stored.raw_signal_catalogue_ids) == (catalogue_id,)
    assert stored.native_record[field] == value
    assert type(stored.native_record[field]) is type(value)
    assert stored.native_record["Provider Null"] is None
    assert reread.native_record[field] == value
    assert type(reread.native_record[field]) is type(value)
    if isinstance(value, Decimal):
        assert reread.native_record[field].as_tuple() == value.as_tuple()
    assert reread.native_units == units
