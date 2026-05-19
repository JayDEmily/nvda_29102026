from __future__ import annotations

from nvda_desk.domain.parallel_risk.unavailable_signals import (
    build_unavailable_signal_snapshot_entry,
    build_unavailable_signal_watch_entry,
)


def test_unavailable_signal_snapshot_marks_future_signal_without_fabricated_value() -> None:
    entry = build_unavailable_signal_snapshot_entry(
        signal_id="vwap_distance",
        signal_family="market_microstructure",
        reason="typed runtime source not yet available",
        expected_signal_inventory_ref="workbook#Parallel Risk Lane Signal Inventory",
        workbook_lineage_refs=["Derived_Features_Catalog!A2:H2"],
    )

    assert entry.value is None
    assert entry.missing_or_quarantined == "missing"
    assert entry.freshness_state == "unknown"
    assert entry.lawful_prl_use_allowed is False
    assert entry.lawful_prl_use_reason == "typed_runtime_signal_unavailable"
    assert entry.workbook_lineage_refs == ["Derived_Features_Catalog!A2:H2"]


def test_unavailable_signal_watch_entry_is_state_of_play_not_action() -> None:
    entry = build_unavailable_signal_watch_entry(
        signal_id="real_gamma_exposure",
        signal_family="options_convexity",
        reason="dense options chain contract not yet available",
        expected_signal_inventory_ref="workbook#Parallel Risk Lane Signal Inventory",
    )

    assert entry.impact_on_profile == "lowers_confidence"
    assert entry.missing_reason == "dense options chain contract not yet available"
    payload = entry.model_dump_json()
    assert "buy" not in payload
    assert "sell" not in payload
    assert "hedge" not in payload
