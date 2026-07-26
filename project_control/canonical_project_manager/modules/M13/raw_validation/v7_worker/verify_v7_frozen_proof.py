"""Verify source/AST and collected-case preservation of the frozen V6 proof."""

from __future__ import annotations

import ast
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
TEST_PATH = Path("tests/tier_a/persistence/test_m13_state_kernel_contract.py")
BASELINE = "cf44a74385536672237de4747d084faaa7971b47"
EXPECTED_HASH = "dc52e96ea1071f112e8c2fca1d23e79551b9159908904f5be3b096c756385633"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _functions(source: bytes) -> dict[str, str]:
    tree = ast.parse(source)
    return {
        node.name: _sha256(ast.dump(node, annotate_fields=True, include_attributes=False).encode())
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_m13_")
    }


def _collect(path: Path) -> tuple[str, ...]:
    result = subprocess.run(
        [
            os.fspath(REPO_ROOT / ".venv/bin/python"),
            "-m",
            "pytest",
            "-c",
            os.devnull,
            os.fspath(path),
            "--collect-only",
            "-q",
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout)
    return tuple(
        line.split("::", 1)[1] for line in result.stdout.splitlines() if "::test_m13_" in line
    )


def main() -> None:
    baseline = subprocess.check_output(
        ["git", "show", f"{BASELINE}:{TEST_PATH.as_posix()}"],
        cwd=REPO_ROOT,
    )
    current = (REPO_ROOT / TEST_PATH).read_bytes()
    baseline_functions = _functions(baseline)
    current_functions = _functions(current)
    with tempfile.TemporaryDirectory(prefix="m13-v7-frozen-") as temp:
        baseline_path = Path(temp) / TEST_PATH.name
        baseline_path.write_bytes(baseline)
        baseline_cases = _collect(baseline_path)
    current_cases = _collect(REPO_ROOT / TEST_PATH)

    changed = sorted(
        name for name, digest in baseline_functions.items() if current_functions.get(name) != digest
    )
    missing_cases = sorted(set(baseline_cases) - set(current_cases))
    duplicate_cases = sorted(case for case in baseline_cases if current_cases.count(case) != 1)
    new_functions = sorted(set(current_functions) - set(baseline_functions))
    new_cases = tuple(case for case in current_cases if case not in set(baseline_cases))

    print(f"baseline_commit={BASELINE}")
    print(f"baseline_file_sha256={_sha256(baseline)}")
    print(f"current_file_sha256={_sha256(current)}")
    print(f"baseline_test_functions={len(baseline_functions)}")
    print(f"current_test_functions={len(current_functions)}")
    print(f"baseline_collected_cases={len(baseline_cases)}")
    print(f"current_collected_cases={len(current_cases)}")
    print("frozen_function_ast_sha256")
    for name, digest in baseline_functions.items():
        print(f"{name}\t{digest}")
    print("new_v7_test_functions")
    for name in new_functions:
        print(name)
    print("new_v7_collected_cases")
    for case in new_cases:
        print(case)

    assert _sha256(baseline) == EXPECTED_HASH
    assert len(baseline_functions) == 24
    assert len(baseline_cases) == 131
    assert not changed, changed
    assert not missing_cases, missing_cases
    assert not duplicate_cases, duplicate_cases
    assert len(new_functions) == 2
    assert len(new_cases) == 21
    print("result=PASS")


if __name__ == "__main__":
    main()
