"""Verify that every pre-V6 M13 test function and parameter ID is preserved."""

from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
TEST_PATH = Path("tests/tier_a/persistence/test_m13_state_kernel_contract.py")
BASELINE = "92c30ef0f1894e8265242b8a0f229daea7ebb603"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_at_baseline() -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE}:{TEST_PATH.as_posix()}"],
        cwd=REPO_ROOT,
    )


def _test_functions(source: bytes) -> dict[str, str]:
    tree = ast.parse(source)
    return {
        node.name: _sha256(ast.dump(node, annotate_fields=True, include_attributes=False).encode())
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_m13_")
    }


def _parameter_ids(source: bytes) -> tuple[str, ...]:
    tree = ast.parse(source)
    ids: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "param"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "pytest"
        ):
            continue
        for keyword in node.keywords:
            if keyword.arg == "id" and isinstance(keyword.value, ast.Constant):
                ids.append(str(keyword.value.value))
    return tuple(ids)


def main() -> None:
    baseline_source = _source_at_baseline()
    current_source = (REPO_ROOT / TEST_PATH).read_bytes()
    baseline_functions = _test_functions(baseline_source)
    current_functions = _test_functions(current_source)
    baseline_ids = _parameter_ids(baseline_source)
    current_ids = _parameter_ids(current_source)

    missing_functions = sorted(set(baseline_functions) - set(current_functions))
    changed_functions = sorted(
        name for name, digest in baseline_functions.items() if current_functions.get(name) != digest
    )
    missing_ids = sorted(set(baseline_ids) - set(current_ids))
    duplicate_baseline_ids = sorted(
        item for item in set(baseline_ids) if current_ids.count(item) != 1
    )
    new_functions = sorted(set(current_functions) - set(baseline_functions))
    new_ids = tuple(item for item in current_ids if item not in set(baseline_ids))

    print(f"baseline_commit={BASELINE}")
    print(f"baseline_file_sha256={_sha256(baseline_source)}")
    print(f"current_file_sha256={_sha256(current_source)}")
    print(f"baseline_test_function_count={len(baseline_functions)}")
    print(f"current_test_function_count={len(current_functions)}")
    print(f"baseline_parameter_id_count={len(baseline_ids)}")
    print(f"current_parameter_id_count={len(current_ids)}")
    print(f"baseline_semantic_case_count={len(baseline_functions) - 1 + len(baseline_ids)}")
    print("baseline_function_ast_sha256")
    for name, digest in baseline_functions.items():
        print(f"{name}\t{digest}")
    print("baseline_parameter_ids")
    for item in baseline_ids:
        print(item)
    print("new_v6_test_functions")
    for name in new_functions:
        print(name)
    print("new_v6_parameter_ids")
    for item in new_ids:
        print(item)

    assert not missing_functions, missing_functions
    assert not changed_functions, changed_functions
    assert not missing_ids, missing_ids
    assert not duplicate_baseline_ids, duplicate_baseline_ids
    assert len(baseline_functions) == 15
    assert len(baseline_ids) == 32
    assert len(baseline_functions) - 1 + len(baseline_ids) == 46
    print("result=PASS")


if __name__ == "__main__":
    main()
