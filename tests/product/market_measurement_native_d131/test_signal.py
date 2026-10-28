"""L04 native D131 pair, prepared for independent L14 execution only."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree  # noqa: E402

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
OPTION_BRIEF = "0bb079166417c42d3ed2c5f8e363e771c88ba44934cda01184d43be2bc960a76"
BOOK_BRIEF = "0ac16b9eb4859665807a86739293a196e63916062c3db7c522ab6303eabcfbe8"
CALL = f.VersionRefV1("native-a2-call", 1)
BOOK = f.VersionRefV1("native-c1-call", 1)


def _option_request(as_of):
    return f.NativeCalculationRequestV1(
        "D087", CALL, as_of, CUTOFF, 0, None, None, None, (), ())


def _book_request(as_of, predecessor_id):
    return f.NativeCalculationRequestV1(
        "D131", BOOK, as_of, CUTOFF, 0, Decimal("0.50"), None, None, (),
        (predecessor_id,))


def _actual_predecessor(source, tmp_path, as_of, label):
    path = tmp_path / ("option-" + label + ".sqlite")
    owner = f.create_native_option_midpoint_owner(
        admission=f.OwnerAdmissionV1("M02", OPTION_BRIEF), raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2))
    predecessor = owner.materialise(_option_request(as_of))
    assert type(predecessor) is f.NativeMeasurementOccurrenceV1
    assert predecessor.result == Decimal("1.30")
    assert predecessor.source is not None
    assert predecessor.source.profile.ref == CALL
    assert predecessor.quote_assembly is not None
    assert len(set(predecessor.quote_assembly.constituent_occurrence_ids)) == 4
    assert predecessor.request.as_of_utc == as_of
    reader = f.create_native_option_midpoint_reader(
        admission=f.OwnerAdmissionV1("M02", OPTION_BRIEF),
        storage=f.SQLiteReadStorageV1(str(path)))
    reopened = reader.get_derived_occurrence(predecessor.derived_occurrence_id)
    assert type(reopened) is f.NativeMeasurementOccurrenceV1
    assert typed_tree(reopened) == typed_tree(predecessor)
    return predecessor, reader


def _reset(source):
    template = next(x for x in source.observations
                    if x.observation_occurrence_id.value == "COH-SMART-C03")
    collector = dict(template.native_record["_collector"])
    collector["control"] = {
        "schema_version": "m00-control-envelope/1", "kind": "error317",
        "origin": "provider_callback", "request": "COH-CALL-R1",
        "generation_before": "OPT-C100-SMART-COHERENT-V2",
        "generation_after": "OPT-C100-SMART-COHERENT-V2",
        "invalidates": True,
    }
    reset = replace(
        template,
        observation_occurrence_id=raw.observation_occurrence_id("C1-ERROR317-AFTER-WARMUP"),
        native_record={"_collector": collector, "errorCode": 317},
        received_ts_utc=T + timedelta(milliseconds=350),
        ingestion_sequence=304, raw_signal_catalogue_ids=None,
        source_endpoint_callback="error",
    )
    source.observations.append(reset)
    return reset


def test_native_success(tmp_path):
    source = PublicDtoReader(scenarios=("A2", "C1", "A3"))
    as_of = T + timedelta(milliseconds=300)
    predecessor, predecessor_reader = _actual_predecessor(source, tmp_path, as_of, "success")
    path = tmp_path / "native-d131.sqlite"
    owner = f.create_native_book_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BOOK_BRIEF), raw_reader=source,
        predecessor_reader=predecessor_reader,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2))
    request = _book_request(as_of, predecessor.derived_occurrence_id)
    result = owner.materialise(request)
    assert type(result) is f.NativeMeasurementOccurrenceV1
    assert type(result.result) is Decimal and result.result == Decimal("8")
    assert result.request == request and len(result.predecessors) == 1
    assert typed_tree(result.predecessors[0]) == typed_tree(predecessor)
    assert result.source is not None
    assert result.source.profile.ref == BOOK
    assert result.source.profile.provider == "foundation-controlled-ibkr-m00-coherent-v2"
    assert result.source.profile.request == "COH-CALL-R1"
    assert result.source.profile.generation == "OPT-C100-SMART-COHERENT-V2"
    assert result.source.profile.contract_identity == predecessor.source.profile.contract_identity
    assert result.source.profile.source_context_ref == predecessor.source.profile.source_context_ref
    assert result.source.profile.source_context_ref == f.VersionRefV1(
        "native-coherent-call-reference", 1)
    assert result.source.controls == ()
    assert tuple((row.side, row.position, row.price, row.size,
                  row.observation_occurrence_id) for row in result.source.standing_rows) == (
        (1, 0, Decimal("1.20"), Decimal("5"), "COH-SMART-C01"),
        (1, 1, Decimal("0.70"), Decimal("7"), "COH-SMART-C02"),
        (0, 0, Decimal("1.40"), Decimal("3"), "COH-SMART-C03"),
    )
    assert result.selected_event_ids == ("COH-SMART-C01", "COH-SMART-C03")
    assert len(result.source.raw_input_lineage) == 15
    assert {x.observation_occurrence_id for x in result.source.raw_input_lineage} == {
        "COH-SMART-C01", "COH-SMART-C02", "COH-SMART-C03"}
    assert {x.raw_signal_id for x in result.source.raw_input_lineage} == {
        "R185", "R187", "R188", "R189", "R190"}
    assert all(x.time_basis == "collector_receipt" and x.event_time_utc is None
               and x.projection.source_timestamp_raw is None
               and x.projection.source_timezone_native is None
               and x.received_ts_utc == x.projection.received_ts_utc
               for x in result.source.raw_input_lineage)
    assert result.quote_assembly is None
    assert result.definition.calculation_definition_version == "D131-NATIVE-CALL-BAND-1"
    assert result.definition.derived_dependencies == ("D087",)
    assert result.units == "contracts" and result.result_shape == "decimal"
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BOOK_BRIEF
    assert all(event_filter is None for event_filter in source.event_filters)
    before = path.read_bytes()
    reader = f.create_native_book_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BOOK_BRIEF),
        storage=f.SQLiteReadStorageV1(str(path)))
    reopened = reader.get_derived_occurrence(result.derived_occurrence_id)
    assert type(reopened) is f.NativeMeasurementOccurrenceV1
    assert typed_tree(reopened) == typed_tree(result)
    history = reader.list_derived_history(
        derived_signal_id="D131", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=as_of,
        knowledge_at_or_before_utc=CUTOFF, limit=1)
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(result)
    assert path.read_bytes() == before


def test_native_refusal(tmp_path):
    source = PublicDtoReader(scenarios=("A2", "C1"))
    reset = _reset(source)
    as_of = T + timedelta(milliseconds=400)
    predecessor, predecessor_reader = _actual_predecessor(source, tmp_path, as_of, "reset")
    assert predecessor.request.as_of_utc == as_of
    assert reset.received_ts_utc < as_of
    assert tuple(x.observation_occurrence_id.value for x in source.observations
                 if x.source_provider.value == "foundation-controlled-ibkr-m00-coherent-v2"
                 and x.received_ts_utc > reset.received_ts_utc) == ()
    path = tmp_path / "refused-d131.sqlite"
    owner = f.create_native_book_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BOOK_BRIEF), raw_reader=source,
        predecessor_reader=predecessor_reader,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2))
    assert owner.materialise(_book_request(as_of, predecessor.derived_occurrence_id)) is None
    assert owner.reads.list_derived_history(
        derived_signal_id="D131", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=as_of, knowledge_at_or_before_utc=CUTOFF,
        limit=10) == ()
    reader = f.create_native_book_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BOOK_BRIEF),
        storage=f.SQLiteReadStorageV1(str(path)))
    assert reader.list_derived_history(
        derived_signal_id="D131", subject_instrument="NVDA-OPT-C100-CONTROL-1",
        effective_at_or_before_utc=as_of, knowledge_at_or_before_utc=CUTOFF,
        limit=10) == ()
    assert all(event_filter is None for event_filter in source.event_filters)
