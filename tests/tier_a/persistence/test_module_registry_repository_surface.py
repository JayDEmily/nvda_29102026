from __future__ import annotations

import pytest

from nvda_desk.repositories.module_registry import ModuleRegistryRepository


def test_module_registry_repository_rejects_empty_and_duplicate_module_ids() -> None:
    repository = ModuleRegistryRepository()

    with pytest.raises(ValueError, match="module_id"):
        repository.write_record("", {"status": "candidate"})

    repository.write_record("module-001", {"status": "candidate"})

    with pytest.raises(ValueError, match="duplicate module_id"):
        repository.write_record("module-001", {"status": "promoted"})


def test_module_registry_repository_readback_is_copy_safe() -> None:
    repository = ModuleRegistryRepository()
    repository.write_record(
        "module-001",
        {
            "status": "candidate",
            "evidence": {"source_ids": ["intent-001"]},
        },
    )

    first_read = repository.read_record("module-001")
    assert first_read == {
        "status": "candidate",
        "evidence": {"source_ids": ["intent-001"]},
    }
    assert first_read is not None
    first_read["evidence"]["source_ids"].append("caller-mutation")

    assert repository.read_record("module-001") == {
        "status": "candidate",
        "evidence": {"source_ids": ["intent-001"]},
    }


def test_module_registry_repository_does_not_expose_promotion_service_writers() -> None:
    repository = ModuleRegistryRepository()

    for attr_name in ("record_decision", "list_decisions", "promote", "promotion_service"):
        assert not hasattr(repository, attr_name)
