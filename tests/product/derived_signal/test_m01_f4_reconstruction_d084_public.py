"""F4 reconstructed D084: individually scoped sector and dispersion predecessors.

The public D084 score must not collapse D076, D077 and D083 into the
parent subject or into one convenient union basket. The inputs are genuine
controlled M00 projections with distinct instrument identities.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
RATIOS = {
    "SPY": Decimal("1.05"),
    "QQQ": Decimal("1.10"),
    "SMH": Decimal("1.20"),
    "SOXX": Decimal("1.30"),
    "NVDA": Decimal("1.20"),
    "AMD": Decimal("1.00"),
    "INTC": Decimal("0.90"),
}
SECTOR = ("SPY", "QQQ", "SMH", "SOXX")
CROSS = ("NVDA", "AMD", "INTC")


def _feature(signal_id: str) -> api.ScoreFeatureV1:
    return api.ScoreFeatureV1(
        signal_id,
        "component",
        (),
        "identity",
        None,
        1,
        Decimal(1),
        None,
        None,
        (),
    )


def _public(
    *,
    missing: tuple[str, str] | None = None,
    future: tuple[str, str] | None = None,
    invalid_basket: bool = False,
):
    m00 = raw.create_owner()
    bindings = []
    for seq, (instrument, ratio) in enumerate(RATIOS.items()):
        for j, (rid, val, ts) in enumerate(
            (
                ("R037", ratio * 100, NOW - timedelta(seconds=2)),
                ("R042", Decimal(100), NOW - timedelta(days=1)),
            )
        ):
            if missing == (instrument, rid):
                continue
            tag = f"{instrument}-{rid}"
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id("recon-d084-" + tag),
                    delivery_artifact_ref=raw.delivery_artifact_ref("recon-d084-" + tag),
                    source_provider=raw.provider_id("controlled-recon-d084"),
                    native_record={"metric": {rid: val}},
                    received_ts_utc=NOW + timedelta(seconds=1)
                    if future == (instrument, rid)
                    else ts,
                    ingestion_sequence=seq * 2 + j + 1,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:d084"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=ts.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                    source_variant="market",
                    subject_instrument=instrument,
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
            bindings.append(
                api.RawInputBindingV1(
                    rid,
                    api.VersionRefV1(f"recon-d084-map-{rid}", 1),
                    api.VersionRefV1("recon-d084-unit", 1),
                    instrument,
                    None,
                )
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                f"recon-d084-map-{rid}",
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-recon-d084",
                "market",
                ("metric", rid),
                "canonical",
            )
            for rid in ("R037", "R042")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "recon-d084-score",
                1,
                "P_SCORE",
                (("intercept", Decimal(0)),),
                tuple(_feature(x) for x in ("D076", "D077", "D083")),
            ),
            api.CalculationParameterSetV1("recon-d084-basic", 1, "P_BASIC", (("version", 1),)),
            api.CalculationParameterSetV1(
                "recon-d084-window", 1, "P_WINDOW", (("window_seconds", 86400),)
            ),
            api.CalculationParameterSetV1(
                "recon-d084-cross", 1, "P_CROSS_SECTION", (("basket_membership", CROSS),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "recon-d084-parent",
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                (),
            ),
            api.InputSelectionPolicyVersionV1(
                "recon-d084-tech",
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                ("SPY", "QQQ"),
            ),
            api.InputSelectionPolicyVersionV1(
                "recon-d084-semis",
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                ("SMH", "SOXX", "QQQ"),
            ),
            api.InputSelectionPolicyVersionV1(
                "recon-d084-cross-select",
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                ("NVDA", "AMD") if invalid_basket else CROSS,
            ),
            api.InputSelectionPolicyVersionV1(
                "recon-d084-leaf",
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "recon-d084-unit",
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
        "D084",
        "US_SECTOR_ROTATION",
        NOW,
        NOW,
        "recon-d084-definition",
        "recon-d084-score",
        1,
        "recon-d084-parent",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_SCORE", "recon-d084-score", 1),
            api.ParameterProfileRefV1("P_BASIC", "recon-d084-basic", 1),
            api.ParameterProfileRefV1("P_WINDOW", "recon-d084-window", 1),
            api.ParameterProfileRefV1("P_CROSS_SECTION", "recon-d084-cross", 1),
        ),
        predecessor_selection_policy_refs=(
            ("D076", api.VersionRefV1("recon-d084-tech", 1)),
            ("D077", api.VersionRefV1("recon-d084-semis", 1)),
            ("D083", api.VersionRefV1("recon-d084-cross-select", 1)),
            *tuple(
                (did, api.VersionRefV1("recon-d084-leaf", 1))
                for did in ("D071", "D072", "D073", "D074")
            ),
        ),
        raw_input_bindings=tuple(bindings),
    )
    return owner, req


def test_reconstructed_d084_three_independent_baskets_exact_score_and_lineage():
    owner, req = _public()
    out = owner.materialise(req)
    assert out is not None
    a = RATIOS
    tech = a["QQQ"].ln() - a["SPY"].ln()
    semis = (a["SMH"].ln() + a["SOXX"].ln()) / 2 - a["QQQ"].ln()
    sample = tuple(a[x].ln() for x in CROSS)
    mean = sum(sample, Decimal(0)) / Decimal(len(sample))
    dispersion = (
        sum(((x - mean) ** 2 for x in sample), Decimal(0)) / Decimal(len(sample) - 1)
    ).sqrt()
    assert out.result == tech + semis + dispersion
    parents = {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in out.predecessor_occurrence_ids
    }
    assert parents == {"D076", "D077", "D083"}
    assert {entry.observation_occurrence_id for entry in out.raw_input_lineage} == {
        f"recon-d084-{instrument}-{rid}" for instrument in RATIOS for rid in ("R037", "R042")
    }
    assert owner.materialise(req) == out


def test_reconstructed_d084_missing_required_cross_basket_member_refuses():
    owner, req = _public(missing=("INTC", "R042"))
    assert owner.materialise(req) is None


def test_reconstructed_d084_future_semis_quote_refuses():
    owner, req = _public(future=("SMH", "R037"))
    assert owner.materialise(req) is None


def test_reconstructed_d084_invalid_cross_basket_refuses():
    owner, req = _public(invalid_basket=True)
    assert owner.materialise(req) is None


def test_reconstructed_d084_missing_child_selection_ref_refuses():
    owner, req = _public()
    altered = replace(
        req,
        predecessor_selection_policy_refs=tuple(
            item for item in req.predecessor_selection_policy_refs if item[0] != "D083"
        ),
    )
    assert owner.materialise(altered) is None
