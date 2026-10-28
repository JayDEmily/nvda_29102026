"""L07 actual public native bid/ask predecessor pair; NOT_RUN until L14."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

from nvda_desk.market_measurement_truth import api as f

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree  # noqa: E402

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
NOW = T + timedelta(seconds=3)
PROFILE = f.VersionRefV1("native-a4-stock", 1)
BID_BRIEF = "73e03e0700902098ecc8a0c9c6e3ffffd94bbc74ab8f27576368ccc0dd19cce0"
ASK_BRIEF = "419afb2f5b0d27d72159587c9b9ad323afcb4dc49242257f9a83fa4317aa5653"
BRIEF = "8510a6e722300d06993ed8a66a8b1b808488913a48625f31183fd2ef9442c7ec"
IDS = tuple("NVDA-M00-A-V1-A4-SEQ" + str(i) for i in (21, 22, 23, 24))


def _parent_request(signal, side, levels):
    return f.NativeCalculationRequestV1(
        signal, PROFILE, T, CUTOFF, levels, None, None, side, (), ())


def _request(bid, ask):
    return f.NativeCalculationRequestV1(
        "D136", PROFILE, T, CUTOFF, 2, None, None, None, (),
        (bid.derived_occurrence_id, ask.derived_occurrence_id))


def _actual_predecessors(tmp_path, ask_levels):
    source = PublicDtoReader(scenarios=("A4", "C2"))
    bid_path, ask_path = tmp_path / "actual-bid.sqlite", tmp_path / "actual-ask.sqlite"
    bid_owner = f.create_native_smart_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BID_BRIEF), raw_reader=source,
        storage=f.SQLiteStorageV1(str(bid_path), True),
        utc_now=lambda: T + timedelta(seconds=2))
    ask_owner = f.create_native_smart_ask_owner(
        admission=f.OwnerAdmissionV1("M02", ASK_BRIEF), raw_reader=source,
        storage=f.SQLiteStorageV1(str(ask_path), True),
        utc_now=lambda: T + timedelta(seconds=2))
    bid = bid_owner.materialise(_parent_request("D134", 1, 2))
    ask = ask_owner.materialise(_parent_request("D135", 0, ask_levels))
    assert type(bid) is f.NativeMeasurementOccurrenceV1
    assert type(ask) is f.NativeMeasurementOccurrenceV1
    assert type(bid.result) is Decimal and bid.result == Decimal("8")
    assert bid.definition.calculation_definition_version == "D134-NATIVE-BID-TOP2-1"
    assert bid.request.depth_levels == 2 and bid.request.side == 1
    assert ask.request.depth_levels == ask_levels and ask.request.side == 0
    assert bid.source is not None and ask.source is not None
    assert typed_tree(bid.source) == typed_tree(ask.source)
    snapshot = bid.source
    assert snapshot.profile.ref == PROFILE
    assert snapshot.profile.provider == "foundation-controlled-ibkr-m00-v1"
    assert snapshot.profile.variant == "ibkr-smart-depth/native-v1"
    assert snapshot.profile.subject_instrument == "NVDA-STK-CONTROL-1"
    assert snapshot.profile.generation == "STK-SMART-G1"
    assert snapshot.profile.request == "STK-SMART-R1"
    assert snapshot.profile.requested_exchange == "SMART"
    assert snapshot.profile.contract_identity == "NVDA-STK-CONTROL-1|STK|None|USD|None|None|1"
    assert snapshot.profile.option_right is None and snapshot.controls == ()
    assert snapshot.profile.warmup_observation_ids == IDS
    assert tuple((x.side, x.position, x.price, x.size, x.observation_occurrence_id)
                 for x in snapshot.standing_rows) == (
        (1, 0, Decimal("99.00"), Decimal("5"), IDS[0]),
        (1, 1, Decimal("98.00"), Decimal("3"), IDS[1]),
        (0, 0, Decimal("101.00"), Decimal("2"), IDS[2]),
        (0, 1, Decimal("102.00"), Decimal("4"), IDS[3]),
    )
    assert len(snapshot.raw_input_lineage) == 20
    assert {x.raw_signal_id for x in snapshot.raw_input_lineage} == {
        "R185", "R187", "R188", "R189", "R190"}
    assert all(x.time_basis == "collector_receipt" and x.event_time_utc is None
               and x.projection.source_timestamp_raw is None
               and x.projection.source_timezone_native is None
               and type(x.canonical_value) is type(x.projection.native_value)
               and x.received_ts_utc == x.projection.received_ts_utc
               for x in snapshot.raw_input_lineage)
    assert all(x is None for x in source.event_filters) and source.control_queries > 0
    bid_reader = f.create_native_smart_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BID_BRIEF),
        storage=f.SQLiteReadStorageV1(str(bid_path)))
    ask_reader = f.create_native_smart_ask_reader(
        admission=f.OwnerAdmissionV1("M02", ASK_BRIEF),
        storage=f.SQLiteReadStorageV1(str(ask_path)))
    assert typed_tree(bid_reader.get_derived_occurrence(bid.derived_occurrence_id)) == typed_tree(bid)
    assert typed_tree(ask_reader.get_derived_occurrence(ask.derived_occurrence_id)) == typed_tree(ask)
    return bid, ask, bid_reader, ask_reader, bid_path, ask_path


def test_native_success(tmp_path):
    bid, ask, bid_reader, ask_reader, bid_path, ask_path = _actual_predecessors(tmp_path, 2)
    assert type(ask.result) is Decimal and ask.result == Decimal("6")
    assert ask.definition.calculation_definition_version == "D135-NATIVE-ASK-TOP2-1"
    assert bid.selected_event_ids == IDS[:2] and ask.selected_event_ids == IDS[2:]
    parent_bytes = bid_path.read_bytes(), ask_path.read_bytes()
    path = tmp_path / "native-d136.sqlite"
    owner = f.create_native_smart_imbalance_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        bid_reader=bid_reader, ask_reader=ask_reader,
        storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: NOW)
    request = _request(bid, ask)
    result = owner.materialise(request)
    assert type(result) is f.NativeMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(1, 7)
    assert result.request == request and result.request.depth_levels == 2
    assert typed_tree(result.predecessors) == typed_tree((bid, ask))
    assert result.source is None and result.quote_assembly is None
    assert result.selected_event_ids == ()
    assert result.definition.calculation_definition_version == "D136-NATIVE-COMMON-TOP2-IMBALANCE-1"
    assert result.definition.raw_dependencies == ()
    assert result.definition.derived_dependencies == ("D134", "D135")
    assert result.units == "-1_to_1" and result.result_shape == "exact_ratio"
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    before = path.read_bytes()
    reader = f.create_native_smart_imbalance_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        storage=f.SQLiteReadStorageV1(str(path)))
    assert typed_tree(reader.get_derived_occurrence(result.derived_occurrence_id)) == typed_tree(result)
    history = reader.list_derived_history(
        derived_signal_id="D136", subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=1)
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(result)
    assert path.read_bytes() == before
    assert (bid_path.read_bytes(), ask_path.read_bytes()) == parent_bytes


def test_native_refusal(tmp_path):
    bid, ask, bid_reader, ask_reader, bid_path, ask_path = _actual_predecessors(tmp_path, 1)
    assert type(ask.result) is Decimal and ask.result == Decimal("2")
    assert ask.definition.calculation_definition_version == "D135-NATIVE-ASK-TOP1-1"
    assert bid.request.depth_levels == 2 and ask.request.depth_levels == 1
    assert ask.selected_event_ids == (IDS[2],)
    request = _request(bid, ask)
    # Only the actual ask predecessor is top-one: the imbalance request remains
    # the unchanged common-top-two contract and cannot accept its numeric depth.
    assert request.depth_levels == 2 and request.side is None
    assert request.predecessor_occurrence_ids == (
        bid.derived_occurrence_id, ask.derived_occurrence_id)
    parent_bytes = bid_path.read_bytes(), ask_path.read_bytes()
    path = tmp_path / "refused-native-d136.sqlite"
    owner = f.create_native_smart_imbalance_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        bid_reader=bid_reader, ask_reader=ask_reader,
        storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: NOW)
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(
        derived_signal_id="D136", subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10) == ()
    before = path.read_bytes()
    reader = f.create_native_smart_imbalance_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        storage=f.SQLiteReadStorageV1(str(path)))
    assert reader.list_derived_history(
        derived_signal_id="D136", subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10) == ()
    assert path.read_bytes() == before
    assert (bid_path.read_bytes(), ask_path.read_bytes()) == parent_bytes
