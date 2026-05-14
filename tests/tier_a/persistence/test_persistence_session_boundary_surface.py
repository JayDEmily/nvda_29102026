from __future__ import annotations

import importlib

from nvda_desk.persistence.session_factory import (
    InMemoryPersistenceSession,
    PersistenceSessionFactory,
)


def test_persistence_session_factory_yields_fresh_bounded_in_memory_sessions() -> None:
    factory = PersistenceSessionFactory()

    with factory.session() as first_session:
        assert isinstance(first_session, InMemoryPersistenceSession)
        first_session["execution_record_ids"] = ["exec-001"]

    with factory.session() as second_session:
        assert isinstance(second_session, InMemoryPersistenceSession)
        assert second_session == {}
        assert second_session is not first_session


def test_persistence_package_does_not_export_donor_db_schema_seed_or_engine_api() -> None:
    persistence_package = importlib.import_module("nvda_desk.persistence")

    assert persistence_package.__all__ == ["ReceiptLedger"]
    assert hasattr(persistence_package, "ReceiptLedger")

    donor_db_api_names = {
        "Base",
        "create_engine_from_url",
        "create_session_factory",
        "create_schema",
        "seed_dev_data",
    }
    for donor_name in donor_db_api_names:
        assert not hasattr(persistence_package, donor_name)


def test_session_factory_surface_does_not_admit_external_engine_or_seed_helpers() -> None:
    session_factory_module = importlib.import_module("nvda_desk.persistence.session_factory")

    assert issubclass(InMemoryPersistenceSession, dict)
    assert hasattr(PersistenceSessionFactory(), "session")

    prohibited_session_surface = {
        "Base",
        "create_engine",
        "create_engine_from_url",
        "create_schema",
        "create_session_factory",
        "seed_dev_data",
        "sessionmaker",
    }
    for donor_name in prohibited_session_surface:
        assert not hasattr(session_factory_module, donor_name)
