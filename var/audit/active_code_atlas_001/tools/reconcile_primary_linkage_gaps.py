#!/usr/bin/env python3
"""Reconcile primary-to-Bridge linkage gaps without mutating primary, Atlas, Bridge, tests, or source."""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
OUT_DIR = ACTIVE_DIR / "primary_linkage_gap_reconciliation"
PRIMARY_PATH = ACTIVE_DIR / "primary_active_code_atlas.json"
COMPARISON_OUTPUT_PATH = (
    ACTIVE_DIR / "primary_to_bridge_comparison" / "primary_to_bridge_comparison.json"
)
BRIDGE_PATH = (
    ROOT
    / "var"
    / "audit"
    / "ledgers"
    / "intent_migration"
    / "native_intent_satisfaction_ledger.json"
)
STATIC_COMPARISON_PATH = (
    ROOT
    / "var"
    / "audit"
    / "active_code_atlas_bridge_comparison_001"
    / "active_code_atlas_bridge_comparison.json"
)
QUEUE_PATH = (
    ROOT
    / "var"
    / "audit"
    / "active_code_atlas_bridge_comparison_001"
    / "active_code_atlas_test_first_execution_queue.json"
)
OUTPUT_PATH = OUT_DIR / "primary_linkage_gap_reconciliation.json"
REPORT_PATH = OUT_DIR / "reports" / "primary_linkage_gap_reconciliation_report.json"

LIMITATION_STATEMENT = (
    "Linkage-gap reconciliation is audit evidence only. It explains unmatched primary-to-Bridge links and selects "
    "the next bounded target where an execution-queue gap remains; it does not mutate primary records, source, "
    "tests, Atlas/Bridge inputs, vocabulary, dependencies, or generated slices."
)
NEXT_UNRESOLVED_TARGET = "ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_044_PLAYBOOK_LIBRARY_ARCHITECTURE_SURFACE_TRANSFORM_REQUIRED"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(cmd: list[str]) -> str:
    return subprocess.check_output(["git", *cmd], cwd=ROOT, text=True).strip()


def sample(values: set[str] | list[str], limit: int = 12) -> list[str]:
    return sorted(str(v) for v in values)[:limit]


def bridge_group_key(record: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    proof = record.get("proof_resolution") or {}
    return (
        str(record.get("blueprint_surface") or "unresolved"),
        str(record.get("target_owner") or "unresolved"),
        str(proof.get("tier") or "unresolved"),
        str(proof.get("test_family_action") or "unresolved"),
        str(proof.get("proof_block_action") or "unresolved"),
        str(record.get("implementation_leaf_type") or "unresolved"),
    )


def comparison_group_key(record: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(record.get("blueprint_surface") or "unresolved"),
        str(record.get("target_owner") or "unresolved"),
        str(record.get("proof_tier") or "unresolved"),
        str(record.get("bridge_test_family_action") or "unresolved"),
        str(record.get("bridge_proof_block_action") or "unresolved"),
        str(record.get("implementation_leaf_type") or "unresolved"),
    )


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    primary = load_json(PRIMARY_PATH)
    comparison_output = load_json(COMPARISON_OUTPUT_PATH)
    bridge = load_json(BRIDGE_PATH)
    static_comparison = load_json(STATIC_COMPARISON_PATH)
    queue = load_json(QUEUE_PATH)

    primary_records = primary.get("records", [])
    bridge_records = bridge.get("records", [])
    comparison_records = static_comparison.get("records", [])
    queue_records = queue.get("records", [])

    comparison_by_id = {r.get("comparison_record_id"): r for r in comparison_records}
    queue_by_id = {r.get("queue_record_id"): r for r in queue_records}
    bridge_by_id = {r.get("satisfaction_record_id"): r for r in bridge_records}
    comparison_id_by_group = {
        comparison_group_key(r): r.get("comparison_record_id") for r in comparison_records
    }

    primary_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    primary_direct_comparison_links: dict[str, list[str]] = defaultdict(list)
    primary_direct_queue_links: dict[str, list[str]] = defaultdict(list)
    primary_nis_to_comparison_links: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in primary_records:
        record_id = str(record.get("active_code_atlas_record_id"))
        surface = str(record.get("surface") or "unresolved")
        primary_by_surface[surface].append(record)
        for link in record.get("linked_bridge_record_ids", []) or []:
            if not isinstance(link, str):
                continue
            if link.startswith("ACABC-"):
                primary_direct_comparison_links[link].append(record_id)
            elif link.startswith("ACATQ-"):
                primary_direct_queue_links[link].append(record_id)
            elif link.startswith("NIS-") and link in bridge_by_id:
                mapped = comparison_id_by_group.get(bridge_group_key(bridge_by_id[link]))
                if mapped:
                    primary_nis_to_comparison_links[mapped].append(
                        {"primary_record_id": record_id, "satisfaction_record_id": link}
                    )

    input_queue_gaps = [
        r.get("queue_record_id") for r in comparison_output.get("queue_gap_records", [])
    ]
    input_comparison_gaps = [
        r.get("comparison_record_id") for r in comparison_output.get("comparison_gap_records", [])
    ]

    queue_reconciliations: list[dict[str, Any]] = []
    comparison_reconciliations: list[dict[str, Any]] = []

    for comparison_id in input_comparison_gaps:
        comp = comparison_by_id.get(comparison_id)
        if comp is None:
            errors.append(f"missing_static_comparison_gap_record:{comparison_id}")
            continue
        surface = str(comp.get("blueprint_surface"))
        direct_records = primary_direct_comparison_links.get(str(comparison_id), [])
        nis_records = primary_nis_to_comparison_links.get(str(comparison_id), [])
        same_surface_records = [
            str(r.get("active_code_atlas_record_id")) for r in primary_by_surface.get(surface, [])
        ]
        status = "unresolved_primary_linkage_gap"
        recommended = "create_or_repair_read_adjudicated_primary_record_linkage_before_full_reconciliation_claim"
        if direct_records:
            status = "reconciled_by_direct_primary_comparison_link"
            recommended = "no_follow_on_required_for_this_group"
        elif nis_records:
            status = "reconciled_by_primary_satisfaction_record_links"
            recommended = "optionally backfill explicit ACABC/ACATQ links in a future primary-record-normalisation pass"
        elif comp.get("test_first_queue_action") == "confirm_existing_proof_only_no_refactor":
            status = "nonqueue_confirm_only_gap"
            recommended = (
                "retain_as_comparison_only_non_execution_gap_no_test_or_source_row_selected"
            )
        comparison_reconciliations.append(
            {
                "comparison_record_id": comparison_id,
                "surface": surface,
                "comparison_status": comp.get("comparison_status"),
                "test_first_queue_action": comp.get("test_first_queue_action"),
                "reconciliation_status": status,
                "direct_primary_record_ids": direct_records,
                "nis_linked_primary_records": nis_records,
                "same_surface_primary_record_ids": same_surface_records,
                "recommended_next_action": recommended,
            }
        )

    for queue_id in input_queue_gaps:
        queue_record = queue_by_id.get(queue_id)
        if queue_record is None:
            errors.append(f"missing_queue_gap_record:{queue_id}")
            continue
        comparison_id = queue_record.get("comparison_record_id")
        comp_recon = next(
            (
                record
                for record in comparison_reconciliations
                if record["comparison_record_id"] == comparison_id
            ),
            None,
        )
        direct_records = primary_direct_queue_links.get(str(queue_id), [])
        status = "unresolved_execution_queue_linkage_gap"
        recommended = NEXT_UNRESOLVED_TARGET
        if direct_records:
            status = "reconciled_by_direct_primary_queue_link"
            recommended = "no_follow_on_required_for_this_queue_row"
        elif (
            comp_recon
            and comp_recon["reconciliation_status"]
            == "reconciled_by_primary_satisfaction_record_links"
        ):
            status = "reconciled_via_comparison_group_satisfaction_links"
            recommended = "optionally backfill explicit ACATQ link in a future primary-record-normalisation pass"
        queue_reconciliations.append(
            {
                "queue_record_id": queue_id,
                "comparison_record_id": comparison_id,
                "surface": queue_record.get("blueprint_surface"),
                "required_action": queue_record.get("required_action"),
                "reconciliation_status": status,
                "direct_primary_record_ids": direct_records,
                "comparison_reconciliation_status": (
                    comp_recon["reconciliation_status"] if comp_recon else None
                ),
                "recommended_next_action": recommended,
            }
        )

    comparison_status_counts = Counter(
        r["reconciliation_status"] for r in comparison_reconciliations
    )
    queue_status_counts = Counter(r["reconciliation_status"] for r in queue_reconciliations)
    unresolved_queue = [
        r["queue_record_id"]
        for r in queue_reconciliations
        if r["reconciliation_status"].startswith("unresolved")
    ]
    unresolved_comparison = [
        r["comparison_record_id"]
        for r in comparison_reconciliations
        if r["reconciliation_status"] == "unresolved_primary_linkage_gap"
    ]
    if unresolved_queue or unresolved_comparison:
        warnings.append(
            "unresolved_linkage_gaps_remain:queue="
            + repr(unresolved_queue)
            + ":comparison="
            + repr(unresolved_comparison)
        )

    summary = {
        "input_queue_gap_count": len(input_queue_gaps),
        "input_comparison_gap_count": len(input_comparison_gaps),
        "queue_reconciliation_status_counts": dict(sorted(queue_status_counts.items())),
        "comparison_reconciliation_status_counts": dict(sorted(comparison_status_counts.items())),
        "unresolved_execution_queue_gap_count": len(unresolved_queue),
        "unresolved_comparison_gap_count": len(unresolved_comparison),
        "unresolved_execution_queue_gap_ids": unresolved_queue,
        "unresolved_comparison_gap_ids": unresolved_comparison,
        "next_target": NEXT_UNRESOLVED_TARGET if unresolved_queue else "none_selected",
    }
    output = {
        "schema_version": "primary_linkage_gap_reconciliation_v1",
        "created_utc": "2026-05-12T00:00:00Z",
        "status": (
            "reconciliation_recorded_with_unresolved_execution_gap"
            if unresolved_queue
            else "reconciliation_recorded_no_unresolved_execution_gap"
        ),
        "classification_note": "AUDIT_RECONCILIATION_ONLY",
        "limitation_statement": LIMITATION_STATEMENT,
        "source_repo_branch": git(["branch", "--show-current"]),
        "source_repo_head": git(["rev-parse", "--short", "HEAD"]),
        "inputs": {
            "primary_active_code_atlas_path": str(PRIMARY_PATH.relative_to(ROOT)),
            "primary_to_bridge_comparison_path": str(COMPARISON_OUTPUT_PATH.relative_to(ROOT)),
            "native_intent_satisfaction_ledger_path": str(BRIDGE_PATH.relative_to(ROOT)),
            "static_comparison_path": str(STATIC_COMPARISON_PATH.relative_to(ROOT)),
            "execution_queue_path": str(QUEUE_PATH.relative_to(ROOT)),
        },
        "summary": summary,
        "comparison_reconciliations": comparison_reconciliations,
        "queue_reconciliations": queue_reconciliations,
    }
    report = {
        "validation_status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
        "limitation_statement": LIMITATION_STATEMENT,
        "output_path": str(OUTPUT_PATH.relative_to(ROOT)),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
