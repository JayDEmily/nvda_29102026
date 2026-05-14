"""Read governed reference bundles through bounded native helpers.

This repository owns only deterministic reads over already-governed reference
artefacts. It does not perform external fetches, orchestration, or packet
carriage.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from nvda_desk.calendar.reference.importer import FinancialCalendarImporter
from nvda_desk.contracts.reference_data import ImportedReferenceBundle


class ReferenceRepository:
    """Load governed reference bundle artefacts into typed contracts."""

    def __init__(self, repo_root: Path | None = None):
        self._repo_root = repo_root
        self._importer = FinancialCalendarImporter(repo_root=repo_root)

    @property
    def repo_root(self) -> Path | None:
        """Return the optional repo root used for bundle-relative reads."""
        return self._repo_root

    def load_bundle_manifest(self, manifest: Mapping[str, Any]) -> ImportedReferenceBundle:
        """Return one imported reference bundle from a manifest mapping."""
        return self._importer.load_manifest(manifest)

    def load_bundle_from_json(self, path: str | Path) -> ImportedReferenceBundle:
        """Return one imported reference bundle from a JSON manifest file."""
        manifest_path = Path(path)
        with manifest_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return self.load_bundle_manifest(payload)
