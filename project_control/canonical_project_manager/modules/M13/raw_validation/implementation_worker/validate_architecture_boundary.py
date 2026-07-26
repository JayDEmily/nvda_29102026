"""Mechanically validate the bounded M13 source and import boundary."""

from __future__ import annotations

import ast
import subprocess
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
SOURCE_ROOT = REPO_ROOT / "src/nvda_desk"
M13_ROOT = SOURCE_ROOT / "m13_state_kernel"
SOURCE_CHECKPOINT = "e8384ada435097d64f46f5fe01d55e8d833bf1f4"

PROHIBITED_IMPORT_FRAGMENTS = {
    "tests",
    "raw_validation",
    "reference_conforming",
    "mutant",
}


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            imports.append(prefix + (node.module or ""))
    return imports


def _package_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for path in SOURCE_ROOT.rglob("*.py"):
        relative = path.relative_to(SOURCE_ROOT)
        owner = relative.parts[0] if len(relative.parts) > 1 else "__root__"
        graph.setdefault(owner, set())
        for imported in _imports(path):
            if imported.startswith("nvda_desk."):
                dependency = imported.split(".", 2)[1]
                if dependency != owner:
                    graph[owner].add(dependency)
    return graph


def _cycles(graph: dict[str, set[str]]) -> set[tuple[str, ...]]:
    found: set[tuple[str, ...]] = set()

    def visit(node: str, path: tuple[str, ...]) -> None:
        if node in path:
            cycle = path[path.index(node) :] + (node,)
            rotations = [
                cycle[index:-1] + cycle[:index] + (cycle[index],) for index in range(len(cycle) - 1)
            ]
            found.add(min(rotations))
            return
        for dependency in graph.get(node, set()):
            visit(dependency, path + (node,))

    for package in graph:
        visit(package, ())
    return found


def main() -> None:
    m13_files = sorted(M13_ROOT.glob("*.py"))
    assert {path.name for path in m13_files} == {
        "__init__.py",
        "contracts.py",
        "in_memory.py",
        "ports.py",
    }

    import_inventory: list[tuple[str, str]] = []
    for path in m13_files:
        for imported in _imports(path):
            import_inventory.append((path.name, imported))
            lowered = imported.casefold()
            assert not any(fragment in lowered for fragment in PROHIBITED_IMPORT_FRAGMENTS)
            if imported.startswith("nvda_desk."):
                assert imported.startswith("nvda_desk.m13_state_kernel")

    changed_source = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            SOURCE_CHECKPOINT,
            "--",
            "src",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    untracked_source = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "src"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.splitlines()
    source_changes = sorted(set(changed_source + untracked_source))
    assert source_changes
    assert all(path.startswith("src/nvda_desk/m13_state_kernel/") for path in source_changes)

    graph = _package_graph()
    cycles = _cycles(graph)
    assert graph["m13_state_kernel"] == set()
    assert not any("m13_state_kernel" in cycle for cycle in cycles)

    print("m13_source_files")
    for path in m13_files:
        print(f"  {path.relative_to(REPO_ROOT)}")
    print("m13_import_inventory")
    for filename, imported in import_inventory:
        print(f"  {filename}: {imported}")
    print("changed_src_paths")
    for path in source_changes:
        print(f"  {path}")
    print(f"top_level_package_cycles_without_m13={len(cycles)}")
    print("m13_outgoing_top_level_dependencies=0")
    print("m13_cycle_membership=0")
    print("architecture_boundary=PASS")


if __name__ == "__main__":
    main()
