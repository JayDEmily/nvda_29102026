from __future__ import annotations

import os
from types import SimpleNamespace
from typing import Any

import pytest

from nvda_desk import composition


def test_injected_construction_passes_only_the_technical_dependency_to_m00(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    persistence = object()
    owner = SimpleNamespace(commands=object(), reads=object())
    calls: list[tuple[str, Any]] = []

    def persistence_factory(dsn: str) -> object:
        calls.append(("persistence", dsn))
        return persistence

    def owner_factory(**kwargs: Any) -> object:
        calls.append(("owner", kwargs))
        return owner

    monkeypatch.setattr(composition, "create_postgres_persistence", persistence_factory)
    app = composition.create_application(
        postgres_dsn="postgresql://stage1-construction",
        raw_signal_owner_factory=owner_factory,
    )

    assert calls == [
        ("persistence", "postgresql://stage1-construction"),
        ("owner", {"durability_port": persistence}),
    ]
    assert type(app) is composition.Application
    assert composition.Application.__slots__ == ("_Application__raw_signal_owner",)
    assert getattr(app, composition.Application.__slots__[0]) is owner
    assert getattr(app, composition.Application.__slots__[0]) is not persistence


def test_owner_factory_only_path_is_bounded_proof_injection() -> None:
    calls: list[dict[str, Any]] = []

    def owner_factory(**kwargs: Any) -> object:
        calls.append(kwargs)
        return SimpleNamespace(commands=object(), reads=object())

    app = composition.create_application(raw_signal_owner_factory=owner_factory)

    assert type(app) is composition.Application
    assert calls == [{}]


def test_production_construction_requires_postgres_dsn() -> None:
    with pytest.raises(ValueError, match="postgres_dsn is required"):
        composition.create_application()


@pytest.mark.skipif(
    not os.environ.get("NVDA_TEST_POSTGRES_DSN"),
    reason="real PostgreSQL construction proof requires NVDA_TEST_POSTGRES_DSN",
)
def test_production_default_constructs_real_postgresql_backed_m00() -> None:
    app = composition.create_application(postgres_dsn=os.environ["NVDA_TEST_POSTGRES_DSN"])
    assert type(app) is composition.Application


def test_application_does_not_invent_long_lived_lifecycle_surface() -> None:
    app = composition.create_application(raw_signal_owner_factory=lambda **_: object())
    for name in ("start", "stop", "close", "shutdown"):
        assert not hasattr(app, name)
