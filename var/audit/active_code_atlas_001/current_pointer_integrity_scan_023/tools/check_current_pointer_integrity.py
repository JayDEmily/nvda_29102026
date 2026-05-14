#!/usr/bin/env python3
"""Check that the live ROADMAP pointer is backed by current artefacts."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
TARGET = "ACTIVE_NARROW_PLACEHOLDER_SCAN_CLASSIFICATION_022_RECORDED"
NEXT_TARGET = "ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_023"
REPORT_PATH = ROOT / "var/audit/active_code_atlas_001/current_pointer_integrity_scan_023/reports/ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_023_REPORT.json"

EXPECTED_ARTEFACTS = [
    "var/audit/active_code_atlas_001/narrow_placeholder_scan_classification_022/reports/ACTIVE_NARROW_PLACEHOLDER_SCAN_CLASSIFICATION_022_REPORT.json",
    "var/audit/active_code_atlas_001/narrow_placeholder_scan_classification_022/receipts/ACTIVE_NARROW_PLACEHOLDER_SCAN_CLASSIFICATION_022_RECEIPT.md",
    "var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_NARROW_PLACEHOLDER_SCAN_CLASSIFICATION_022_FULL_READ_MANIFEST.json",
]


def metadata(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "byte_count": len(data),
        "line_count": 0 if not data else data.count(b"\n") + (0 if data.endswith(b"\n") else 1),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    roadmap = read_text("ROADMAP_LEDGER.md")
    plans = read_text("PLANS.md")
    agents = read_text("AGENTS.md")

    current_pointer_match = re.search(r"\| Current phase \| `([^`]+)`", roadmap)
    current_tranche_match = re.search(r"\| Current target tranche \| `([^`]+)`", roadmap)
    current_pointer = current_pointer_match.group(1) if current_pointer_match else None
    current_tranche = current_tranche_match.group(1) if current_tranche_match else None

    errors: list[str] = []
    warnings: list[str] = []
    if current_pointer != TARGET:
        errors.append(f"current_phase_mismatch:expected={TARGET}:actual={current_pointer}")
    if current_tranche != TARGET:
        errors.append(f"current_target_tranche_mismatch:expected={TARGET}:actual={current_tranche}")
    if TARGET not in roadmap:
        errors.append(f"target_missing_from_roadmap:{TARGET}")
    if "Continue the next lawful control/audit/evidence/manifest/receipt/ledger hardening leaf" not in roadmap:
        warnings.append("roadmap_next_supporting_tranche_continuation_phrase_not_found")
    if "continue-until-tokens" not in plans and "context/token exhaustion" not in plans:
        warnings.append("plans_continuation_language_not_detected")
    if "User-directed continuation law" not in agents:
        errors.append("agents_user_directed_continuation_law_missing")

    artefact_status: list[dict[str, Any]] = []
    for rel in EXPECTED_ARTEFACTS:
        path = ROOT / rel
        entry: dict[str, Any] = {"path": rel, "exists": path.exists(), "is_file": path.is_file()}
        if path.is_file():
            entry.update(metadata(path))
        else:
            errors.append(f"expected_artefact_missing:{rel}")
        artefact_status.append(entry)

    manifest_path = ROOT / EXPECTED_ARTEFACTS[-1]
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("target_tranche") != "ACTIVE_NARROW_PLACEHOLDER_SCAN_CLASSIFICATION_022":
            errors.append("manifest_target_tranche_unexpected")
        if manifest.get("full_read_false_count") != 0:
            errors.append(f"manifest_full_read_false_count_nonzero:{manifest.get('full_read_false_count')}")
        if manifest.get("entry_count") != len(manifest.get("entries", [])):
            errors.append("manifest_entry_count_does_not_match_entries_length")

    report = {
        "schema_version": 1,
        "target_tranche": NEXT_TARGET,
        "status": "PASS" if not errors else "FAIL",
        "scope": "current_pointer_integrity_scan_after_022",
        "checked_pointer_target": TARGET,
        "current_phase": current_pointer,
        "current_target_tranche": current_tranche,
        "expected_artefacts": artefact_status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "new_live_control_defect_selected": bool(errors),
        "runtime_source_test_mutation_opened": False,
        "dependency_mutation_opened": False,
        "vocabulary_data_mutation_opened": False,
        "original_atlas_bridge_mutation_opened": False,
        "generated_slice_rebuild_opened": False,
        "archive_payload_restored_or_used": False,
        "proof": {
            "final_proof_status": "PENDING_FINAL_VALIDATION"
        },
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
