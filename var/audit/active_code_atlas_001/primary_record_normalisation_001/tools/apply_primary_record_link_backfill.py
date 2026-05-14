#!/usr/bin/env python3
"""Backfill explicit ACABC/ACATQ links from bounded reconciliation into primary source records.

This mutates only the read-adjudicated audit record file for vocabulary governance.
It does not mutate source, tests, runtime behaviour, dependencies, vocabulary data,
original Atlas/Bridge JSON, or generated slices.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
ACTIVE_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
SOURCE_RECORD_PATH = ACTIVE_DIR / "vocabulary_governance_surface" / "vocabulary_governance_active_code_atlas_records.json"
RECONCILIATION_PATH = ACTIVE_DIR / "primary_linkage_gap_reconciliation_002" / "primary_linkage_gap_reconciliation_002.json"
REPORT_PATH = ACTIVE_DIR / "primary_record_normalisation_001" / "reports" / "ACTIVE_CODE_ATLAS_PRIMARY_RECORD_NORMALISATION_001_REPORT.json"

ALLOWED_BACKFILL: dict[str, list[str]] = {
    "ACAV-001-0001": ["ACABC-0047", "ACATQ-0046"],
    "ACAV-001-0002": ["ACABC-0046", "ACATQ-0045"],
    "ACAV-001-0003": ["ACABC-0046", "ACATQ-0045"],
    "ACAV-001-0004": ["ACABC-0047", "ACATQ-0046"],
    "ACAV-001-0005": ["ACABC-0047", "ACATQ-0046"],
    "ACAV-001-0006": ["ACABC-0048"],
    "ACAV-001-0007": ["ACABC-0046", "ACATQ-0045"],
    "ACAV-001-0008": ["ACABC-0045", "ACATQ-0044"],
}
EXPECTED_NO_PRIMARY_LINK_COMPARISON_IDS = ["ACABC-0035"]


def repo_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def repo_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def meta(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "byte_count": len(data),
        "line_count": 0 if not data else data.count(b"\n") + (0 if data.endswith(b"\n") else 1),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    source_before = meta(SOURCE_RECORD_PATH)
    payload = json.loads(SOURCE_RECORD_PATH.read_text(encoding="utf-8"))
    reconciliation = json.loads(RECONCILIATION_PATH.read_text(encoding="utf-8"))

    errors: list[str] = []
    warnings: list[str] = []
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise SystemExit("records field missing or not a list")
    by_id = {record.get("active_code_atlas_record_id"): record for record in records if isinstance(record, dict)}

    reconciliation_primary_ids = sorted(
        {
            link["primary_record_id"]
            for item in reconciliation.get("queue_reconciliations", []) + reconciliation.get("comparison_reconciliations", [])
            for link in item.get("nis_linked_primary_records", [])
            if link.get("primary_record_id")
        }
    )
    expected_primary_ids = sorted(ALLOWED_BACKFILL)
    if reconciliation_primary_ids != expected_primary_ids:
        errors.append(
            f"reconciliation_primary_ids_mismatch:expected={expected_primary_ids}:actual={reconciliation_primary_ids}"
        )

    no_primary_link_comparison_ids = sorted(
        item.get("comparison_record_id")
        for item in reconciliation.get("comparison_reconciliations", [])
        if not item.get("nis_linked_primary_records")
    )
    if no_primary_link_comparison_ids != EXPECTED_NO_PRIMARY_LINK_COMPARISON_IDS:
        errors.append(
            "unexpected_no_primary_link_comparison_ids:"
            f"expected={EXPECTED_NO_PRIMARY_LINK_COMPARISON_IDS}:actual={no_primary_link_comparison_ids}"
        )

    changed_records: list[dict[str, Any]] = []
    added_links: list[dict[str, Any]] = []
    for record_id, links_to_add in ALLOWED_BACKFILL.items():
        record = by_id.get(record_id)
        if record is None:
            errors.append(f"source_record_missing:{record_id}")
            continue
        existing = record.get("linked_bridge_record_ids")
        if not isinstance(existing, list):
            errors.append(f"linked_bridge_record_ids_not_list:{record_id}")
            continue
        original = list(existing)
        for link in links_to_add:
            if link not in existing:
                existing.append(link)
                added_links.append({"active_code_atlas_record_id": record_id, "link_added": link})
        if original != existing:
            record["linked_bridge_record_ids"] = sorted(existing, key=lambda value: (not str(value).startswith("NIS-"), str(value)))
            notes = record.setdefault("adjudication_notes", [])
            if not isinstance(notes, list):
                errors.append(f"adjudication_notes_not_list:{record_id}")
                continue
            note = (
                "Primary-record normalisation 001 added explicit ACABC/ACATQ audit links from "
                "post-row044 bounded reconciliation; this is linkage metadata only and does not change source/test/runtime semantics."
            )
            if note not in notes:
                notes.append(note)
            changed_records.append(
                {
                    "active_code_atlas_record_id": record_id,
                    "links_before": original,
                    "links_after": record["linked_bridge_record_ids"],
                }
            )

    if not added_links:
        warnings.append("no_new_links_added; file may already be normalised")

    if not errors:
        SOURCE_RECORD_PATH.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    report = {
        "schema_version": "primary_record_normalisation_v1",
        "status": "PASS" if not errors else "FAIL",
        "classification_note": "AUDIT_LINKAGE_METADATA_BACKFILL_ONLY",
        "source_repo_branch": repo_branch(),
        "source_repo_head_before_backfill": repo_head(),
        "limitation_statement": (
            "This normalisation pass adds explicit ACABC/ACATQ audit links to read-adjudicated primary source records "
            "where the bounded post-row044 reconciliation already established NIS-to-primary linkage. It does not mutate "
            "runtime/source/test/dependency/vocabulary/original Atlas/Bridge/generated-slice material and does not prove feature maturity."
        ),
        "source_record_file_before": source_before,
        "source_record_file_after": meta(SOURCE_RECORD_PATH) if not errors else None,
        "reconciliation_input": meta(RECONCILIATION_PATH),
        "allowed_backfill": ALLOWED_BACKFILL,
        "expected_no_primary_link_comparison_ids": EXPECTED_NO_PRIMARY_LINK_COMPARISON_IDS,
        "changed_record_count": len(changed_records),
        "added_link_count": len(added_links),
        "changed_records": changed_records,
        "added_links": added_links,
        "errors": errors,
        "warnings": warnings,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
