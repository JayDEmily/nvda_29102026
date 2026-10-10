"""F4 RC06: D040 public weighted momentum, slope and persistence score."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
END = NOW - timedelta(seconds=2)


def _public(
    *, missing: str | None = None, wrong_subject: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    rows = (
        ("R143", "trend-last", Decimal(120), END),
        ("R143", "trend-1m", Decimal(110), END - timedelta(minutes=1)),
        ("R143", "trend-5m", Decimal(100), END - timedelta(minutes=5)),
        ("R143", "trend-30m", Decimal(80), END - timedelta(minutes=30)),
        ("R137", "trend-vwap-last", Decimal(120), END),
        ("R137", "trend-vwap-5m", Decimal(100), END - timedelta(minutes=5)),
    )
    for index, (rid, oid, value, stamp) in enumerate(rows, 1):
        if oid == missing:
            continue
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref(oid),
                source_provider=raw.provider_id("controlled-rc06-trend"),
                native_record={"metric": {rid: value}},
                received_ts_utc=stamp,
                ingestion_sequence=index,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc06:trend"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument="AMD" if oid == wrong_subject else "NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc06-trend-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc06-trend", "metric", ("metric", rid), "canonical",
            ) for rid in ("R143", "R137")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc06-trend-score", 1, "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(
                    api.ScoreFeatureV1(
                        did, "component", () if component is None else (component,),
                        "identity", None, 1, Decimal(1), None, None, (),
                    )
                    for did, component in (
                        ("D020", None),
                        ("D021", None),
                        ("D027", "price_per_minute"),
                        ("D024", "accel_1v5"),
                    )
                ),
            ),
            api.CalculationParameterSetV1(
                "rc06-trend-window", 1, "P_WINDOW",
                (("window_seconds", 1800),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc06-trend-subject", 1, ("subject_instrument",),
                timedelta(minutes=40), timedelta(minutes=40), ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc06-trend-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D040", "NVDA", NOW, NOW, "rc06-trend-public",
        "rc06-trend-score", 1, "rc06-trend-subject", 1, (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "rc06-trend-score", 1),
            api.ParameterProfileRefV1("P_WINDOW", "rc06-trend-window", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc06-trend-map-" + rid, 1),
                api.VersionRefV1("rc06-trend-unit", 1), "NVDA", None,
            ) for rid in ("R143", "R137")
        ),
    )
    return owner, request


def test_rc06_public_d040_exact_four_predecessors_and_weighted_trend() -> None:
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None
    q1 = (Decimal(120) / Decimal(110)).ln()
    q5 = (Decimal(120) / Decimal(100)).ln()
    q30 = (Decimal(120) / Decimal(80)).ln()
    expected = q5 + q30 + Decimal(4) + q1 - q5 / Decimal(5)
    assert out.result == expected
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == {"D020", "D021", "D027", "D024"}
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "trend-last", "trend-1m", "trend-5m", "trend-30m",
        "trend-vwap-last", "trend-vwap-5m",
    }
    assert owner.materialise(req) == out


def test_rc06_public_d040_missing_half_hour_anchor_refuses() -> None:
    owner, req = _public(missing="trend-30m")
    assert owner.materialise(req) is None


def test_rc06_public_d040_wrong_subject_vwap_anchor_refuses() -> None:
    owner, req = _public(wrong_subject="trend-vwap-5m")
    assert owner.materialise(req) is None
