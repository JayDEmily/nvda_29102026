#!/usr/bin/env python3
"""Compare synthesized primary active-code Atlas records to read-only Atlas/Bridge evidence.

This is an audit/control artefact generator. It does not mutate source, tests,
original Atlas/Bridge JSON, generated Atlas slices, vocabulary, dependencies, or
runtime code.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
OUT_DIR = ACTIVE_DIR / "primary_to_bridge_comparison"
PRIMARY_PATH = ACTIVE_DIR / "primary_active_code_atlas.json"
ATLAS_PATH = ROOT / "var" / "audit" / "imports" / "atlas_bridge_inputs" / "legacy_intent_atlas.json"
BRIDGE_PATH = (
    ROOT
    / "var"
    / "audit"
    / "ledgers"
    / "intent_migration"
    / "native_intent_satisfaction_ledger.json"
)
COMPARISON_PATH = (
    ROOT
    / "var"
    / "audit"
    / "active_code_atlas_bridge_comparison_001"
    / "active_code_atlas_bridge_comparison.json"
)
RECORD_JOIN_PATH = (
    ROOT
    / "var"
    / "audit"
    / "active_code_atlas_bridge_comparison_001"
    / "active_code_atlas_record_join.json"
)
QUEUE_PATH = (
    ROOT
    / "var"
    / "audit"
    / "active_code_atlas_bridge_comparison_001"
    / "active_code_atlas_test_first_execution_queue.json"
)
OUTPUT_PATH = OUT_DIR / "primary_to_bridge_comparison.json"
REPORT_PATH = OUT_DIR / "reports" / "primary_to_bridge_comparison_report.json"

LIMITATION_STATEMENT = (
    "Primary-to-Bridge comparison is audit/navigation evidence only. It compares synthesized "
    "read-adjudicated active-code Atlas records with read-only Atlas/Bridge artefacts; it does "
    "not prove semantic correctness, native satisfaction, implementation maturity, or feature import."
)
EXPECTED_PRIMARY_SURFACES = 18
EXPECTED_QUEUE_RECORDS = 46
EXPECTED_COMPARISON_RECORDS = 48
EXPECTED_ATLAS_RECORDS = 1716
EXPECTED_BRIDGE_RECORDS = 1716


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(cmd: list[str]) -> str:
    return subprocess.check_output(["git", *cmd], cwd=ROOT, text=True).strip()


def sorted_counter(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def sample(values: set[str] | list[str], limit: int = 12) -> list[str]:
    return sorted(values)[:limit]


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    primary = load_json(PRIMARY_PATH)
    atlas = load_json(ATLAS_PATH)
    bridge = load_json(BRIDGE_PATH)
    comparison = load_json(COMPARISON_PATH)
    record_join = load_json(RECORD_JOIN_PATH)
    queue = load_json(QUEUE_PATH)

    primary_records = primary.get("records", [])
    atlas_records = atlas.get("records", [])
    bridge_records = bridge.get("records", [])
    comparison_records = comparison.get("records", [])
    queue_records = queue.get("records", [])
    record_join_records = record_join.get("records", [])

    if len(primary_records) == 0:
        errors.append("primary_records_empty")
    if primary.get("surface_count") != EXPECTED_PRIMARY_SURFACES:
        errors.append(
            f"primary_surface_count_mismatch:expected={EXPECTED_PRIMARY_SURFACES}:actual={primary.get('surface_count')}"
        )
    if len(atlas_records) != EXPECTED_ATLAS_RECORDS:
        errors.append(
            f"atlas_record_count_mismatch:expected={EXPECTED_ATLAS_RECORDS}:actual={len(atlas_records)}"
        )
    if len(bridge_records) != EXPECTED_BRIDGE_RECORDS:
        errors.append(
            f"bridge_record_count_mismatch:expected={EXPECTED_BRIDGE_RECORDS}:actual={len(bridge_records)}"
        )
    if len(comparison_records) != EXPECTED_COMPARISON_RECORDS:
        errors.append(
            f"comparison_record_count_mismatch:expected={EXPECTED_COMPARISON_RECORDS}:actual={len(comparison_records)}"
        )
    if len(queue_records) != EXPECTED_QUEUE_RECORDS:
        errors.append(
            f"queue_record_count_mismatch:expected={EXPECTED_QUEUE_RECORDS}:actual={len(queue_records)}"
        )
    if len(record_join_records) != EXPECTED_ATLAS_RECORDS:
        errors.append(
            f"record_join_count_mismatch:expected={EXPECTED_ATLAS_RECORDS}:actual={len(record_join_records)}"
        )

    atlas_ids = {r.get("atlas_record_id") for r in atlas_records}
    bridge_ids = {r.get("satisfaction_record_id") for r in bridge_records}
    comparison_ids = {r.get("comparison_record_id") for r in comparison_records}
    queue_ids = {r.get("queue_record_id") for r in queue_records}

    primary_atlas_links: set[str] = set()
    primary_bridge_links: set[str] = set()
    primary_comparison_links: set[str] = set()
    primary_queue_links: set[str] = set()
    primary_unknown_links: set[str] = set()
    duplicate_primary_ids: list[str] = []
    primary_id_counts = Counter(r.get("active_code_atlas_record_id") for r in primary_records)
    duplicate_primary_ids = sorted(str(k) for k, v in primary_id_counts.items() if v > 1)
    if duplicate_primary_ids:
        errors.append(f"duplicate_primary_record_ids:{duplicate_primary_ids}")

    for record in primary_records:
        for atlas_id in record.get("linked_atlas_record_ids", []) or []:
            if atlas_id not in atlas_ids:
                warnings.append(
                    f"primary_linked_atlas_navigation_id_not_in_legacy_corpus:{record.get('active_code_atlas_record_id')}:{atlas_id}"
                )
            primary_atlas_links.add(atlas_id)
        for bridge_link in record.get("linked_bridge_record_ids", []) or []:
            if bridge_link.startswith("NIS-"):
                if bridge_link not in bridge_ids:
                    errors.append(
                        f"primary_linked_satisfaction_record_missing:{record.get('active_code_atlas_record_id')}:{bridge_link}"
                    )
                primary_bridge_links.add(bridge_link)
            elif bridge_link.startswith("ACABC-"):
                if bridge_link not in comparison_ids:
                    errors.append(
                        f"primary_linked_comparison_record_missing:{record.get('active_code_atlas_record_id')}:{bridge_link}"
                    )
                primary_comparison_links.add(bridge_link)
            elif bridge_link.startswith("ACATQ-"):
                if bridge_link not in queue_ids:
                    errors.append(
                        f"primary_linked_queue_record_missing:{record.get('active_code_atlas_record_id')}:{bridge_link}"
                    )
                primary_queue_links.add(bridge_link)
            else:
                primary_unknown_links.add(str(bridge_link))
    if primary_unknown_links:
        errors.append(f"primary_unknown_bridge_link_prefixes:{sample(primary_unknown_links)}")

    queue_unlinked = sorted(queue_ids - primary_queue_links)
    comparison_unlinked = sorted(comparison_ids - primary_comparison_links)
    if queue_unlinked:
        warnings.append(f"queue_records_without_primary_link:{queue_unlinked}")
    if comparison_unlinked:
        warnings.append(f"comparison_records_without_primary_link:{comparison_unlinked}")

    bridge_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in bridge_records:
        bridge_by_surface[str(record.get("blueprint_surface") or "unresolved")].append(record)
    atlas_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in bridge_records:
        surface = str(record.get("blueprint_surface") or "unresolved")
        atlas_by_surface[surface].append(record)
    comparison_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in comparison_records:
        comparison_by_surface[str(record.get("blueprint_surface") or "unresolved")].append(record)
    queue_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in queue_records:
        queue_by_surface[str(record.get("blueprint_surface") or "unresolved")].append(record)
    primary_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in primary_records:
        primary_by_surface[str(record.get("surface") or "unresolved")].append(record)

    all_surfaces = sorted(
        set(primary_by_surface)
        | set(bridge_by_surface)
        | set(comparison_by_surface)
        | set(queue_by_surface)
    )
    surface_records: list[dict[str, Any]] = []
    for idx, surface in enumerate(all_surfaces, start=1):
        primary_surface_records = primary_by_surface.get(surface, [])
        comparison_surface_ids = {
            r.get("comparison_record_id") for r in comparison_by_surface.get(surface, [])
        }
        queue_surface_ids = {r.get("queue_record_id") for r in queue_by_surface.get(surface, [])}
        primary_surface_comparison_links = {
            link
            for r in primary_surface_records
            for link in (r.get("linked_bridge_record_ids", []) or [])
            if isinstance(link, str) and link.startswith("ACABC-")
        }
        primary_surface_queue_links = {
            link
            for r in primary_surface_records
            for link in (r.get("linked_bridge_record_ids", []) or [])
            if isinstance(link, str) and link.startswith("ACATQ-")
        }
        primary_surface_atlas_links = {
            link
            for r in primary_surface_records
            for link in (r.get("linked_atlas_record_ids", []) or [])
        }
        primary_surface_nis_links = {
            link
            for r in primary_surface_records
            for link in (r.get("linked_bridge_record_ids", []) or [])
            if isinstance(link, str) and link.startswith("NIS-")
        }
        surface_records.append(
            {
                "surface_comparison_id": f"ACAPBC-{idx:04d}",
                "surface": surface,
                "primary_record_count": len(primary_surface_records),
                "bridge_record_count": len(bridge_by_surface.get(surface, [])),
                "comparison_group_count": len(comparison_by_surface.get(surface, [])),
                "execution_queue_record_count": len(queue_by_surface.get(surface, [])),
                "primary_linked_atlas_record_count": len(primary_surface_atlas_links),
                "primary_linked_satisfaction_record_count": len(primary_surface_nis_links),
                "primary_linked_comparison_group_count": len(primary_surface_comparison_links),
                "primary_linked_execution_queue_record_count": len(primary_surface_queue_links),
                "comparison_group_ids_without_primary_link": sorted(
                    comparison_surface_ids - primary_surface_comparison_links
                ),
                "execution_queue_ids_without_primary_link": sorted(
                    queue_surface_ids - primary_surface_queue_links
                ),
                "sample_primary_record_ids": sample(
                    {str(r.get("active_code_atlas_record_id")) for r in primary_surface_records}
                ),
            }
        )

    queue_gap_records = []
    queue_by_id = {r.get("queue_record_id"): r for r in queue_records}
    comparison_by_id = {r.get("comparison_record_id"): r for r in comparison_records}
    for queue_id in queue_unlinked:
        qr = queue_by_id[queue_id]
        queue_gap_records.append(
            {
                "queue_record_id": queue_id,
                "comparison_record_id": qr.get("comparison_record_id"),
                "surface": qr.get("blueprint_surface"),
                "required_action": qr.get("required_action"),
                "comparison_status": qr.get("comparison_status"),
                "gap_status": "not_linked_by_primary_active_code_atlas_record",
                "recommended_next_action": "audit_linkage_or_create_read_adjudicated_record_before_claiming_full_queue_reconciliation",
            }
        )

    comparison_gap_records = []
    for comparison_id in comparison_unlinked:
        cr = comparison_by_id[comparison_id]
        comparison_gap_records.append(
            {
                "comparison_record_id": comparison_id,
                "surface": cr.get("blueprint_surface"),
                "target_owner": cr.get("target_owner"),
                "comparison_status": cr.get("comparison_status"),
                "test_first_queue_action": cr.get("test_first_queue_action"),
                "gap_status": "not_linked_by_primary_active_code_atlas_record",
                "recommended_next_action": "audit_linkage_or_record_explicit_no_primary_record_reason_before_status_upgrade",
            }
        )

    summary = {
        "primary_record_count": len(primary_records),
        "primary_surface_count": len(primary_by_surface),
        "atlas_record_count": len(atlas_records),
        "bridge_record_count": len(bridge_records),
        "static_comparison_record_count": len(comparison_records),
        "static_record_join_count": len(record_join_records),
        "execution_queue_record_count": len(queue_records),
        "primary_linked_atlas_or_navigation_id_count": len(primary_atlas_links),
        "primary_linked_satisfaction_record_count": len(primary_bridge_links),
        "primary_linked_comparison_group_count": len(primary_comparison_links),
        "primary_linked_execution_queue_record_count": len(primary_queue_links),
        "execution_queue_records_without_primary_link_count": len(queue_unlinked),
        "comparison_groups_without_primary_link_count": len(comparison_unlinked),
        "primary_record_status_counts": sorted_counter(
            [str(r.get("record_status")) for r in primary_records]
        ),
        "primary_surface_counts": dict(
            sorted(Counter(str(r.get("surface")) for r in primary_records).items())
        ),
        "static_comparison_status_counts": dict(
            sorted(Counter(str(r.get("comparison_status")) for r in comparison_records).items())
        ),
        "execution_queue_required_action_counts": dict(
            sorted(Counter(str(r.get("required_action")) for r in queue_records).items())
        ),
    }

    output = {
        "schema_version": "primary_to_bridge_comparison_v1",
        "created_utc": "2026-05-12T00:00:00Z",
        "status": (
            "comparison_generated_with_gaps"
            if (queue_unlinked or comparison_unlinked)
            else "comparison_generated_no_gaps_detected"
        ),
        "classification_note": "AUDIT_COMPARISON_ONLY",
        "limitation_statement": LIMITATION_STATEMENT,
        "source_repo_branch": git(["branch", "--show-current"]),
        "source_repo_head": git(["rev-parse", "--short", "HEAD"]),
        "inputs": {
            "primary_active_code_atlas_path": str(PRIMARY_PATH.relative_to(ROOT)),
            "legacy_intent_atlas_path": str(ATLAS_PATH.relative_to(ROOT)),
            "native_intent_satisfaction_ledger_path": str(BRIDGE_PATH.relative_to(ROOT)),
            "static_comparison_path": str(COMPARISON_PATH.relative_to(ROOT)),
            "static_record_join_path": str(RECORD_JOIN_PATH.relative_to(ROOT)),
            "execution_queue_path": str(QUEUE_PATH.relative_to(ROOT)),
        },
        "guardrails": [
            "donor Atlas remains read-only evidence",
            "native satisfaction ledger remains read-only evidence",
            "static comparison and queue remain navigation evidence",
            "primary active-code Atlas records are read-adjudicated evidence, not semantic satisfaction claims",
            "no source, test, runtime, dependency, vocabulary, original Atlas/Bridge, or generated slice mutation is authorised by this comparison",
        ],
        "summary": summary,
        "surface_records": surface_records,
        "queue_gap_records": queue_gap_records,
        "comparison_gap_records": comparison_gap_records,
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
