"""Proof-first D123 official-reporting identity refusal.

The Programme Owner's 2026-10-11 instruction forbids treating the last two
received source ticks as distinct official OI reporting periods.  The two
controlled records below deliberately contain source/event and receipt times
but NO identity attesting distinct official reporting periods; 'official-v1'
is a native vintage label, not a declared reporting-period identifier.

This is an intentionally failing RED proof for the current kernel.  It must
not be 'fixed' by treating timestamp proximity or opaque vintage strings as
an official reporting-period and revision-ordering convention.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.derived_signal_calculation_truth._stage1 import (
    KernelValueV1,
    evaluate_stage1_kernel,
)

NOW = datetime(2026, 10, 11, 1, tzinfo=UTC)


def test_d123_refuses_two_ticks_without_proved_distinct_official_periods() -> None:
    exact_contract = (
        ("contract_id", "C150"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", "call"),
        ("source_provider", "controlled-native-official-oi"),
        ("source_variant", "official-oi"),
        ("revision_vintage_native", "official-v1"),
    )
    ticks = (
        KernelValueV1(
            value=Decimal(100),
            occurrence_id="tick-1",
            effective_at_utc=NOW - timedelta(days=1),
            received_ts_utc=NOW - timedelta(days=1) + timedelta(seconds=1),
            subject_instrument="NVDA",
            source_temporal_kind="true_instant",
            source_timestamp_raw=(NOW - timedelta(days=1)).isoformat(),
            metadata=exact_contract,
        ),
        KernelValueV1(
            value=Decimal(125),
            occurrence_id="tick-2",
            effective_at_utc=NOW - timedelta(minutes=1),
            received_ts_utc=NOW - timedelta(seconds=50),
            subject_instrument="NVDA",
            source_temporal_kind="true_instant",
            source_timestamp_raw=(NOW - timedelta(minutes=1)).isoformat(),
            metadata=exact_contract,
        ),
    )
    result = evaluate_stage1_kernel(
        "D123",
        raw_inputs={"R047": ticks},
        derived_inputs={},
        parameter_set=api.CalculationParameterSetV1(
            "d123-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),)
        ),
        contexts=(),
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )
    # Neither tick asserts an immutable official reporting-period identity.
    # A value of +25 would invent that two received ticks are two distinct
    # official refreshes; D123 must fail closed on this source history.
    assert result is None
