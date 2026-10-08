"""Leaf-3 proofs against the accepted Stage-1 catalogue and real kernel inputs."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import _catalogue, _stage1, api

AT = datetime(2026, 10, 8, 3, 0, tzinfo=UTC)


def kv(
    value: object,
    oid: str,
    *,
    at: datetime = AT,
    metadata: tuple[tuple[str, object], ...] = (),
    temporal: str = "derived",
) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=value,
        occurrence_id=oid,
        effective_at_utc=at,
        received_ts_utc=at,
        subject_instrument="NVDA",
        source_temporal_kind=temporal,
        metadata=metadata,
    )


def param(profile: str, **config: object) -> api.CalculationParameterSetV1:
    return api.CalculationParameterSetV1(
        context_id="leaf3-" + profile,
        version=1,
        profile=profile,
        parameters=tuple(config.items()) or (("selection_mode", "exact"),),  # type: ignore[arg-type]
    )


def evaluate(
    identity: str,
    *,
    raw: dict[str, tuple[_stage1.KernelValueV1, ...]] | None = None,
    derived: dict[str, tuple[_stage1.KernelValueV1, ...]] | None = None,
    parameters: api.CalculationParameterSetV1,
    contexts: tuple[object, ...] = (),
) -> _stage1.KernelResultV1 | None:
    return _stage1.evaluate_stage1_kernel(
        identity,
        raw_inputs=raw or {},
        derived_inputs=derived or {},
        parameter_set=parameters,
        contexts=contexts,
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )


def test_stage1_authority_census_exact_profiles_and_no_advanced_dispatch() -> None:
    rows = _catalogue.catalogue_rows()
    stage1 = tuple(row for row in rows if row.kernel_id in _stage1.STAGE1_KERNEL_IDS)
    by_kernel = Counter(row.kernel_id for row in stage1)
    assert by_kernel == {
        "K01_TIME": 10,
        "K02_ALGEBRA": 57,
        "K03_CHANGE_RETURN": 33,
        "K04_STANDARDISE_RANK": 9,
        "K05_REALIZED_RISK": 8,
        "K06_REGRESSION_DEPENDENCE": 7,
        "K07_WEIGHTED_SCORE": 24,
        "K08_RULE_BUCKET_POLICY": 24,
        "K16_STRUCTURED_ASSEMBLY": 1,
        "K17_ORDER_FLOW_IMBALANCE": 1,
    }
    assert len(stage1) == len(set(_stage1.supported_stage1_ids())) == 174
    assert tuple(row.derived_id for row in stage1) == _stage1.supported_stage1_ids()
    assert all(len(row.parameter_profiles) == 1 for row in stage1)
    for row in stage1:
        profile = row.parameter_profiles[0]
        assert f"CalculationParameterSet:{profile}" in row.typed_contexts or not any(
            item.startswith("CalculationParameterSet:") for item in row.typed_contexts
        )
        assert evaluate(row.derived_id, parameters=param("P_NOT_AUTHORISED")) is None
    for row in rows:
        if row.kernel_id.startswith(tuple(f"K{i:02d}_" for i in range(9, 16))):
            assert evaluate(row.derived_id, parameters=param(row.parameter_profiles[0])) is None


def test_d145_ofi_is_reachable_from_its_exact_catalogue_raw_dependencies() -> None:
    # The public M01 seam supplies R187/R188/R189/R190, never '__book_states__'.
    fields = {"R187": [], "R188": [], "R189": [], "R190": []}
    for oid, sec, op, side, price, size in (
        ("e1", 3, "insert", "bid", "100", "10"),
        ("e2", 2, "insert", "ask", "101", "8"),
        ("e3", 1, "update", "bid", "100", "12"),
        ("e4", 0, "update", "ask", "101", "7"),
    ):
        at = AT - timedelta(seconds=sec)
        for field, value in zip(
            ("R187", "R188", "R189", "R190"),
            (op, side, Decimal(price), Decimal(size)),
            strict=True,
        ):
            fields[field].append(kv(value, oid, at=at, temporal="true_instant"))
    result = evaluate(
        "D145",
        raw={key: tuple(reversed(values)) for key, values in fields.items()},
        parameters=param("P_OFI", window_seconds=5),
    )
    assert result is not None
    assert result.value == Decimal("3")  # +2 bid, -(-1 ask)


def test_d145_refuses_insufficient_book_state_without_fabricating_top_levels() -> None:
    assert evaluate(
        "D145",
        raw={"R187": (kv("insert", "e1"),)},
        parameters=param("P_OFI", window_seconds=5),
    ) is None


def test_d008_is_structured_with_admitted_temporal_coverage_and_skew() -> None:
    # Two exact true-instant predecessor observations and one receipt-only
    # observation: receipt-only counts as missing event time, not a timestamp.
    feature = api.ScoreFeatureV1(
        signal_id="D002", extractor="component", extractor_arguments=("age_seconds",),
        transform="bounded_ratio", transform_scale=Decimal("10"),
        orientation=-1, weight=Decimal(1), clip_min=None, clip_max=None,
        baseline_values=(),
    )
    score = api.CalculationParameterSetV1(
        context_id="quality-score", version=1, profile="P_SCORE",
        parameters=(("intercept", Decimal(0)),), score_features=(feature,),
    )
    result = evaluate(
        "D008",
        raw={"R001": (
            kv("quote", "r1", at=AT - timedelta(seconds=2), temporal="true_instant"),
            kv("quote", "r3", temporal="true_instant"),
            kv("news", "r2", temporal="receipt_only"),
        )},
        derived={
            "D001": (kv(AT - timedelta(seconds=2), "t1"), kv(AT, "t2")),
            "D002": (kv((("age_seconds", Decimal("2")),), "a1"),),
        },
        parameters=score,
    )
    assert result is not None
    values = dict(result.value)
    assert values["max_true_instant_skew_seconds"] == Decimal("2")
    assert values["event_time_coverage_fraction"] == Decimal(2) / Decimal(3)
    assert values["missing_event_time_count"] == 1
    assert Decimal(0) <= values["alignment_score"] <= Decimal(1)


def test_d155_preserves_component_units_quality_freshness_and_occurrence_id() -> None:
    component_ids = _catalogue.catalogue_row("D155").derived_dependencies
    components = {
        did: (kv(Decimal("2"), f"{did}-1", at=AT - timedelta(seconds=4), metadata=(
            ("units", "score"), ("quality", "admitted"), ("freshness", "current"),
        )),)
        for did in component_ids
    }
    result = evaluate(
        "D155",
        derived=components,
        parameters=param("P_STATE_VECTOR", component_order=component_ids),
    )
    assert result is not None
    component = result.value[0]
    assert component[0] == "D150"
    assert component[1] == Decimal("2")
    assert component[2] == "D150-1"
    assert dict(component[3])["units"] == "score"
    assert dict(component[3])["quality"] == "admitted"
    assert dict(component[3])["freshness"] == "current"


def test_d173_refuses_undeclared_neighbours_even_when_predecessor_values_exist() -> None:
    feature = api.ScoreFeatureV1(
        signal_id="D165", extractor="component", extractor_arguments=("value",),
        transform="identity", transform_scale=None, orientation=1, weight=Decimal(1),
        clip_min=None, clip_max=None, baseline_values=(),
    )
    p = api.CalculationParameterSetV1(
        context_id="score", version=1, profile="P_SCORE",
        parameters=(("intercept", Decimal(0)),), score_features=(feature,),
    )
    subject = api.CandidateStructureContextV1(
        context_id="subject", version=1, candidate_identity="A",
        leg_contract_identities=("call-a",), leg_sides=("buy",),
        leg_quantities=(Decimal(1),), quantity=Decimal(1),
        premium_assumptions=(), entry_assumptions=(), risk_capital_currency=Decimal(100),
    )
    universe = api.CandidateSetContextV1(
        context_id="universe", version=1, candidate_identities=("A", "B", "C"),
        eligibility_classes=(("A", "eligible"), ("B", "eligible"), ("C", "eligible")),
        neighbour_relations=(("A", "B"),),
    )
    derived = {"D165": (
        kv((("candidate", "A"), ("value", Decimal(10))), "a"),
        kv((("candidate", "B"), ("value", Decimal(13))), "b"),
        kv((("candidate", "C"), ("value", Decimal(99))), "c"),
    ), "D171": (kv(Decimal(1), "advice-1"),),
        "D172": (kv(Decimal(1), "advice-2"),)}
    result = evaluate("D173", derived=derived, parameters=p, contexts=(subject, universe))
    assert result is not None
    comps = dict(result.value)
    assert comps["subject_candidate"] == "A"
    assert comps["comparisons"] == (("B", Decimal("3")),)
    assert "C" not in str(result.value)
    no_neighbours = api.CandidateSetContextV1(
        context_id="universe2", version=1, candidate_identities=("A", "B", "C"),
        eligibility_classes=universe.eligibility_classes, neighbour_relations=(),
    )
    assert (
        evaluate("D173", derived=derived, parameters=p, contexts=(subject, no_neighbours))
        is None
    )
