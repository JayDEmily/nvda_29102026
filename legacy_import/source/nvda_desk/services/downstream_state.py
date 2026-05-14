"""Repo-native downstream state readers.

This module binds the architecture-only downstream shells to explicit repo-native
capital, inventory, and receipt readers without encoding behavioural policy.
"""
from __future__ import annotations

from nvda_desk.schemas.downstream import (
    DownstreamRecommendationHistoryReservation,
    DownstreamStateReadResult,
    DownstreamStateSnapshot,
    DownstreamStateSource,
)
from nvda_desk.services.execution_records import ExecutionRecordsService


class DownstreamStateService:
    """Read repo-native state for downstream architecture shells."""

    def __init__(self, execution_records_service: ExecutionRecordsService):
        self._execution_records = execution_records_service

    def read(self, *, symbol: str = "NVDA", limit: int = 20) -> DownstreamStateReadResult:
        """Read repo-native capital, inventory, and receipt state."""

        capital_state = self._execution_records.latest_capital_state()
        positions = self._execution_records.list_positions(symbol=symbol, limit=limit).positions
        position_instances = self._execution_records.list_position_instances(
            symbol=symbol,
            limit=limit,
        ).position_instances
        signal_receipts = self._execution_records.list_signals(limit=limit).signal_events
        veto_receipts = self._execution_records.list_vetoes(limit=limit).veto_events
        risk_block_receipts = self._execution_records.list_risk_blocks(limit=limit).risk_block_events
        order_event_receipts = self._execution_records.list_order_events(limit=limit).order_events
        fill_event_receipts = self._execution_records.list_fill_events(limit=limit).fill_events
        reservation = self._reservation()
        return DownstreamStateReadResult(
            state_snapshot=DownstreamStateSnapshot(
                state_source=DownstreamStateSource.EXECUTION_RECORDS,
                capital_state_present=True,
                open_position_count=len([row for row in positions if row.quantity != 0]),
                position_instance_count=len(position_instances),
                signal_receipt_count=len(signal_receipts),
                veto_receipt_count=len(veto_receipts),
                risk_block_receipt_count=len(risk_block_receipts),
                order_event_count=len(order_event_receipts),
                fill_event_count=len(fill_event_receipts),
                recommendation_history_reserved=True,
                notes=[
                    "repo_native_state_attached",
                    "order_fill_history_attached",
                ],
            ),
            capital_state=capital_state,
            positions=positions,
            position_instances=position_instances,
            signal_receipts=signal_receipts,
            veto_receipts=veto_receipts,
            risk_block_receipts=risk_block_receipts,
            order_event_receipts=order_event_receipts,
            fill_event_receipts=fill_event_receipts,
            recommendation_history_reservation=reservation,
        )

    def degraded(self, *, error: Exception) -> DownstreamStateReadResult:
        """Return a truthful degraded-state receipt when repo-native state fails."""

        error_note = f"state_read_error:{type(error).__name__}"
        return DownstreamStateReadResult(
            state_snapshot=DownstreamStateSnapshot(
                state_source=DownstreamStateSource.NOT_AVAILABLE,
                capital_state_present=False,
                recommendation_history_reserved=True,
                degraded_reason=type(error).__name__,
                notes=[
                    "degraded_state_receipt_emitted",
                    error_note,
                    "no_placeholder_state_claimed",
                ],
            ),
            recommendation_history_reservation=DownstreamRecommendationHistoryReservation(
                existing_receipt_tables=[],
                future_home="downstream_recommendation_history_reader",
                notes=[
                    "recommendation_history_home_reserved",
                    "repo_native_state_read_failed",
                    error_note,
                ],
            ),
        )

    def placeholder(self) -> DownstreamStateReadResult:
        """Return the legacy placeholder-only state receipt.

        This path remains available only for older callers. Runtime should prefer
        ``degraded(...)`` so state-read failures stay explicit instead of looking
        like a neutral placeholder attachment.
        """

        return DownstreamStateReadResult(
            state_snapshot=DownstreamStateSnapshot(
                state_source=DownstreamStateSource.NOT_AVAILABLE,
                capital_state_present=False,
                recommendation_history_reserved=True,
                notes=[
                    "legacy_placeholder_only_state_receipt",
                    "runtime_should_prefer_degraded_state_receipt",
                ],
            ),
            recommendation_history_reservation=DownstreamRecommendationHistoryReservation(
                existing_receipt_tables=[],
                future_home="downstream_recommendation_history_reader",
                notes=[
                    "recommendation_history_home_reserved",
                    "placeholder_only_no_policy",
                ],
            ),
        )

    @staticmethod
    def _reservation() -> DownstreamRecommendationHistoryReservation:
        return DownstreamRecommendationHistoryReservation(
            existing_receipt_tables=[
                "module_signal_event",
                "module_veto_event",
                "risk_block_event",
                "order_intent_record",
                "order_event_record",
                "fill_event_record",
            ],
            future_home="downstream_recommendation_history_reader",
            notes=[
                "every_pass_receipt_required",
                "same_pass_loop_still_forbidden",
            ],
        )
