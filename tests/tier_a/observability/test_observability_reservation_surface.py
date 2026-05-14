from __future__ import annotations

import ast
from pathlib import Path


def _python_files(*roots: str) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        files.extend(sorted(Path(root).rglob("*.py")))
    return files


def _imports_package(path: Path, package_name: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == package_name or alias.name.startswith(f"{package_name}."):
                    return True
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == package_name or node.module.startswith(f"{package_name}."):
                return True
    return False


def test_observability_package_home_remains_absent() -> None:
    observability_path = Path("src/nvda_desk/observability")

    assert observability_path.parts[-2:] == ("nvda_desk", "observability")
    assert observability_path.exists() is False


def test_observability_package_is_not_imported_by_native_runtime_or_native_tier_a_b_tests() -> None:
    scoped_files = _python_files("src/nvda_desk", "tests/tier_a", "tests/tier_b")
    observability_importers = [
        str(path) for path in scoped_files if _imports_package(path, "nvda_desk.observability")
    ]
    assert observability_importers == []
