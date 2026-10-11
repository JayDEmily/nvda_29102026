"""Proof-first: D041 and predecessor D040 require independently versioned P_SCORE truth.

The data enter through admitted M00 observations; the request cannot implicitly
use D041's scoring schema to evaluate its D040 predecessor (brief §5 K07,
§§8/13). This is a new reconstruction proof, not the missing original commit.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
END = NOW - timedelta(seconds=2)
RISK_STAMPS = tuple(NOW - timedelta(seconds=1805 - 900 * i) for i in range(3))


def _public(*, omitted: str | None = None, child_version: int = 1):
    m00 = raw.create_owner()
    records = (
        ("R143", "close-last", Decimal(120), END),
        ("R143", "close-1m", Decimal(110), END - timedelta(minutes=1)),
        ("R143", "close-5m", Decimal(100), END - timedelta(minutes=5)),
        ("R143", "close-30m", Decimal(80), END - timedelta(minutes=30)),
        ("R137", "vwap-last", Decimal(120), END),
        ("R137", "vwap-5m", Decimal(100), END - timedelta(minutes=5)),
        ("R037", "price-last", Decimal(125), END),
        *(
            ("R151", f"rv-{i}", Decimal(100) * Decimal("1.1") ** i, stamp)
            for i, stamp in enumerate(RISK_STAMPS)
        ),
    )
    for i, (rid, oid, value, stamp) in enumerate(records, 1):
        if oid == omitted:
            continue
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("recon-d041-" + oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("recon-d041-" + oid),
                source_provider=raw.provider_id("controlled-recon-d041"),
                native_record={"metric": {rid: value}},
                received_ts_utc=stamp,
                ingestion_sequence=i,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d041"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    ids = ("R143", "R137", "R037", "R151")

    def score(sid, version, features):
        return api.CalculationParameterSetV1(
            sid,
            version,
            "P_SCORE",
            (("intercept", Decimal(0)),),
            tuple(
                api.ScoreFeatureV1(
                    did,
                    "component",
                    () if component is None else (component,),
                    "identity",
                    None,
                    orientation,
                    Decimal(1),
                    None,
                    None,
                    (),
                )
                for did, component, orientation in features
            ),
        )

    trend_features = (
        ("D020", None, 1),
        ("D021", None, 1),
        ("D027", "price_per_minute", 1),
        ("D024", "accel_1v5", 1),
    )
    mean_features = (
        ("D026", "percent_difference", 1),
        ("D040", None, -1),
        ("D033", None, -1),
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"recon-d041-map-{rid}",
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-recon-d041",
                "metric",
                ("metric", rid),
                "canonical",
            )
            for rid in ids
        ),
        parameter_sets=(
            score("recon-d041-parent", 1, mean_features),
            score("recon-d041-trend", 1, trend_features),
            score("recon-d041-trend", 2, (*trend_features[:-1], ("D024", "accel_1v5", -1))),
            api.CalculationParameterSetV1(
                "recon-d041-window", 1, "P_WINDOW", (("window_seconds", 1800),)
            ),
            api.CalculationParameterSetV1(
                "recon-d041-risk",
                1,
                "P_VOL_WINDOW",
                (
                    ("required_intervals", 2),
                    ("required_sample_instants_utc", RISK_STAMPS),
                    (
                        "trading_year_fraction_per_interval",
                        Decimal(15) / (Decimal(252) * Decimal(390)),
                    ),
                ),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "recon-d041-subject",
                1,
                ("subject_instrument",),
                timedelta(minutes=40),
                timedelta(minutes=40),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "recon-d041-unit",
                1,
                "canonical",
                "canonical",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D041",
        "NVDA",
        NOW,
        NOW,
        "recon-d041-definition",
        "recon-d041-parent",
        1,
        "recon-d041-subject",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "recon-d041-parent", 1),
            api.ParameterProfileRefV1("P_WINDOW", "recon-d041-window", 1),
            api.ParameterProfileRefV1("P_VOL_WINDOW", "recon-d041-risk", 1),
        ),
        predecessor_parameter_profile_refs=(
            ("D040", api.ParameterProfileRefV1("P_SCORE", "recon-d041-trend", child_version)),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1(f"recon-d041-map-{rid}", 1),
                api.VersionRefV1("recon-d041-unit", 1),
                "NVDA",
                None,
            )
            for rid in ids
        ),
    )
    return owner, request


def test_reconstructed_d041_public_distinct_nested_score_versions_and_lineage():
    owner, request = _public()
    result = owner.materialise(request)
    assert result is not None
    q1 = (Decimal(120) / Decimal(110)).ln()
    q5 = (Decimal(120) / Decimal(100)).ln()
    q30 = (Decimal(120) / Decimal(80)).ln()
    trend = q5 + q30 + Decimal(4) + q1 - q5 / Decimal(5)
    # Exact Decimal result from the required three-instance return grid.
    rv = Decimal("7.714827737067631758319928528")
    predecessors = {
        previous.derived_signal_id: previous
        for previous in (
            owner.reads.get_derived_occurrence(pid) for pid in result.predecessor_occurrence_ids
        )
        if previous is not None
    }
    assert set(predecessors) == {"D026", "D040", "D033"}
    assert predecessors["D040"].result == trend
    assert predecessors["D033"].result == rv
    percent_difference = dict(predecessors["D026"].result)["percent_difference"]
    assert percent_difference == Decimal(100) * (Decimal(125) / Decimal(120) - 1)
    expected = sum((percent_difference, -trend, -rv), Decimal(0))
    assert result.result == expected
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "recon-d041-" + name
        for name in (
            "close-last",
            "close-1m",
            "close-5m",
            "close-30m",
            "vwap-last",
            "vwap-5m",
            "price-last",
            "rv-0",
            "rv-1",
            "rv-2",
        )
    }
    assert owner.materialise(request) == result
    other = owner.materialise(
        replace(
            request,
            predecessor_parameter_profile_refs=(
                (
                    "D040",
                    api.ParameterProfileRefV1("P_SCORE", "recon-d041-trend", 2),
                ),
            ),
        )
    )
    assert other is not None and other.derived_occurrence_id != result.derived_occurrence_id
    assert other.result != result.result


def test_reconstructed_d041_missing_nested_parameter_contract_refuses():
    owner, request = _public()
    assert owner.materialise(replace(request, predecessor_parameter_profile_refs=())) is None


def test_reconstructed_d041_missing_risk_history_refuses():
    owner, request = _public(omitted="rv-1")
    assert owner.materialise(request) is None


def test_reconstructed_d041_unknown_child_parameter_version_refuses():
    owner, request = _public(child_version=999)
    assert owner.materialise(request) is None


def test_reconstructed_d041_rejects_duplicate_child_profile_bindings():
    import pytest

    _, request = _public()
    with pytest.raises(ValueError, match="distinct by D and profile"):
        replace(
            request,
            predecessor_parameter_profile_refs=(
                ("D040", api.ParameterProfileRefV1("P_SCORE", "recon-d041-trend", 1)),
                ("D040", api.ParameterProfileRefV1("P_SCORE", "recon-d041-trend", 2)),
            ),
        )
