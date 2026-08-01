"""Load the promoted PRL expected-signal inventory from runtime-safe YAML."""

from __future__ import annotations

from pathlib import Path

import yaml

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskExpectedSignalRecord,
    ParallelRiskSignalInventoryDocument,
    parallel_risk_signal_inventory_document_from_dict,
)

DEFAULT_PARALLEL_RISK_SIGNAL_INVENTORY_PATH = Path("config/parallel_risk_signal_inventory.v1.yaml")


class ParallelRiskSignalInventoryService:
    """Typed access to expected PRL signals without reading the governed workbook."""

    def __init__(
        self,
        inventory_path: Path | str = DEFAULT_PARALLEL_RISK_SIGNAL_INVENTORY_PATH,
    ) -> None:
        self.inventory_path = Path(inventory_path)

    def load_document(self) -> ParallelRiskSignalInventoryDocument:
        """Load and validate the runtime-safe promoted inventory document."""

        payload = yaml.safe_load(self.inventory_path.read_text(encoding="utf-8")) or {}
        return parallel_risk_signal_inventory_document_from_dict(payload)

    def record_map(self) -> dict[str, ParallelRiskExpectedSignalRecord]:
        """Return expected signal records keyed by signal id."""

        return self.load_document().record_map()

    def required_runtime_records(self) -> list[ParallelRiskExpectedSignalRecord]:
        """Return current-atom signals available to runtime after typed promotion."""

        return self.load_document().required_runtime_records()
