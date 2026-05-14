#!/usr/bin/env python3
"""Generate the Atlas + Bridge + active-code Atlas comparison ledger.

This is an audit/control artefact generator. It does not mutate source, tests,
Atlas JSON, Bridge JSON, generated Atlas slices, vocabulary, dependencies, or
runtime code.
"""
from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "var/audit/active_code_atlas_bridge_comparison_001"

ATLAS_PATH = ROOT / "var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json"
BRIDGE_PATH = ROOT / "var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json"
ACTIVE_PATH = ROOT / "var/audit/active_code_atlas_001/active_code_atlas.json"
CURRENT_MAP_PATH = ROOT / "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md"
BLUEPRINT_PATH = ROOT / "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md"

RUNTIME_TYPES = {"runtime_behaviour", "runtime_module", "schema_contract", "config_contract", "data_reference"}
TEST_TYPES = {"test_contract", "test_module"}
DOCSTRING_TYPES = {"docstring_claim"}
CONTROL_TYPES = {
    "audit_receipt_or_ledger",
    "normative_or_control_document",
    "project_control_surface",
    "build_or_environment_contract",
    "atlas_bridge_evidence",
    "repo_file",
    "surface_summary",
}

SURFACE_LINE_RANGES = {
    "External source interfaces and API ingress": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 135, "line_end": 150},
    "Raw capture and source temporal law": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 152, "line_end": 167},
    "Raw signal families": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 169, "line_end": 184},
    "Financial and event calendar architecture": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 186, "line_end": 201},
    "Prepared ingress and runtime context preparation": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 203, "line_end": 218},
    "DMPV3 packet carriage": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 220, "line_end": 235},
    "Serial desk-cognition spine": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 237, "line_end": 252},
    "Parallel risk lane": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 254, "line_end": 269},
    "Dynamic coefficient and modifier authority": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 271, "line_end": 286},
    "Playbook library architecture": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 288, "line_end": 303},
    "Downstream capital deployment authority": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 305, "line_end": 320},
    "Opening architecture and placement readiness": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 322, "line_end": 337},
    "Live position and inventory architecture": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 339, "line_end": 354},
    "Exit and close architecture": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 356, "line_end": 371},
    "Review and explanation layer": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 373, "line_end": 388},
    "Persistence, ledgers, and receipts": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 390, "line_end": 405},
    "Testing, proof, and checkpoint surfaces": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 407, "line_end": 422},
    "Vocabulary governance interface": {"path": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md", "line_start": 424, "line_end": 439},
}

SURFACE_ORDER = list(SURFACE_LINE_RANGES)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def git(cmd: list[str]) -> str:
    return subprocess.check_output(["git", *cmd], cwd=ROOT, text=True).strip()


def counter_dict(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(v) for v in values).items(), key=lambda kv: (-kv[1], kv[0])))


def sample(values: list[str], limit: int = 10) -> list[str]:
    return values[:limit]


def group_key(rec: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    proof = rec.get("proof_resolution") or {}
    return (
        rec.get("blueprint_surface") or "unresolved",
        rec.get("target_owner") or "unresolved",
        proof.get("tier") or "unresolved",
        proof.get("test_family_action") or "unresolved",
        proof.get("proof_block_action") or "unresolved",
        rec.get("implementation_leaf_type") or "unresolved",
    )


def status_for_group(bridge_records: list[dict[str, Any]], active_records: list[dict[str, Any]]) -> tuple[str, list[str]]:
    native_statuses = Counter(r.get("native_satisfaction_status") for r in bridge_records)
    blocked_reasons = [r.get("blocked_reason") for r in bridge_records if r.get("blocked_reason")]
    active_types = Counter(r.get("record_type") for r in active_records)
    runtime_count = sum(active_types[t] for t in RUNTIME_TYPES)
    test_count = sum(active_types[t] for t in TEST_TYPES)
    doc_count = sum(active_types[t] for t in DOCSTRING_TYPES)
    control_count = sum(active_types[t] for t in CONTROL_TYPES)

    basis: list[str] = []
    if blocked_reasons:
        basis.append("Bridge records include explicit blocked_reason values.")
        return "blocked", basis
    if native_statuses.get("already_satisfied") == len(bridge_records):
        if runtime_count and test_count:
            basis.append("Bridge marks all records already_satisfied and active-code Atlas has runtime/contract plus test evidence classes.")
            basis.append("Still provisional_static: no pytest/proof-block execution was run in this comparison gate.")
            return "already_satisfied", basis
        basis.append("Bridge marks all records already_satisfied but active-code Atlas lacks both runtime/contract and test evidence classes.")
        return "partially_satisfied", basis
    if native_statuses.get("missing") == len(bridge_records):
        if runtime_count or test_count:
            basis.append("Bridge marks records missing, but active-code Atlas has same-surface evidence; treat as partial static surface evidence, not satisfaction.")
            return "partially_satisfied", basis
        basis.append("Bridge marks records missing and active-code Atlas has no runtime/test evidence for the same surface-owner group.")
        return "missing", basis
    if native_statuses.get("transform_required") == len(bridge_records):
        basis.append("Bridge marks records transform_required; active evidence cannot be imported without target-shape/test-first work.")
        if runtime_count or test_count or control_count or doc_count:
            basis.append("Active-code Atlas has same-surface evidence, but this only supports test-first migration planning.")
        return "transform_required", basis

    if native_statuses.get("transform_required"):
        basis.append("Bridge group mixes transform_required with other states; use transform_required until adjudicated.")
        return "transform_required", basis
    if native_statuses.get("missing") and not (runtime_count or test_count):
        basis.append("Bridge group includes missing records and active-code Atlas lacks runtime/test evidence.")
        return "missing", basis
    if runtime_count or test_count or control_count or doc_count:
        basis.append("Active-code Atlas has same-surface evidence, but Bridge does not show full satisfaction.")
        return "partially_satisfied", basis
    basis.append("No active evidence found for same surface-owner group.")
    return "missing", basis


def required_test_action(bridge_records: list[dict[str, Any]]) -> dict[str, Any]:
    test_decisions = Counter(r.get("existing_test_decision") for r in bridge_records)
    proof_tiers = Counter((r.get("proof_resolution") or {}).get("tier") for r in bridge_records)
    test_family_actions = Counter((r.get("proof_resolution") or {}).get("test_family_action") for r in bridge_records)
    proof_block_actions = Counter((r.get("proof_resolution") or {}).get("proof_block_action") for r in bridge_records)

    if test_decisions.get("new_test_family_required"):
        action = "write_new_test_family_before_code"
    elif test_decisions.get("extend_existing_same_invariant"):
        action = "extend_existing_test_family_before_code"
    elif test_decisions.get("no_test_change_required"):
        action = "confirm_existing_proof_only_no_refactor"
    else:
        action = "adjudicate_test_family_route"

    return {
        "required_action": action,
        "proof_tier_counts": dict(proof_tiers),
        "test_family_action_counts": dict(test_family_actions),
        "proof_block_action_counts": dict(proof_block_actions),
        "existing_test_decision_counts": dict(test_decisions),
    }



def _norm_symbol(symbol: str | None) -> str:
    if not symbol:
        return ""
    value = str(symbol)
    if ":" in value:
        value = value.split(":", 1)[1]
    return value.strip()


def build_record_join(
    atlas_records: list[dict[str, Any]],
    bridge_records: list[dict[str, Any]],
    active_records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Build one static join row per Atlas/Bridge record.

    The join is intentionally conservative: symbol suffix matches and same-surface
    evidence are static pointers for human review, not semantic satisfaction.
    """
    bridge_by_atlas = {r["atlas_record_id"]: r for r in bridge_records}
    active_by_surface_owner: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    active_by_norm_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in active_records:
        active_by_surface_owner[(rec.get("blueprint_surface") or "unresolved", rec.get("target_owner") or "unresolved")].append(rec)
        active_by_norm_symbol[_norm_symbol(rec.get("symbol_name"))].append(rec)

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for idx, atlas in enumerate(atlas_records, start=1):
        bridge = bridge_by_atlas.get(atlas["atlas_record_id"])
        if bridge is None:
            status = "missing_bridge_record"
            rows.append({
                "record_join_id": f"ACARJ-{idx:04d}",
                "atlas_record_id": atlas["atlas_record_id"],
                "intent_unit_id": atlas.get("intent_unit_id"),
                "atlas_symbol_name": atlas.get("symbol_name"),
                "join_status": status,
                "status_basis": ["No Bridge record found for Atlas record id."],
            })
            status_counts[status] += 1
            continue
        surface = bridge.get("blueprint_surface") or "unresolved"
        owner = bridge.get("target_owner") or "unresolved"
        same_surface = active_by_surface_owner.get((surface, owner), [])
        atlas_symbol_norm = _norm_symbol(atlas.get("symbol_name"))
        symbol_candidates_all = active_by_norm_symbol.get(atlas_symbol_norm, [])
        symbol_candidates_same_surface = [r for r in symbol_candidates_all if (r.get("blueprint_surface"), r.get("target_owner")) == (surface, owner)]
        test_records_same_surface = [r for r in same_surface if r.get("record_type") in TEST_TYPES]
        runtime_records_same_surface = [r for r in same_surface if r.get("record_type") in RUNTIME_TYPES]
        bridge_status = bridge.get("native_satisfaction_status")

        basis: list[str] = []
        if symbol_candidates_same_surface:
            if test_records_same_surface:
                status = "active_symbol_and_surface_test_evidence_present"
                basis.append("Active-code Atlas has same-symbol/same-surface evidence and same-surface test evidence.")
            else:
                status = "active_symbol_present_test_evidence_not_static_matched"
                basis.append("Active-code Atlas has same-symbol/same-surface evidence, but no same-surface test record was statically linked.")
            if bridge_status in {"missing", "transform_required"}:
                basis.append("Bridge status is missing/transform_required, so this is a stale-or-transform candidate for human adjudication, not satisfaction proof.")
        elif symbol_candidates_all:
            status = "active_symbol_present_different_surface_or_owner"
            basis.append("Active-code Atlas has same-symbol evidence, but not under the Bridge surface/owner pair.")
        elif same_surface:
            if bridge_status == "missing" and not runtime_records_same_surface and not test_records_same_surface:
                status = "surface_control_evidence_only"
                basis.append("Only same-surface control/doc/receipt evidence was statically found.")
            else:
                status = "same_surface_evidence_only"
                basis.append("Active-code Atlas has same-surface evidence, but no same-symbol static match.")
        else:
            status = "no_active_surface_evidence"
            basis.append("No active-code Atlas records found for the Bridge surface/owner pair.")

        status_counts[status] += 1
        rows.append({
            "record_join_id": f"ACARJ-{idx:04d}",
            "atlas_record_id": atlas["atlas_record_id"],
            "intent_unit_id": atlas.get("intent_unit_id"),
            "atlas_symbol_name": atlas.get("symbol_name"),
            "atlas_record_type": atlas.get("record_type"),
            "atlas_construct_type": atlas.get("construct_type"),
            "bridge_satisfaction_record_id": bridge.get("satisfaction_record_id"),
            "blueprint_surface": surface,
            "target_owner": owner,
            "bridge_native_satisfaction_status": bridge_status,
            "bridge_existing_test_decision": bridge.get("existing_test_decision"),
            "bridge_implementation_leaf_type": bridge.get("implementation_leaf_type"),
            "proof_resolution": bridge.get("proof_resolution"),
            "active_same_symbol_same_surface_record_count": len(symbol_candidates_same_surface),
            "active_same_symbol_any_surface_record_count": len(symbol_candidates_all),
            "active_same_surface_owner_record_count": len(same_surface),
            "active_same_surface_test_record_count": len(test_records_same_surface),
            "active_same_surface_runtime_or_contract_record_count": len(runtime_records_same_surface),
            "sample_active_same_symbol_record_ids": sample([r["active_code_record_id"] for r in symbol_candidates_same_surface]),
            "sample_active_same_surface_record_ids": sample([r["active_code_record_id"] for r in same_surface]),
            "join_status": status,
            "status_basis": basis,
            "normative_surface_evidence": SURFACE_LINE_RANGES.get(surface),
            "notes": "Static record-level join only; same-symbol match is evidence for adjudication, not implementation correctness or proof success.",
        })
    return rows, dict(sorted(status_counts.items()))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "reports").mkdir(exist_ok=True)
    (OUT / "receipts").mkdir(exist_ok=True)

    atlas = load_json(ATLAS_PATH)
    bridge = load_json(BRIDGE_PATH)
    active = load_json(ACTIVE_PATH)
    atlas_records = atlas["records"]
    bridge_records = bridge["records"]
    active_records = active["records"]

    atlas_by_id = {r["atlas_record_id"]: r for r in atlas_records}
    active_by_surface_owner: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for rec in active_records:
        active_by_surface_owner[(rec.get("blueprint_surface") or "unresolved", rec.get("target_owner") or "unresolved")].append(rec)

    record_join_rows, record_join_status_counts = build_record_join(atlas_records, bridge_records, active_records)

    bridge_groups: dict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for rec in bridge_records:
        bridge_groups[group_key(rec)].append(rec)

    comparison_records = []
    test_queue_records = []
    for idx, (key, records) in enumerate(sorted(bridge_groups.items(), key=lambda kv: (SURFACE_ORDER.index(kv[0][0]) if kv[0][0] in SURFACE_ORDER else 999, kv[0])) , start=1):
        surface, target_owner, proof_tier, test_family_action, proof_block_action, implementation_leaf_type = key
        active_group = active_by_surface_owner.get((surface, target_owner), [])
        bridge_atlas_ids = [r["atlas_record_id"] for r in records]
        atlas_group = [atlas_by_id[a] for a in bridge_atlas_ids if a in atlas_by_id]
        status, basis = status_for_group(records, active_group)
        test_action = required_test_action(records)
        active_types = Counter(r.get("record_type") for r in active_group)
        evidence_classes = {
            "runtime_or_contract": sum(active_types[t] for t in RUNTIME_TYPES),
            "test": sum(active_types[t] for t in TEST_TYPES),
            "docstring": sum(active_types[t] for t in DOCSTRING_TYPES),
            "control_or_receipt": sum(active_types[t] for t in CONTROL_TYPES),
        }
        rec_id = f"ACABC-{idx:04d}"
        comparison_records.append({
            "comparison_record_id": rec_id,
            "blueprint_surface": surface,
            "target_owner": target_owner,
            "proof_tier": proof_tier,
            "bridge_test_family_action": test_family_action,
            "bridge_proof_block_action": proof_block_action,
            "implementation_leaf_type": implementation_leaf_type,
            "bridge_record_count": len(records),
            "atlas_record_count_joined": len(atlas_group),
            "active_code_record_count_same_surface_owner": len(active_group),
            "active_evidence_class_counts": evidence_classes,
            "bridge_native_satisfaction_status_counts": counter_dict([r.get("native_satisfaction_status") for r in records]),
            "bridge_existing_test_decision_counts": counter_dict([r.get("existing_test_decision") for r in records]),
            "active_record_type_counts": counter_dict([r.get("record_type") for r in active_group]),
            "active_construct_type_counts": counter_dict([r.get("construct_type") for r in active_group]),
            "comparison_status": status,
            "status_basis": basis,
            "test_first_queue_action": test_action["required_action"],
            "test_first_queue_basis": test_action,
            "normative_surface_evidence": SURFACE_LINE_RANGES.get(surface),
            "sample_atlas_record_ids": sample(bridge_atlas_ids),
            "sample_active_code_record_ids": sample([r["active_code_record_id"] for r in active_group]),
            "source_paths_sample": sample(sorted({r.get("source_file", "") for r in active_group if r.get("source_file")})),
            "notes": "Static comparison only: no proof execution, source/test mutation, refactor, original Atlas/Bridge mutation, generated slice rebuild, dependency, VENV, black, or ruff opened.",
        })
        if test_action["required_action"] != "confirm_existing_proof_only_no_refactor":
            test_queue_records.append({
                "queue_record_id": f"ACATQ-{len(test_queue_records)+1:04d}",
                "comparison_record_id": rec_id,
                "blueprint_surface": surface,
                "target_owner": target_owner,
                "proof_tier": proof_tier,
                "required_action": test_action["required_action"],
                "bridge_record_count": len(records),
                "comparison_status": status,
                "implementation_leaf_type": implementation_leaf_type,
                "normative_surface_evidence": SURFACE_LINE_RANGES.get(surface),
                "must_happen_before": "any source refactor, feature import, donor Atlas implementation, or status upgrade claim",
                "closed_boundaries": [
                    "no source implementation change in this queue artefact",
                    "no test implementation change in this comparison gate",
                    "no refactor",
                    "no original Atlas/Bridge JSON mutation",
                    "no generated Atlas slice rebuild",
                    "no vocabulary mutation",
                ],
            })

    comparison_status_counts = Counter(r["comparison_status"] for r in comparison_records)
    test_action_counts = Counter(r["test_first_queue_action"] for r in comparison_records)
    surface_counts = Counter(r["blueprint_surface"] for r in comparison_records)

    metadata = {
        "ledger_name": "active_code_atlas_bridge_comparison",
        "schema_version": "1.0-draft",
        "status": "static_comparison_generated_no_refactor_opened",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_repo_head": git(["rev-parse", "--short=12", "HEAD"]),
        "source_repo_branch": git(["branch", "--show-current"]),
        "inputs": {
            "atlas_path": str(ATLAS_PATH.relative_to(ROOT)),
            "atlas_record_count": len(atlas_records),
            "bridge_path": str(BRIDGE_PATH.relative_to(ROOT)),
            "bridge_record_count": len(bridge_records),
            "active_code_atlas_path": str(ACTIVE_PATH.relative_to(ROOT)),
            "active_code_record_count": len(active_records),
            "current_state_map_path": str(CURRENT_MAP_PATH.relative_to(ROOT)),
            "blueprint_path": str(BLUEPRINT_PATH.relative_to(ROOT)),
        },
        "guardrails": [
            "donor Atlas is evidence only, not runtime authority",
            "active code is observed reality only, not correctness authority",
            "docstrings are separate low-authority evidence",
            "static comparison is not proof execution",
            "tests must be written or extended before any implementation/refactor leaf",
        ],
    }

    comparison = {
        **metadata,
        "summary": {
            "comparison_record_count": len(comparison_records),
            "test_first_queue_record_count": len(test_queue_records),
            "comparison_status_counts": dict(sorted(comparison_status_counts.items())),
            "test_first_action_counts": dict(sorted(test_action_counts.items())),
            "comparison_records_by_surface": dict(surface_counts),
            "bridge_record_count_accounted_for": sum(r["bridge_record_count"] for r in comparison_records),
            "atlas_record_count_joined": sum(r["atlas_record_count_joined"] for r in comparison_records),
            "active_code_record_count_total_available": len(active_records),
            "record_level_join_count": len(record_join_rows),
            "record_level_join_status_counts": record_join_status_counts,
        },
        "records": comparison_records,
        "record_level_join_path": "var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json",
    }

    test_queue = {
        "ledger_name": "active_code_atlas_test_first_queue",
        "schema_version": "1.0-draft",
        "status": "queued_from_static_comparison_no_tests_written",
        "generated_at_utc": metadata["generated_at_utc"],
        "source_repo_head": metadata["source_repo_head"],
        "source_repo_branch": metadata["source_repo_branch"],
        "purpose": "Queue Tier A/B test-family work required before source refactor or Atlas donor implementation leaves.",
        "queue_guardrail": "This queue does not itself authorise test implementation, source implementation, refactor, runtime/dependency changes, vocabulary mutation, or Atlas/Bridge mutation.",
        "summary": {
            "queue_record_count": len(test_queue_records),
            "required_action_counts": dict(Counter(r["required_action"] for r in test_queue_records)),
            "proof_tier_counts": dict(Counter(r["proof_tier"] for r in test_queue_records)),
            "surface_counts": dict(Counter(r["blueprint_surface"] for r in test_queue_records)),
        },
        "records": test_queue_records,
    }

    with (OUT / "active_code_atlas_bridge_comparison.json").open("w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, sort_keys=True)
        f.write("\n")
    record_join = {
        "ledger_name": "active_code_atlas_record_join",
        "schema_version": "1.0-draft",
        "status": "static_record_level_join_generated_no_satisfaction_claim",
        "generated_at_utc": metadata["generated_at_utc"],
        "source_repo_head": metadata["source_repo_head"],
        "source_repo_branch": metadata["source_repo_branch"],
        "summary": {
            "record_join_count": len(record_join_rows),
            "join_status_counts": record_join_status_counts,
            "guardrail": "symbol/surface matches are static adjudication evidence only, not proof of correctness",
        },
        "records": record_join_rows,
    }
    with (OUT / "active_code_atlas_record_join.json").open("w", encoding="utf-8") as f:
        json.dump(record_join, f, indent=2, sort_keys=True)
        f.write("\n")
    with (OUT / "active_code_atlas_test_first_queue.json").open("w", encoding="utf-8") as f:
        json.dump(test_queue, f, indent=2, sort_keys=True)
        f.write("\n")
    with (OUT / "active_code_atlas_bridge_comparison_summary.json").open("w", encoding="utf-8") as f:
        json.dump({"comparison_summary": comparison["summary"], "record_join_summary": record_join["summary"], "test_queue_summary": test_queue["summary"]}, f, indent=2, sort_keys=True)
        f.write("\n")

    md = [
        "# ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001 summary",
        "",
        "Status: `static_comparison_generated_no_refactor_opened`",
        "",
        "## Inputs",
        "",
        f"- Atlas intent corpus: `{metadata['inputs']['atlas_path']}` records={len(atlas_records)}",
        f"- Atlas Bridge ledger: `{metadata['inputs']['bridge_path']}` records={len(bridge_records)}",
        f"- Active-code Atlas: `{metadata['inputs']['active_code_atlas_path']}` records={len(active_records)}",
        "",
        "## Result counts",
        "",
        f"- comparison records: {len(comparison_records)}",
        f"- bridge records accounted for: {comparison['summary']['bridge_record_count_accounted_for']}",
        f"- Atlas records joined: {comparison['summary']['atlas_record_count_joined']}",
        f"- test-first queue records: {len(test_queue_records)}",
        f"- record-level join records: {len(record_join_rows)}",
        "",
        "## Group status counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for k, v in sorted(comparison_status_counts.items()):
        md.append(f"| `{k}` | {v} |")
    md += [
        "",
        "## Record-level join status counts",
        "",
        "| Join status | Count |",
        "|---|---:|",
    ]
    for k, v in sorted(record_join_status_counts.items()):
        md.append(f"| `{k}` | {v} |")
    md += [
        "",
        "## Test-first action counts",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for k, v in sorted(test_action_counts.items()):
        md.append(f"| `{k}` | {v} |")
    md += [
        "",
        "## Guardrail",
        "",
        "This output is static comparison only. It does not execute pytest/proof blocks and does not authorise source refactor, feature import, test implementation, dependency changes, vocabulary mutation, original Atlas/Bridge mutation, or generated slice rebuild.",
        "",
        "## Files emitted",
        "",
        "- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json`",
        "- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison_summary.json`",
        "- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json`",
        "- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_queue.json`",
    ]
    (OUT / "ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    qmd = [
        "# ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001 test-first queue",
        "",
        "Status: `queued_from_static_comparison_no_tests_written`",
        "",
        "This queue records the test-family work that must occur before any source refactor, feature import, donor Atlas implementation, or status-upgrade claim.",
        "",
        "It does not itself write tests or authorise refactor.",
        "",
        "| Queue ID | Surface | Tier | Required action | Bridge records | Comparison status |",
        "|---|---|---|---|---:|---|",
    ]
    for row in test_queue_records:
        qmd.append(
            f"| `{row['queue_record_id']}` | {row['blueprint_surface']} | {row['proof_tier']} | `{row['required_action']}` | {row['bridge_record_count']} | `{row['comparison_status']}` |"
        )
    (OUT / "ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_TEST_FIRST_QUEUE.md").write_text("\n".join(qmd) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "generated",
        "comparison_record_count": len(comparison_records),
        "bridge_record_count_accounted_for": comparison["summary"]["bridge_record_count_accounted_for"],
        "atlas_record_count_joined": comparison["summary"]["atlas_record_count_joined"],
        "test_first_queue_record_count": len(test_queue_records),
        "record_level_join_count": len(record_join_rows),
        "record_level_join_status_counts": record_join_status_counts,
        "comparison_status_counts": dict(sorted(comparison_status_counts.items())),
        "test_first_action_counts": dict(sorted(test_action_counts.items())),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
