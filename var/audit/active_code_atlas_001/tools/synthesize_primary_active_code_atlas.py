#!/usr/bin/env python3
"""Synthesize the primary active-code Atlas from read-adjudicated surface records."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
OUTPUT_PATH = ACTIVE_DIR / "primary_active_code_atlas.json"
REPORT_PATH = ACTIVE_DIR / "primary_synthesis" / "reports" / "primary_active_code_atlas_synthesis_report.json"
LIMITATION_STATEMENT = (
    "Primary active-code Atlas synthesized only from read-adjudicated surface records; "
    "this does not import donor Atlas behaviour, mutate runtime code, or prove feature maturity."
)
EXPECTED_SURFACE_COUNT = 18


def _record_files() -> list[Path]:
    return sorted(path for path in ACTIVE_DIR.glob("*/*records.json") if path.is_file())


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    record_files = _record_files()
    record_ids: Counter[str] = Counter()
    surface_counts: Counter[str] = Counter()

    for path in record_files:
        payload = _load_json(path)
        payload_records = payload.get("records")
        if not isinstance(payload_records, list):
            errors.append(f"records_missing_or_not_list:{path.relative_to(ROOT)}")
            continue
        for idx, record in enumerate(payload_records):
            if not isinstance(record, dict):
                errors.append(f"record_not_object:{path.relative_to(ROOT)}:{idx}")
                continue
            record_id = record.get("active_code_atlas_record_id")
            surface = record.get("surface")
            if not isinstance(record_id, str) or not record_id:
                errors.append(f"record_id_missing:{path.relative_to(ROOT)}:{idx}")
                continue
            if not isinstance(surface, str) or not surface:
                errors.append(f"surface_missing:{path.relative_to(ROOT)}:{record_id}")
                continue
            record_ids[record_id] += 1
            surface_counts[surface] += 1
            copied = dict(record)
            copied["source_surface_record_file"] = str(path.relative_to(ROOT))
            records.append(copied)

    duplicates = sorted(record_id for record_id, count in record_ids.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate_active_code_atlas_record_ids:{duplicates}")
    if len(surface_counts) != EXPECTED_SURFACE_COUNT:
        errors.append(
            f"surface_count_mismatch:expected={EXPECTED_SURFACE_COUNT}:actual={len(surface_counts)}"
        )
    if not records:
        errors.append("no_records_synthesized")

    records.sort(key=lambda item: item["active_code_atlas_record_id"])
    output = {
        "schema_version": "primary_active_code_atlas_v1",
        "created_utc": "2026-05-12T00:00:00Z",
        "status": "synthesized_from_read_adjudicated_surface_records" if not errors else "synthesis_failed",
        "limitation_statement": LIMITATION_STATEMENT,
        "source_record_file_count": len(record_files),
        "record_count": len(records),
        "surface_count": len(surface_counts),
        "surface_counts": dict(sorted(surface_counts.items())),
        "records": records,
    }
    report = {
        "validation_status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "source_record_file_count": len(record_files),
        "record_count": len(records),
        "surface_count": len(surface_counts),
        "surface_counts": dict(sorted(surface_counts.items())),
        "duplicate_record_id_count": len(duplicates),
        "limitation_statement": LIMITATION_STATEMENT,
        "output_path": str(OUTPUT_PATH.relative_to(ROOT)),
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
