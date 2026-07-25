#!/usr/bin/env python3
"""Portable final validator for P2 Recovery Part 1 auditor correction.

All completion claims are derived from current repository state and fresh command
execution. The input candidate archive path is supplied explicitly by the caller.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

EXPECTED_INPUT_SHA256 = "91fa33be85dd18880cec0234da28dcf313150ca56cfd9b0db91600348aa56e6c"
EXPECTED_BRANCH = "work/NVIDIA_2026_pm001_pm010_restart_20260721"
EXPECTED_HEAD = "21c1e5eccfbb818bdd422afd42117f23b1f74f26"
SCOPE = tuple(f"{number:03d}" for number in range(67, 121))
TEXT_SUFFIXES = {
    "",
    ".csv",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--input-archive", type=Path, required=True)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def forbidden_path_tokens() -> tuple[str, ...]:
    # Fragment construction avoids embedding a worker-specific path in this script.
    return (
        "/" + "mnt" + "/data/",
        "/" + "tmp/",
        "/" + "home" + "/oai/",
        "\\" + "mnt" + "\\data\\",
    )


def current_protected_paths(repo: Path) -> set[str]:
    roots = (
        "config",
        "docs",
        "data/vocabulary",
        "src",
        "tests",
        "project_control/canonical_project_manager/units/PM-019",
        "project_control/canonical_project_manager/units/PM-020",
    )
    result: set[str] = set()
    for root in roots:
        base = repo / root
        if not base.exists():
            continue
        result.update(path.relative_to(repo).as_posix() for path in base.rglob("*") if path.is_file())
    return result


def run_git(repo: Path, *args: str) -> tuple[int, str]:
    process = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return process.returncode, process.stdout.strip()


def validate(repo: Path, input_archive: Path) -> tuple[list[str], dict[str, str]]:
    failures: list[str] = []
    facts: dict[str, str] = {}
    p1 = repo / "project_control/canonical_project_manager/P2_RECOVERY_PART1"
    pm_root = repo / "project_control/canonical_project_manager"
    ledger_path = pm_root / "P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv"

    # Input and repository identity.
    if not input_archive.is_file():
        failures.append("input archive does not exist")
        input_sha = "MISSING"
    else:
        input_sha = sha256_file(input_archive)
        if input_sha != EXPECTED_INPUT_SHA256:
            failures.append("input archive SHA-256 mismatch")
    facts["input_archive_sha256"] = "PASS" if input_sha == EXPECTED_INPUT_SHA256 else "FAIL"

    branch_rc, branch = run_git(repo, "branch", "--show-current")
    head_rc, head = run_git(repo, "rev-parse", "HEAD")
    if branch_rc != 0 or branch != EXPECTED_BRANCH:
        failures.append("Git branch mismatch")
    if head_rc != 0 or head != EXPECTED_HEAD:
        failures.append("Git HEAD mismatch")
    facts["repository_identity"] = "PASS" if branch == EXPECTED_BRANCH and head == EXPECTED_HEAD else "FAIL"

    # Ledger and quarantine scope.
    rows = read_tsv(ledger_path)
    scoped = [row for row in rows if row.get("SEQUENCE") in SCOPE]
    yes_count = sum(row.get("SEMANTICALLY_READ") == "YES" for row in rows)
    no_count = sum(row.get("SEMANTICALLY_READ") == "NO" for row in rows)
    scope_ok = len(rows) == 179 and len(scoped) == 54 and len({row["SEQUENCE"] for row in scoped}) == 54
    scope_ok = scope_ok and all(row.get("SEMANTICALLY_READ") == "YES" for row in scoped)
    if not scope_ok:
        failures.append("Part 1 ledger scope or YES state mismatch")
    facts["ledger_scope"] = "PASS" if scope_ok else "FAIL"
    facts["ledger_counts"] = f"yes={yes_count} no={no_count}"

    quarantine_rows = read_tsv(p1 / "QUARANTINE_MANIFEST.tsv")
    quarantine_ok = len(quarantine_rows) == 54 and {row["SEQUENCE"] for row in quarantine_rows} == set(SCOPE)
    for row in quarantine_rows:
        path = repo / row["QUARANTINE_PATH"]
        if not path.is_file() or sha256_file(path) != row["SHA256"]:
            quarantine_ok = False
            break
    if not quarantine_ok:
        failures.append("quarantine manifest or quarantined receipt hash mismatch")
    facts["quarantine"] = "PASS" if quarantine_ok else "FAIL"

    # Fresh row validation. Import and execute all 54 validators from current receipts.
    row_module = load_module(p1 / "P2_RECOVERY_PART1_VALIDATE_ROW.py", "p2_part1_row_validator")
    row_failures: list[str] = []
    for sequence in SCOPE:
        result = row_module.validate_sequence(repo, sequence)
        if not result.passed:
            row_failures.extend(f"{sequence}:{error}" for error in result.errors)
    if row_failures:
        failures.append(f"row validator failures={len(row_failures)}")
    facts["row_validators"] = "PASS" if not row_failures else "FAIL"
    facts["row_validator_passes"] = str(54 - len({entry.split(':', 1)[0] for entry in row_failures}))

    # Sequence 096 explicit correction contract.
    seq096 = next((row for row in scoped if row["SEQUENCE"] == "096"), None)
    seq096_ok = bool(
        seq096
        and seq096.get("SEMANTICALLY_READ") == "YES"
        and seq096.get("ASSERTION_GROUP_COUNT") == "12"
        and seq096.get("RELATIONSHIP_COUNT") == "12"
        and seq096.get("FINAL_FILE_DISPOSITION") == "BLOCKED_P3_REPAIR"
    )
    if not seq096_ok:
        failures.append("sequence 096 correction contract mismatch")
    facts["sequence_096"] = "PASS" if seq096_ok else "FAIL"

    # Fresh duplicate/generic detector execution.
    duplicate_cmd = [
        sys.executable,
        str(p1 / "P2_RECOVERY_PART1_DUPLICATE_TEXT_DETECTOR.py"),
        "--repo-root",
        str(repo),
        "--report",
        str(p1 / "validation/DUPLICATE_GENERIC_REVIEW.tsv"),
        "--resolutions",
        str(p1 / "validation/DUPLICATE_REVIEW_RESOLUTIONS.tsv"),
    ]
    duplicate_process = subprocess.run(
        duplicate_cmd,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    unresolved_match = re.search(r"(?m)^UNRESOLVED_HITS=(\d+)$", duplicate_process.stdout)
    unresolved = int(unresolved_match.group(1)) if unresolved_match else -1
    duplicate_ok = duplicate_process.returncode == 0 and unresolved == 0
    if not duplicate_ok:
        failures.append("duplicate/generic detector did not reproduce zero unresolved hits")
    facts["duplicate_detector"] = "PASS" if duplicate_ok else "FAIL"
    facts["unresolved_duplicate_reasoning"] = str(unresolved)

    # Fresh 54-file test route.
    inventory_rows = read_tsv(p1 / "TEST_INVENTORY.tsv")
    test_paths = [row["TEST_PATH"] for row in inventory_rows]
    tests_ok = len(test_paths) == 54 and len(set(test_paths)) == 54 and all((repo / path).is_file() for path in test_paths)
    test_output = ""
    test_rc = -1
    passed_count = -1
    if tests_ok:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo / "src")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        test_process = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_paths],
            cwd=repo,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        test_output = test_process.stdout
        test_rc = test_process.returncode
        matches = re.findall(r"(?m)(\d+) passed(?:, [^\n]+)? in [^\n]+", test_output)
        passed_count = int(matches[-1]) if matches else -1
        tests_ok = test_rc == 0 and passed_count == 227
    if not tests_ok:
        failures.append("54-file targeted test route did not reproduce 227 passed with exit 0")
    facts["targeted_tests"] = "PASS" if tests_ok else "FAIL"
    facts["targeted_test_passes"] = str(passed_count)
    facts["targeted_test_exit_code"] = str(test_rc)

    # Out-of-scope ledger and receipt invariance from frozen repair-start evidence.
    baseline_out_rows = read_tsv(p1 / "auditor_repair/BASELINE_OUT_OF_SCOPE_LEDGER.tsv")
    current_out_rows = [row for row in rows if row.get("SEQUENCE") not in SCOPE]
    out_ledger_ok = current_out_rows == baseline_out_rows
    baseline_receipts = read_tsv(p1 / "auditor_repair/BASELINE_OUT_OF_SCOPE_RECEIPTS_SHA256.tsv")
    out_receipts_ok = len(baseline_receipts) == 125
    for row in baseline_receipts:
        path = repo / row["RECEIPT_PATH"]
        if not path.is_file() or sha256_file(path) != row["SHA256"]:
            out_receipts_ok = False
            break
    out_scope_ok = out_ledger_ok and out_receipts_ok
    if not out_scope_ok:
        failures.append("out-of-scope ledger or receipt invariance failed")
    facts["out_of_scope_invariance"] = "PASS" if out_scope_ok else "FAIL"

    # Protected tests/source/config/normative and PM-019/PM-020 surfaces.
    protected_rows = read_tsv(p1 / "auditor_repair/BASELINE_PROTECTED_SURFACES_SHA256.tsv")
    protected_expected = {row["PATH"]: row["SHA256"] for row in protected_rows}
    protected_current = current_protected_paths(repo)
    protected_ok = protected_current == set(protected_expected)
    if protected_ok:
        for relative, expected_sha in protected_expected.items():
            if sha256_file(repo / relative) != expected_sha:
                protected_ok = False
                break
    if not protected_ok:
        failures.append("protected surface set or hashes changed")
    facts["protected_surfaces"] = "PASS" if protected_ok else "FAIL"

    # P3 state is derived from a frozen roadmap hash and its current closed marker.
    roadmap_baseline = read_tsv(p1 / "auditor_repair/BASELINE_ROADMAP_LEDGER_V2_SHA256.tsv")
    roadmap_path = repo / "ROADMAP_LEDGER_V2.md"
    roadmap_text = roadmap_path.read_text(encoding="utf-8") if roadmap_path.is_file() else ""
    roadmap_ok = (
        len(roadmap_baseline) == 1
        and roadmap_baseline[0].get("PATH") == "ROADMAP_LEDGER_V2.md"
        and roadmap_path.is_file()
        and sha256_file(roadmap_path) == roadmap_baseline[0].get("SHA256")
        and "| P3 | closed |" in roadmap_text
    )
    pm019_exit = (repo / "project_control/canonical_project_manager/units/PM-019/PM-019_VALIDATION.exit_code").read_text(encoding="utf-8").strip()
    pm020_exit = (repo / "project_control/canonical_project_manager/units/PM-020/PM-020_PREPACKAGE_VALIDATION.exit_code").read_text(encoding="utf-8").strip()
    state_ok = protected_ok and roadmap_ok and pm019_exit == "1" and pm020_exit == "1"
    if not state_ok:
        failures.append("PM-019, PM-020 or P3 frozen state mismatch")
    facts["pm019_pm020_p3_unchanged"] = "PASS" if state_ok else "FAIL"
    facts["p2_complete"] = "NO" if pm019_exit != "0" or pm020_exit != "0" else "UNKNOWN"
    facts["p3_started"] = "NO" if roadmap_ok else "UNKNOWN"

    # Evidence containment and worker-path independence.
    misplaced = [
        path.name
        for path in pm_root.iterdir()
        if path.name.startswith("P2_RECOVERY_PART1") and path.name != "P2_RECOVERY_PART1"
    ]
    if misplaced:
        failures.append("Part 1 evidence exists outside its authorised directory")
    facts["evidence_containment"] = "PASS" if not misplaced else "FAIL"

    path_hits: list[str] = []
    tokens = forbidden_path_tokens()
    for path in p1.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(token in text for token in tokens):
            path_hits.append(path.relative_to(repo).as_posix())
    if path_hits:
        failures.append(f"worker-absolute path hits={len(path_hits)}")
    facts["worker_absolute_paths"] = "PASS" if not path_hits else "FAIL"
    facts["worker_absolute_path_count"] = str(len(path_hits))

    all_gates = not failures
    facts["part_1_complete"] = "YES" if all_gates else "NO"
    facts["result"] = "PASS" if all_gates else "FAIL"
    return failures, facts


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    input_archive = args.input_archive.resolve()
    failures, facts = validate(repo, input_archive)

    ordered = (
        "input_archive_sha256",
        "repository_identity",
        "ledger_scope",
        "ledger_counts",
        "quarantine",
        "sequence_096",
        "row_validators",
        "row_validator_passes",
        "duplicate_detector",
        "unresolved_duplicate_reasoning",
        "targeted_tests",
        "targeted_test_passes",
        "targeted_test_exit_code",
        "out_of_scope_invariance",
        "protected_surfaces",
        "pm019_pm020_p3_unchanged",
        "evidence_containment",
        "worker_absolute_paths",
        "worker_absolute_path_count",
        "part_1_complete",
        "p2_complete",
        "p3_started",
        "result",
    )
    for key in ordered:
        print(f"{key}={facts.get(key, 'UNKNOWN')}")
    for failure in failures:
        print(f"failure={failure}")
    return 0 if facts.get("result") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
