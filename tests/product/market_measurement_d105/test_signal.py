"""D105 actual 365-prior-day comparable-IV rank and zero prior-range refusal."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "NVDA_30D_ATM_CONTROLLED"
PROVIDER, VARIANT = "foundation-controlled-iv-history", "daily_constant_maturity_iv_v1"
BRIEF = "b450ae7bc14068908d3a5cf8df8523ed74a275c818d120c8bdb108ef62b73211"
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
META = (
    ("series.id", ("series", "id")), ("underlying.id", ("underlying", "id")),
    ("tenor.days", ("tenor", "days")), ("measure.kind", ("measure", "kind")),
    ("model.convention", ("model", "convention")),
    ("period.close_utc", ("period", "close_utc")),
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r183-comparable-iv", 1, r.RawSignalCatalogueId("R183"), PROVIDER, VARIANT,
    ("iv", "close"), "annualised_decimal_volatility", META,
)
UNIT = f.UnitConventionVersionV1("mmt-comparable-iv", 1, "annualised_decimal_volatility",
                                 "annualised_decimal_volatility", Decimal(1), Decimal(0))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-comparable-iv-year", 1),
    T - timedelta(days=365), T + timedelta(seconds=1), T - timedelta(days=365),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d105-selection", 1,
    ("subject_instrument", "series.id", "tenor.days", "measure.kind", "model.convention"),
    timedelta(days=365), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
DEFINITION = f.CalculationDefinitionV1(
    "D105", "D105-PRIOR-YEAR-IV-RANK-1", "K04_STANDARDISE_RANK",
    "100*(current-min(prior365))/(max(prior365)-min(prior365))", ("R183",), (),
    "P_BASELINE", "iv_rank_points", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d105-controlled", 1, "P_BASELINE", SUBJECT, (SUBJECT,),
)
ANCHORS = (T, *(T - timedelta(days=k) for k in range(365, 0, -1)))


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D105", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R183", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), SUBJECT,
        ),),
    ), CONTEXT, ())


def prior_value(index, refused):
    if refused:
        return Decimal(".40")
    return Decimal(".20" if index < 100 else ".40" if index < 165 else ".60")


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d105_signal(tmp_path, refused):
    raw = r.create_owner()
    expected = {}
    for index, anchor in enumerate(ANCHORS):
        value = Decimal(".70") if index == 0 else prior_value(index - 1, refused)
        stamp = anchor.isoformat().replace("+00:00", "Z")
        native = {
            "series": {"id": SUBJECT}, "underlying": {"id": "NVDA"},
            "tenor": {"days": "30"}, "measure": {"kind": "atm_constant_maturity"},
            "model": {"convention": "controlled-comparable-iv/1"},
            "period": {"close_utc": stamp}, "iv": {"close": value},
        }
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d105-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d105-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=native,
            received_ts_utc=anchor, ingestion_sequence=index + 1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R183"),),
            source_variant=VARIANT, subject_instrument=SUBJECT,
            native_units="annualised_decimal_volatility",
            source_timestamp_raw=stamp, source_timezone_native="UTC",
        ))
        expected[anchor] = (value, stamp, f"d105-{index}")
    projected = {}
    cursor = None
    pages = 0
    while True:
        page = raw.reads.list_projected_raw_history(
            r.RawSignalCatalogueId("R183"), mappings=(MAPPING,),
            subject_instrument=SUBJECT, received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T, limit=100, cursor=cursor,
        )
        pages += 1
        for item in page.items:
            stamp = item.source_timestamp_raw
            anchor = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            value, expected_stamp, identity = expected[anchor]
            assert stamp == expected_stamp and item.native_value == value
            assert item.observation_occurrence_id.value == identity
            assert item.received_ts_utc == anchor
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("series.id", SUBJECT), ("underlying.id", "NVDA"),
                ("tenor.days", "30"), ("measure.kind", "atm_constant_maturity"),
                ("model.convention", "controlled-comparable-iv/1"),
                ("period.close_utc", stamp),
            ))
            assert anchor not in projected
            projected[anchor] = item
        cursor = page.next_cursor
        if cursor is None:
            break
        assert pages < 1000
    assert pages >= 4 and len(projected) == 366 and set(projected) == set(ANCHORS)
    assert len(ANCHORS[1:]) == 365 and T not in ANCHORS[1:]
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d105.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    own_request = request()
    result = owner.materialise(own_request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D105", subject_instrument=SUBJECT,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(125, 1)
    assert result.request == own_request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(f.RawInputLineageV1(
        "R183", projected[anchor].observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        projected[anchor], expected[anchor][0], anchor,
    ) for anchor in ANCHORS)
    assert result.predecessors == () and result.window_seconds == 31536000
    assert result.units == "iv_rank_points" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
