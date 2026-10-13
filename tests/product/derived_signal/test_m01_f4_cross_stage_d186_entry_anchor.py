"""D186 compares the exact stored entry D155 carrier using explicit K07 extractors."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api
from nvda_desk.derived_signal_calculation_truth._catalogue import catalogue_row

AT = datetime(2026, 10, 12, 8, tzinfo=UTC)
_COMPONENTS = catalogue_row("D155").derived_dependencies


def _v(
    id: str,
    age: int,
    value: Decimal,
    *,
    alignment: Decimal = Decimal("0.8"),
    subject: str = "NVDA",
    missing_component: str | None = None,
    altered_unit: str | None = None,
    received_age: int | None = None,
) -> _stage1.KernelValueV1:
    when = AT - timedelta(minutes=age)
    received = AT - timedelta(minutes=received_age if received_age is not None else age)
    components = tuple(
        (
            did,
            (("alignment_score", alignment), ("missing_event_time_count", 0))
            if did == "D008"
            else value if did == "D150" else Decimal(1),
            f"{id}-{did}",
            (("units", altered_unit if altered_unit and did == "D150" else "score"),),
        )
        for did in _COMPONENTS
        if did != missing_component
    )
    return _stage1.KernelValueV1(
        value=components,
        occurrence_id=id,
        effective_at_utc=when,
        received_ts_utc=received,
        subject_instrument=subject,
        source_temporal_kind="derived",
        metadata=(("units", "similarity/feature deltas"), ("result_shape", "structured")),
    )


def _profile(
    *features: tuple[str, tuple[object, ...], Decimal, Decimal]
) -> api.CalculationParameterSetV1:
    fields: list[tuple[str, object]] = []
    for i, (did, spec, weight, scale) in enumerate(features, 1):
        fields.extend(
            ((f"similarity_feature:{i}", (did, *spec)),
             (f"similarity_weight:{i}", weight),
             (f"similarity_scale:{i}", scale))
        )
    return api.CalculationParameterSetV1("similarity", 1, "P_RULE", tuple(fields))


DEFAULT = _profile(("D150", ("component",), Decimal(1), Decimal(2)))


def _eval(history, anchor: str, profile=DEFAULT):
    ctx = api.EntryStateContextV1("entry-anchor", 1, anchor)
    return _stage1.evaluate_stage1_kernel(
        "D186",
        raw_inputs={},
        derived_inputs={"D155": history},
        parameter_set=profile,
        contexts=(ctx,),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )


def test_d186_resolves_explicit_stored_entry_id_not_undeclared_inline_payload():
    entry = _v("original-entry", 4, Decimal(10))
    current = _v("current-state", 0, Decimal(12))
    result = _eval((entry, current), entry.occurrence_id)
    assert result is not None
    assert dict(result.value)["similarity"] == Decimal("-0.5").exp()
    assert dict(result.value)["distance_squared"] == Decimal(1)
    assert dict(dict(result.value)["deltas"]) == {"1:D150:component": (Decimal(2), Decimal(1))}
    assert set(result.input_occurrence_ids) == {entry.occurrence_id, current.occurrence_id}
    assert _eval((entry, current), "nonexistent-entry") is None
    assert _eval((current,), entry.occurrence_id) is None
    assert _eval((entry, current), current.occurrence_id) is None


def test_d186_extracts_nested_scalar_using_k07_and_uses_only_selected_history():
    entry = _v("entry", 5, Decimal(10), alignment=Decimal("0.6"))
    stale = _v("stale-not-entry", 2, Decimal(100))
    current = _v("current", 0, Decimal(12), alignment=Decimal("0.8"))
    profile = _profile(
        ("D150", ("component",), Decimal("0.75"), Decimal(2)),
        ("D008", ("component", "alignment_score"), Decimal("0.25"), Decimal("0.1")),
    )
    result = _eval((entry, stale, current), "entry", profile)
    assert result is not None
    assert dict(result.value)["distance_squared"] == Decimal("1.75")
    assert result.input_occurrence_ids == ("current", "entry")
    assert dict(dict(result.value)["deltas"])["2:D008:component"] == (
        Decimal("0.2"), Decimal(2)
    )


@pytest.mark.parametrize("scenario", [
    "absent", "duplicate", "future_entry", "later_receipt", "different_subject",
    "schema_missing", "schema_unit", "future_current",
])
def test_d186_refuses_incompatible_history(scenario: str):
    entry = _v("entry", 4, Decimal(10))
    current = _v("current", 0, Decimal(12))
    if scenario == "absent":
        history = (current,)
    elif scenario == "duplicate":
        history = (entry, entry, current)
    elif scenario == "future_entry":
        history = (_v("entry", -1, Decimal(10)), current)
    elif scenario == "later_receipt":
        history = (_v("entry", 4, Decimal(10), received_age=-1), current)
    elif scenario == "different_subject":
        history = (_v("entry", 4, Decimal(10), subject="SPY"), current)
    elif scenario == "schema_missing":
        history = (entry, _v("current", 0, Decimal(12), missing_component="D132"))
    elif scenario == "schema_unit":
        history = (entry, _v("current", 0, Decimal(12), altered_unit="currency"))
    else:
        history = (entry, _v("current", -1, Decimal(12)))
    assert _eval(history, "entry") is None


@pytest.mark.parametrize("fields", [
    (),
    (("similarity_feature:1", ("D150", "component")),),
    (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal(1))),
    (("similarity_feature:2", ("D150", "component")), ("similarity_weight:2", Decimal(1)), ("similarity_scale:2", Decimal(2))),
    (("similarity_feature:1", ("D150", "invalid")), ("similarity_weight:1", Decimal(1)), ("similarity_scale:1", Decimal(2))),
    (("similarity_feature:1", ("D151", "component")), ("similarity_weight:1", Decimal(1)), ("similarity_scale:1", Decimal(2))),
    (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal("0.5")), ("similarity_scale:1", Decimal(2))),
    (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal(-1)), ("similarity_scale:1", Decimal(2))),
    (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal(1)), ("similarity_scale:1", Decimal(0))),
    (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal(1)), ("similarity_scale:1", Decimal(2)), ("similarity_scale:3", Decimal(2))),
])
def test_d186_refuses_unadmitted_feature_profiles(fields):
    parameter = api.CalculationParameterSetV1("other", 1, "P_RULE", fields or (("unrelated", 1),))
    assert _eval((_v("entry", 4, Decimal(10)), _v("current", 0, Decimal(12))), "entry", parameter) is None


def test_d186_refuses_duplicate_feature_selector():
    duplicate = _profile(
        ("D150", ("component",), Decimal("0.5"), Decimal(2)),
        ("D150", ("component",), Decimal("0.5"), Decimal(2)),
    )
    assert _eval((_v("entry", 4, Decimal(10)), _v("current", 0, Decimal(12))), "entry", duplicate) is None


def test_d186_nested_profile_is_not_admitted_by_typed_carrier():
    with pytest.raises(TypeError, match="immutable scalar"):
        api.CalculationParameterSetV1(
            "legacy", 1, "P_RULE", (("similarity_weights", (("D150", Decimal(1)),)),)
        )
