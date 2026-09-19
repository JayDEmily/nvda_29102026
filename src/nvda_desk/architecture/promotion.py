"""Registry-derived promotion runner with clean-worktree invariance."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TextIO

from .proof import load_and_validate_proof_state
from .validation import validate_architecture


def _git_status(repository_root: Path) -> str:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=repository_root,
        text=True,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def run_promotion_set(
    repository_root: Path,
    promotion_set_id: str,
    *,
    check_only: bool = False,
    output: TextIO = sys.stdout,
) -> int:
    before = _git_status(repository_root)
    if before:
        print("FAIL: worktree is not clean before promotion", file=output)
        return 2
    for line in validate_architecture(repository_root):
        print(line, file=output)
    state = load_and_validate_proof_state(repository_root)
    paths = state.paths_for_set(promotion_set_id)
    print(f"promotion set: {promotion_set_id}", file=output)
    print(f"resolved test paths: {len(paths)}", file=output)
    for path in paths:
        print(f"  {path}", file=output)
    if check_only:
        return 0
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *paths],
        cwd=repository_root,
        text=True,
    )
    after = _git_status(repository_root)
    if after != before:
        print("FAIL: promotion execution changed the worktree", file=output)
        return 3
    return completed.returncode
