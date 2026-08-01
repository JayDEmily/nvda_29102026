from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEGACY_IMPORT_PREFIXES = ("legacy_import", "nvda_desk.legacy.imported")
TRANSFORM_BOUNDARY_GUARD_FILES = (
    Path("tests/tier_a/downstream_runtime/test_exit_close_transform_boundary_surface.py"),
    Path("tests/tier_a/downstream_runtime/test_live_inventory_transform_boundary_surface.py"),
    Path("tests/tier_a/financial_calendar/test_financial_calendar_transform_boundary_surface.py"),
    Path("tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py"),
    Path("tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py"),
    Path("tests/tier_a/review_runtime/test_review_transform_boundary_surface.py"),
    Path("tests/tier_a/serial_recommendation/test_serial_transform_boundary_surface.py"),
    Path("tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py"),
    Path("tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py"),
)


def _native_python_paths() -> list[Path]:
    candidates = []
    for relative_root in ("src", "tests/tier_a", "tests/tier_b"):
        root = REPO_ROOT / relative_root
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if path == Path(__file__).resolve():
                continue
            candidates.append(path)
    return sorted(candidates)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _legacy_imports(path: Path) -> set[str]:
    return {
        module
        for module in _imported_modules(path)
        if any(
            module == prefix or module.startswith(f"{prefix}.") for prefix in LEGACY_IMPORT_PREFIXES
        )
    }


def _legacy_dynamic_import_targets(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    targets: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        is_dynamic_import = (
            isinstance(func, ast.Name)
            and func.id == "__import__"
            or isinstance(func, ast.Attribute)
            and func.attr == "import_module"
            and isinstance(func.value, ast.Name)
            and func.value.id == "importlib"
        )
        if not is_dynamic_import:
            continue
        first_arg = node.args[0]
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            module = first_arg.value
            if any(
                module == prefix or module.startswith(f"{prefix}.")
                for prefix in LEGACY_IMPORT_PREFIXES
            ):
                targets.add(module)
    return targets


def test_imported_module_subsystem_remains_outside_native_runtime_and_native_proof() -> None:
    assert not (REPO_ROOT / "src/nvda_desk/legacy/imported").exists()

    offending_imports: dict[str, list[str]] = {}
    for path in _native_python_paths():
        legacy_imports = _legacy_imports(path)
        if legacy_imports:
            offending_imports[path.relative_to(REPO_ROOT).as_posix()] = sorted(legacy_imports)

    assert offending_imports == {}


def test_transform_boundary_guard_strings_are_not_imported_legacy_modules() -> None:
    """Transform-boundary tests may name donor roots while proving non-imports."""

    for relative_path in TRANSFORM_BOUNDARY_GUARD_FILES:
        path = REPO_ROOT / relative_path
        assert "legacy_import" in path.read_text(encoding="utf-8")
        assert _legacy_imports(path) == set()


def test_imported_module_archive_tree_is_explicitly_quarantined() -> None:
    readme_path = REPO_ROOT / "legacy_import/README.md"
    readme_text = readme_path.read_text(encoding="utf-8")
    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "historical source evidence only" in readme_text
    assert (
        "There is currently **no** admitted native package at `src/nvda_desk/legacy/imported/`."
        in readme_text
    )
    assert (
        "Native runtime and native Tier A / Tier B proof must not import from this tree."
        in readme_text
    )
    assert 'packages = ["src/nvda_desk", "scripts"]' in pyproject_text
    assert "/tests" in pyproject_text
    assert "legacy_import" not in pyproject_text


def test_native_runtime_and_proof_do_not_dynamic_import_legacy_subsystem() -> None:
    offending_dynamic_imports: dict[str, list[str]] = {}
    for path in _native_python_paths():
        targets = _legacy_dynamic_import_targets(path)
        if targets:
            offending_dynamic_imports[path.relative_to(REPO_ROOT).as_posix()] = sorted(targets)

    assert offending_dynamic_imports == {}
