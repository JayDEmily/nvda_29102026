"""Bounded operational event/session CRUD shell separated from reference projection."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

_MATERIALITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(slots=True)
class MarketEventDTO:
    """One operational event row for repo-native CRUD ownership."""

    event_id: str
    event_type: str
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    tags: list[str] = field(default_factory=list)
    symbol: str | None = None
    materiality: str = "low"
    lineage_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SessionCalendarDTO:
    """One operational session row for repo-native CRUD ownership."""

    session_id: str
    trade_date: str
    session_state: str
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class RuntimeCalendarQuery:
    symbol: str | None
    window_start_utc: datetime
    window_end_utc: datetime
    minimum_materiality: str = "low"
    observed_at: datetime | None = None

    @property
    def minimum_materiality_rank(self) -> int:
        return _materiality_rank(self.minimum_materiality)


@dataclass(frozen=True, slots=True)
class RuntimeCalendarEventMatch:
    event: MarketEventDTO
    proximity_seconds: int
    materiality_rank: int


@dataclass(frozen=True, slots=True)
class RuntimeCalendarSnapshot:
    query: RuntimeCalendarQuery
    matches: list[RuntimeCalendarEventMatch]
    decision_authority: str = "calendar_context_only"
    candidate_formation_allowed: bool = False
    capital_sizing_allowed: bool = False

    def lineage_for(self, event_id: str) -> list[str]:
        for match in self.matches:
            if match.event.event_id == event_id:
                return list(match.event.lineage_ids)
        return []


class OperationalEventRepository:
    """In-memory operational event store kept separate from reference projection."""

    def __init__(self) -> None:
        self._events: list[MarketEventDTO] = []

    def create_event(self, event: MarketEventDTO) -> MarketEventDTO:
        """Store and return one operational event DTO."""

        self._events.append(event)
        return event

    def list_events(self) -> list[MarketEventDTO]:
        """Return the stored operational events in insertion order."""

        return list(self._events)

    def ingest_precursor_context(self, precursor) -> None:
        """Compose checked reference projection into bounded operational query state."""

        trace = getattr(precursor, "projection_trace", None)
        if trace is None:
            raise ValueError("calendar_projection_trace_required")
        if getattr(trace, "candidate_formation_allowed", True):
            raise ValueError("calendar_projection_candidate_authority_forbidden")
        if getattr(trace, "capital_sizing_allowed", True):
            raise ValueError("calendar_projection_capital_authority_forbidden")
        existing = {event.event_id for event in self._events}
        for snapshot in precursor.events:
            if snapshot.event_id in existing:
                raise ValueError(f"duplicate operational calendar event_id: {snapshot.event_id}")
            reference = snapshot.reference
            if reference is None:
                raise ValueError("calendar_event_reference_required")
            self._events.append(
                MarketEventDTO(
                    event_id=snapshot.event_id,
                    event_type=snapshot.event_type,
                    starts_at=reference.observed_at,
                    tags=list(snapshot.runtime_tags),
                    lineage_ids=[reference.source_artifact_id],
                )
            )
            existing.add(snapshot.event_id)

    def query_runtime_calendar(
        self, query: RuntimeCalendarQuery
    ) -> list[RuntimeCalendarEventMatch]:
        """Return material runtime calendar matches for one bounded query."""

        matches = [
            RuntimeCalendarEventMatch(
                event=event,
                proximity_seconds=_proximity_seconds(event=event, query=query),
                materiality_rank=_materiality_rank(event.materiality),
            )
            for event in self._events
            if _event_matches_query(event=event, query=query)
        ]
        return sorted(
            matches,
            key=lambda match: (
                match.proximity_seconds,
                -match.materiality_rank,
                match.event.event_id,
            ),
        )

    def build_runtime_calendar_snapshot(
        self, query: RuntimeCalendarQuery
    ) -> RuntimeCalendarSnapshot:
        """Build one context-only runtime calendar projection."""

        return RuntimeCalendarSnapshot(query=query, matches=self.query_runtime_calendar(query))


class OperationalSessionRepository:
    """In-memory operational session store kept separate from reference projection."""

    def __init__(self) -> None:
        self._sessions: list[SessionCalendarDTO] = []

    def create_session(self, session: SessionCalendarDTO) -> SessionCalendarDTO:
        """Store and return one operational session DTO."""

        self._sessions.append(session)
        return session

    def list_sessions(self) -> list[SessionCalendarDTO]:
        """Return the stored operational sessions in insertion order."""

        return list(self._sessions)


def _event_matches_query(*, event: MarketEventDTO, query: RuntimeCalendarQuery) -> bool:
    if query.symbol is not None and event.symbol not in {query.symbol, None}:
        return False
    if _materiality_rank(event.materiality) < query.minimum_materiality_rank:
        return False
    if event.starts_at is None:
        return False
    event_end = event.ends_at or event.starts_at
    return event.starts_at <= query.window_end_utc and event_end >= query.window_start_utc


def _proximity_seconds(*, event: MarketEventDTO, query: RuntimeCalendarQuery) -> int:
    observed_at = query.observed_at or query.window_start_utc
    if event.starts_at is None:
        return 0
    return int(abs((event.starts_at - observed_at).total_seconds()))


def _materiality_rank(materiality: str) -> int:
    return _MATERIALITY_RANK.get(materiality, 0)
