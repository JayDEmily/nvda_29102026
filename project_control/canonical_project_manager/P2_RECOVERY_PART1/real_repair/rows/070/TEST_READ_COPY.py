from __future__ import annotations

from pathlib import Path

from nvda_desk.config.parallel_risk_signal_inventory import ParallelRiskSignalInventoryService
from nvda_desk.domain.parallel_risk.unavailable_signals import (
    build_inventory_backed_unavailable_signals,
)

CONFIG = Path("config/parallel_risk_signal_inventory.v1.yaml")


def _inventory():
    return ParallelRiskSignalInventoryService(CONFIG).load_document()


def test_inventory_backed_unavailable_signals_marks_present_and_missing_expected() -> None:
    inventory = _inventory()
    result = build_inventory_backed_unavailable_signals(
        inventory=inventory,
        present_signal_ids={"source_time_utc", "scheduled_event_window_active"},
    )

    assert result.presence_by_signal_id["source_time_utc"] == "present"
    assert result.presence_by_signal_id["vix_level"] == "missing"
    missing = {entry.signal_id: entry for entry in result.missing_signal_register}
    assert missing["vix_level"].impact_on_profile == "lowers_confidence"
    assert missing["vix_level"].expected_signal_inventory_ref == (
        "parallel_risk_signal_inventory.v1#vix_level"
    )


def test_inventory_backed_deferred_rich_signals_are_unavailable_not_fabricated() -> None:
    result = build_inventory_backed_unavailable_signals(
        inventory=_inventory(),
        present_signal_ids={
            "source_time_utc",
            "scheduled_event_window_active",
            "vix_level",
            "spot_price",
            "front_dte",
            "next_dte",
        },
    )

    deferred_snapshot = {
        entry.signal_id: entry
        for entry in result.signal_snapshot
        if entry.missing_or_quarantined == "deferred"
    }
    assert "dense_options_chain" in deferred_snapshot
    assert "gamma_exposure_flip" in deferred_snapshot
    assert deferred_snapshot["dense_options_chain"].value is None
    assert deferred_snapshot["dense_options_chain"].lawful_prl_use_allowed is False
    assert "fabricated" not in str(deferred_snapshot["dense_options_chain"].value).lower()


def test_inventory_backed_excluded_signals_are_not_demanded_at_runtime() -> None:
    result = build_inventory_backed_unavailable_signals(
        inventory=_inventory(),
        present_signal_ids=set(),
    )

    assert result.presence_by_signal_id["capital_sizing_signal"] == "excluded"
    assert result.presence_by_signal_id["order_instruction_signal"] == "excluded"
    assert "capital_sizing_signal" not in {entry.signal_id for entry in result.signal_snapshot}
    assert "order_instruction_signal" not in {entry.signal_id for entry in result.missing_signal_register}


def test_inventory_backed_unavailable_not_yet_sourced_and_quarantine_states() -> None:
    result = build_inventory_backed_unavailable_signals(
        inventory=_inventory(),
        present_signal_ids={"source_time_utc", "scheduled_event_window_active", "spot_price"},
        quarantined_signal_ids={"vix_level"},
        rejected_signal_ids={"front_dte"},
    )

    states = result.presence_by_signal_id
    assert states["regime_context_packet"] == "unavailable"
    assert states["vix_level"] == "quarantined"
    assert states["front_dte"] == "rejected"
    entries = {entry.signal_id: entry for entry in result.signal_snapshot}
    assert entries["regime_context_packet"].value is None
    assert entries["vix_level"].value is None
    assert entries["front_dte"].value is None


def test_inventory_backed_unavailable_signals_are_state_of_play_not_action_language() -> None:
    result = build_inventory_backed_unavailable_signals(
        inventory=_inventory(),
        present_signal_ids=set(),
    )

    payload = "\n".join(
        [entry.model_dump_json() for entry in result.signal_snapshot]
        + [entry.model_dump_json() for entry in result.missing_signal_register]
    ).lower()
    for forbidden in [
        "buy",
        "sell",
        "fade",
        "chase",
        "size up",
        "stand down",
        "take the trade",
        "avoid the trade",
    ]:
        assert forbidden not in payload
