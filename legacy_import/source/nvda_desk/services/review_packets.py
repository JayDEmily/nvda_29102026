from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.elements import ColumnElement

from nvda_desk.db.models import (
    DailyPnlReport,
    EvaluationRun,
    ExperimentRun,
    FillEventRecord,
    ModuleSignalEvent,
    ModuleVetoEvent,
    OrderEventRecord,
    OrderIntentRecord,
    PositionSnapshot,
    RiskBlockEvent,
)
from nvda_desk.schemas.downstream import DownstreamArchitectureReceipt
from nvda_desk.schemas.execution_records import (
    DailyPnlReportCreate,
    DailyPnlReportPayload,
)
from nvda_desk.schemas.market import PrecursorRuntimePacket
from nvda_desk.schemas.review import (
    DailyReviewPacket,
    DownstreamArchitectureReviewSurface,
    ModuleHealthPacket,
    PromotionEvidencePacket,
    RecordCountSummary,
    ReviewFailurePacket,
)
from nvda_desk.services.events import EventsService
from nvda_desk.services.execution_records import ExecutionRecordsService


class ReviewPacketService:
    def __init__(
        self,
        session_factory: sessionmaker[Session],
        execution_records_service: ExecutionRecordsService,
        events_service: EventsService,
    ):
        self._session_factory = session_factory
        self._execution_records_service = execution_records_service
        self._events_service = events_service

    def module_health(self, module_id: str) -> ModuleHealthPacket:
        with self._session_factory() as session:
            evaluation_count = self._count(
                session, EvaluationRun, EvaluationRun.module_id == module_id
            )
            experiment_count = self._count(
                session, ExperimentRun, ExperimentRun.module_id == module_id
            )
            signal_event_count = self._count(
                session, ModuleSignalEvent, ModuleSignalEvent.module_id == module_id
            )
            veto_event_count = self._count(
                session, ModuleVetoEvent, ModuleVetoEvent.module_id == module_id
            )
            risk_block_event_count = self._count(
                session, RiskBlockEvent, RiskBlockEvent.module_id == module_id
            )
            order_event_count = self._count_order_events(session, module_id)
            fill_event_count = self._count_fill_events(session, module_id)
            position_snapshot_count = self._count_positions(session)
            last_signal_at = session.scalar(
                select(ModuleSignalEvent.requested_at)
                .where(ModuleSignalEvent.module_id == module_id)
                .order_by(desc(ModuleSignalEvent.requested_at))
                .limit(1)
            )
            last_fill_at = session.scalar(
                select(FillEventRecord.fill_ts)
                .join(
                    OrderIntentRecord,
                    OrderIntentRecord.id == FillEventRecord.order_intent_id,
                )
                .where(OrderIntentRecord.module_id == module_id)
                .order_by(desc(FillEventRecord.fill_ts))
                .limit(1)
            )
            latest_daily_pnl = session.scalar(
                select(DailyPnlReport).order_by(desc(DailyPnlReport.report_date)).limit(1)
            )
            open_positions = list(
                session.scalars(
                    select(PositionSnapshot.symbol)
                    .where(PositionSnapshot.quantity != 0)
                    .order_by(desc(PositionSnapshot.snapshot_ts))
                    .limit(20)
                )
            )
        return ModuleHealthPacket(
            module_id=module_id,
            evaluation_count=evaluation_count,
            experiment_count=experiment_count,
            latest_daily_pnl=(
                None
                if latest_daily_pnl is None
                else self._execution_records_service._to_daily_pnl_payload(latest_daily_pnl)
            ),
            record_counts=RecordCountSummary(
                signal_event_count=signal_event_count,
                veto_event_count=veto_event_count,
                risk_block_event_count=risk_block_event_count,
                order_event_count=order_event_count,
                fill_event_count=fill_event_count,
                position_snapshot_count=position_snapshot_count,
            ),
            last_signal_at=last_signal_at,
            last_fill_at=last_fill_at,
            open_position_symbols=sorted(set(open_positions)),
        )

    @staticmethod
    def render_precursor_runtime_binding(
        packet: PrecursorRuntimePacket | None,
    ) -> dict[str, object] | None:
        """Return a review-safe serialisation of the additive precursor runtime packet."""

        if packet is None:
            return None
        return packet.model_dump(mode="json")

    @staticmethod
    def render_failure_taxonomy(
        packet: ReviewFailurePacket | None,
    ) -> dict[str, object] | None:
        """Return a review-safe serialisation of the Gate 77 failure packet."""

        if packet is None:
            return None
        return packet.model_dump(mode="json")

    @staticmethod
    def render_promotion_evidence(
        packet: PromotionEvidencePacket | None,
    ) -> dict[str, object] | None:
        """Return a review-safe serialisation of Gate 77 promotion evidence."""

        if packet is None:
            return None
        return packet.model_dump(mode="json")


    @staticmethod
    def render_downstream_architecture_receipt(
        receipt: DownstreamArchitectureReceipt | None,
    ) -> DownstreamArchitectureReviewSurface | None:
        """Return a review-safe rendering of the downstream architecture receipt."""

        if receipt is None:
            return None
        return DownstreamArchitectureReviewSurface(
            policy_freeze_state=receipt.policy_freeze_state,
            deferred_domains=list(receipt.deferred_domains),
            opening_policy_status=receipt.opening_snapshot.opening_authorisation.policy_status.value,
            live_inventory_policy_status=receipt.live_inventory_snapshot.live_position_health.policy_status.value,
            notes=list(receipt.notes),
        )

    def daily_packet(self, *, report_date: date, symbol: str = "NVDA") -> DailyReviewPacket:
        account_state = self._execution_records_service.latest_capital_state()
        positions = self._execution_records_service.list_positions(
            symbol=symbol, limit=20
        ).positions
        daily_report = self._daily_report_or_zero(symbol=symbol, report_date=report_date)
        module_ids = self._active_module_ids(report_date)
        module_health = [self.module_health(module_id) for module_id in module_ids]
        recent_events = self._events_service.get_proximity(
            requested_at=datetime.combine(report_date, datetime.min.time(), tzinfo=UTC)
            + timedelta(hours=20),
            symbol=symbol,
        )
        return DailyReviewPacket(
            requested_at=datetime.now(tz=UTC),
            report_date=report_date,
            trade_count=daily_report.trade_count,
            realized_pnl=daily_report.realized_pnl,
            unrealized_pnl=daily_report.unrealized_pnl,
            account_state=account_state,
            positions=positions,
            module_health=module_health,
            recent_events=recent_events.upcoming_events + recent_events.recent_events,
        )

    def _daily_report_or_zero(
        self,
        *,
        symbol: str,
        report_date: date,
    ) -> DailyPnlReportPayload:
        reports = self._execution_records_service.list_daily_pnl(symbol=symbol, limit=20).reports
        for report in reports:
            if report.report_date == report_date:
                return report
        return self._execution_records_service.record_daily_pnl(
            DailyPnlReportCreate(
                symbol=symbol,
                report_date=report_date,
                realized_pnl=0.0,
                unrealized_pnl=0.0,
                gross_exposure=0.0,
                turnover=0.0,
                trade_count=0,
                notes=["auto_zero_report_for_review_packet"],
            )
        )

    def _active_module_ids(self, report_date: date) -> list[str]:
        start = datetime.combine(report_date, datetime.min.time(), tzinfo=UTC)
        end = start + timedelta(days=1)
        with self._session_factory() as session:
            module_ids = {
                row[0]
                for row in session.execute(
                    select(ModuleSignalEvent.module_id)
                    .where(ModuleSignalEvent.requested_at >= start)
                    .where(ModuleSignalEvent.requested_at < end)
                )
            }
            if not module_ids:
                fallback = session.scalar(
                    select(ModuleSignalEvent.module_id)
                    .order_by(desc(ModuleSignalEvent.created_at))
                    .limit(1)
                )
                if fallback is not None:
                    module_ids.add(fallback)
        return sorted(module_ids)

    def _count(self, session: Session, model: type[object], criterion: ColumnElement[bool]) -> int:
        return int(session.scalar(select(func.count()).select_from(model).where(criterion)) or 0)

    def _count_order_events(self, session: Session, module_id: str) -> int:
        return int(
            session.scalar(
                select(func.count())
                .select_from(OrderEventRecord)
                .join(
                    OrderIntentRecord,
                    OrderIntentRecord.id == OrderEventRecord.order_intent_id,
                )
                .where(OrderIntentRecord.module_id == module_id)
            )
            or 0
        )

    def _count_fill_events(self, session: Session, module_id: str) -> int:
        return int(
            session.scalar(
                select(func.count())
                .select_from(FillEventRecord)
                .join(
                    OrderIntentRecord,
                    OrderIntentRecord.id == FillEventRecord.order_intent_id,
                )
                .where(OrderIntentRecord.module_id == module_id)
            )
            or 0
        )

    def _count_positions(self, session: Session) -> int:
        return int(session.scalar(select(func.count()).select_from(PositionSnapshot)) or 0)
