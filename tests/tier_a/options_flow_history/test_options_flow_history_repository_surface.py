from __future__ import annotations

from nvda_desk.repositories.options_flow_history_repository import OptionsFlowHistoryRepository
from nvda_desk.services.options_flow_context_service import OptionsFlowContextService


def test_options_flow_history_repository_and_context_service_surfaces_are_present() -> None:
    assert OptionsFlowHistoryRepository is not None
    assert OptionsFlowContextService is not None


def test_options_flow_history_repository_preserves_append_order_and_copy_boundary() -> None:
    repository = OptionsFlowHistoryRepository()
    source = {"record_id": "flow-1", "payload": {"front_dte": 1}}

    repository.append_record(source)
    repository.append_record({"record_id": "flow-2", "payload": {"front_dte": 5}})
    source["payload"]["front_dte"] = 99
    listed = repository.list_records()
    listed[0]["payload"]["front_dte"] = 42

    assert repository.list_records() == [
        {"record_id": "flow-1", "payload": {"front_dte": 1}},
        {"record_id": "flow-2", "payload": {"front_dte": 5}},
    ]
