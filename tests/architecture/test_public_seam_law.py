from pathlib import Path

from nvda_desk.architecture.dependencies import analyse_source_tree
from nvda_desk.architecture.registry import ArchitectureObject, ArchitectureRegistry


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


def _rules() -> dict:
    return {
        "framework_packages": ["nvda_desk.architecture"],
        "category_rules": {
            category: {"may_depend_on": ["M"], "forbidden": []} for category in "MPGAKS"
        },
        "declared_owner_edges": [{"source": "M01", "target": "M02"}],
        "public_seam_exceptions": [],
        "forbid_dynamic_imports_in_runtime_owners": True,
    }


def _analyse(tmp_path: Path, statement: str):
    source = tmp_path / "src"
    path = source / "nvda_desk/m01/impl.py"
    path.parent.mkdir(parents=True)
    path.write_text(statement, encoding="utf-8")
    registry = ArchitectureRegistry(
        (
            _owner("M01", "nvda_desk.m01", ("M02",)),
            _owner("M02", "nvda_desk.m02"),
        ),
        frozenset(),
    )
    return analyse_source_tree(source, registry, _rules())


def test_exact_declared_public_seam_is_accepted(tmp_path: Path) -> None:
    assert _analyse(tmp_path, "from nvda_desk.m02.api import Contract\n") == ()


def test_private_cross_owner_submodule_is_rejected(tmp_path: Path) -> None:
    violations = _analyse(
        tmp_path,
        "from nvda_desk.m02.internal.contracts import Contract\n",
    )
    assert [item.code for item in violations] == ["PRIVATE_SEAM"]


def test_same_owner_internal_import_is_not_a_false_positive(tmp_path: Path) -> None:
    violations = _analyse(tmp_path, "from nvda_desk.m01.internal.helpers import helper\n")
    assert violations == ()
