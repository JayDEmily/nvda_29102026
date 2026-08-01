"""Canonical M10 K15 paper execution-gateway API."""
from .contracts import (
    PAPER_PORT_VERSION, PLACEMENT_POLICY_VERSION, ExecutionEvent,
    ExecutionReceipt, PlacementIntent, PlacementPolicy,
)
from .port import ExecutionPort, PaperExecutionPort
from .service import ExecutionGateway

__all__ = [
    "ExecutionEvent", "ExecutionGateway", "ExecutionPort", "ExecutionReceipt",
    "PAPER_PORT_VERSION", "PLACEMENT_POLICY_VERSION", "PaperExecutionPort",
    "PlacementIntent", "PlacementPolicy",
]
