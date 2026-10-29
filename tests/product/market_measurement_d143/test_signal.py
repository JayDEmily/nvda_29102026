"""D143: complete direct two-venue standing book and missing marketMaker refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA"
PROVIDER, VARIANT = "foundation-controlled-direct-book", "direct_venue_v1"
GENERATION = "controlled-direct-generation/1"
BRIEF = "a6008036bb46d81996ac5bc9d9054db8544349d90477b806b0184def034fff9d"
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
    ("R192", "position", "book_position"), ("R193", "marketMaker", "venue_id"),
    ("R194", "operation", "book_operation"), ("R195", "side", "book_side"),
    ("R196", "price", "USD_per_share"), ("R197", "size", "shares"),
)
IDENTITY = (("generation.id", ("generation", "id")),
            ("event.id", ("event", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d143-" + rid.lower(), 1, r.RawSignalCatalogueId(rid), PROVIDER,
    VARIANT, ("book", field), unit, IDENTITY,
) for rid, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d143-" + rid.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for rid, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D143", "D143-DIRECT-VENUE-CONCENTRATION-1", "K02_ALGEBRA",
    "per-venue complete standing top-one bid+ask depth shares and sum squared shares",
    tuple(rid for rid, _, _ in ROLES), (), "P_BASIC", "concentration index",
    "venue_concentration", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d143-two-venues-top-one", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
SELECTION = f.BookEventSelectionV1(
    f.VersionRefV1("mmt-d143-direct-positional", 1), PROVIDER, VARIANT,
    GENERATION, T - timedelta(seconds=10), 100,
)
EVENTS = (
    ("ALPHA", 0, Decimal("99"), Decimal("2")),
    ("ALPHA", 1, Decimal("101"), Decimal("1")),
    ("BETA", 0, Decimal("99"), Decimal("0.5")),
    ("BETA", 1, Decimal("101"), Decimal("0.5")),
)


@pytest.mark.parametrize("missing_venue", (False, True), ids=("success", "refusal"))
def test_d143_signal(tmp_path, missing_venue):
    raw = r.create_owner()
    for i, (venue, side, price, size) in enumerate(EVENTS):
        omit = missing_venue and i == 3
        book = {"position": 0, "operation": 0, "side": side, "price": price, "size": size}
        if not omit:
            book["marketMaker"] = venue
        stamp = T - timedelta(seconds=4 - i)
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d143-book-{i}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d143-controlled"),
            source_provider=r.provider_id(PROVIDER),
            native_record={"generation": {"id": GENERATION}, "event": {"id": f"direct-{i}"},
                           "subject": {"id": SUBJECT}, "book": book},
            received_ts_utc=stamp, ingestion_sequence=i + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(rid) for rid, _, _ in ROLES
                                           if not (omit and rid == "R193")),
            source_variant=VARIANT, subject_instrument=SUBJECT, native_units="mixed_direct_roles",
            source_timestamp_raw=stamp.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        ))
    for role, mapping in enumerate(MAPS):
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None
        assert len(page.items) == (3 if missing_venue and role == 1 else 4)
        assert all(type(item.native_value) is (
            str if role == 1 else int if role in (0, 2, 3) else Decimal
        ) for item in page.items)
        if role == 5:
            assert {item.observation_occurrence_id.value for item in page.items} == {
                f"d143-book-{i}" for i in range(4)
            }
    request = f.DirectVenueRequestV1(f.CalculationRequestV1(
        "D143", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), SELECTION.ref, (SELECTION.ref,),
        tuple(f.RawInputBindingV1(
            rid, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (rid, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), SELECTION, ("ALPHA", "BETA"), 1)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d143.sqlite")
    owner = f.create_direct_venue_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    occurrence = owner.materialise(request)
    reader = f.create_direct_venue_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    query = dict(derived_signal_id="D143", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if missing_venue:
        assert occurrence is None and reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.DirectVenueOccurrenceV1
    assert occurrence.result == f.VenueConcentrationV1(
        ("ALPHA", "BETA"), (f.ExactRatioV1(3, 4), f.ExactRatioV1(1, 4)),
        f.ExactRatioV1(5, 8),
    )
    assert occurrence.request == request and occurrence.definition == DEFINITION
    assert occurrence.parameter_set == PARAMETER and occurrence.selection == SELECTION
    assert occurrence.unit_conventions == UNITS and occurrence.projection_mappings == MAPS
    assert occurrence.owner_object_id == "M02" and occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.owner_namespace == "neutral_market_measurement_truth/direct-venue/v1"
    assert occurrence.units == "concentration index"
    assert occurrence.result_shape == "venue_concentration"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == 24
    assert tuple((x.venue, x.side, x.position, x.size) for x in occurrence.standing_rows) == (
        ("ALPHA", 0, 0, Decimal(2)), ("ALPHA", 1, 0, Decimal(1)),
        ("BETA", 0, 0, Decimal("0.5")), ("BETA", 1, 0, Decimal("0.5")),
    )
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
