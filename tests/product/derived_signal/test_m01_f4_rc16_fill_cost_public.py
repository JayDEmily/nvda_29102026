"""F4 RC16: D179 arrival benchmark and D193 matched realised cost via M00."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
IDENTITY = raw.RawSelectionIdentityV1(
    (
        ("contract_id", "NVDA-C150-DEC"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
    )
)
IDENTITY_PATHS = tuple((key, ("identity", key)) for key, _ in IDENTITY.values)
FIELDS = ("R034", "R035", "R229", "R221", "R233", "R228", "R016")


def _public(
    did: str,
    *,
    side: str = "buy",
    missing: str | None = None,
    future: str | None = None,
    wrong_quote_contract: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    records = (
        ("quote", {"R034": Decimal("99.5"), "R035": Decimal("100.5")}, 4),
        (
            "fill",
            {
                "R229": Decimal("100.2"),
                "R221": Decimal("99.8"),
                "R233": Decimal(2),
                "R228": Decimal(3),
                "R016": Decimal(100),
            },
            2,
        ),
    )
    for seq, (tag, native, seconds) in enumerate(records, start=1):
        data = dict(native)
        if missing in data:
            del data[missing]
        stamp = NOW - timedelta(seconds=seconds)
        identity = dict(IDENTITY.values)
        if wrong_quote_contract and tag == "quote":
            identity["contract_id"] = "OTHER-CALL"
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id("fill-cost-" + tag),
                delivery_artifact_ref=raw.delivery_artifact_ref("fill-cost-" + tag),
                source_provider=raw.provider_id("controlled-rc16-fill"),
                native_record={"values": data, "identity": identity},
                received_ts_utc=NOW + timedelta(seconds=1) if tag == future else stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc16:fill"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in native),
                source_variant="fill",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc16-fill-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-rc16-fill",
                "fill",
                ("values", rid),
                "canonical",
                IDENTITY_PATHS,
            )
            for rid in FIELDS
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc16-fill-basic",
                1,
                "P_BASIC",
                (("side", side),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc16-fill-contract",
                1,
                tuple(dict(IDENTITY.values)),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc16-fill-unit",
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
    req = api.CalculationRequestV1(
        did,
        "NVDA",
        NOW,
        NOW,
        "rc16-fill-cost-public",
        "rc16-fill-basic",
        1,
        "rc16-fill-contract",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("rc16-fill-map-" + rid, 1),
                api.VersionRefV1("rc16-fill-unit", 1),
                "NVDA",
                IDENTITY,
            )
            for rid in FIELDS
        ),
    )
    return owner, req


@pytest.mark.parametrize(("side", "expected"), (("buy", Decimal("0.4")), ("sell", Decimal("-0.4"))))
def test_d179_exact_signed_arrival_slippage_and_lineage(side: str, expected: Decimal) -> None:
    owner, req = _public("D179", side=side)
    out = owner.materialise(req)
    assert out is not None
    assert dict(out.result) == {
        "price_slippage": expected,
        "bps_slippage": Decimal(10000) * expected / Decimal("99.8"),
    }
    assert out.selection_identity == IDENTITY
    assert {r.raw_signal_id for r in out.raw_input_lineage} == {
        "R229",
        "R221",
        "R034",
        "R035",
    }
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == {"D087"}
    assert owner.materialise(req) == out


@pytest.mark.parametrize(("side", "expected"), (("buy", Decimal(122)), ("sell", Decimal(-118))))
def test_d193_cost_uses_d179_arrival_slippage_not_d087_quote_mid(
    side: str,
    expected: Decimal,
) -> None:
    owner, req = _public("D193", side=side)
    out = owner.materialise(req)
    assert out is not None
    assert out.result == expected
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == {"D087", "D179"}
    assert {r.raw_signal_id for r in out.raw_input_lineage} == set(FIELDS)
    assert owner.materialise(req) == out


@pytest.mark.parametrize("did", ("D179", "D193"))
def test_realised_cost_refuses_missing_arrival_benchmark(did: str) -> None:
    owner, req = _public(did, missing="R221")
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", ("D179", "D193"))
def test_realised_cost_refuses_wrong_contract_quote(did: str) -> None:
    owner, req = _public(did, wrong_quote_contract=True)
    assert owner.materialise(req) is None


def test_d193_refuses_missing_executed_quantity() -> None:
    owner, req = _public("D193", missing="R228")
    assert owner.materialise(req) is None


def test_d193_refuses_future_received_execution() -> None:
    owner, req = _public("D193", future="fill")
    assert owner.materialise(req) is None
