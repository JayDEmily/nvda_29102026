"""F4 RC04 K04: admitted-M00 public baseline and sample-SD evidence.

Accepted brief K04: current is excluded from the N strictly prior historical
samples, SD uses N-1, a zero spread refuses z-score, and no sample is
fabricated to complete missing history.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
CASES = (
    ("D029", "R144", "z"),
    ("D030", "R062", "z"),
    ("D031", "R063", "z"),
)


def _owner_request(
    did: str,
    rid: str,
    *,
    no_history: bool = False,
    flat_history: bool = False,
    wrong_subject: bool = False,
    future_current: bool = False,
    missing_fraction: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    anchor = NOW - timedelta(minutes=1)
    samples = (
        ("baseline-older", Decimal(8), anchor - timedelta(minutes=4), "NVDA"),
        ("baseline-prior", Decimal(8 if flat_history else 12),
         anchor - timedelta(minutes=2), "NVDA"),
        ("baseline-current", Decimal(16), anchor, "NVDA"),
        ("baseline-other-subject", Decimal(999), anchor - timedelta(minutes=3), "AMD"),
    )
    source_ids = (rid,) if did != "D028" else (rid, "R044")
    seq = 0
    for oid, value, effective, subject in samples:
        if no_history and oid.startswith("baseline-") and oid != "baseline-current":
            continue
        if wrong_subject and oid == "baseline-prior":
            subject = "AMD"
        if future_current and oid == "baseline-current":
            effective = NOW + timedelta(seconds=3)
        seq += 1
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("baseline-" + oid),
                source_provider=raw.provider_id("controlled-rc04"),
                native_record={"metrics": {rid: value}},
                received_ts_utc=effective,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rc04:baseline"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=effective.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="metric",
                subject_instrument=subject,
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    if did == "D028" and not missing_fraction:
        seq += 1
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("baseline-session-fraction"),
                delivery_artifact_ref=raw.delivery_artifact_ref("baseline-fraction"),
                source_provider=raw.provider_id("controlled-rc04"),
                native_record={"metrics": {"R044": Decimal("0.5")}},
                received_ts_utc=anchor,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rc04:baseline"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=anchor.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R044"),),
                source_variant="metric",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc04-baseline-map-" + key, 1,
                raw.RawSignalCatalogueId(key),
                "controlled-rc04", "metric", ("metrics", key), "canonical",
            )
            for key in source_ids
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc04-baseline", 1, "P_BASELINE",
                (("history_count", 2), ("minimum_sample", 2)),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc04-subject", 1, ("subject_instrument",),
                timedelta(minutes=15), timedelta(minutes=15),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc04-unit", 1, "canonical", "canonical",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW,
        "rc04-public", "rc04-baseline", 1,
        "rc04-subject", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                key, api.VersionRefV1("rc04-baseline-map-" + key, 1),
                api.VersionRefV1("rc04-unit", 1), "NVDA", None,
            ) for key in source_ids
        ),
    )
    return owner, req


@pytest.mark.parametrize(("did", "rid", "kind"), CASES)
def test_rc04_public_baseline_excludes_current_and_preserves_lineage(
    did: str, rid: str, kind: str,
) -> None:
    owner, req = _owner_request(did, rid)
    result = owner.materialise(req)
    assert result is not None
    expected = Decimal("1.6") if kind == "1.6" else Decimal(6) / Decimal(8).sqrt()
    assert result.result == expected
    used = {entry.observation_occurrence_id for entry in result.raw_input_lineage}
    assert {"baseline-older", "baseline-prior", "baseline-current"} <= used
    assert "baseline-other-subject" not in used
    if did == "D028":
        assert "baseline-session-fraction" in used
    assert result.predecessor_occurrence_ids == ()
    assert owner.materialise(req) == result


@pytest.mark.parametrize(("did", "rid", "kind"), CASES)
def test_rc04_public_baseline_missing_prior_sample_refuses(
    did: str, rid: str, kind: str,
) -> None:
    owner, req = _owner_request(did, rid, no_history=True)
    assert owner.materialise(req) is None


@pytest.mark.parametrize(("did", "rid", "kind"), CASES[1:])
def test_rc04_public_zero_sample_standard_deviation_refuses(
    did: str, rid: str, kind: str,
) -> None:
    owner, req = _owner_request(did, rid, flat_history=True)
    assert owner.materialise(req) is None


def test_rc04_public_d028_missing_elapsed_session_fraction_refuses() -> None:
    owner, req = _owner_request("D028", "R041", missing_fraction=True)
    assert owner.materialise(req) is None
