"""D082: genuine aligned R151 closes, signed Pearson return matrix and missing row."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
ANCHORS = tuple(T - timedelta(minutes=k) for k in (3, 2, 1, 0))
MEMBERS = ("NVDA", "SPY", "QQQ")
CLOSES = (("1", "2", "4", "12"), ("1", "2", "6", "12"), ("1", "3", "9", "18"))
PROVIDER, VARIANT = "foundation-controlled-correlation", "minute_close_v1"
BRIEF = "f2b03173b89ac336728346dbacb625ba4e7bb23e3ca23a690a4ece412f84143e"
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
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r151-correlation", 1, r.RawSignalCatalogueId("R151"), PROVIDER, VARIANT,
    ("bar", "close"), "price",
    (
        ("instrument.id", ("instrument", "id")),
        ("bar.end_utc", ("bar", "end_utc")),
        ("bar.kind", ("bar", "kind")),
        ("adjustment.basis", ("adjustment", "basis")),
    ),
)
UNIT = f.UnitConventionVersionV1(
    "mmt-correlation-price", 1, "price", "price", Decimal("1"), Decimal("0")
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-correlation-window", 1), ANCHORS[0], T + timedelta(minutes=1),
    ANCHORS[0],
)
DEFINITION = f.CalculationDefinitionV1(
    "D082", "D082-ALIGNED-RETURN-CORRELATION-1", "K06_REGRESSION_DEPENDENCE",
    "Pearson correlation of three aligned log-return vectors", ("R151",), (),
    "P_REGRESSION", "correlation", "correlation_matrix", AUTHORITY,
)
PARAM = f.CalculationParameterSetV1(
    "mmt-d082-controlled", 1, "P_REGRESSION", "US_CORRELATION_BASKET", MEMBERS
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d082-selection", 1,
    ("subject_instrument", "instrument.id", "bar.end_utc"), timedelta(seconds=180),
    timedelta(0), ("true_instant",), MEMBERS, PROVIDER, VARIANT,
    PROVIDER + "/" + VARIANT, 100, 1000,
)


def _utc(value):
    return value.isoformat().replace("+00:00", "Z")


def _request():
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D082", "US_CORRELATION_BASKET", T, CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAM.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    "R151", f.VersionRefV1(MAPPING.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1), member,
                ) for member in MEMBERS
            ),
        ), CONTEXT, (),
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d082_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = {}
    for member_index, member in enumerate(MEMBERS):
        for anchor_index, anchor in enumerate(ANCHORS):
            if refused and (member, anchor_index) == ("SPY", 2):
                continue
            close = Decimal(CLOSES[member_index][anchor_index])
            native = {
                "bar": {"close": close, "end_utc": _utc(anchor),
                        "kind": "controlled_minute_close"},
                "instrument": {"id": member},
                "adjustment": {"basis": "controlled_unadjusted/1"},
            }
            identity = f"d082-{member.lower()}-{anchor_index}"
            raw.commands.admit_raw_observation_occurrence(
                r.RawObservationOccurrenceV1(
                    concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=r.observation_occurrence_id(identity),
                    delivery_artifact_ref=r.delivery_artifact_ref("d082-controlled"),
                    source_provider=r.provider_id(PROVIDER), native_record=native,
                    received_ts_utc=anchor,
                    ingestion_sequence=member_index * 4 + anchor_index + 1,
                    ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                    source_temporal_kind="true_instant",
                    raw_signal_catalogue_ids=(MAPPING.raw_signal_catalogue_id,),
                    source_variant=VARIANT, subject_instrument=member,
                    native_units="price", source_timestamp_raw=_utc(anchor),
                    source_timezone_native="UTC",
                )
            )
            page = raw.reads.list_projected_raw_history(
                MAPPING.raw_signal_catalogue_id, mappings=(MAPPING,),
                subject_instrument=member, received_at_or_before_utc=CUTOFF,
                event_at_or_before_utc=anchor, limit=100, cursor=None,
            )
            assert page.next_cursor is None
            item = next(x for x in page.items if x.observation_occurrence_id.value == identity)
            assert item.native_value == close
            assert item.received_ts_utc == anchor and item.source_timestamp_raw == _utc(anchor)
            assert item.selection_identity == r.RawSelectionIdentityV1((
                ("instrument.id", member), ("bar.end_utc", _utc(anchor)),
                ("bar.kind", "controlled_minute_close"),
                ("adjustment.basis", "controlled_unadjusted/1"),
            ))
            projected[(member, anchor_index)] = item
    assert len(projected) == (11 if refused else 12)
    assert all((member, 0) in projected and (member, 3) in projected for member in MEMBERS)
    if refused:
        assert ("SPY", 2) not in projected
        assert all(
            (member, i) in projected for member in MEMBERS for i in range(4)
            if (member, i) != ("SPY", 2)
        )
    request = _request()
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d082.sqlite")
    owner = f.create_window_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id="D082", subject_instrument="US_CORRELATION_BASKET",
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.CorrelationMatrixV1
    assert result.result.members == MEMBERS
    assert result.result.rows == (
        (Decimal("1"), Decimal("-0.5"), Decimal("-1")),
        (Decimal("-0.5"), Decimal("1"), Decimal("0.5")),
        (Decimal("-1"), Decimal("0.5"), Decimal("1")),
    )
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.implementation_brief_sha256 == BRIEF
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            "R151", projected[(member, i)].observation_occurrence_id.value,
            f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
            projected[(member, i)], Decimal(CLOSES[j][i]), ANCHORS[i],
        ) for j, member in enumerate(MEMBERS) for i in range(4)
    )
    assert result.predecessors == () and result.window_seconds == 180
    assert result.units == "correlation" and result.result_shape == "correlation_matrix"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
