from __future__ import annotations

import pytest

from nvda_desk.repositories.capital_state_repository import CapitalStateRepository


def test_capital_state_repository_rejects_duplicate_ids_and_preserves_copy_boundary() -> None:
    repository = CapitalStateRepository()
    source = {"cash": 1000.0, "metadata": {"source": "seed"}}

    repository.write_snapshot("cap-1", source)
    source["metadata"]["source"] = "mutated"
    readback = repository.read_snapshot("cap-1")
    assert readback == {"cash": 1000.0, "metadata": {"source": "seed"}}
    assert readback is not None
    readback["metadata"]["source"] = "readback-mutated"

    assert repository.read_snapshot("cap-1") == {
        "cash": 1000.0,
        "metadata": {"source": "seed"},
    }
    with pytest.raises(ValueError, match="duplicate snapshot_id"):
        repository.write_snapshot("cap-1", {"cash": 900.0})


def test_capital_state_repository_lists_snapshots_in_insertion_order() -> None:
    repository = CapitalStateRepository()

    repository.write_snapshot("cap-1", {"cash": 1000.0})
    repository.write_snapshot("cap-2", {"cash": 900.0})

    listed = repository.list_snapshots()
    listed[0]["cash"] = 1.0
    assert repository.list_snapshots() == [{"cash": 1000.0}, {"cash": 900.0}]


def test_capital_state_repository_reads_and_lists_identifier_records_copy_safely() -> None:
    repository = CapitalStateRepository()
    repository.write_snapshot("cap-1", {"cash": 1000.0, "metadata": {"source": "ledger"}})

    record = repository.read_snapshot_record("cap-1")
    assert record == {
        "snapshot_id": "cap-1",
        "snapshot": {"cash": 1000.0, "metadata": {"source": "ledger"}},
    }
    assert record is not None
    record["snapshot"]["metadata"]["source"] = "mutated"

    assert repository.list_snapshot_records() == [
        {
            "snapshot_id": "cap-1",
            "snapshot": {"cash": 1000.0, "metadata": {"source": "ledger"}},
        }
    ]


def test_capital_state_repository_rejects_empty_id_and_duplicate_after_normalisation() -> None:
    repository = CapitalStateRepository()

    with pytest.raises(ValueError, match="snapshot_id must be non-empty"):
        repository.write_snapshot("  ", {"cash": 1000.0})

    repository.write_snapshot("cap-1", {"cash": 1000.0})
    with pytest.raises(ValueError, match="duplicate snapshot_id: cap-1"):
        repository.write_snapshot(" cap-1 ", {"cash": 900.0})

    assert repository.read_snapshot(" cap-1 ") == {"cash": 1000.0}
