from __future__ import annotations

from datetime import datetime, timedelta

from nvda_desk.domain.parallel_risk.freshness import build_freshness_register_entry


def test_freshness_register_marks_fresh_ageing_and_stale_with_deterministic_defaults() -> None:
    generated = datetime(2026, 5, 18, 14, 30, 0)

    fresh = build_freshness_register_entry(
        signal_id="vix_level",
        source_time_utc=generated - timedelta(seconds=30),
        generated_at_utc=generated,
    )
    ageing = build_freshness_register_entry(
        signal_id="source_time_ageing",
        source_time_utc=generated - timedelta(seconds=90),
        generated_at_utc=generated,
    )
    stale = build_freshness_register_entry(
        signal_id="source_time_stale",
        source_time_utc=generated - timedelta(seconds=150),
        generated_at_utc=generated,
    )

    assert fresh.freshness_state == "fresh"
    assert fresh.observed_age_seconds == 30
    assert fresh.max_allowed_age_seconds == 60
    assert ageing.freshness_state == "ageing"
    assert stale.freshness_state == "stale"


def test_freshness_register_unknown_when_source_or_generated_time_absent() -> None:
    entry = build_freshness_register_entry(signal_id="missing_source_time")

    assert entry.freshness_state == "unknown"
    assert entry.observed_age_seconds is None
    assert entry.impact_on_profile == "freshness_unknown_state_of_play"


def test_freshness_register_is_metadata_only_and_neutral_state_of_play() -> None:
    generated = datetime(2026, 5, 18, 14, 30, 0)
    entry = build_freshness_register_entry(
        signal_id="options_flow_snapshot",
        source_time_utc=generated - timedelta(seconds=150),
        captured_at_utc=generated - timedelta(seconds=140),
        persisted_at_utc=generated - timedelta(seconds=130),
        generated_at_utc=generated,
        source_refs=["source:options_flow_fixture"],
    )

    assert entry.freshness_state == "stale"
    assert entry.captured_at_utc == generated - timedelta(seconds=140)
    assert entry.persisted_at_utc == generated - timedelta(seconds=130)
    assert entry.source_refs == ["source:options_flow_fixture"]
    assert entry.impact_on_profile == "freshness_stale_uncertainty_contribution"
    assert "trade" not in entry.model_dump_json()
    assert "order" not in entry.model_dump_json()
