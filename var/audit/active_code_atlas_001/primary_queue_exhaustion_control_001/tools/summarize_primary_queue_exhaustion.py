#!/usr/bin/env python3
"""Build the post-row044 primary queue-exhaustion control summary from read audit artefacts."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
OUT_DIR = ROOT / "var" / "audit" / "active_code_atlas_001" / "primary_queue_exhaustion_control_001"
REPORT_PATH = OUT_DIR / "reports" / "ACTIVE_CODE_ATLAS_PRIMARY_QUEUE_EXHAUSTION_CONTROL_001_REPORT.json"

INPUTS = {
    "primary_active_code_atlas": "var/audit/active_code_atlas_001/primary_active_code_atlas.json",
    "primary_synthesis_report": "var/audit/active_code_atlas_001/primary_synthesis/reports/primary_active_code_atlas_synthesis_report.json",
    "primary_to_bridge_comparison": "var/audit/active_code_atlas_001/primary_to_bridge_comparison/primary_to_bridge_comparison.json",
    "primary_to_bridge_comparison_report": "var/audit/active_code_atlas_001/primary_to_bridge_comparison/reports/primary_to_bridge_comparison_report.json",
    "post_row044_linkage_reconciliation": "var/audit/active_code_atlas_001/primary_linkage_gap_reconciliation_002/primary_linkage_gap_reconciliation_002.json",
    "post_row044_linkage_reconciliation_report": "var/audit/active_code_atlas_001/primary_linkage_gap_reconciliation_002/reports/primary_linkage_gap_reconciliation_002_report.json",
}
OPTIONAL_INPUTS = {
    "primary_record_normalisation_report": "var/audit/active_code_atlas_001/primary_record_normalisation_001/reports/ACTIVE_CODE_ATLAS_PRIMARY_RECORD_NORMALISATION_001_REPORT.json",
}

EXPECTED_PRE_NORMALISATION_QUEUE_IDS = ["ACATQ-0044", "ACATQ-0045", "ACATQ-0046"]
EXPECTED_PRE_NORMALISATION_COMPARISON_IDS = ["ACABC-0035", "ACABC-0045", "ACABC-0046", "ACABC-0047", "ACABC-0048"]
EXPECTED_POST_NORMALISATION_QUEUE_IDS: list[str] = []
EXPECTED_POST_NORMALISATION_COMPARISON_IDS = ["ACABC-0035"]


def repo_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def repo_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def file_metadata(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    data = path.read_bytes()
    return {
        "path": rel,
        "byte_count": len(data),
        "line_count": 0 if not data else data.count(b"\n") + (0 if data.endswith(b"\n") else 1),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def load_json(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> None:
    primary = load_json(INPUTS["primary_active_code_atlas"])
    synthesis_report = load_json(INPUTS["primary_synthesis_report"])
    comparison = load_json(INPUTS["primary_to_bridge_comparison"])
    comparison_report = load_json(INPUTS["primary_to_bridge_comparison_report"])
    reconciliation = load_json(INPUTS["post_row044_linkage_reconciliation"])
    reconciliation_report = load_json(INPUTS["post_row044_linkage_reconciliation_report"])

    queue_gap_ids = [record["queue_record_id"] for record in comparison.get("queue_gap_records", [])]
    comparison_gap_ids = [record["comparison_record_id"] for record in comparison.get("comparison_gap_records", [])]
    reconciled_queue_ids = [record["queue_record_id"] for record in reconciliation.get("queue_reconciliations", [])]
    reconciled_comparison_ids = [record["comparison_record_id"] for record in reconciliation.get("comparison_reconciliations", [])]

    errors: list[str] = []
    warnings: list[str] = []

    if synthesis_report.get("validation_status") != "PASS":
        errors.append("primary_synthesis_report_not_pass")
    if comparison_report.get("validation_status") != "PASS":
        errors.append("primary_to_bridge_comparison_report_not_pass")
    if reconciliation_report.get("validation_status") != "PASS":
        errors.append("post_row044_linkage_reconciliation_report_not_pass")
    normalisation_report_path = ROOT / OPTIONAL_INPUTS["primary_record_normalisation_report"]
    normalisation_report = None
    if normalisation_report_path.exists():
        normalisation_report = load_json(OPTIONAL_INPUTS["primary_record_normalisation_report"])
        if normalisation_report.get("status") != "PASS":
            errors.append("primary_record_normalisation_report_not_pass")

    pre_normalisation_shape = (
        queue_gap_ids == EXPECTED_PRE_NORMALISATION_QUEUE_IDS
        and comparison_gap_ids == EXPECTED_PRE_NORMALISATION_COMPARISON_IDS
    )
    post_normalisation_shape = (
        queue_gap_ids == EXPECTED_POST_NORMALISATION_QUEUE_IDS
        and comparison_gap_ids == EXPECTED_POST_NORMALISATION_COMPARISON_IDS
        and normalisation_report is not None
    )
    if not pre_normalisation_shape and not post_normalisation_shape:
        errors.append(
            "unexpected_current_comparison_gap_shape:"
            f"queue={queue_gap_ids}:comparison={comparison_gap_ids}:"
            f"normalisation_report_present={normalisation_report is not None}"
        )
    if pre_normalisation_shape:
        if sorted(reconciled_queue_ids) != sorted(queue_gap_ids):
            errors.append(f"reconciled_queue_ids_do_not_match_comparison_gaps:{reconciled_queue_ids}:{queue_gap_ids}")
        if sorted(reconciled_comparison_ids) != sorted(comparison_gap_ids):
            errors.append(
                f"reconciled_comparison_ids_do_not_match_comparison_gaps:{reconciled_comparison_ids}:{comparison_gap_ids}"
            )
    if post_normalisation_shape:
        if sorted(reconciled_queue_ids) != EXPECTED_PRE_NORMALISATION_QUEUE_IDS:
            errors.append(f"reconciliation_input_queue_ids_changed_unexpectedly:{reconciled_queue_ids}")
        if "ACABC-0035" not in reconciled_comparison_ids:
            errors.append("comparison_only_gap_acabc_0035_not_preserved_in_reconciliation_input")

    recon_summary = reconciliation_report.get("summary", {})
    if recon_summary.get("unresolved_execution_queue_gap_count") != 0:
        errors.append("unresolved_execution_queue_gap_count_nonzero")
    if recon_summary.get("unresolved_comparison_gap_count") != 0:
        errors.append("unresolved_comparison_gap_count_nonzero")

    comparison_warnings = comparison_report.get("warnings", [])
    if comparison_warnings:
        warnings.append(
            "primary_to_bridge_comparison_report_retains_navigation_warnings; "
            "this control summary does not rewrite comparator output"
        )

    report = {
        "schema_version": "primary_queue_exhaustion_control_v1",
        "status": "PASS" if not errors else "FAIL",
        "classification_note": "AUDIT_CONTROL_ROLLUP_ONLY",
        "source_repo_branch": repo_branch(),
        "source_repo_head": repo_head(),
        "limitation_statement": (
            "This control rollup records the post-row044 audit queue state from already generated primary synthesis, "
            "primary-to-Bridge comparison, and bounded linkage reconciliation artefacts. It does not mutate primary records, "
            "source, tests, runtime behaviour, dependencies, vocabulary data, original Atlas/Bridge JSON, or generated slices. "
            "It does not prove feature maturity."
        ),
        "inputs": {
            **{name: file_metadata(path) for name, path in INPUTS.items()},
            **{
                name: file_metadata(path)
                for name, path in OPTIONAL_INPUTS.items()
                if (ROOT / path).exists()
            },
        },
        "summary": {
            "primary_record_count": primary.get("record_count"),
            "primary_surface_count": primary.get("surface_count"),
            "primary_source_record_file_count": primary.get("source_record_file_count"),
            "primary_synthesis_status": synthesis_report.get("validation_status"),
            "primary_synthesis_error_count": synthesis_report.get("error_count"),
            "primary_synthesis_warning_count": synthesis_report.get("warning_count"),
            "primary_to_bridge_comparison_status": comparison_report.get("validation_status"),
            "primary_to_bridge_comparison_warning_count": comparison_report.get("warning_count"),
            "execution_queue_record_count": comparison.get("summary", {}).get("execution_queue_record_count"),
            "primary_linked_execution_queue_record_count": comparison.get("summary", {}).get(
                "primary_linked_execution_queue_record_count"
            ),
            "current_comparison_queue_gap_ids": queue_gap_ids,
            "current_comparison_comparison_gap_ids": comparison_gap_ids,
            "pre_normalisation_reconciled_queue_ids": reconciled_queue_ids,
            "pre_normalisation_reconciled_comparison_ids": reconciled_comparison_ids,
            "comparison_shape": "post_normalisation" if post_normalisation_shape else "pre_normalisation",
            "primary_record_normalisation_status": (normalisation_report or {}).get("status"),
            "primary_record_normalisation_added_link_count": (normalisation_report or {}).get("added_link_count"),
            "unresolved_execution_queue_gap_count_after_reconciliation": recon_summary.get(
                "unresolved_execution_queue_gap_count"
            ),
            "unresolved_execution_queue_gap_ids_after_reconciliation": recon_summary.get(
                "unresolved_execution_queue_gap_ids"
            ),
            "unresolved_comparison_gap_count_after_reconciliation": recon_summary.get(
                "unresolved_comparison_gap_count"
            ),
            "unresolved_comparison_gap_ids_after_reconciliation": recon_summary.get("unresolved_comparison_gap_ids"),
            "next_target": "no_execution_queue_gap_selected_by_current_primary_to_bridge_comparison_plus_reconciliation_overlay",
        },
        "guardrails": [
            "primary active-code Atlas remains an audit/read-adjudicated snapshot, not normative runtime truth",
            "comparator warnings are retained as navigation warnings and are not silently rewritten",
            "no runtime/source/test/dependency/vocabulary/original Atlas/Bridge/generated slice mutation is opened",
            "future primary-record-normalisation or architecture/refactor work requires explicit live authority",
        ],
        "errors": errors,
        "warnings": warnings,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
