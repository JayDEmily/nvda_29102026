from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.contracts.daily_pnl import DailyPnlReport
from nvda_desk.downstream.daily_pnl import DailyPnlReportService
from nvda_desk.persistence.execution_records import ExecutionRecordsRepository
from nvda_desk.repositories.position_repository import PositionRepository

_REVIEW_REDIRECT_KEYS = frozenset(
    {
        "order_submitted",
        "live_broker_adapter",
        "capital_sizing",
        "execution_allowed",
        "position_mutation",
    }
)


class ModuleHealthSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    module_id: str
    order_event_count: int = Field(default=0, ge=0)
    fill_event_count: int = Field(default=0, ge=0)
    record_count: int = Field(default=0, ge=0)


class ModuleHealthPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    module_summaries: tuple[ModuleHealthSummary, ...] = Field(default_factory=tuple)
    position_snapshot_count: int = Field(default=0, ge=0)
    rendering_authority_mutated: bool = False


class ReviewSafeRendering(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    packet_kind: str
    review_safe_payload: dict[str, Any]
    redacted_keys: tuple[str, ...] = Field(default_factory=tuple)
    runtime_authority_mutated: bool = False


class DailyReviewPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str
    symbol: str
    trade_date: str
    module_health: ModuleHealthPacket
    daily_pnl: DailyPnlReport
    renderings: tuple[ReviewSafeRendering, ...] = Field(default_factory=tuple)
    missing_material_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_packet_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_receipt_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_artifact_ids: tuple[str, ...] = Field(default_factory=tuple)
    rendering_authority_mutated: bool = False

    @field_validator(
        "missing_material_ids",
        "source_packet_ids",
        "source_receipt_ids",
        "source_artifact_ids",
    )
    @classmethod
    def _validate_evidence_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalised = tuple(item.strip() for item in value)
        if any(not item for item in normalised):
            raise ValueError("review evidence identity must not be blank")
        if len(normalised) != len(set(normalised)):
            raise ValueError("review evidence identities must be unique")
        return normalised

    @model_validator(mode="after")
    def _validate_review_only(self) -> "DailyReviewPacket":
        if self.rendering_authority_mutated:
            raise ValueError("daily review packet must not mutate runtime authority")
        return self


class ReviewPacketService:
    def __init__(
        self,
        *,
        execution_records: ExecutionRecordsRepository | None = None,
        position_repository: PositionRepository | None = None,
        daily_pnl_service: DailyPnlReportService | None = None,
        active_module_ids: tuple[str, ...] = (),
    ) -> None:
        self._execution_records = execution_records or ExecutionRecordsRepository()
        self._position_repository = position_repository or PositionRepository()
        self._daily_pnl_service = daily_pnl_service or DailyPnlReportService()
        self._active_module_ids = tuple(active_module_ids)

    def build_module_health_packet(self, *, packet_id: str) -> ModuleHealthPacket:
        records = self._execution_records.list_records()
        module_ids = self._resolve_active_module_ids(records)
        summaries = tuple(
            self._build_module_summary(module_id, records) for module_id in module_ids
        )
        return ModuleHealthPacket(
            packet_id=packet_id,
            module_summaries=summaries,
            position_snapshot_count=len(self._position_repository.list_position_records()),
        )

    def render_review_safe_packet(
        self, *, packet_id: str, packet_kind: str, payload: Mapping[str, Any]
    ) -> ReviewSafeRendering:
        safe_payload, redacted_keys = _redact_review_payload(dict(payload))
        return ReviewSafeRendering(
            packet_id=packet_id,
            packet_kind=packet_kind,
            review_safe_payload=safe_payload,
            redacted_keys=tuple(sorted(redacted_keys)),
        )

    def build_daily_review_packet(
        self,
        *,
        packet_id: str,
        symbol: str,
        trade_date: str,
        renderings: tuple[ReviewSafeRendering, ...] = (),
    ) -> DailyReviewPacket:
        normalised_symbol = symbol.strip().upper()
        health = self.build_module_health_packet(packet_id=f"{packet_id}::module-health")
        pnl = self._daily_pnl_service.find_report(symbol=normalised_symbol, trade_date=trade_date)
        missing_material_ids: tuple[str, ...] = ()
        source_receipt_ids: tuple[str, ...] = ()
        if pnl is None:
            missing_material_ids = (f"daily_pnl_report::{normalised_symbol}::{trade_date}",)
            pnl = DailyPnlReport(
                report_id=f"{packet_id}::pnl-fallback",
                trade_date=trade_date,
                symbol=normalised_symbol,
                context={"fallback": True},
            )
        else:
            source_receipt_ids = (pnl.report_id,)
        source_packet_ids = tuple(
            dict.fromkeys((health.packet_id, *(rendering.packet_id for rendering in renderings)))
        )
        source_artifact_ids = tuple(dict.fromkeys(pnl.evidence_ids))
        return DailyReviewPacket(
            packet_id=packet_id,
            symbol=normalised_symbol,
            trade_date=trade_date,
            module_health=health,
            daily_pnl=pnl,
            renderings=renderings,
            missing_material_ids=missing_material_ids,
            source_packet_ids=source_packet_ids,
            source_receipt_ids=source_receipt_ids,
            source_artifact_ids=source_artifact_ids,
        )

    @property
    def daily_pnl_service(self) -> DailyPnlReportService:
        return self._daily_pnl_service

    def _resolve_active_module_ids(self, records: list[dict[str, Any]]) -> tuple[str, ...]:
        module_ids = list(self._active_module_ids)
        for record in records:
            module_id = str(record.get("module_id") or "").strip()
            if module_id and module_id not in module_ids:
                module_ids.append(module_id)
        return tuple(module_ids)

    def _build_module_summary(
        self, module_id: str, records: list[dict[str, Any]]
    ) -> ModuleHealthSummary:
        selected = [record for record in records if str(record.get("module_id") or "") == module_id]
        return ModuleHealthSummary(
            module_id=module_id,
            order_event_count=sum(
                1 for record in selected if record.get("record_type") == "order_event"
            ),
            fill_event_count=sum(
                1 for record in selected if record.get("record_type") == "fill_event"
            ),
            record_count=len(selected),
        )


def _redact_review_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], set[str]]:
    safe: dict[str, Any] = {}
    redacted: set[str] = set()
    for key, value in payload.items():
        key_text = str(key)
        if key_text in _REVIEW_REDIRECT_KEYS:
            redacted.add(key_text)
            continue
        if isinstance(value, dict):
            child, child_redacted = _redact_review_payload(deepcopy(value))
            safe[key_text] = child
            redacted.update(child_redacted)
        else:
            safe[key_text] = deepcopy(value)
    return safe, redacted
