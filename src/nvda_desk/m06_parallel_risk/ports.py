"""Read-only provider protocols for exact M06 owner facts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from nvda_desk.contracts.prepared_data import SourceCaptureReference

from .owner_facts import LiquidityOwnerFact


class LiquidityFactProvider(ABC):
    """Provide an exact M01-admitted liquidity fact or no fact; never a synthetic default."""

    @abstractmethod
    def read_liquidity_fact(
        self,
        *,
        symbol: str,
        effective_at_utc: datetime,
        required_notional: Decimal,
        source_capture_refs: tuple[SourceCaptureReference, ...],
    ) -> LiquidityOwnerFact | None:
        """Return one validated provider fact, or ``None`` when authority is unavailable."""
        raise NotImplementedError


__all__ = ["LiquidityFactProvider"]
