from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_api_dto_boundary_surface_is_present() -> None:
    dto_module = _require_module("nvda_desk.adapters.egress.api_dto_adapter")
    assert dto_module.__name__ == "nvda_desk.adapters.egress.api_dto_adapter"
    deps_module = _require_module("nvda_desk.api.deps")
    assert deps_module.__name__ == "nvda_desk.api.deps"

    adapter_cls = _require_attr(dto_module, "ApiDtoAdapter")
    assert adapter_cls is getattr(dto_module, "ApiDtoAdapter")
    get_api_dto_adapter = _require_attr(deps_module, "get_api_dto_adapter")
    assert get_api_dto_adapter is getattr(deps_module, "get_api_dto_adapter")

    adapter = get_api_dto_adapter()

    assert isinstance(adapter, adapter_cls)
    assert callable(_require_attr(adapter_cls, "to_runtime_dto"))
    assert callable(_require_attr(adapter_cls, "to_review_dto"))
    assert callable(_require_attr(adapter_cls, "to_state_dto"))


def test_api_shell_uses_admitted_dto_boundary_owner() -> None:
    app_module = _require_module("nvda_desk.api.app")
    assert app_module.__name__ == "nvda_desk.api.app"

    create_app = _require_attr(app_module, "create_app")
    assert create_app is getattr(app_module, "create_app")

    class StubOrchestrator:
        def run_once(self, stage_inputs):
            return {"stage_inputs": dict(stage_inputs), "kind": "native-runtime-receipt"}

    class RecordingDtoAdapter:
        def __init__(self) -> None:
            self.calls: list[tuple[str, dict]] = []

        def to_runtime_dto(self, value):
            payload = dict(value)
            self.calls.append(("runtime", payload))
            return {"dto_kind": "runtime", "payload": payload}

        def to_review_dto(self, value):
            payload = dict(value)
            self.calls.append(("review", payload))
            return {"dto_kind": "review", "payload": payload}

        def to_state_dto(self, value):
            payload = dict(value)
            self.calls.append(("state", payload))
            return {"dto_kind": "state", "payload": payload}

    adapter = RecordingDtoAdapter()
    app = create_app(orchestrator=StubOrchestrator(), dto_adapter=adapter)

    assert app.healthcheck() == {"dto_kind": "state", "payload": {"status": "ok"}}
    assert app.run_once({"temporal": {"present": True}}) == {
        "dto_kind": "runtime",
        "payload": {
            "stage_inputs": {"temporal": {"present": True}},
            "kind": "native-runtime-receipt",
        },
    }
    assert adapter.calls == [
        ("state", {"status": "ok"}),
        (
            "runtime",
            {
                "stage_inputs": {"temporal": {"present": True}},
                "kind": "native-runtime-receipt",
            },
        ),
    ]
