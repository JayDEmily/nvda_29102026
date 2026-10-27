"""D136 actual D134/D135 public predecessors and incompatible ask depth."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
PROVIDER, VARIANT = "foundation-controlled-smart-book", "positional_four_field_v1"
GENERATION = "controlled-smart-four-field-generation/1"
ASK_BRIEF = "bbd3cbf1e050bfbf9d80bd11eb828df025a0b8cadda93d178d0b028f307dd514"
BID_BRIEF = "628cddf853ab1c074a8b89264533714d7211a83618704742b2435b02121ac336"
BRIEF = "e4c8ed923a5f70ee6ce9e76f17bffc88bd6c92b9be975f033c46f2fed3922420"
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
ASK_DEFINITION = f.CalculationDefinitionV1(
    "D135", "D135-SMART-TOP-TWO-ASK-1", "K02_ALGEBRA",
    "sum(top two standing SMART ask sizes after positional replay)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "shares", "scalar_decimal",
    AUTHORITY,
)
ASK_PARAMETER = f.CalculationParameterSetV1(
    "mmt-d135-top-two", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d134-smart-four-field", 1), PROVIDER, VARIANT,
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



BID_DEFINITION = f.CalculationDefinitionV1(
    "D134", "D134-SMART-TOP-TWO-BID-1", "K02_ALGEBRA",
    "sum(top two standing SMART bid sizes after positional replay)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "shares", "scalar_decimal",
    AUTHORITY,
)
BID_PARAMETER = f.CalculationParameterSetV1(
    "mmt-d134-top-two", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
DEFINITION = f.CalculationDefinitionV1(
    "D136", "D136-SMART-DEPTH-IMBALANCE-1", "K02_ALGEBRA",
    "(bid_depth-ask_depth)/(bid_depth+ask_depth)", (), ("D134", "D135"),
    "P_BASIC", "-1_to_1", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d136-same-book-top-levels", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)


def parent_request(signal, definition, parameter):
    return f.SmartDepthRequestV1(f.CalculationRequestV1(
        signal, SUBJECT, T, CUTOFF, definition.calculation_definition_version,
        f.VersionRefV1(parameter.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            raw_id, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw_id, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, 2)


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d136_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = []
    for sequence, (event_id, position, side, size) in enumerate((
        ("bid0", 0, 0, Decimal("5")), ("bid1", 1, 0, Decimal("3")),
        ("ask0", 0, 1, Decimal("2")), ("ask1", 1, 1, Decimal("4")),
    ), 1):
        projected.extend(admit(raw, event_id, position, 0, side, size,
                               6 - sequence, sequence))
    assert len(projected) == 16
    bid_path, ask_path = str(tmp_path / "d134.sqlite"), str(tmp_path / "d135.sqlite")
    bid_owner = f.create_smart_depth_owner(
        admission=f.OwnerAdmissionV1("M02", BID_BRIEF), raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(bid_path, True), utc_now=lambda: NOW,
    )
    ask_owner = f.create_smart_ask_owner(
        admission=f.OwnerAdmissionV1("M02", ASK_BRIEF), raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(ask_path, True), utc_now=lambda: NOW,
    )
    bid = bid_owner.materialise(parent_request("D134", BID_DEFINITION, BID_PARAMETER))
    ask = ask_owner.materialise(parent_request("D135", ASK_DEFINITION, ASK_PARAMETER))
    assert type(bid) is f.SmartDepthOccurrenceV1 and bid.result == Decimal("8")
    assert type(ask) is f.SmartDepthOccurrenceV1 and ask.result == Decimal("6")
    assert bid.raw_input_lineage == ask.raw_input_lineage
    assert bid.request.depth_levels == ask.request.depth_levels == 2
    bid_reader = f.create_smart_depth_reader(
        admission=f.OwnerAdmissionV1("M02", BID_BRIEF),
        storage=f.SQLiteReadStorageV1(bid_path),
    )
    ask_reader = f.create_smart_ask_reader(
        admission=f.OwnerAdmissionV1("M02", ASK_BRIEF),
        storage=f.SQLiteReadStorageV1(ask_path),
    )
    assert bid_reader.get_derived_occurrence(bid.derived_occurrence_id) == bid
    assert ask_reader.get_derived_occurrence(ask.derived_occurrence_id) == ask
    levels = (2, 3) if refused else (2, 2)
    request = f.SmartImbalanceRequestV1(f.CalculationRequestV1(
        "D136", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1("mmt-d136-same-book-selection", 1),
        (f.VersionRefV1("mmt-d136-same-book-selection", 1),), (),
    ), (bid.derived_occurrence_id, ask.derived_occurrence_id), levels)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d136.sqlite")
    owner = f.create_smart_imbalance_owner(
        admission=admission, bid_reader=bid_reader, ask_reader=ask_reader,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    reader = f.create_smart_imbalance_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    query = dict(derived_signal_id="D136", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF,
                 limit=10)
    if refused:
        assert request.requested_depth_levels == (2, 3)
        assert bid.request.depth_levels == 2 and ask.request.depth_levels == 2
        assert occurrence is None and reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.SmartImbalanceOccurrenceV1
    assert occurrence.result == f.ExactRatioV1(1, 7)
    assert occurrence.predecessors == (bid, ask)
    assert occurrence.request == request
    assert occurrence.definition == DEFINITION and occurrence.parameter_set == PARAMETER
    assert occurrence.owner_object_id == "M02"
    assert occurrence.owner_namespace.endswith("/smart-imbalance/v1")
    assert occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.units == "-1_to_1" and occurrence.result_shape == "exact_ratio"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
