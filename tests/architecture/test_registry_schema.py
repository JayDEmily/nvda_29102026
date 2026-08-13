import json
from pathlib import Path

import pytest

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import (
    SchemaValidationError,
    validate_document,
    validate_instance,
)

ROOT = Path(__file__).resolve().parents[2]


def test_all_architecture_registries_conform_to_committed_schemas() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    assert [item.id for item in registry.objects] == ["P01", "G01", "G02", "A00", "K01"]


def test_vocabulary_registry_conforms_to_schema() -> None:
    validate_document(
        ROOT / "config/vocabulary/vocabulary.yaml",
        ROOT / "schemas/vocabulary.schema.json",
    )


def _module_schema() -> dict[str, object]:
    return json.loads((ROOT / "schemas/module.schema.json").read_text(encoding="utf-8"))


def test_module_template_starts_as_placeholder() -> None:
    template = (ROOT / "templates/module/registry-entry.yaml.template").read_text(
        encoding="utf-8"
    )
    assert "  status: placeholder\n" in template
    assert "  status: active\n" not in template


def test_incomplete_placeholder_module_is_accepted_by_schema() -> None:
    document = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M00",
                "name": "candidate",
                "status": "placeholder",
                "description": "candidate module",
            }
        ],
        "retired_ids": [],
    }

    validate_instance(document, _module_schema())


def test_incomplete_active_module_is_rejected_by_schema() -> None:
    document = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M00",
                "name": "candidate",
                "status": "active",
                "description": "candidate module",
            }
        ],
        "retired_ids": [],
    }

    with pytest.raises(SchemaValidationError, match="missing required properties"):
        validate_instance(document, _module_schema())


def test_complete_active_module_is_accepted_by_schema() -> None:
    document = {
        "schema_version": "1.0",
        "modules": [
            {
                "id": "M00",
                "name": "candidate",
                "status": "active",
                "description": "candidate module",
                "semantic_responsibility": "Own one bounded semantic decision.",
                "inputs": ["source_input"],
                "outputs": ["accepted_output"],
                "permitted_dependencies": [],
                "package": "nvda_desk.candidate",
                "public_seam": "nvda_desk.candidate.api",
                "exclusions": ["Unrelated semantics."],
                "state_ownership": "Owns only candidate-local state.",
                "time_ownership": "Owns only candidate-local time semantics.",
                "side_effects": [],
            }
        ],
        "retired_ids": [],
    }

    validate_instance(document, _module_schema())
