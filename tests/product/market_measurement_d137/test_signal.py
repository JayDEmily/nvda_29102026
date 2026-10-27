"""D137: exact coherent public top-book microprice and zero-denominator refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT, PROVIDER, VARIANT = "NVDA", "foundation-controlled-top-book", "coherent_quote_v1"
BRIEF = "58ecb7858c5ecf1dd5d7c840f8f03a76ae259bcd9fdf93c6a58d3fb4f907c302"
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
    ("R033", "bid_size", "shares"), ("R034", "bid_price", "USD_per_share"),
    ("R035", "ask_price", "USD_per_share"), ("R036", "ask_size", "shares"),
)
IDENTITY = (("quote.id", ("quote", "id")), ("subject.id", ("subject", "id")))
MAPS = tuple(r.RawSignalProjectionMappingV1(
    "mmt-d137-" + raw.lower(), 1, r.RawSignalCatalogueId(raw), PROVIDER,
    VARIANT, ("quote", field), unit, IDENTITY,
) for raw, field, unit in ROLES)
UNITS = tuple(f.UnitConventionVersionV1(
    "mmt-d137-" + raw.lower() + "-unit", 1, unit, unit, Decimal(1), Decimal(0),
) for raw, _, unit in ROLES)
DEFINITION = f.CalculationDefinitionV1(
    "D137", "D137-COHERENT-TOP-BOOK-MICROPRICE-1", "K02_ALGEBRA",
    "(ask_price*bid_size+bid_price*ask_size)/(bid_size+ask_size)",
    tuple(raw for raw, _, _ in ROLES), (), "P_BASIC", "USD_per_share", "exact_ratio",
    AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d137-nvda-top-book", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d137-coherent-quote", 1, ("subject_instrument", "quote.id", "subject.id"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (SUBJECT,),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-top-book-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D137", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), tuple(f.RawInputBindingV1(
            raw, f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), SUBJECT,
        ) for (raw, _, _), mapping, unit in zip(ROLES, MAPS, UNITS, strict=True)),
    ), CONTEXT, ())


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d137_signal(tmp_path, refused):
    raw = r.create_owner()
    amounts = (Decimal(0), Decimal("99"), Decimal("101"), Decimal(0)) if refused else (
        Decimal("3"), Decimal("99"), Decimal("101"), Decimal("1"),
    )
    fields = {field: amount for (_, field, _), amount in zip(ROLES, amounts, strict=True)}
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id("d137-coherent-quote"),
        delivery_artifact_ref=r.delivery_artifact_ref("d137-controlled"),
        source_provider=r.provider_id(PROVIDER),
        native_record={"quote": {"id": "controlled-quote/1", **fields},
                       "subject": {"id": SUBJECT}},
        received_ts_utc=T, ingestion_sequence=1,
        ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=tuple(mapping.raw_signal_catalogue_id for mapping in MAPS),
        source_variant=VARIANT, subject_instrument=SUBJECT, native_units="mixed_quote_roles",
        source_timestamp_raw="2026-10-20T12:40:00Z", source_timezone_native="UTC",
    ))
    projected = []
    for role, mapping in enumerate(MAPS):
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id, mappings=(mapping,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.native_value == amounts[role] and type(item.native_value) is Decimal
        assert item.observation_occurrence_id.value == "d137-coherent-quote"
        assert item.selection_identity == r.RawSelectionIdentityV1((
            ("quote.id", "controlled-quote/1"), ("subject.id", SUBJECT),
        ))
        projected.append(item)
    assert len(projected) == 4
    if refused:
        assert projected[0].native_value == projected[3].native_value == 0
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d137.sqlite")
    owner = f.create_microprice_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    occurrence = owner.materialise(own_request)
    reader = f.create_microprice_reader(
        admission=admission, storage=f.SQLiteReadStorageV1(path),
    )
    query = dict(derived_signal_id="D137", subject_instrument=SUBJECT,
                 effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF,
                 limit=10)
    if refused:
        assert occurrence is None and reader.list_derived_history(**query) == ()
        return
    assert type(occurrence) is f.WindowMeasurementOccurrenceV1
    assert occurrence.result == f.ExactRatioV1(201, 2)
    assert occurrence.request == own_request and occurrence.definition == DEFINITION
    assert occurrence.parameter_set == PARAMETER and occurrence.input_selection_policy == POLICY
    assert occurrence.unit_conventions == UNITS and occurrence.projection_mappings == MAPS
    assert occurrence.owner_object_id == "M02"
    assert occurrence.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert occurrence.implementation_brief_sha256 == BRIEF
    assert occurrence.predecessors == () and occurrence.window_seconds == 0
    assert occurrence.units == "USD_per_share" and occurrence.result_shape == "exact_ratio"
    assert (occurrence.effective_as_of_utc, occurrence.knowledge_cutoff_utc,
            occurrence.calculated_at_utc) == (T, CUTOFF, NOW)
    assert len(occurrence.raw_input_lineage) == 4
    for role, line in enumerate(occurrence.raw_input_lineage):
        mapping, unit, item = MAPS[role], UNITS[role], projected[role]
        assert line == f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value, item.observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1(unit.context_id, 1),
            item, amounts[role], T,
        )
    assert reader.get_derived_occurrence(occurrence.derived_occurrence_id) == occurrence
    assert reader.list_derived_history(**query) == (occurrence,)
