"""Exact net-edge conversion; Stage-2 predecessors are controlled carriers only."""

from datetime import UTC, datetime
from decimal import Decimal as D

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api

NOW = datetime(2026, 10, 13, 9, tzinfo=UTC)


def named(**fields):
    return tuple(fields.items())


def k(identity, value, **metadata):
    if identity in {"D133", "D177"}:
        metadata = (
            dict(
                parameter_context_refs=tuple(
                    api.VersionRefV1(name, 1) for name in ("candidate", "order", "utility")
                ),
                convention_refs=(api.VersionRefV1("premium", 1),),
                source_knowledge_cutoff_utc=NOW,
            )
            | metadata
        )
    return _stage1.KernelValueV1(
        value, identity, NOW, NOW, "NVDA", "derived", metadata=tuple(metadata.items())
    )


def case(side="buy", edge=D(20), reserve=D(30), size=D(2), multiplier=D(100)):
    candidate = api.CandidateStructureContextV1(
        "candidate",
        1,
        "candidate-id",
        ("option",),
        (side,),
        (size,),
        D(1),
        (("option", D(5)),),
        (),
        D(1000),
    )
    order = api.OrderIntentContextV1("order", 1, side, size, "normal")
    cost = named(
        expected_fill_price=D("5.5") if side == "buy" else D("4.5"),
        signed_slippage_per_unit=D(".5"),
        slippage_bps=D(1000),
        expected_slippage_currency=size * multiplier * D(".5"),
        intended_size=size,
        multiplier=multiplier,
        side=side,
        contract_identity="option",
        decision_midpoint=D(5),
        currency="USD",
        order_intent_ref=("order", 1),
        candidate_ref=("candidate", 1),
        convention_ref=("premium", 1),
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )
    utility = named(
        net_currency_utility=edge,
        currency="USD",
        utility_domain="net_currency",
        utility_definition_ref=("utility", 1),
        candidate_ref=("candidate", 1),
        execution_reference_id="D133",
        convention_ref=("premium", 1),
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )
    params = dict(
        execution_edge_definition="EXECUTION_EDGE_CURRENCY_V1",
        risk_currency="USD",
        minimum_retained_edge_currency=reserve,
        urgency_cost_caps=("normal|0.8",),
        leg_headroom_weights=("option|1",),
        allocation_version="allocation-v1",
        side="sell" if side == "buy" else "buy",  # must never override typed intent
    )
    return dict(
        raw={"R034": D(4), "R035": D(6), "R189": D(10), "R190": D(10)},
        cost=cost,
        utility=utility,
        params=params,
        contexts=(candidate, order),
    )


def evaluate(c, did="D178"):
    raw = {
        key: (
            k(key, value, contract_id="option", currency="USD", unit_convention_ref=("premium", 1)),
        )
        for key, value in c["raw"].items()
    }
    derived = {"D133": (k("D133", c["cost"]),), "D177": (k("D177", c["utility"]),)}
    return _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs=raw,
        derived_inputs=derived,
        parameter_set=api.CalculationParameterSetV1(
            "execution-rule", 1, "P_RULE", tuple(c["params"].items())
        ),
        contexts=c["contexts"],
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )


@pytest.mark.parametrize("side,expected", [("buy", "5.45"), ("sell", "4.55")])
def test_already_net_edge_reference_and_typed_side(side, expected):
    result = evaluate(case(side))
    assert result is not None and result.value == D(expected)


@pytest.mark.parametrize("size,multiplier,expected", [(2, 50, "5.4"), (4, 100, "5.475")])
def test_option_premium_conversion_uses_exact_size_and_multiplier(size, multiplier, expected):
    result = evaluate(case(size=D(size), multiplier=D(multiplier)))
    assert result is not None and result.value == D(expected)


def test_execution_cost_and_urgency_caps_bind_independently():
    c = case(edge=D(40))
    result = evaluate(c)
    assert result is not None and result.value == D("5.5")
    c["params"]["urgency_cost_caps"] = ("normal|0.2",)
    result = evaluate(c)
    assert result is not None and result.value == D("5.2")


@pytest.mark.parametrize(
    "field,value",
    [
        ("expected_slippage_currency", D(99)),
        ("slippage_bps", D(999)),
        ("currency", "EUR"),
        ("contract_identity", "other"),
        ("intended_size", D(1)),
        ("order_intent_ref", ("order", 2)),
        ("signed_slippage_per_unit", D("-.5")),
    ],
)
def test_incompatible_execution_reference_refuses(field, value):
    c = case()
    cost = dict(c["cost"])
    cost[field] = value
    c["cost"] = tuple(cost.items())
    assert evaluate(c) is None


def test_scalar_predecessors_and_nonlinear_scores_refuse():
    c = case()
    c["cost"] = D(4)
    assert evaluate(c) is None
    c = case()
    utility = dict(c["utility"])
    utility["utility_domain"] = "sigmoid_score"
    c["utility"] = tuple(utility.items())
    assert evaluate(c) is None


def test_missing_urgency_and_impossible_retained_edge_refuse():
    c = case()
    c["params"]["urgency_cost_caps"] = ("urgent|0.5",)
    assert evaluate(c) is None
    assert evaluate(case(edge=D(-100), reserve=D(30))) is None


def test_d164_consumes_retained_currency_slippage_once():
    c = case()
    schedule = api.ExecutionCostScheduleVersionV1(
        "schedule", 1, (("fixed", D(1)),), (("exchange", D(2)),), (("multi", D(3)),), "USD"
    )

    def calculate(cost):
        return _stage1.evaluate_stage1_kernel(
            "D164",
            raw_inputs={},
            derived_inputs={"D133": (k("D133", cost),)},
            parameter_set=api.CalculationParameterSetV1("fees", 1, "P_BASIC", (("rule", "fees"),)),
            contexts=(schedule,),
            as_of_utc=NOW,
            knowledge_cutoff_utc=NOW,
        )

    result = calculate(c["cost"])
    assert result is not None and dict(result.value)["total"] == D(106)
    cost = dict(c["cost"])
    cost["currency"] = "EUR"
    assert calculate(tuple(cost.items())) is None


def test_two_legs_do_not_each_spend_the_full_retained_edge():
    c = case()
    candidate, order = c["contexts"]
    from dataclasses import replace

    candidate = replace(
        candidate,
        leg_contract_identities=("option", "other-option"),
        leg_sides=("buy", "buy"),
        leg_quantities=(D(2), D(2)),
        premium_assumptions=(("option", D(5)), ("other-option", D(5))),
    )
    c["contexts"] = (candidate, order)
    c["params"]["leg_headroom_weights"] = ("option|0.5", "other-option|0.5")
    result = evaluate(c)
    assert result is not None and result.value == D("5.475")
    c["params"]["leg_headroom_weights"] = ("option|1", "other-option|1")
    assert evaluate(c) is None


def test_foreign_quote_contract_and_convention_refuse():
    c = case()
    for changed in (
        {"contract_id": "foreign"},
        {"currency": "EUR"},
        {"unit_convention_ref": ("premium", 2)},
    ):
        raw = {
            key: (
                k(
                    key,
                    value,
                    **(
                        dict(
                            contract_id="option", currency="USD", unit_convention_ref=("premium", 1)
                        )
                        | changed
                    ),
                ),
            )
            for key, value in c["raw"].items()
        }
        result = _stage1.evaluate_stage1_kernel(
            "D178",
            raw_inputs=raw,
            derived_inputs={"D133": (k("D133", c["cost"]),), "D177": (k("D177", c["utility"]),)},
            parameter_set=api.CalculationParameterSetV1(
                "execution-rule", 1, "P_RULE", tuple(c["params"].items())
            ),
            contexts=c["contexts"],
            as_of_utc=NOW,
            knowledge_cutoff_utc=NOW,
        )
        assert result is None


def test_explicit_exit_currency_cannot_relabel_a_foreign_execution_reference():
    result = _stage1.evaluate_stage1_kernel(
        "D191",
        raw_inputs={"R034": (k("R034", D(4)),), "R035": (k("R035", D(6)),)},
        derived_inputs={
            "D133": (k("D133", named(expected_fill_price=D(5), currency="EUR")),),
            "D164": (
                k(
                    "D164",
                    named(
                        commissions=D(3), fees=D(1), multi_leg_incremental_cost=D(2), currency="USD"
                    ),
                ),
            ),
        },
        parameter_set=api.CalculationParameterSetV1(
            "exit",
            1,
            "P_BASIC",
            (("liquidation_quantity", D(2)), ("multiplier", D(100)), ("currency", "USD")),
        ),
        contexts=(),
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )
    assert result is None
