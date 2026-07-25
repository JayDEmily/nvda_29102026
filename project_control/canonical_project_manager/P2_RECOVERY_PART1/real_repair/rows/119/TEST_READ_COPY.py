from __future__ import annotations

from nvda_desk.persistence.execution_records import ExecutionRecordsRepository


def test_execution_records_repository_preserves_append_order_and_copy_boundary() -> None:
    repository = ExecutionRecordsRepository()
    source = {"execution_id": "exec-1", "payload": {"side": "buy"}}

    repository.append_record(source)
    repository.append_record({"execution_id": "exec-2", "payload": {"side": "hold"}})
    source["payload"]["side"] = "mutated"
    listed = repository.list_records()
    listed[0]["payload"]["side"] = "listed-mutated"

    assert repository.list_records() == [
        {"execution_id": "exec-1", "payload": {"side": "buy"}},
        {"execution_id": "exec-2", "payload": {"side": "hold"}},
    ]


def test_execution_records_repository_exposes_no_keyed_overwrite_method() -> None:
    repository = ExecutionRecordsRepository()

    assert hasattr(repository, "append_record")
    assert hasattr(repository, "list_records")
    assert not hasattr(repository, "write_record")
    assert not hasattr(repository, "upsert_record")
