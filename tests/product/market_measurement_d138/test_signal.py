"""D138: actual public D011 and six complete typed SMART groups; reset refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 16, 1, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_slope_v1"
GENERATION = "controlled-smart-slope-generation/1"
BRIEF = "9506421b312273a849b16ee930c59b553e48c6ac096b7a4c081a31eb856e9150"
D011_BRIEF = "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
ROLES = (
    ("R185", "position", "book_position"), ("R187", "operation", "book_operation"),
    ("R188", "side", "book_side"), ("R189", "price", "USD_per_share"),
    ("R190", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d138-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER, VARIANT,
    ("book", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d138-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D138", "D138-L2-CONTRACT-20261016-01", "K06_REGRESSION_DEPENDENCE",
    "OLS(cumulative standing depth, abs(price - actual D011 midpoint)) per side",
    tuple(raw for raw, _, _ in ROLES), ("D011",), "P_REGRESSION", "depth per price distance",
    "book_slope_pair", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d138-three-level", 1, "P_REGRESSION", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d138-smart-positional", 1), PROVIDER, VARIANT, GENERATION,
    T - timedelta(seconds=10), 100,
)


def admit(raw, identity, provider, variant, record, ids, stamp, sequence):
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(identity),
        delivery_artifact_ref=r.delivery_artifact_ref("d138-controlled"),
        source_provider=r.provider_id(provider), native_record=record,
        received_ts_utc=stamp, ingestion_sequence=sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope(provider + "/" + variant),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(x) for x in ids),
        source_variant=variant, subject_instrument=SUBJECT, native_units="mixed_book_roles",
        source_timestamp_raw=stamp.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    ))


def midpoint(raw, tmp_path):
    provider, variant = "foundation-pilot-fixture", "cash_quote_v1"
    maps = tuple(r.RawSignalProjectionMappingV1(
        "mmt-pilot-" + field, 1, r.RawSignalCatalogueId(rid), provider, variant,
        ("quote", field), "price", (),
    ) for rid, field in (("R034", "bid"), ("R035", "ask")))
    for i, (mapping, value) in enumerate(zip(maps, (Decimal("99"), Decimal("101")), strict=True)):
        event = T - timedelta(seconds=2 - i)
        admit(raw, "d138-d011-" + str(i), provider, variant,
              {"quote": {mapping.native_field_path[1]: value}},
              (mapping.raw_signal_catalogue_id.value,), event, i + 1)
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert len(page.items) == 1 and page.items[0].native_value == value
    definition = f.CalculationDefinitionV1(
        "D011", "D011-MIDPOINT-1", "K02_ALGEBRA", "(R034 + R035) / 2",
        ("R034", "R035"), (), "P_BASIC", "price", "scalar_decimal", AUTHORITY,
    )
    parameter = f.CalculationParameterSetV1(
        "mmt-pilot-basic", 1, "P_BASIC", SUBJECT, (SUBJECT,),
    )
    policy = f.InputSelectionPolicyVersionV1(
        "mmt-pilot-selection", 1, ("subject_instrument",), timedelta(seconds=60),
        timedelta(seconds=10), ("true_instant",), (), provider, variant,
        provider + "/" + variant, 100, 1000,
    )
    unit = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal(1), Decimal(0))
    owner = f.create_owner(
        admission=f.OwnerAdmissionV1("M02", D011_BRIEF), raw_projection_reader=raw.reads,
        definitions=(definition,), parameter_sets=(parameter,), input_selection_policies=(policy,),
        unit_conventions=(unit,), raw_projection_mappings=maps,
        storage=f.SQLiteStorageV1(str(tmp_path / "d011.sqlite"), True), utc_now=lambda: NOW,
    )
    request = f.CalculationRequestV1(
        "D011", SUBJECT, T, CUTOFF, definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1), f.VersionRefV1(policy.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            m.raw_signal_catalogue_id.value, f.VersionRefV1(m.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for m in maps),
    )
    result = owner.materialise(request)
    assert result is not None and result.result == Decimal(100)
    assert tuple(line.raw_signal_id for line in result.raw_input_lineage) == ("R034", "R035")
    return owner, result


@pytest.mark.parametrize("reset", (False, True), ids=("success", "refusal"))
def test_d138_signal(tmp_path, reset):
    raw = r.create_owner()
    parent_owner, parent = midpoint(raw, tmp_path)
    groups = []
    for i, (side, pos, price, size) in enumerate((
        (0, 0, 99, 2), (0, 1, 98, 3), (0, 2, 97, 4),
        (1, 0, 101, 1), (1, 1, 102, 2), (1, 2, 103, 3),
    )):
        record = {"generation": {"id": GENERATION}, "event": {"id": f"d138-event-{i}"},
                  "subject": {"id": SUBJECT}, "book": {
                      "position": pos, "operation": 0, "side": side,
                      "price": Decimal(price), "size": Decimal(size),
                  }}
        stamp = T - timedelta(seconds=6 - i)
        admit(raw, f"d138-book-{i}", PROVIDER, VARIANT, record,
              tuple(x[0] for x in ROLES), stamp, i + 3)
        groups.append((record, stamp))
    if reset:
        admit(raw, "d138-reset", PROVIDER, VARIANT,
              {"generation": {"id": GENERATION}, "event": {"id": "d138-reset"},
               "subject": {"id": SUBJECT}, "book": {"operation": 317}},
              ("R187",), T, 9)
    for role, mapping in enumerate(MAPS):
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert len(page.items) == (7 if reset and role == 1 else 6)
        assert all(type(x.native_value) is (int if role < 3 else Decimal)
                   for x in page.items)
        identities = {
            x.observation_occurrence_id.value for x in page.items
            if x.observation_occurrence_id.value != "d138-reset"
        }
        assert identities == {f"d138-book-{i}" for i in range(6)}
    request = f.BookSlopeRequestV1(f.CalculationRequestV1(
        "D138", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            raw_id, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw_id, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, parent.derived_occurrence_id, 3)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d138.sqlite")
    owner = f.create_book_slope_owner(
        admission=admission, raw_projection_reader=raw.reads,
        predecessor_reader=parent_owner.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    reader = f.create_book_slope_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    query = dict(derived_signal_id="D138", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if reset:
        assert occurrence is None and reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.BookSlopeOccurrenceV1
    assert occurrence.result == f.BookSlopePairV1(f.ExactRatioV1(7, 2), f.ExactRatioV1(5, 2))
    assert occurrence.predecessor == parent and occurrence.request == request
    assert occurrence.definition == DEFINITION and occurrence.parameter_set == PARAMETER
    assert occurrence.unit_conventions == UNITS and occurrence.projection_mappings == MAPS
    assert occurrence.owner_object_id == "M02" and occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.owner_namespace == "neutral_market_measurement_truth/book-slope/v1"
    assert occurrence.units == "depth per price distance"
    assert occurrence.result_shape == "book_slope_pair"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == 30
    assert len(occurrence.standing_rows) == 6
    assert tuple((x.side, x.position, x.size) for x in occurrence.standing_rows) == (
        (0, 0, Decimal(2)), (0, 1, Decimal(3)), (0, 2, Decimal(4)),
        (1, 0, Decimal(1)), (1, 1, Decimal(2)), (1, 2, Decimal(3)),
    )
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
