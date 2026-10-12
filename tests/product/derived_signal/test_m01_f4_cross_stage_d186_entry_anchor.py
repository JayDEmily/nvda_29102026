"""D186 typed entry-occurrence identity is a reference, not an inline vector."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import _stage1, api

AT = datetime(2026, 10, 12, 8, tzinfo=UTC)


def _v(id: str, age: int, value: Decimal) -> _stage1.KernelValueV1:
    when = AT - timedelta(minutes=age)
    return _stage1.KernelValueV1(
        value=(("x", value),),
        occurrence_id=id,
        effective_at_utc=when,
        received_ts_utc=when,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
    )


def _eval(history, anchor: str):
    p = api.CalculationParameterSetV1(
        "similarity",
        1,
        "P_RULE",
        (("similarity_weights", (("x", Decimal(1)),)), ("similarity_scales", (("x", Decimal(2)),))),
    )
    ctx = api.EntryStateContextV1("entry-anchor", 1, anchor)
    return _stage1.evaluate_stage1_kernel(
        "D186",
        raw_inputs={},
        derived_inputs={"D155": history},
        parameter_set=p,
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
    assert set(result.input_occurrence_ids) == {entry.occurrence_id, current.occurrence_id}
    assert _eval((entry, current), "nonexistent-entry") is None
    assert _eval((current,), entry.occurrence_id) is None
    assert _eval((entry, current), current.occurrence_id) is None
