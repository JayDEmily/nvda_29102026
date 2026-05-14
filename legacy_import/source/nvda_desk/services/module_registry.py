from __future__ import annotations

import json

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import ModuleSpec
from nvda_desk.schemas.module import (
    ModuleClass,
    ModuleDescriptor,
    ModuleSpecCreate,
    ModuleSpecListResponse,
    ModuleSpecPayload,
    ModuleStatus,
)


class ModuleRegistryService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def create_spec(self, payload: ModuleSpecCreate) -> ModuleSpecPayload:
        with self._session_factory() as session:
            row = ModuleSpec(
                module_id=payload.descriptor.module_id,
                name=payload.descriptor.name,
                module_class=payload.descriptor.module_class.value,
                status=payload.descriptor.status.value,
                thesis=payload.descriptor.thesis,
                required_inputs_json=json.dumps(payload.required_inputs),
                parameters_json=json.dumps(payload.parameters),
                notes_md=payload.notes_md,
                source_refs_json=json.dumps(payload.source_refs),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_specs(self, limit: int = 20) -> ModuleSpecListResponse:
        with self._session_factory() as session:
            stmt = select(ModuleSpec).order_by(desc(ModuleSpec.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return ModuleSpecListResponse(specs=[self._to_payload(row) for row in rows])

    def _to_payload(self, row: ModuleSpec) -> ModuleSpecPayload:
        return ModuleSpecPayload(
            spec_id=row.id,
            created_at=row.created_at,
            descriptor=ModuleDescriptor(
                module_id=row.module_id,
                name=row.name,
                module_class=ModuleClass(row.module_class),
                status=ModuleStatus(row.status),
                thesis=row.thesis,
            ),
            required_inputs=list(json.loads(row.required_inputs_json)),
            parameters=dict(json.loads(row.parameters_json)),
            notes_md=row.notes_md,
            source_refs=list(json.loads(row.source_refs_json)),
        )
