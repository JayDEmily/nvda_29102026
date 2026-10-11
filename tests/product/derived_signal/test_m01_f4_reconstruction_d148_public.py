"""Reconstructed F4 RC21: D148 public macro factor and predecessor provenance."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
CURRENT = NOW - timedelta(seconds=3)
PAST = CURRENT - timedelta(days=1)
RAW = ("R256", "R258", "R259", "R247", "R249", "R252")
VALUES = dict(
    zip(
        RAW,
        (Decimal(1), Decimal(2), Decimal(3), Decimal("0.04"), Decimal("0.0525"), Decimal("0.027")),
        strict=True,
    )
)


def _public(
    *, missing: str | None = None, future: str | None = None, wrong_subject: str | None = None
):
    m00 = raw.create_owner()
    data = [
        ("R249", "prior-nominal", Decimal("0.0500"), PAST),
        ("R252", "prior-real", Decimal("0.0250"), PAST),
    ] + [(rid, "current-" + rid, value, CURRENT) for rid, value in VALUES.items()]
    for i, (rid, tag, value, timestamp) in enumerate(data, 1):
        if tag == missing:
            continue
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("recon-d148-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("recon-d148-" + tag),
                source_provider=raw.provider_id("controlled-recon-d148"),
                native_record={"metric": {rid: value}},
                received_ts_utc=NOW + timedelta(seconds=1) if tag == future else timestamp,
                ingestion_sequence=i,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d148"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=timestamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument="AMD" if tag == wrong_subject else "NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "recon-d148-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-recon-d148",
                "metric",
                ("metric", rid),
                "canonical",
            )
            for rid in RAW
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "recon-d148-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(
                    api.ScoreFeatureV1(
                        did, "component", (), "identity", None, 1, Decimal(1), None, None, ()
                    )
                    for did in (*RAW, "D042", "D044", "D045")
                ),
            ),
            api.CalculationParameterSetV1(
                "recon-d148-basic", 1, "P_BASIC", (("unit", "canonical"),)
            ),
            api.CalculationParameterSetV1(
                "recon-d148-window", 1, "P_WINDOW", (("anchor_days", 1),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "recon-d148-subject",
                1,
                ("subject_instrument",),
                timedelta(days=2),
                timedelta(days=2),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "recon-d148-unit",
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
        "D148",
        "NVDA",
        NOW,
        NOW,
        "recon-d148-definition",
        "recon-d148-score",
        1,
        "recon-d148-subject",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "recon-d148-score", 1),
            api.ParameterProfileRefV1("P_BASIC", "recon-d148-basic", 1),
            api.ParameterProfileRefV1("P_WINDOW", "recon-d148-window", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("recon-d148-map-" + rid, 1),
                api.VersionRefV1("recon-d148-unit", 1),
                "NVDA",
                None,
            )
            for rid in RAW
        ),
    )
    return owner, request


def test_reconstructed_d148_public_exact_macro_factor_and_full_lineage():
    owner, request = _public()
    out = owner.materialise(request)
    assert out is not None
    # Brief §5 D042 returns percentage points (100 times decimal-yield spread),
    # while D044/D045 return basis-point changes.
    assert out.result == Decimal("52.3695")
    predecessors = {
        item.derived_signal_id: item
        for item in (
            owner.reads.get_derived_occurrence(pid) for pid in out.predecessor_occurrence_ids
        )
        if item is not None
    }
    assert set(predecessors) == {"D042", "D044", "D045"}
    assert predecessors["D042"].result == Decimal("1.25")
    assert predecessors["D044"].result == Decimal("20")
    assert predecessors["D045"].result == Decimal("25")
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "recon-d148-" + tag
        for tag in ("prior-nominal", "prior-real", *("current-" + rid for rid in RAW))
    }
    assert owner.materialise(request) == out


def test_reconstructed_d148_absent_required_macro_component_refuses():
    owner, req = _public(missing="current-R258")
    assert owner.materialise(req) is None


def test_reconstructed_d148_future_required_macro_component_refuses():
    owner, req = _public(future="current-R258")
    assert owner.materialise(req) is None


def test_reconstructed_d148_wrong_subject_macro_component_refuses():
    owner, req = _public(wrong_subject="current-R259")
    assert owner.materialise(req) is None


def test_reconstructed_d148_missing_required_prior_rate_period_refuses():
    owner, req = _public(missing="prior-real")
    assert owner.materialise(req) is None
