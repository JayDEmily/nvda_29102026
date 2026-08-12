"""AST-based dependency, cycle, dynamic-import and public-seam validation."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import yaml

from .registry import ArchitectureObject, ArchitectureRegistry
from .schema import validate_document


@dataclass(frozen=True, slots=True)
class ImportEdge:
    source_owner: str
    target_owner: str
    imported_path: str
    source_file: str
    line: int


@dataclass(frozen=True, slots=True)
class ArchitectureViolation:
    code: str
    message: str
    source_file: str | None = None
    line: int | None = None


def _module_name(source_root: Path, path: Path) -> str:
    relative = path.relative_to(source_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _resolve_from(
    module_name: str,
    node: ast.ImportFrom,
    *,
    package_module: bool,
) -> str | None:
    if node.level == 0:
        return node.module
    package_parts = module_name.split(".")
    if not package_module:
        package_parts = package_parts[:-1]
    ascend = node.level - 1
    if ascend > len(package_parts):
        return None
    base = package_parts[: len(package_parts) - ascend]
    if node.module:
        base.extend(node.module.split("."))
    return ".".join(base)


def _owner_for(module: str, owners: Iterable[ArchitectureObject]) -> ArchitectureObject | None:
    matches = [
        owner
        for owner in owners
        if owner.package and (module == owner.package or module.startswith(owner.package + "."))
    ]
    if not matches:
        return None
    return max(matches, key=lambda item: len(item.package or ""))


def _contains_cycle(edges: Iterable[tuple[str, str]]) -> bool:
    graph: dict[str, set[str]] = {}
    for source, target in edges:
        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set())
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(target) for target in graph[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def analyse_repository(repository_root: Path) -> tuple[ArchitectureViolation, ...]:
    registry = ArchitectureRegistry.from_repository(repository_root)
    rules_path = repository_root / "config" / "architecture" / "dependency_rules.yaml"
    validate_document(rules_path, repository_root / "schemas" / "dependency_rules.schema.json")
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    return analyse_source_tree(repository_root / "src", registry, rules)


def analyse_source_tree(
    source_root: Path,
    registry: ArchitectureRegistry,
    rules: dict,
) -> tuple[ArchitectureViolation, ...]:
    owners = registry.package_owners()
    framework_packages = tuple(rules.get("framework_packages", ()))
    declared_edges = {tuple(edge) for edge in rules.get("declared_owner_edges", ())}
    seam_exceptions = {
        (item["source_owner"], item["target_owner"], item["import_path"])
        for item in rules.get("public_seam_exceptions", ())
    }
    violations: list[ArchitectureViolation] = []
    observed_edges: list[ImportEdge] = []

    for path in sorted(source_root.rglob("*.py")):
        module_name = _module_name(source_root, path)
        source_owner = _owner_for(module_name, owners)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            violations.append(ArchitectureViolation("SYNTAX", str(exc), str(path), exc.lineno))
            continue

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and rules.get("forbid_dynamic_imports_in_runtime_owners")
                and source_owner
            ):
                name = None
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    name = f"{node.func.value.id}.{node.func.attr}"
                if name in {"__import__", "importlib.import_module"}:
                    violations.append(
                        ArchitectureViolation(
                            "DYNAMIC_IMPORT",
                            f"{source_owner.id} uses forbidden dynamic import {name}",
                            str(path),
                            node.lineno,
                        )
                    )
            imported: list[str] = []
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                resolved = _resolve_from(
                    module_name,
                    node,
                    package_module=path.name == "__init__.py",
                )
                if resolved:
                    imported = [resolved]
            for imported_path in imported:
                if any(
                    imported_path == framework or imported_path.startswith(framework + ".")
                    for framework in framework_packages
                ):
                    continue
                target_owner = _owner_for(imported_path, owners)
                if (
                    source_owner is None
                    or target_owner is None
                    or source_owner.id == target_owner.id
                ):
                    continue
                edge = ImportEdge(
                    source_owner.id, target_owner.id, imported_path, str(path), node.lineno
                )
                observed_edges.append(edge)
                if (source_owner.id, target_owner.id) not in declared_edges:
                    violations.append(
                        ArchitectureViolation(
                            "UNDECLARED_EDGE",
                            f"{source_owner.id} imports {target_owner.id} "
                            "without a declared owner edge",
                            str(path),
                            node.lineno,
                        )
                    )
                source_rule = rules["category_rules"][source_owner.category]
                if target_owner.category not in source_rule["may_depend_on"]:
                    violations.append(
                        ArchitectureViolation(
                            "FORBIDDEN_DIRECTION",
                            f"{source_owner.category} may not depend on {target_owner.category}",
                            str(path),
                            node.lineno,
                        )
                    )
                exception = (source_owner.id, target_owner.id, imported_path) in seam_exceptions
                if not exception and imported_path != target_owner.public_seam:
                    violations.append(
                        ArchitectureViolation(
                            "PRIVATE_SEAM",
                            f"{source_owner.id} imports {imported_path}; "
                            f"required seam is {target_owner.public_seam}",
                            str(path),
                            node.lineno,
                        )
                    )

    module_edges = [
        (source, target)
        for source, target in declared_edges
        if registry.get(source).category == "M" and registry.get(target).category == "M"
    ]
    if _contains_cycle(module_edges):
        violations.append(
            ArchitectureViolation("MODULE_CYCLE", "declared runtime-module graph is cyclic")
        )

    # A declared edge is authority, but it must correspond to a current permitted dependency.
    for source, target in sorted(declared_edges):
        source_object = registry.get(source)
        target_object = registry.get(target)
        if target not in source_object.permitted_dependencies:
            violations.append(
                ArchitectureViolation(
                    "EDGE_NOT_IN_OWNER_REGISTRY",
                    f"declared edge {source}->{target} is absent from "
                    f"{source}'s permitted_dependencies",
                )
            )
        if target_object.status == "retired":
            violations.append(
                ArchitectureViolation(
                    "EDGE_TO_RETIRED", f"declared edge {source}->{target} targets a retired object"
                )
            )
    return tuple(violations)
