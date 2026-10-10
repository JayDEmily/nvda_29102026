"""F4 RC14: public M00 exact comparable-IV baseline for D105/106."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
POINT = raw.RawSelectionIdentityV1((
    ("underlying_instrument", "NVDA"), ("surface_point", "ATM30D"),
))
KEY_PATHS = tuple((key, ("selection", key)) for key, _ in POINT.values)


def _public(
    did: str, *, current: Decimal = Decimal("0.30"),
    missing: str | None = None, wrong_point: str | None = None,
    future: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    rows = (
        ("prior-1", Decimal("0.20"), 100),
        ("prior-2", Decimal("0.40"), 50),
        ("current", current, 0),
        ("other-point", Decimal("0.99"), 1),
    )
    for seq, (oid, value, days) in enumerate(rows, 1):
        if oid == missing:
            continue
        identity = dict(POINT.values)
        if oid in (wrong_point, "other-point"):
            identity["surface_point"] = "OTM10D"
        at = NOW - timedelta(days=days, seconds=4)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("ivbase-" + oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("ivbase-" + oid),
                source_provider=raw.provider_id("controlled-rc14-ivbase"),
                native_record={"metric": {"R183": value}, "selection": identity},
                received_ts_utc=NOW + timedelta(seconds=1) if oid == future else at,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:ivbase"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=at.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId("R183"),),
                source_variant="surface-point",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=(raw.RawSignalProjectionMappingV1(
            "rc14-ivbase-map", 1, raw.RawSignalCatalogueId("R183"),
            "controlled-rc14-ivbase", "surface-point", ("metric", "R183"),
            "canonical", KEY_PATHS,
        ),),
        parameter_sets=(api.CalculationParameterSetV1(
            "rc14-ivbase", 1, "P_BASELINE", (("history_count", 2), ("minimum_sample", 2)),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc14-ivbase-select", 1, tuple(key for key, _ in POINT.values),
            timedelta(days=366), timedelta(days=366), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "rc14-ivbase-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "rc14-ivbase-public", "rc14-ivbase", 1,
        "rc14-ivbase-select", 1, (),
        raw_input_bindings=(api.RawInputBindingV1(
            "R183", api.VersionRefV1("rc14-ivbase-map", 1),
            api.VersionRefV1("rc14-ivbase-unit", 1), "NVDA", POINT,
        ),),
    )
    return owner, request


@pytest.mark.parametrize("did", ("D105", "D106"))
def test_rc14_historical_only_iv_baseline_exact_midrange(did: str) -> None:
    owner, req = _public(did)
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal(50)
    assert out.selection_identity == POINT
    assert {line.observation_occurrence_id for line in out.raw_input_lineage} == {
        "ivbase-prior-1", "ivbase-prior-2", "ivbase-current",
    }
    assert owner.materialise(req) == out


@pytest.mark.parametrize("did,expected", (("D105", Decimal(100)), ("D106", Decimal(75))))
def test_rc14_iv_current_equal_to_prior_observation(did: str, expected: Decimal) -> None:
    owner, req = _public(did, current=Decimal("0.40"))
    out = owner.materialise(req)
    assert out is not None and out.result == expected


@pytest.mark.parametrize("did", ("D105", "D106"))
def test_rc14_iv_baseline_refuses_insufficient_prior_history(did: str) -> None:
    owner, req = _public(did, missing="prior-1")
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", ("D105", "D106"))
def test_rc14_iv_baseline_refuses_different_point_history(did: str) -> None:
    owner, req = _public(did, wrong_point="prior-1")
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", ("D105", "D106"))
def test_rc14_iv_baseline_refuses_current_after_cutoff(did: str) -> None:
    owner, req = _public(did, future="current")
    assert owner.materialise(req) is None
