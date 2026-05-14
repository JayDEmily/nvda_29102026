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


def test_broker_boundary_protocol_surface_is_present() -> None:
    module = _require_module("nvda_desk.adapters.egress.broker_protocol")
    assert module.__name__ == "nvda_desk.adapters.egress.broker_protocol"

    gateway_protocol = _require_attr(module, "BrokerGatewayProtocol")
    assert gateway_protocol is getattr(module, "BrokerGatewayProtocol")
    broker_protocol = _require_attr(module, "BrokerProtocol")
    assert broker_protocol is getattr(module, "BrokerProtocol")

    assert broker_protocol is gateway_protocol
    assert callable(_require_attr(gateway_protocol, "submit_order_intent"))
    assert callable(_require_attr(gateway_protocol, "read_order_events"))
    assert callable(_require_attr(gateway_protocol, "read_fill_events"))
    assert callable(_require_attr(gateway_protocol, "read_positions"))


def test_broker_boundary_remains_protocol_only_without_concrete_adapters() -> None:
    module = _require_module("nvda_desk.adapters.egress.broker_protocol")
    assert module.__name__ == "nvda_desk.adapters.egress.broker_protocol"

    assert not hasattr(module, "PaperBrokerAdapter")
    assert not hasattr(module, "LiveBrokerAdapter")
