"""External source/API ingress authority-readiness proofs."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.external_source import (
    ExternalIngressMode,
    ExternalPayloadCarrier,
    ExternalSourceFamily,
    ExternalSourceInterfaceSpec,
    validate_external_payload_boundary,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN_CLIENT_IMPORTS = {"openai", "requests", "httpx", "aiohttp", "websocket"}


def _market_spec() -> ExternalSourceInterfaceSpec:
    return ExternalSourceInterfaceSpec(
        source_id="recorded-nvda-market-snapshot",
        source_family=ExternalSourceFamily.MARKET,
        ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
        typed_carrier_name="ExternalPayloadCarrier",
    )


def test_external_source_spec_is_authority_readiness_only() -> None:
    spec = _market_spec()

    assert spec.network_enabled is False
    assert spec.credential_fields == ()
    assert spec.source_family is ExternalSourceFamily.MARKET
    assert spec.ingress_mode is ExternalIngressMode.RECORDED_API_RESPONSE


def test_external_source_spec_rejects_network_and_credentials() -> None:
    with pytest.raises(ValidationError, match="external_network_clients_not_admitted"):
        ExternalSourceInterfaceSpec(
            source_id="live-client",
            source_family=ExternalSourceFamily.OPTIONS,
            ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
            network_enabled=True,
        )

    with pytest.raises(ValidationError, match="external_credentials_not_admitted"):
        ExternalSourceInterfaceSpec(
            source_id="credentialed-client",
            source_family=ExternalSourceFamily.BROKER,
            ingress_mode=ExternalIngressMode.RECORDED_BROKER_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
            credential_fields=("api_key",),
        )


def test_external_payload_carrier_is_copy_safe_and_boundary_only() -> None:
    payload = {"symbol": "NVDA", "bid": 123.45, "nested": {"source": "recorded"}}
    carrier = ExternalPayloadCarrier(interface=_market_spec(), payload=payload)

    payload["bid"] = 999.0
    payload["nested"]["source"] = "mutated"
    detached = carrier.payload_copy()
    detached["nested"]["source"] = "caller-mutated"

    assert carrier.payload["bid"] == 123.45
    assert carrier.payload["nested"]["source"] == "recorded"


def test_external_payload_boundary_rejects_runtime_and_secret_keys() -> None:
    result = validate_external_payload_boundary(
        interface=_market_spec(),
        payload={
            "symbol": "NVDA",
            "trade_allowed": True,
            "order_qty": 100,
            "api_key": "not-admitted",
        },
    )

    assert result.accepted is False
    assert result.rejection_reason == "forbidden_external_payload_keys"
    assert result.rejected_keys == ("api_key", "order_qty", "trade_allowed")


def test_external_payload_boundary_accepts_recorded_source_shapes() -> None:
    result = validate_external_payload_boundary(
        interface=_market_spec(),
        payload={"symbol": "NVDA", "bid": 123.45, "ask": 123.55, "source_sequence": 7},
    )

    assert result.accepted is True
    assert result.rejection_reason is None
    assert result.rejected_keys == ()


def test_current_ingress_adapters_do_not_import_concrete_network_clients() -> None:
    adapter_files = sorted((REPO_ROOT / "src/nvda_desk/adapters/ingress").glob("*.py"))
    assert [path.name for path in adapter_files] == [
        "__init__.py",
        "calendar_feed.py",
        "market_snapshot_feed.py",
        "options_surface_feed.py",
    ]

    imported_roots: set[str] = set()
    for path in adapter_files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".", maxsplit=1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".", maxsplit=1)[0])

    assert imported_roots.isdisjoint(FORBIDDEN_CLIENT_IMPORTS) is True


def test_broker_boundary_remains_protocol_only_not_concrete_adapter() -> None:
    broker_module = (REPO_ROOT / "src/nvda_desk/adapters/egress/broker_protocol.py").read_text(
        encoding="utf-8"
    )

    assert "class BrokerGatewayProtocol(Protocol):" in broker_module
    assert "requests" not in broker_module
    assert "httpx" not in broker_module
    assert "submit_order_intent" in broker_module


def test_external_source_spec_rejects_empty_identity_fields() -> None:
    with pytest.raises(ValidationError):
        ExternalSourceInterfaceSpec(
            source_id="",
            source_family=ExternalSourceFamily.MARKET,
            ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
        )

    with pytest.raises(ValidationError):
        ExternalSourceInterfaceSpec(
            source_id="recorded-nvda-market-snapshot",
            source_family=ExternalSourceFamily.MARKET,
            ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
            typed_carrier_name="",
        )


def test_external_payload_carrier_rejects_extra_client_state_fields() -> None:
    with pytest.raises(ValidationError):
        ExternalPayloadCarrier(
            interface=_market_spec(),
            payload={"symbol": "NVDA", "bid": 123.45},
            client_session="not-admitted",
        )


def test_external_payload_boundary_rejects_each_critical_authority_or_secret_key() -> None:
    critical_keys = (
        "api_key",
        "auth_header",
        "authorised_notional_usd",
        "brokerage_order",
        "execution_receipt",
        "order_qty",
        "persistence_write_path",
        "position_size",
        "secret",
        "trade_allowed",
    )

    for key in critical_keys:
        result = validate_external_payload_boundary(
            interface=_market_spec(),
            payload={"symbol": "NVDA", key: "not-admitted"},
        )

        assert result.accepted is False, key
        assert result.rejection_reason == "forbidden_external_payload_keys", key
        assert result.rejected_keys == (key,), key


def test_external_source_validation_result_is_immutable() -> None:
    result = validate_external_payload_boundary(
        interface=_market_spec(),
        payload={"symbol": "NVDA", "bid": 123.45},
    )

    with pytest.raises(ValidationError):
        result.accepted = False


def test_external_payload_boundary_rejects_nested_authority_or_secret_keys() -> None:
    result = validate_external_payload_boundary(
        interface=_market_spec(),
        payload={
            "symbol": "NVDA",
            "metadata": {
                "provider": "recorded-fixture",
                "api_key": "not-admitted",
                "trade_allowed": True,
            },
        },
    )

    assert result.accepted is False
    assert result.rejection_reason == "forbidden_external_payload_keys"
    assert result.rejected_keys == ("api_key", "trade_allowed")
