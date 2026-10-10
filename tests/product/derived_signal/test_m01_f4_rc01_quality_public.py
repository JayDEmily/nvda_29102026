"""F4 RC01: public M00 temporal-quality score and structured alignment (D006/D008)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, 0, tzinfo=UTC)
EVENT = NOW - timedelta(seconds=10)


def feature(
    signal_id: str,
    weight: str,
    *,
    orientation: int = 1,
    extractor: str = "component",
    arguments: tuple[str, ...] = (),
) -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(
        signal_id,
        extractor,
        arguments,
        "identity",
        None,
        orientation,
        Decimal(weight),
        None,
        None,
        (),
    )


def owner_request(
    did: str,
    *,
    omit: str | None = None,
    all_receipt_only: bool = False,
    other_subject: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    samples = (
        ("R001", "quality-r1", "quote", NOW - timedelta(seconds=5), "true_instant"),
        ("R001", "quality-r2", "option", NOW - timedelta(seconds=10), "true_instant"),
        ("R001", "quality-r3", "receipt", NOW - timedelta(seconds=7), "receipt_only"),
        ("R002", "quality-ts", EVENT.isoformat(), EVENT, "true_instant"),
        ("R003", "quality-tz", "UTC", EVENT, "true_instant"),
        ("R005", "quality-type", Decimal(1), EVENT, "true_instant"),
        ("R058", "quality-cadence", Decimal(5), EVENT, "true_instant"),
    )
    for idx, (rid, oid, value, event, kind) in enumerate(samples, 1):
        if rid == omit:
            continue
        if all_receipt_only and rid == "R001":
            kind = "receipt_only"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("quality-" + oid),
                source_provider=raw.provider_id("controlled-rc01-quality"),
                native_record={"metric": {"value": value}},
                received_ts_utc=event,
                ingestion_sequence=idx,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc01:quality"),
                source_temporal_kind=kind,
                source_timestamp_raw=event.isoformat() if kind == "true_instant" else None,
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="quality",
                subject_instrument="AMD" if rid == other_subject else "NVDA",
                native_units="quality_units",
                revision_vintage_native="v1",
            )
        )
    score_features = (
        (
            feature("D002", "0.1", extractor="component", arguments=("age_seconds",)),
            feature("R005", "0.5"),
            feature("R058", "0.25"),
        )
        if did == "D006"
        else (
            feature(
                "D002", "0.2", orientation=-1, extractor="component", arguments=("age_seconds",)
            ),
        )
    )
    raw_ids = ("R001", "R002", "R003", "R005", "R058")
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "quality-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-rc01-quality",
                "quality",
                ("metric", "value"),
                "quality_units",
            )
            for rid in raw_ids
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "quality-time",
                1,
                "P_TIME",
                (("exchange_timezone", "UTC"),),
            ),
            api.CalculationParameterSetV1(
                "quality-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                score_features,
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "quality-selector",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant", "receipt_only"),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "quality-units",
                1,
                "quality_units",
                "quality_units",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        did,
        "NVDA",
        NOW,
        NOW,
        "quality-public",
        "quality-score",
        1,
        "quality-selector",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "quality-score", 1),
            api.ParameterProfileRefV1("P_TIME", "quality-time", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("quality-map-" + rid, 1),
                api.VersionRefV1("quality-units", 1),
                "NVDA",
                None,
            )
            for rid in raw_ids
        ),
    )
    return owner, request


def test_d006_public_combines_exact_time_age_data_type_and_update_cadence() -> None:
    owner, req = owner_request("D006")
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal("2.75")
    assert {"R001", "R002", "R003", "R005", "R058"} <= {
        item.raw_signal_id for item in out.raw_input_lineage
    }
    assert {
        owner.reads.get_derived_occurrence(p).derived_signal_id
        for p in out.predecessor_occurrence_ids
    } == {"D002"}
    assert owner.materialise(req) == out


def test_d008_public_instant_skew_and_receipt_missingness_are_not_conflated() -> None:
    owner, req = owner_request("D008")
    out = owner.materialise(req)
    assert out is not None
    fields = dict(out.result)
    assert fields["max_true_instant_skew_seconds"] == Decimal(5)
    assert fields["event_time_coverage_fraction"] == Decimal(2) / Decimal(3)
    assert fields["missing_event_time_count"] == 1
    assert fields["alignment_score"] == Decimal(1) / (Decimal(1) + Decimal(2).exp())
    assert {"D001", "D002"} == {
        owner.reads.get_derived_occurrence(p).derived_signal_id
        for p in out.predecessor_occurrence_ids
    }
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} >= {
        "quality-r1",
        "quality-r2",
        "quality-r3",
        "quality-ts",
        "quality-tz",
    }
    assert owner.materialise(req) == out


@pytest.mark.parametrize(
    ("did", "absent"),
    (
        ("D006", "R005"),
        ("D006", "R058"),
        ("D006", "R002"),
        ("D008", "R001"),
        ("D008", "R002"),
    ),
)
def test_rc01_quality_public_refuses_missing_declared_inputs(did: str, absent: str) -> None:
    owner, req = owner_request(did, omit=absent)
    assert owner.materialise(req) is None


def test_d008_public_all_receipt_only_does_not_invent_event_time_skew() -> None:
    owner, req = owner_request("D008", all_receipt_only=True)
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", ("D006", "D008"))
def test_rc01_quality_refuses_wrong_subject(did: str) -> None:
    owner, req = owner_request(did, other_subject="R001")
    assert owner.materialise(req) is None
