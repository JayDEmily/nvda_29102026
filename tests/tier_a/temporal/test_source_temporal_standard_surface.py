from __future__ import annotations

from datetime import date, datetime

import pytest

from nvda_desk.contracts.temporal import SourceTemporalStandard, build_source_temporal_payload


def test_source_temporal_standard_accepts_date_level_truth_without_fabricated_timestamp() -> None:
    carrier = SourceTemporalStandard(
        source_date=date(2026, 4, 21),
        captured_at_utc=datetime(2026, 4, 22, 0, 1),
        persisted_at_utc=datetime(2026, 4, 22, 0, 2),
        source_provider="workbook_fixture",
        time_granularity="date",
    )

    assert carrier.source_date == date(2026, 4, 21)
    assert carrier.source_time_utc is None
    assert carrier.captured_at_utc == datetime(2026, 4, 22, 0, 1)
    assert carrier.persisted_at_utc == datetime(2026, 4, 22, 0, 2)


def test_source_temporal_standard_rejects_capture_and_persistence_clock_substitution() -> None:
    with pytest.raises(
        ValueError,
        match="source temporal standard requires source_time_utc or source_date",
    ):
        SourceTemporalStandard(
            captured_at_utc=datetime(2026, 4, 22, 0, 1),
            persisted_at_utc=datetime(2026, 4, 22, 0, 2),
        )


def test_build_source_temporal_payload_infers_granularity_without_inventing_precision() -> None:
    date_payload = build_source_temporal_payload(source_date=date(2026, 4, 21))
    timestamp_payload = build_source_temporal_payload(
        source_time_utc=datetime(2026, 4, 21, 9, 31, 45)
    )

    assert date_payload["source_time_kind"] == "date"
    assert date_payload["time_granularity"] == "date"
    assert date_payload["source_time_utc"] is None
    assert timestamp_payload["source_time_kind"] == "timestamp"
    assert timestamp_payload["time_granularity"] == "timestamp"
    assert timestamp_payload["source_date"] is None


def test_source_temporal_standard_forbids_extra_runtime_authority_fields() -> None:
    with pytest.raises(ValueError):
        SourceTemporalStandard(
            source_time_utc=datetime(2026, 4, 21, 9, 31, 45),
            trade_allowed=True,
        )
