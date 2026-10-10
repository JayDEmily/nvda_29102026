"""F4 RC16 proof first: M00-native complete live position legs and P&L state.

Each admitted leg has a separate native occurrence. Missing an exposure for a
selected leg is absence, not licence to compute on a smaller position set.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
GREEKS = {
    "D181": ("R112", (Decimal("0.5"), Decimal("0.2")), Decimal(80)),
    "D182": ("R115", (Decimal("0.04"), Decimal("0.01")), Decimal(7)),
    "D183": ("R116", (Decimal("1.2"), Decimal("0.5")), Decimal(190)),
    "D184": ("R117", (Decimal("-0.2"), Decimal("-0.1")), Decimal(-30)),
}


def _public(
    did: str, *, missing_on_second_leg: str | None = None,
    denominator_zero: bool = False, future_second_leg: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    if did in GREEKS:
        greek, (first, second), _ = GREEKS[did]
        data = (
            ("pos-leg-a", {"R212": Decimal(2), "R016": Decimal(100), greek: first}),
            ("pos-leg-b", {"R212": Decimal(-1), "R016": Decimal(100), greek: second}),
        )
    elif did == "D180":
        data = (("order-42-status", {"R219": Decimal(0) if denominator_zero else Decimal(6), "R220": Decimal(0) if denominator_zero else Decimal(4)}),)
    else:
        data = (("position-pnl", {"R214": Decimal(125), "R215": Decimal(-45), "R216": Decimal(80)}),)
    active_ids = tuple(dict.fromkeys(key for _, values in data for key in values))
    for seq, (oid, values) in enumerate(data, 1):
        v = dict(values)
        if oid == "pos-leg-b" and missing_on_second_leg:
            v.pop(missing_on_second_leg, None)
        stamp = NOW - timedelta(seconds=3)
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(oid),
                delivery_artifact_ref=raw.delivery_artifact_ref("rc16-" + oid),
                source_provider=raw.provider_id("controlled-rc16"),
                native_record={"position": v},
                received_ts_utc=NOW + timedelta(seconds=1) if future_second_leg and oid == "pos-leg-b" else stamp,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc16:positions"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(k) for k in v),
                source_variant="position",
                subject_instrument="NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc16-map-" + rid, 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc16", "position", ("position", rid), "canonical",
            ) for rid in active_ids
        ),
        parameter_sets=(api.CalculationParameterSetV1("rc16-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "rc16-select", 1, ("subject_instrument",),
            timedelta(seconds=30), timedelta(seconds=30), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "rc16-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW, "rc16-position-public", "rc16-basic", 1,
        "rc16-select", 1, (),
        raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1("rc16-map-" + rid, 1),
            api.VersionRefV1("rc16-unit", 1), "NVDA", None,
        ) for rid in active_ids),
    )
    return owner, req


@pytest.mark.parametrize("did", tuple(GREEKS))
def test_rc16_complete_two_leg_live_exposure(did: str) -> None:
    owner, req = _public(did)
    out = owner.materialise(req)
    assert out is not None and out.result == GREEKS[did][2]
    assert {item.observation_occurrence_id for item in out.raw_input_lineage} == {
        "pos-leg-a", "pos-leg-b",
    }
    assert {item.raw_signal_id for item in out.raw_input_lineage} == {
        "R212", "R016", GREEKS[did][0],
    }
    assert owner.materialise(req) == out


@pytest.mark.parametrize("did", tuple(GREEKS))
def test_rc16_incomplete_second_position_leg_must_refuse(did: str) -> None:
    owner, req = _public(did, missing_on_second_leg=GREEKS[did][0])
    assert owner.materialise(req) is None


@pytest.mark.parametrize("did", tuple(GREEKS))
def test_rc16_entirely_future_leg_not_visible_at_cutoff(did: str) -> None:
    owner, req = _public(did, future_second_leg=True)
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal(2) * Decimal(100) * GREEKS[did][1][0]
    assert {item.observation_occurrence_id for item in out.raw_input_lineage} == {"pos-leg-a"}


def test_rc16_public_fill_completion_exact_six_over_ten() -> None:
    owner, req = _public("D180")
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal("0.6")
    assert {item.raw_signal_id for item in out.raw_input_lineage} == {"R219", "R220"}
    assert owner.materialise(req) == out


def test_rc16_public_fill_completion_zero_denominator_refuses() -> None:
    owner, req = _public("D180", denominator_zero=True)
    assert owner.materialise(req) is None


def test_rc16_public_pnl_state_preserves_all_components() -> None:
    owner, req = _public("D185")
    out = owner.materialise(req)
    assert out is not None and dict(out.result) == {
        "realised": Decimal(125), "unrealised": Decimal(-45), "total": Decimal(80),
    }
    assert {item.raw_signal_id for item in out.raw_input_lineage} == {
        "R214", "R215", "R216",
    }
    assert owner.materialise(req) == out
