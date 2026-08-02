"""Canonical M10 K15 paper execution-gateway API."""

from .contracts import (
    LIVE_PLACEMENT_POLICY_VERSION,
    PAPER_PORT_VERSION,
    PLACEMENT_POLICY_VERSION,
    ExecutionEvent,
    ExecutionReceipt,
    LivePlacementIntent,
    LivePlacementPolicy,
    PlacementIntent,
    PlacementPolicy,
)
from .port import ExecutionPort, PaperExecutionPort
from .service import ExecutionGateway

__all__ = [
    "ExecutionEvent",
    "ExecutionGateway",
    "ExecutionPort",
    "ExecutionReceipt",
    "LIVE_PLACEMENT_POLICY_VERSION",
    "LivePlacementIntent",
    "LivePlacementPolicy",
    "PAPER_PORT_VERSION",
    "PLACEMENT_POLICY_VERSION",
    "PaperExecutionPort",
    "PlacementIntent",
    "PlacementPolicy",
]
