#!/usr/bin/env python3
"""Build a bounded evidence packet for the post-row044 linkage-gap intake repair.

This script extracts only the residual queue rows and comparison groups named by
live ROADMAP_LEDGER.md state, plus direct records referenced by those selected
comparison groups. It deliberately does not adjudicate or reconcile the gaps.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]

QUEUE_IDS = ("ACATQ-0044", "ACATQ-0045", "ACATQ-0046")
COMPARISON_IDS = (
    "ACABC-0035",
    "ACABC-0045",
    "ACABC-0046",
    "ACABC-0047",
    "ACABC-0048",
)

TARGET_TRANCHE = "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_POST_ROW044_RECONCILIATION"
PACKET_ID = "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET"

SOURCES = {
    "primary_active_code_atlas": Path("var/audit/active_code_atlas_001/primary_active_code_atlas.json"),
    "primary_to_bridge_comparison": Path(
        "var/audit/active_code_atlas_001/primary_to_bridge_comparison/primary_to_bridge_comparison.json"
    ),
    "static_bridge_comparison": Path(
        "var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json"
    ),
    "static_test_first_queue": Path(
        "var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_execution_queue.json"
    ),
    "static_record_join": Path(
        "var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json"
    ),
    "native_intent_satisfaction_ledger": Path(
        "var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json"
    ),
    "legacy_intent_atlas": Path("var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json"),
}

OUT_PACKET = Path(
    "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/packet/"
    "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET.json"
)
OUT_REPORT = Path(
    "var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/"
    "ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET_REPORT.json"
)


def rel(path: Path) -> str:
    return path.as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def metadata(path: Path) -> dict[str, Any]:
    full = ROOT / path
    data = full.read_bytes()
    return {
        "path": rel(path),
        "sha256": sha256_bytes(data),
        "byte_count": len(data),
        "line_count": len(data.decode("utf-8").splitlines()),
    }


def load_json(path: Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    full.write_text(text, encoding="utf-8")


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def records_by(records: list[dict[str, Any]], key: str, wanted: tuple[str, ...] | set[str]) -> list[dict[str, Any]]:
    wanted_set = set(wanted)
    selected = [record for record in records if record.get(key) in wanted_set]
    return sorted(selected, key=lambda record: str(record.get(key, "")))


def ids_for(records: list[dict[str, Any]], key: str) -> list[str]:
    return sorted(str(record[key]) for record in records if key in record)


def ensure_exact(actual: list[str], expected: tuple[str, ...] | set[str], label: str, errors: list[str]) -> None:
    actual_set = set(actual)
    expected_set = set(expected)
    missing = sorted(expected_set - actual_set)
    unexpected = sorted(actual_set - expected_set)
    if missing:
        errors.append(f"{label} missing requested ids: {missing}")
    if unexpected:
        errors.append(f"{label} included unrelated ids: {unexpected}")


def contains_any(value: Any, needles: set[str]) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return any(needle in value for needle in needles)
    if isinstance(value, list):
        return any(contains_any(item, needles) for item in value)
    if isinstance(value, dict):
        return any(contains_any(item, needles) for item in value.values())
    return False


def main() -> int:
    errors: list[str] = []

    loaded = {name: load_json(path) for name, path in SOURCES.items()}
    source_metadata = {name: metadata(path) for name, path in SOURCES.items()}

    static_queue_records = records_by(loaded["static_test_first_queue"]["records"], "queue_record_id", QUEUE_IDS)
    ensure_exact(ids_for(static_queue_records, "queue_record_id"), QUEUE_IDS, "static_test_first_queue", errors)

    primary_comparison = loaded["primary_to_bridge_comparison"]
    primary_queue_gap_records = records_by(primary_comparison["queue_gap_records"], "queue_record_id", QUEUE_IDS)
    ensure_exact(ids_for(primary_queue_gap_records, "queue_record_id"), QUEUE_IDS, "primary_to_bridge queue_gap_records", errors)

    primary_comparison_gap_records = records_by(
        primary_comparison["comparison_gap_records"], "comparison_record_id", COMPARISON_IDS
    )
    ensure_exact(
        ids_for(primary_comparison_gap_records, "comparison_record_id"),
        COMPARISON_IDS,
        "primary_to_bridge comparison_gap_records",
        errors,
    )

    static_comparison_records = records_by(loaded["static_bridge_comparison"]["records"], "comparison_record_id", COMPARISON_IDS)
    ensure_exact(
        ids_for(static_comparison_records, "comparison_record_id"),
        COMPARISON_IDS,
        "static_bridge_comparison",
        errors,
    )

    comparison_ids_referenced_by_queue = sorted(
        {str(record.get("comparison_record_id")) for record in static_queue_records if record.get("comparison_record_id")}
    )
    unexpected_queue_comparison_refs = sorted(set(comparison_ids_referenced_by_queue) - set(COMPARISON_IDS))
    if unexpected_queue_comparison_refs:
        errors.append(
            "queue records reference comparison IDs outside requested comparison set: "
            f"{unexpected_queue_comparison_refs}"
        )

    selected_atlas_record_ids = sorted(
        {
            str(atlas_record_id)
            for record in static_comparison_records
            for atlas_record_id in record.get("sample_atlas_record_ids", [])
        }
    )

    static_join_records = [
        record
        for record in loaded["static_record_join"]["records"]
        if record.get("atlas_record_id") in set(selected_atlas_record_ids)
    ]
    static_join_records = sorted(
        static_join_records,
        key=lambda record: (str(record.get("atlas_record_id", "")), str(record.get("record_join_id", ""))),
    )
    join_atlas_ids = ids_for(static_join_records, "atlas_record_id")
    ensure_exact(join_atlas_ids, set(selected_atlas_record_ids), "static_record_join atlas references", errors)

    selected_satisfaction_record_ids = sorted(
        {
            str(record.get("bridge_satisfaction_record_id"))
            for record in static_join_records
            if record.get("bridge_satisfaction_record_id")
        }
    )

    native_records = [
        record
        for record in loaded["native_intent_satisfaction_ledger"]["records"]
        if record.get("atlas_record_id") in set(selected_atlas_record_ids)
    ]
    native_records = sorted(native_records, key=lambda record: str(record.get("atlas_record_id", "")))
    ensure_exact(ids_for(native_records, "atlas_record_id"), set(selected_atlas_record_ids), "native ledger atlas references", errors)

    legacy_atlas_records = [
        record
        for record in loaded["legacy_intent_atlas"]["records"]
        if record.get("atlas_record_id") in set(selected_atlas_record_ids)
    ]
    legacy_atlas_records = sorted(legacy_atlas_records, key=lambda record: str(record.get("atlas_record_id", "")))
    ensure_exact(
        ids_for(legacy_atlas_records, "atlas_record_id"),
        set(selected_atlas_record_ids),
        "legacy intent atlas references",
        errors,
    )

    active_needles = set(QUEUE_IDS) | set(COMPARISON_IDS)
    active_primary_records = []
    for record in loaded["primary_active_code_atlas"]["records"]:
        linked_atlas_ids = set(record.get("linked_atlas_record_ids", []))
        linked_bridge_ids = set(record.get("linked_bridge_record_ids", []))
        if linked_atlas_ids & set(selected_atlas_record_ids):
            active_primary_records.append(record)
            continue
        if linked_bridge_ids & set(selected_satisfaction_record_ids):
            active_primary_records.append(record)
            continue
        if contains_any(record.get("test_first_gap_or_action"), active_needles):
            active_primary_records.append(record)
            continue
    active_primary_records = sorted(
        active_primary_records,
        key=lambda record: str(record.get("active_code_atlas_record_id", "")),
    )

    extraction_sources = {
        "static_test_first_queue": {
            **source_metadata["static_test_first_queue"],
            "extraction_key": "records.queue_record_id in requested_queue_record_ids",
            "requested_ids": list(QUEUE_IDS),
            "extracted_record_count": len(static_queue_records),
            "extracted_ids": ids_for(static_queue_records, "queue_record_id"),
        },
        "primary_to_bridge_comparison_queue_gaps": {
            **source_metadata["primary_to_bridge_comparison"],
            "extraction_key": "queue_gap_records.queue_record_id in requested_queue_record_ids",
            "requested_ids": list(QUEUE_IDS),
            "extracted_record_count": len(primary_queue_gap_records),
            "extracted_ids": ids_for(primary_queue_gap_records, "queue_record_id"),
        },
        "primary_to_bridge_comparison_comparison_gaps": {
            **source_metadata["primary_to_bridge_comparison"],
            "extraction_key": "comparison_gap_records.comparison_record_id in requested_comparison_record_ids",
            "requested_ids": list(COMPARISON_IDS),
            "extracted_record_count": len(primary_comparison_gap_records),
            "extracted_ids": ids_for(primary_comparison_gap_records, "comparison_record_id"),
        },
        "static_bridge_comparison": {
            **source_metadata["static_bridge_comparison"],
            "extraction_key": "records.comparison_record_id in requested_comparison_record_ids",
            "requested_ids": list(COMPARISON_IDS),
            "extracted_record_count": len(static_comparison_records),
            "extracted_ids": ids_for(static_comparison_records, "comparison_record_id"),
        },
        "static_record_join": {
            **source_metadata["static_record_join"],
            "extraction_key": "records.atlas_record_id in selected_atlas_record_ids_from_static_bridge_comparison.sample_atlas_record_ids",
            "requested_ids": selected_atlas_record_ids,
            "extracted_record_count": len(static_join_records),
            "extracted_ids": ids_for(static_join_records, "atlas_record_id"),
        },
        "native_intent_satisfaction_ledger": {
            **source_metadata["native_intent_satisfaction_ledger"],
            "extraction_key": "records.atlas_record_id in selected_atlas_record_ids_from_static_bridge_comparison.sample_atlas_record_ids",
            "requested_ids": selected_atlas_record_ids,
            "extracted_record_count": len(native_records),
            "extracted_ids": ids_for(native_records, "atlas_record_id"),
        },
        "legacy_intent_atlas": {
            **source_metadata["legacy_intent_atlas"],
            "extraction_key": "records.atlas_record_id in selected_atlas_record_ids_from_static_bridge_comparison.sample_atlas_record_ids",
            "requested_ids": selected_atlas_record_ids,
            "extracted_record_count": len(legacy_atlas_records),
            "extracted_ids": ids_for(legacy_atlas_records, "atlas_record_id"),
        },
        "primary_active_code_atlas_direct_link_probe": {
            **source_metadata["primary_active_code_atlas"],
            "extraction_key": (
                "records where linked_atlas_record_ids intersects selected_atlas_record_ids OR "
                "linked_bridge_record_ids intersects selected_satisfaction_record_ids OR "
                "test_first_gap_or_action contains requested queue/comparison IDs"
            ),
            "requested_ids": sorted(list(set(QUEUE_IDS) | set(COMPARISON_IDS) | set(selected_atlas_record_ids))),
            "extracted_record_count": len(active_primary_records),
            "extracted_ids": ids_for(active_primary_records, "active_code_atlas_record_id"),
        },
    }

    no_unrelated_ids = errors == []

    packet = {
        "schema_version": 1,
        "packet_id": PACKET_ID,
        "target_tranche": TARGET_TRANCHE,
        "source_repo_head": git_head(),
        "scope_statement": (
            "Bounded-intake control repair only. This packet extracts residual linkage-gap records "
            "and direct referenced Atlas/native/join records; it does not adjudicate, reconcile, "
            "close, or implement any gap."
        ),
        "forbidden_actions_preserved": [
            "no runtime/source/test mutation",
            "no vocabulary data mutation",
            "no original Atlas/Bridge JSON mutation",
            "no generated Atlas slice rebuild",
            "no row 030 reopening",
            "no _archive tarball restore or reliance",
            "no reconciliation target closure claim",
        ],
        "requested_queue_record_ids": list(QUEUE_IDS),
        "requested_comparison_record_ids": list(COMPARISON_IDS),
        "selected_atlas_record_ids": selected_atlas_record_ids,
        "selected_bridge_satisfaction_record_ids": selected_satisfaction_record_ids,
        "extraction_rules": extraction_sources,
        "no_unrelated_ids_check": {
            "status": "PASS" if no_unrelated_ids else "FAIL",
            "errors": errors,
            "queue_record_ids_in_packet": ids_for(static_queue_records, "queue_record_id"),
            "comparison_record_ids_in_packet": ids_for(static_comparison_records, "comparison_record_id"),
            "atlas_record_ids_in_direct_reference_sections": selected_atlas_record_ids,
            "primary_active_code_direct_link_probe_record_count": len(active_primary_records),
            "primary_active_code_direct_link_probe_record_ids": ids_for(
                active_primary_records, "active_code_atlas_record_id"
            ),
        },
        "records": {
            "static_test_first_queue_records": static_queue_records,
            "primary_to_bridge_queue_gap_records": primary_queue_gap_records,
            "primary_to_bridge_comparison_gap_records": primary_comparison_gap_records,
            "static_bridge_comparison_records": static_comparison_records,
            "static_record_join_records": static_join_records,
            "native_intent_satisfaction_records": native_records,
            "legacy_intent_atlas_records": legacy_atlas_records,
            "primary_active_code_direct_link_probe_records": active_primary_records,
        },
    }

    write_json(OUT_PACKET, packet)
    packet_bytes = (ROOT / OUT_PACKET).read_bytes()

    report = {
        "schema_version": 1,
        "report_id": f"{PACKET_ID}_REPORT",
        "target_tranche": TARGET_TRANCHE,
        "validation_status": "PASS" if no_unrelated_ids else "FAIL",
        "errors": errors,
        "output_packet": {
            "path": rel(OUT_PACKET),
            "sha256": sha256_bytes(packet_bytes),
            "byte_count": len(packet_bytes),
            "line_count": len(packet_bytes.decode("utf-8").splitlines()),
        },
        "requested_queue_record_ids": list(QUEUE_IDS),
        "requested_comparison_record_ids": list(COMPARISON_IDS),
        "selected_atlas_record_ids": selected_atlas_record_ids,
        "selected_bridge_satisfaction_record_ids": selected_satisfaction_record_ids,
        "source_extraction_summary": extraction_sources,
        "proof_no_unrelated_ids_included": {
            "queue_ids_exact_match": ids_for(static_queue_records, "queue_record_id") == list(QUEUE_IDS),
            "comparison_ids_exact_match": ids_for(static_comparison_records, "comparison_record_id") == list(COMPARISON_IDS),
            "primary_to_bridge_queue_gap_ids_exact_match": ids_for(primary_queue_gap_records, "queue_record_id")
            == list(QUEUE_IDS),
            "primary_to_bridge_comparison_gap_ids_exact_match": ids_for(
                primary_comparison_gap_records, "comparison_record_id"
            )
            == list(COMPARISON_IDS),
            "direct_reference_atlas_ids_exact_match_across_join_native_legacy": (
                sorted(ids_for(static_join_records, "atlas_record_id"))
                == sorted(ids_for(native_records, "atlas_record_id"))
                == sorted(ids_for(legacy_atlas_records, "atlas_record_id"))
                == selected_atlas_record_ids
            ),
        },
    }
    write_json(OUT_REPORT, report)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if no_unrelated_ids else 1


if __name__ == "__main__":
    raise SystemExit(main())
