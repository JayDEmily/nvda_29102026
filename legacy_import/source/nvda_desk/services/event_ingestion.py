from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from nvda_desk.schemas.events import (
    EventConfidenceTier,
    EventFreshnessState,
    EventSourceClass,
    EventSourceProvenance,
    NormalisedEventRecord,
    RawEventSourceObservation,
    SourceConflictDisposition,
    SourceOutagePolicy,
)


class EventIngestionService:
    """Normalise bounded source observations into one visible shared event truth.

    The service groups observations by governed event identity and preserves source disagreement
    explicitly rather than merging it away silently.
    """

    _FRESHNESS_ORDER = {
        EventFreshnessState.CURRENT: 0,
        EventFreshnessState.DEFERRED: 1,
        EventFreshnessState.STALE: 2,
    }
    _CONFIDENCE_ORDER = {
        EventConfidenceTier.AUTHORITATIVE: 0,
        EventConfidenceTier.CORROBORATED: 1,
        EventConfidenceTier.PROVISIONAL: 2,
        EventConfidenceTier.DEGRADED: 3,
    }
    _SOURCE_CLASS_ORDER = {
        EventSourceClass.ISSUER_IR: 0,
        EventSourceClass.EXCHANGE_CALENDAR: 1,
        EventSourceClass.POLICY_CALENDAR: 2,
        EventSourceClass.MACRO_CALENDAR: 3,
        EventSourceClass.OPTIONS_EXPIRY_CALENDAR: 4,
        EventSourceClass.INTERNAL_CURATED: 5,
    }
    _OUTAGE_ORDER = {
        None: 0,
        SourceOutagePolicy.USE_LAST_VERIFIED_WITH_FLAG: 1,
        SourceOutagePolicy.DEGRADE_TO_UNKNOWN: 2,
        SourceOutagePolicy.DROP_SOURCE_AND_BLOCK_UNSUPPORTED: 3,
    }

    def normalise(
        self, observations: Sequence[RawEventSourceObservation]
    ) -> list[NormalisedEventRecord]:
        grouped: dict[tuple[str | None, str, str, str], list[RawEventSourceObservation]] = (
            defaultdict(list)
        )
        for observation in observations:
            key = (
                observation.symbol,
                observation.event_id,
                observation.event_type,
                observation.event_at.isoformat(),
            )
            grouped[key].append(observation)

        records: list[NormalisedEventRecord] = []
        for items in grouped.values():
            ordered = sorted(items, key=self._winner_sort_key)
            winner = ordered[0]
            labels = {item.label for item in ordered}
            conflict_notes = []
            if len(labels) > 1:
                conflict_notes.append("label_conflict_visible")
            if any(item.outage_policy is not None for item in ordered):
                conflict_notes.append("source_outage_visible")
            if len(ordered) > 1:
                conflict_notes.append("source_precedence_applied")
            provenance = [
                EventSourceProvenance(
                    source=item.source,
                    source_class=item.source_class,
                    source_document=item.source_document,
                    observed_at=item.observed_at,
                    freshness_state=item.freshness_state,
                    confidence_tier=item.confidence_tier,
                    conflict_disposition=self._conflict_disposition(item, winner),
                    outage_policy=item.outage_policy,
                    lineage_key=item.lineage_key,
                    notes=list(item.notes),
                )
                for item in ordered
            ]
            records.append(
                NormalisedEventRecord(
                    record_id=f"evt::{winner.event_id}::{winner.event_at.isoformat()}",
                    symbol=winner.symbol,
                    event_id=winner.event_id,
                    event_at=winner.event_at,
                    event_type=winner.event_type,
                    label=winner.label,
                    event_class=winner.event_class,
                    event_subclass=winner.event_subclass,
                    semantic_phase=winner.semantic_phase,
                    materiality_tier=winner.materiality_tier,
                    layer_id=winner.layer_id,
                    jurisdiction=winner.jurisdiction,
                    venues=list(winner.venues),
                    entities=list(winner.entities),
                    runtime_tags=list(winner.runtime_tags),
                    evaluation_tags=list(winner.evaluation_tags),
                    source_status=winner.source_status,
                    source_document=winner.source_document,
                    repo_artifact_id=winner.repo_artifact_id,
                    repo_artifact_path=winner.repo_artifact_path,
                    import_lineage_key=winner.import_lineage_key,
                    window_start_at=winner.window_start_at,
                    window_end_at=winner.window_end_at,
                    provenance=provenance,
                    lineage_keys=[item.lineage_key for item in ordered],
                    conflict_notes=conflict_notes,
                    tags=sorted({
                        *[item.source_class.value for item in ordered],
                        *winner.runtime_tags,
                        *winner.evaluation_tags,
                        *( [winner.layer_id] if winner.layer_id else []),
                    }),
                )
            )
        return sorted(
            records,
            key=lambda record: (record.event_at, record.event_id, record.record_id),
        )

    def _winner_sort_key(
        self, observation: RawEventSourceObservation
    ) -> tuple[int, int, int, int, float, str, str]:
        return (
            self._OUTAGE_ORDER[observation.outage_policy],
            self._FRESHNESS_ORDER[observation.freshness_state],
            self._CONFIDENCE_ORDER[observation.confidence_tier],
            self._SOURCE_CLASS_ORDER[observation.source_class],
            -observation.observed_at.timestamp(),
            observation.source.value,
            observation.lineage_key,
        )

    def _conflict_disposition(
        self,
        observation: RawEventSourceObservation,
        winner: RawEventSourceObservation,
    ) -> SourceConflictDisposition:
        if observation.lineage_key == winner.lineage_key:
            return SourceConflictDisposition.KEEP_CONFLICT_VISIBLE
        if winner.confidence_tier is EventConfidenceTier.AUTHORITATIVE:
            return SourceConflictDisposition.AUTHORITATIVE_SOURCE_WINS
        if winner.confidence_tier is EventConfidenceTier.CORROBORATED:
            return SourceConflictDisposition.LATEST_CORROBORATED_WINS
        return SourceConflictDisposition.KEEP_CONFLICT_VISIBLE
