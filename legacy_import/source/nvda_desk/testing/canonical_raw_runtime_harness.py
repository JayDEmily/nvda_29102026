"""Canonical raw-path harness helpers for the successor testing pack.

These helpers deliberately start from the admitted canonical raw bundle and walk
through the checked-in runtime path:

raw bundle -> prepared runtime dataset -> cognition inputs -> runtime-ready harness

They do not claim broader raw-ingress coverage than the one admitted canonical
bundle actually provides.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    TemporalContextInput,
)
from nvda_desk.schemas.dataset import RealDataBundle, RuntimeSnapshotSanityReport
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.real_data_loader import RealDataLoaderService


class CanonicalRawRuntimeHarnessInput(BaseModel):
    """Typed single-run harness input derived from one admitted raw bundle."""

    model_config = ConfigDict(extra="forbid")

    fixture_id: str
    dataset_id: str
    raw_bundle_path: str
    raw_bundle: RealDataBundle
    prepared_snapshot_count: int = Field(ge=1)
    sanity_report: RuntimeSnapshotSanityReport
    source_snapshot_ts: datetime
    sequence_id: str | None = None
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput
    options_flow_input: OptionsFlowContextInput
    inventory_state: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


class CanonicalRawRuntimeHarnessService:
    """Build one explicit runtime harness input from one admitted raw bundle."""

    def __init__(self) -> None:
        self._loader = RealDataLoaderService()
        self._converter = ChainToCognitionService()

    def build_from_path(
        self,
        *,
        raw_bundle_path: str | Path,
        dataset_id: str,
        regime_input: MarketRegimeContextInput,
        inventory_state: InventoryState,
        risk_budget_remaining_pct: float,
        snapshot_index: int = 0,
        fixture_id: str = "canonical_raw_runtime_harness",
    ) -> CanonicalRawRuntimeHarnessInput:
        raw_path = Path(raw_bundle_path)
        raw_bundle = self._loader.load_json_bundle(raw_path)
        prepared_dataset = self._loader.prepare_runtime_dataset(raw_bundle, dataset_id=dataset_id)
        sanity_report = self._loader.build_runtime_snapshot_sanity_report(raw_bundle, prepared_dataset)
        snapshot = prepared_dataset.snapshots[snapshot_index]
        converted = self._converter.convert_snapshot(snapshot)
        return CanonicalRawRuntimeHarnessInput(
            fixture_id=fixture_id,
            dataset_id=prepared_dataset.dataset_id,
            raw_bundle_path=raw_path.as_posix(),
            raw_bundle=raw_bundle,
            prepared_snapshot_count=len(prepared_dataset.snapshots),
            sanity_report=sanity_report,
            source_snapshot_ts=snapshot.ts,
            sequence_id=converted.lineage.sequence_id,
            temporal_input=converted.temporal_input,
            regime_input=regime_input,
            options_flow_input=converted.options_flow_input,
            inventory_state=inventory_state,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
        )
