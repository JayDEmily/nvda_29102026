from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.external_source import (
    ExternalIngressMode,
    ExternalPayloadCarrier,
    ExternalSourceFamily,
    ExternalSourceInterfaceSpec,
    validate_external_payload_boundary,
)


def _operator_bundle_spec() -> ExternalSourceInterfaceSpec:
    return ExternalSourceInterfaceSpec(
        source_id="operator-fixture-bundle",
        source_family=ExternalSourceFamily.OPERATOR_BUNDLE,
        ingress_mode=ExternalIngressMode.OPERATOR_BUNDLE,
        typed_carrier_name="ExternalPayloadCarrier",
    )


def test_external_source_contract_keeps_live_network_authority_closed() -> None:
    assert {mode.value for mode in ExternalIngressMode} == {
        "operator_bundle",
        "checked_in_reference",
        "recorded_api_response",
        "recorded_broker_response",
        "offline_fixture",
    }

    with pytest.raises(ValidationError, match="external_network_clients_not_admitted"):
        ExternalSourceInterfaceSpec(
            source_id="live-network-client",
            source_family=ExternalSourceFamily.MARKET,
            ingress_mode=ExternalIngressMode.RECORDED_API_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
            network_enabled=True,
        )


def test_external_source_contract_keeps_credentials_out_of_interface_specs() -> None:
    with pytest.raises(ValidationError, match="external_credentials_not_admitted"):
        ExternalSourceInterfaceSpec(
            source_id="credentialed-broker",
            source_family=ExternalSourceFamily.BROKER,
            ingress_mode=ExternalIngressMode.RECORDED_BROKER_RESPONSE,
            typed_carrier_name="ExternalPayloadCarrier",
            credential_fields=("api_key", "secret"),
        )


def test_external_source_contract_rejects_nested_payload_authority_on_carrier_construction() -> (
    None
):
    with pytest.raises(ValidationError, match="forbidden_external_payload_keys:api_key,order_qty"):
        ExternalPayloadCarrier(
            interface=_operator_bundle_spec(),
            payload={
                "symbol": "NVDA",
                "nested": {
                    "api_key": "not-admitted",
                    "orders": [{"order_qty": 10}],
                },
            },
        )


def test_external_source_contract_accepts_recorded_payload_without_mutating_source_input() -> None:
    payload = {
        "symbol": "NVDA",
        "metadata": {"provider": "recorded-fixture", "sequence": 7},
    }

    result = validate_external_payload_boundary(
        interface=_operator_bundle_spec(),
        payload=payload,
    )
    carrier = ExternalPayloadCarrier(interface=_operator_bundle_spec(), payload=payload)

    payload["metadata"]["sequence"] = 99
    detached = carrier.payload_copy()
    detached["metadata"]["sequence"] = 100

    assert result.accepted is True
    assert result.rejected_keys == ()
    assert carrier.payload["metadata"]["sequence"] == 7
