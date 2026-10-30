"""L05 native D134 pair, authored before production and NOT_RUN until L14."""

import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
BRIEF = "73e03e0700902098ecc8a0c9c6e3ffffd94bbc74ab8f27576368ccc0dd19cce0"
PROFILE = f.VersionRefV1("native-a4-stock", 1)
IDS = tuple("NVDA-M00-A-V1-A4-SEQ" + str(i) for i in (21, 22, 23, 24))
ROLES = {"R185", "R187", "R188", "R190"}


def _request():
    return f.NativeCalculationRequestV1("D134", PROFILE, T, CUTOFF, 2, None, None, 1, (), ())


def _four_roles():
    source = PublicDtoReader(scenarios=("A4", "C2"))
    # R189 is not a D134 mathematical dependency. Original native observations
    # still retain their price metadata; the calculation needs no price projection.
    source.projections = [
        x for x in source.projections if x.raw_signal_catalogue_id.value != "R189"
    ]
    return source


def test_native_success(tmp_path):
    source = _four_roles()
    path = tmp_path / "native-d134.sqlite"
    owner = f.create_native_smart_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    request = _request()
    result = owner.materialise(request)
    assert type(result) is f.NativeMeasurementOccurrenceV1
    assert type(result.result) is Decimal and result.result == Decimal("8")
    assert result.request == request and result.predecessors == ()
    assert result.quote_assembly is None and result.source is not None
    snapshot = result.source
    assert snapshot.profile.ref == PROFILE
    assert snapshot.profile.provider == "foundation-controlled-ibkr-m00-v1"
    assert snapshot.profile.variant == "ibkr-smart-depth/native-v1"
    assert snapshot.profile.subject_instrument == "NVDA-STK-CONTROL-1"
    assert snapshot.profile.request == "STK-SMART-R1"
    assert snapshot.profile.generation == "STK-SMART-G1"
    assert snapshot.profile.requested_exchange == "SMART"
    assert snapshot.profile.ingestion_scope == "STK1/SMART/G1"
    assert snapshot.profile.security_type == "STK" and snapshot.profile.option_right is None
    assert snapshot.profile.contract_identity == "NVDA-STK-CONTROL-1|STK|None|USD|None|None|1"
    assert snapshot.profile.source_context_ref == f.VersionRefV1("native-a4-stock-context", 1)
    assert snapshot.profile.warmup_observation_ids == IDS
    assert snapshot.controls == ()
    assert tuple(
        (r.side, r.position, r.price, r.size, r.requested_exchange, r.observation_occurrence_id)
        for r in snapshot.standing_rows
    ) == (
        (1, 0, None, Decimal("5"), "SMART", IDS[0]),
        (1, 1, None, Decimal("3"), "SMART", IDS[1]),
        (0, 0, None, Decimal("2"), "SMART", IDS[2]),
        (0, 1, None, Decimal("4"), "SMART", IDS[3]),
    )
    assert result.selected_event_ids == IDS[:2]
    assert len(snapshot.raw_input_lineage) == 16
    assert {x.raw_signal_id for x in snapshot.raw_input_lineage} == ROLES
    assert {x.observation_occurrence_id for x in snapshot.raw_input_lineage} == set(IDS)
    for line in snapshot.raw_input_lineage:
        item = next(
            x
            for x in source.projections
            if x.observation_occurrence_id.value == line.observation_occurrence_id
            and x.raw_signal_catalogue_id.value == line.raw_signal_id
        )
        assert typed_tree(line.projection) == typed_tree(item)
        assert type(line.canonical_value) is (Decimal if line.raw_signal_id == "R190" else int)
        assert typed_tree(line.canonical_value) == typed_tree(item.native_value)
        assert line.projection_mapping_ref == f.VersionRefV1(item.projection_mapping_id, 1)
        assert line.time_basis == "collector_receipt" and line.event_time_utc is None
        assert item.source_temporal_kind == "receipt_only"
        assert item.source_timestamp_raw is None and item.source_timezone_native is None
        assert line.received_ts_utc == item.received_ts_utc
    assert result.definition.calculation_definition_version == "D134-NATIVE-BID-TOP2-1"
    assert result.definition.raw_dependencies == ("R185", "R187", "R188", "R190")
    assert result.definition.derived_dependencies == ()
    assert result.units == "shares" and result.result_shape == "decimal"
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        T + timedelta(seconds=2),
    )
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
    before = path.read_bytes()
    reader = f.create_native_smart_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    reopened = reader.get_derived_occurrence(result.derived_occurrence_id)
    assert type(reopened) is f.NativeMeasurementOccurrenceV1
    assert typed_tree(reopened) == typed_tree(result)
    history = reader.list_derived_history(
        derived_signal_id="D134",
        subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=1,
    )
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(result)
    assert path.read_bytes() == before


def test_native_refusal(tmp_path):
    source = _four_roles()
    source.projections = [
        x
        for x in source.projections
        if not (
            x.raw_signal_catalogue_id.value == "R187"
            and x.observation_occurrence_id.value == IDS[-1]
        )
    ]
    final = tuple(x for x in source.projections if x.observation_occurrence_id.value == IDS[-1])
    assert len(final) == 3
    assert {x.raw_signal_catalogue_id.value for x in final} == {"R185", "R188", "R190"}
    assert tuple(x.native_value for x in final) == (1, 0, Decimal("4"))
    assert {
        x.raw_signal_catalogue_id.value
        for x in source.projections
        if x.observation_occurrence_id.value == IDS[0]
    } == ROLES
    path = tmp_path / "refused-native-d134.sqlite"
    owner = f.create_native_smart_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    assert owner.materialise(_request()) is None
    assert (
        owner.reads.list_derived_history(
            derived_signal_id="D134",
            subject_instrument="NVDA-STK-CONTROL-1",
            effective_at_or_before_utc=T,
            knowledge_at_or_before_utc=CUTOFF,
            limit=10,
        )
        == ()
    )
    before = path.read_bytes()
    reader = f.create_native_smart_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    assert (
        reader.list_derived_history(
            derived_signal_id="D134",
            subject_instrument="NVDA-STK-CONTROL-1",
            effective_at_or_before_utc=T,
            knowledge_at_or_before_utc=CUTOFF,
            limit=10,
        )
        == ()
    )
    assert path.read_bytes() == before
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
