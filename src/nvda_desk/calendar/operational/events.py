"""Bounded operational event/session CRUD shell separated from reference projection."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class MarketEventDTO:
    """One operational event row for repo-native CRUD ownership."""

    event_id: str
    event_type: str
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SessionCalendarDTO:
    """One operational session row for repo-native CRUD ownership."""

    session_id: str
    trade_date: str
    session_state: str
    tags: list[str] = field(default_factory=list)


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
