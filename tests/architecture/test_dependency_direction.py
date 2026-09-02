import json
import shutil
from pathlib import Path

import pytest
import yaml

from nvda_desk.architecture.dependencies import analyse_repository, analyse_source_tree
from nvda_desk.architecture.registry import ArchitectureObject, ArchitectureRegistry
from nvda_desk.architecture.schema import SchemaValidationError, validate_instance

ROOT = Path(__file__).resolve().parents[2]


def _rules(edges: list[dict[str, str]]) -> dict:
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


def test_committed_dependency_graph_is_acyclic_and_directionally_valid(tmp_path: Path) -> None:
    assert analyse_repository(ROOT) == ()

    schema = json.loads((ROOT / "schemas/dependency_rules.schema.json").read_text(encoding="utf-8"))
    malformed_rules = yaml.safe_load(
        (ROOT / "config/architecture/dependency_rules.yaml").read_text(encoding="utf-8")
    )
    malformed_rules["public_seam_exceptions"] = [{}]
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        validate_instance(malformed_rules, schema)

    source = tmp_path / "src"
    source.mkdir()
    registry = _registry(
        _owner("M01", "nvda_desk.m01", ("M02",)),
        _owner("M02", "nvda_desk.m02", ("M03",)),
        _owner("M03", "nvda_desk.m03"),
    )
    rules = _rules(
        [
            {"source": "M01", "target": "M02"},
            {"source": "M02", "target": "M03"},
        ]
    )
    assert analyse_source_tree(source, registry, rules) == ()

    repository = tmp_path / "repository"
    shutil.copytree(ROOT / "schemas", repository / "schemas")
    shutil.copytree(ROOT / "config/architecture", repository / "config/architecture")
    runtime_source = repository / "src/nvda_desk/m01/impl.py"
    runtime_source.parent.mkdir(parents=True)
    runtime_source.write_text(
        "from nvda_desk.protocol_contract.api import ProtocolContract\n"
        "from nvda_desk.kernel_contract.api import KernelContract\n",
        encoding="utf-8",
    )

    modules = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M01",
                "name": "integration_probe",
                "status": "active",
                "description": "real-path dependency integration fixture",
                "semantic_responsibility": "prove architecture loading only",
                "inputs": [],
                "outputs": [],
                "permitted_dependencies": ["P02", "K02"],
                "package": "nvda_desk.m01",
                "public_seam": "nvda_desk.m01.api",
                "exclusions": ["no business behaviour"],
                "state_ownership": "none",
                "time_ownership": "none",
                "side_effects": [],
                "predecessors": [],
                "successors": [],
            }
        ],
        "retired_ids": [],
    }
    (repository / "config/architecture/modules.yaml").write_text(
        yaml.safe_dump(modules, sort_keys=False), encoding="utf-8"
    )

    protocols = yaml.safe_load(
        (repository / "config/architecture/protocols.yaml").read_text(encoding="utf-8")
    )
    protocols["protocols"].append(
        {
            "id": "P02",
            "name": "integration_protocol",
            "status": "active",
            "description": "Python-visible protocol integration fixture",
            "package": "nvda_desk.protocol_contract",
            "public_seam": "nvda_desk.protocol_contract.api",
            "predecessors": [],
            "successors": [],
        }
    )
    (repository / "config/architecture/protocols.yaml").write_text(
        yaml.safe_dump(protocols, sort_keys=False), encoding="utf-8"
    )

    kernels = yaml.safe_load(
        (repository / "config/architecture/kernels.yaml").read_text(encoding="utf-8")
    )
    kernels["kernels"].append(
        {
            "id": "K02",
            "name": "integration_kernel",
            "status": "active",
            "description": "executable kernel integration fixture",
            "package": "nvda_desk.kernel_contract",
            "public_seam": "nvda_desk.kernel_contract.api",
            "predecessors": [],
            "successors": [],
        }
    )
    (repository / "config/architecture/kernels.yaml").write_text(
        yaml.safe_dump(kernels, sort_keys=False), encoding="utf-8"
    )

    real_rules = yaml.safe_load(
        (repository / "config/architecture/dependency_rules.yaml").read_text(encoding="utf-8")
    )
    real_rules["declared_owner_edges"] = [
        {"source": "M01", "target": "P02"},
        {"source": "M01", "target": "K02"},
    ]
    (repository / "config/architecture/dependency_rules.yaml").write_text(
        yaml.safe_dump(real_rules, sort_keys=False), encoding="utf-8"
    )

    assert analyse_repository(repository) == ()


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
            _rules([{"source": "M01", "target": "M02"}, {"source": "M02", "target": "M01"}]),
        )
    }
    assert "MODULE_CYCLE" in codes


def test_dynamic_import_in_runtime_owner_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "src"
    path = source / "nvda_desk/m01/impl.py"
    path.parent.mkdir(parents=True)
    registry = _registry(_owner("M01", "nvda_desk.m01"))
    statements = (
        "import importlib\nvalue = importlib.import_module('nvda_desk.m02.api')\n",
        "import importlib as il\nvalue = il.import_module('nvda_desk.m02.api')\n",
        "from importlib import import_module as load\nvalue = load('nvda_desk.m02.api')\n",
        "value = __import__('nvda_desk.m02.api')\n",
        "import builtins as b\nvalue = b.__import__('nvda_desk.m02.api')\n",
        "from builtins import __import__ as load\nvalue = load('nvda_desk.m02.api')\n",
    )
    for statement in statements:
        path.write_text(statement, encoding="utf-8")
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
    codes = {
        item.code
        for item in analyse_source_tree(
            source, registry, _rules([{"source": "M01", "target": "A00"}])
        )
    }
    assert "FORBIDDEN_DIRECTION" in codes


def test_declared_edge_must_also_be_owned_by_source_registry(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    registry = _registry(
        _owner("M01", "nvda_desk.m01"),
        _owner("M02", "nvda_desk.m02"),
    )
    codes = {
        item.code
        for item in analyse_source_tree(
            source, registry, _rules([{"source": "M01", "target": "M02"}])
        )
    }
    assert "EDGE_NOT_IN_OWNER_REGISTRY" in codes
