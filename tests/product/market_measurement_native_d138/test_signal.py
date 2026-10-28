"""L08 native D138 pair, authored before production; NOT_RUN until L14."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
import sys

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree  # noqa: E402

T = datetime(2026, 10, 16, 1, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
BRIEF = "cd2519685a80a453b839ac10a34d8488f73b8b1b87ef01a10c346e1445f5130b"
D011_BRIEF = "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
PROFILE = f.VersionRefV1("native-d138-slope", 1)
PROVIDER = "foundation-controlled-native-reconciliation-v1"
VARIANT = "ibkr-smart-depth/receipt-slope-v1"
ROLES = (("R185", "position", "book-position"),
         ("R187", "operation", "operation-code"),
         ("R188", "side", "side-code"), ("R189", "price", "USD/share"),
         ("R190", "size", "shares"))
ROWS = (("REC-SLOPE-B0", 51, 1, 0, 99, 2),
        ("REC-SLOPE-B1", 52, 1, 1, 98, 3),
        ("REC-SLOPE-B2", 53, 1, 2, 97, 4),
        ("REC-SLOPE-A0", 54, 0, 0, 101, 5),
        ("REC-SLOPE-A1", 55, 0, 1, 102, 2),
        ("REC-SLOPE-A2", 56, 0, 2, 103, 3))
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c"),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549"),
)


def _slope_source(reset=False):
    source = PublicDtoReader(scenarios=())
    contract = {"security_type": "STK", "right": None, "currency": "USD",
                "expiry": None, "strike": None, "multiplier": 1}
    collector = {"subject": "NVDA", "request": "REC-SLOPE-R1",
                 "generation": "REC-SLOPE-G1", "requested_exchange": "SMART",
                 "scenario_id": "REC-SLOPE", "contract_spec": contract}
    identity = r.RawSelectionIdentityV1(tuple(
        (key, collector[key]) for key in (
            "subject", "request", "generation", "requested_exchange", "scenario_id")))
    for sequence, (oid, second, side, position, price, size) in enumerate(ROWS, 1):
        receipt = T.replace(minute=59, second=second) - timedelta(hours=1)
        native = {"_collector": collector, "operation": 0, "side": side,
                  "position": position, "price": Decimal(price), "size": Decimal(size),
                  "isSmartDepth": True, "marketMaker": "SYNTHETIC"}
        observation = r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(oid),
            delivery_artifact_ref=r.delivery_artifact_ref("native-d138-synthetic-v1"),
            source_provider=r.provider_id(PROVIDER), native_record=native,
            received_ts_utc=receipt, ingestion_sequence=sequence,
            ingestion_sequence_scope=r.ingestion_sequence_scope("NVDA/REC-SLOPE/G1"),
            source_temporal_kind="receipt_only",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(x[0]) for x in ROLES),
            source_product_api="TWS_SOCKET_API_SYNTHETIC_SPECIMEN",
            source_endpoint_callback="updateMktDepthL2", native_identifier="NVDA",
            source_variant=VARIANT, subject_instrument="NVDA", native_units="mixed_book_roles",
        )
        source.observations.append(observation)
        for rid, field, unit in ROLES:
            source.projections.append(r.ProjectedRawValueV1(
                r.RawSignalCatalogueId(rid), observation.observation_occurrence_id,
                "mmt-native-d138-" + rid.lower(), 1, PROVIDER, VARIANT,
                (field,), native[field], unit, "NVDA", "receipt_only", None, None,
                receipt, sequence, observation.ingestion_sequence_scope, None, identity))
    if reset:
        control = dict(collector)
        control["control"] = {
            "schema_version": "m00-control-envelope/1", "kind": "error317",
            "origin": "provider_callback", "request": "REC-SLOPE-R1",
            "generation_before": "REC-SLOPE-G1", "generation_after": "REC-SLOPE-G1",
            "invalidates": True,
        }
        source.observations.append(replace(source.observations[-1],
            observation_occurrence_id=r.observation_occurrence_id("REC-SLOPE-RESET"),
            native_record={"_collector": control, "errorCode": 317},
            received_ts_utc=T-timedelta(seconds=1), ingestion_sequence=7,
            raw_signal_catalogue_ids=None, source_endpoint_callback="error"))
    return source


def _actual_midpoint(tmp_path):
    # Independent local public DTO inputs for the unchanged D011 profile.
    # No M00 owner/replay and no import of a historical private fixture.
    source = PublicDtoReader(scenarios=())
    maps = tuple(r.RawSignalProjectionMappingV1(
        "mmt-pilot-" + field, 1, r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture", "cash_quote_v1", ("quote", field), "price", ())
        for rid, field in (("R034", "bid"), ("R035", "ask")))
    for i, (mapping, value) in enumerate(zip(maps, (Decimal("99"), Decimal("101")), strict=True)):
        receipt = T-timedelta(seconds=2-i)
        source.projections.append(r.ProjectedRawValueV1(
            mapping.raw_signal_catalogue_id, r.observation_occurrence_id("native-d138-d011-"+str(i)),
            mapping.mapping_id, 1, mapping.source_provider, mapping.source_variant,
            mapping.native_field_path, value, "price", "NVDA", "true_instant",
            receipt.isoformat().replace("+00:00", "Z"), "UTC", receipt, i+1,
            r.ingestion_sequence_scope("foundation-pilot-fixture/cash_quote_v1"), None))
    definition = f.CalculationDefinitionV1(
        "D011", "D011-MIDPOINT-1", "K02_ALGEBRA", "(R034 + R035) / 2",
        ("R034", "R035"), (), "P_BASIC", "price", "scalar_decimal", AUTHORITY)
    parameter = f.CalculationParameterSetV1("mmt-pilot-basic", 1, "P_BASIC", "NVDA", ("NVDA",))
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-pilot-selection", 1, ("subject_instrument",), timedelta(seconds=60),
        timedelta(seconds=10), ("true_instant",), (), "foundation-pilot-fixture",
        "cash_quote_v1", "foundation-pilot-fixture/cash_quote_v1", 100, 1000)
    unit = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal(1), Decimal(0))
    path = tmp_path / "actual-d011.sqlite"
    owner = f.create_owner(
        admission=f.OwnerAdmissionV1("M02", D011_BRIEF), raw_projection_reader=source,
        definitions=(definition,), parameter_sets=(parameter,), input_selection_policies=(policy,),
        unit_conventions=(unit,), raw_projection_mappings=maps,
        storage=f.SQLiteStorageV1(str(path), True), utc_now=lambda: NOW)
    request = f.CalculationRequestV1(
        "D011", "NVDA", T, CUTOFF, "D011-MIDPOINT-1",
        f.VersionRefV1("mmt-pilot-basic", 1), f.VersionRefV1("mmt-pilot-selection", 1), (),
        tuple(f.RawInputBindingV1(m.raw_signal_catalogue_id.value,
              f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1("mmt-pilot-price", 1), "NVDA")
              for m in maps))
    parent = owner.materialise(request)
    assert type(parent) is f.DerivedSignalOccurrenceV1 and parent.result == Decimal("100")
    assert parent.subject_instrument == "NVDA" and parent.effective_as_of_utc == T
    assert parent.knowledge_cutoff_utc == CUTOFF
    assert tuple(x.raw_signal_id for x in parent.raw_input_lineage) == ("R034", "R035")
    before = path.read_bytes()
    reader = f.create_reader(admission=f.OwnerAdmissionV1("M02", D011_BRIEF),
                             storage=f.SQLiteReadStorageV1(str(path)))
    assert typed_tree(reader.get_derived_occurrence(parent.derived_occurrence_id)) == typed_tree(parent)
    assert path.read_bytes() == before
    return reader, parent, path, before


def _request(parent):
    return f.NativeCalculationRequestV1(
        "D138", PROFILE, T, CUTOFF, 3, None, None, None, (), (parent.derived_occurrence_id,))


def test_native_success(tmp_path):
    parent_reader, parent, parent_path, parent_bytes = _actual_midpoint(tmp_path)
    source = _slope_source()
    path = tmp_path / "native-d138.sqlite"
    owner = f.create_native_book_slope_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF), raw_reader=source,
        predecessor_reader=parent_reader, storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: NOW)
    result = owner.materialise(_request(parent))
    assert type(result) is f.NativeMeasurementOccurrenceV1
    assert type(result.result) is f.BookSlopePairV1
    assert result.result == f.BookSlopePairV1(f.ExactRatioV1(7, 2), f.ExactRatioV1(5, 2))
    assert typed_tree(result.predecessors) == typed_tree((parent,))
    assert result.source is not None and result.quote_assembly is None
    snapshot = result.source
    assert snapshot.profile.ref == PROFILE
    assert (snapshot.profile.provider, snapshot.profile.variant, snapshot.profile.subject_instrument,
            snapshot.profile.request, snapshot.profile.generation, snapshot.profile.ingestion_scope,
            snapshot.profile.requested_exchange) == (
        PROVIDER, VARIANT, "NVDA", "REC-SLOPE-R1", "REC-SLOPE-G1", "NVDA/REC-SLOPE/G1", "SMART")
    assert snapshot.profile.time_basis == "collector_receipt" and snapshot.controls == ()
    assert snapshot.profile.contract_identity == "NVDA|STK|None|USD|None|None|1"
    assert snapshot.profile.security_type == "STK" and snapshot.profile.option_right is None
    assert snapshot.profile.complete_from_utc == T-timedelta(seconds=10)
    assert snapshot.profile.warmup_observation_ids == tuple(x[0] for x in ROWS)
    assert result.selected_event_ids == tuple(x[0] for x in ROWS)
    assert tuple((x.side, x.position, x.price, x.size) for x in snapshot.standing_rows) == (
        (1, 0, Decimal(99), Decimal(2)), (1, 1, Decimal(98), Decimal(3)),
        (1, 2, Decimal(97), Decimal(4)), (0, 0, Decimal(101), Decimal(5)),
        (0, 1, Decimal(102), Decimal(2)), (0, 2, Decimal(103), Decimal(3)))
    assert len(snapshot.raw_input_lineage) == 30
    assert {x.raw_signal_id for x in snapshot.raw_input_lineage} == {x[0] for x in ROLES}
    for line in snapshot.raw_input_lineage:
        projection = next(x for x in source.projections
                          if x.raw_signal_catalogue_id.value == line.raw_signal_id
                          and x.observation_occurrence_id.value == line.observation_occurrence_id)
        assert typed_tree(line.projection) == typed_tree(projection)
        assert typed_tree(line.canonical_value) == typed_tree(projection.native_value)
        assert type(line.canonical_value) is (Decimal if line.raw_signal_id in ("R189", "R190") else int)
        assert line.time_basis == "collector_receipt" and line.event_time_utc is None
        assert projection.source_timestamp_raw is None and projection.source_timezone_native is None
        assert line.received_ts_utc == projection.received_ts_utc
        assert line.projection_mapping_ref == f.VersionRefV1(projection.projection_mapping_id, 1)
    assert result.definition.calculation_definition_version == "D138-NATIVE-THREE-LEVEL-OLS-1"
    assert result.definition.kernel_id == "K06_REGRESSION_DEPENDENCE"
    assert result.definition.parameter_profile == "P_REGRESSION"
    assert result.definition.raw_dependencies == tuple(x[0] for x in ROLES)
    assert result.definition.derived_dependencies == ("D011",)
    assert result.units == "depth per price distance" and result.result_shape == "book_slope_pair"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T, CUTOFF, NOW)
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
    before = path.read_bytes()
    reader = f.create_native_book_slope_reader(admission=f.OwnerAdmissionV1("M02", BRIEF),
                                              storage=f.SQLiteReadStorageV1(str(path)))
    assert typed_tree(reader.get_derived_occurrence(result.derived_occurrence_id)) == typed_tree(result)
    history = reader.list_derived_history(derived_signal_id="D138", subject_instrument="NVDA",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(result)
    assert path.read_bytes() == before and parent_path.read_bytes() == parent_bytes


def test_native_refusal(tmp_path):
    parent_reader, parent, parent_path, parent_bytes = _actual_midpoint(tmp_path)
    source = _slope_source(reset=True)
    assert len(source.projections) == 30
    assert {x.observation_occurrence_id.value for x in source.projections} == {x[0] for x in ROWS}
    assert source.observations[-1].source_endpoint_callback == "error"
    assert source.observations[-1].raw_signal_catalogue_ids is None
    assert source.observations[-1].native_record["errorCode"] == 317
    assert source.observations[-1].received_ts_utc == T-timedelta(seconds=1)
    assert all(x.received_ts_utc < source.observations[-1].received_ts_utc for x in source.projections)
    path = tmp_path / "refused-native-d138.sqlite"
    owner = f.create_native_book_slope_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF), raw_reader=source,
        predecessor_reader=parent_reader, storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: NOW)
    assert owner.materialise(_request(parent)) is None
    query = dict(derived_signal_id="D138", subject_instrument="NVDA",
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    assert owner.reads.list_derived_history(**query) == ()
    before = path.read_bytes()
    reader = f.create_native_book_slope_reader(admission=f.OwnerAdmissionV1("M02", BRIEF),
                                              storage=f.SQLiteReadStorageV1(str(path)))
    assert reader.list_derived_history(**query) == ()
    assert path.read_bytes() == before and parent_path.read_bytes() == parent_bytes
    assert source.control_queries > 0 and all(x is None for x in source.event_filters)
