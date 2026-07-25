from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.exit_close import CloseHandoffMaterial

DONOR_TRANSFORM_REQUIRED_KEYS = (
    "active_import_registry",
    "atlas_candidate_import",
    "bridge_projection_cache",
    "capital_deployment_override",
    "capital_resizing_authority",
    "carry_policy_rollover",
    "close_execution_adapter",
    "close_order_ticket",
    "closure_fill_router",
    "db_position_mutation",
    "donor_replay_cursor",
    "execution_bridge_order",
    "execution_record_snapshot",
    "exit_backtest_lane",
    "exit_policy_import_registry",
    "exit_research_signal",
    "fill_feedback_ingestion",
    "hidden_live_inventory_write",
    "historical_trace_review",
    "imported_exit_model",
    "intraday_rebalance_plan",
    "legacy_exit_runner",
    "live_broker_close_order",
    "live_inventory_patch",
    "market_source_refresh",
    "overnight_carry_decision",
    "overnight_gap_policy",
    "parallel_risk_recompute",
    "placement_authorisation_replay",
    "position_repository_write",
    "raw_ingress_snapshot",
    "research_notebook_trace",
    "review_explanation_override",
    "risk_budget_reallocation",
    "serial_candidate_rebuild",
    "source_api_poll",
    "state_reader_override",
    "stop_loss_import_registry",
    "take_profit_import_registry",
    "trace_review_mutation",
    "trailing_stop_import_registry",
    "unbounded_exit_strategy",
    "upstream_signal_refresh",
    "wire_broker_submit",
)


@pytest.mark.parametrize("donor_key", DONOR_TRANSFORM_REQUIRED_KEYS)
def test_exit_close_handoff_rejects_transform_required_donor_payloads(
    donor_key: str,
) -> None:
    with pytest.raises(ValidationError, match="forbidden authority keys"):
        CloseHandoffMaterial(
            handoff_id=f"handoff-{donor_key}",
            decision_id="decision-row043",
            position_id="position-row043",
            close_intent_preview={"nested": {donor_key: "donor-payload"}},
        )


def test_exit_close_transform_boundary_does_not_import_donor_runtime_modules() -> None:
    source = Path("src/nvda_desk/downstream/exit_close.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }

    assert not any("legacy_import" in module for module in imported_modules)
    assert "live_broker_close_order" not in source
    assert "position_repository_write" not in source
