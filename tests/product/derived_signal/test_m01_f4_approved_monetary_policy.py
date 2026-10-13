"""Approved reference limits, joint clipping and actual comparable breach."""
from datetime import UTC, datetime
from decimal import Decimal as D
from fractions import Fraction

import pytest

from nvda_desk.derived_signal_calculation_truth import _catalogue, _stage1, api

NOW = datetime(2026, 10, 13, 9, tzinfo=UTC)
NAMES = ("delta", "gamma", "vega", "theta")
UNITS = ("shares", "shares_per_currency", "currency_per_volatility_point", "currency_per_day")


def kv(identity, value, subject="NVDA", **metadata):
    return _stage1.KernelValueV1(value, identity, NOW, NOW, subject, "derived",
                                 metadata=tuple(metadata.items()))


def nt(**values):
    return tuple(values.items())


def fixture(vector=(D(1000), D(0), D(0), D(0))):
    candidate = api.CandidateStructureContextV1(
        "candidate", 1, "managed", ("option",), ("buy",), (D(2),), D(1),
        (("option", D(5)),), (), D(10000),
    )
    live = api.LivePositionContextV1("live", 1, "position", ("option",),
                                   (D(2),), (D(100),), ("position-source",), ("state-source",))
    scope = api.RiskScopeContextV1(
        "scope", 1, "account", "account-subject", "USD", "managed", "NVDA", "live_sleeve",
        api.VersionRefV1("candidate", 1), api.VersionRefV1("live", 1), ("position-source",),
        api.VersionRefV1("membership", 1), api.VersionRefV1("risk-definition", 1),
    )
    definition = api.CalculationParameterSetV1("risk-definition", 1, "P_RULE", (
        ("risk_definition_id", "GREEK_SHOCK_ENVELOPE_V1"),
        ("risk_definition_version", "D175-REFERENCE-20261013-01"),
        ("risk_currency", "USD"), ("risk_price_shock", D(1)),
        ("risk_volatility_points_shock", D(1)), ("risk_horizon_days", D(1)),
    ))
    membership = api.CalculationParameterSetV1("membership", 1, "P_BASIC", (
        ("account_identity", "account"), ("sleeve_identity", "managed"),
        ("complete_members", ("option|2|position-source",)),
    ))
    policy = dict(definition.parameters) | dict(
        limit_policy_definition="REFERENCE_CALIBRATED_ENVELOPE_V1",
        capital_active=True, tail_active=True, stress_active=True,
        concentration_active=True, liquidity_active=True,
        capital_fraction=D(".10"), tail_fraction=D(".03"), stress_fraction=D(".06"),
        concentration_fraction=D(".20"), liquidity_fraction=D(".50"),
    )
    common = dict(currency="USD", candidate_ref=("candidate", 1),
                  scope_ref=("scope", 1), scenario_grid_ref=("grid", 1),
                  model_ref=("model", 1), option_convention_ref=("option-model", 1),
                  as_of_utc=NOW, knowledge_cutoff_utc=NOW)
    matrix = nt(**common, gross_scenario_PnL=(("down", D(-400)), ("up", D(100))),
                scenario_weights=(("down", D(".5")), ("up", D(".5"))),
                reference_greeks=tuple(zip(NAMES, vector, strict=True)),
                greek_units=tuple(zip(NAMES, UNITS, strict=True)),
                d168_occurrence_id="D168", position_source_refs=("position-source",))
    tail = nt(**common, CVaR_currency=D(200), confidence=D(".95"),
              d174_occurrence_id="D174", scenario_ids=("down", "up"))
    raw = {identity: (kv(identity, value, "account-subject", account_identity="account",
                         currency="USD", canonical_units="USD"),)
           for identity, value in zip(("R205", "R206", "R209", "R208"),
                                      (D(10000), D(3000), D(2500), D(1000)), strict=True)}
    return dict(raw=raw, derived={"D162": (kv("D162", tail),), "D174": (kv("D174", matrix),)},
                params=policy, contexts=(candidate, live, scope, definition, membership))


def ev(identity, f):
    return _stage1.evaluate_stage1_kernel(
        identity, raw_inputs=f["raw"], derived_inputs=f["derived"],
        parameter_set=api.CalculationParameterSetV1("policy", 1,
            _catalogue.catalogue_row(identity).parameter_profiles[0], tuple(f["params"].items())),
        contexts=f["contexts"], as_of_utc=NOW, knowledge_cutoff_utc=NOW,
    )


def budget(f):
    result = ev("D175", f)
    assert result is not None, "approved reference-calibrated limit is absent"
    return result.value


@pytest.mark.parametrize("changed,expected,binding", [
    ({}, 1000, "capital"), ({"tail_fraction": D(".01")}, 500, "tail"),
    ({"stress_fraction": D(".02")}, 500, "stress"),
    ({"concentration_fraction": D(".04")}, 400, "concentration"),
    ({"liquidity_fraction": D(".1")}, 250, "liquidity"),
    ({"capital_fraction": D(0)}, 0, "capital"),
])
def test_each_native_limit_maps_into_one_exact_envelope(changed, expected, binding):
    f = fixture(); f["params"].update(changed)
    b = dict(budget(f))
    assert Fraction(*b["maximum_currency_exact"]) == expected
    assert binding in b["binding_limits"]
    assert Fraction(*b["maximum_percent_risk_capital_exact"]) == Fraction(expected, 100)


@pytest.mark.parametrize("identity,value", [("R206", -10), ("R209", -1), ("R208", 12000)])
def test_negative_capacity_is_zero_not_absolute_value(identity, value):
    f = fixture(); old = f["raw"][identity][0]
    f["raw"][identity] = (kv(identity, D(value), old.subject_instrument, **dict(old.metadata)),)
    assert dict(budget(f))["maximum_currency_exact"] == (0, 1)


def test_zero_native_losses_are_nonbinding_and_inactive_is_distinct():
    f = fixture()
    tail = dict(f["derived"]["D162"][0].value);tail["CVaR_currency"] = D(-20)
    f["derived"]["D162"] = (kv("D162", tuple(tail.items())),)
    matrix = dict(f["derived"]["D174"][0].value)
    matrix["gross_scenario_PnL"] = (("down", D(0)), ("up", D(100)))
    f["derived"]["D174"] = (kv("D174", tuple(matrix.items())),)
    b = dict(budget(f));records = dict(b["active_limit_records"])
    assert dict(records["tail"])["status"] == "nonbinding_zero_measurement"
    assert dict(records["stress"])["status"] == "nonbinding_zero_measurement"
    f["params"]["tail_active"] = False
    assert dict(dict(dict(budget(f))["active_limit_records"])["tail"])["status"] == "inactive_by_policy"


@pytest.mark.parametrize("change", ["missing_flag", "bad_fraction", "wrong_account", "wrong_currency",
    "wrong_matrix", "wrong_scenarios", "missing_predecessor", "incomplete_members", "zero_coordinate"])
def test_policy_contract_refusals(change):
    f = fixture()
    if change == "missing_flag": del f["params"]["tail_active"]
    elif change == "bad_fraction": f["params"]["capital_fraction"] = D("1.01")
    elif change in {"wrong_account", "wrong_currency"}:
        metadata = dict(f["raw"]["R205"][0].metadata)
        metadata["account_identity" if change == "wrong_account" else "currency"] = "wrong"
        f["raw"]["R205"] = (kv("R205", D(10000), "account-subject", **metadata),)
    elif change in {"wrong_matrix", "wrong_scenarios"}:
        tail = dict(f["derived"]["D162"][0].value)
        tail["d174_occurrence_id" if change == "wrong_matrix" else "scenario_ids"] = "wrong"
        f["derived"]["D162"] = (kv("D162", tuple(tail.items())),)
    elif change == "missing_predecessor": del f["derived"]["D162"]
    elif change == "incomplete_members": f["contexts"] = f["contexts"][:-1]
    elif change == "zero_coordinate": f = fixture((D(0),) * 4)
    assert ev("D175", f) is None


def hedge_fixture(f):
    b = budget(f); ref = dict(b)["reference_greeks"]
    derived = {"D175": (kv("D175", b),)}
    for (name, value), identity in zip(ref, ("D181", "D182", "D183", "D184"), strict=True):
        derived[identity] = (kv(identity, value, units=dict(zip(NAMES, UNITS, strict=True))[name],
                               position_context_ref=("live", 1),
                               position_source_refs=("position-source",)),)
    return dict(raw={}, derived=derived, contexts=f["contexts"],
                params=dict(f["params"]) | {"target_bands": tuple(name + "|0|0" for name in NAMES)})


def test_four_greeks_share_one_budget_and_residual_does_not_increase():
    f = fixture((D(600), D(200), D(200), D(100))); f["params"]["capital_fraction"] = D(".04")
    hf = hedge_fixture(f);result = ev("D189", hf)
    assert result is not None
    h = dict(result.value)
    assert Fraction(*h["adjustment_risk_currency_exact"]) <= 400
    assert Fraction(*h["residual_risk_currency_exact"]) <= Fraction(*h["current_risk_currency_exact"])
    ratios = [value / dict(h["unclipped_adjustment"])[name] for name, value in h["adjustment"]]
    assert len(set(ratios)) == 1
    assert h["post_adjustment_native_loss_status"] == "requires_revaluation"


def test_theta_only_and_zero_budget():
    f = fixture((D(0), D(0), D(0), D(1000)))
    result = ev("D189", hedge_fixture(f));assert result is not None
    assert dict(dict(result.value)["adjustment"])["theta"] == D(-1000)
    f["params"]["capital_fraction"] = D(0)
    result = ev("D189", hedge_fixture(f));assert result is not None
    assert all(value == 0 for _, value in dict(result.value)["adjustment"])


@pytest.mark.parametrize("bands", [("delta|0|0",), tuple(name + "|2|1" for name in NAMES),
    ("delta|0|0", "delta|0|0", "vega|0|0", "theta|0|0")])
def test_missing_duplicate_reversed_bands_refuse(bands):
    f = hedge_fixture(fixture()); f["params"]["target_bands"] = bands
    assert ev("D189", f) is None


def action_fixture(tail_fraction=D(".03")):
    f = fixture(); f["params"]["tail_fraction"] = tail_fraction
    hf = hedge_fixture(f);hedge = ev("D189", hf);assert hedge is not None
    p = dict(f["params"]) | dict(mandatory_exit_on_invalidation=True,
        invalidation_threshold=D(".8"), invalidation_domain="score",
        mandatory_hedge_on_risk=True, modify_minimum=D(1), utility_domain="net_currency",
        exit_margin_currency=D(0))
    derived = {"D175": hf["derived"]["D175"], "D189": (kv("D189", hedge.value),),
        "D187": (kv("D187", D(".2"), units="score"),),
        "D188": (kv("D188", nt(expected_currency_PnL=D(10), currency="USD")),),
        "D190": (kv("D190", D(0), utility_domain="net_currency"),),
        "D191": (kv("D191", D(5), currency="USD"),)}
    return dict(raw={}, derived=derived, contexts=f["contexts"], params=p)


@pytest.mark.parametrize("fraction,expected", [(".04", "hold"), (".03", "hold"), (".01", "hedge")])
def test_nonzero_hedge_is_not_proof_of_breach(fraction, expected):
    f = action_fixture(D(fraction));result = ev("D192", f)
    assert result is not None and result.value == expected


def test_mandatory_exit_precedes_breach_hedge_and_utility():
    f = action_fixture(D(".01"));f["derived"]["D187"] = (kv("D187", D(".9"), units="score"),)
    result = ev("D192", f);assert result is not None and result.value == "exit"
    del f["derived"]["D188"]
    assert ev("D192", f) is None


@pytest.mark.parametrize("mutation", ["other_budget", "false_current", "missing_hold_currency", "utility_domain"])
def test_tampered_or_incomparable_action_evidence_refuses(mutation):
    f = action_fixture()
    if mutation in {"other_budget", "false_current"}:
        h = dict(f["derived"]["D189"][0].value)
        h["d175_occurrence_id" if mutation == "other_budget" else "current_risk_currency_exact"] = (
            "other" if mutation == "other_budget" else (2000, 1))
        f["derived"]["D189"] = (kv("D189", tuple(h.items())),)
    elif mutation == "missing_hold_currency": f["derived"]["D188"] = (kv("D188", nt(utility=D(1))),)
    else: f["derived"]["D190"] = (kv("D190", D(2), utility_domain="sigmoid"),)
    assert ev("D192", f) is None
