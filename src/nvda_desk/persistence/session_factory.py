"""Create bounded in-memory persistence sessions for the rebuild phase."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator


class InMemoryPersistenceSession(dict):
    """Small dict-backed persistence session used during the rebuild phase."""


class PersistenceSessionFactory:
    """Create deterministic in-memory sessions for repository helpers."""

    @contextmanager
    def session(self) -> Iterator[InMemoryPersistenceSession]:
        """Yield one bounded in-memory persistence session."""
        yield InMemoryPersistenceSession()
