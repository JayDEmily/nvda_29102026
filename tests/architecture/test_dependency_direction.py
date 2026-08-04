from pathlib import Path

from nvda_desk.architecture.dependencies import analyse_repository, analyse_source_tree
from nvda_desk.architecture.registry import ArchitectureObject, ArchitectureRegistry

ROOT = Path(__file__).resolve().parents[2]


def _rules(edges: list[list[str]]) -> dict:
    return {
        "framework_packages": ["nvda_desk.architecture"],
        "category_rules": {
            "A": {"may_depend_on": ["M", "P", "K"], "forbidden": ["G", "S"]},
            "M": {"may_depend_on": ["M", "P", "K"], "forbidden": ["A", "G", "S"]},
            "P": {"may_depend_on": [], "forbidden": ["A", "M", "G", "K", "S"]},
            "K": {"may_depend_on": [], "forbidden": ["A", "M", "P", "G", "S"]},
            "G": {"may_depend_on": [], "forbidden": ["A", "M", "P", "K", "S"]},
            "S": {"may_depend_on": [], "forbidden": ["A", "M", "P", "G", "K"]},
        },
        "declared_owner_edges": edges,
        "public_seam_exceptions": [],
        "forbid_dynamic_imports_in_runtime_owners": True,
    }


def _registry(*objects: ArchitectureObject) -> ArchitectureRegistry:
    return ArchitectureRegistry(tuple(objects), frozenset())


def _owner(object_id: str, package: str, dependencies: tuple[str, ...] = ()) -> ArchitectureObject:
    return ArchitectureObject(
        object_id,
        package.rsplit(".", 1)[-1],
        "active",
        "fixture",
        package=package,
        public_seam=f"{package}.api",
        permitted_dependencies=dependencies,
    )


def test_committed_dependency_graph_is_acyclic_and_directionally_valid() -> None:
    assert analyse_repository(ROOT) == ()


def test_undeclared_cross_owner_import_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    path = source / "nvda_desk/m01/impl.py"
    path.parent.mkdir(parents=True)
    path.write_text("from nvda_desk.m02.api import Contract\n", encoding="utf-8")
    registry = _registry(_owner("M01", "nvda_desk.m01"), _owner("M02", "nvda_desk.m02"))
    codes = {item.code for item in analyse_source_tree(source, registry, _rules([]))}
    assert "UNDECLARED_EDGE" in codes


def test_declared_module_cycle_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    registry = _registry(
        _owner("M01", "nvda_desk.m01", ("M02",)),
        _owner("M02", "nvda_desk.m02", ("M01",)),
    )
    codes = {
        item.code
        for item in analyse_source_tree(
            source,
            registry,
            _rules([["M01", "M02"], ["M02", "M01"]]),
        )
    }
    assert "MODULE_CYCLE" in codes


def test_dynamic_import_in_runtime_owner_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    path = source / "nvda_desk/m01/impl.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        "import importlib\nvalue = importlib.import_module('nvda_desk.m02.api')\n",
        encoding="utf-8",
    )
    registry = _registry(_owner("M01", "nvda_desk.m01"))
    codes = {item.code for item in analyse_source_tree(source, registry, _rules([]))}
    assert "DYNAMIC_IMPORT" in codes


def test_forbidden_runtime_to_application_shell_direction_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    path = source / "nvda_desk/m01/impl.py"
    path.parent.mkdir(parents=True)
    path.write_text("from nvda_desk.shell.api import start\n", encoding="utf-8")
    registry = _registry(
        _owner("M01", "nvda_desk.m01", ("A00",)),
        _owner("A00", "nvda_desk.shell"),
    )
    codes = {item.code for item in analyse_source_tree(source, registry, _rules([["M01", "A00"]]))}
    assert "FORBIDDEN_DIRECTION" in codes


def test_declared_edge_must_also_be_owned_by_source_registry(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    registry = _registry(
        _owner("M01", "nvda_desk.m01"),
        _owner("M02", "nvda_desk.m02"),
    )
    codes = {item.code for item in analyse_source_tree(source, registry, _rules([["M01", "M02"]]))}
    assert "EDGE_NOT_IN_OWNER_REGISTRY" in codes
