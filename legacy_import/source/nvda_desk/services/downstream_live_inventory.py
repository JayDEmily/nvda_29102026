"""Architecture-only downstream live-inventory shells."""
from __future__ import annotations

from nvda_desk.schemas.downstream import (
    CapitalRotationResult,
    CloseExecutionResult,
    DownstreamLiveInventorySnapshot,
    DownstreamPolicyStatus,
    DownstreamReadSurface,
    DownstreamStateReadResult,
    ExitDecisionResult,
    LivePositionHealthResult,
    PositionManagementResult,
)


class DownstreamLiveInventoryService:
    """Build architecture-only live-inventory shells without behaviour."""

    service_id = "downstream_live_inventory_service"

    def build_snapshot(
        self,
        *,
        state_read_result: DownstreamStateReadResult | None = None,
    ) -> DownstreamLiveInventorySnapshot:
        """Return the downstream live-inventory shell snapshot."""

        return DownstreamLiveInventorySnapshot(
            live_position_health=self._result(
                shell_name="live_position_health",
                state_read_result=state_read_result,
                reads_from=[
                    DownstreamReadSurface.POSITIONS,
                    DownstreamReadSurface.POSITION_INSTANCES,
                ],
                not_read=[
                    "health_thresholds_deferred",
                    "stop_logic_deferred",
                ],
            ),
            position_management=self._result(
                shell_name="position_management",
                state_read_result=state_read_result,
                reads_from=[DownstreamReadSurface.POSITIONS],
                not_read=[
                    "trim_add_flatten_policy_deferred",
                    "inventory_management_formula_deferred",
                ],
            ),
            capital_rotation=self._result(
                shell_name="capital_rotation",
                state_read_result=state_read_result,
                reads_from=[DownstreamReadSurface.CAPITAL_STATE],
                not_read=[
                    "capital_rotation_policy_deferred",
                    "cross_position_rotation_formula_deferred",
                ],
            ),
            exit_decision=self._result(
                shell_name="exit_decision",
                state_read_result=state_read_result,
                reads_from=[DownstreamReadSurface.POSITIONS],
                not_read=[
                    "exit_policy_deferred",
                    "profit_taking_formula_deferred",
                ],
            ),
            close_execution=self._result(
                shell_name="close_execution",
                state_read_result=state_read_result,
                reads_from=[DownstreamReadSurface.POSITIONS],
                not_read=[
                    "close_execution_policy_deferred",
                    "broker_close_handoff_deferred",
                ],
            ),
            notes=[
                "architecture_only_live_inventory_snapshot",
                "behavioural_policy_deferred_to_later_pack",
            ],
        )

    def _result(
        self,
        *,
        shell_name: str,
        state_read_result: DownstreamStateReadResult | None,
        reads_from: list[DownstreamReadSurface],
        not_read: list[str],
    ) -> LivePositionHealthResult | PositionManagementResult | CapitalRotationResult | ExitDecisionResult | CloseExecutionResult:
        base = dict(
            service_id=self.service_id,
            shell_name=shell_name,
            policy_status=(
                DownstreamPolicyStatus.STATE_ATTACHED_NO_POLICY
                if state_read_result is not None
                else DownstreamPolicyStatus.RESERVED_HOME_ONLY
            ),
            decision_owner=None,
            reads_from=reads_from if state_read_result is not None else [],
            not_read=[*not_read, "no_live_inventory_policy_authored_in_bootstrap"],
            state_snapshot=None if state_read_result is None else state_read_result.state_snapshot,
            recommendation_history_reservation=(
                None if state_read_result is None else state_read_result.recommendation_history_reservation
            ),
            notes=[f"{shell_name}_home_reserved_only"],
        )
        mapping = {
            "live_position_health": LivePositionHealthResult,
            "position_management": PositionManagementResult,
            "capital_rotation": CapitalRotationResult,
            "exit_decision": ExitDecisionResult,
            "close_execution": CloseExecutionResult,
        }
        return mapping[shell_name](**base)
