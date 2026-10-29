"""D135 public top-two ask depth and reset invalidation."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_four_field_v1"
GENERATION = "controlled-smart-four-field-generation/1"
BRIEF = "9abfefacb6af1da85f8c22780d604edbe94bfb9e8a572aece3ecbd1856979840"
SUBJECT = "NVDA"
ROLES = (
    ("R185", "position", "book_position"), ("R187", "operation", "book_operation"),
    ("R188", "side", "book_side"), ("R190", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d134-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER,
    VARIANT, ("book", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d134-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
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
DEFINITION = f.CalculationDefinitionV1(
    "D135", "D135-SMART-TOP-TWO-ASK-1", "K02_ALGEBRA",
    "sum(top two standing SMART ask sizes after positional replay)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "shares", "scalar_decimal",
    AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d135-top-two", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
DEFINITION_TOP_ONE = f.CalculationDefinitionV1(
    "D135", "D135-SMART-TOP-ONE-ASK-1", "K02_ALGEBRA",
    "sum(top one standing SMART ask size after positional replay)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "shares", "scalar_decimal",
    AUTHORITY,
)
PARAMETER_TOP_ONE = f.CalculationParameterSetV1(
    "mmt-d135-top-one", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d134-smart-four-field", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
SELECTION_TOP_ONE = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d135-smart-top-one", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)


def admit(raw, event_id, position, operation, side, size, seconds, sequence):
    ids = (("R187",) if operation == 317 else
           ("R185", "R188", "R190") if operation is None else tuple(
        raw_id for raw_id, _, _ in ROLES)
          )
    record = {"generation": {"id": GENERATION}, "event": {"id": event_id},
              "subject": {"id": SUBJECT}, "book": {}}
    if operation != 317:
        record["book"].update(position=position, side=side, size=size)
    if operation is not None:
        record["book"]["operation"] = operation
    stamp = T - timedelta(seconds=seconds)
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id("d135-" + event_id),
        delivery_artifact_ref=r.delivery_artifact_ref("d135-controlled"),
        source_provider=r.provider_id(PROVIDER), native_record=record,
        received_ts_utc=stamp, ingestion_sequence=sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(raw_id) for raw_id in ids),
        source_variant=VARIANT, subject_instrument=SUBJECT, native_units="mixed_book_roles",
        source_timestamp_raw=stamp.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    ))
    projected = []
    for mapping in MAPS:
        if mapping.raw_signal_catalogue_id.value not in ids:
            continue
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        item = next(v for v in page.items
                    if v.observation_occurrence_id.value == "d135-" + event_id)
        assert item.selection_identity.value_for("event.id") == event_id
        assert item.native_field_path == mapping.native_field_path
        projected.append(item)
    assert len(projected) == len(ids)
    return projected


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d135_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = []
    for sequence, (event_id, position, side, size) in enumerate((
        ("bid0", 0, 0, Decimal("5")), ("bid1", 1, 0, Decimal("3")),
        ("ask0", 0, 1, Decimal("2")), ("ask1", 1, 1, Decimal("4")),
    ), 1):
        projected.extend(admit(raw, event_id, position, 0, side, size,
                               6 - sequence, sequence))
    assert len(projected) == 16
    if refused:
        reset = admit(raw, "reset", None, 317, None, None, 1, 5)
        assert len(reset) == 1 and reset[0].raw_signal_catalogue_id.value == "R187"
        assert reset[0].native_value == 317
        projected.extend(reset)
    request = f.SmartDepthRequestV1(f.CalculationRequestV1(
        "D135", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            raw_id, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw_id, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, 2)
    top_one_request = f.SmartDepthRequestV1(f.CalculationRequestV1(
        "D135", SUBJECT, T, CUTOFF, DEFINITION_TOP_ONE.calculation_definition_version,
        f.VersionRefV1(PARAMETER_TOP_ONE.context_id, 1), SELECTION_TOP_ONE.ref,
        (SELECTION_TOP_ONE.ref,), tuple(f.RawInputBindingV1(
            raw_id, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw_id, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION_TOP_ONE, 1)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d135.sqlite")
    owner = f.create_smart_ask_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    top_one_path = str(tmp_path / "d135-top-one.sqlite")
    top_one_owner = f.create_smart_ask_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(top_one_path, True), utc_now=lambda: NOW,
    )
    top_one = top_one_owner.materialise(top_one_request)
    reader = f.create_smart_ask_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    top_one_reader = f.create_smart_ask_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(top_one_path),
    )
    query = dict(derived_signal_id="D135", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF,
                 limit=10)
    if refused:
        assert occurrence is None and reader.list_derived_history(**query) == ()
        assert top_one is None and top_one_reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.SmartDepthOccurrenceV1
    assert occurrence.result == Decimal("6")
    assert occurrence.standing_rows == (
        f.SmartSizeRowV1(0, 0, Decimal("5")),
        f.SmartSizeRowV1(0, 1, Decimal("3")),
        f.SmartSizeRowV1(1, 0, Decimal("2")),
        f.SmartSizeRowV1(1, 1, Decimal("4")),
    )
    assert occurrence.owner_object_id == "M02" and occurrence.owner_namespace.endswith(
        "/smart-depth/v1")
    assert occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.definition == DEFINITION and occurrence.parameter_set == PARAMETER
    assert occurrence.request == request and occurrence.projection_mappings == MAPS
    assert occurrence.unit_conventions == UNITS
    assert occurrence.units == "shares" and occurrence.result_shape == "scalar_decimal"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == len(projected) == 16
    for line in occurrence.raw_input_lineage:
        item = next(v for v in projected
                    if v.observation_occurrence_id.value == line.observation_occurrence_id
                    and v.raw_signal_catalogue_id.value == line.raw_signal_id)
        assert line.projection == item and line.canonical_value == item.native_value
        assert type(line.canonical_value) is (int if line.raw_signal_id in
                                               ("R185", "R187", "R188") else Decimal)
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
    assert type(top_one) is f.SmartDepthOccurrenceV1
    assert top_one.derived_occurrence_id != occurrence.derived_occurrence_id
    assert top_one.result == Decimal("2") and top_one.request == top_one_request
    assert top_one.definition == DEFINITION_TOP_ONE
    assert top_one.parameter_set == PARAMETER_TOP_ONE
    assert top_one.request.selection == SELECTION_TOP_ONE
    assert top_one.raw_input_lineage == occurrence.raw_input_lineage
    assert top_one.standing_rows == occurrence.standing_rows
    assert top_one.projection_mappings == MAPS and top_one.unit_conventions == UNITS
    assert top_one.implementation_brief_sha256 == BRIEF
    assert top_one_reader.get_derived_occurrence(top_one.derived_occurrence_id) == top_one
    assert top_one_reader.list_derived_history(**query) == (top_one,)
