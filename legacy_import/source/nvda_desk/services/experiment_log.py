from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any, cast

from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import ExperimentRun
from nvda_desk.schemas.eval import (
    ExperimentRunListResponse,
    ExperimentRunPayload,
    ExperimentType,
)


class ExperimentLogService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def record(
        self,
        *,
        symbol: str,
        module_id: str,
        experiment_type: ExperimentType,
        config_name: str,
        requested_at: datetime,
        input_payload: BaseModel,
        output_payload: BaseModel,
        ranking_score: float | None = None,
    ) -> ExperimentRunPayload:
        with self._session_factory() as session:
            row = ExperimentRun(
                symbol=symbol,
                module_id=module_id,
                experiment_type=experiment_type,
                config_name=config_name,
                requested_at=(
                    requested_at.astimezone(UTC)
                    if requested_at.tzinfo
                    else requested_at.replace(tzinfo=UTC)
                ),
                ranking_score=(None if ranking_score is None else round(ranking_score, 6)),
                input_json=self._dump_payload(input_payload),
                output_json=self._dump_payload(output_payload),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_runs(
        self,
        *,
        module_id: str | None = None,
        experiment_type: ExperimentType | None = None,
        limit: int = 20,
    ) -> ExperimentRunListResponse:
        with self._session_factory() as session:
            stmt = select(ExperimentRun)
            if module_id is not None:
                stmt = stmt.where(ExperimentRun.module_id == module_id)
            if experiment_type is not None:
                stmt = stmt.where(ExperimentRun.experiment_type == experiment_type)
            stmt = stmt.order_by(desc(ExperimentRun.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return ExperimentRunListResponse(experiments=[self._to_payload(row) for row in rows])

    def latest_run(
        self,
        *,
        module_id: str,
        experiment_type: ExperimentType,
    ) -> ExperimentRunPayload | None:
        with self._session_factory() as session:
            stmt = (
                select(ExperimentRun)
                .where(ExperimentRun.module_id == module_id)
                .where(ExperimentRun.experiment_type == experiment_type)
                .order_by(desc(ExperimentRun.created_at))
                .limit(1)
            )
            row = session.scalar(stmt)
        return None if row is None else self._to_payload(row)

    def _dump_payload(self, payload: BaseModel) -> str:
        return json.dumps(payload.model_dump(mode="json"))

    def _to_payload(self, row: ExperimentRun) -> ExperimentRunPayload:
        ranking_score = None if row.ranking_score is None else float(row.ranking_score)
        return ExperimentRunPayload(
            experiment_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            experiment_type=cast(ExperimentType, row.experiment_type),
            config_name=row.config_name,
            requested_at=row.requested_at,
            ranking_score=ranking_score,
            input_payload=cast(dict[str, Any], json.loads(row.input_json)),
            output_payload=cast(dict[str, Any], json.loads(row.output_json)),
        )
