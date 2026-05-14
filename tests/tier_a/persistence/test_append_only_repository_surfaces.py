from __future__ import annotations

from nvda_desk.repositories.execution_event_repository import ExecutionEventRepository
from nvda_desk.repositories.market_observation_repository import MarketObservationRepository


def test_execution_event_repository_preserves_append_order_and_copy_boundary() -> None:
    repository = ExecutionEventRepository()
    source = {"event_id": "evt-1", "payload": {"stage": "submitted"}}

    repository.append_event(source)
    repository.append_event({"event_id": "evt-2", "payload": {"stage": "accepted"}})
    source["payload"]["stage"] = "mutated"
    listed = repository.list_events()
    listed[0]["payload"]["stage"] = "listed-mutated"

    assert repository.list_events() == [
        {"event_id": "evt-1", "payload": {"stage": "submitted"}},
        {"event_id": "evt-2", "payload": {"stage": "accepted"}},
    ]


def test_market_observation_repository_preserves_append_order_and_copy_boundary() -> None:
    repository = MarketObservationRepository()
    source = {"observation_id": "obs-1", "payload": {"spot": 101.0}}

    repository.append_observation(source)
    repository.append_observation({"observation_id": "obs-2", "payload": {"spot": 102.0}})
    source["payload"]["spot"] = 999.0
    listed = repository.list_observations()
    listed[0]["payload"]["spot"] = 0.0

    assert repository.list_observations() == [
        {"observation_id": "obs-1", "payload": {"spot": 101.0}},
        {"observation_id": "obs-2", "payload": {"spot": 102.0}},
    ]


def test_append_only_observation_repositories_do_not_expose_keyed_mutators() -> None:
    """Append-only observation stores must not expose keyed overwrite/update surfaces."""

    prohibited_mutators = {
        "delete",
        "delete_event",
        "delete_observation",
        "replace",
        "replace_event",
        "replace_observation",
        "upsert",
        "upsert_event",
        "upsert_observation",
        "write",
        "write_event",
        "write_observation",
    }

    for repository in (ExecutionEventRepository(), MarketObservationRepository()):
        public_methods = {
            name
            for name in dir(repository)
            if not name.startswith("_") and callable(getattr(repository, name))
        }

        assert public_methods.isdisjoint(prohibited_mutators)
