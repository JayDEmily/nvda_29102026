"""Bounded exit/close contracts for row 5.14."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ExitCloseAction = Literal["hold", "trim", "close"]
ExitCloseState = Literal["hold", "trim_ready", "close_ready", "blocked"]

EXIT_CLOSE_FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "active_import_registry",
        "atlas_candidate_import",
        "bridge_projection_cache",
        "broker_order_id",
        "broker_execution",
        "capital_deployment_override",
        "capital_resizing_authority",
        "capital_sizing",
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
        "external_source_ingress",
        "fill_feedback_ingestion",
        "hidden_live_inventory_write",
        "historical_trace_review",
        "imported_exit_model",
        "intraday_rebalance_plan",
        "legacy_exit_runner",
        "live_broker_close_order",
        "live_inventory_patch",
        "live_order_placement",
        "market_source_refresh",
        "new_candidate",
        "order_execution",
        "overnight_carry_decision",
        "overnight_gap_policy",
        "parallel_risk_recompute",
        "placement_authorisation_replay",
        "portfolio_rebalance",
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
    }
)


def find_forbidden_exit_close_authority_keys(value: Any) -> list[str]:
    """Return forbidden authority-key names found anywhere in a nested payload."""

    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                key_text = str(key)
                if key_text in EXIT_CLOSE_FORBIDDEN_AUTHORITY_KEYS:
                    found.add(key_text)
                walk(child)
        elif isinstance(node, (list, tuple, set)):
            for child in node:
                walk(child)

    walk(value)
    return sorted(found)


def _fingerprint(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ExitCloseInputTrace(BaseModel):
    """Trace proving exit/close consumed admitted downstream state only."""

    model_config = ConfigDict(extra="forbid")

    live_inventory_receipt_id: str = Field(min_length=1)
    position_id: str = Field(min_length=1)
    playbook_metadata_receipt_ids: tuple[str, ...] = Field(default_factory=tuple)
    placement_readiness_id: str = Field(min_length=1)
    capital_deployment_receipt_id: str = Field(min_length=1)
    parallel_risk_packet_id: str = Field(min_length=1)
    close_policy_id: str = Field(min_length=1)
    consumed_inputs: tuple[str, ...] = Field(
        default=(
            "live_inventory_snapshot",
            "playbook_metadata_receipts",
            "placement_readiness_result",
            "capital_deployment_receipt",
            "parallel_risk_packet",
            "bounded_close_policy",
        )
    )
    context: dict[str, Any] = Field(default_factory=dict)

    @field_validator("context")
    @classmethod
    def _reject_hidden_authority_keys(cls, value: dict[str, Any]) -> dict[str, Any]:
        forbidden = find_forbidden_exit_close_authority_keys(value)
        if forbidden:
            raise ValueError(
                "exit/close input trace contains forbidden authority keys: " + ", ".join(forbidden)
            )
        return value


class ExitClosePolicyDecision(BaseModel):
    """Bounded exit-policy decision without broker execution."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(min_length=1)
    position_id: str = Field(min_length=1)
    requested_action: ExitCloseAction
    exit_state: ExitCloseState
    trigger_ids: tuple[str, ...] = Field(default_factory=tuple)
    blocked_reasons: tuple[str, ...] = Field(default_factory=tuple)
    input_trace: ExitCloseInputTrace
    broker_execution_opened: bool = False
    live_inventory_mutated: bool = False
    capital_sizing_recomputed: bool = False

    @model_validator(mode="after")
    def _validate_state_consistency(self) -> "ExitClosePolicyDecision":
        expected_state = {
            "hold": "hold",
            "trim": "trim_ready",
            "close": "close_ready",
        }[self.requested_action]
        if self.blocked_reasons:
            if self.exit_state != "blocked":
                raise ValueError("blocked exit/close decisions must use exit_state='blocked'")
        elif self.exit_state != expected_state:
            raise ValueError("exit_state must match requested_action when not blocked")
        if self.broker_execution_opened:
            raise ValueError("exit/close policy decision must not open broker execution")
        if self.live_inventory_mutated:
            raise ValueError("exit/close policy decision must not mutate live inventory")
        if self.capital_sizing_recomputed:
            raise ValueError("exit/close policy decision must not recompute capital sizing")
        return self


class CloseHandoffMaterial(BaseModel):
    """Protocol-only close handoff material for a future broker boundary."""

    model_config = ConfigDict(extra="forbid")

    handoff_id: str = Field(min_length=1)
    decision_id: str = Field(min_length=1)
    position_id: str = Field(min_length=1)
    close_intent_preview: dict[str, Any] = Field(default_factory=dict)
    broker_boundary_mode: str = "protocol_only"
    broker_protocol_only: bool = True
    execution_allowed: bool = False
    live_order_placement_opened: bool = False

    @model_validator(mode="after")
    def _validate_protocol_only(self) -> "CloseHandoffMaterial":
        if self.broker_boundary_mode != "protocol_only":
            raise ValueError("close handoff may use broker_boundary_mode='protocol_only' only")
        if (
            not self.broker_protocol_only
            or self.execution_allowed
            or self.live_order_placement_opened
        ):
            raise ValueError("close handoff must remain non-executing protocol-only material")
        forbidden = find_forbidden_exit_close_authority_keys(self.close_intent_preview)
        if forbidden:
            raise ValueError(
                "close handoff preview contains forbidden authority keys: " + ", ".join(forbidden)
            )
        return self


class ExitCloseReceipt(BaseModel):
    """Receipt tying one exit/close decision to replayable position-closure evidence."""

    model_config = ConfigDict(extra="forbid")

    receipt_id: str = Field(min_length=1)
    decision: ExitClosePolicyDecision
    input_trace: ExitCloseInputTrace
    close_handoff: CloseHandoffMaterial | None = None
    emitted_output: dict[str, Any] = Field(default_factory=dict)
    position_closure_replay_fingerprint: str
    broker_execution_opened: bool = False
    live_inventory_mutated: bool = False

    @model_validator(mode="after")
    def _validate_receipt_boundary(self) -> "ExitCloseReceipt":
        if self.broker_execution_opened:
            raise ValueError("exit/close receipt must not open broker execution")
        if self.live_inventory_mutated:
            raise ValueError("exit/close receipt must not mutate live inventory")
        if self.input_trace != self.decision.input_trace:
            raise ValueError("exit/close receipt input_trace must match decision input_trace")
        forbidden = find_forbidden_exit_close_authority_keys(self.emitted_output)
        if forbidden:
            raise ValueError(
                "exit/close emitted output contains forbidden authority keys: "
                + ", ".join(forbidden)
            )
        return self


def fingerprint_exit_close_replay(
    *,
    decision: ExitClosePolicyDecision,
    close_handoff: CloseHandoffMaterial | None = None,
) -> str:
    """Return deterministic replay fingerprint for a bounded exit/close result."""

    return _fingerprint(
        {
            "decision": decision.model_dump(mode="json"),
            "close_handoff": close_handoff.model_dump(mode="json") if close_handoff else None,
        }
    )
