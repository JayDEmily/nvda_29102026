from pathlib import Path

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.architecture.schema import validate_document

ROOT = Path(__file__).resolve().parents[2]


def test_all_architecture_registries_conform_to_committed_schemas() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    assert [item.id for item in registry.objects] == ["P01", "G01", "G02", "A00", "K01"]


def test_vocabulary_registry_conforms_to_schema() -> None:
    validate_document(
        ROOT / "config/vocabulary/vocabulary.yaml",
        ROOT / "schemas/vocabulary.schema.json",
    )
