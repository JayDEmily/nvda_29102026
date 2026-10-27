"""D139: actual typed R001 collector receipt and positional insert rate."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-smart-book", "receipt_rate_v1"
GENERATION = "controlled-smart-rate-generation/1"
BRIEF = "77e84fa49327cebe561167b7086b2db3acc71ae1bdeee3054656885c271a2f89"
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
    ("R001", ("time", "receipt"), "UTC_datetime"),
    ("R185", ("book", "position"), "book_position"),
    ("R187", ("book", "operation"), "book_operation"),
    ("R188", ("book", "side"), "book_side"),
    ("R190", ("book", "size"), "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d139-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER,
    VARIANT, path, unit, IDENTITY,
) for raw, path, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d139-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D139", "D139-RECEIPT-CLOCK-INSERT-RATE-1", "K08_RULE_BUCKET_POLICY",
    "count and inserted standing size of bid positions1-2 in four-second R001 receipt bucket",
    tuple(raw for raw, _, _ in ROLES), (), "P_RULE", "events or size/time",
    "book_rate_pair", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d139-bid-positions1-2-4s", 1, "P_RULE", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d139-receipt-positional", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)


def admit(raw, i, side, pos, size, received, event, missing_op=False):
    record = {"generation": {"id": GENERATION}, "event": {"id": f"rate-{i}"},
              "subject": {"id": SUBJECT}, "time": {"receipt": received},
              "book": {"position": pos, "side": side, "size": Decimal(size)}}
    if not missing_op:
        record["book"]["operation"] = 0
    ids = tuple(raw_id for raw_id, _, _ in ROLES if not (missing_op and raw_id == "R187"))
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(f"d139-book-{i}"),
        delivery_artifact_ref=r.delivery_artifact_ref("d139-controlled"),
        source_provider=r.provider_id(PROVIDER), native_record=record,
        received_ts_utc=received, ingestion_sequence=i + 1,
        ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(x) for x in ids),
        source_variant=VARIANT, subject_instrument=SUBJECT, native_units="mixed_book_roles",
        source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    ))


@pytest.mark.parametrize("missing_op", (False, True), ids=("success", "refusal"))
def test_d139_signal(tmp_path, missing_op):
    raw = r.create_owner()
    events = (
        (0, 0, 2, T - timedelta(seconds=6), T - timedelta(seconds=7)),
        (1, 0, 1, T - timedelta(seconds=5), T - timedelta(seconds=8)),
        (0, 1, 3, T - timedelta(seconds=3), T - timedelta(seconds=9)),
        (0, 2, 5, T - timedelta(seconds=1), T - timedelta(seconds=8)),
    )
    for i, (side, pos, size, receipt, event) in enumerate(events):
        admit(raw, i, side, pos, size, receipt, event, missing_op and i == 3)
    for role, mapping in enumerate(MAPS):
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None
        assert len(page.items) == (3 if missing_op and role == 2 else 4)
        assert all(type(item.native_value) is (
            datetime if role == 0 else int if role < 4 else Decimal
        ) for item in page.items)
        for item in page.items:
            i = int(item.observation_occurrence_id.value.rsplit("-", 1)[1])
            assert item.received_ts_utc == events[i][3]
            assert item.source_timestamp_raw == events[i][4].isoformat().replace("+00:00", "Z")
            if role == 0:
                assert item.native_value == events[i][3]
                assert item.native_value != events[i][4]
    request = f.BookRateRequestV1(f.CalculationRequestV1(
        "D139", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            rid, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (rid, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, 4, 0, (1, 2))
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d139.sqlite")
    owner = f.create_book_insert_rate_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    reader = f.create_book_insert_rate_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    query = dict(derived_signal_id="D139", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if missing_op:
        assert occurrence is None and reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.BookRateOccurrenceV1
    assert occurrence.result == f.BookRatePairV1(f.ExactRatioV1(1, 2), f.ExactRatioV1(2, 1))
    assert occurrence.request == request and occurrence.definition == DEFINITION
    assert occurrence.parameter_set == PARAMETER and occurrence.selection == SELECTION
    assert occurrence.unit_conventions == UNITS and occurrence.projection_mappings == MAPS
    assert occurrence.owner_object_id == "M02" and occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.owner_namespace == "neutral_market_measurement_truth/book-rate/v1"
    assert occurrence.units == "events or size/time" and occurrence.result_shape == "book_rate_pair"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == 20
    assert occurrence.selected_event_ids == ("d139-book-2", "d139-book-3")
    assert tuple((x.side, x.position, x.size) for x in occurrence.standing_rows) == (
        (0, 0, Decimal(2)), (0, 1, Decimal(3)), (0, 2, Decimal(5)),
        (1, 0, Decimal(1)),
    )
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
