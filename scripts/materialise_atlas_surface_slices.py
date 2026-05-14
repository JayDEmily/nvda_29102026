"""Materialise Atlas/Bridge records into blueprint-surface slice files.

This script uses only Python standard-library modules. It reads the immutable
Atlas/Bridge evidence files and writes derived, deterministic slice files under
``var/audit/atlas_surface_slices`` so future tranche work can load one bounded
surface instead of repeatedly loading the full native ledger and Atlas bundle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NATIVE_LEDGER = Path("var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json")
RAW_ATLAS = Path("var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json")
COVERAGE_VIEW = Path("var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json")
OWNER_MAP_VIEW = Path("var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json")
OUT_DIR = Path("var/audit/atlas_surface_slices")
SLICE_DIR = OUT_DIR / "slices"
MANIFEST = OUT_DIR / "atlas_surface_slice_manifest.json"
CHECKSUMS = OUT_DIR / "atlas_surface_slice_checksums.json"
SLICE_SCHEMA = OUT_DIR / "atlas_surface_slice.schema.json"


def read_json(path: Path) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with (ROOT / path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(surface: str) -> str:
    slug = surface.strip().lower()
    slug = slug.replace("/", " ")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    if not slug:
        raise ValueError(f"Cannot slugify empty surface: {surface!r}")
    return slug


def counter_for(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(record.get(key)) for record in records).items()))


def build_coverage_index(coverage: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for file_index, file_entry in enumerate(coverage.get("files", [])):
        for range_index, range_entry in enumerate(file_entry.get("ranges", [])):
            atlas_record_id = range_entry.get("atlas_record_id")
            if not atlas_record_id:
                continue
            by_id[atlas_record_id].append(
                {
                    "coverage_file_index": file_index,
                    "coverage_range_index": range_index,
                    "source_file": file_entry.get("source_file"),
                    "file_status": file_entry.get("file_status"),
                    "bounded_batch_status": file_entry.get("bounded_batch_status"),
                    "file_line_start": file_entry.get("line_start"),
                    "file_line_end": file_entry.get("line_end"),
                    "range_line_start": range_entry.get("line_start"),
                    "range_line_end": range_entry.get("line_end"),
                    "disposition": range_entry.get("disposition"),
                }
            )
    return dict(by_id)


def build_owner_index(owner_map: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for owner_index, owner_entry in enumerate(owner_map.get("owners", [])):
        summary = {
            "owner_map_index": owner_index,
            "lawful_owner_candidate": owner_entry.get("lawful_owner_candidate"),
            "owner_confidence": owner_entry.get("owner_confidence"),
            "record_count": owner_entry.get("record_count"),
            "status_counts": owner_entry.get("status_counts"),
            "proof_families": owner_entry.get("proof_families"),
            "notes": owner_entry.get("notes"),
        }
        for atlas_record_id in owner_entry.get("record_ids", []):
            by_id[atlas_record_id].append(summary)
    return dict(by_id)


def validate_source_inputs(
    native_records: list[dict[str, Any]],
    raw_records: list[dict[str, Any]],
    coverage_index: dict[str, list[dict[str, Any]]],
    owner_index: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    native_ids = [record["atlas_record_id"] for record in native_records]
    raw_ids = [record["atlas_record_id"] for record in raw_records]
    duplicate_native_ids = sorted(
        [record_id for record_id, count in Counter(native_ids).items() if count > 1]
    )
    duplicate_raw_ids = sorted(
        [record_id for record_id, count in Counter(raw_ids).items() if count > 1]
    )
    raw_set = set(raw_ids)
    native_set = set(native_ids)
    missing_raw = sorted(native_set - raw_set)
    coverage_unknown = sorted(set(coverage_index) - native_set)
    owner_unknown = sorted(set(owner_index) - native_set)
    return {
        "native_record_count": len(native_records),
        "raw_record_count": len(raw_records),
        "duplicate_native_atlas_record_ids": duplicate_native_ids,
        "duplicate_raw_atlas_record_ids": duplicate_raw_ids,
        "native_records_missing_raw_atlas_record": missing_raw,
        "coverage_refs_not_in_native_ledger": coverage_unknown,
        "owner_refs_not_in_native_ledger": owner_unknown,
    }


def make_slice_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "atlas_surface_slice.schema.json",
        "title": "Atlas surface slice",
        "type": "object",
        "required": [
            "slice_name",
            "blueprint_surface",
            "record_count",
            "source_files",
            "counts",
            "records",
        ],
        "properties": {
            "slice_name": {"type": "string"},
            "blueprint_surface": {"type": "string"},
            "record_count": {"type": "integer", "minimum": 0},
            "source_files": {"type": "object"},
            "counts": {"type": "object"},
            "records": {"type": "array"},
        },
    }


def materialise() -> dict[str, Any]:
    native_ledger = read_json(NATIVE_LEDGER)
    raw_atlas = read_json(RAW_ATLAS)
    coverage = read_json(COVERAGE_VIEW)
    owner_map = read_json(OWNER_MAP_VIEW)

    native_records = native_ledger["records"]
    raw_records = raw_atlas["records"]
    raw_by_id = {record["atlas_record_id"]: record for record in raw_records}
    coverage_index = build_coverage_index(coverage)
    owner_index = build_owner_index(owner_map)
    validation = validate_source_inputs(native_records, raw_records, coverage_index, owner_index)
    if (
        validation["duplicate_native_atlas_record_ids"]
        or validation["duplicate_raw_atlas_record_ids"]
        or validation["native_records_missing_raw_atlas_record"]
        or validation["coverage_refs_not_in_native_ledger"]
        or validation["owner_refs_not_in_native_ledger"]
    ):
        raise RuntimeError(f"Atlas source validation failed: {validation}")

    if (ROOT / OUT_DIR).exists():
        shutil.rmtree(ROOT / OUT_DIR)
    (ROOT / SLICE_DIR).mkdir(parents=True, exist_ok=True)
    write_json(SLICE_SCHEMA, make_slice_schema())

    source_files = {
        "native_intent_satisfaction_ledger": {
            "path": str(NATIVE_LEDGER),
            "sha256": sha256_file(NATIVE_LEDGER),
            "record_count": len(native_records),
        },
        "legacy_intent_atlas": {
            "path": str(RAW_ATLAS),
            "sha256": sha256_file(RAW_ATLAS),
            "record_count": len(raw_records),
        },
        "legacy_file_coverage_view": {
            "path": str(COVERAGE_VIEW),
            "sha256": sha256_file(COVERAGE_VIEW),
            "file_count": len(coverage.get("files", [])),
        },
        "legacy_owner_map_view": {
            "path": str(OWNER_MAP_VIEW),
            "sha256": sha256_file(OWNER_MAP_VIEW),
            "owner_count": len(owner_map.get("owners", [])),
        },
    }

    by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in native_records:
        by_surface[record["blueprint_surface"]].append(record)

    surfaces: list[dict[str, Any]] = []
    generated_paths: list[Path] = [SLICE_SCHEMA]
    all_slice_ids: list[str] = []
    for surface in sorted(by_surface):
        records = by_surface[surface]
        slug = slugify(surface)
        slice_path = SLICE_DIR / f"{slug}.json"
        slice_records = []
        for satisfaction_record in records:
            atlas_record_id = satisfaction_record["atlas_record_id"]
            all_slice_ids.append(atlas_record_id)
            slice_records.append(
                {
                    "satisfaction_record_id": satisfaction_record.get("satisfaction_record_id"),
                    "atlas_record_id": atlas_record_id,
                    "intent_unit_id": satisfaction_record.get("intent_unit_id"),
                    "satisfaction_record": satisfaction_record,
                    "legacy_intent_record": raw_by_id[atlas_record_id],
                    "coverage_refs": coverage_index.get(atlas_record_id, []),
                    "owner_refs": owner_index.get(atlas_record_id, []),
                }
            )
        slice_data = {
            "slice_name": slug,
            "blueprint_surface": surface,
            "status": "derived_materialised_slice",
            "record_count": len(slice_records),
            "source_files": source_files,
            "counts": {
                "native_satisfaction_status": counter_for(records, "native_satisfaction_status"),
                "implementation_leaf_type": counter_for(records, "implementation_leaf_type"),
                "implementation_leaf_required": counter_for(
                    records, "implementation_leaf_required"
                ),
                "blueprint_surface_status": counter_for(records, "blueprint_surface_status"),
                "proof_resolution": counter_for(records, "proof_resolution"),
                "existing_test_decision": counter_for(records, "existing_test_decision"),
            },
            "records": slice_records,
        }
        write_json(slice_path, slice_data)
        generated_paths.append(slice_path)
        surfaces.append(
            {
                "blueprint_surface": surface,
                "slice_name": slug,
                "path": str(slice_path),
                "record_count": len(slice_records),
                "counts": slice_data["counts"],
            }
        )

    duplicate_slice_ids = sorted(
        [record_id for record_id, count in Counter(all_slice_ids).items() if count > 1]
    )
    manifest = {
        "manifest_name": "atlas_surface_slice_manifest",
        "schema_version": "1.0",
        "status": "closed",
        "generated_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "purpose": "Materialised blueprint_surface slices for bounded Atlas migration work.",
        "source_files": source_files,
        "validation": {
            **validation,
            "slice_count": len(surfaces),
            "total_records_across_slices": len(all_slice_ids),
            "duplicate_atlas_record_ids_across_slices": duplicate_slice_ids,
            "slice_total_matches_native_record_count": len(all_slice_ids) == len(native_records),
        },
        "surfaces": surfaces,
    }
    manifest["checksum_manifest_path"] = str(CHECKSUMS)
    write_json(MANIFEST, manifest)
    generated_paths.append(MANIFEST)

    generated_file_checksums = {
        str(path): sha256_file(path) for path in sorted(generated_paths, key=str)
    }
    checksum_manifest = {
        "manifest_name": "atlas_surface_slice_checksums",
        "schema_version": "1.0",
        "status": "closed",
        "generated_at_utc": manifest["generated_at_utc"],
        "source_files": source_files,
        "generated_file_checksums": generated_file_checksums,
    }
    write_json(CHECKSUMS, checksum_manifest)

    return manifest


def validate_outputs() -> dict[str, Any]:
    manifest = read_json(MANIFEST)
    checksums = read_json(CHECKSUMS)
    failures: list[str] = []
    surfaces = manifest.get("surfaces", [])
    total = 0
    seen: set[str] = set()
    for surface in surfaces:
        path = Path(surface["path"])
        data = read_json(path)
        if data["blueprint_surface"] != surface["blueprint_surface"]:
            failures.append(f"surface mismatch for {path}")
        if data["record_count"] != len(data["records"]):
            failures.append(f"record_count mismatch for {path}")
        if data["record_count"] != surface["record_count"]:
            failures.append(f"manifest count mismatch for {path}")
        total += data["record_count"]
        for record in data["records"]:
            atlas_record_id = record["atlas_record_id"]
            if atlas_record_id in seen:
                failures.append(f"duplicate atlas_record_id across slices: {atlas_record_id}")
            seen.add(atlas_record_id)
    if total != manifest["validation"]["native_record_count"]:
        failures.append("slice total does not match native record count")
    for path_str, expected in checksums["generated_file_checksums"].items():
        actual = sha256_file(Path(path_str))
        if actual != expected:
            failures.append(f"checksum mismatch for {path_str}")
    return {
        "result": "passed" if not failures else "failed",
        "failures": failures,
        "slice_count": len(surfaces),
        "total_records_across_slices": total,
        "unique_atlas_record_ids_across_slices": len(seen),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate existing slice outputs without regenerating them",
    )
    args = parser.parse_args()
    if not args.validate_only:
        manifest = materialise()
        print(
            json.dumps(
                {
                    "generated": True,
                    "slice_count": len(manifest["surfaces"]),
                    "total_records": manifest["validation"]["total_records_across_slices"],
                },
                indent=2,
            )
        )
    validation = validate_outputs()
    print(json.dumps(validation, indent=2))
    if validation["result"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
