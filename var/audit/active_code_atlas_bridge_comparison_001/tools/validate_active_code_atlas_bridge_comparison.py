#!/usr/bin/env python3
"""Validate the static Atlas + Bridge + structural-inventory comparison artefacts."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "var/audit/active_code_atlas_bridge_comparison_001"
COMPARISON = OUT / "active_code_atlas_bridge_comparison.json"
QUEUE = OUT / "active_code_atlas_test_first_queue.json"
SUMMARY = OUT / "active_code_atlas_bridge_comparison_summary.json"
RECORD_JOIN = OUT / "active_code_atlas_record_join.json"
ATLAS = ROOT / "var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json"
BRIDGE = ROOT / "var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json"
ACTIVE = ROOT / "var/audit/active_code_atlas_001/active_code_atlas.json"
ALLOWED_STATUSES = {"already_satisfied", "partially_satisfied", "missing", "transform_required", "blocked", "conflict"}
ALLOWED_ACTIONS = {"write_new_test_family_before_code", "extend_existing_test_family_before_code", "confirm_existing_proof_only_no_refactor", "adjudicate_test_family_route"}
LIMITATION_STATEMENT = "This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status."

errors: list[str] = []
warnings: list[str] = []

def load(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"cannot_parse_json:{path}:{exc}")
        return None

atlas = load(ATLAS)
bridge = load(BRIDGE)
active = load(ACTIVE)
comparison = load(COMPARISON)
queue = load(QUEUE)
summary = load(SUMMARY)
record_join = load(RECORD_JOIN)

if comparison and bridge and atlas and active:
    records = comparison.get("records", [])
    if not records:
        errors.append("comparison_records_empty")
    ids = [r.get("comparison_record_id") for r in records]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_comparison_record_id")
    accounted = sum(int(r.get("bridge_record_count", 0)) for r in records)
    if accounted != len(bridge.get("records", [])):
        errors.append(f"bridge_count_mismatch:accounted={accounted}:expected={len(bridge.get('records', []))}")
    joined = sum(int(r.get("atlas_record_count_joined", 0)) for r in records)
    if joined != len(atlas.get("records", [])):
        errors.append(f"atlas_join_count_mismatch:joined={joined}:expected={len(atlas.get('records', []))}")
    for r in records:
        status = r.get("comparison_status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"invalid_comparison_status:{r.get('comparison_record_id')}:{status}")
        action = r.get("test_first_queue_action")
        if action not in ALLOWED_ACTIONS:
            errors.append(f"invalid_test_first_action:{r.get('comparison_record_id')}:{action}")
        if not r.get("normative_surface_evidence"):
            errors.append(f"missing_normative_surface_evidence:{r.get('comparison_record_id')}")
        if not r.get("status_basis"):
            errors.append(f"missing_status_basis:{r.get('comparison_record_id')}")
    sum_status_counts = dict(Counter(r.get("comparison_status") for r in records))
    declared_status_counts = comparison.get("summary", {}).get("comparison_status_counts")
    if dict(sorted(sum_status_counts.items())) != dict(sorted(declared_status_counts.items())):
        errors.append("comparison_status_count_summary_mismatch")
    if comparison.get("summary", {}).get("active_code_record_count_total_available") != len(active.get("records", [])):
        errors.append("active_code_record_count_summary_mismatch")

if record_join and atlas and bridge:
    rj = record_join.get("records", [])
    if len(rj) != len(atlas.get("records", [])):
        errors.append(f"record_join_count_mismatch:joined={len(rj)}:expected={len(atlas.get('records', []))}")
    rj_ids = [r.get("record_join_id") for r in rj]
    if len(rj_ids) != len(set(rj_ids)):
        errors.append("duplicate_record_join_id")
    atlas_ids = {r.get("atlas_record_id") for r in atlas.get("records", [])}
    bridge_atlas_ids = {r.get("atlas_record_id") for r in bridge.get("records", [])}
    for r in rj:
        if r.get("atlas_record_id") not in atlas_ids:
            errors.append(f"record_join_bad_atlas_id:{r.get('record_join_id')}:{r.get('atlas_record_id')}")
        if r.get("atlas_record_id") not in bridge_atlas_ids:
            errors.append(f"record_join_missing_bridge_id:{r.get('record_join_id')}:{r.get('atlas_record_id')}")
        if not r.get("join_status"):
            errors.append(f"record_join_missing_status:{r.get('record_join_id')}")
        if not r.get("status_basis"):
            errors.append(f"record_join_missing_status_basis:{r.get('record_join_id')}")
    declared = record_join.get("summary", {}).get("join_status_counts", {})
    actual = dict(Counter(r.get("join_status") for r in rj))
    if dict(sorted(declared.items())) != dict(sorted(actual.items())):
        errors.append("record_join_status_count_summary_mismatch")

if queue and comparison:
    qrecords = queue.get("records", [])
    qids = [r.get("queue_record_id") for r in qrecords]
    if len(qids) != len(set(qids)):
        errors.append("duplicate_queue_record_id")
    comparison_ids = {r.get("comparison_record_id") for r in comparison.get("records", [])}
    for r in qrecords:
        if r.get("comparison_record_id") not in comparison_ids:
            errors.append(f"queue_record_bad_comparison_join:{r.get('queue_record_id')}:{r.get('comparison_record_id')}")
        if r.get("required_action") == "confirm_existing_proof_only_no_refactor":
            errors.append(f"queue_includes_confirm_only_record:{r.get('queue_record_id')}")
        if not r.get("normative_surface_evidence"):
            errors.append(f"queue_missing_normative_surface_evidence:{r.get('queue_record_id')}")

try:
    status = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
    diff_check_status = status.returncode
    if status.returncode != 0:
        errors.append("git_diff_check_failed")
except Exception as exc:  # noqa: BLE001
    diff_check_status = None
    errors.append(f"git_diff_check_error:{exc}")

report = {
    "validation_status": "PASS" if not errors else "FAIL",
    "error_count": len(errors),
    "warning_count": len(warnings),
    "errors": errors,
    "warnings": warnings,
    "comparison_record_count": len(comparison.get("records", [])) if comparison else 0,
    "record_join_count": len(record_join.get("records", [])) if record_join else 0,
    "queue_record_count": len(queue.get("records", [])) if queue else 0,
    "bridge_record_count_accounted_for": sum(int(r.get("bridge_record_count", 0)) for r in comparison.get("records", [])) if comparison else 0,
    "atlas_record_count_joined": sum(int(r.get("atlas_record_count_joined", 0)) for r in comparison.get("records", [])) if comparison else 0,
    "git_diff_check_status": diff_check_status,
    "classification_note": "STATIC_STRUCTURAL_TRIAGE_ONLY",
    "limitation_statement": LIMITATION_STATEMENT,
}

with (OUT / "active_code_atlas_bridge_comparison_validation_report.json").open("w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if not errors else 1)
