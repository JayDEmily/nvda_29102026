"""Validate the V6 worker-owned mutation boundary and frozen production source."""

from __future__ import annotations

import compileall
import hashlib
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[6]
BASELINE = "92c30ef0f1894e8265242b8a0f229daea7ebb603"
TEST_PATH = "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
WORKER_PREFIX = "project_control/canonical_project_manager/modules/M13/raw_validation/v6_worker/"
RECORD_PATH = "project_control/canonical_project_manager/modules/M13/M13_PROOF_RECORD.md"


def _git_lines(*args: str) -> list[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()


def _git_blob(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path}"],
        cwd=REPO_ROOT,
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    changed = set(_git_lines("diff", "--name-only", BASELINE))
    changed.update(_git_lines("ls-files", "--others", "--exclude-standard"))
    assert changed
    assert all(
        path == TEST_PATH or path == RECORD_PATH or path.startswith(WORKER_PREFIX)
        for path in changed
    ), sorted(changed)

    source_paths = _git_lines("ls-files", "src/nvda_desk/m13_state_kernel")
    assert source_paths
    for path in source_paths:
        current = (REPO_ROOT / path).read_bytes()
        baseline = _git_blob(path)
        assert current == baseline, path
        print(f"frozen_source_sha256[{path}]={_sha256(current)}")

    for path in (
        "config/proof_blocks.yaml",
        "config/retained_test_registry.yaml",
    ):
        current = (REPO_ROOT / path).read_bytes()
        assert current == _git_blob(path), path
        print(f"frozen_configuration_sha256[{path}]={_sha256(current)}")

    normative_changes = [
        path
        for path in changed
        if path.startswith("docs/")
        or "normative_authority" in path
        or path.endswith("EXEC_PLAN.md")
        or path.endswith("GATE_C_COMPLETION_PROTOCOL.md")
        or path == "ROADMAP_LEDGER_V2.md"
    ]
    assert not normative_changes, normative_changes

    yaml_files = sorted(set(REPO_ROOT.rglob("*.yaml")) | set(REPO_ROOT.rglob("*.yml")))
    for path in yaml_files:
        if any(part in {".venv", ".git"} for part in path.parts):
            continue
        yaml.safe_load(path.read_text(encoding="utf-8"))

    assert compileall.compile_file(REPO_ROOT / TEST_PATH, quiet=1, force=True)
    assert compileall.compile_dir(
        REPO_ROOT / WORKER_PREFIX,
        quiet=1,
        force=True,
    )
    subprocess.run(["git", "diff", "--check"], cwd=REPO_ROOT, check=True)

    print(f"changed_path_count={len(changed)}")
    for path in sorted(changed):
        print(f"changed_path={path}")
    print(f"yaml_file_count={len(yaml_files)}")
    print("frozen_rejected_implementation=PASS")
    print("frozen_configuration=PASS")
    print("normative_document_scan=PASS")
    print("bounded_changed_paths=PASS")
    print("yaml_validation=PASS")
    print("python_compile_validation=PASS")
    print("git_diff_check=PASS")


if __name__ == "__main__":
    main()
