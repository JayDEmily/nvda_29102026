"""Define the protocol-only broker boundary without admitting concrete adapters."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, Sequence


class BrokerGatewayProtocol(Protocol):
    """Protocol-only broker boundary for future outbound order adapters."""

    def submit_order_intent(self, order_intent: Mapping[str, Any]) -> Mapping[str, Any]:
        """Submit one bounded order-intent payload and return one broker receipt mapping."""

    def read_order_events(self) -> Sequence[Mapping[str, Any]]:
        """Return bounded order-event mappings from the broker boundary."""

    def read_fill_events(self) -> Sequence[Mapping[str, Any]]:
        """Return bounded fill-event mappings from the broker boundary."""

    def read_positions(self) -> Sequence[Mapping[str, Any]]:
        """Return bounded broker-position mappings from the broker boundary."""


BrokerProtocol = BrokerGatewayProtocol

__all__ = ["BrokerGatewayProtocol", "BrokerProtocol"]
