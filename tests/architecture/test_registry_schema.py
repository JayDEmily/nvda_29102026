import json
from pathlib import Path

import pytest

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import (
    SchemaValidationError,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[2]


def test_all_architecture_registries_conform_to_committed_schemas() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    assert [item.id for item in registry.objects] == ["M00", "M01", "P01", "G01", "A00", "K01"]

    module_schema = json.loads((ROOT / "schemas/module.schema.json").read_text(encoding="utf-8"))
    incomplete_active_module = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M01",
                "name": "example",
                "status": "active",
                "description": "intentionally incomplete active module",
            }
        ],
        "retired_ids": [],
    }
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        validate_instance(incomplete_active_module, module_schema)

    complete_active_module = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M01",
                "name": "example",
                "status": "active",
                "description": "schema dependency-category probe",
                "semantic_responsibility": "fixture responsibility",
                "inputs": [],
                "outputs": [],
                "permitted_dependencies": ["M02", "P01", "K01"],
                "package": "nvda_desk.example",
                "public_seam": "nvda_desk.example.api",
                "exclusions": ["no business behaviour"],
                "state_ownership": "none",
                "time_ownership": "none",
                "side_effects": [],
                "component_forms": ["service"],
                "state_writer_boundary": "none",
                "state_reader_boundaries": [],
                "persistence_mechanisms": [],
                "prohibited_state_writers": [],
                "replay_obligations": [],
            }
        ],
        "retired_ids": [],
    }
    validate_instance(complete_active_module, module_schema)
    complete_active_module["modules"][0]["permitted_dependencies"] = ["A00"]
    with pytest.raises(SchemaValidationError, match="does not match"):
        validate_instance(complete_active_module, module_schema)

    kernel_schema = json.loads((ROOT / "schemas/kernel.schema.json").read_text(encoding="utf-8"))
    active_kernel = {
        "schema_version": "1.0",
        "kernels": [
            {
                "id": "K02",
                "name": "example_kernel",
                "status": "active",
                "description": "active technical-kernel representation probe",
                "package": "nvda_desk.example_kernel",
                "public_seam": "nvda_desk.example_kernel.api",
            }
        ],
        "retired_ids": [],
    }
    validate_instance(active_kernel, kernel_schema)
    del active_kernel["kernels"][0]["public_seam"]
    with pytest.raises(SchemaValidationError, match="missing required properties"):
        validate_instance(active_kernel, kernel_schema)

    protocol_schema = json.loads(
        (ROOT / "schemas/protocol.schema.json").read_text(encoding="utf-8")
    )
    active_protocol = {
        "schema_version": "1.0",
        "protocols": [
            {
                "id": "P02",
                "name": "example_protocol",
                "status": "active",
                "description": "protocol with an optional Python-visible seam",
                "package": "nvda_desk.example_protocol",
                "public_seam": "nvda_desk.example_protocol.api",
            }
        ],
        "retired_ids": [],
    }
    validate_instance(active_protocol, protocol_schema)
    del active_protocol["protocols"][0]["package"]
    del active_protocol["protocols"][0]["public_seam"]
    validate_instance(active_protocol, protocol_schema)
