#!/usr/bin/env python3
"""Write bounded-intake manifests for the post-row044 linkage-gap intake repair.

The manifests deliberately cover the bounded packet/control artefacts and actually
read control/normative files. They do not claim full-read coverage over the full
536k-line global evidence sources.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
TARGET_TRANCHE = "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_POST_ROW044_RECONCILIATION"
CURRENT_TARGET_MANIFEST = Path(
    "var/audit/active_code_atlas_001/full_read_manifests/"
    "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_POST_ROW044_RECONCILIATION_FULL_READ_MANIFEST.json"
)
PACKET_MANIFEST = Path(
    "var/audit/active_code_atlas_001/full_read_manifests/"
    "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_INTAKE_CONTROL_REPAIR_FULL_READ_MANIFEST.json"
)

ENTRY_PATHS = [
    ("control", "AGENTS.md"),
    ("control", "PLANS.md"),
    ("control", "ROADMAP_LEDGER.md"),
    ("normative", "docs/00_CONTROL_SURFACE_ROUTING_INDEX.md"),
    ("normative", "docs/01_NORMATIVE_CORE.md"),
    ("normative", "docs/08_TESTING_AND_PROMOTION_CORE.md"),
    ("normative", "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md"),
    ("architecture_map", "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md"),
    (
        "handoff_receipt",
        "var/audit/active_code_atlas_001/handoff_control_repair_001/receipts/"
        "ACTIVE_CODE_ATLAS_HANDOFF_CONTROL_REPAIR_001_RECEIPT.md",
    ),
    (
        "validator",
        "var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py",
    ),
    (
        "bounded_intake_tool",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/tools/"
        "extract_bounded_reconciliation_packet.py",
    ),
    (
        "bounded_intake_tool",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/tools/"
        "write_bounded_intake_manifests.py",
    ),
    (
        "bounded_intake_packet",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/packet/"
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET.json",
    ),
    (
        "bounded_intake_report",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/"
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET_REPORT.json",
    ),
    (
        "bounded_intake_report",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/"
        "extract_bounded_reconciliation_packet.stdout.json",
    ),
    (
        "bounded_intake_report",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/"
        "extract_bounded_reconciliation_packet.status",
    ),
    (
        "bounded_intake_control_artifact",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/"
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_INTAKE_CONTROL_ARTEFACT.md",
    ),
    (
        "bounded_intake_receipt",
        "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/receipts/"
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_INTAKE_CONTROL_REPAIR_RECEIPT.md",
    ),
]


def file_entry(material_class: str, rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    data = path.read_bytes()
    text = data.decode("utf-8")
    line_count = len(text.splitlines())
    return {
        "path": rel_path,
        "material_class": material_class,
        "byte_count": len(data),
        "line_count": line_count,
        "sha256": hashlib.sha256(data).hexdigest(),
        "full_read": True,
        "read_method": "line_numbered_full_read_in_worker_thread_or_author_generated_then_full_read",
        "read_ranges": [{"start_line": 1, "end_line": line_count}],
        "notes": "Bounded-intake control repair evidence; does not claim full-read coverage over excluded global source files.",
    }


def write_manifest(path: Path, manifest_id: str, scope: str) -> None:
    entries = [file_entry(material_class, rel_path) for material_class, rel_path in ENTRY_PATHS]
    payload = {
        "schema_version": 1,
        "manifest_id": manifest_id,
        "target_tranche": TARGET_TRANCHE,
        "manifest_scope": scope,
        "status": "bounded_intake_control_repair_evidence_not_reconciliation_closure",
        "full_read_false_count": 0,
        "entry_count": len(entries),
        "entries": entries,
        "exclusion_note": (
            "The prior 536k-line global material source set is intentionally not represented as full-read evidence. "
            "This manifest points the current target to the bounded packet and actually read control/normative/control-repair files only."
        ),
        "next_gate": (
            "Before substantive reconciliation, read the bounded packet in full and use current hash evidence; "
            "do not treat this packet-creation repair as target closure."
        ),
    }
    (ROOT / path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_manifest(
        CURRENT_TARGET_MANIFEST,
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_POST_ROW044_RECONCILIATION_FULL_READ_MANIFEST",
        "current_target_regenerated_to_bounded_intake_packet",
    )
    write_manifest(
        PACKET_MANIFEST,
        "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_INTAKE_CONTROL_REPAIR_FULL_READ_MANIFEST",
        "bounded_packet_control_repair_manifest",
    )
    print(CURRENT_TARGET_MANIFEST.as_posix())
    print(PACKET_MANIFEST.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
