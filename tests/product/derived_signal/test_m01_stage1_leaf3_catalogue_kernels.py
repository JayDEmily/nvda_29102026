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


def test_k06_pearson_correlations_refuse_zero_variance_not_substitute_zero() -> None:
    readings = tuple(
        kv(Decimal("100"), f"nvda-{i}", at=AT - timedelta(minutes=3 - i))
        for i in range(3)
    ) + tuple(
        _stage1.KernelValueV1(
            value=Decimal(i + 1), occurrence_id=f"spy-{i}",
            effective_at_utc=AT - timedelta(minutes=3 - i),
            received_ts_utc=AT, subject_instrument="SPY",
            source_temporal_kind="true_instant",
        )
        for i in range(3)
    )
    assert evaluate(
        "D082", raw={"R151": readings},
        parameters=param("P_REGRESSION", minimum_sample=3),
    ) is None


def test_k02_liquidation_requires_exact_quantity_and_multiplier() -> None:
    derived = {
        "D133": (kv((("expected_fill_price", Decimal("5")),), "fill"),),
        "D164": (kv((("commissions", Decimal("3")), ("fees", Decimal("1")),
                       ("multi_leg_incremental_cost", Decimal("2"))), "cost"),),
    }
    assert evaluate("D191", derived=derived, parameters=param("P_BASIC")) is None
    calculated = evaluate(
        "D191", derived=derived,
        parameters=param("P_BASIC", liquidation_quantity=Decimal("2"), multiplier=Decimal("100")),
    )
    assert calculated is not None and calculated.value == Decimal("994")


def test_k08_risk_quantity_refuses_implicit_uncertainty_and_liquidity_multipliers() -> None:
    derived = {"D175": (kv(Decimal("100"), "risk"),)}
    assert evaluate(
        "D176", derived=derived, parameters=param("P_RULE", risk_per_unit=Decimal("10")),
    ) is None
    calculated = evaluate(
        "D176", derived=derived,
        parameters=param("P_RULE", risk_per_unit=Decimal("10"),
                         uncertainty_multiplier=Decimal("1.25"),
                         liquidity_multiplier=Decimal("2")),
    )
    assert calculated is not None and calculated.value == 4


def test_k08_insert_delete_rates_require_versioned_window() -> None:
    for identity in ("D139", "D140"):
        assert evaluate(identity, parameters=param("P_RULE")) is None


def test_every_stage1_row_routes_once_via_its_hash_bound_kernel(monkeypatch: object) -> None:
    # Runtime branch census: inject a recorder at each kernel's unique
    # mathematical entrypoint. This proves dispatch, not numerical semantics;
    # separate live mathematical tests exercise the real implementations.
    from pytest import MonkeyPatch

    assert isinstance(monkeypatch, MonkeyPatch)
    dispatch = {
        "K01_TIME": "_eval_k01",
        "K02_ALGEBRA": "_eval_k02",
        "K03_CHANGE_RETURN": "_eval_k03",
        "K04_STANDARDISE_RANK": "_eval_k04",
        "K05_REALIZED_RISK": "_eval_k05",
        "K06_REGRESSION_DEPENDENCE": "_eval_k06",
        "K07_WEIGHTED_SCORE": "_eval_k07",
        "K08_RULE_BUCKET_POLICY": "_eval_k08",
        "K16_STRUCTURED_ASSEMBLY": "_eval_k16",
        "K17_ORDER_FLOW_IMBALANCE": "_eval_k17",
    }
    routed: list[str] = []
    for kernel, name in dispatch.items():
        def marker(*args: object, _kernel: str = kernel, **kwargs: object) -> Decimal:
            routed.append(_kernel)
            return Decimal(3)
        monkeypatch.setattr(_stage1, name, marker)
    for row in _catalogue.catalogue_rows():
        if row.kernel_id not in dispatch:
            continue
        routed.clear()
        result = evaluate(row.derived_id, parameters=param(row.parameter_profiles[0]))
        assert result is not None and result.value == Decimal(3), row.derived_id
        assert routed == [row.kernel_id], row.derived_id


def test_static_stage1_row_branches_have_explicit_implementation_markers() -> None:
    # An implementation marker is not a proof of correct arithmetic, but
    # catches a catalogue ID added without any corresponding kernel handling.
    import ast
    from pathlib import Path

    module = ast.parse(Path(_stage1.__file__).read_text(encoding="utf-8"))
    functions = {
        node.name: node for node in module.body if isinstance(node, ast.FunctionDef)
    }
    branches = {
        "K01_TIME": "_eval_k01", "K02_ALGEBRA": "_eval_k02",
        "K03_CHANGE_RETURN": "_eval_k03", "K04_STANDARDISE_RANK": "_eval_k04",
        "K06_REGRESSION_DEPENDENCE": "_eval_k06",
        "K08_RULE_BUCKET_POLICY": "_eval_k08",
        "K16_STRUCTURED_ASSEMBLY": "_eval_k16",
    }
    for row in _catalogue.catalogue_rows():
        if row.kernel_id not in branches:
            continue
        markers = {
            node.value for node in ast.walk(functions[branches[row.kernel_id]])
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        assert row.derived_id in markers, row.derived_id
