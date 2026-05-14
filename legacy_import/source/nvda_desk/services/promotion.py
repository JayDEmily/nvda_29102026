from __future__ import annotations

import json

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import PromotionDecision
from nvda_desk.schemas.module import (
    ModuleStatus,
    PromotionDecisionCreate,
    PromotionDecisionListResponse,
    PromotionDecisionPayload,
)


class PromotionService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def record_decision(self, payload: PromotionDecisionCreate) -> PromotionDecisionPayload:
        with self._session_factory() as session:
            row = PromotionDecision(
                module_id=payload.module_id,
                from_status=payload.from_status.value,
                to_status=payload.to_status.value,
                decision_reason=payload.decision_reason,
                evaluation_ids_json=json.dumps(payload.evaluation_ids),
                evidence_refs_json=json.dumps(payload.evidence_refs),
                approved_by=payload.approved_by,
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_decisions(
        self, module_id: str | None = None, limit: int = 20
    ) -> PromotionDecisionListResponse:
        with self._session_factory() as session:
            stmt = select(PromotionDecision)
            if module_id:
                stmt = stmt.where(PromotionDecision.module_id == module_id)
            stmt = stmt.order_by(desc(PromotionDecision.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return PromotionDecisionListResponse(decisions=[self._to_payload(row) for row in rows])

    def _to_payload(self, row: PromotionDecision) -> PromotionDecisionPayload:
        return PromotionDecisionPayload(
            decision_id=row.id,
            created_at=row.created_at,
            module_id=row.module_id,
            from_status=ModuleStatus(row.from_status),
            to_status=ModuleStatus(row.to_status),
            decision_reason=row.decision_reason,
            evaluation_ids=list(json.loads(row.evaluation_ids_json)),
            evidence_refs=list(json.loads(row.evidence_refs_json)),
            approved_by=row.approved_by,
        )
