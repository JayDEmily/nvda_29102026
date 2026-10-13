"""Cross-stage own-kernel checks, with controlled Stage-2 predecessor values.

The controlled values are not evidence of Stage-2 integration or full graph reachability.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal as D

from nvda_desk.derived_signal_calculation_truth import _catalogue, _stage1, api

NOW = datetime(2026, 10, 12, 8, tzinfo=UTC)


def kv(did, value, *, mins=0, units=()):
    when = NOW - timedelta(minutes=mins)
    return _stage1.KernelValueV1(
        value=value,
        occurrence_id=f"{did}-{mins}",
        effective_at_utc=when,
        received_ts_utc=when,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
        metadata=units,
    )


def evaluate(did, derived, *, params=(), contexts=()):
    row = _catalogue.catalogue_row(did)
    parameter = api.CalculationParameterSetV1(
        f"remain-{did}",
        1,
        row.parameter_profiles[0],
        tuple(params) or (("selection_mode", "exact"),),
    )
    return _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs={},
        derived_inputs=derived,
        parameter_set=parameter,
        contexts=contexts,
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )


def test_d155_exact_canonical_state_components_and_lineage():
    ids = _catalogue.catalogue_row("D155").derived_dependencies
    components = {
        did: (kv(did, D(i + 1), units=(("units", "score"),)),) for i, did in enumerate(ids)
    }
    result = evaluate("D155", components, params=(("component_order", ids),))
    assert result is not None and len(result.value) == len(ids)
    assert tuple(x[0] for x in result.value) == ids
    assert set(result.input_occurrence_ids) == {f"{did}-0" for did in ids}
    assert evaluate("D155", {}, params=(("component_order", ids),)) is None


def test_d156_ridge_dependence_uses_full_versioned_state_history():
    states = (
        kv("D155", (("x", D(1)), ("y", D(1))), mins=3),
        kv("D155", (("x", D(2)), ("y", D(3))), mins=2),
        kv("D155", (("x", D(4)), ("y", D(2))), mins=1),
    )
    prior = kv("D082", D("0.2"))
    result = evaluate(
        "D156", {"D155": states, "D082": (prior,)}, params=(("ridge_coefficient", D("0.1")),)
    )
    assert result is not None
    named = dict(result.value)
    assert len(named["partial_correlation_matrix"]) == 2
    assert len(result.input_occurrence_ids) == 4
    assert (
        evaluate(
            "D156",
            {"D155": states[:1], "D082": (prior,)},
            params=(("ridge_coefficient", D("0.1")),),
        )
        is None
    )


def test_d167_candidate_set_eligibility_and_exact_tie_order():
    context = api.CandidateSetContextV1(
        "candidates",
        1,
        ("A", "B"),
        (("A", "eligible"), ("B", "eligible")),
        (),
    )
    flags = (
        kv("D166", (("candidate", "A"), ("value", True))),
        kv("D166", (("candidate", "B"), ("value", True)), mins=1),
    )
    values = (
        kv("D165", (("candidate", "A"), ("value", D(4)))),
        kv("D165", (("candidate", "B"), ("value", D(7))), mins=1),
    )
    result = evaluate("D167", {"D166": flags, "D165": values}, contexts=(context,))
    assert result is not None and result.value == "B"
    assert set(result.input_occurrence_ids) == {x.occurrence_id for x in flags + values}
    assert evaluate("D167", {"D166": flags}, contexts=(context,)) is None


def test_d190_modify_utility_uses_exact_candidate_set():
    context = api.CandidateSetContextV1(
        "candidates",
        1,
        ("A", "B"),
        (("A", "eligible"), ("B", "eligible")),
        (),
    )
    values = (
        kv("D165", (("candidate", "A"), ("value", D(6)))),
        kv("D165", (("candidate", "B"), ("value", D(8))), mins=1),
    )
    result = evaluate(
        "D190",
        {"D188": (kv("D188", (("utility", D(3)),)),), "D165": values},
        contexts=(context,),
    )
    assert result is not None and result.value == D(5)
    assert (
        evaluate("D190", {"D188": (kv("D188", (("utility", D(3)),)),)}, contexts=(context,)) is None
    )


def test_d192_fixed_action_order_from_controlled_values():
    from .test_m01_f4_approved_monetary_policy import action_fixture, ev, kv
    f = action_fixture()
    f["derived"]["D190"] = (kv("D190", D(4), utility_domain="net_currency"),)
    f["params"]["modify_minimum"] = D(3)
    result = ev("D192", f)
    assert result is not None and result.value == "modify"
    assert set(result.input_occurrence_ids) == set(f["derived"])
