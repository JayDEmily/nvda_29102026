"""L03 fixed native D087 pair; prepared, NOT_RUN until independent L14."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

from nvda_desk.market_measurement_truth import api as f

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader  # noqa: E402

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
BRIEF = "0bb079166417c42d3ed2c5f8e363e771c88ba44934cda01184d43be2bc960a76"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF)
CALL = f.VersionRefV1("native-a2-call", 1)
PUT = f.VersionRefV1("native-a3-put", 1)


def _request(ref, milliseconds, cutoff_seconds=1):
    return f.NativeCalculationRequestV1(
        "D087", ref, T + timedelta(milliseconds=milliseconds),
        T + timedelta(seconds=cutoff_seconds), 0, None, None, None, (), (),
    )


def test_native_success(tmp_path):
    public = PublicDtoReader(scenarios=("A2", "A3", "A4"))
    call_path = tmp_path / "call.sqlite"
    call_owner = f.create_native_option_midpoint_owner(
        admission=ADMISSION, raw_reader=public,
        storage=f.SQLiteStorageV1(str(call_path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    call_request = _request(CALL, 300)
    call = call_owner.materialise(call_request)
    assert call is not None
    assert type(call.result) is Decimal and call.result == Decimal("1.30")
    assert call.request == call_request and call.source is not None
    assert call.source.profile.ref == CALL
    assert call.source.profile.option_right == "C"
    assert call.source.profile.request == "OPT-C100-R1"
    assert call.source.profile.generation == "OPT-L1-G1"
    assert call.source.profile.provider == "foundation-controlled-ibkr-m00-v1"
    assert call.source.profile.subject_instrument == "NVDA-OPT-C100-CONTROL-1"
    assert call.definition.raw_dependencies == ("R034", "R035")
    assert call.quote_assembly is not None
    assert call.quote_assembly.constituent_occurrence_ids == (
        "NVDA-M00-A-V1-A2-SEQ12", "NVDA-M00-A-V1-A2-SEQ11",
        "NVDA-M00-A-V1-A2-SEQ13", "NVDA-M00-A-V1-A2-SEQ14",
    )  # R033/R034/R035/R036 role order, distinct callback identities.
    assert call.quote_assembly.constituent_receipts_utc == (
        T + timedelta(milliseconds=130), T + timedelta(milliseconds=100),
        T + timedelta(milliseconds=160), T + timedelta(milliseconds=180),
    )
    assert call.quote_assembly.maximum_skew == timedelta(milliseconds=250)
    assert call.quote_assembly.maximum_latest_age == timedelta(milliseconds=1000)
    assert call.selected_event_ids == call.quote_assembly.constituent_occurrence_ids
    assert tuple(x.raw_signal_id for x in call.source.raw_input_lineage) == (
        "R033", "R034", "R035", "R036",
    )
    assert tuple(x.canonical_value for x in call.source.raw_input_lineage) == (
        Decimal(10), Decimal("1.20"), Decimal("1.40"), Decimal(8),
    )
    assert all(x.time_basis == "collector_receipt" and x.event_time_utc is None
               and x.projection.source_timestamp_raw is None
               and x.projection.source_timezone_native is None
               and x.received_ts_utc == x.projection.received_ts_utc
               for x in call.source.raw_input_lineage)
    assert all(event_filter is None for event_filter in public.event_filters)
    assert call.predecessors == () and call.owner_object_id == "M02"
    assert call.implementation_brief_sha256 == BRIEF
    assert call.units == "USD/underlying share premium" and call.result_shape == "decimal"
    call_before = call_path.read_bytes()
    call_reader = f.create_native_option_midpoint_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(call_path)))
    assert call_reader.get_derived_occurrence(call.derived_occurrence_id) == call
    assert call_reader.list_derived_history(
        derived_signal_id="D087", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=T + timedelta(milliseconds=300),
        knowledge_at_or_before_utc=T + timedelta(seconds=1), limit=1,
    ) == (call,)
    assert call_path.read_bytes() == call_before

    put_path = tmp_path / "put.sqlite"
    put_owner = f.create_native_option_midpoint_owner(
        admission=ADMISSION, raw_reader=public,
        storage=f.SQLiteStorageV1(str(put_path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    put_request = _request(PUT, 400)
    put = put_owner.materialise(put_request)
    assert put is not None
    assert type(put.result) is Decimal and put.result == Decimal("2.30")
    assert put.source is not None and put.source.profile.option_right == "P"
    assert put.source.profile.subject_instrument == "NVDA-OPT-P100-CONTROL-1"
    assert put.source.profile.generation == "OPT-P100-L1-G1"
    assert put.quote_assembly is not None
    assert put.quote_assembly.constituent_occurrence_ids == (
        "NVDA-M00-A-V1-A3-SEQ16", "NVDA-M00-A-V1-A3-SEQ15",
        "NVDA-M00-A-V1-A3-SEQ17", "NVDA-M00-A-V1-A3-SEQ18",
    )
    assert put.quote_assembly.constituent_receipts_utc == (
        T + timedelta(milliseconds=220), T + timedelta(milliseconds=200),
        T + timedelta(milliseconds=250), T + timedelta(milliseconds=270),
    )
    assert put.selected_event_ids == put.quote_assembly.constituent_occurrence_ids
    assert tuple(x.canonical_value for x in put.source.raw_input_lineage) == (
        Decimal(6), Decimal("2.20"), Decimal("2.40"), Decimal(4),
    )
    put_before = put_path.read_bytes()
    put_reader = f.create_native_option_midpoint_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(put_path)))
    assert put_reader.get_derived_occurrence(put.derived_occurrence_id) == put
    assert put_path.read_bytes() == put_before
    assert call.derived_occurrence_id != put.derived_occurrence_id


def test_native_refusal(tmp_path):
    missing = PublicDtoReader(scenarios=("A2", "A3"))
    missing.projections = [item for item in missing.projections
                           if not (item.raw_signal_catalogue_id.value == "R036"
                                   and item.observation_occurrence_id.value
                                   == "NVDA-M00-A-V1-A2-SEQ14")]
    assert {item.raw_signal_catalogue_id.value for item in missing.projections
            if item.observation_occurrence_id.value.startswith("NVDA-M00-A-V1-A2-")} == {
                "R033", "R034", "R035",
            }
    missing_owner = f.create_native_option_midpoint_owner(
        admission=ADMISSION, raw_reader=missing,
        storage=f.SQLiteStorageV1(str(tmp_path / "missing.sqlite"), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    assert missing_owner.materialise(_request(CALL, 300)) is None
    assert missing_owner.reads.list_derived_history(
        derived_signal_id="D087", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=T + timedelta(seconds=3),
        knowledge_at_or_before_utc=T + timedelta(seconds=3), limit=10,
    ) == ()

    complete = PublicDtoReader(scenarios=("A2", "A3"))
    stale_owner = f.create_native_option_midpoint_owner(
        admission=ADMISSION, raw_reader=complete,
        storage=f.SQLiteStorageV1(str(tmp_path / "stale.sqlite"), True),
        utc_now=lambda: T + timedelta(seconds=4),
    )
    assert stale_owner.materialise(_request(CALL, 2000, cutoff_seconds=3)) is None
    assert stale_owner.reads.list_derived_history(
        derived_signal_id="D087", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=T + timedelta(seconds=3),
        knowledge_at_or_before_utc=T + timedelta(seconds=3), limit=10,
    ) == ()
    # Available PUT observations cannot complete either missing or stale CALL.
    assert all(event_filter is None for event_filter in missing.event_filters + complete.event_filters)
