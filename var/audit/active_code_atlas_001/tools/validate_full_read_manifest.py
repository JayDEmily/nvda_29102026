#!/usr/bin/env python3
"""Validate FULL_READ_MANIFEST files against current repository files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ACTIVE_CODE_ATLAS_DIR = ROOT / "var" / "audit" / "active_code_atlas_001"
MANIFEST_DIR = ACTIVE_CODE_ATLAS_DIR / "full_read_manifests"
REPORT_PATH = ACTIVE_CODE_ATLAS_DIR / "reports" / "validate_full_read_manifest_output.json"


def file_metadata(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "byte_count": len(data),
        "line_count": 0 if not data else data.count(b"\n") + (0 if data.endswith(b"\n") else 1),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def as_manifest_paths(selected: list[str] | None) -> list[Path]:
    if selected:
        return [ROOT / path for path in selected]
    return sorted(MANIFEST_DIR.glob("*.json"))


def validate_chunk_ranges(
    *,
    errors: list[str],
    manifest_rel: str,
    entry_idx: int,
    entry_path: str,
    read_method: str,
    line_count: int,
    chunk_ranges: Any,
) -> None:
    is_chunked = "chunk" in read_method.lower()
    if is_chunked and not chunk_ranges:
        errors.append(f"chunk_ranges_required_for_chunked_read:{manifest_rel}:{entry_idx}:{entry_path}")
        return
    if chunk_ranges in (None, []):
        return
    if not isinstance(chunk_ranges, list):
        errors.append(f"chunk_ranges_not_list:{manifest_rel}:{entry_idx}:{entry_path}")
        return
    previous_end = 0
    for range_idx, chunk_range in enumerate(chunk_ranges):
        if not isinstance(chunk_range, dict):
            errors.append(f"chunk_range_not_object:{manifest_rel}:{entry_idx}:{entry_path}:{range_idx}")
            continue
        start = chunk_range.get("start_line")
        end = chunk_range.get("end_line")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"chunk_range_bounds_not_int:{manifest_rel}:{entry_idx}:{entry_path}:{range_idx}")
            continue
        if start < 1 or end < 1 or start > end or end > line_count:
            errors.append(
                f"chunk_range_out_of_bounds:{manifest_rel}:{entry_idx}:{entry_path}:{range_idx}:{start}-{end}:line_count={line_count}"
            )
        if start <= previous_end:
            errors.append(
                f"chunk_ranges_not_ordered:{manifest_rel}:{entry_idx}:{entry_path}:{range_idx}:{start}-{end}:previous_end={previous_end}"
            )
        previous_end = end


def validate_manifest(path: Path, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    manifest_rel = str(path.relative_to(ROOT)) if path.exists() else str(path)
    if not path.exists():
        errors.append(f"manifest_missing:{manifest_rel}")
        return {"manifest": manifest_rel, "entry_count": 0}
    if not path.is_file():
        errors.append(f"manifest_not_file:{manifest_rel}")
        return {"manifest": manifest_rel, "entry_count": 0}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"manifest_json_parse_failed:{manifest_rel}:{exc}")
        return {"manifest": manifest_rel, "entry_count": 0}
    if not isinstance(payload, dict):
        errors.append(f"manifest_top_level_not_object:{manifest_rel}")
        return {"manifest": manifest_rel, "entry_count": 0}
    entries = payload.get("entries")
    if not isinstance(entries, list):
        errors.append(f"manifest_entries_missing_or_not_list:{manifest_rel}")
        return {"manifest": manifest_rel, "entry_count": 0}

    seen_paths: set[str] = set()
    stale_count = 0
    full_read_false_count = 0
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"manifest_entry_not_object:{manifest_rel}:{idx}")
            continue
        entry_path = entry.get("path")
        if not isinstance(entry_path, str) or not entry_path:
            errors.append(f"manifest_entry_path_missing:{manifest_rel}:{idx}")
            continue
        if entry_path in seen_paths:
            errors.append(f"manifest_duplicate_path:{manifest_rel}:{idx}:{entry_path}")
        seen_paths.add(entry_path)
        target = ROOT / entry_path
        if not target.exists():
            errors.append(f"manifest_entry_path_missing_on_disk:{manifest_rel}:{idx}:{entry_path}")
            continue
        if not target.is_file():
            errors.append(f"manifest_entry_path_not_file:{manifest_rel}:{idx}:{entry_path}")
            continue
        actual = file_metadata(target)
        for field in ("byte_count", "line_count", "sha256"):
            if entry.get(field) != actual[field]:
                stale_count += 1 if field == "sha256" else 0
                errors.append(
                    f"manifest_entry_stale_{field}:{manifest_rel}:{idx}:{entry_path}:manifest={entry.get(field)!r}:actual={actual[field]!r}"
                )
        full_read = entry.get("full_read")
        if not isinstance(full_read, bool):
            errors.append(f"manifest_entry_full_read_not_bool:{manifest_rel}:{idx}:{entry_path}")
        elif full_read is False:
            full_read_false_count += 1
        read_method = entry.get("read_method")
        if not isinstance(read_method, str) or not read_method:
            errors.append(f"manifest_entry_read_method_missing:{manifest_rel}:{idx}:{entry_path}")
            read_method = ""
        validate_chunk_ranges(
            errors=errors,
            manifest_rel=manifest_rel,
            entry_idx=idx,
            entry_path=entry_path,
            read_method=read_method,
            line_count=actual["line_count"],
            chunk_ranges=entry.get("chunk_ranges"),
        )
    if not entries:
        warnings.append(f"manifest_entries_empty:{manifest_rel}")
    return {
        "manifest": manifest_rel,
        "entry_count": len(entries),
        "unique_path_count": len(seen_paths),
        "stale_hash_mismatch_count": stale_count,
        "full_read_false_count": full_read_false_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="*", help="Optional manifest path(s) relative to repo root.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    manifest_paths = as_manifest_paths(args.manifest)
    summaries = [validate_manifest(path, errors, warnings) for path in manifest_paths]
    if not manifest_paths:
        warnings.append(f"no_manifest_files_found:{MANIFEST_DIR.relative_to(ROOT)}")
    report = {
        "validation_status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "manifest_count": len(manifest_paths),
        "manifests": summaries,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
