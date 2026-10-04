import shutil
from pathlib import Path

import pytest
import yaml

from nvda_desk.architecture.dependencies import analyse_repository
from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import SchemaValidationError
from nvda_desk.architecture.validation import ArchitectureValidationError, validate_architecture

ROOT = Path(__file__).resolve().parents[2]


def _copy_repository_surface(tmp_path: Path, name: str, *, full: bool = False) -> Path:
    repository = tmp_path / name
    source_names = ("config", "schemas", "src", "docs", "tests") if full else (
        "config",
        "schemas",
        "src",
    )
    for source_name in source_names:
        shutil.copytree(ROOT / source_name, repository / source_name)
    return repository


def _active_module(
    object_id: str,
    package_name: str,
    *,
    dependencies: list[str] | None = None,
) -> dict:
    return {
        "id": object_id,
        "name": package_name,
        "status": "active",
        "description": "behaviour-neutral structural readiness fixture",
        "semantic_responsibility": "fixture-only architecture ownership",
        "inputs": [],
        "outputs": [],
        "permitted_dependencies": dependencies or [],
        "package": f"nvda_desk.{package_name}",
        "public_seam": f"nvda_desk.{package_name}.api",
        "exclusions": ["no product or domain behaviour"],
        "state_ownership": "none",
        "time_ownership": "none",
        "side_effects": [],
        "component_forms": ["service"],
        "state_writer_boundary": "none",
        "state_reader_boundaries": [],
        "persistence_mechanisms": [],
        "prohibited_state_writers": [],
        "replay_obligations": [],
        "predecessors": [],
        "successors": [],
    }


def _write_modules(repository: Path, modules: list[dict]) -> None:
    path = repository / "config/architecture/modules.yaml"
    path.write_text(
        yaml.safe_dump(
            {"schema_version": "1.0", "modules": modules, "retired_ids": []},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    shells_path = repository / "config/architecture/application_shells.yaml"
    shells = yaml.safe_load(shells_path.read_text(encoding="utf-8"))
    shells["application_shells"][0]["permitted_dependencies"] = []
    shells_path.write_text(yaml.safe_dump(shells, sort_keys=False), encoding="utf-8")
    _write_edges(repository, [])


def _write_edges(repository: Path, edges: list[dict[str, str]]) -> None:
    path = repository / "config/architecture/dependency_rules.yaml"
    rules = yaml.safe_load(path.read_text(encoding="utf-8"))
    rules["declared_owner_edges"] = edges
    path.write_text(yaml.safe_dump(rules, sort_keys=False), encoding="utf-8")


def _write_source(repository: Path, package_name: str, body: str) -> None:
    path = repository / f"src/nvda_desk/{package_name}/impl.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_aggregate_validator_accepts_first_lawful_active_module(tmp_path: Path) -> None:
    repository = _copy_repository_surface(tmp_path, "first-module", full=True)
    _write_modules(repository, [_active_module("M01", "example_module")])
    api = repository / "src/nvda_desk/example_module/api.py"
    api.parent.mkdir(parents=True, exist_ok=True)
    (api.parent / "__init__.py").write_text("", encoding="utf-8")
    api.write_text('"""Fixture public seam."""\n', encoding="utf-8")

    result = validate_architecture(repository)

    assert "active runtime modules: 1" in result


def test_aggregate_validator_rejects_active_owner_without_declared_implementation(
    tmp_path: Path,
) -> None:
    repository = _copy_repository_surface(tmp_path, "missing-implementation", full=True)
    _write_modules(repository, [_active_module("M01", "missing_module")])

    with pytest.raises(ArchitectureValidationError, match="registered package does not exist"):
        validate_architecture(repository)


def test_aggregate_validator_accepts_lawful_protocol_and_kernel_activation(
    tmp_path: Path,
) -> None:
    repository = _copy_repository_surface(tmp_path, "p-k-activation", full=True)

    protocols_path = repository / "config/architecture/protocols.yaml"
    protocols = yaml.safe_load(protocols_path.read_text(encoding="utf-8"))
    protocols["protocols"].extend(
        [
            {
                "id": "P02",
                "name": "declarative_protocol",
                "status": "active",
                "description": "declarative protocol without runtime package",
                "predecessors": [],
                "successors": [],
            },
            {
                "id": "P03",
                "name": "python_protocol",
                "status": "active",
                "description": "Python-visible protocol fixture",
                "package": "nvda_desk.python_protocol",
                "public_seam": "nvda_desk.python_protocol.api",
                "predecessors": [],
                "successors": [],
            },
        ]
    )
    protocols_path.write_text(yaml.safe_dump(protocols, sort_keys=False), encoding="utf-8")

    kernels_path = repository / "config/architecture/kernels.yaml"
    kernels = yaml.safe_load(kernels_path.read_text(encoding="utf-8"))
    kernels["kernels"].append(
        {
            "id": "K02",
            "name": "technical_kernel",
            "status": "active",
            "description": "Python-visible technical kernel fixture",
            "package": "nvda_desk.technical_kernel",
            "public_seam": "nvda_desk.technical_kernel.api",
            "predecessors": [],
            "successors": [],
        }
    )
    kernels_path.write_text(yaml.safe_dump(kernels, sort_keys=False), encoding="utf-8")

    for package_name in ("python_protocol", "technical_kernel"):
        package = repository / f"src/nvda_desk/{package_name}"
        package.mkdir(parents=True, exist_ok=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        (package / "api.py").write_text('"""Fixture public seam."""\n', encoding="utf-8")

    result = validate_architecture(repository)

    assert "architecture objects: 9" in result
    assert "active runtime modules: 1" in result


def test_real_config_accepts_declared_m_to_m_and_rejects_undeclared_edge(tmp_path: Path) -> None:
    valid = _copy_repository_surface(tmp_path, "valid-m-to-m")
    modules = [
        _active_module("M01", "m01", dependencies=["M02"]),
        _active_module("M02", "m02"),
    ]
    _write_modules(valid, modules)
    _write_edges(valid, [{"source": "M01", "target": "M02"}])
    _write_source(valid, "m01", "from nvda_desk.m02.api import Contract\n")
    assert analyse_repository(valid) == ()

    invalid = _copy_repository_surface(tmp_path, "undeclared-m-to-m")
    _write_modules(invalid, modules)
    _write_edges(invalid, [])
    _write_source(invalid, "m01", "from nvda_desk.m02.api import Contract\n")
    codes = {item.code for item in analyse_repository(invalid)}
    assert "UNDECLARED_EDGE" in codes


def test_real_config_rejects_forbidden_reverse_dependency(tmp_path: Path) -> None:
    repository = _copy_repository_surface(tmp_path, "forbidden-reverse")
    _write_modules(repository, [_active_module("M01", "m01")])
    protocols_path = repository / "config/architecture/protocols.yaml"
    protocols = yaml.safe_load(protocols_path.read_text(encoding="utf-8"))
    protocols["protocols"].append(
        {
            "id": "P02",
            "name": "protocol_probe",
            "status": "active",
            "description": "Python-visible protocol fixture",
            "package": "nvda_desk.protocol_probe",
            "public_seam": "nvda_desk.protocol_probe.api",
            "predecessors": [],
            "successors": [],
        }
    )
    protocols_path.write_text(yaml.safe_dump(protocols, sort_keys=False), encoding="utf-8")
    _write_edges(repository, [{"source": "P02", "target": "M01"}])
    _write_source(repository, "protocol_probe", "from nvda_desk.m01.api import Contract\n")
    codes = {item.code for item in analyse_repository(repository)}
    assert "FORBIDDEN_DIRECTION" in codes


def test_real_config_rejects_module_cycle(tmp_path: Path) -> None:
    repository = _copy_repository_surface(tmp_path, "module-cycle")
    _write_modules(
        repository,
        [
            _active_module("M01", "m01", dependencies=["M02"]),
            _active_module("M02", "m02", dependencies=["M01"]),
        ],
    )
    _write_edges(
        repository,
        [{"source": "M01", "target": "M02"}, {"source": "M02", "target": "M01"}],
    )
    codes = {item.code for item in analyse_repository(repository)}
    assert "MODULE_CYCLE" in codes


@pytest.mark.parametrize(
    "statement",
    [
        "from nvda_desk.m02.internal import Contract\n",
        "from nvda_desk import m02\n",
    ],
)
def test_real_config_rejects_private_and_importfrom_seam_bypass(
    tmp_path: Path, statement: str
) -> None:
    repository = _copy_repository_surface(tmp_path, "private-seam")
    _write_modules(
        repository,
        [
            _active_module("M01", "m01", dependencies=["M02"]),
            _active_module("M02", "m02"),
        ],
    )
    _write_edges(repository, [{"source": "M01", "target": "M02"}])
    _write_source(repository, "m01", statement)
    codes = {item.code for item in analyse_repository(repository)}
    assert "PRIVATE_SEAM" in codes


def test_real_config_rejects_named_dynamic_import_bypass(tmp_path: Path) -> None:
    repository = _copy_repository_surface(tmp_path, "dynamic-import")
    _write_modules(repository, [_active_module("M01", "m01")])
    _write_source(
        repository,
        "m01",
        "import importlib as loader\nvalue = loader.import_module('nvda_desk.anything')\n",
    )
    codes = {item.code for item in analyse_repository(repository)}
    assert "DYNAMIC_IMPORT" in codes


def test_registry_loader_rejects_incomplete_ownership_and_invalid_p_k_activation(
    tmp_path: Path,
) -> None:
    required_projection_fields = (
        "semantic_responsibility",
        "state_ownership",
        "component_forms",
        "state_writer_boundary",
        "state_reader_boundaries",
        "persistence_mechanisms",
        "prohibited_state_writers",
        "replay_obligations",
    )
    for field in required_projection_fields:
        incomplete = _copy_repository_surface(tmp_path, f"incomplete-owner-{field}")
        module = _active_module("M01", "m01")
        del module[field]
        _write_modules(incomplete, [module])
        with pytest.raises(SchemaValidationError, match="missing required properties"):
            ArchitectureRegistry.from_repository(incomplete)

    invalid_form = _copy_repository_surface(tmp_path, "invalid-component-form")
    module = _active_module("M01", "m01")
    module["component_forms"] = ["service_locator"]
    _write_modules(invalid_form, [module])
    with pytest.raises(SchemaValidationError, match="is not in"):
        ArchitectureRegistry.from_repository(invalid_form)

    invalid_protocol = _copy_repository_surface(tmp_path, "invalid-protocol")
    protocols_path = invalid_protocol / "config/architecture/protocols.yaml"
    protocols = yaml.safe_load(protocols_path.read_text(encoding="utf-8"))
    protocols["protocols"].append(
        {
            "id": "P02",
            "name": "invalid_protocol",
            "status": "active",
            "description": "package without public seam",
            "package": "nvda_desk.invalid_protocol",
            "predecessors": [],
            "successors": [],
        }
    )
    protocols_path.write_text(yaml.safe_dump(protocols, sort_keys=False), encoding="utf-8")
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        ArchitectureRegistry.from_repository(invalid_protocol)

    invalid_kernel = _copy_repository_surface(tmp_path, "invalid-kernel")
    kernels_path = invalid_kernel / "config/architecture/kernels.yaml"
    kernels = yaml.safe_load(kernels_path.read_text(encoding="utf-8"))
    kernels["kernels"].append(
        {
            "id": "K02",
            "name": "invalid_kernel",
            "status": "active",
            "description": "active kernel without Python-visible seam",
            "package": "nvda_desk.invalid_kernel",
            "predecessors": [],
            "successors": [],
        }
    )
    kernels_path.write_text(yaml.safe_dump(kernels, sort_keys=False), encoding="utf-8")
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        ArchitectureRegistry.from_repository(invalid_kernel)


def test_dependency_loader_rejects_malformed_public_seam_exception(tmp_path: Path) -> None:
    repository = _copy_repository_surface(tmp_path, "bad-exception")
    rules_path = repository / "config/architecture/dependency_rules.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    rules["public_seam_exceptions"] = [{"source_owner": "M01"}]
    rules_path.write_text(yaml.safe_dump(rules, sort_keys=False), encoding="utf-8")
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        analyse_repository(repository)


def test_current_foundation_objects_do_not_carry_pre_reset_lineage_aliases() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    for object_id in ("A00", "P01", "K01", "G01"):
        assert registry.get(object_id).predecessors == ()
        assert registry.get(object_id).successors == ()
