"""D063: one complete release-specific sample and one missing selected member."""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

D, BRIEF = "D063", "09d32004835d2cd8ac9b8aa3911a97f4b1f1f62b418564c9a0280ce65983185e"
FACTS = (
    (
        "syn-release-jul",
        "2026-07-15T12:30:00Z",
        "actual",
        "R286",
        "2.4",
        "2026-07-15T12:30:02Z",
        "a1",
    ),
    (
        "syn-release-jul",
        "2026-07-15T12:30:00Z",
        "consensus",
        "R285",
        "2.5",
        "2026-07-14T12:00:00Z",
        "c1",
    ),
    (
        "syn-release-aug",
        "2026-08-14T12:30:00Z",
        "actual",
        "R286",
        "2.5",
        "2026-08-14T12:30:02Z",
        "a1",
    ),
    (
        "syn-release-aug",
        "2026-08-14T12:30:00Z",
        "consensus",
        "R285",
        "2.5",
        "2026-08-13T12:00:00Z",
        "c1",
    ),
    (
        "syn-release-sep",
        "2026-09-15T12:30:00Z",
        "actual",
        "R286",
        "2.6",
        "2026-09-15T12:30:02Z",
        "a1",
    ),
    (
        "syn-release-sep",
        "2026-09-15T12:30:00Z",
        "consensus",
        "R285",
        "2.5",
        "2026-09-14T12:00:00Z",
        "c1",
    ),
    (
        "syn-release-oct",
        "2026-10-15T12:30:00Z",
        "actual",
        "R286",
        "2.7",
        "2026-10-15T12:30:02Z",
        "a1",
    ),
    (
        "syn-release-oct",
        "2026-10-15T12:30:00Z",
        "consensus",
        "R285",
        "2.5",
        "2026-10-14T12:00:00Z",
        "c1",
    ),
)
FAMILY = "US-CPI-HEADLINE-YOY-SYNTHETIC"


def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


T, CUTOFF, NOW = map(dt, ("2026-10-15T12:30:00Z", "2026-10-15T13:00:00Z", "2026-10-15T13:00:01Z"))
START = dt("2026-07-14T12:00:00Z")
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-release-history", 1), START, CUTOFF, START)
META = tuple(
    ("release." + key, ("release", key))
    for key in ("id", "family", "scheduled_utc", "kind", "known_utc", "revision")
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-release",
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-controlled-events",
        "release_snapshot_v1",
        ("release", kind),
        "synthetic_pct_yoy",
        META,
    )
    for rid, kind in (("R286", "actual"), ("R285", "consensus"))
)
UNIT = f.UnitConventionVersionV1(
    "mmt-release-units", 1, "synthetic_pct_yoy", "synthetic_pct_yoy", Decimal("1"), Decimal("0")
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d063-selection",
    1,
    ("subject_instrument", "release.id", "release.family", "release.kind"),
    timedelta(days=100),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-controlled-events",
    "release_snapshot_v1",
    "foundation-controlled-events/release_snapshot_v1",
    100,
    1000,
)
PARAM = f.CalculationParameterSetV1("mmt-d063-controlled", 1, "P_BASELINE", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    D,
    "D063-MACRO-SURPRISE-1",
    "K04_STANDARDISE_RANK",
    "(current_surprise-mean(prior_surprises))/sample_sd(prior_surprises)",
    ("R286", "R285"),
    (),
    "P_BASELINE",
    "z-score",
    "scalar_decimal",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
    ),
)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d063_signal(tmp_path, refused):
    raw = r.create_owner()
    selected = []
    for index, (release_id, scheduled, kind, rid, value, known, revision) in enumerate(FACTS):
        if refused and release_id == "syn-release-sep" and kind == "actual":
            continue
        event = dt(known if kind == "consensus" else scheduled)
        identity = "d063-raw-" + str(index)
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d063-controlled"),
                source_provider=r.provider_id("foundation-controlled-events"),
                native_record={
                    "release": {
                        "id": release_id,
                        "family": FAMILY,
                        "scheduled_utc": scheduled,
                        "kind": kind,
                        "known_utc": known,
                        "revision": revision,
                        kind: Decimal(value),
                    }
                },
                received_ts_utc=dt(known),
                ingestion_sequence=index + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-controlled-events/release_snapshot_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(r.RawSignalCatalogueId(rid),),
                source_variant="release_snapshot_v1",
                subject_instrument="NVDA",
                native_units="synthetic_pct_yoy",
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            )
        )
        selected.append(
            (index, identity, release_id, scheduled, kind, rid, value, known, revision, event)
        )
    projections = {}
    for mapping in MAPS:
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T,
            limit=100,
            cursor=None,
        )
        assert page.next_cursor is None
        projections.update({p.observation_occurrence_id.value: p for p in page.items})
    assert len(projections) == (7 if refused else 8)
    for _, identity, release_id, scheduled, kind, rid, value, known, revision, event in selected:
        item = projections[identity]
        assert item.native_value == Decimal(value) and item.received_ts_utc == dt(known)
        assert item.raw_signal_catalogue_id == r.RawSignalCatalogueId(rid)
        assert item.source_timestamp_raw == event.isoformat().replace("+00:00", "Z")
        assert item.selection_identity == r.RawSelectionIdentityV1(
            tuple(
                ("release." + key, val)
                for key, val in (
                    ("id", release_id),
                    ("family", FAMILY),
                    ("scheduled_utc", scheduled),
                    ("kind", kind),
                    ("known_utc", known),
                    ("revision", revision),
                )
            )
        )
    if refused:
        assert "d063-raw-4" not in projections
        assert (
            "d063-raw-5" in projections
            and "d063-raw-6" in projections
            and "d063-raw-7" in projections
        )
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "m02.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            D,
            "NVDA",
            T,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAM.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    m.raw_signal_catalogue_id.value,
                    f.VersionRefV1(m.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    "NVDA",
                )
                for m in MAPS
            ),
        ),
        CONTEXT,
        (),
    )
    result = owner.materialise(request)
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(
        derived_signal_id=D,
        subject_instrument="NVDA",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is Decimal and result.result == Decimal("2")
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAM and result.input_selection_policy == POLICY
    assert result.unit_conventions == (UNIT,) and result.projection_mappings == MAPS
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            rid,
            identity,
            f.VersionRefV1(MAPS[0 if kind == "actual" else 1].mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            projections[identity],
            Decimal(value),
            event,
        )
        for _, identity, _, _, kind, rid, value, _, _, event in selected
    )
    assert result.predecessors == () and result.window_seconds == int(
        (T - dt("2026-07-15T12:30:00Z")).total_seconds()
    )
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == D
    assert result.units == "z-score" and result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (
        owner.reads.get_derived_occurrence(result.derived_occurrence_id)
        == reader.get_derived_occurrence(result.derived_occurrence_id)
        == result
    )
    assert reader.list_derived_history(**args) == (result,)
