from __future__ import annotations

import pytest

from nvda_desk.repositories.review_repository import ReviewRepository


def test_review_repository_rejects_duplicate_ids_and_preserves_copy_boundary() -> None:
    repository = ReviewRepository()
    source = {"review_status": "recorded", "lineage": {"source": "review-stage"}}

    repository.write_packet("review-1", source)
    source["lineage"]["source"] = "mutated"
    readback = repository.read_packet("review-1")
    assert readback == {
        "review_status": "recorded",
        "lineage": {"source": "review-stage"},
    }
    assert readback is not None
    readback["lineage"]["source"] = "readback-mutated"

    assert repository.read_packet("review-1") == {
        "review_status": "recorded",
        "lineage": {"source": "review-stage"},
    }
    with pytest.raises(ValueError, match="duplicate packet_id"):
        repository.write_packet("review-1", {"review_status": "replacement"})


def test_review_repository_lists_packets_in_insertion_order() -> None:
    repository = ReviewRepository()

    repository.write_packet("review-1", {"sequence": 1})
    repository.write_packet("review-2", {"sequence": 2})

    listed = repository.list_packets()
    listed[0]["sequence"] = 99
    assert repository.list_packets() == [{"sequence": 1}, {"sequence": 2}]


def test_review_repository_rejects_empty_id_and_duplicate_after_normalisation() -> None:
    repository = ReviewRepository()

    with pytest.raises(ValueError, match="packet_id must be non-empty"):
        repository.write_packet("  ", {"review_status": "recorded"})

    repository.write_packet("review-1", {"sequence": 1})
    with pytest.raises(ValueError, match="duplicate packet_id: review-1"):
        repository.write_packet(" review-1 ", {"sequence": 2})

    assert repository.read_packet(" review-1 ") == {"sequence": 1}
