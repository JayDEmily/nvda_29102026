"""Canonical prepared-runtime harness helpers for the testing-module pack.

These helpers intentionally bind one prepared-runtime snapshot to explicit
companion regime and inventory truth. They do not claim broader real-data
coverage than the repo has actually admitted.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    TemporalContextInput,
)
from nvda_desk.schemas.dataset import PreparedRuntimeSnapshot
from nvda_desk.services.chain_to_cognition import ChainToCognitionService


class CanonicalRuntimeHarnessInput(BaseModel):
    """Typed single-run runtime harness input built from one prepared snapshot."""

    model_config = ConfigDict(extra="forbid")

    fixture_id: str
    dataset_id: str
    source_snapshot_ts: datetime
    sequence_id: str | None = None
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput
    options_flow_input: OptionsFlowContextInput
    inventory_state: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


class CanonicalRuntimeHarnessService:
    """Build one explicit runtime harness input from a prepared snapshot."""

    def build(
        self,
        *,
        dataset_id: str,
        snapshot: PreparedRuntimeSnapshot,
        regime_input: MarketRegimeContextInput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        fixture_id: str = "canonical_prepared_runtime_harness",
    ) -> CanonicalRuntimeHarnessInput:
        converted = ChainToCognitionService().convert_snapshot(snapshot)
        return CanonicalRuntimeHarnessInput(
            fixture_id=fixture_id,
            dataset_id=dataset_id,
            source_snapshot_ts=snapshot.ts,
            sequence_id=converted.lineage.sequence_id,
            temporal_input=converted.temporal_input,
            regime_input=regime_input,
            options_flow_input=converted.options_flow_input,
            inventory_state=inventory_state,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
        )
