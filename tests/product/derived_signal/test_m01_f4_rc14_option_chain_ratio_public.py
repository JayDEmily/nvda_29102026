"""F4 RC14: exact expiry/strike-region aggregated call:put ratios through M00."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
REGION = raw.RawSelectionIdentityV1((
    ("underlying_instrument", "NVDA"),
    ("expiry", "2026-12-18"),
    ("strike_region", "145-155"),
))
KEY_PATHS = tuple((key, ("selection", key)) for key, _ in REGION.values)
PAIRS = {
    "D118": ("R049", "R050", Decimal(300), Decimal(150)),
    "D119": ("R047", "R048", Decimal(400), Decimal(200)),
}


def _public(
    did: str, *, missing: str | None = None, zero_denominator: bool = False,
    wrong_region: str | None = None, future: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    numerator, denominator, num, den = PAIRS[did]
    m00 = raw.create_owner()
    rows = (
        (numerator, "chosen-call", num, REGION),
        (denominator, "chosen-put", Decimal(0) if zero_denominator else den, REGION),
        (numerator, "decoy-call", Decimal(9999), raw.RawSelectionIdentityV1((
            ("underlying_instrument", "NVDA"),
            ("expiry", "2027-01-15"),
            ("strike_region", "145-155"),
        ))),
    )
    for seq, (rid, oid, quantity, chosen_identity) in enumerate(rows, 1):
        if oid == missing:
            continue
        selected = dict(chosen_identity.values)
        if oid == wrong_region:
            selected["strike_region"] = "200-210"
        stamp = NOW - timedelta(seconds=4)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("rc14-" + oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc14-" + oid),
                source_provider=raw.provider_id("controlled-rc14-chain"),
                native_record={"metric": {rid: quantity}, "selection": selected},
                received_ts_utc=NOW + timedelta(seconds=1) if oid == future else stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc14:chain"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="expiry-region-aggregate",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc14-chain-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc14-chain", "expiry-region-aggregate",
                ("metric", rid), "canonical", KEY_PATHS,
            ) for rid in (numerator, denominator)
        ),
        parameter_sets=(api.CalculationParameterSetV1(
            "rc14-ratio-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc14-ratio-select", 1, tuple(key for key, _ in REGION.values),
            timedelta(seconds=30), timedelta(seconds=30), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "rc14-ratio-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "rc14-chain-ratio-public", "rc14-ratio-basic", 1,
        "rc14-ratio-select", 1, (),
        raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("rc14-chain-map-" + rid, 1),
            api.VersionRefV1("rc14-ratio-unit", 1), "NVDA", REGION,
        ) for rid in (numerator, denominator)),
    )
    return owner, request


@pytest.mark.parametrize("did", tuple(PAIRS))
def test_rc14_exact_chain_ratio_and_raw_identity(did: str) -> None:
    owner, req = _public(did)
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal(2)
    assert out.selection_identity == REGION
    assert {item.observation_occurrence_id for item in out.raw_input_lineage} == {
        "rc14-chosen-call", "rc14-chosen-put",
    }
    assert {item.raw_signal_id for item in out.raw_input_lineage} == set(PAIRS[did][:2])
    assert owner.materialise(req) == out


@pytest.mark.parametrize("did", tuple(PAIRS))
def test_rc14_chain_ratio_refuses_missing_put(did: str) -> None:
    owner, req = _public(did, missing="chosen-put")
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", tuple(PAIRS))
def test_rc14_chain_ratio_refuses_zero_denominator(did: str) -> None:
    owner, req = _public(did, zero_denominator=True)
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", tuple(PAIRS))
def test_rc14_chain_ratio_refuses_wrong_strike_region(did: str) -> None:
    owner, req = _public(did, wrong_region="chosen-put")
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", tuple(PAIRS))
def test_rc14_chain_ratio_refuses_future_put_receipt(did: str) -> None:
    owner, req = _public(did, future="chosen-put")
    assert owner.materialise(req) is None
