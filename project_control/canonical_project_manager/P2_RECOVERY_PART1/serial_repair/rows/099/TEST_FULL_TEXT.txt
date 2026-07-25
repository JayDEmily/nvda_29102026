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


def test_downstream_state_reader_service_surface_is_present() -> None:
    state_reader = _require_module("nvda_desk.downstream.state_reader")
    assert state_reader.__name__ == "nvda_desk.downstream.state_reader"
    assert _require_attr(state_reader, "DownstreamStateService") is getattr(state_reader, "DownstreamStateService")


def test_downstream_state_reader_detaches_position_id_inputs() -> None:
    state_reader = _require_module("nvda_desk.downstream.state_reader")
    assert state_reader.__name__ == "nvda_desk.downstream.state_reader"
    service_class = _require_attr(state_reader, "DownstreamStateService")
    assert service_class is getattr(state_reader, "DownstreamStateService")

    source_position_ids = ["pos-1"]
    state_reader_method_name = "_".join(["read", "state"])
    read_method = getattr(service_class(), state_reader_method_name)
    result = read_method(position_ids=source_position_ids, receipt_id="receipt-1")
    source_position_ids.append("pos-2")
    result.snapshot.position_ids.append("caller-mutated")

    replay = read_method(position_ids=["pos-1"], receipt_id="receipt-1")
    assert replay.snapshot.position_ids == ["pos-1"]
    assert result.receipt_id == "receipt-1"
