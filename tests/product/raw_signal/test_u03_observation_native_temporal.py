from __future__ import annotations

import os
import subprocess
import sys
from array import array
from collections import UserDict
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, get_args, get_type_hints

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    copy_with,
    observation,
    typed_identity,
)

from nvda_desk.raw_signal_occurrence_truth import api

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
        ({"Native": -0.0}, {"Native": 0.0}),
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


class _ExplosiveEquality:
    equality_called = False

    def __eq__(self, other: object) -> bool:
        type(self).equality_called = True
        raise AssertionError("unsupported native value equality must never be invoked")


def test_public_native_record_annotation_exposes_finite_native_value_v1() -> None:
    hints = get_type_hints(api.RawObservationOccurrenceV1)
    native_record_annotation = hints["native_record"]
    key_type, value_type = get_args(native_record_annotation)
    assert key_type is str
    assert value_type is api.NativeValueV1
    assert "NativeValueV1" in api.__all__


def test_public_static_native_value_v1_rejects_outside_carrier_specimens() -> None:
    specimen = Path(__file__).resolve().parent / "typecheck" / "native_value_negative.py"
    source_lines = specimen.read_text(encoding="utf-8").splitlines()
    expected_lines = {
        number for number, line in enumerate(source_lines, start=1) if "NATIVE_NEGATIVE" in line
    }
    assert len(expected_lines) == 4
    root = Path(__file__).resolve().parents[3]
    env = os.environ.copy()
    env["MYPYPATH"] = str(root / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--strict",
            "--disallow-any-expr",
            "--show-error-codes",
            "--no-error-summary",
            str(specimen),
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0, "outside-carrier static specimen unexpectedly type-checked"
    reported_lines: set[int] = set()
    for line in (result.stdout + result.stderr).splitlines():
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        try:
            reported_lines.add(int(parts[1]))
        except ValueError:
            continue
    assert not expected_lines - reported_lines, result.stdout + result.stderr


def test_allowed_recursive_native_values_are_canonicalised_alias_safe_and_idempotent() -> None:
    owner = build_owner()
    mutable_list: list[Any] = [None, True, 1, -0.0, Decimal("1.00"), "x", b"bytes"]
    first_native = UserDict(
        {
            "Outer": UserDict({"Tuple": ("a", 2), "List": mutable_list}),
            "Other": "value",
        }
    )
    first = admit_observation(owner, observation(native_record=first_native))

    mutable_list[2] = 999
    first_native["Other"] = "mutated"
    stored_outer = first.native_record["Outer"]
    assert isinstance(stored_outer, dict)
    stored_list = stored_outer["List"]
    assert isinstance(stored_list, list)
    assert stored_list[2] == 1
    assert first.native_record["Other"] == "value"

    stored_list[2] = 777
    reread_outer = first.native_record["Outer"]
    assert isinstance(reread_outer, dict)
    reread_list = reread_outer["List"]
    assert isinstance(reread_list, list)
    assert reread_list[2] == 1

    reconstructed = observation(
        native_record={
            "Other": "value",
            "Outer": {
                "List": [None, True, 1, -0.0, Decimal("1.00"), "x", b"bytes"],
                "Tuple": ("a", 2),
            },
        }
    )
    assert admit_observation(owner, reconstructed) is first


@pytest.mark.parametrize(
    ("label", "unsupported"),
    [
        ("reviewer026-complex", complex(-0.0, 0.0)),
        ("reviewer027-bytearray", bytearray(b"abc")),
        ("reviewer027-non-string-key", {1: "x"}),
        ("reviewer028-array", array("b", [1])),
        ("reviewer028-range", range(0, 3, 2)),
        ("reviewer029-datetime", datetime(2026, 9, 20, 12, 0, tzinfo=UTC)),
        ("set", {"x"}),
        ("frozenset", frozenset({"x"})),
    ],
    ids=lambda item: item if isinstance(item, str) else None,
)
def test_superseded_witnesses_are_unsupported_and_do_not_replace_first_occurrence(
    label: str, unsupported: object
) -> None:
    del label
    owner = build_owner()
    first = admit_observation(owner, observation(native_record={"Native": b"first"}))

    with pytest.raises(TypeError, match=r"NativeValueV1|exact built-in strings"):
        retry = observation(native_record={"Native": unsupported})
        admit_observation(owner, retry)

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    assert reread.native_record["Native"] == b"first"


def test_arbitrary_custom_equality_object_fails_closed_without_invoking_equality() -> None:
    owner = build_owner()
    first = admit_observation(owner, observation(native_record={"Native": "first"}))
    unsupported = _ExplosiveEquality()
    _ExplosiveEquality.equality_called = False

    with pytest.raises(TypeError, match="NativeValueV1"):
        retry = observation(native_record={"Native": unsupported})
        admit_observation(owner, retry)

    assert not _ExplosiveEquality.equality_called
    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first
    assert reread.native_record["Native"] == "first"


def test_same_observation_identity_rejects_recursive_container_kind_change() -> None:
    owner = build_owner()
    first = admit_observation(
        owner, observation(native_record={"Native": {"Nested": [Decimal("1.00"), -0.0]}})
    )

    with pytest.raises((TypeError, ValueError)):
        admit_observation(
            owner,
            observation(native_record={"Native": {"Nested": (Decimal("1.00"), -0.0)}}),
        )

    reread = owner.reads.get_raw_observation_occurrence(first.observation_occurrence_id)
    assert reread is first


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
