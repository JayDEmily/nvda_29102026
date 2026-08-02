"""Translate bounded ASGI requests into the accepted M00 application contracts."""

from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Mapping

from pydantic import ValidationError

from nvda_desk.entry.cli import prepare_command, query_command, run_command
from nvda_desk.m00_application_shell import RunCoordinator

AsgiReceive = Callable[[], Awaitable[dict[str, Any]]]
AsgiSend = Callable[[dict[str, Any]], Awaitable[None]]


async def _request_body(receive: AsgiReceive) -> bytes:
    chunks: list[bytes] = []
    while True:
        message = await receive()
        message_type = message.get("type")
        if message_type == "http.disconnect":
            break
        if message_type != "http.request":
            raise ValueError("unexpected_asgi_message")
        chunks.append(message.get("body", b""))
        if not message.get("more_body", False):
            break
    return b"".join(chunks)


async def _json_response(
    send: AsgiSend,
    *,
    status: int,
    payload: Mapping[str, Any],
) -> None:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body, "more_body": False})


class _ApplicationAsgiApp:
    """Minimal transport adapter; all application meaning remains in M00."""

    def __init__(self, *, coordinator: RunCoordinator) -> None:
        if coordinator is None:
            raise ValueError("run_coordinator_required")
        self._coordinator = coordinator

    async def __call__(
        self,
        scope: Mapping[str, Any],
        receive: AsgiReceive,
        send: AsgiSend,
    ) -> None:
        if scope.get("type") != "http":
            raise ValueError("http_scope_required")

        method = str(scope.get("method", "")).upper()
        path = str(scope.get("path", ""))
        if path == "/health":
            if method != "GET":
                await _json_response(
                    send,
                    status=405,
                    payload={"error": "method_not_allowed"},
                )
                return
            await _json_response(send, status=200, payload={"status": "ok"})
            return

        handlers = {
            "/commands/prepare": (prepare_command, "invalid_upstream_preparation_command"),
            "/commands/run": (run_command, "invalid_application_command"),
            "/queries/review": (query_command, "invalid_application_query"),
        }
        selected = handlers.get(path)
        if selected is None:
            await _json_response(send, status=404, payload={"error": "not_found"})
            return
        if method != "POST":
            await _json_response(
                send,
                status=405,
                payload={"error": "method_not_allowed"},
            )
            return

        raw_body = await _request_body(receive)
        try:
            payload = json.loads(raw_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            await _json_response(send, status=400, payload={"error": "invalid_json"})
            return
        if not isinstance(payload, dict):
            await _json_response(send, status=400, payload={"error": "invalid_json"})
            return

        handler, validation_error = selected
        try:
            result = handler(payload, coordinator=self._coordinator)
        except (ValidationError, TypeError, ValueError):
            await _json_response(send, status=422, payload={"error": validation_error})
            return
        await _json_response(send, status=200, payload=result)


def configure_middlewares(app: _ApplicationAsgiApp) -> _ApplicationAsgiApp:
    """Return the transport adapter unchanged until middleware is separately admitted."""

    return app


def create_app(*, coordinator: RunCoordinator) -> _ApplicationAsgiApp:
    """Create the canonical ASGI adapter around one explicit M00 coordinator."""

    return configure_middlewares(_ApplicationAsgiApp(coordinator=coordinator))
