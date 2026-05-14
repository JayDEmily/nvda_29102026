from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import Instrument, OptionSnapshot, OptionsFlowHistoryObservation
from nvda_desk.schemas.cognition import OptionsFlowContextInput, OptionsFlowContextOutput
from nvda_desk.schemas.options import OptionSnapshotPayload, OptionType
from nvda_desk.schemas.options_flow_history import (
    OptionsFlowHistoryLineage,
    OptionsFlowHistoryObservationRecord,
    OptionsFlowHistoryObservationStorePayload,
    OptionsFlowHistoryWriteResult,
)


class OptionsFlowHistoryBuilder:
    """Build one bounded observational record from the live options-flow boundary."""

    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def build(
        self,
        *,
        symbol: str,
        observed_at: datetime,
        options_flow_input: OptionsFlowContextInput,
        options_flow_output: OptionsFlowContextOutput,
    ) -> OptionsFlowHistoryObservationRecord:
        observed_at = self._aware(observed_at)
        as_of_date = observed_at.date()
        front_expiry = as_of_date + timedelta(days=options_flow_input.front_dte)
        next_expiry = as_of_date + timedelta(days=options_flow_input.next_dte)
        front_rows: list[OptionSnapshotPayload] = []
        next_rows: list[OptionSnapshotPayload] = []
        with self._session_factory() as session:
            instrument = session.scalar(select(Instrument).where(Instrument.symbol == symbol))
            if instrument is not None:
                rows = list(
                    session.scalars(
                        select(OptionSnapshot)
                        .where(OptionSnapshot.instrument_id == instrument.id)
                        .where(OptionSnapshot.as_of_date == as_of_date)
                        .where(OptionSnapshot.expiry.in_([front_expiry, next_expiry]))
                        .order_by(OptionSnapshot.expiry, OptionSnapshot.option_type, OptionSnapshot.strike)
                    )
                )
                front_rows = [self._to_payload(row) for row in rows if row.expiry == front_expiry]
                next_rows = [self._to_payload(row) for row in rows if row.expiry == next_expiry]
        partiality_state = self._partiality_state(front_rows=front_rows, next_rows=next_rows)
        return OptionsFlowHistoryObservationRecord(
            symbol=symbol,
            observed_at=observed_at,
            chain_ts=observed_at,
            front_expiry=front_expiry,
            next_expiry=next_expiry,
            derived_state=options_flow_output,
            front_expiry_rows=front_rows,
            next_expiry_rows=next_rows,
            partiality_state=partiality_state,
            record_completeness_flag=partiality_state == "complete",
            lineage=OptionsFlowHistoryLineage(
                raw_source_authority="persisted_option_snapshot",
                observed_at=observed_at,
                chain_ts=observed_at,
                raw_source_as_of_date=as_of_date,
                source_identity=f"{symbol}:{as_of_date.isoformat()}",
            ),
        )

    def _to_payload(self, row: OptionSnapshot) -> OptionSnapshotPayload:
        option_type = OptionType.CALL if row.option_type.lower() == 'call' else OptionType.PUT
        return OptionSnapshotPayload(
            as_of_date=row.as_of_date,
            expiry=row.expiry,
            option_type=option_type,
            strike=row.strike,
            bid=row.bid,
            ask=row.ask,
            last=row.last,
            volume=row.volume,
            open_interest=row.open_interest,
            iv=row.iv,
            delta=row.delta,
            gamma=row.gamma,
            delta_change=row.delta_change,
            provenance=row.provenance,
            confidence=row.confidence,
            source_document=row.source_document,
            source_pages=row.source_pages,
        )

    def _partiality_state(
        self, *, front_rows: list[OptionSnapshotPayload], next_rows: list[OptionSnapshotPayload]
    ) -> str:
        if front_rows and next_rows:
            return "complete"
        if front_rows and not next_rows:
            return "next_expiry_missing"
        if next_rows and not front_rows:
            return "front_expiry_missing"
        return "raw_subset_missing"

    def _aware(self, value: datetime) -> datetime:
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


class OptionsFlowHistoryStore:
    """Append-only store for options-flow observational records."""

    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def write(
        self, record: OptionsFlowHistoryObservationRecord
    ) -> OptionsFlowHistoryObservationStorePayload:
        with self._session_factory() as session:
            row = OptionsFlowHistoryObservation(
                symbol=record.symbol,
                observed_at=record.observed_at,
                chain_ts=record.chain_ts,
                front_expiry=record.front_expiry,
                next_expiry=record.next_expiry,
                partiality_state=record.partiality_state,
                record_completeness_flag=record.record_completeness_flag,
                raw_source_authority=record.lineage.raw_source_authority,
                lineage_json=json.dumps(record.lineage.model_dump(mode="json")),
                derived_state_json=json.dumps(record.derived_state.model_dump(mode="json")),
                front_expiry_rows_json=json.dumps([r.model_dump(mode="json") for r in record.front_expiry_rows]),
                next_expiry_rows_json=json.dumps([r.model_dump(mode="json") for r in record.next_expiry_rows]),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return OptionsFlowHistoryObservationStorePayload(
                observation_id=row.id,
                created_at=row.created_at,
                record=record,
            )

    def list_by_symbol(self, symbol: str) -> list[OptionsFlowHistoryObservationStorePayload]:
        with self._session_factory() as session:
            rows = list(
                session.scalars(
                    select(OptionsFlowHistoryObservation)
                    .where(OptionsFlowHistoryObservation.symbol == symbol)
                    .order_by(desc(OptionsFlowHistoryObservation.observed_at))
                )
            )
        records: list[OptionsFlowHistoryObservationStorePayload] = []
        for row in rows:
            record = OptionsFlowHistoryObservationRecord(
                symbol=row.symbol,
                observed_at=row.observed_at,
                chain_ts=row.chain_ts,
                front_expiry=row.front_expiry,
                next_expiry=row.next_expiry,
                derived_state=OptionsFlowContextOutput(**json.loads(row.derived_state_json)),
                front_expiry_rows=[OptionSnapshotPayload(**payload) for payload in json.loads(row.front_expiry_rows_json)],
                next_expiry_rows=[OptionSnapshotPayload(**payload) for payload in json.loads(row.next_expiry_rows_json)],
                partiality_state=row.partiality_state,
                record_completeness_flag=row.record_completeness_flag,
                lineage=OptionsFlowHistoryLineage(**json.loads(row.lineage_json)),
            )
            records.append(
                OptionsFlowHistoryObservationStorePayload(
                    observation_id=row.id,
                    created_at=row.created_at,
                    record=record,
                )
            )
        return records


def build_and_persist_options_flow_history(
    *,
    builder: OptionsFlowHistoryBuilder,
    store: OptionsFlowHistoryStore,
    symbol: str,
    observed_at: datetime,
    options_flow_input: OptionsFlowContextInput,
    options_flow_output: OptionsFlowContextOutput,
) -> OptionsFlowHistoryWriteResult:
    record = builder.build(
        symbol=symbol,
        observed_at=observed_at,
        options_flow_input=options_flow_input,
        options_flow_output=options_flow_output,
    )
    persisted = store.write(record)
    return OptionsFlowHistoryWriteResult(status="persisted", persisted=persisted)
