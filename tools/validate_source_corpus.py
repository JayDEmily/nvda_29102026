#!/usr/bin/env python3
"""Mechanically validate the immutable two-tranche reconstruction corpus."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SOURCE_MANIFEST.tsv"
EXPECTED = {"A_original": 61, "B_successor": 37}
EXPECTED_TOTAL = sum(EXPECTED.values())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    if not MANIFEST.is_file():
        fail("SOURCE_MANIFEST.tsv is missing")

    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    if len(rows) != EXPECTED_TOTAL:
        fail(f"manifest has {len(rows)} rows; expected {EXPECTED_TOTAL}")

    required_columns = {
        "source_id",
        "tranche",
        "repository_path",
        "sha256",
        "recovered_git_blob",
        "original_repository_path",
        "status",
    }
    missing_columns = required_columns.difference(rows[0].keys() if rows else set())
    if missing_columns:
        fail(f"manifest is missing columns: {sorted(missing_columns)}")

    ids = [row["source_id"] for row in rows]
    paths = [row["repository_path"] for row in rows]
    if len(ids) != len(set(ids)):
        fail("source IDs are not unique")
    if len(paths) != len(set(paths)):
        fail("repository paths are not unique")

    counts = Counter(row["tranche"] for row in rows)
    if dict(counts) != EXPECTED:
        fail(f"tranche counts are {dict(counts)}; expected {EXPECTED}")

    manifest_paths: set[str] = set()
    for row in rows:
        relpath = row["repository_path"]
        manifest_paths.add(relpath)
        path = ROOT / relpath
        if not path.is_file():
            fail(f"manifest path does not exist: {relpath}")
        if path.stat().st_size == 0:
            fail(f"source document is empty: {relpath}")
        observed_hash = sha256(path)
        if observed_hash != row["sha256"]:
            fail(
                f"SHA-256 mismatch for {relpath}: "
                f"manifest={row['sha256']} observed={observed_hash}"
            )
        if row["status"] != "admitted_immutable_source":
            fail(f"unexpected status for {relpath}: {row['status']}")
        if row["tranche"] == "B_successor":
            if not row["recovered_git_blob"]:
                fail(f"successor source lacks recovered Git blob: {relpath}")
            if not row["original_repository_path"].startswith("var/audit/briefs/"):
                fail(f"successor source lacks original brief path: {relpath}")

    observed_paths = {
        path.relative_to(ROOT).as_posix()
        for folder in (ROOT / "source_planning", ROOT / "source_successor_briefs")
        for path in folder.glob("*.md")
    }
    if observed_paths != manifest_paths:
        missing = sorted(manifest_paths - observed_paths)
        extra = sorted(observed_paths - manifest_paths)
        fail(f"source tree and manifest differ; missing={missing}, extra={extra}")

    print(
        "PASS: 98 immutable source documents validated "
        "(61 original + 37 successor); IDs, paths and SHA-256 values are consistent"
    )
    print(
        "NOTE: this script validates corpus identity and completeness, "
        "not semantic authority"
    )


if __name__ == "__main__":
    main()
