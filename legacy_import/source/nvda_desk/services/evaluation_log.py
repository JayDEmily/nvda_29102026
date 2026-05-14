from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import cast

from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import EvaluationRun
from nvda_desk.schemas.eval import (
    EvaluationRunListResponse,
    EvaluationRunPayload,
    EvalVerdict,
)
from nvda_desk.schemas.module import ModuleDescriptor


class EvaluationLogService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def record(
        self,
        *,
        symbol: str,
        descriptor: ModuleDescriptor,
        requested_at: datetime,
        verdict: EvalVerdict,
        score: float,
        input_payload: BaseModel,
        output_payload: BaseModel,
    ) -> EvaluationRunPayload:
        with self._session_factory() as session:
            row = EvaluationRun(
                symbol=symbol,
                module_id=descriptor.module_id,
                module_name=descriptor.name,
                module_class=descriptor.module_class.value,
                verdict=verdict,
                score=score,
                requested_at=(
                    requested_at.astimezone(UTC)
                    if requested_at.tzinfo
                    else requested_at.replace(tzinfo=UTC)
                ),
                input_json=self._dump_model(input_payload),
                output_json=self._dump_model(output_payload),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_runs(self, module_id: str | None = None, limit: int = 20) -> EvaluationRunListResponse:
        with self._session_factory() as session:
            stmt = select(EvaluationRun)
            if module_id:
                stmt = stmt.where(EvaluationRun.module_id == module_id)
            stmt = stmt.order_by(desc(EvaluationRun.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return EvaluationRunListResponse(evaluations=[self._to_payload(row) for row in rows])

    def _dump_model(self, model: BaseModel) -> str:
        return json.dumps(model.model_dump(mode="json"))

    def _to_payload(self, row: EvaluationRun) -> EvaluationRunPayload:
        return EvaluationRunPayload(
            evaluation_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            module_name=row.module_name,
            module_class=row.module_class,
            verdict=cast(EvalVerdict, row.verdict),
            score=float(row.score),
            requested_at=row.requested_at,
            input_payload=dict(json.loads(row.input_json)),
            output_payload=dict(json.loads(row.output_json)),
        )
