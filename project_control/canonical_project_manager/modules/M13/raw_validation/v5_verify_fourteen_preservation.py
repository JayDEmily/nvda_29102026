from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path


SOURCE_COMMIT = "479000b512ef74b8134bc11cefc7a3ef13fac0e1"
TEST_PATH = Path("tests/tier_a/persistence/test_m13_state_kernel_contract.py")


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _test_functions(content: bytes) -> dict[str, str]:
    tree = ast.parse(content.decode("utf-8"))
    functions: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            functions[node.name] = ast.dump(node, annotate_fields=True, include_attributes=False)
    return functions


def main() -> int:
    prior = subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{TEST_PATH.as_posix()}"]
    )
    current = TEST_PATH.read_bytes()
    prior_functions = _test_functions(prior)
    current_functions = _test_functions(current)
    frozen_names = tuple(prior_functions)
    added_names = tuple(name for name in current_functions if name not in prior_functions)
    removed_names = tuple(name for name in prior_functions if name not in current_functions)
    changed_names = tuple(
        name
        for name in frozen_names
        if name in current_functions and prior_functions[name] != current_functions[name]
    )

    print(f"source_commit={SOURCE_COMMIT}")
    print(f"prior_whole_file_sha256={_sha256(prior)}")
    print(f"current_whole_file_sha256={_sha256(current)}")
    print(f"frozen_function_count={len(frozen_names)}")
    print(f"current_function_count={len(current_functions)}")
    print(f"semantic_test_count={len(current_functions) - 1 + 32}")
    print(f"frozen_function_names={','.join(frozen_names)}")
    print(f"added_function_names={','.join(added_names)}")
    print(f"removed_function_names={','.join(removed_names)}")
    print(f"changed_function_names={','.join(changed_names)}")
    for name in frozen_names:
        prior_hash = _sha256(prior_functions[name].encode("utf-8"))
        current_hash = _sha256(current_functions.get(name, "").encode("utf-8"))
        status = "PASS" if prior_hash == current_hash else "FAIL"
        print(
            f"function={name}\tprior_ast_sha256={prior_hash}"
            f"\tcurrent_ast_sha256={current_hash}\tstatus={status}"
        )
    passed = (
        len(frozen_names) == 14
        and len(current_functions) == 15
        and not removed_names
        and not changed_names
        and added_names == ("test_m13_unsuccessful_execute_attempt_leaves_no_binding_matrix",)
    )
    print(f"fourteen_test_functions_unchanged={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
