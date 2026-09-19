#!/usr/bin/env python3
"""Run the separately admitted product-proof aggregate when it is ready."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from validate_product_proof import validate_product_proof


def _git_status(repository_root: Path) -> str:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=repository_root,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping document")
    return value


def run_product_proof(repository_root: Path, aggregate_id: str) -> int:
    before = _git_status(repository_root)
    if before:
        print("FAIL: worktree is not clean before product-proof aggregate")
        return 2
    try:
        for line in validate_product_proof(repository_root):
            print(line)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    config_root = repository_root / "config" / "product_proof"
    aggregates = _load_yaml(config_root / "aggregates.yaml")["aggregates"]
    aggregate = next((item for item in aggregates if item["id"] == aggregate_id), None)
    if aggregate is None:
        print(f"FAIL: unknown product-proof aggregate {aggregate_id}")
        return 3
    if aggregate["state"] != "READY_FOR_PROOF":
        print(
            "FAIL: product-proof aggregate is not ready; "
            f"state={aggregate['state']} (this is not a product-proof PASS)"
        )
        return 4

    families = _load_yaml(config_root / "families.yaml")["families"]
    by_id = {item["id"]: item for item in families}
    paths = [by_id[family_id]["path"] for family_id in aggregate["family_ids"]]
    if not paths:
        print("FAIL: ready product-proof aggregate resolved zero physical test paths")
        return 5
    print(f"product-proof aggregate: {aggregate_id}")
    print(f"resolved physical test paths: {len(paths)}")
    for path in paths:
        print(f"  {path}")
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *paths],
        cwd=repository_root,
        text=True,
        check=False,
    )
    after = _git_status(repository_root)
    if after != before:
        print("FAIL: product-proof execution changed the worktree")
        return 6
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate", default="raw_signal_occurrence_truth_product")
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    root = (args.repository or Path(__file__).resolve().parents[1]).resolve()
    return run_product_proof(root, args.aggregate)


if __name__ == "__main__":
    raise SystemExit(main())
