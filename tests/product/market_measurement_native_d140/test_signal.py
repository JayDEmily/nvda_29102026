"""L10 native deletion pair; authored before production, NOT_RUN until L14."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree  # noqa: E402

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T+timedelta(seconds=1), T+timedelta(seconds=2)
BRIEF = "91f680af16d74b589883d363242572de2dc95360f036db5ccfa5fb9b1ae269c2"
SOURCE_BRIEF = "5b777c5842b091f6dc4bef148970c4cf81b68864bd24f5a1633d392f38d96ead"
PROFILE = f.VersionRefV1("native-d140-delete", 1)
PROVIDER = "foundation-controlled-native-reconciliation-v1"
VARIANT = "ibkr-smart-depth/receipt-rate-v1"
ROLES = (("R001", ("time", "receipt"), "UTC_datetime"),
         ("R185", ("position",), "book-position"),
         ("R187", ("operation",), "operation-code"),
         ("R188", ("side",), "side-code"), ("R190", ("size",), "shares"))
WARMUP = (("REC-RATE-B0", 9, 1, 0, 5), ("REC-RATE-B1", 8, 1, 1, 6),
          ("REC-RATE-B2", 7, 1, 2, 7), ("REC-RATE-A0", 6, 0, 0, 2))
WARMUP_IDS = tuple(x[0] for x in WARMUP)


def _source(nonexistent=False):
    source = PublicDtoReader(scenarios=())
    collector = {"subject": "NVDA", "request": "REC-RATE-R1",
                 "generation": "REC-RATE-G1", "requested_exchange": "SMART",
                 "scenario_id": "REC-RATE", "contract_spec": {
                     "security_type": "STK", "right": None, "currency": "USD",
                     "expiry": None, "strike": None, "multiplier": 1}}
    identity = r.RawSelectionIdentityV1(tuple((key, collector[key]) for key in (
        "subject", "request", "generation", "requested_exchange", "scenario_id")))
    rows = (*WARMUP, ("REC-RATE-D1", 1, 1, 9 if nonexistent else 1, 0))
    for sequence, (oid, age, side, position, size) in enumerate(rows, 1):
        receipt = T-timedelta(seconds=age)
        native = {"_collector": collector, "time": {"receipt": receipt},
                  "operation": 2 if oid == "REC-RATE-D1" else 0, "side": side,
                  "position": position, "size": Decimal(size),
                  "isSmartDepth": True, "marketMaker": "SYNTHETIC"}
        observation = r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(oid),
            delivery_artifact_ref=r.delivery_artifact_ref("native-rate-synthetic-v1"),
            source_provider=r.provider_id(PROVIDER), native_record=native,
            received_ts_utc=receipt, ingestion_sequence=sequence,
            ingestion_sequence_scope=r.ingestion_sequence_scope("NVDA/REC-RATE/G1"),
            source_temporal_kind="receipt_only",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(x[0]) for x in ROLES),
            source_product_api="TWS_SOCKET_API_SYNTHETIC_SPECIMEN",
            source_endpoint_callback="updateMktDepthL2", native_identifier="NVDA",
            source_variant=VARIANT, subject_instrument="NVDA", native_units="mixed_book_roles")
        source.observations.append(observation)
        for rid, path, unit in ROLES:
            value = receipt if rid == "R001" else native[path[0]]
            source.projections.append(r.ProjectedRawValueV1(
                r.RawSignalCatalogueId(rid), observation.observation_occurrence_id,
                "mmt-native-rate-"+rid.lower(), 1, PROVIDER, VARIANT, path, value, unit,
                "NVDA", "receipt_only", None, None, receipt, sequence,
                observation.ingestion_sequence_scope, None, identity))
    return source


def _request():
    return f.NativeCalculationRequestV1(
        "D140", PROFILE, T, CUTOFF, 0, None, 2, 1, (1, 2), ())


def test_native_success(tmp_path):
    source = _source()
    # Observe the actual complete pre-window standing6 before native size0 delete.
    prefix_owner = f.create_native_source_owner(
        admission=f.OwnerAdmissionV1("M02", SOURCE_BRIEF), raw_reader=source,
        storage=f.MemoryStorageV1(), utc_now=lambda: NOW)
    prefix = prefix_owner.materialise(f.NativeSourceRequestV1(PROFILE, T-timedelta(seconds=2), CUTOFF))
    assert type(prefix) is f.NativeSourceSnapshotV1
    assert tuple((x.side, x.position, x.size) for x in prefix.standing_rows) == (
        (1, 0, Decimal(5)), (1, 1, Decimal(6)), (1, 2, Decimal(7)), (0, 0, Decimal(2)))
    assert prefix.profile.warmup_observation_ids == WARMUP_IDS
    assert len(prefix.raw_input_lineage) == 20
    delete = tuple(x for x in source.projections
                   if x.observation_occurrence_id.value == "REC-RATE-D1")
    assert tuple(x.native_value for x in delete) == (T-timedelta(seconds=1), 1, 2, 1, Decimal(0))
    path = tmp_path / "native-d140.sqlite"
    owner = f.create_native_book_delete_rate_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF), raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: NOW)
    request = _request()
    value = owner.materialise(request)
    assert type(value) is f.NativeMeasurementOccurrenceV1
    assert type(value.result) is f.BookRatePairV1
    assert value.result == f.BookRatePairV1(f.ExactRatioV1(1, 2), f.ExactRatioV1(3, 1))
    assert value.request == request and value.predecessors == () and value.quote_assembly is None
    assert value.selected_event_ids == ("REC-RATE-D1",)
    assert value.source is not None
    snapshot = value.source
    assert snapshot.profile.ref == PROFILE
    assert (snapshot.profile.provider, snapshot.profile.variant, snapshot.profile.subject_instrument,
            snapshot.profile.request, snapshot.profile.generation, snapshot.profile.ingestion_scope,
            snapshot.profile.requested_exchange) == (
        PROVIDER, VARIANT, "NVDA", "REC-RATE-R1", "REC-RATE-G1", "NVDA/REC-RATE/G1", "SMART")
    assert snapshot.profile.time_basis == "collector_receipt" and snapshot.controls == ()
    assert snapshot.profile.security_type == "STK" and snapshot.profile.option_right is None
    assert snapshot.profile.contract_identity == "NVDA|STK|None|USD|None|None|1"
    assert snapshot.profile.complete_from_utc == T-timedelta(seconds=10)
    assert snapshot.profile.warmup_observation_ids == WARMUP_IDS
    assert snapshot.profile.warmup_side_levels == ((0, 1), (1, 3))
    assert tuple((x.side, x.position, x.price, x.size) for x in snapshot.standing_rows) == (
        (1, 0, None, Decimal(5)), (1, 1, None, Decimal(7)), (0, 0, None, Decimal(2)))
    assert len(snapshot.raw_input_lineage) == 25
    assert {x.raw_signal_id for x in snapshot.raw_input_lineage} == {x[0] for x in ROLES}
    assert {x.observation_occurrence_id for x in snapshot.raw_input_lineage} == {*WARMUP_IDS, "REC-RATE-D1"}
    for line in snapshot.raw_input_lineage:
        original = next(x for x in source.projections
                        if x.observation_occurrence_id.value == line.observation_occurrence_id
                        and x.raw_signal_catalogue_id.value == line.raw_signal_id)
        assert typed_tree(line.projection) == typed_tree(original)
        assert typed_tree(line.canonical_value) == typed_tree(original.native_value)
        assert type(line.canonical_value) is (
            datetime if line.raw_signal_id == "R001" else Decimal if line.raw_signal_id == "R190" else int)
        assert line.time_basis == "collector_receipt" and line.event_time_utc is None
        assert original.source_temporal_kind == "receipt_only"
        assert original.source_timestamp_raw is None and original.source_timezone_native is None
        assert line.received_ts_utc == original.received_ts_utc
        assert line.projection_mapping_ref == f.VersionRefV1(original.projection_mapping_id, 1)
        if line.raw_signal_id == "R001":
            observation = next(x for x in source.observations
                               if x.observation_occurrence_id.value == line.observation_occurrence_id)
            assert original.native_field_path == ("time", "receipt")
            assert line.canonical_value == observation.received_ts_utc
            assert observation.native_record["time"]["receipt"] == observation.received_ts_utc
    assert value.definition.calculation_definition_version == "D140-NATIVE-RECEIPT-DELETE-1"
    assert value.definition.kernel_id == "K08_RULE_BUCKET_POLICY"
    assert value.definition.parameter_profile == "P_RULE"
    assert value.definition.raw_dependencies == tuple(x[0] for x in ROLES)
    assert value.definition.derived_dependencies == ()
    assert value.units == "events or size/time" and value.result_shape == "book_rate_pair"
    assert (value.effective_as_of_utc, value.knowledge_cutoff_utc, value.calculated_at_utc) == (
        T, CUTOFF, NOW)
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
    before = path.read_bytes()
    reader = f.create_native_book_delete_rate_reader(admission=f.OwnerAdmissionV1("M02", BRIEF),
                                                    storage=f.SQLiteReadStorageV1(str(path)))
    assert typed_tree(reader.get_derived_occurrence(value.derived_occurrence_id)) == typed_tree(value)
    history = reader.list_derived_history(derived_signal_id="D140", subject_instrument="NVDA",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(value)
    assert path.read_bytes() == before


def test_native_refusal(tmp_path):
    source = _source(nonexistent=True)
    final = tuple(x for x in source.projections
                  if x.observation_occurrence_id.value == "REC-RATE-D1")
    assert len(final) == 5 and len(source.projections) == 25
    assert {x.raw_signal_catalogue_id.value for x in final} == {x[0] for x in ROLES}
    assert tuple(x.native_value for x in final) == (T-timedelta(seconds=1), 9, 2, 1, Decimal(0))
    assert not any("control" in x.native_record["_collector"] for x in source.observations)
    assert all({x.raw_signal_catalogue_id.value for x in source.projections
                if x.observation_occurrence_id.value == oid} == {x[0] for x in ROLES}
               for oid in WARMUP_IDS)
    path = tmp_path / "refused-native-d140.sqlite"
    owner = f.create_native_book_delete_rate_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF), raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: NOW)
    assert owner.materialise(_request()) is None
    query = dict(derived_signal_id="D140", subject_instrument="NVDA",
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    assert owner.reads.list_derived_history(**query) == ()
    before = path.read_bytes()
    reader = f.create_native_book_delete_rate_reader(admission=f.OwnerAdmissionV1("M02", BRIEF),
                                                    storage=f.SQLiteReadStorageV1(str(path)))
    assert reader.list_derived_history(**query) == ()
    assert path.read_bytes() == before
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
