from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nvda_desk.db.base import Base


class Instrument(Base):
    __tablename__ = "instrument"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    asset_class: Mapped[str] = mapped_column(String(32))
    venue: Mapped[str] = mapped_column(String(32), default="NASDAQ")

    bars: Mapped[list[Bar1m]] = relationship(
        back_populates="instrument", cascade="all, delete-orphan"
    )


class Bar1m(Base):
    __tablename__ = "bar_1m"
    __table_args__ = (
        UniqueConstraint("instrument_id", "ts_utc", name="uq_bar_1m_instrument_ts"),
        Index("ix_bar_1m_instrument_ts", "instrument_id", "ts_utc"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instrument.id", ondelete="CASCADE"))
    ts_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    open: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    high: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    low: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    close: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    volume: Mapped[int] = mapped_column()

    instrument: Mapped[Instrument] = relationship(back_populates="bars")


class OptionSnapshot(Base):
    __tablename__ = "option_snapshot"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id",
            "as_of_date",
            "expiry",
            "option_type",
            "strike",
            name="uq_option_snapshot_identity",
        ),
        Index(
            "ix_option_snapshot_surface",
            "instrument_id",
            "as_of_date",
            "expiry",
            "option_type",
            "strike",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instrument.id", ondelete="CASCADE"))
    as_of_date: Mapped[date] = mapped_column(Date())
    expiry: Mapped[date | None] = mapped_column(Date(), nullable=True)
    option_type: Mapped[str] = mapped_column(String(8), index=True)
    strike: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    bid: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    ask: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    last: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    volume: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    open_interest: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    iv: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    delta: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    gamma: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    delta_change: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    provenance: Mapped[str] = mapped_column(String(64), default="unknown")
    confidence: Mapped[str] = mapped_column(String(32), default="unknown")
    source_document: Mapped[str] = mapped_column(String(255), default="unknown")
    source_pages: Mapped[str] = mapped_column(String(64), default="")

    instrument: Mapped[Instrument] = relationship()


class OptionsFlowHistoryObservation(Base):
    __tablename__ = "options_flow_history_observation"
    __table_args__ = (
        UniqueConstraint("symbol", "observed_at", name="uq_options_flow_history_observation_identity"),
        Index("ix_options_flow_history_observation_symbol_observed", "symbol", "observed_at"),
        Index("ix_options_flow_history_observation_symbol_chain", "symbol", "chain_ts"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    chain_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    front_expiry: Mapped[date] = mapped_column(Date())
    next_expiry: Mapped[date] = mapped_column(Date())
    partiality_state: Mapped[str] = mapped_column(String(32))
    record_completeness_flag: Mapped[bool] = mapped_column(Boolean(), default=False)
    raw_source_authority: Mapped[str] = mapped_column(String(64))
    lineage_json: Mapped[str] = mapped_column(Text())
    derived_state_json: Mapped[str] = mapped_column(Text())
    front_expiry_rows_json: Mapped[str] = mapped_column(Text(), default="[]")
    next_expiry_rows_json: Mapped[str] = mapped_column(Text(), default="[]")



class ResearchNote(Base):
    __tablename__ = "research_note"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(255))
    thesis: Mapped[str] = mapped_column(Text())
    body_md: Mapped[str] = mapped_column(Text())
    tags_json: Mapped[str] = mapped_column(Text(), default="[]")


class EvaluationRun(Base):
    __tablename__ = "evaluation_run"
    __table_args__ = (Index("ix_evaluation_run_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    module_name: Mapped[str] = mapped_column(String(255))
    module_class: Mapped[str] = mapped_column(String(32))
    verdict: Mapped[str] = mapped_column(String(16), index=True)
    score: Mapped[Decimal] = mapped_column(Numeric(8, 6))
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    input_json: Mapped[str] = mapped_column(Text())
    output_json: Mapped[str] = mapped_column(Text())


class ExperimentRun(Base):
    __tablename__ = "experiment_run"
    __table_args__ = (
        Index("ix_experiment_run_module_created", "module_id", "created_at"),
        Index(
            "ix_experiment_run_module_type_created",
            "module_id",
            "experiment_type",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    experiment_type: Mapped[str] = mapped_column(String(32), index=True)
    config_name: Mapped[str] = mapped_column(String(128), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ranking_score: Mapped[Decimal | None] = mapped_column(Numeric(8, 6), nullable=True)
    input_json: Mapped[str] = mapped_column(Text())
    output_json: Mapped[str] = mapped_column(Text())


class RiskDecisionLog(Base):
    __tablename__ = "risk_decision_log"
    __table_args__ = (Index("ix_risk_decision_log_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    action: Mapped[str] = mapped_column(String(16), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    input_json: Mapped[str] = mapped_column(Text())
    output_json: Mapped[str] = mapped_column(Text())


class ModuleSpec(Base):
    __tablename__ = "module_spec"
    __table_args__ = (Index("ix_module_spec_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    name: Mapped[str] = mapped_column(String(255))
    module_class: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), index=True)
    thesis: Mapped[str] = mapped_column(Text())
    required_inputs_json: Mapped[str] = mapped_column(Text(), default="[]")
    parameters_json: Mapped[str] = mapped_column(Text(), default="{}")
    notes_md: Mapped[str] = mapped_column(Text(), default="")
    source_refs_json: Mapped[str] = mapped_column(Text(), default="[]")


class PromotionDecision(Base):
    __tablename__ = "promotion_decision"
    __table_args__ = (Index("ix_promotion_decision_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    from_status: Mapped[str] = mapped_column(String(32), index=True)
    to_status: Mapped[str] = mapped_column(String(32), index=True)
    decision_reason: Mapped[str] = mapped_column(Text())
    evaluation_ids_json: Mapped[str] = mapped_column(Text(), default="[]")
    evidence_refs_json: Mapped[str] = mapped_column(Text(), default="[]")
    approved_by: Mapped[str] = mapped_column(String(255), default="operator")


class SessionCalendar(Base):
    __tablename__ = "session_calendar"
    __table_args__ = (
        UniqueConstraint("session_date", "venue", name="uq_session_calendar_date_venue"),
        Index("ix_session_calendar_date", "session_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_date: Mapped[date] = mapped_column(Date(), index=True)
    venue: Mapped[str] = mapped_column(String(32), default="NASDAQ")
    market_open_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    market_close_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    session_label: Mapped[str] = mapped_column(String(32), default="regular")
    is_half_day: Mapped[bool] = mapped_column(Boolean(), default=False)


class MarketEvent(Base):
    __tablename__ = "market_event"
    __table_args__ = (
        Index("ix_market_event_ts", "event_ts"),
        Index("ix_market_event_symbol_ts", "symbol", "event_ts"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    event_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    impact_level: Mapped[str] = mapped_column(String(16), default="medium")
    title: Mapped[str] = mapped_column(String(255))
    source_document: Mapped[str] = mapped_column(String(255), default="manual")
    notes_md: Mapped[str] = mapped_column(Text(), default="")


class ModuleSignalEvent(Base):
    __tablename__ = "module_signal_event"
    __table_args__ = (Index("ix_module_signal_event_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    signal_code: Mapped[str] = mapped_column(String(128), index=True)
    direction: Mapped[str] = mapped_column(String(16), default="long")
    score: Mapped[Decimal] = mapped_column(Numeric(8, 6))
    payload_json: Mapped[str] = mapped_column(Text(), default="{}")


class ModuleVetoEvent(Base):
    __tablename__ = "module_veto_event"
    __table_args__ = (Index("ix_module_veto_event_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    veto_code: Mapped[str] = mapped_column(String(128), index=True)
    reason: Mapped[str] = mapped_column(Text())
    payload_json: Mapped[str] = mapped_column(Text(), default="{}")


class RiskBlockEvent(Base):
    __tablename__ = "risk_block_event"
    __table_args__ = (Index("ix_risk_block_event_module_created", "module_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    linked_risk_decision_id: Mapped[int | None] = mapped_column(
        ForeignKey("risk_decision_log.id", ondelete="SET NULL"),
        nullable=True,
    )
    reason_codes_json: Mapped[str] = mapped_column(Text(), default="[]")
    payload_json: Mapped[str] = mapped_column(Text(), default="{}")


class OrderIntentRecord(Base):
    __tablename__ = "order_intent"
    __table_args__ = (
        Index("ix_order_intent_module_created", "module_id", "created_at"),
        Index("ix_order_intent_position_instance_created", "position_instance_ref", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    module_id: Mapped[str] = mapped_column(String(128), index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    side: Mapped[str] = mapped_column(String(8), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    order_type: Mapped[str] = mapped_column(String(16), default="limit")
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    position_instance_ref: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    setup_variant_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    execution_expression_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tradable_expression_family: Mapped[str | None] = mapped_column(String(64), nullable=True)
    lifecycle_state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    lifecycle_action: Mapped[str | None] = mapped_column(String(32), nullable=True)
    current_position_size_pct: Mapped[Decimal | None] = mapped_column(Numeric(8, 3), nullable=True)
    carry_state_eligible: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    hard_flat_required: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    client_order_ref: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    payload_json: Mapped[str] = mapped_column(Text(), default="{}")


class OrderEventRecord(Base):
    __tablename__ = "order_event"
    __table_args__ = (Index("ix_order_event_intent_ts", "order_intent_id", "event_ts"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order_intent_id: Mapped[int] = mapped_column(ForeignKey("order_intent.id", ondelete="CASCADE"))
    event_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), index=True)
    detail: Mapped[str] = mapped_column(Text())
    payload_json: Mapped[str] = mapped_column(Text(), default="{}")


class FillEventRecord(Base):
    __tablename__ = "fill_event"
    __table_args__ = (Index("ix_fill_event_intent_ts", "order_intent_id", "fill_ts"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order_intent_id: Mapped[int] = mapped_column(ForeignKey("order_intent.id", ondelete="CASCADE"))
    fill_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    fill_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    notional: Mapped[Decimal] = mapped_column(Numeric(18, 6))


class PositionSnapshot(Base):
    __tablename__ = "position_snapshot"
    __table_args__ = (Index("ix_position_snapshot_symbol_ts", "symbol", "snapshot_ts"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    average_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    market_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    market_value: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    unrealized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    source: Mapped[str] = mapped_column(String(32), default="broker_offline")


class PositionInstanceSnapshot(Base):
    __tablename__ = "position_instance_snapshot"
    __table_args__ = (
        Index("ix_position_instance_snapshot_ref_ts", "position_instance_ref", "snapshot_ts"),
        Index("ix_position_instance_snapshot_symbol_ts", "symbol", "snapshot_ts"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    position_instance_ref: Mapped[str] = mapped_column(String(128), index=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    setup_variant_id: Mapped[str] = mapped_column(String(128))
    execution_expression_id: Mapped[str] = mapped_column(String(128))
    tradable_expression_family: Mapped[str] = mapped_column(String(64))
    lifecycle_state: Mapped[str] = mapped_column(String(64))
    lifecycle_action: Mapped[str] = mapped_column(String(32))
    current_position_size_pct: Mapped[Decimal] = mapped_column(Numeric(8, 3), default=Decimal("0"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    average_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    market_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    market_value: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    unrealized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    carry_state_eligible: Mapped[bool] = mapped_column(Boolean(), default=False)
    hard_flat_required: Mapped[bool] = mapped_column(Boolean(), default=False)
    source: Mapped[str] = mapped_column(String(32), default="broker_offline")


class CapitalStateSnapshot(Base):
    __tablename__ = "capital_state_snapshot"
    __table_args__ = (Index("ix_capital_state_snapshot_ts", "snapshot_ts"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    cash: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    equity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    buying_power: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    gross_exposure: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    net_exposure: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    source: Mapped[str] = mapped_column(String(32), default="broker_offline")


class DailyPnlReport(Base):
    __tablename__ = "daily_pnl_report"
    __table_args__ = (
        UniqueConstraint("symbol", "report_date", name="uq_daily_pnl_report_symbol_date"),
        Index("ix_daily_pnl_report_date", "report_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    report_date: Mapped[date] = mapped_column(Date(), index=True)
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    unrealized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    gross_exposure: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    turnover: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    trade_count: Mapped[int] = mapped_column(Integer(), default=0)
    notes_json: Mapped[str] = mapped_column(Text(), default="[]")
