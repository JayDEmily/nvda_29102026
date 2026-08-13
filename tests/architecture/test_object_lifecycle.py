from pathlib import Path

import pytest

from nvda_desk.architecture.registry import ArchitectureObject, ArchitectureRegistry
from nvda_desk.composition import CompositionPlan

ROOT = Path(__file__).resolve().parents[2]


def test_reset_registry_has_no_active_runtime_module_or_composable_placeholder() -> None:
    registry = ArchitectureRegistry.from_repository(ROOT)
    assert registry.active_runtime_modules() == ()
    assert CompositionPlan.from_registry(registry).object_ids == ()
    for object_id in ("P01", "G01", "G02", "A00", "K01"):
        with pytest.raises(ValueError, match="not composable"):
            registry.require_composable(object_id)


def test_retired_identifier_cannot_be_reused() -> None:
    item = ArchitectureObject("M100", "candidate", "placeholder", "candidate")
    with pytest.raises(ValueError, match="retired identifiers were reused"):
        ArchitectureRegistry((item,), frozenset({"M100"}))


def test_active_executable_object_requires_package_and_public_seam() -> None:
    item = ArchitectureObject("M100", "candidate", "active", "candidate")
    with pytest.raises(ValueError, match="lacks package/public_seam"):
        ArchitectureRegistry((item,), frozenset())
