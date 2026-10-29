"""F4 RC06: M00-public deterministic weighted regime scores D061/D070.

Immutable P_SCORE feature schemas enumerate every accepted predecessor;
P_WINDOW history remains source-native at exact 300-second/day anchors.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
VOL_RECORDS = (
    ("R236", Decimal(21), Decimal(20)),
    ("R237", Decimal(110), Decimal(100)),
    ("R238", Decimal(18), None),
    ("R239", Decimal(19), None),
    ("R240", Decimal(23), None),
)
OVERSEAS_RECORDS = (
    ("R270", Decimal(120), Decimal(100)),
    ("R271", Decimal(110), Decimal(100)),
    ("R272", Decimal(105), Decimal(100)),
    ("R273", Decimal(95), Decimal(100)),
    ("R274", Decimal(120), Decimal(100)),
    ("R275", Decimal(110), Decimal(100)),
    ("R276", Decimal(90), Decimal(100)),
)


def _feature(did: str, component: str | None = None) -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(
        did, "component", () if component is None else (component,),
        "identity", None, 1, Decimal(1), None, None, (),
    )


def _public(
    did: str,
    *,
    missing: str | None = None,
    future_current: str | None = None,
    wrong_subject: str | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    records = VOL_RECORDS if did == "D061" else OVERSEAS_RECORDS
    if did == "D061":
        features = (
            _feature("D052", "percent_change"),
            _feature("D053", "percent_change"),
            _feature("D057", "point_difference"),
            _feature("D058", "point_difference"),
            _feature("D059", "point_difference"),
            _feature("D060"),
        )
    else:
        features = tuple(_feature(f"D{i:03d}") for i in (*range(66, 70), *range(49, 52)))
    seq = 0
    for rid, current, prior in records:
        for is_current, value in ((False, prior), (True, current)):
            if value is None:
                continue
            if missing == rid and is_current:
                continue
            anchor = (
                timedelta(days=1) if rid in {"R270", "R271", "R272", "R273"}
                else timedelta(seconds=300)
            )
            ts = NOW - timedelta(seconds=2) - (timedelta(0) if is_current else anchor)
            oid = f"regime-{rid}-{'current' if is_current else 'prior'}"
            seq += 1
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id(oid),
                    delivery_artifact_ref=raw.delivery_artifact_ref(oid),
                    source_provider=raw.provider_id("controlled-rc06"),
                    native_record={"metric": {rid: value}},
                    received_ts_utc=NOW + timedelta(seconds=3)
                    if future_current == rid and is_current else ts,
                    ingestion_sequence=seq,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("rc06:regime"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=ts.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                    source_variant="metric",
                    subject_instrument="AMD" if wrong_subject == rid else "NVDA",
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
    raw_ids = tuple(rid for rid, *_ in records)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"rc06-map-{rid}", 1, raw.RawSignalCatalogueId(rid),
                "controlled-rc06", "metric", ("metric", rid), "canonical",
            ) for rid in raw_ids
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc06-score", 1, "P_SCORE", (("intercept", Decimal(0)),), features
            ),
            api.CalculationParameterSetV1(
                "rc06-window", 1, "P_WINDOW",
                (("anchor_seconds", 300), ("anchor_days", 1)),
            ),
            api.CalculationParameterSetV1(
                "rc06-basic", 1, "P_BASIC", (("basic_version", 1),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc06-select", 1, ("subject_instrument",),
                timedelta(days=3), timedelta(days=3), ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc06-unit", 1, "canonical", "canonical",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW,
        "rc06-regime-public", "rc06-score", 1,
        "rc06-select", 1, (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "rc06-score", 1),
            api.ParameterProfileRefV1("P_WINDOW", "rc06-window", 1),
            api.ParameterProfileRefV1("P_BASIC", "rc06-basic", 1),
        ),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1(f"rc06-map-{rid}", 1),
                api.VersionRefV1("rc06-unit", 1), "NVDA", None,
            ) for rid in raw_ids
        ),
    )
    return owner, req


@pytest.mark.parametrize("did", ("D061", "D070"))
def test_rc06_public_all_declared_predecessors_and_score_schema(
    did: str,
) -> None:
    owner, req = _public(did)
    out = owner.materialise(req)
    assert out is not None
    if did == "D061":
        expected = Decimal(5) + Decimal(10) - Decimal(1) - Decimal(2) - Decimal(2) + (
            Decimal(110) / Decimal(21)
        )
        predecessors = {"D052", "D053", "D057", "D058", "D059", "D060"}
        raw_ids = {rid for rid, *_ in VOL_RECORDS}
    else:
        expected = (
            sum(
                ((curr / prior).ln() for rid, curr, prior in OVERSEAS_RECORDS[:4]),
                Decimal(0),
            )
            + Decimal(20) + Decimal(10) - Decimal(10)
        )
        predecessors = {"D066", "D067", "D068", "D069", "D049", "D050", "D051"}
        raw_ids = {rid for rid, *_ in OVERSEAS_RECORDS}
    assert out.result == expected
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    } == predecessors
    assert {entry.raw_signal_id for entry in out.raw_input_lineage} == raw_ids
    assert owner.materialise(req) == out


@pytest.mark.parametrize(("did", "rid"), (("D061", "R236"), ("D070", "R270")))
def test_rc06_public_regime_missing_required_source_refuses(did: str, rid: str) -> None:
    owner, req = _public(did, missing=rid)
    assert owner.materialise(req) is None


@pytest.mark.parametrize(("did", "rid"), (("D061", "R237"), ("D070", "R274")))
def test_rc06_public_regime_future_source_refuses(did: str, rid: str) -> None:
    owner, req = _public(did, future_current=rid)
    assert owner.materialise(req) is None


@pytest.mark.parametrize(("did", "rid"), (("D061", "R239"), ("D070", "R273")))
def test_rc06_public_regime_wrong_subject_refuses(did: str, rid: str) -> None:
    owner, req = _public(did, wrong_subject=rid)
    assert owner.materialise(req) is None
