from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

from nvda_desk.schemas.events import (
    EventMaterialityTier,
    EventQueryWindow,
    EventStoreQueryResult,
    LiveEventReference,
    LiveEventSnapshot,
    NormalisedEventRecord,
    ReplayEventConsumerMode,
)


class EventStoreService:
    """Shared event truth service for runtime, review, and replay consumers.

    Purpose:
        Provide one bounded store/query surface over normalised event truth so
        runtime, review, and replay use identical nearby-event semantics.
    Inputs:
        Sequences of `NormalisedEventRecord` objects produced by the Gate 72
        ingestion layer.
    Outputs:
        `EventStoreQueryResult` objects carrying nearby events, material events,
        and lineage maps for the requested consumer mode.
    Determinism:
        Applies stable query windows and explicit materiality filtering without
        hidden source-specific shortcuts.
    """

    def __init__(self, records: Sequence[NormalisedEventRecord]):
        self._records = sorted(records, key=lambda record: (record.event_at, record.record_id))

    def query(
        self,
        *,
        requested_at: datetime,
        symbol: str | None = None,
        query_window: EventQueryWindow | None = None,
        minimum_materiality: EventMaterialityTier = EventMaterialityTier.POSTURE_RELEVANT,
        replay_mode: ReplayEventConsumerMode = ReplayEventConsumerMode.RUNTIME_NEARBY,
    ) -> EventStoreQueryResult:
        window = query_window or EventQueryWindow(lookback_minutes=240, lookahead_minutes=1440)
        lower = self._aware(requested_at) - timedelta(minutes=window.lookback_minutes)
        upper = self._aware(requested_at) + timedelta(minutes=window.lookahead_minutes)
        nearby = [
            record
            for record in self._records
            if self._record_intersects_query_window(record, lower=lower, upper=upper)
            and self._symbol_matches(record.symbol, symbol)
        ]
        material = [
            record
            for record in nearby
            if self._materiality_rank(record.materiality_tier)
            >= self._materiality_rank(minimum_materiality)
        ]
        lineage_map = {record.record_id: list(record.lineage_keys) for record in nearby}
        return EventStoreQueryResult(
            requested_at=self._aware(requested_at),
            symbol=symbol,
            query_window=window,
            nearby_events=nearby,
            material_events=material,
            lineage_map=lineage_map,
            replay_mode=replay_mode,
        )

    def build_live_event_snapshot(
        self,
        *,
        requested_at: datetime,
        symbol: str | None = None,
        query_window: EventQueryWindow | None = None,
        minimum_materiality: EventMaterialityTier = EventMaterialityTier.POSTURE_RELEVANT,
    ) -> LiveEventSnapshot:
        result = self.query(
            requested_at=requested_at,
            symbol=symbol,
            query_window=query_window,
            minimum_materiality=minimum_materiality,
            replay_mode=ReplayEventConsumerMode.RUNTIME_NEARBY,
        )
        next_event = min(
            (
                record
                for record in result.nearby_events
                if self._aware(record.event_at) >= self._aware(requested_at)
            ),
            key=lambda record: record.event_at,
            default=None,
        )
        lineage_keys = sorted({key for keys in result.lineage_map.values() for key in keys})
        return LiveEventSnapshot(
            requested_at=result.requested_at,
            symbol=result.symbol,
            query_window=result.query_window,
            next_event=(self._to_live_reference(next_event) if next_event is not None else None),
            nearby_events=[self._to_live_reference(record) for record in result.nearby_events],
            material_events=[self._to_live_reference(record) for record in result.material_events],
            lineage_keys=lineage_keys,
        )

    def lineage_for(self, record_id: str) -> list[str]:
        for record in self._records:
            if record.record_id == record_id:
                return list(record.lineage_keys)
        return []

    def _to_live_reference(self, record: NormalisedEventRecord) -> LiveEventReference:
        return LiveEventReference(
            record_id=record.record_id,
            event_id=record.event_id,
            event_at=record.event_at,
            event_type=record.event_type,
            label=record.label,
            event_class=record.event_class,
            event_subclass=record.event_subclass,
            semantic_phase=record.semantic_phase,
            materiality_tier=record.materiality_tier,
            layer_id=record.layer_id,
            jurisdiction=record.jurisdiction,
            venues=list(record.venues),
            entities=list(record.entities),
            runtime_tags=list(record.runtime_tags),
            evaluation_tags=list(record.evaluation_tags),
            source_status=record.source_status,
            source_document=record.source_document,
            repo_artifact_id=record.repo_artifact_id,
            import_lineage_key=record.import_lineage_key,
            window_start_at=record.window_start_at,
            window_end_at=record.window_end_at,
            provenance_count=len(record.provenance),
            lineage_keys=list(record.lineage_keys),
        )


    def _record_intersects_query_window(
        self,
        record: NormalisedEventRecord,
        *,
        lower: datetime,
        upper: datetime,
    ) -> bool:
        event_at = self._aware(record.event_at)
        window_start = self._aware(record.window_start_at or record.event_at)
        window_end = self._aware(record.window_end_at or record.event_at)
        effective_start = min(event_at, window_start)
        effective_end = max(event_at, window_end)
        return effective_end >= lower and effective_start <= upper

    def _materiality_rank(self, tier: EventMaterialityTier) -> int:
        ordering = {
            EventMaterialityTier.BACKGROUND: 0,
            EventMaterialityTier.MONITOR: 1,
            EventMaterialityTier.POSTURE_RELEVANT: 2,
            EventMaterialityTier.DESK_CRITICAL: 3,
        }
        return ordering[tier]

    def _symbol_matches(self, record_symbol: str | None, requested_symbol: str | None) -> bool:
        return requested_symbol is None or record_symbol in {None, requested_symbol}

    def _aware(self, ts: datetime) -> datetime:
        return ts.astimezone(UTC) if ts.tzinfo is not None else ts.replace(tzinfo=UTC)
