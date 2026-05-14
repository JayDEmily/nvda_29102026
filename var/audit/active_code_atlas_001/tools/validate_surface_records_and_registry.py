#!/usr/bin/env python3
"""Validate read-adjudicated surface record evidence ranges and retained-test inventories."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_CODE_ATLAS_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
REPORT_PATH = ACTIVE_CODE_ATLAS_DIR / "reports" / "validate_surface_records_and_registry_output.json"
REGISTRY_PATH = ROOT / "config" / "retained_test_registry.yaml"
LIMITATION_STATEMENT = (
    "This is static structural evidence only. It does not prove semantic correctness, "
    "native satisfaction, implementation maturity, or test pass status."
)

SURFACE_RECORD_FILES = sorted(
    path
    for path in ACTIVE_CODE_ATLAS_DIR.glob("*/*records.json")
    if path.is_file()
)
EVIDENCE_LIST_FIELDS = (
    "normative_evidence",
    "active_source_evidence",
    "active_test_evidence",
    "proof_block_or_registry_evidence",
)


def line_count(path: Path) -> int:
    data = path.read_bytes()
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def validate_evidence_ranges(errors: list[str], warnings: list[str]) -> dict[str, object]:
    checked_files: Counter[str] = Counter()
    evidence_count = 0
    record_count = 0
    for record_path in SURFACE_RECORD_FILES:
        try:
            payload = json.loads(record_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"surface_records_json_parse_failed:{record_path.relative_to(ROOT)}:{exc}")
            continue
        records = payload.get("records")
        if not isinstance(records, list):
            errors.append(f"surface_records_missing_records_list:{record_path.relative_to(ROOT)}")
            continue
        record_count += len(records)
        for idx, record in enumerate(records):
            record_id = record.get("active_code_atlas_record_id", f"index_{idx}") if isinstance(record, dict) else f"index_{idx}"
            if not isinstance(record, dict):
                errors.append(f"surface_record_not_object:{record_path.relative_to(ROOT)}:{idx}")
                continue
            for field in EVIDENCE_LIST_FIELDS:
                entries = record.get(field, []) or []
                if not isinstance(entries, list):
                    errors.append(
                        f"evidence_field_not_list:{record_path.relative_to(ROOT)}:{record_id}:{field}"
                    )
                    continue
                for ev_idx, evidence in enumerate(entries):
                    evidence_count += 1
                    prefix = f"{record_path.relative_to(ROOT)}:{record_id}:{field}[{ev_idx}]"
                    if not isinstance(evidence, dict):
                        errors.append(f"evidence_entry_not_object:{prefix}")
                        continue
                    rel_path = evidence.get("path")
                    start = evidence.get("line_start")
                    end = evidence.get("line_end")
                    if not isinstance(rel_path, str) or not rel_path:
                        errors.append(f"evidence_path_missing:{prefix}")
                        continue
                    target = ROOT / rel_path
                    if not target.exists():
                        errors.append(f"evidence_path_missing_on_disk:{prefix}:{rel_path}")
                        continue
                    if not target.is_file():
                        errors.append(f"evidence_path_not_file:{prefix}:{rel_path}")
                        continue
                    checked_files[str(target.relative_to(ROOT))] += 1
                    lc = line_count(target)
                    if not isinstance(start, int) or not isinstance(end, int):
                        errors.append(f"evidence_line_range_not_int:{prefix}:{rel_path}:{start!r}:{end!r}")
                        continue
                    if start < 1 or end < 1 or start > end or end > lc:
                        errors.append(
                            f"evidence_line_range_out_of_bounds:{prefix}:{rel_path}:{start}-{end}:line_count={lc}"
                        )
    if not SURFACE_RECORD_FILES:
        warnings.append("no_surface_record_files_found")
    return {
        "surface_record_file_count": len(SURFACE_RECORD_FILES),
        "surface_record_files": [str(p.relative_to(ROOT)) for p in SURFACE_RECORD_FILES],
        "surface_record_count": record_count,
        "evidence_entry_count": evidence_count,
        "unique_evidence_path_count": len(checked_files),
    }


def validate_registry(errors: list[str]) -> dict[str, object]:
    try:
        registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"registry_yaml_parse_failed:{REGISTRY_PATH.relative_to(ROOT)}:{exc}")
        return {}
    if not isinstance(registry, dict):
        errors.append("registry_top_level_not_mapping")
        return {}

    summary: dict[str, object] = {}
    inventory_specs = {
        "tier_a_registry_reconciliation_inventory": {
            "prefix": "tests/tier_a/",
            "count_key": "tier_a_test_count",
            "registered_count_key": "registered_retained_seed_tier_a",
            "registered_status": "registered_retained_seed_tier_a",
            "outside_count_key": "tier_a_file_registered_outside_retained_seed_tier_a",
            "pending_count_key": "pending_explicit_registry_record",
        },
        "tier_b_registry_reconciliation_inventory": {
            "prefix": "tests/tier_b/",
            "count_key": "tier_b_test_count",
            "registered_count_key": "registered_retained_tier_b",
            "registered_status": "registered_retained_tier_b",
            "outside_count_key": "tier_b_file_registered_outside_retained_tier_b",
            "pending_count_key": "pending_explicit_registry_record",
            "covered_count_key": "covered_by_command_or_owns_after_amendment",
        },
    }

    for inventory_name, spec in inventory_specs.items():
        inventory = registry.get(inventory_name)
        if not isinstance(inventory, dict):
            errors.append(f"registry_inventory_missing_or_not_mapping:{inventory_name}")
            continue
        entries = inventory.get("entries", [])
        if not isinstance(entries, list):
            errors.append(f"registry_inventory_entries_not_list:{inventory_name}")
            entries = []
        declared_total = inventory.get(spec["count_key"])
        if declared_total != len(entries):
            errors.append(
                f"registry_inventory_total_count_mismatch:{inventory_name}:{spec['count_key']}={declared_total}:entries={len(entries)}"
            )
        status_counts = Counter()
        paths: list[str] = []
        for idx, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"registry_inventory_entry_not_mapping:{inventory_name}:{idx}")
                continue
            rel_path = entry.get("path")
            status = entry.get("registry_status")
            if not isinstance(rel_path, str) or not rel_path:
                errors.append(f"registry_inventory_entry_path_missing:{inventory_name}:{idx}")
                continue
            paths.append(rel_path)
            if not rel_path.startswith(spec["prefix"]):
                errors.append(
                    f"registry_inventory_wrong_tier_path:{inventory_name}:{idx}:{rel_path}:expected_prefix={spec['prefix']}"
                )
            if not (ROOT / rel_path).is_file():
                errors.append(f"registry_inventory_path_missing_on_disk:{inventory_name}:{idx}:{rel_path}")
            status_counts[str(status)] += 1
        duplicate_paths = sorted(path for path, count in Counter(paths).items() if count > 1)
        if duplicate_paths:
            errors.append(f"registry_inventory_duplicate_paths:{inventory_name}:{duplicate_paths}")
        counts = inventory.get("counts", {})
        if not isinstance(counts, dict):
            errors.append(f"registry_inventory_counts_not_mapping:{inventory_name}")
            counts = {}
        registered_count = counts.get(spec["registered_count_key"])
        actual_registered = status_counts.get(spec["registered_status"], 0)
        if registered_count != actual_registered:
            errors.append(
                f"registry_inventory_registered_count_mismatch:{inventory_name}:{spec['registered_count_key']}={registered_count}:actual={actual_registered}"
            )
        for optional_count_key in (spec.get("outside_count_key"), spec.get("pending_count_key")):
            if optional_count_key and counts.get(optional_count_key) != 0:
                errors.append(
                    f"registry_inventory_nonzero_exception_count:{inventory_name}:{optional_count_key}={counts.get(optional_count_key)}"
                )
        covered_count_key = spec.get("covered_count_key")
        if covered_count_key and counts.get(covered_count_key) != len(entries):
            errors.append(
                f"registry_inventory_covered_count_mismatch:{inventory_name}:{covered_count_key}={counts.get(covered_count_key)}:entries={len(entries)}"
            )
        summary[inventory_name] = {
            "declared_total": declared_total,
            "entry_count": len(entries),
            "status_counts": dict(sorted(status_counts.items())),
            "declared_counts": counts,
            "duplicate_path_count": len(duplicate_paths),
        }
    return summary


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    evidence_summary = validate_evidence_ranges(errors, warnings)
    registry_summary = validate_registry(errors)
    report = {
        "validation_status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "limitation_statement": LIMITATION_STATEMENT,
        "evidence_range_validation": evidence_summary,
        "retained_registry_inventory_validation": registry_summary,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
