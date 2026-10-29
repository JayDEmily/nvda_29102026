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
    changed_component_type: bool = False,
    changed_outer_shape: bool = False,
    wrong_component_units: bool = False,
    wrong_outer_units: bool = False,
) -> _stage1.KernelValueV1:
    when = AT - timedelta(minutes=age)
    received = AT - timedelta(minutes=received_age if received_age is not None else age)
    components = tuple(
        (
            did,
            (("alignment_score", alignment), ("missing_event_time_count", 0))
            if did == "D008"
            else value
            if did == "D150"
            else "one"
            if changed_component_type and did == "D132"
            else Decimal(1),
            f"{id}-{did}",
            (
                (
                    "units",
                    altered_unit
                    if altered_unit and did == "D150"
                    else "wrong"
                    if wrong_component_units
                    else catalogue_row(did).units,
                ),
            ),
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
        metadata=(
            ("units", "wrong" if wrong_outer_units else catalogue_row("D155").units),
            ("result_shape", "scalar" if changed_outer_shape else "structured"),
        ),
    )


def _profile(
    *features: tuple[str, tuple[object, ...], Decimal, Decimal],
) -> api.CalculationParameterSetV1:
    fields: list[tuple[str, object]] = []
    for i, (did, spec, weight, scale) in enumerate(features, 1):
        fields.extend(
            (
                (f"similarity_feature:{i}", (did, *spec)),
                (f"similarity_weight:{i}", weight),
                (f"similarity_scale:{i}", scale),
            )
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


def test_d186_accepts_actual_d155_k16_assembly_with_canonical_units():
    """Use the genuine Stage-1 K16 assembler, not a fabricated D155 shape."""
    assembly_profile = api.CalculationParameterSetV1(
        "state-vector", 1, "P_STATE_VECTOR", (("component_order", _COMPONENTS),)
    )

    def state(occurrence_id: str, age: int, d150: Decimal) -> _stage1.KernelValueV1:
        when = AT - timedelta(minutes=age)
        components = {
            did: (
                _stage1.KernelValueV1(
                    value=d150 if did == "D150" else Decimal(1),
                    occurrence_id=f"{occurrence_id}-{did}",
                    effective_at_utc=when,
                    received_ts_utc=when,
                    subject_instrument="NVDA",
                    source_temporal_kind="derived",
                    metadata=(("units", catalogue_row(did).units),),
                ),
            )
            for did in _COMPONENTS
        }
        assembled = _stage1.evaluate_stage1_kernel(
            "D155",
            raw_inputs={},
            derived_inputs=components,
            parameter_set=assembly_profile,
            contexts=(),
            as_of_utc=when,
            knowledge_cutoff_utc=when,
        )
        assert assembled is not None
        assert assembled.result_shape == "structured"
        return _stage1.KernelValueV1(
            value=assembled.value,
            occurrence_id=occurrence_id,
            effective_at_utc=when,
            received_ts_utc=when,
            subject_instrument="NVDA",
            source_temporal_kind="derived",
            metadata=(("units", assembled.units), ("result_shape", assembled.result_shape)),
        )

    result = _eval((state("entry", 4, Decimal(10)), state("current", 0, Decimal(12))), "entry")
    assert result is not None
    assert dict(result.value)["distance_squared"] == Decimal(1)
    assert result.input_occurrence_ids == ("current", "entry")


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
    assert dict(dict(result.value)["deltas"])["2:D008:component"] == (Decimal("0.2"), Decimal(2))


@pytest.mark.parametrize(
    "scenario",
    [
        "absent",
        "duplicate",
        "future_entry",
        "later_receipt",
        "different_subject",
        "schema_missing",
        "schema_unit",
        "future_current",
        "schema_type",
        "outer_shape",
        "noncanonical_component_units_pair",
        "noncanonical_outer_units_pair",
    ],
)
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
    elif scenario == "schema_type":
        history = (entry, _v("current", 0, Decimal(12), changed_component_type=True))
    elif scenario == "outer_shape":
        history = (entry, _v("current", 0, Decimal(12), changed_outer_shape=True))
    elif scenario == "noncanonical_component_units_pair":
        history = (
            _v("entry", 4, Decimal(10), wrong_component_units=True),
            _v("current", 0, Decimal(12), wrong_component_units=True),
        )
    elif scenario == "noncanonical_outer_units_pair":
        history = (
            _v("entry", 4, Decimal(10), wrong_outer_units=True),
            _v("current", 0, Decimal(12), wrong_outer_units=True),
        )
    else:
        history = (entry, _v("current", -1, Decimal(12)))
    assert _eval(history, "entry") is None


@pytest.mark.parametrize(
    "fields",
    [
        (),
        (("similarity_feature:1", ("D150", "component")),),
        (("similarity_feature:1", ("D150", "component")), ("similarity_weight:1", Decimal(1))),
        (
            ("similarity_feature:2", ("D150", "component")),
            ("similarity_weight:2", Decimal(1)),
            ("similarity_scale:2", Decimal(2)),
        ),
        (
            ("similarity_feature:1", ("D150", "invalid")),
            ("similarity_weight:1", Decimal(1)),
            ("similarity_scale:1", Decimal(2)),
        ),
        (
            ("similarity_feature:1", ("D151", "component")),
            ("similarity_weight:1", Decimal(1)),
            ("similarity_scale:1", Decimal(2)),
        ),
        (
            ("similarity_feature:1", ("D150", "component")),
            ("similarity_weight:1", Decimal("0.5")),
            ("similarity_scale:1", Decimal(2)),
        ),
        (
            ("similarity_feature:1", ("D150", "component")),
            ("similarity_weight:1", Decimal(-1)),
            ("similarity_scale:1", Decimal(2)),
        ),
        (
            ("similarity_feature:1", ("D150", "component")),
            ("similarity_weight:1", Decimal(1)),
            ("similarity_scale:1", Decimal(0)),
        ),
        (
            ("similarity_feature:1", ("D150", "component")),
            ("similarity_weight:1", Decimal(1)),
            ("similarity_scale:1", Decimal(2)),
            ("similarity_scale:3", Decimal(2)),
        ),
    ],
)
def test_d186_refuses_unadmitted_feature_profiles(fields):
    parameter = api.CalculationParameterSetV1("other", 1, "P_RULE", fields or (("unrelated", 1),))
    assert (
        _eval((_v("entry", 4, Decimal(10)), _v("current", 0, Decimal(12))), "entry", parameter)
        is None
    )


def test_d186_refuses_duplicate_feature_selector():
    duplicate = _profile(
        ("D150", ("component",), Decimal("0.5"), Decimal(2)),
        ("D150", ("component",), Decimal("0.5"), Decimal(2)),
    )
    assert (
        _eval((_v("entry", 4, Decimal(10)), _v("current", 0, Decimal(12))), "entry", duplicate)
        is None
    )


def test_d186_nested_profile_is_not_admitted_by_typed_carrier():
    with pytest.raises(TypeError, match="immutable scalar"):
        api.CalculationParameterSetV1(
            "legacy", 1, "P_RULE", (("similarity_weights", (("D150", Decimal(1)),)),)
        )
