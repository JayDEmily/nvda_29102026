"""L12 fixed native D137 pair; prepared, NOT_RUN until independent L14."""

import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
BRIEF = "e245fb52e9cdb2d09e88a5d4ad4b298049840e07a1a70288311ff6c651ff82a5"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF)
CALL = f.VersionRefV1("native-a2-call", 1)
PUT = f.VersionRefV1("native-a3-put", 1)


def _request(ref, milliseconds, cutoff_seconds=1):
    return f.NativeCalculationRequestV1(
        "D137",
        ref,
        T + timedelta(milliseconds=milliseconds),
        T + timedelta(seconds=cutoff_seconds),
        0,
        None,
        None,
        None,
        (),
        (),
    )


def test_native_success(tmp_path):
    public = PublicDtoReader(scenarios=("A2", "A3", "A4"))
    call_path = tmp_path / "call.sqlite"
    call_owner = f.create_native_microprice_owner(
        admission=ADMISSION,
        raw_reader=public,
        storage=f.SQLiteStorageV1(str(call_path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    call_request = _request(CALL, 300)
    call = call_owner.materialise(call_request)
    assert call is not None
    assert type(call.result) is f.ExactRatioV1 and call.result == f.ExactRatioV1(59, 45)
    assert call.request == call_request and call.source is not None
    assert call.source.profile.ref == CALL
    assert call.source.profile.option_right == "C"
    assert call.source.profile.request == "OPT-C100-R1"
    assert call.source.profile.generation == "OPT-L1-G1"
    assert call.source.profile.provider == "foundation-controlled-ibkr-m00-v1"
    assert call.source.profile.subject_instrument == "NVDA-OPT-C100-CONTROL-1"
    assert call.definition.raw_dependencies == ("R033", "R034", "R035", "R036")
    assert call.quote_assembly is not None
    assert call.quote_assembly.constituent_occurrence_ids == (
        "NVDA-M00-A-V1-A2-SEQ12",
        "NVDA-M00-A-V1-A2-SEQ11",
        "NVDA-M00-A-V1-A2-SEQ13",
        "NVDA-M00-A-V1-A2-SEQ14",
    )  # R033/R034/R035/R036 role order, distinct callback identities.
    assert call.quote_assembly.constituent_receipts_utc == (
        T + timedelta(milliseconds=130),
        T + timedelta(milliseconds=100),
        T + timedelta(milliseconds=160),
        T + timedelta(milliseconds=180),
    )
    assert call.quote_assembly.maximum_skew == timedelta(milliseconds=250)
    assert call.quote_assembly.maximum_latest_age == timedelta(milliseconds=1000)
    assert call.selected_event_ids == call.quote_assembly.constituent_occurrence_ids
    assert tuple(x.raw_signal_id for x in call.source.raw_input_lineage) == (
        "R033",
        "R034",
        "R035",
        "R036",
    )
    assert tuple(x.canonical_value for x in call.source.raw_input_lineage) == (
        Decimal(10),
        Decimal("1.20"),
        Decimal("1.40"),
        Decimal(8),
    )
    assert all(
        x.time_basis == "collector_receipt"
        and x.event_time_utc is None
        and x.projection.source_timestamp_raw is None
        and x.projection.source_timezone_native is None
        and x.received_ts_utc == x.projection.received_ts_utc
        for x in call.source.raw_input_lineage
    )
    assert all(event_filter is None for event_filter in public.event_filters)
    assert call.predecessors == () and call.owner_object_id == "M02"
    assert call.implementation_brief_sha256 == BRIEF
    assert call.units == "USD/underlying share premium" and call.result_shape == "exact_ratio"
    call_before = call_path.read_bytes()
    call_reader = f.create_native_microprice_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(call_path))
    )
    reopened_call = call_reader.get_derived_occurrence(call.derived_occurrence_id)
    assert type(reopened_call) is f.NativeMeasurementOccurrenceV1
    assert typed_tree(reopened_call) == typed_tree(call)
    call_history = call_reader.list_derived_history(
        derived_signal_id="D137",
        subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=T + timedelta(milliseconds=300),
        knowledge_at_or_before_utc=T + timedelta(seconds=1),
        limit=1,
    )
    assert len(call_history) == 1 and typed_tree(call_history[0]) == typed_tree(call)
    assert call_path.read_bytes() == call_before

    put_path = tmp_path / "put.sqlite"
    put_owner = f.create_native_microprice_owner(
        admission=ADMISSION,
        raw_reader=public,
        storage=f.SQLiteStorageV1(str(put_path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    put_request = _request(PUT, 400)
    put = put_owner.materialise(put_request)
    assert put is not None
    assert type(put.result) is f.ExactRatioV1 and put.result == f.ExactRatioV1(58, 25)
    assert put.source is not None and put.source.profile.option_right == "P"
    assert put.source.profile.subject_instrument == "NVDA-OPT-P100-CONTROL-1"
    assert put.source.profile.generation == "OPT-P100-L1-G1"
    assert put.quote_assembly is not None
    assert put.quote_assembly.constituent_occurrence_ids == (
        "NVDA-M00-A-V1-A3-SEQ16",
        "NVDA-M00-A-V1-A3-SEQ15",
        "NVDA-M00-A-V1-A3-SEQ17",
        "NVDA-M00-A-V1-A3-SEQ18",
    )
    assert put.quote_assembly.constituent_receipts_utc == (
        T + timedelta(milliseconds=220),
        T + timedelta(milliseconds=200),
        T + timedelta(milliseconds=250),
        T + timedelta(milliseconds=270),
    )
    assert put.selected_event_ids == put.quote_assembly.constituent_occurrence_ids
    assert tuple(x.canonical_value for x in put.source.raw_input_lineage) == (
        Decimal(6),
        Decimal("2.20"),
        Decimal("2.40"),
        Decimal(4),
    )
    put_before = put_path.read_bytes()
    put_reader = f.create_native_microprice_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(put_path))
    )
    reopened_put = put_reader.get_derived_occurrence(put.derived_occurrence_id)
    assert type(reopened_put) is f.NativeMeasurementOccurrenceV1
    assert typed_tree(reopened_put) == typed_tree(put)
    assert put_path.read_bytes() == put_before
    assert call.derived_occurrence_id != put.derived_occurrence_id


def test_native_refusal(tmp_path):
    missing = PublicDtoReader(scenarios=("A2", "A3"))
    missing.projections = [
        item
        for item in missing.projections
        if not (
            item.raw_signal_catalogue_id.value == "R036"
            and item.observation_occurrence_id.value == "NVDA-M00-A-V1-A2-SEQ14"
        )
    ]
    assert {
        item.raw_signal_catalogue_id.value
        for item in missing.projections
        if item.observation_occurrence_id.value.startswith("NVDA-M00-A-V1-A2-")
    } == {
        "R033",
        "R034",
        "R035",
    }
    missing_owner = f.create_native_microprice_owner(
        admission=ADMISSION,
        raw_reader=missing,
        storage=f.SQLiteStorageV1(str(tmp_path / "missing.sqlite"), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    assert missing_owner.materialise(_request(CALL, 300)) is None
    assert (
        missing_owner.reads.list_derived_history(
            derived_signal_id="D137",
            subject_instrument="NVDA-OPT-C100-CONTROL-1",
            effective_at_or_before_utc=T + timedelta(seconds=3),
            knowledge_at_or_before_utc=T + timedelta(seconds=3),
            limit=10,
        )
        == ()
    )

    missing_before = (tmp_path / "missing.sqlite").read_bytes()
    reader = f.create_native_microprice_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(tmp_path / "missing.sqlite"))
    )
    assert (
        reader.list_derived_history(
            derived_signal_id="D137",
            subject_instrument="NVDA-OPT-C100-CONTROL-1",
            effective_at_or_before_utc=T + timedelta(seconds=3),
            knowledge_at_or_before_utc=T + timedelta(seconds=3),
            limit=10,
        )
        == ()
    )
    assert (tmp_path / "missing.sqlite").read_bytes() == missing_before
    assert all(event_filter is None for event_filter in missing.event_filters)
