from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LegacyExtractionService:
    def __init__(self, repo_root: Path):
        self._repo_root = repo_root

    def load_jsonl(self, relative_path: str) -> list[dict[str, Any]]:
        path = self._repo_root / relative_path
        if not path.exists():
            raise ValueError(f"missing extraction artefact: {relative_path}")
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

    def inventory_summary(self) -> dict[str, Any]:
        items = self.load_jsonl("backlog/remaining_legacy_source_inventory.jsonl")
        return {
            "document_count": len(items),
            "documents": [item["document_name"] for item in items],
        }

    def fixture_summary(self) -> dict[str, Any]:
        rows = self.load_jsonl("backlog/legacy_data_fixtures_manifest.jsonl")
        return {
            "fixture_candidate_count": len(rows),
            "documents": sorted({row["source_document"] for row in rows}),
        }
