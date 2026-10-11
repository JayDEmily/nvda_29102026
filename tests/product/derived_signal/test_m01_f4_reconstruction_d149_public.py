"""Reconstructed F4 RC21 D149: exact funding and independently-scored D061."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
FUNDING = {"R257": Decimal("0.03"), "R256": Decimal("0.025")}
VOL = (
    ("R236", Decimal(21), Decimal(20)),
    ("R237", Decimal(110), Decimal(100)),
    ("R238", Decimal(18), None),
    ("R239", Decimal(19), None),
    ("R240", Decimal(23), None),
)
IDS = (*FUNDING, *(rid for rid, _, _ in VOL))


def _feature(did: str, component: str | None = None):
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
    *, missing: str | None = None, future: str | None = None, wrong_subject: str | None = None
):
    m00 = raw.create_owner()
    data = [
        (rid, "current-" + rid, value, NOW - timedelta(seconds=2)) for rid, value in FUNDING.items()
    ]
    for rid, latest, prior in VOL:
        if prior is not None:
            data.append((rid, "prior-" + rid, prior, NOW - timedelta(seconds=302)))
        data.append((rid, "current-" + rid, latest, NOW - timedelta(seconds=2)))
    for seq, (rid, tag, value, ts) in enumerate(data, 1):
        if tag == missing:
            continue
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("recon-d149-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("recon-d149-" + tag),
                source_provider=raw.provider_id("controlled-recon-d149"),
                native_record={"metric": {rid: value}},
                received_ts_utc=NOW + timedelta(seconds=1) if tag == future else ts,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d149"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=ts.isoformat(),
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
                "recon-d149-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-recon-d149",
                "metric",
                ("metric", rid),
                "canonical",
            )
            for rid in IDS
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "recon-d149-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(_feature(did) for did in ("R257", "R256", "D047", "D061")),
            ),
            api.CalculationParameterSetV1(
                "recon-d149-vol-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                (
                    _feature("D052", "percent_change"),
                    _feature("D053", "percent_change"),
                    _feature("D057", "point_difference"),
                    _feature("D058", "point_difference"),
                    _feature("D059", "point_difference"),
                    _feature("D060"),
                ),
            ),
            api.CalculationParameterSetV1(
                "recon-d149-window",
                1,
                "P_WINDOW",
                (("anchor_seconds", 300),),
            ),
            api.CalculationParameterSetV1(
                "recon-d149-basic",
                1,
                "P_BASIC",
                (("basic_version", 1),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "recon-d149-select",
                1,
                ("subject_instrument",),
                timedelta(minutes=10),
                timedelta(minutes=10),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "recon-d149-unit",
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
        "D149",
        "NVDA",
        NOW,
        NOW,
        "recon-d149-definition",
        "recon-d149-score",
        1,
        "recon-d149-select",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "recon-d149-score", 1),
            api.ParameterProfileRefV1("P_WINDOW", "recon-d149-window", 1),
            api.ParameterProfileRefV1("P_BASIC", "recon-d149-basic", 1),
        ),
        predecessor_parameter_profile_refs=(
            ("D061", api.ParameterProfileRefV1("P_SCORE", "recon-d149-vol-score", 1)),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("recon-d149-map-" + rid, 1),
                api.VersionRefV1("recon-d149-unit", 1),
                "NVDA",
                None,
            )
            for rid in IDS
        ),
    )
    return owner, request


def test_reconstructed_d149_public_exact_funding_regime_and_lineage():
    owner, req = _public()
    result = owner.materialise(req)
    assert result is not None
    child_expected = Decimal(10) + Decimal(110) / Decimal(21)
    expected = sum((Decimal("0.03"), Decimal("0.025"), Decimal(50), child_expected), Decimal(0))
    assert result.result == expected
    parents = {
        child.derived_signal_id: child
        for child in (
            owner.reads.get_derived_occurrence(pid) for pid in result.predecessor_occurrence_ids
        )
        if child is not None
    }
    assert set(parents) == {"D047", "D061"}
    assert parents["D047"].result == Decimal(50)
    assert parents["D061"].result == child_expected
    assert api.VersionRefV1("recon-d149-vol-score", 1) in parents["D061"].parameter_context_refs
    assert api.VersionRefV1("recon-d149-score", 1) in result.parameter_context_refs
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "recon-d149-" + tag
        for tag in (
            "current-R257",
            "current-R256",
            "prior-R236",
            "prior-R237",
            *("current-" + rid for rid, *_ in VOL),
        )
    }
    assert owner.materialise(req) == result


def test_reconstructed_d149_refuses_wrong_child_score_profile():
    owner, req = _public()
    assert owner.materialise(replace(req, predecessor_parameter_profile_refs=())) is None


def test_reconstructed_d149_refuses_missing_funding_input():
    owner, req = _public(missing="current-R257")
    assert owner.materialise(req) is None


def test_reconstructed_d149_refuses_missing_child_history():
    owner, req = _public(missing="prior-R236")
    assert owner.materialise(req) is None


def test_reconstructed_d149_refuses_future_funding_input():
    owner, req = _public(future="current-R257")
    assert owner.materialise(req) is None


def test_reconstructed_d149_refuses_wrong_subject_child_input():
    owner, req = _public(wrong_subject="current-R238")
    assert owner.materialise(req) is None
