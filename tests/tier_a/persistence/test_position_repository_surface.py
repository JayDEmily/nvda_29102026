from __future__ import annotations

import pytest

from nvda_desk.repositories.position_repository import PositionRepository


def test_position_repository_rejects_duplicate_ids_and_preserves_copy_boundary() -> None:
    repository = PositionRepository()
    source = {"symbol": "NVDA", "quantity": 1, "metadata": {"source": "seed"}}

    repository.write_position("pos-1", source)
    source["metadata"]["source"] = "mutated"
    readback = repository.read_position("pos-1")
    assert readback == {"symbol": "NVDA", "quantity": 1, "metadata": {"source": "seed"}}
    assert readback is not None
    readback["metadata"]["source"] = "readback-mutated"

    assert repository.read_position("pos-1") == {
        "symbol": "NVDA",
        "quantity": 1,
        "metadata": {"source": "seed"},
    }
    with pytest.raises(ValueError, match="duplicate position_id"):
        repository.write_position("pos-1", {"symbol": "NVDA", "quantity": 2})


def test_position_repository_lists_snapshots_in_insertion_order() -> None:
    repository = PositionRepository()

    repository.write_position("pos-1", {"quantity": 1})
    repository.write_position("pos-2", {"quantity": 2})

    listed = repository.list_positions()
    listed[0]["quantity"] = 99
    assert repository.list_positions() == [{"quantity": 1}, {"quantity": 2}]


def test_position_repository_reads_and_lists_identifier_records_copy_safely() -> None:
    repository = PositionRepository()
    repository.write_position("pos-1", {"symbol": "NVDA", "metadata": {"source": "fill"}})

    record = repository.read_position_record("pos-1")
    assert record == {
        "position_id": "pos-1",
        "position": {"symbol": "NVDA", "metadata": {"source": "fill"}},
    }
    assert record is not None
    record["position"]["metadata"]["source"] = "mutated"

    assert repository.list_position_records() == [
        {
            "position_id": "pos-1",
            "position": {"symbol": "NVDA", "metadata": {"source": "fill"}},
        }
    ]


def test_position_repository_rejects_empty_id_and_duplicate_after_normalisation() -> None:
    repository = PositionRepository()

    with pytest.raises(ValueError, match="position_id must be non-empty"):
        repository.write_position("  ", {"symbol": "NVDA"})

    repository.write_position("pos-1", {"symbol": "NVDA", "quantity": 1})
    with pytest.raises(ValueError, match="duplicate position_id: pos-1"):
        repository.write_position(" pos-1 ", {"symbol": "NVDA", "quantity": 2})

    assert repository.read_position(" pos-1 ") == {"symbol": "NVDA", "quantity": 1}


def test_position_repository_replaces_existing_position_copy_safely() -> None:
    repository = PositionRepository()
    replacement = {"symbol": "NVDA", "declared_exposure": 10.0, "metadata": {"source": "fills"}}
    repository.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 1.0})

    repository.replace_position(" pos-1 ", replacement)
    replacement["metadata"]["source"] = "mutated"
    readback = repository.read_position("pos-1")
    assert readback == {
        "symbol": "NVDA",
        "declared_exposure": 10.0,
        "metadata": {"source": "fills"},
    }
    assert readback is not None
    readback["metadata"]["source"] = "readback-mutated"

    assert repository.read_position("pos-1") == {
        "symbol": "NVDA",
        "declared_exposure": 10.0,
        "metadata": {"source": "fills"},
    }
