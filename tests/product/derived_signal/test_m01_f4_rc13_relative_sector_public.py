"""F4 RC13 proof: relative-sector operands require independent exact instruments.

The accepted catalogue binds D076 to D072(QQQ) minus D071(SPY), and
D077 to D073(SMH), D074(SOXX), and D072(QQQ).  A single parent request
subject is not the instrument identity of all its predecessors.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
RATIOS = {
    "SPY": Decimal("1.05"),
    "QQQ": Decimal("1.10"),
    "SMH": Decimal("1.20"),
    "SOXX": Decimal("1.30"),
    "AMD": Decimal("9.00"),
}
SELECTION = {"D071": "SPY", "D072": "QQQ", "D073": "SMH", "D074": "SOXX"}


def _public(
    derived_id: str, *, absent: tuple[str, str] | None = None,
    future: tuple[str, str] | None = None, alias_collision: bool = False,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    assert derived_id in {"D076", "D077"}
    members = ("SPY", "QQQ") if derived_id == "D076" else ("SMH", "SOXX", "QQQ")
    if alias_collision:
        members = (*members, "SPX")
    m00 = raw.create_owner()
    seq = 0
    for instrument in (*members, "AMD"):
        for label, raw_id, price, time in (
            ("current", "R037", RATIOS.get(instrument, Decimal("1.06")) * 100,
             NOW - timedelta(seconds=2)),
            ("prior", "R042", Decimal(100), NOW - timedelta(days=1)),
        ):
            if absent == (instrument, label):
                continue
            seq += 1
            oid = f"{instrument}-{label}"
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id(oid),
                    delivery_artifact_ref=raw.delivery_artifact_ref("relative-" + oid),
                    source_provider=raw.provider_id("controlled-rc13-relative"),
                    native_record={"metric": {raw_id: price}},
                    received_ts_utc=NOW + timedelta(seconds=2)
                    if future == (instrument, label) else time,
                    ingestion_sequence=seq,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("rc13:relative"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=time.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(raw_id),),
                    source_variant="market",
                    subject_instrument=instrument,
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"relative-map-{rid}", 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc13-relative", "market", ("metric", rid), "canonical",
            ) for rid in ("R037", "R042")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "relative-basic", 1, "P_BASIC", (("version", 1),)
            ),
            api.CalculationParameterSetV1(
                "relative-window", 1, "P_WINDOW", (("window_seconds", 86400),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "relative-parent", 1, ("subject_instrument",),
                timedelta(days=3), timedelta(days=3), ("true_instant",), members,
            ),
            api.InputSelectionPolicyVersionV1(
                "relative-child", 1, ("subject_instrument",),
                timedelta(days=3), timedelta(days=3), ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "relative-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    dependencies = ("D072", "D071") if derived_id == "D076" else (
        "D073", "D074", "D072"
    )
    request = api.CalculationRequestV1(
        derived_id, "US_TECH" if derived_id == "D076" else "SEMIS", NOW, NOW,
        "relative-sector-public", "relative-basic", 1, "relative-parent", 1, (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_BASIC", "relative-basic", 1),
            api.ParameterProfileRefV1("P_WINDOW", "relative-window", 1),
        ),
        predecessor_selection_policy_refs=tuple(
            (did, api.VersionRefV1("relative-child", 1)) for did in dependencies
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1(f"relative-map-{rid}", 1),
                api.VersionRefV1("relative-unit", 1), instrument, None,
            ) for instrument in members for rid in ("R037", "R042")
        ),
    )
    return owner, request


@pytest.mark.parametrize("did", ("D076", "D077"))
def test_rc13_relative_returns_use_exact_distinct_predecessor_subjects(did: str) -> None:
    owner, request = _public(did)
    out = owner.materialise(request)
    assert out is not None
    log = lambda symbol: RATIOS[symbol].ln()
    expected = log("QQQ") - log("SPY") if did == "D076" else (
        (log("SMH") + log("SOXX")) / 2 - log("QQQ")
    )
    assert out.result == expected
    required = {"SPY", "QQQ"} if did == "D076" else {"SMH", "SOXX", "QQQ"}
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        f"{member}-{stage}" for member in required for stage in ("current", "prior")
    }
    assert {owner.reads.get_derived_occurrence(pid).derived_signal_id
            for pid in out.predecessor_occurrence_ids} == (
        {"D071", "D072"} if did == "D076" else {"D072", "D073", "D074"}
    )
    assert owner.materialise(request) == out


@pytest.mark.parametrize("did,missing", (
    ("D076", ("SPY", "prior")), ("D077", ("SOXX", "prior")),
))
def test_rc13_relative_returns_refuse_missing_exact_member(did: str, missing: tuple[str, str]) -> None:
    owner, request = _public(did, absent=missing)
    assert owner.materialise(request) is None


@pytest.mark.parametrize("did,late", (
    ("D076", ("QQQ", "current")), ("D077", ("SMH", "current")),
))
def test_rc13_relative_returns_refuse_future_member(did: str, late: tuple[str, str]) -> None:
    owner, request = _public(did, future=late)
    assert owner.materialise(request) is None


def test_rc13_relative_refuses_ambiguous_market_alias() -> None:
    owner, request = _public("D076", alias_collision=True)
    assert owner.materialise(request) is None
