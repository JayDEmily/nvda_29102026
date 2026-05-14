#!/usr/bin/env python3
"""Reconcile post-row044 primary linkage gaps from the bounded evidence packet only.

This tool deliberately does not read the full Atlas, Bridge, comparison, queue,
primary Atlas, source, test, vocabulary, dependency, or generated slice inputs.
Those global material files were reduced into the bounded packet by the prior
control-gate repair. This pass consumes that small packet as the material
source so the reconciliation can be audited without pretending that the global
536k-line source set was read.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
PACKET_PATH = (
    ACTIVE_DIR
    / "bounded_reconciliation_intake_001"
    / "packet"
    / "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET.json"
)
OUT_DIR = ACTIVE_DIR / "primary_linkage_gap_reconciliation_002"
OUTPUT_PATH = OUT_DIR / "primary_linkage_gap_reconciliation_002.json"
REPORT_PATH = OUT_DIR / "reports" / "primary_linkage_gap_reconciliation_002_report.json"

EXPECTED_QUEUE_IDS = ["ACATQ-0044", "ACATQ-0045", "ACATQ-0046"]
EXPECTED_COMPARISON_IDS = [
    "ACABC-0035",
    "ACABC-0045",
    "ACABC-0046",
    "ACABC-0047",
    "ACABC-0048",
]

LIMITATION_STATEMENT = (
    "Post-row044 linkage-gap reconciliation is audit evidence only. It classifies "
    "the bounded residual primary-to-Bridge queue/comparison gaps from the bounded "
    "evidence packet; it does not mutate primary active-code Atlas records, source, "
    "tests, Atlas/Bridge inputs, vocabulary, dependencies, or generated slices."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(cmd: list[str]) -> str:
    return subprocess.check_output(["git", *cmd], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ids(records: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(record[key]) for record in records)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    packet = load_json(PACKET_PATH)
    records = packet.get("records", {})
    queue_gap_records = as_list(records.get("primary_to_bridge_queue_gap_records"))
    comparison_gap_records = as_list(records.get("primary_to_bridge_comparison_gap_records"))
    static_comparison_records = as_list(records.get("static_bridge_comparison_records"))
    static_queue_records = as_list(records.get("static_test_first_queue_records"))
    native_records = as_list(records.get("native_intent_satisfaction_records"))
    primary_probe_records = as_list(records.get("primary_active_code_direct_link_probe_records"))

    queue_ids = ids(queue_gap_records, "queue_record_id")
    comparison_ids = ids(comparison_gap_records, "comparison_record_id")
    if queue_ids != EXPECTED_QUEUE_IDS:
        errors.append(f"unexpected_queue_gap_ids:{queue_ids}")
    if comparison_ids != EXPECTED_COMPARISON_IDS:
        errors.append(f"unexpected_comparison_gap_ids:{comparison_ids}")

    packet_check = packet.get("no_unrelated_ids_check", {})
    if packet_check.get("status") != "PASS" or packet_check.get("errors"):
        errors.append("packet_no_unrelated_ids_check_not_pass")

    queue_by_id = {str(record["queue_record_id"]): record for record in queue_gap_records}
    static_queue_by_id = {str(record["queue_record_id"]): record for record in static_queue_records}
    comparison_by_id = {
        str(record["comparison_record_id"]): record for record in comparison_gap_records
    }
    static_comparison_by_id = {
        str(record["comparison_record_id"]): record for record in static_comparison_records
    }
    native_by_id = {
        str(record["satisfaction_record_id"]): record for record in native_records
    }

    primary_by_nis: dict[str, list[str]] = defaultdict(list)
    primary_by_surface: dict[str, list[str]] = defaultdict(list)
    primary_atlas_links: dict[str, list[str]] = defaultdict(list)
    for primary in primary_probe_records:
        primary_id = str(primary.get("active_code_atlas_record_id"))
        surface = str(primary.get("surface") or "unresolved")
        primary_by_surface[surface].append(primary_id)
        for bridge_id in as_list(primary.get("linked_bridge_record_ids")):
            primary_by_nis[str(bridge_id)].append(primary_id)
        for atlas_id in as_list(primary.get("linked_atlas_record_ids")):
            primary_atlas_links[str(atlas_id)].append(primary_id)

    comparison_reconciliations: list[dict[str, Any]] = []
    for comparison_id in EXPECTED_COMPARISON_IDS:
        gap = comparison_by_id.get(comparison_id)
        static = static_comparison_by_id.get(comparison_id)
        if not gap or not static:
            errors.append(f"missing_comparison_record:{comparison_id}")
            continue
        surface = str(gap.get("surface") or static.get("blueprint_surface"))
        relevant_native_records = [
            record
            for record in native_records
            if str(record.get("blueprint_surface")) == surface
            and str(record.get("target_owner")) == str(static.get("target_owner"))
            and str(record.get("proof_resolution", {}).get("tier")) == str(static.get("proof_tier"))
            and str(record.get("proof_resolution", {}).get("test_family_action"))
            == str(static.get("bridge_test_family_action"))
            and str(record.get("proof_resolution", {}).get("proof_block_action"))
            == str(static.get("bridge_proof_block_action"))
            and str(record.get("implementation_leaf_type"))
            == str(static.get("implementation_leaf_type"))
        ]
        native_ids = sorted(str(record["satisfaction_record_id"]) for record in relevant_native_records)
        linked_primary: list[dict[str, str]] = []
        for native_id in native_ids:
            for primary_id in primary_by_nis.get(native_id, []):
                linked_primary.append(
                    {"primary_record_id": primary_id, "satisfaction_record_id": native_id}
                )

        if linked_primary:
            status = "reconciled_by_primary_satisfaction_record_links"
            next_action = (
                "no execution queue target remains for this comparison group; "
                "explicit ACABC/ACATQ primary-link backfill may be handled only in a "
                "future primary-record-normalisation pass"
            )
        elif gap.get("test_first_queue_action") == "confirm_existing_proof_only_no_refactor":
            status = "nonqueue_confirm_only_gap_retained_no_execution_row"
            next_action = (
                "retain as comparison-only confirm-existing-proof group; no test-first "
                "queue row is selected by the bounded packet"
            )
        else:
            status = "unresolved_primary_linkage_gap"
            next_action = (
                "create_or_repair_read_adjudicated_primary_record_linkage_before_full_reconciliation_claim"
            )

        comparison_reconciliations.append(
            {
                "comparison_record_id": comparison_id,
                "surface": surface,
                "target_owner": gap.get("target_owner") or static.get("target_owner"),
                "comparison_status": gap.get("comparison_status"),
                "test_first_queue_action": gap.get("test_first_queue_action"),
                "reconciliation_status": status,
                "packet_static_bridge_record_count": static.get("bridge_record_count"),
                "packet_static_native_satisfaction_status_counts": static.get(
                    "bridge_native_satisfaction_status_counts", {}
                ),
                "matched_satisfaction_record_ids": native_ids,
                "nis_linked_primary_records": linked_primary,
                "same_surface_primary_probe_record_ids": sorted(primary_by_surface.get(surface, [])),
                "recommended_next_action": next_action,
            }
        )

    comparison_status_by_id = {
        record["comparison_record_id"]: record for record in comparison_reconciliations
    }
    queue_reconciliations: list[dict[str, Any]] = []
    for queue_id in EXPECTED_QUEUE_IDS:
        gap = queue_by_id.get(queue_id)
        static = static_queue_by_id.get(queue_id)
        if not gap or not static:
            errors.append(f"missing_queue_record:{queue_id}")
            continue
        comparison_id = str(gap.get("comparison_record_id"))
        comp = comparison_status_by_id.get(comparison_id)
        if comp and comp["reconciliation_status"] == "reconciled_by_primary_satisfaction_record_links":
            status = "reconciled_via_comparison_group_satisfaction_links"
            next_action = "no execution queue target remains for this queue row"
        else:
            status = "unresolved_execution_queue_linkage_gap"
            next_action = "select_this_queue_row_as_next_test_first_execution_target"
        queue_reconciliations.append(
            {
                "queue_record_id": queue_id,
                "comparison_record_id": comparison_id,
                "surface": gap.get("surface") or static.get("blueprint_surface"),
                "required_action": gap.get("required_action") or static.get("required_action"),
                "comparison_status": gap.get("comparison_status") or static.get("comparison_status"),
                "reconciliation_status": status,
                "comparison_reconciliation_status": comp.get("reconciliation_status") if comp else None,
                "matched_satisfaction_record_ids": comp.get("matched_satisfaction_record_ids", []) if comp else [],
                "nis_linked_primary_records": comp.get("nis_linked_primary_records", []) if comp else [],
                "recommended_next_action": next_action,
            }
        )

    comparison_counts = Counter(
        record["reconciliation_status"] for record in comparison_reconciliations
    )
    queue_counts = Counter(record["reconciliation_status"] for record in queue_reconciliations)
    unresolved_queue_ids = [
        record["queue_record_id"]
        for record in queue_reconciliations
        if record["reconciliation_status"] == "unresolved_execution_queue_linkage_gap"
    ]
    unresolved_comparison_ids = [
        record["comparison_record_id"]
        for record in comparison_reconciliations
        if record["reconciliation_status"] == "unresolved_primary_linkage_gap"
    ]

    if unresolved_queue_ids or unresolved_comparison_ids:
        status = "reconciliation_recorded_with_unresolved_gaps"
        warnings.append(
            "unresolved_linkage_gaps_remain:"
            f"queue={unresolved_queue_ids}:comparison={unresolved_comparison_ids}"
        )
        next_target = "select_next_unresolved_execution_queue_gap"
    else:
        status = "reconciliation_recorded_no_unresolved_execution_queue_gaps"
        next_target = "no_unresolved_execution_queue_gap_in_bounded_post_row044_packet"

    output = {
        "schema_version": "primary_linkage_gap_reconciliation_v2_bounded_packet",
        "status": status,
        "classification_note": "AUDIT_RECONCILIATION_ONLY",
        "limitation_statement": LIMITATION_STATEMENT,
        "source_repo_branch": git(["branch", "--show-current"]),
        "source_repo_head": git(["rev-parse", "HEAD"]),
        "inputs": {
            "bounded_packet_path": str(PACKET_PATH.relative_to(ROOT)),
            "bounded_packet_sha256": sha256(PACKET_PATH),
            "bounded_packet_line_count": len(PACKET_PATH.read_text(encoding="utf-8").splitlines()),
            "requested_queue_record_ids": EXPECTED_QUEUE_IDS,
            "requested_comparison_record_ids": EXPECTED_COMPARISON_IDS,
            "packet_source_repo_head": packet.get("source_repo_head"),
            "full_global_source_set_used": False,
        },
        "summary": {
            "input_queue_gap_count": len(queue_reconciliations),
            "input_comparison_gap_count": len(comparison_reconciliations),
            "queue_reconciliation_status_counts": dict(sorted(queue_counts.items())),
            "comparison_reconciliation_status_counts": dict(sorted(comparison_counts.items())),
            "unresolved_execution_queue_gap_count": len(unresolved_queue_ids),
            "unresolved_comparison_gap_count": len(unresolved_comparison_ids),
            "unresolved_execution_queue_gap_ids": unresolved_queue_ids,
            "unresolved_comparison_gap_ids": unresolved_comparison_ids,
            "next_target": next_target,
        },
        "comparison_reconciliations": comparison_reconciliations,
        "queue_reconciliations": queue_reconciliations,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if errors:
        validation_status = "FAIL"
    else:
        validation_status = "PASS"
    report = {
        "validation_status": validation_status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "summary": output["summary"],
        "output_path": str(OUTPUT_PATH.relative_to(ROOT)),
        "limitation_statement": LIMITATION_STATEMENT,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
