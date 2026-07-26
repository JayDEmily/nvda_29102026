"""Write deterministic changed-path and SHA-256 manifests for the worker checkpoint."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER_ROOT = Path(__file__).resolve().parent
SOURCE_CHECKPOINT = "e8384ada435097d64f46f5fe01d55e8d833bf1f4"
HASH_MANIFEST = WORKER_ROOT / "M13_IMPLEMENTATION_EVIDENCE_SHA256SUMS.txt"
PATH_MANIFEST = WORKER_ROOT / "M13_IMPLEMENTATION_CHANGED_PATHS.txt"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", SOURCE_CHECKPOINT],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    paths = sorted(set(changed + untracked))
    PATH_MANIFEST.write_text("\n".join(paths) + "\n", encoding="utf-8")

    evidence_paths = sorted(
        path
        for path in WORKER_ROOT.rglob("*")
        if path.is_file()
        and path != HASH_MANIFEST
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    production_paths = sorted(
        path
        for path in (REPO_ROOT / "src/nvda_desk/m13_state_kernel").glob("*.py")
        if path.is_file()
    )
    authority_paths = [
        REPO_ROOT / "tests/tier_a/persistence/test_m13_state_kernel_contract.py",
        REPO_ROOT / "config/proof_blocks.yaml",
        REPO_ROOT / "config/retained_test_registry.yaml",
        REPO_ROOT / "project_control/canonical_project_manager/modules/M13/"
        "M13_IMPLEMENTATION_WORKER_RECORD.md",
    ]
    manifest_paths = sorted(set(evidence_paths + production_paths + authority_paths))
    lines = [f"{_hash(path)}  {path.relative_to(REPO_ROOT)}" for path in manifest_paths]
    HASH_MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"changed_paths={len(paths)}")
    print(f"tracked_hash_targets={len(manifest_paths)}")
    print("evidence_manifest=PASS")


if __name__ == "__main__":
    main()
