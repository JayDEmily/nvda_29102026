"""Validate frozen surfaces, syntax, configuration and bounded changed paths."""

from __future__ import annotations

import compileall
import hashlib
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE_CHECKPOINT = "e8384ada435097d64f46f5fe01d55e8d833bf1f4"
FROZEN_TEST = REPO_ROOT / "tests/tier_a/persistence/test_m13_state_kernel_contract.py"
FROZEN_TEST_SHA256 = "7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a"
M13_ROOT = REPO_ROOT / "src/nvda_desk/m13_state_kernel"
WORKER_ROOT = Path(__file__).resolve().parent


def _git_lines(*args: str) -> list[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()


def main() -> None:
    frozen_hash = hashlib.sha256(FROZEN_TEST.read_bytes()).hexdigest()
    assert frozen_hash == FROZEN_TEST_SHA256

    assert not _git_lines("diff", "--name-only", SOURCE_CHECKPOINT, "--", "tests")
    assert not _git_lines("ls-files", "--others", "--exclude-standard", "--", "tests")
    assert not _git_lines("diff", "--name-only", SOURCE_CHECKPOINT, "--", "docs")
    assert not _git_lines("diff", "--name-only", SOURCE_CHECKPOINT, "--", "config")

    changed = set(_git_lines("diff", "--name-only", SOURCE_CHECKPOINT))
    changed.update(_git_lines("ls-files", "--others", "--exclude-standard"))
    allowed_prefixes = (
        "src/nvda_desk/m13_state_kernel/",
        "project_control/canonical_project_manager/modules/M13/"
        "raw_validation/implementation_worker/",
        "project_control/canonical_project_manager/modules/M13/"
        "M13_IMPLEMENTATION_WORKER_RECORD.md",
    )
    assert changed
    assert all(path.startswith(allowed_prefixes) for path in changed)

    for config in (
        REPO_ROOT / "config/proof_blocks.yaml",
        REPO_ROOT / "config/retained_test_registry.yaml",
    ):
        parsed = yaml.safe_load(config.read_text(encoding="utf-8"))
        assert parsed is not None

    assert compileall.compile_dir(M13_ROOT, quiet=1, force=True)
    assert compileall.compile_dir(WORKER_ROOT, quiet=1, force=True)

    subprocess.run(["git", "diff", "--check"], cwd=REPO_ROOT, check=True)

    production_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(M13_ROOT.glob("*.py"))
    ).casefold()
    for prohibited in (
        "import tests",
        "raw_validation",
        "reference_conforming",
        "sqlite",
        "multiprocess",
        "crash recovery",
        "restart recovery",
    ):
        assert prohibited not in production_text

    reference = (
        REPO_ROOT / "project_control/canonical_project_manager/modules/M13/raw_validation/"
        "v4_reference_conforming_source.py"
    )
    production_hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(M13_ROOT.glob("*.py"))
    }
    reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    assert reference_hash not in production_hashes.values()

    print(f"frozen_test_sha256={frozen_hash}")
    print("frozen_test_semantics_unchanged=PASS")
    print("normative_docs_unchanged=PASS")
    print("proof_and_retained_config_unchanged=PASS")
    print(f"bounded_changed_paths={len(changed)}")
    print("yaml_validation=PASS")
    print("python_compile_validation=PASS")
    print("git_diff_check=PASS")
    print("prohibited_production_claim_scan=PASS")
    print(f"reference_sha256={reference_hash}")
    for filename, source_hash in production_hashes.items():
        print(f"production_sha256[{filename}]={source_hash}")
    print("material_source_independence_hash_check=PASS")


if __name__ == "__main__":
    main()
