"""Verify the sole V6 source archive and its frozen proof/implementation facts."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_ARCHIVE_SHA256 = "68f2624ac7df594eb15b3f346d21be23af3247ecfe343bce83080d8bb44893cd"
EXPECTED_BRANCH = "review/m13-implementation-v1"
EXPECTED_COMMIT = "92c30ef0f1894e8265242b8a0f229daea7ebb603"
EXPECTED_PROOF_SHA256 = "7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a"
IMPLEMENTATION_COMMIT = "ddbd7257ab7305b2a3648f9f1d810b07670808aa"
DISPOSITION = (
    "CLOSED:M13_PROOF_REPAIR_V6_REQUIRED_FOR_REENTRANT_EXECUTION_" "AND_RECEIPT_CONTRACT_TRUTH"
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_source_checkpoint.py ARCHIVE")
    archive = Path(sys.argv[1]).resolve()
    assert archive.is_file()
    archive_hash = _sha256(archive)
    assert archive_hash == EXPECTED_ARCHIVE_SHA256
    subprocess.run(["tar", "-tzf", str(archive)], check=True, stdout=subprocess.DEVNULL)

    with tempfile.TemporaryDirectory(prefix="m13-v6-source-verify-") as temp:
        extract_root = Path(temp)
        subprocess.run(
            [
                "tar",
                "--no-same-owner",
                "-xzf",
                str(archive),
                "-C",
                str(extract_root),
            ],
            check=True,
        )
        repositories = [path.parent for path in extract_root.rglob(".git") if path.is_dir()]
        assert len(repositories) == 1
        repo = repositories[0]
        branch = _git(repo, "branch", "--show-current")
        commit = _git(repo, "rev-parse", "HEAD")
        status = _git(repo, "status", "--porcelain")
        history_count = int(_git(repo, "rev-list", "--count", "--all"))
        assert branch == EXPECTED_BRANCH
        assert commit == EXPECTED_COMMIT
        assert status == ""
        assert history_count >= 195

        proof = repo / "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
        proof_hash = _sha256(proof)
        assert proof_hash == EXPECTED_PROOF_SHA256

        review = (
            repo / "project_control/canonical_project_manager/modules/M13/"
            "M13_IMPLEMENTATION_PM_REVIEW_V1.md"
        ).read_text(encoding="utf-8")
        assert DISPOSITION in review
        gate = (
            repo / "project_control/canonical_project_manager/" "GATE_C_COMPLETION_PROTOCOL.md"
        ).read_text(encoding="utf-8")
        ledger = (repo / "ROADMAP_LEDGER_V2.md").read_text(encoding="utf-8")
        assert DISPOSITION in gate
        assert "`M13-IMPLEMENT`, merge, M01 and all later modules remain closed" in gate
        assert "M13 merge/completion, M01 and all later modules remain closed" in ledger

        source_diff = _git(
            repo,
            "diff",
            "--name-only",
            IMPLEMENTATION_COMMIT,
            "HEAD",
            "--",
            "src/nvda_desk/m13_state_kernel",
        )
        assert source_diff == ""

        print(f"archive={archive.name}")
        print(f"archive_sha256={archive_hash}")
        print("archive_integrity=PASS")
        print(f"branch={branch}")
        print(f"commit={commit}")
        print("worktree=clean")
        print(f"reachable_history_commits={history_count}")
        print(f"frozen_proof_sha256={proof_hash}")
        print("complete_git_history=PASS")
        print("rejected_implementation_unchanged=PASS")
        print(f"pm_disposition={DISPOSITION}")
        print("m13_implementation_merge_m01_later_modules=CLOSED")
        print("source_checkpoint=PASS")


if __name__ == "__main__":
    main()
