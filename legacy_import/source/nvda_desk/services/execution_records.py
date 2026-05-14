from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, cast

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import (
    Bar1m,
    CapitalStateSnapshot,
    DailyPnlReport,
    FillEventRecord,
    Instrument,
    ModuleSignalEvent,
    ModuleVetoEvent,
    OrderEventRecord,
    OrderIntentRecord,
    PositionInstanceSnapshot,
    PositionSnapshot,
    RiskBlockEvent,
)
from nvda_desk.schemas.execution_records import (
    BrokerFillEventListResponse,
    BrokerFillEventPayload,
    BrokerOrderEventListResponse,
    BrokerOrderEventPayload,
    BrokerOrderPayload,
    BrokerPaperOrderInput,
    CapitalStateSnapshotPayload,
    DailyPnlReportCreate,
    DailyPnlReportListResponse,
    DailyPnlReportPayload,
    ModuleSignalEventCreate,
    ModuleSignalEventListResponse,
    ModuleSignalEventPayload,
    ModuleVetoEventCreate,
    ModuleVetoEventListResponse,
    ModuleVetoEventPayload,
    PositionInstanceSnapshotListResponse,
    PositionInstanceSnapshotPayload,
    PositionSnapshotListResponse,
    PositionSnapshotPayload,
    RiskBlockEventCreate,
    RiskBlockEventListResponse,
    RiskBlockEventPayload,
)


class ExecutionRecordsService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def record_signal(self, payload: ModuleSignalEventCreate) -> ModuleSignalEventPayload:
        with self._session_factory() as session:
            row = ModuleSignalEvent(
                symbol=payload.symbol,
                module_id=payload.module_id,
                requested_at=self._aware(payload.requested_at),
                signal_code=payload.signal_code,
                direction=payload.direction,
                score=Decimal(str(payload.score)),
                payload_json=json.dumps(payload.payload),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_signal_payload(row)

    def list_signals(
        self, module_id: str | None = None, limit: int = 20
    ) -> ModuleSignalEventListResponse:
        with self._session_factory() as session:
            stmt = select(ModuleSignalEvent)
            if module_id:
                stmt = stmt.where(ModuleSignalEvent.module_id == module_id)
            rows = list(
                session.scalars(stmt.order_by(desc(ModuleSignalEvent.created_at)).limit(limit))
            )
        return ModuleSignalEventListResponse(
            signal_events=[self._to_signal_payload(row) for row in rows]
        )

    def record_veto(self, payload: ModuleVetoEventCreate) -> ModuleVetoEventPayload:
        with self._session_factory() as session:
            row = ModuleVetoEvent(
                symbol=payload.symbol,
                module_id=payload.module_id,
                requested_at=self._aware(payload.requested_at),
                veto_code=payload.veto_code,
                reason=payload.reason,
                payload_json=json.dumps(payload.payload),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_veto_payload(row)

    def list_vetoes(
        self, module_id: str | None = None, limit: int = 20
    ) -> ModuleVetoEventListResponse:
        with self._session_factory() as session:
            stmt = select(ModuleVetoEvent)
            if module_id:
                stmt = stmt.where(ModuleVetoEvent.module_id == module_id)
            rows = list(
                session.scalars(stmt.order_by(desc(ModuleVetoEvent.created_at)).limit(limit))
            )
        return ModuleVetoEventListResponse(veto_events=[self._to_veto_payload(row) for row in rows])

    def record_risk_block(self, payload: RiskBlockEventCreate) -> RiskBlockEventPayload:
        with self._session_factory() as session:
            row = RiskBlockEvent(
                symbol=payload.symbol,
                module_id=payload.module_id,
                requested_at=self._aware(payload.requested_at),
                linked_risk_decision_id=payload.linked_risk_decision_id,
                reason_codes_json=json.dumps(payload.reason_codes),
                payload_json=json.dumps(payload.payload),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_risk_block_payload(row)

    def list_risk_blocks(
        self, module_id: str | None = None, limit: int = 20
    ) -> RiskBlockEventListResponse:
        with self._session_factory() as session:
            stmt = select(RiskBlockEvent)
            if module_id:
                stmt = stmt.where(RiskBlockEvent.module_id == module_id)
            rows = list(
                session.scalars(stmt.order_by(desc(RiskBlockEvent.created_at)).limit(limit))
            )
        return RiskBlockEventListResponse(
            risk_block_events=[self._to_risk_block_payload(row) for row in rows]
        )

    def place_paper_order(self, payload: BrokerPaperOrderInput) -> BrokerOrderPayload:
        with self._session_factory() as session:
            requested_at = self._aware(payload.requested_at)
            client_order_ref = (
                f"paper-{int(requested_at.timestamp())}-{payload.symbol.lower()}-{payload.side}"
            )
            intent = OrderIntentRecord(
                symbol=payload.symbol,
                module_id=payload.module_id,
                requested_at=requested_at,
                side=payload.side,
                quantity=Decimal(str(payload.quantity)),
                order_type=payload.order_type,
                limit_price=Decimal(str(payload.limit_price)),
                position_instance_ref=payload.position_instance_ref,
                setup_variant_id=payload.setup_variant_id,
                execution_expression_id=payload.execution_expression_id,
                tradable_expression_family=payload.tradable_expression_family,
                lifecycle_state=payload.lifecycle_state,
                lifecycle_action=payload.lifecycle_action,
                current_position_size_pct=self._decimal_or_none(payload.current_position_size_pct),
                carry_state_eligible=payload.carry_state_eligible,
                hard_flat_required=payload.hard_flat_required,
                client_order_ref=client_order_ref,
                status="filled",
                payload_json=json.dumps(payload.payload),
            )
            session.add(intent)
            session.flush()
            session.add(
                OrderEventRecord(
                    order_intent_id=intent.id,
                    event_ts=requested_at,
                    status="submitted",
                    detail="offline_paper_submit",
                    payload_json=json.dumps({"client_order_ref": client_order_ref}),
                )
            )
            session.add(
                OrderEventRecord(
                    order_intent_id=intent.id,
                    event_ts=requested_at,
                    status="filled",
                    detail="offline_paper_fill",
                    payload_json=json.dumps({"fill_price": payload.limit_price}),
                )
            )
            quantity = Decimal(str(payload.quantity))
            fill_price = Decimal(str(payload.limit_price))
            notional = quantity * fill_price
            session.add(
                FillEventRecord(
                    order_intent_id=intent.id,
                    fill_ts=requested_at,
                    quantity=quantity,
                    fill_price=fill_price,
                    notional=notional,
                )
            )
            self._derive_position(
                session,
                payload.symbol,
                payload.side,
                quantity,
                fill_price,
                requested_at,
            )
            self._derive_position_instance(
                session,
                payload=payload,
                side=payload.side,
                quantity=quantity,
                fill_price=fill_price,
                snapshot_ts=requested_at,
            )
            session.flush()
            capital = self._derive_capital_state(session, payload.side, notional, requested_at)
            session.commit()
            return BrokerOrderPayload(
                order_intent_id=intent.id,
                client_order_ref=client_order_ref,
                status="filled",
                filled_quantity=float(quantity),
                average_fill_price=float(fill_price),
                cash_after=float(capital.cash),
                equity_after=float(capital.equity),
                gross_exposure_after=float(capital.gross_exposure),
            )

    def list_order_events(self, limit: int = 20) -> BrokerOrderEventListResponse:
        with self._session_factory() as session:
            rows = list(
                session.scalars(
                    select(OrderEventRecord)
                    .order_by(desc(OrderEventRecord.created_at))
                    .limit(limit)
                )
            )
        return BrokerOrderEventListResponse(
            order_events=[self._to_order_event_payload(row) for row in rows]
        )

    def list_fill_events(self, limit: int = 20) -> BrokerFillEventListResponse:
        with self._session_factory() as session:
            rows = list(
                session.scalars(select(FillEventRecord).order_by(desc(FillEventRecord.created_at)).limit(limit))
            )
        return BrokerFillEventListResponse(
            fill_events=[self._to_fill_event_payload(row) for row in rows]
        )

    def list_positions(
        self, symbol: str | None = None, limit: int = 20
    ) -> PositionSnapshotListResponse:
        with self._session_factory() as session:
            stmt = select(PositionSnapshot)
            if symbol:
                stmt = stmt.where(PositionSnapshot.symbol == symbol)
            rows = list(
                session.scalars(stmt.order_by(desc(PositionSnapshot.snapshot_ts)).limit(limit))
            )
        return PositionSnapshotListResponse(
            positions=[self._to_position_payload(row) for row in rows]
        )

    def list_position_instances(
        self,
        *,
        symbol: str | None = None,
        position_instance_ref: str | None = None,
        limit: int = 20,
    ) -> PositionInstanceSnapshotListResponse:
        with self._session_factory() as session:
            stmt = select(PositionInstanceSnapshot)
            if symbol:
                stmt = stmt.where(PositionInstanceSnapshot.symbol == symbol)
            if position_instance_ref:
                stmt = stmt.where(PositionInstanceSnapshot.position_instance_ref == position_instance_ref)
            rows = list(
                session.scalars(
                    stmt.order_by(
                        desc(PositionInstanceSnapshot.snapshot_ts),
                        desc(PositionInstanceSnapshot.created_at),
                    )
                )
            )
        latest_by_ref: list[PositionInstanceSnapshot] = []
        seen: set[str] = set()
        for row in rows:
            if row.position_instance_ref in seen:
                continue
            seen.add(row.position_instance_ref)
            latest_by_ref.append(row)
            if len(latest_by_ref) >= limit:
                break
        return PositionInstanceSnapshotListResponse(
            position_instances=[self._to_position_instance_payload(row) for row in latest_by_ref]
        )

    def latest_capital_state(self) -> CapitalStateSnapshotPayload:
        with self._session_factory() as session:
            row = session.scalar(
                select(CapitalStateSnapshot)
                .order_by(desc(CapitalStateSnapshot.snapshot_ts))
                .limit(1)
            )
            if row is None:
                row = CapitalStateSnapshot(
                    snapshot_ts=datetime.now(tz=UTC),
                    cash=Decimal("100000.000000"),
                    equity=Decimal("100000.000000"),
                    buying_power=Decimal("100000.000000"),
                    gross_exposure=Decimal("0.000000"),
                    net_exposure=Decimal("0.000000"),
                    source="broker_offline",
                )
                session.add(row)
                session.commit()
                session.refresh(row)
        return self._to_capital_payload(row)

    def record_daily_pnl(self, payload: DailyPnlReportCreate) -> DailyPnlReportPayload:
        with self._session_factory() as session:
            row = session.scalar(
                select(DailyPnlReport)
                .where(DailyPnlReport.symbol == payload.symbol)
                .where(DailyPnlReport.report_date == payload.report_date)
            )
            if row is None:
                row = DailyPnlReport(
                    symbol=payload.symbol,
                    report_date=payload.report_date,
                    realized_pnl=Decimal(str(payload.realized_pnl)),
                    unrealized_pnl=Decimal(str(payload.unrealized_pnl)),
                    gross_exposure=Decimal(str(payload.gross_exposure)),
                    turnover=Decimal(str(payload.turnover)),
                    trade_count=payload.trade_count,
                    notes_json=json.dumps(payload.notes),
                )
                session.add(row)
            else:
                row.realized_pnl = Decimal(str(payload.realized_pnl))
                row.unrealized_pnl = Decimal(str(payload.unrealized_pnl))
                row.gross_exposure = Decimal(str(payload.gross_exposure))
                row.turnover = Decimal(str(payload.turnover))
                row.trade_count = payload.trade_count
                row.notes_json = json.dumps(payload.notes)
            session.commit()
            session.refresh(row)
            return self._to_daily_pnl_payload(row)

    def list_daily_pnl(
        self, symbol: str | None = None, limit: int = 20
    ) -> DailyPnlReportListResponse:
        with self._session_factory() as session:
            stmt = select(DailyPnlReport)
            if symbol:
                stmt = stmt.where(DailyPnlReport.symbol == symbol)
            rows = list(
                session.scalars(stmt.order_by(desc(DailyPnlReport.report_date)).limit(limit))
            )
        return DailyPnlReportListResponse(reports=[self._to_daily_pnl_payload(row) for row in rows])

    def _derive_position(
        self,
        session: Session,
        symbol: str,
        side: str,
        quantity: Decimal,
        fill_price: Decimal,
        snapshot_ts: datetime,
    ) -> None:
        prior = session.scalar(
            select(PositionSnapshot)
            .where(PositionSnapshot.symbol == symbol)
            .order_by(desc(PositionSnapshot.snapshot_ts))
            .limit(1)
        )
        prior_qty = prior.quantity if prior is not None else Decimal("0")
        prior_avg = prior.average_price if prior is not None else fill_price
        signed_qty = quantity if side == "buy" else -quantity
        new_qty = prior_qty + signed_qty
        avg_price = self._roll_average_price(
            prior_qty=prior_qty,
            prior_avg=prior_avg,
            side=side,
            quantity=quantity,
            fill_price=fill_price,
            new_qty=new_qty,
        )
        market_price = self._latest_price(session, symbol) or fill_price
        market_value = new_qty * market_price
        unrealized = (market_price - avg_price) * new_qty if new_qty != 0 else Decimal("0")
        session.add(
            PositionSnapshot(
                symbol=symbol,
                snapshot_ts=snapshot_ts,
                quantity=new_qty,
                average_price=avg_price,
                market_price=market_price,
                market_value=market_value,
                unrealized_pnl=unrealized,
                source="broker_offline",
            )
        )

    def _derive_position_instance(
        self,
        session: Session,
        *,
        payload: BrokerPaperOrderInput,
        side: str,
        quantity: Decimal,
        fill_price: Decimal,
        snapshot_ts: datetime,
    ) -> None:
        if payload.position_instance_ref is None:
            return
        prior = session.scalar(
            select(PositionInstanceSnapshot)
            .where(PositionInstanceSnapshot.position_instance_ref == payload.position_instance_ref)
            .order_by(desc(PositionInstanceSnapshot.snapshot_ts), desc(PositionInstanceSnapshot.created_at))
            .limit(1)
        )
        prior_qty = prior.quantity if prior is not None else Decimal("0")
        prior_avg = prior.average_price if prior is not None else fill_price
        signed_qty = quantity if side == "buy" else -quantity
        new_qty = prior_qty + signed_qty
        avg_price = self._roll_average_price(
            prior_qty=prior_qty,
            prior_avg=prior_avg,
            side=side,
            quantity=quantity,
            fill_price=fill_price,
            new_qty=new_qty,
        )
        market_price = self._latest_price(session, payload.symbol) or fill_price
        market_value = new_qty * market_price
        unrealized = (market_price - avg_price) * new_qty if new_qty != 0 else Decimal("0")
        setup_variant_id = payload.setup_variant_id or (
            prior.setup_variant_id if prior is not None else "opening_drive_continuation"
        )
        execution_expression_id = payload.execution_expression_id or (
            prior.execution_expression_id if prior is not None else "continuation_ladder_exec"
        )
        tradable_expression_family = payload.tradable_expression_family or (
            prior.tradable_expression_family if prior is not None else "single_leg_call_debit"
        )
        lifecycle_state = payload.lifecycle_state or (
            prior.lifecycle_state if prior is not None else "position_open"
        )
        lifecycle_action = payload.lifecycle_action or self._default_lifecycle_action(side, new_qty)
        current_position_size_pct = self._decimal_or_none(payload.current_position_size_pct)
        if current_position_size_pct is None:
            current_position_size_pct = (
                prior.current_position_size_pct if prior is not None else Decimal("0")
            )
        carry_state_eligible = (
            payload.carry_state_eligible
            if payload.carry_state_eligible is not None
            else (prior.carry_state_eligible if prior is not None else False)
        )
        hard_flat_required = (
            payload.hard_flat_required
            if payload.hard_flat_required is not None
            else (prior.hard_flat_required if prior is not None else False)
        )
        session.add(
            PositionInstanceSnapshot(
                position_instance_ref=payload.position_instance_ref,
                symbol=payload.symbol,
                snapshot_ts=snapshot_ts,
                setup_variant_id=setup_variant_id,
                execution_expression_id=execution_expression_id,
                tradable_expression_family=tradable_expression_family,
                lifecycle_state=lifecycle_state,
                lifecycle_action=lifecycle_action,
                current_position_size_pct=current_position_size_pct,
                quantity=new_qty,
                average_price=avg_price,
                market_price=market_price,
                market_value=market_value,
                unrealized_pnl=unrealized,
                carry_state_eligible=carry_state_eligible,
                hard_flat_required=hard_flat_required,
                source="broker_offline",
            )
        )

    def _derive_capital_state(
        self,
        session: Session,
        side: str,
        notional: Decimal,
        snapshot_ts: datetime,
    ) -> CapitalStateSnapshot:
        prior = session.scalar(
            select(CapitalStateSnapshot).order_by(desc(CapitalStateSnapshot.snapshot_ts)).limit(1)
        )
        starting_cash = prior.cash if prior is not None else Decimal("100000.000000")
        cash = starting_cash - notional if side == "buy" else starting_cash + notional
        latest_positions = self._latest_positions(session)
        gross_exposure = sum(
            (abs(row.market_value) for row in latest_positions), start=Decimal("0")
        )
        net_exposure = sum((row.market_value for row in latest_positions), start=Decimal("0"))
        equity = cash + net_exposure
        row = CapitalStateSnapshot(
            snapshot_ts=snapshot_ts,
            cash=cash,
            equity=equity,
            buying_power=cash,
            gross_exposure=gross_exposure,
            net_exposure=net_exposure,
            source="broker_offline",
        )
        session.add(row)
        return row

    def _latest_positions(self, session: Session) -> list[PositionSnapshot]:
        symbols = list(session.scalars(select(PositionSnapshot.symbol).distinct()))
        rows: list[PositionSnapshot] = []
        for symbol in symbols:
            row = session.scalar(
                select(PositionSnapshot)
                .where(PositionSnapshot.symbol == symbol)
                .order_by(desc(PositionSnapshot.snapshot_ts))
                .limit(1)
            )
            if row is not None:
                rows.append(row)
        return rows

    def _latest_price(self, session: Session, symbol: str) -> Decimal | None:
        return session.scalar(
            select(Bar1m.close)
            .join(Instrument, Instrument.id == Bar1m.instrument_id)
            .where(Instrument.symbol == symbol)
            .order_by(desc(Bar1m.ts_utc))
            .limit(1)
        )

    def _to_signal_payload(self, row: ModuleSignalEvent) -> ModuleSignalEventPayload:
        return ModuleSignalEventPayload(
            signal_event_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            requested_at=row.requested_at,
            signal_code=row.signal_code,
            direction=row.direction,
            score=float(row.score),
            payload=dict(json.loads(row.payload_json)),
        )

    def _to_veto_payload(self, row: ModuleVetoEvent) -> ModuleVetoEventPayload:
        return ModuleVetoEventPayload(
            veto_event_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            requested_at=row.requested_at,
            veto_code=row.veto_code,
            reason=row.reason,
            payload=dict(json.loads(row.payload_json)),
        )

    def _to_risk_block_payload(self, row: RiskBlockEvent) -> RiskBlockEventPayload:
        return RiskBlockEventPayload(
            risk_block_event_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            requested_at=row.requested_at,
            reason_codes=list(json.loads(row.reason_codes_json)),
            linked_risk_decision_id=row.linked_risk_decision_id,
            payload=dict(json.loads(row.payload_json)),
        )

    def _to_order_event_payload(self, row: OrderEventRecord) -> BrokerOrderEventPayload:
        return BrokerOrderEventPayload(
            order_event_id=row.id,
            order_intent_id=row.order_intent_id,
            created_at=row.created_at,
            event_ts=row.event_ts,
            status=row.status,
            detail=row.detail,
            payload=dict(json.loads(row.payload_json)),
        )

    def _to_fill_event_payload(self, row: FillEventRecord) -> BrokerFillEventPayload:
        return BrokerFillEventPayload(
            fill_event_id=row.id,
            order_intent_id=row.order_intent_id,
            created_at=row.created_at,
            fill_ts=row.fill_ts,
            quantity=float(row.quantity),
            fill_price=float(row.fill_price),
            notional=float(row.notional),
        )

    def _to_position_payload(self, row: PositionSnapshot) -> PositionSnapshotPayload:
        return PositionSnapshotPayload(
            position_snapshot_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            snapshot_ts=row.snapshot_ts,
            quantity=float(row.quantity),
            average_price=float(row.average_price),
            market_price=float(row.market_price),
            market_value=float(row.market_value),
            unrealized_pnl=float(row.unrealized_pnl),
            source=row.source,
        )

    def _to_position_instance_payload(
        self, row: PositionInstanceSnapshot
    ) -> PositionInstanceSnapshotPayload:
        return PositionInstanceSnapshotPayload(
            position_instance_snapshot_id=row.id,
            created_at=row.created_at,
            position_instance_ref=row.position_instance_ref,
            symbol=row.symbol,
            snapshot_ts=row.snapshot_ts,
            setup_variant_id=row.setup_variant_id,
            execution_expression_id=row.execution_expression_id,
            tradable_expression_family=cast(Any, row.tradable_expression_family),
            lifecycle_state=row.lifecycle_state,
            lifecycle_action=cast(Any, row.lifecycle_action),
            current_position_size_pct=float(row.current_position_size_pct),
            quantity=float(row.quantity),
            average_price=float(row.average_price),
            market_price=float(row.market_price),
            market_value=float(row.market_value),
            unrealized_pnl=float(row.unrealized_pnl),
            carry_state_eligible=bool(row.carry_state_eligible),
            hard_flat_required=bool(row.hard_flat_required),
            source=row.source,
        )

    def _to_capital_payload(self, row: CapitalStateSnapshot) -> CapitalStateSnapshotPayload:
        return CapitalStateSnapshotPayload(
            capital_state_snapshot_id=row.id,
            created_at=row.created_at,
            snapshot_ts=row.snapshot_ts,
            cash=float(row.cash),
            equity=float(row.equity),
            buying_power=float(row.buying_power),
            gross_exposure=float(row.gross_exposure),
            net_exposure=float(row.net_exposure),
            source=row.source,
        )

    def _to_daily_pnl_payload(self, row: DailyPnlReport) -> DailyPnlReportPayload:
        return DailyPnlReportPayload(
            daily_pnl_report_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            report_date=row.report_date,
            realized_pnl=float(row.realized_pnl),
            unrealized_pnl=float(row.unrealized_pnl),
            gross_exposure=float(row.gross_exposure),
            turnover=float(row.turnover),
            trade_count=row.trade_count,
            notes=list(json.loads(row.notes_json)),
        )

    def _aware(self, ts: datetime) -> datetime:
        return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)

    @staticmethod
    def _roll_average_price(
        *,
        prior_qty: Decimal,
        prior_avg: Decimal,
        side: str,
        quantity: Decimal,
        fill_price: Decimal,
        new_qty: Decimal,
    ) -> Decimal:
        if new_qty == 0:
            return Decimal("0")
        if side == "buy" and prior_qty >= 0:
            return ((prior_qty * prior_avg) + (quantity * fill_price)) / new_qty
        return prior_avg

    @staticmethod
    def _default_lifecycle_action(side: str, new_qty: Decimal) -> str:
        if new_qty == 0:
            return "flatten"
        return "add" if side == "buy" else "trim"

    @staticmethod
    def _decimal_or_none(value: float | None) -> Decimal | None:
        if value is None:
            return None
        return Decimal(str(value))
