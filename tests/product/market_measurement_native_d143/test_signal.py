"""L11 native subscribed-side MPID pair, authored before production; NOT_RUN."""

import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
BRIEF = "b69227f2fbb9cc29702a9bf43ea2b88168757948074675eb48e756c143a40886"
SOURCE_BRIEF = "5b777c5842b091f6dc4bef148970c4cf81b68864bd24f5a1633d392f38d96ead"
PROFILE = f.VersionRefV1("native-c2-stock", 1)
IDS = tuple("COH-DIRECT-STK-0" + str(i) for i in (1, 2, 3, 4))
ROLES = ("R192", "R193", "R194", "R195", "R196", "R197")


def _request():
    return f.NativeCalculationRequestV1("D143", PROFILE, T, CUTOFF, 2, None, None, None, (), ())


def _append_mutation(source, *, deletion):
    # Explicit L01 direct_mutation recipe; original public C2 DTOs stay intact.
    template = next(x for x in source.observations if x.observation_occurrence_id.value == IDS[0])
    oid = "REC-DIRECT-D0" if deletion else "REC-DIRECT-I0"
    receipt = T - timedelta(seconds=1, milliseconds=50 if deletion else 100)
    sequence = 406 if deletion else 405
    native = dict(template.native_record)
    native.update(
        position=0,
        operation=2 if deletion else 0,
        side=1,
        price=Decimal("99.10"),
        size=Decimal("0") if deletion else Decimal("9"),
        marketMaker="BETA",
    )
    observation = replace(
        template,
        observation_occurrence_id=r.observation_occurrence_id(oid),
        delivery_artifact_ref=r.delivery_artifact_ref("native-d143-synthetic:" + oid),
        native_record=native,
        received_ts_utc=receipt,
        ingestion_sequence=sequence,
    )
    source.observations.append(observation)
    originals = tuple(x for x in source.projections if x.observation_occurrence_id.value == IDS[0])
    for item in originals:
        identity = r.RawSelectionIdentityV1(
            tuple(
                (key, "BETA" if key == "marketMaker" else value)
                for key, value in item.selection_identity.values
            )
        )
        source.projections.append(
            replace(
                item,
                observation_occurrence_id=observation.observation_occurrence_id,
                native_value=native[item.native_field_path[0]],
                received_ts_utc=receipt,
                ingestion_sequence=sequence,
                selection_identity=identity,
            )
        )


def test_native_success(tmp_path):
    source = PublicDtoReader(scenarios=("C2", "A4"))
    _append_mutation(source, deletion=False)
    source_owner = f.create_native_source_owner(
        admission=f.OwnerAdmissionV1("M02", SOURCE_BRIEF),
        raw_reader=source,
        storage=f.MemoryStorageV1(),
        utc_now=lambda: NOW,
    )
    intermediate = source_owner.materialise(
        f.NativeSourceRequestV1(PROFILE, T - timedelta(seconds=1, milliseconds=100), CUTOFF)
    )
    assert type(intermediate) is f.NativeSourceSnapshotV1
    assert tuple(
        (x.mpid, x.side, x.position, x.price, x.size, x.observation_occurrence_id)
        for x in intermediate.standing_rows
    ) == (
        ("BETA", 1, 0, Decimal("99.10"), Decimal("9"), "REC-DIRECT-I0"),
        ("ALPHA", 1, 1, Decimal("99.00"), Decimal("4"), IDS[0]),
        ("BETA", 1, 2, Decimal("98.50"), Decimal("1"), IDS[1]),
        ("ALPHA", 0, 0, Decimal("101.00"), Decimal("2"), IDS[2]),
        ("BETA", 0, 1, Decimal("101.50"), Decimal("1"), IDS[3]),
    )
    assert len(intermediate.raw_input_lineage) == 30
    _append_mutation(source, deletion=True)
    path = tmp_path / "native-d143.sqlite"
    owner = f.create_native_direct_venue_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: NOW,
    )
    request = _request()
    value = owner.materialise(request)
    assert type(value) is f.NativeMeasurementOccurrenceV1
    assert type(value.result) is f.VenueConcentrationV1
    assert value.result == f.VenueConcentrationV1(
        ("ALPHA", "BETA"), (f.ExactRatioV1(3, 4), f.ExactRatioV1(1, 4)), f.ExactRatioV1(5, 8)
    )
    assert value.request == request and value.predecessors == () and value.quote_assembly is None
    assert value.source is not None
    snapshot = value.source
    assert snapshot.profile.ref == PROFILE
    assert (
        snapshot.profile.provider,
        snapshot.profile.variant,
        snapshot.profile.subject_instrument,
        snapshot.profile.request,
        snapshot.profile.generation,
        snapshot.profile.ingestion_scope,
        snapshot.profile.requested_exchange,
    ) == (
        "foundation-controlled-ibkr-m00-coherent-v2",
        "ibkr-direct-depth/native-v2",
        "NVDA-STK-CONTROL-1",
        "COH-DIRECT-STK-R1",
        "COH-DIRECT-STK-GEN1",
        "STK1/DIRECT-EXCH1/GEN1",
        "SYNTH-DIRECT-EXCHANGE-1",
    )
    assert snapshot.profile.security_type == "STK" and snapshot.profile.option_right is None
    assert snapshot.profile.contract_identity == "NVDA-STK-CONTROL-1|STK|None|USD|None|None|1"
    assert snapshot.profile.source_context_ref == f.VersionRefV1("native-c2-stock-context", 1)
    assert snapshot.profile.warmup_observation_ids == IDS
    assert snapshot.profile.warmup_side_levels == ((0, 2), (1, 2))
    assert snapshot.profile.complete_from_utc == T - timedelta(seconds=2)
    assert snapshot.controls == () and snapshot.profile.time_basis == "collector_receipt"
    assert tuple(
        (x.mpid, x.side, x.position, x.price, x.size, x.observation_occurrence_id)
        for x in snapshot.standing_rows
    ) == (
        ("ALPHA", 1, 0, Decimal("99.00"), Decimal("4"), IDS[0]),
        ("BETA", 1, 1, Decimal("98.50"), Decimal("1"), IDS[1]),
        ("ALPHA", 0, 0, Decimal("101.00"), Decimal("2"), IDS[2]),
        ("BETA", 0, 1, Decimal("101.50"), Decimal("1"), IDS[3]),
    )
    assert sum(x.size for x in snapshot.standing_rows if x.mpid == "ALPHA") == Decimal("6")
    assert sum(x.size for x in snapshot.standing_rows if x.mpid == "BETA") == Decimal("2")
    assert all(
        x.requested_exchange == "SYNTH-DIRECT-EXCHANGE-1" and x.mpid != x.requested_exchange
        for x in snapshot.standing_rows
    )
    assert value.selected_event_ids == IDS
    assert len(snapshot.raw_input_lineage) == 36
    assert {x.observation_occurrence_id for x in snapshot.raw_input_lineage} == {
        *IDS,
        "REC-DIRECT-I0",
        "REC-DIRECT-D0",
    }
    assert {x.raw_signal_id for x in snapshot.raw_input_lineage} == set(ROLES)
    for line in snapshot.raw_input_lineage:
        original = next(
            x
            for x in source.projections
            if x.observation_occurrence_id.value == line.observation_occurrence_id
            and x.raw_signal_catalogue_id.value == line.raw_signal_id
        )
        assert typed_tree(line.projection) == typed_tree(original)
        assert typed_tree(line.canonical_value) == typed_tree(original.native_value)
        assert type(line.canonical_value) is (
            str
            if line.raw_signal_id == "R193"
            else int
            if line.raw_signal_id in ("R192", "R194", "R195")
            else Decimal
        )
        assert line.time_basis == "collector_receipt" and line.event_time_utc is None
        assert original.source_temporal_kind == "receipt_only"
        assert original.source_timestamp_raw is None and original.source_timezone_native is None
        assert line.received_ts_utc == original.received_ts_utc
        assert line.projection_mapping_ref == f.VersionRefV1(original.projection_mapping_id, 1)
        assert original.selection_identity.value_for("marketMaker") in ("ALPHA", "BETA")
        assert original.selection_identity.value_for("isSmartDepth") is False
    assert (
        value.definition.calculation_definition_version
        == "D143-NATIVE-SUBSCRIBED-ALL-ROWS-MPID-HHI-1"
    )
    assert value.definition.kernel_id == "K02_ALGEBRA"
    assert value.definition.parameter_profile == "P_BASIC"
    assert (
        value.definition.raw_dependencies == ROLES and value.definition.derived_dependencies == ()
    )
    assert (
        value.units == "normalised MPID concentration"
        and value.result_shape == "venue_concentration"
    )
    assert (value.effective_as_of_utc, value.knowledge_cutoff_utc, value.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
    before = path.read_bytes()
    reader = f.create_native_direct_venue_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    assert typed_tree(reader.get_derived_occurrence(value.derived_occurrence_id)) == typed_tree(
        value
    )
    history = reader.list_derived_history(
        derived_signal_id="D143",
        subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(value)
    assert path.read_bytes() == before
    # Later source callbacks cannot mutate the previously returned public snapshot.
    assert intermediate.standing_rows[0].observation_occurrence_id == "REC-DIRECT-I0"
    assert intermediate.standing_rows[1].position == 1


def test_native_refusal(tmp_path):
    source = PublicDtoReader(scenarios=("C2", "A4"))
    source.projections = [
        x
        for x in source.projections
        if not (
            x.observation_occurrence_id.value == IDS[-1]
            and x.raw_signal_catalogue_id.value == "R193"
        )
    ]
    final = tuple(x for x in source.projections if x.observation_occurrence_id.value == IDS[-1])
    assert len(final) == 5
    assert {x.raw_signal_catalogue_id.value for x in final} == set(ROLES) - {"R193"}
    assert next(
        x.native_value for x in final if x.raw_signal_catalogue_id.value == "R197"
    ) == Decimal("1")
    assert all(
        {
            x.raw_signal_catalogue_id.value
            for x in source.projections
            if x.observation_occurrence_id.value == oid
        }
        == set(ROLES)
        for oid in IDS[:-1]
    )
    path = tmp_path / "refused-native-d143.sqlite"
    owner = f.create_native_direct_venue_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: NOW,
    )
    assert owner.materialise(_request()) is None
    query = dict(
        derived_signal_id="D143",
        subject_instrument="NVDA-STK-CONTROL-1",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    assert owner.reads.list_derived_history(**query) == ()
    before = path.read_bytes()
    reader = f.create_native_direct_venue_reader(
        admission=f.OwnerAdmissionV1("M02", BRIEF), storage=f.SQLiteReadStorageV1(str(path))
    )
    assert reader.list_derived_history(**query) == ()
    assert path.read_bytes() == before
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
