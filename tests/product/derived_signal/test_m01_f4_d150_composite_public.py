"""F4 D150: controlled M00-to-M01 end-to-end composite with six exact D edges.

The numeric inputs are controlled projections, not real-provider source claims.
Each K07 composite has its *own* named immutable score schema.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 12, 4, tzinfo=UTC)
HISTORICAL = (*("R270", "R271", "R272", "R273", "R274", "R275", "R276", "R245"),)
GROWTH = ("R267", "R268", "R269", "R264", "R265", "R266")
INFLATION = ("R260", "R261", "R262", "R263", "R255")
POLICY = ("R256", "R258", "R259", "R247", "R249", "R252")
VOLATILITY = ("R236", "R237", "R238", "R239", "R240")
ALL = tuple(
    dict.fromkeys((*HISTORICAL, *GROWTH, *INFLATION, *POLICY, *VOLATILITY, "R257", "R285", "R286"))
)


def _score_feature(did: str, component: str | None = None) -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(
        did,
        "component",
        () if component is None else (component,),
        "identity",
        None,
        1,
        Decimal(1),
        None,
        None,
        (),
    )


def _public(
    *, absent: str | None = None, future: str | None = None, wrong_subject: str | None = None
):
    m00 = raw.create_owner()
    data: list[tuple[str, str, Decimal, datetime]] = []
    at = NOW - timedelta(seconds=3)
    # Eight matched daily change/return series for international and dollar inputs.
    for rid in HISTORICAL:
        data.extend(
            (
                (rid, f"{rid}-prior", Decimal(100), at - timedelta(days=1)),
                (rid, f"{rid}-current", Decimal(110), at),
            )
        )
    # Two distinct level factors with shared release-surprise definition.
    data.extend(
        (rid, f"{rid}-current", Decimal(index), at) for index, rid in enumerate(GROWTH, start=1)
    )
    data.extend(
        (rid, f"{rid}-current", Decimal(index), at) for index, rid in enumerate(INFLATION, start=1)
    )
    # D148 includes two basis-point rate changes, while D149 reuses R256.
    policy_values = (
        Decimal("0.025"),
        Decimal(2),
        Decimal(3),
        Decimal("0.04"),
        Decimal("0.0525"),
        Decimal("0.027"),
    )
    data.extend(
        (rid, f"{rid}-current", value, at) for rid, value in zip(POLICY, policy_values, strict=True)
    )
    data.extend(
        (
            ("R249", "R249-prior", Decimal("0.0500"), at - timedelta(days=1)),
            ("R252", "R252-prior", Decimal("0.0250"), at - timedelta(days=1)),
            ("R257", "R257-current", Decimal("0.03"), at),
        )
    )
    for rid, latest, prior in (
        ("R236", Decimal(21), Decimal(20)),
        ("R237", Decimal(110), Decimal(100)),
        ("R238", Decimal(18), None),
        ("R239", Decimal(19), None),
        ("R240", Decimal(23), None),
    ):
        if prior is not None:
            data.append((rid, f"{rid}-prior", prior, at - timedelta(seconds=300)))
        data.append((rid, f"{rid}-current", latest, at))
    for tag, age, actual, consensus in (
        ("prior1", 90, 110, 100),
        ("prior2", 60, 120, 100),
        ("prior3", 30, 140, 100),
        ("current", 0, 150, 100),
    ):
        date = at - timedelta(days=age)
        data.extend(
            (
                ("R286", f"{tag}-R286", Decimal(actual), date),
                ("R285", f"{tag}-R285", Decimal(consensus), date),
            )
        )

    for seq, (rid, tag, value, stamp) in enumerate(data, start=1):
        if tag == absent:
            continue
        # Release-history actual/consensus values share one M00 native event ID,
        # required for D063's exact same-occurrence join.
        event = tag.rsplit("-", 1)[0] if rid in {"R286", "R285"} else tag
        oid = f"f4-d150-{event}"
        # Combined multi-R release projections must be admitted only once.
        if rid == "R285":
            continue
        catalogue = ("R286", "R285") if rid == "R286" else (rid,)
        native = {"R286": value, "R285": Decimal(100)} if rid == "R286" else {rid: value}
        if rid == "R286" and absent == f"{event}-R285":
            del native["R285"]
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref(oid),
                source_provider=raw.provider_id("controlled-f4-d150"),
                native_record={"metric": native, "identity": {"release_family": "US-CPI"}},
                received_ts_utc=NOW + timedelta(seconds=2) if tag == future else stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("f4:d150"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in catalogue),
                source_variant="metric",
                subject_instrument="AMD" if tag == wrong_subject else "NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )

    schema = {
        "D150": ("D070", "D146", "D147", "D148", "D149", "D048"),
        "D070": ("D066", "D067", "D068", "D069", "D049", "D050", "D051"),
        "D146": (*GROWTH, "D063"),
        "D147": (*INFLATION, "D063"),
        "D148": (*POLICY, "D042", "D044", "D045"),
        "D149": ("R257", "R256", "D047", "D061"),
        "D061": ("D052", "D053", "D057", "D058", "D059", "D060"),
    }
    parameter_sets = [
        api.CalculationParameterSetV1(
            f"f4-d150-score-{did}",
            1,
            "P_SCORE",
            (("intercept", Decimal(0)),),
            tuple(
                _score_feature(
                    x,
                    "percent_change"
                    if x in {"D052", "D053"}
                    else "point_difference"
                    if x in {"D057", "D058", "D059"}
                    else None,
                )
                for x in members
            ),
        )
        for did, members in schema.items()
    ]
    parameter_sets.extend(
        (
            api.CalculationParameterSetV1("f4-d150-window", 1, "P_WINDOW", (("anchor_days", 1),)),
            api.CalculationParameterSetV1(
                "f4-d150-vol-window", 1, "P_WINDOW", (("anchor_seconds", 300),)
            ),
            api.CalculationParameterSetV1("f4-d150-basic", 1, "P_BASIC", (("version", 1),)),
            api.CalculationParameterSetV1(
                "f4-d150-baseline", 1, "P_BASELINE", (("history_count", 2), ("minimum_sample", 2))
            ),
        )
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"f4-d150-map-{rid}",
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-f4-d150",
                "metric",
                ("metric", rid),
                "canonical",
                (
                    (("release_family", ("identity", "release_family")),)
                    if rid in ("R285", "R286")
                    else ()
                ),
            )
            for rid in ALL
        ),
        parameter_sets=tuple(parameter_sets),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "f4-d150-policy",
                1,
                ("subject_instrument",),
                timedelta(days=125),
                timedelta(days=125),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "f4-d150-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    profiles = (
        api.ParameterProfileRefV1("P_SCORE", "f4-d150-score-D150", 1),
        api.ParameterProfileRefV1("P_WINDOW", "f4-d150-window", 1),
        api.ParameterProfileRefV1("P_BASIC", "f4-d150-basic", 1),
        api.ParameterProfileRefV1("P_BASELINE", "f4-d150-baseline", 1),
    )
    override = tuple(
        (did, api.ParameterProfileRefV1("P_SCORE", f"f4-d150-score-{did}", 1))
        for did in schema
        if did != "D150"
    ) + tuple(
        (did, api.ParameterProfileRefV1("P_WINDOW", "f4-d150-vol-window", 1))
        for did in ("D052", "D053")
    )
    bindings = tuple(
        api.RawInputBindingV1(
            rid,
            api.VersionRefV1(f"f4-d150-map-{rid}", 1),
            api.VersionRefV1("f4-d150-unit", 1),
            "NVDA",
            raw.RawSelectionIdentityV1((("release_family", "US-CPI"),))
            if rid in ("R285", "R286")
            else None,
        )
        for rid in ALL
    )
    request = api.CalculationRequestV1(
        "D150",
        "NVDA",
        NOW,
        NOW,
        "f4-d150-definition",
        "f4-d150-score-D150",
        1,
        "f4-d150-policy",
        1,
        (),
        parameter_profile_refs=profiles,
        predecessor_parameter_profile_refs=override,
        raw_input_bindings=bindings,
    )
    return owner, request


def test_d150_exact_six_predecessor_public_composition_and_lineage():
    owner, req = _public()
    result = owner.materialise(req)
    assert result is not None
    parents = {
        p.derived_signal_id: p
        for p in (
            owner.reads.get_derived_occurrence(pid) for pid in result.predecessor_occurrence_ids
        )
        if p is not None
    }
    assert set(parents) == {"D070", "D146", "D147", "D148", "D149", "D048"}
    assert result.result == sum((p.result for p in parents.values()), Decimal(0))
    # Independent numerical oracle: D070 four daily log returns and three FX
    # percentage changes; D146/147 the same release-specific surprise z-score;
    # D148 policy/rate composition; D149 funding/volatility; D048 dollar change.
    surprise_z = Decimal(20) / Decimal(200).sqrt()
    expected = (
        4 * (Decimal(110) / Decimal(100)).ln()
        + Decimal(30)
        + Decimal(21)
        + surprise_z
        + Decimal(15)
        + surprise_z
        + Decimal("51.3945")
        + Decimal("0.03")
        + Decimal("0.025")
        + Decimal(50)
        + Decimal(10)
        + Decimal(110) / Decimal(21)
        + Decimal(10)
    )
    assert abs(result.result - expected) < Decimal("0.000000000000000000000001")
    assert len(result.raw_input_lineage) == 51
    for did, occurrence in parents.items():
        assert (
            api.VersionRefV1(f"f4-d150-score-{did}", 1) in occurrence.parameter_context_refs
            if did != "D048"
            else occurrence is not None
        )
    assert {x.raw_signal_id for x in result.raw_input_lineage} == set(ALL)
    assert owner.materialise(req) == result


def test_d150_refuses_missing_international_member():
    owner, req = _public(absent="R270-current")
    assert owner.materialise(req) is None


def test_d150_refuses_future_growth_member():
    owner, req = _public(future="R267-current")
    assert owner.materialise(req) is None


def test_d150_refuses_missing_child_score_profile():
    owner, req = _public()
    altered = replace(
        req,
        predecessor_parameter_profile_refs=tuple(
            pair for pair in req.predecessor_parameter_profile_refs if pair[0] != "D070"
        ),
    )
    assert owner.materialise(altered) is None


def test_d150_refuses_missing_release_consensus():
    owner, req = _public(absent="current-R285")
    assert owner.materialise(req) is None


def test_d150_refuses_wrong_subject_policy_input():
    owner, req = _public(wrong_subject="R249-current")
    assert owner.materialise(req) is None


def test_d150_refuses_mapping_version_incompatibility():
    owner, req = _public()
    bindings = tuple(
        replace(binding, projection_mapping_ref=api.VersionRefV1("f4-d150-map-R245", 2))
        if binding.raw_signal_id == "R245"
        else binding
        for binding in req.raw_input_bindings
    )
    assert owner.materialise(replace(req, raw_input_bindings=bindings)) is None


def test_d150_refuses_knowledge_cutoff_before_current_sources():
    owner, req = _public()
    assert owner.materialise(replace(req, knowledge_cutoff_utc=NOW - timedelta(seconds=5))) is None


@pytest.mark.parametrize(
    "raw_id",
    (
        "R270-current",  # D070 international score
        "R267-current",  # D146 growth score
        "R260-current",  # D147 inflation score
        "R249-current",  # D148 policy score
        "R257-current",  # D149 funding score
        "R245-current",  # D048 dollar change
    ),
)
def test_d150_refuses_missing_source_of_each_declared_predecessor(raw_id: str):
    owner, req = _public(absent=raw_id)
    assert owner.materialise(req) is None
