from __future__ import annotations

from datetime import datetime, timezone

from nvda_desk.calendar.operational.events import OperationalEventRepository
from nvda_desk.calendar.reference.importer import FinancialCalendarImporter
from nvda_desk.calendar.reference.projection import FinancialCalendarProjectionService
from nvda_desk.repositories.execution_event_repository import ExecutionEventRepository
from nvda_desk.repositories.market_observation_repository import MarketObservationRepository


def test_c006_reference_projection_has_one_explicit_owned_composition_into_operational_query_state() -> (
    None
):
    bundle = FinancialCalendarImporter().load_manifest(
        {
            "bundle_id": "calendar-bundle-1",
            "version": "v1",
            "artifacts": [
                {
                    "artifact_id": "calendar-artifact-1",
                    "source_path": "calendar.json",
                    "version": "v1",
                }
            ],
            "layers": [{"layer_id": "reference-events", "artifact_ids": ["calendar-artifact-1"]}],
        }
    )
    precursor = FinancialCalendarProjectionService().project_runtime_context(
        bundle=bundle,
        event_rows=[
            {
                "event_id": "event-1",
                "source_artifact_id": "calendar-artifact-1",
                "event_type": "fomc_window",
            }
        ],
        context_id="calendar-context-1",
        effective_at=datetime(2026, 4, 21, 13, 30, tzinfo=timezone.utc),
    )
    repository = OperationalEventRepository()

    assert hasattr(repository, "ingest_precursor_context")
    repository.ingest_precursor_context(precursor)  # type: ignore[attr-defined]
    assert [event.event_id for event in repository.list_events()] == ["event-1"]


def _assert_append_only_contract(repository, append_name: str, list_name: str, first: dict) -> None:
    getattr(repository, append_name)(first)
    first["payload"]["value"] = "mutated"
    listed = getattr(repository, list_name)()
    listed[0]["payload"]["value"] = "listed-mutated"
    assert getattr(repository, list_name)()[0]["payload"]["value"] == "original"


def test_c019_c023_shared_memory_repository_contract_is_copy_safe_and_instance_isolated() -> None:
    execution_a = ExecutionEventRepository()
    execution_b = ExecutionEventRepository()
    _assert_append_only_contract(
        execution_a,
        "append_event",
        "list_events",
        {"event_id": "event-1", "payload": {"value": "original"}},
    )
    assert execution_b.list_events() == []

    observation_a = MarketObservationRepository()
    observation_b = MarketObservationRepository()
    _assert_append_only_contract(
        observation_a,
        "append_observation",
        "list_observations",
        {"observation_id": "observation-1", "payload": {"value": "original"}},
    )
    assert observation_b.list_observations() == []
