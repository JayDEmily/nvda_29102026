"""F4 proof-first: D079-D081 must share exact aligned historical M00 factor observations.

Authoritative M01 brief §5 K06: dependent D075 and market/technology/semi
factors D071/D076/D077 must all enter the same fitted, versioned OLS model.
This fixture uses controlled raw M00 observations, not injected kernel values.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 9, tzinfo=UTC)
INSTRUMENTS = ("NVDA", "SPY", "QQQ", "SMH", "SOXX")
FACTORS = (
    ("0.011", "0.002", "0.004"),
    ("-0.012", "0.003", "0.001"),
    ("0.006", "-0.004", "0.003"),
    ("-0.003", "-0.002", "-0.005"),
    ("0.019", "0.004", "-0.002"),
    ("0.007", "-0.005", "-0.003"),
    ("-0.005", "0.006", "0.005"),
)
EXPECTED = {"D079": Decimal(2), "D080": Decimal(3), "D081": Decimal(4)}


def _data(
    *,
    missing: tuple[str, int] | None = None,
    old_outlier: bool = False,
):
    m00 = raw.create_owner()
    seq = 0
    grid = (("0.003", "0.007", "-0.006"), *FACTORS) if old_outlier else FACTORS
    for name in INSTRUMENTS:
        observations = [("prior", NOW - timedelta(days=1), Decimal(100))]
        for i, (market, tech, semis) in enumerate(grid):
            m, t, s = Decimal(market), Decimal(tech), Decimal(semis)
            exponent = {
                "NVDA": Decimal("0.001")
                + 2 * m
                + 3 * t
                + 4 * s
                + (Decimal("0.08") if old_outlier and i == 0 else Decimal(0)),
                "SPY": m,
                "QQQ": m + t,
                "SMH": m + t + s,
                "SOXX": m + t + s,
            }[name]
            observations.append(
                (str(i), NOW - timedelta(minutes=len(grid) - i), 100 * exponent.exp())
            )
        for tag, stamp, price in observations:
            if tag != "prior" and missing == (name, int(tag)):
                continue
            rid = "R042" if tag == "prior" else "R037"
            seq += 1
            m00.commands.admit_raw_observation_occurrence(
                raw.RawObservationOccurrenceV1(
                    concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                    contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                    observation_occurrence_id=raw.observation_occurrence_id(
                        f"recon-reg-{name}-{tag}"
                    ),
                    delivery_artifact_ref=raw.delivery_artifact_ref(f"recon-reg-{name}-{tag}"),
                    source_provider=raw.provider_id("controlled-regression"),
                    native_record={"metric": {rid: price}},
                    received_ts_utc=stamp,
                    ingestion_sequence=seq,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("recon:regression"),
                    source_temporal_kind="true_instant",
                    source_timestamp_raw=stamp.isoformat(),
                    source_timezone_native="UTC",
                    raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                    source_variant="prices",
                    subject_instrument=name,
                    native_units="canonical",
                    revision_vintage_native="v1",
                )
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "regression-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-regression",
                "prices",
                ("metric", rid),
                "canonical",
            )
            for rid in ("R037", "R042")
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "regression-reg", 1, "P_REGRESSION", (("minimum_sample", 7), ("history_count", 7))
            ),
            api.CalculationParameterSetV1(
                "regression-window", 1, "P_WINDOW", (("window_seconds", 86400),)
            ),
            api.CalculationParameterSetV1(
                "regression-basic", 1, "P_BASIC", (("basic_version", 1),)
            ),
        ),
        input_selection_policies=tuple(
            api.InputSelectionPolicyVersionV1(
                label,
                1,
                ("subject_instrument",),
                timedelta(days=3),
                timedelta(days=3),
                ("true_instant",),
                members,
            )
            for label, members in (
                ("regression-parent", ()),
                ("regression-leaf", ()),
                ("regression-tech", ("SPY", "QQQ")),
                ("regression-semis", ("SMH", "SOXX", "QQQ")),
            )
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "regression-unit", 1, "canonical", "canonical", Decimal(1), Decimal(0)
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    bindings = tuple(
        api.RawInputBindingV1(
            rid,
            api.VersionRefV1("regression-map-" + rid, 1),
            api.VersionRefV1("regression-unit", 1),
            name,
            None,
        )
        for name in INSTRUMENTS
        for rid in ("R037", "R042")
    )
    request = api.CalculationRequestV1(
        "D079",
        "NVDA",
        NOW - timedelta(minutes=1),
        NOW - timedelta(minutes=1),
        "regression-def",
        "regression-reg",
        1,
        "regression-parent",
        1,
        (),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_REGRESSION", "regression-reg", 1),
            api.ParameterProfileRefV1("P_WINDOW", "regression-window", 1),
            api.ParameterProfileRefV1("P_BASIC", "regression-basic", 1),
        ),
        predecessor_selection_policy_refs=(
            ("D075", api.VersionRefV1("regression-leaf", 1)),
            ("D071", api.VersionRefV1("regression-leaf", 1)),
            ("D076", api.VersionRefV1("regression-tech", 1)),
            ("D077", api.VersionRefV1("regression-semis", 1)),
            *((did, api.VersionRefV1("regression-leaf", 1)) for did in ("D072", "D073", "D074")),
        ),
        raw_input_bindings=bindings,
    )
    return owner, request


def _seed_history(
    owner: api.DerivedSignalCalculationOwnerV1,
    request: api.CalculationRequestV1,
    *,
    allow_missing: bool = False,
    factor_count: int = len(FACTORS),
):
    """Materialise prior market returns through the public M00-to-M01 owner."""
    for i in range(factor_count):
        instant = NOW - timedelta(minutes=factor_count - i)
        for did, subject, members, policy in (
            ("D075", "NVDA", ("NVDA",), "regression-leaf"),
            ("D071", "SPY", ("SPY",), "regression-leaf"),
            ("D076", "US_TECH", ("SPY", "QQQ"), "regression-tech"),
            ("D077", "SEMIS", ("SMH", "SOXX", "QQQ"), "regression-semis"),
        ):
            child = replace(
                request,
                derived_signal_id=did,
                subject_instrument=subject,
                as_of_utc=instant,
                knowledge_cutoff_utc=instant,
                parameter_set_id="regression-basic"
                if did in {"D076", "D077"}
                else "regression-window",
                input_selection_policy_id=policy,
                raw_input_bindings=tuple(
                    b for b in request.raw_input_bindings if b.subject_instrument in members
                ),
            )
            out = owner.materialise(child)
            if not allow_missing:
                assert out is not None, (did, instant)


@pytest.mark.parametrize("did,expected", tuple(EXPECTED.items()))
def test_regression_public_uses_entire_aligned_model_history(did: str, expected: Decimal):
    owner, request = _data()
    _seed_history(owner, request)
    output = owner.materialise(replace(request, derived_signal_id=did))
    assert output is not None, f"{did} must have seven aligned source-derived samples"
    assert abs(output.result - expected) < Decimal("0.000000000001")
    assert {
        owner.reads.get_derived_occurrence(pid).derived_signal_id
        for pid in output.predecessor_occurrence_ids
    } == {"D075", "D071", "D076", "D077"}
    assert len(output.raw_input_lineage) >= 30
    assert owner.materialise(replace(request, derived_signal_id=did)) == output


def test_regression_refuses_missing_common_timestamp():
    owner, request = _data(missing=("SPY", 0))
    _seed_history(owner, request, allow_missing=True)
    assert owner.materialise(request) is None


def test_regression_window_excludes_earlier_outlier_outside_selected_history():
    owner, request = _data(old_outlier=True)
    _seed_history(owner, request, factor_count=len(FACTORS) + 1)
    for did, expected in EXPECTED.items():
        output = owner.materialise(replace(request, derived_signal_id=did))
        assert output is not None
        assert abs(output.result - expected) < Decimal("0.000000000001")


def test_regression_three_coefficients_share_exact_fitted_samples_and_versions():
    owner, request = _data()
    _seed_history(owner, request)
    results = [owner.materialise(replace(request, derived_signal_id=did)) for did in EXPECTED]
    assert all(item is not None for item in results)
    assert len({item.predecessor_occurrence_ids for item in results if item}) == 1
    assert len({item.raw_input_lineage for item in results if item}) == 1
    assert len({item.parameter_context_refs for item in results if item}) == 1
    assert len(results[0].predecessor_occurrence_ids) == 28
    assert len(results[0].raw_input_lineage) == 40


def test_regression_requires_explicit_versioned_sector_selection():
    owner, request = _data()
    _seed_history(owner, request)
    bad = replace(
        request,
        predecessor_selection_policy_refs=tuple(
            item for item in request.predecessor_selection_policy_refs if item[0] != "D077"
        ),
    )
    assert owner.materialise(bad) is None


def test_regression_refuses_unbound_extra_alias():
    owner, request = _data()
    _seed_history(owner, request)
    extra = api.RawInputBindingV1(
        "R037",
        api.VersionRefV1("regression-map-R037", 1),
        api.VersionRefV1("regression-unit", 1),
        "SPX",
        None,
    )
    assert (
        owner.materialise(replace(request, raw_input_bindings=(*request.raw_input_bindings, extra)))
        is None
    )
