"""Build the final changed-path and key-file hash inventories."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
WORKER = Path(__file__).resolve().parent
BASELINE = "92c30ef0f1894e8265242b8a0f229daea7ebb603"
CHANGED_PATHS = WORKER / "M13_V6_CHANGED_PATHS.txt"
FILE_HASHES = WORKER / "M13_V6_KEY_FILE_SHA256SUMS.txt"


def _git_lines(*args: str) -> list[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    changed = set(_git_lines("diff", "--name-only", BASELINE))
    changed.update(_git_lines("ls-files", "--others", "--exclude-standard"))
    changed.update(
        (
            CHANGED_PATHS.relative_to(REPO_ROOT).as_posix(),
            FILE_HASHES.relative_to(REPO_ROOT).as_posix(),
        )
    )
    CHANGED_PATHS.write_text(
        "\n".join(sorted(changed)) + "\n",
        encoding="utf-8",
    )

    key_files = (
        REPO_ROOT / "tests/tier_a/persistence/test_m13_state_kernel_contract.py",
        REPO_ROOT / "project_control/canonical_project_manager/modules/M13/M13_PROOF_RECORD.md",
        WORKER / "v6_reference_conforming_source.py",
        WORKER / "v6_configurable_mutant_source.py",
        WORKER / "V6_REENTRANCY_MATRIX.tsv",
        WORKER / "V6_ACTIVE_LIFECYCLE_MATRIX.tsv",
        WORKER / "V6_ATOMIC_RECEIPT_MATRIX.tsv",
        WORKER / "V6_FALSIFICATION_MATRIX.tsv",
        WORKER / "V6_PROOF_TO_N06.tsv",
    )
    source_files = sorted((REPO_ROOT / "src/nvda_desk/m13_state_kernel").glob("*.py"))
    FILE_HASHES.write_text(
        "\n".join(
            f"{_sha256(path)}  {path.relative_to(REPO_ROOT).as_posix()}"
            for path in (*key_files, *source_files)
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"changed_paths={len(changed)}")
    print(f"key_file_hashes={len(key_files) + len(source_files)}")
    print("closeout_inventory=PASS")


if __name__ == "__main__":
    main()
