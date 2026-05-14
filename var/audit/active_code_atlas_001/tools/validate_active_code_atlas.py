#!/usr/bin/env python3
"""Validate the static structural inventory scaffold schema and records."""
from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
SCHEMA_PATH = OUT_DIR / "active_code_atlas_schema.json"
ATLAS_PATH = OUT_DIR / "active_code_atlas.json"
REPORT_PATH = OUT_DIR / "active_code_atlas_validation_report.json"
CURRENT_MAP = ROOT / "NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_count(path: Path) -> int:
    data = path.read_bytes()
    if not data:
        return 1
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def parse_surfaces() -> list[str]:
    surfaces = []
    for line in read(CURRENT_MAP).splitlines():
        if line.startswith("| 5."):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                surfaces.append(cells[1])
    return surfaces


def main() -> None:
    schema = json.loads(read(SCHEMA_PATH))
    atlas = json.loads(read(ATLAS_PATH))
    required_top = schema["top_level_required_fields"]
    required_record = schema["record_required_fields"]
    enum_map = schema["enums"]
    governed_surfaces = parse_surfaces()
    allowed_surfaces = set(governed_surfaces + enum_map.get("blueprint_surface_extra", []))
    errors: list[str] = []
    warnings: list[str] = []
    for key in required_top:
        if key not in atlas:
            errors.append(f"missing top-level field: {key}")
    records = atlas.get("records", [])
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        records = []

    if atlas.get("classification") != "ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001":
        errors.append("top-level classification must be ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001")
    if "static structural evidence only" not in str(atlas.get("limitation_statement", "")).lower():
        errors.append("missing static structural limitation_statement")
    ids = [r.get("active_code_record_id") for r in records if isinstance(r, dict)]
    duplicates = [rid for rid, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate active_code_record_id values: {duplicates[:20]}")
    surfaces_seen = Counter()
    type_counts = Counter()
    status_counts = Counter()
    evidence_status_counts = Counter()
    owner_confidence_counts = Counter()
    for idx, rec in enumerate(records):
        prefix = f"record[{idx}] {rec.get('active_code_record_id', '<missing-id>')}"
        for key in required_record:
            if key not in rec:
                errors.append(f"{prefix}: missing field {key}")
        surface = rec.get("blueprint_surface")
        if surface not in allowed_surfaces:
            errors.append(f"{prefix}: invalid blueprint_surface {surface!r}")
        else:
            surfaces_seen[surface] += 1
        for enum_field in ("evidence_status", "owner_confidence", "native_satisfaction_status", "status"):
            allowed = set(enum_map.get(enum_field, []))
            val = rec.get(enum_field)
            if val not in allowed:
                errors.append(f"{prefix}: invalid {enum_field} {val!r}")
        source_file = rec.get("source_file")
        if source_file:
            path = ROOT / source_file
            if not path.exists():
                if rec.get("status") != "blocked":
                    errors.append(f"{prefix}: source_file does not exist: {source_file}")
            else:
                start = rec.get("source_line_start")
                end = rec.get("source_line_end")
                if not isinstance(start, int) or not isinstance(end, int):
                    errors.append(f"{prefix}: source_line_start/source_line_end must be integers")
                else:
                    lc = line_count(path)
                    if start < 1 or end < 1 or start > end or end > lc:
                        errors.append(f"{prefix}: invalid line range {start}-{end} for {source_file} line_count={lc}")
        if rec.get("record_type") == "docstring_claim" and rec.get("evidence_status") != "docstring_only":
            errors.append(f"{prefix}: docstring_claim must use evidence_status docstring_only")
        if rec.get("record_type") in {"runtime_behaviour", "runtime_module"} and rec.get("native_satisfaction_status") == "satisfied":
            errors.append(f"{prefix}: runtime static evidence cannot claim native_satisfaction_status satisfied")
        type_counts[rec.get("record_type")] += 1
        status_counts[rec.get("status")] += 1
        evidence_status_counts[rec.get("evidence_status")] += 1
        owner_confidence_counts[rec.get("owner_confidence")] += 1
    missing_governed_surfaces = [surface for surface in governed_surfaces if surfaces_seen[surface] == 0]
    if missing_governed_surfaces:
        errors.append(f"missing governed surfaces in records: {missing_governed_surfaces}")
    report = {
        "validation_status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "record_count": len(records),
        "governed_surface_count": len(governed_surfaces),
        "surfaces_seen": dict(sorted(surfaces_seen.items())),
        "type_counts": dict(sorted(type_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "evidence_status_counts": dict(sorted(evidence_status_counts.items())),
        "owner_confidence_counts": dict(sorted(owner_confidence_counts.items())),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
