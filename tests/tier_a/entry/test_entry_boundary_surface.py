from __future__ import annotations

import asyncio
import inspect
import json
from pathlib import Path
from typing import Any

import pytest
from tests.support.m00_application_shell_contract_harness import (
    production_api,
    production_query,
    production_runtime_fixture,
)


async def _asgi_request(
    app: Any,
    *,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    raw_body: bytes | None = None,
) -> tuple[int, dict[str, str], dict[str, Any]]:
    body = raw_body
    if body is None:
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
    messages = [
        {
            "type": "http.request",
            "body": body,
            "more_body": False,
        }
    ]
    sent: list[dict[str, Any]] = []

    async def receive() -> dict[str, Any]:
        if messages:
            return messages.pop(0)
        return {"type": "http.disconnect"}

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await app(
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.5"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": [(b"content-type", b"application/json")],
            "client": ("127.0.0.1", 50000),
            "server": ("testserver", 80),
        },
        receive,
        send,
    )
    start = next(item for item in sent if item["type"] == "http.response.start")
    response_body = b"".join(
        item.get("body", b"") for item in sent if item["type"] == "http.response.body"
    )
    headers = {
        key.decode("latin-1"): value.decode("latin-1") for key, value in start.get("headers", [])
    }
    return start["status"], headers, json.loads(response_body or b"{}")


def _runtime_payload(*, suffix: str) -> tuple[dict[str, Any], Any, Any]:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix=suffix)
    payload = fixture["command"].model_dump(mode="json")
    return payload, fixture["coordinator"], fixture


def _query_payload(*, suffix: str) -> tuple[dict[str, Any], Any, Any]:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix=suffix)
    query = production_query(api, suffix=suffix)
    return query.model_dump(mode="json"), fixture["coordinator"], fixture


def test_entry_public_surface_is_transport_only() -> None:
    import nvda_desk.entry as entry
    import nvda_desk.entry.asgi as asgi
    import nvda_desk.entry.cli as cli

    assert entry.__all__ == [
        "build_cli",
        "configure_middlewares",
        "create_app",
        "query_command",
        "run_cli",
        "run_command",
    ]
    assert entry.create_app is asgi.create_app
    assert entry.run_command is cli.run_command
    assert entry.query_command is cli.query_command
    assert not hasattr(entry, "inspect_config_command")
    assert not hasattr(entry, "run_once_command")


def test_cli_requires_explicit_run_coordinator() -> None:
    from nvda_desk.entry.cli import build_cli, query_command, run_cli, run_command

    for callable_ in (build_cli, run_cli, run_command, query_command):
        signature = inspect.signature(callable_)
        parameter = signature.parameters["coordinator"]
        assert parameter.default is inspect.Parameter.empty
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY

    with pytest.raises(TypeError):
        build_cli()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        run_cli(["run", "--payload-json", "{}"])  # type: ignore[call-arg]


def test_cli_run_translates_exact_application_command() -> None:
    from nvda_desk.entry.cli import run_cli, run_command

    payload, coordinator, fixture = _runtime_payload(suffix="entry-cli-run")

    direct = run_command(payload, coordinator=coordinator)
    via_parser = run_cli(
        ["run", "--payload-json", json.dumps(payload)],
        coordinator=coordinator,
    )

    assert direct["command_id"] == "m00.command.entry-cli-run"
    assert direct["outcome"] == "paper_filled"
    assert via_parser["command_id"] == direct["command_id"]
    assert via_parser["outcome"] == direct["outcome"]
    assert len(fixture["scope_factory"].calls) == 2


def test_cli_query_translates_exact_application_query_without_runtime() -> None:
    from nvda_desk.entry.cli import query_command, run_cli

    payload, coordinator, fixture = _query_payload(suffix="entry-cli-query")

    direct = query_command(payload, coordinator=coordinator)
    via_parser = run_cli(
        ["query", "--payload-json", json.dumps(payload)],
        coordinator=coordinator,
    )

    assert direct["replay_class"] == "comparison_only"
    assert direct["runtime_authority_promoted"] is False
    assert via_parser == direct
    assert fixture["scope_factory"].calls == []
    assert fixture["parallel_evaluator"].calls == []


def test_cli_rejects_untyped_or_extra_authority() -> None:
    from pydantic import ValidationError

    from nvda_desk.entry.cli import query_command, run_command

    payload, coordinator, _ = _runtime_payload(suffix="entry-cli-invalid")
    payload["transport_policy"] = "invented"
    with pytest.raises(ValidationError):
        run_command(payload, coordinator=coordinator)

    query_payload, query_coordinator, _ = _query_payload(suffix="entry-query-invalid")
    query_payload["live_side_effects"] = ["network_read"]
    with pytest.raises(ValidationError):
        query_command(query_payload, coordinator=query_coordinator)


def test_asgi_requires_explicit_run_coordinator_and_preserves_middleware_identity() -> None:
    from nvda_desk.entry.asgi import configure_middlewares, create_app

    signature = inspect.signature(create_app)
    parameter = signature.parameters["coordinator"]
    assert parameter.default is inspect.Parameter.empty
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    with pytest.raises(TypeError):
        create_app()  # type: ignore[call-arg]

    _, coordinator, _ = _runtime_payload(suffix="entry-asgi-construction")
    app = create_app(coordinator=coordinator)
    assert configure_middlewares(app) is app


def test_asgi_health_is_mechanical_and_side_effect_free() -> None:
    from nvda_desk.entry.asgi import create_app

    _, coordinator, fixture = _runtime_payload(suffix="entry-asgi-health")
    app = create_app(coordinator=coordinator)

    status, headers, body = asyncio.run(_asgi_request(app, method="GET", path="/health"))

    assert status == 200
    assert headers["content-type"] == "application/json"
    assert body == {"status": "ok"}
    assert fixture["scope_factory"].calls == []
    assert fixture["parallel_evaluator"].calls == []


def test_asgi_command_route_matches_cli_translation() -> None:
    from nvda_desk.entry.asgi import create_app
    from nvda_desk.entry.cli import run_command

    payload, coordinator, _ = _runtime_payload(suffix="entry-asgi-run")
    cli_result = run_command(payload, coordinator=coordinator)
    app = create_app(coordinator=coordinator)

    status, _, body = asyncio.run(
        _asgi_request(app, method="POST", path="/commands/run", payload=payload)
    )

    assert status == 200
    assert body["command_id"] == cli_result["command_id"]
    assert body["outcome"] == cli_result["outcome"]
    assert body["owner_steps"] == cli_result["owner_steps"]


def test_asgi_query_route_matches_cli_and_does_not_invoke_runtime() -> None:
    from nvda_desk.entry.asgi import create_app
    from nvda_desk.entry.cli import query_command

    payload, coordinator, fixture = _query_payload(suffix="entry-asgi-query")
    cli_result = query_command(payload, coordinator=coordinator)
    app = create_app(coordinator=coordinator)

    status, _, body = asyncio.run(
        _asgi_request(app, method="POST", path="/queries/review", payload=payload)
    )

    assert status == 200
    assert body == cli_result
    assert fixture["scope_factory"].calls == []
    assert fixture["parallel_evaluator"].calls == []


@pytest.mark.parametrize(
    ("method", "path", "raw_body", "expected_status", "expected_error"),
    [
        ("POST", "/commands/run", b"{", 400, "invalid_json"),
        ("POST", "/commands/run", b"{}", 422, "invalid_application_command"),
        ("POST", "/queries/review", b"{}", 422, "invalid_application_query"),
        ("GET", "/commands/run", b"", 405, "method_not_allowed"),
        ("POST", "/unknown", b"{}", 404, "not_found"),
    ],
)
def test_asgi_fails_closed_at_transport_boundary(
    method: str,
    path: str,
    raw_body: bytes,
    expected_status: int,
    expected_error: str,
) -> None:
    from nvda_desk.entry.asgi import create_app

    _, coordinator, _ = _runtime_payload(suffix=f"entry-asgi-error-{expected_status}")
    app = create_app(coordinator=coordinator)

    status, _, body = asyncio.run(_asgi_request(app, method=method, path=path, raw_body=raw_body))

    assert status == expected_status
    assert body == {"error": expected_error}


def test_entry_sources_quarantine_legacy_composition_and_domain_owners() -> None:
    entry_root = Path("src/nvda_desk/entry")
    source = "\n".join(path.read_text(encoding="utf-8") for path in entry_root.glob("*.py"))

    assert "nvda_desk.m00_application_shell" in source
    for prohibited in (
        "nvda_desk.api.app",
        "nvda_desk.api.deps",
        "nvda_desk.runtime.orchestrator",
        "DeskRuntimeOrchestrator",
        "HttpApp",
        "datetime.now",
        "datetime.utcnow",
    ):
        assert prohibited not in source
    for owner in range(1, 14):
        assert f"nvda_desk.m{owner:02d}_" not in source
