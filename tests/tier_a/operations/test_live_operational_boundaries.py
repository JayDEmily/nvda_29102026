"""Tier A proof for fail-closed live-provider and broker boundaries."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest
from tests.support.m10_k15_contract_harness import production_capital_receipt


def _api() -> dict[str, Any]:
    from nvda_desk.m10_execution_gateway import (
        ExecutionGateway,
        LivePlacementPolicy,
        PlacementPolicy,
    )
    from nvda_desk.operational_boundaries import (
        BrokerOperationalConfig,
        EnvironmentCredentialResolver,
        LiveBrokerAdapter,
        LiveMarketDataAdapter,
        MarketDataOperationalConfig,
        OperationalBlocker,
        OperationalMode,
        ProviderSnapshotReceipt,
        ProviderSnapshotRequest,
    )

    return {
        "ExecutionGateway": ExecutionGateway,
        "LivePlacementPolicy": LivePlacementPolicy,
        "PlacementPolicy": PlacementPolicy,
        "BrokerOperationalConfig": BrokerOperationalConfig,
        "EnvironmentCredentialResolver": EnvironmentCredentialResolver,
        "LiveBrokerAdapter": LiveBrokerAdapter,
        "LiveMarketDataAdapter": LiveMarketDataAdapter,
        "MarketDataOperationalConfig": MarketDataOperationalConfig,
        "OperationalBlocker": OperationalBlocker,
        "OperationalMode": OperationalMode,
        "ProviderSnapshotReceipt": ProviderSnapshotReceipt,
        "ProviderSnapshotRequest": ProviderSnapshotRequest,
    }


def _live_intent():
    api = _api()
    gateway = api["ExecutionGateway"]()
    capital = production_capital_receipt()
    plan = gateway.create_intent(
        capital,
        api["PlacementPolicy"](quantity_quantum=Decimal("0.001")),
        limit_price=Decimal("123.45"),
        intent_at_utc=datetime(2026, 8, 1, 1, 1, tzinfo=UTC),
    )
    policy = api["LivePlacementPolicy"](
        broker_id="broker.alpha",
        account_id="account.live.001",
        environment="live",
        live_authorisation_id="approval:live:001",
        quantity_quantum=Decimal("0.001"),
    )
    return gateway.create_live_intent(
        plan,
        policy,
        authorised_at_utc=datetime(2026, 8, 1, 1, 1, 30, tzinfo=UTC),
    )


class _Resolver:
    def __init__(self, value: str | None) -> None:
        self.value = value
        self.calls: list[str] = []

    def resolve(self, reference: str) -> str | None:
        self.calls.append(reference)
        return self.value


class _MarketTransport:
    transport_kind = "hermetic"

    def __init__(self, *, fail: bool = False, network_proven: bool = False) -> None:
        self.fail = fail
        self.network_proven = network_proven
        self.calls: list[dict[str, Any]] = []

    def fetch_snapshot(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        if self.fail:
            raise ConnectionError("endpoint unavailable")
        return {
            "provider_request_id": "provider-request:remote-1",
            "observed_at_utc": datetime(2026, 8, 1, 1, 2, tzinfo=UTC),
            "raw_material": b'{"symbol":"NVDA","price":"123.45"}',
            "network_fetch_proven": self.network_proven,
        }


class _BrokerTransport:
    transport_kind = "hermetic"

    def __init__(self, *, fail: bool = False, network_proven: bool = False) -> None:
        self.fail = fail
        self.network_proven = network_proven
        self.calls: list[dict[str, Any]] = []

    def submit_order(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(kwargs)
        if self.fail:
            raise ConnectionError("endpoint unavailable")
        return {
            "broker_order_id": "broker-order:validation:1",
            "status": "accepted",
            "acknowledged_at_utc": datetime(2026, 8, 1, 1, 2, tzinfo=UTC),
            "network_submission_proven": self.network_proven,
        }


def test_m10_live_intent_is_separate_authority_bound_to_exact_paper_plan() -> None:
    intent = _live_intent()

    assert intent.placement_plan.intent_id == intent.placement_plan_id
    assert intent.placement_plan.semantic_fingerprint == intent.placement_plan_fingerprint
    assert intent.paper_only is False
    assert intent.live_execution_allowed is True
    assert intent.broker_id == "broker.alpha"
    assert intent.account_id == "account.live.001"
    assert intent.live_authorisation_id == "approval:live:001"
    assert intent.quantity == intent.placement_plan.quantity
    assert intent.planned_notional <= intent.placement_plan.authorised_notional


def test_default_offline_provider_boundary_never_resolves_credentials_or_calls_transport() -> None:
    api = _api()
    resolver = _Resolver("secret")
    transport = _MarketTransport()
    adapter = api["LiveMarketDataAdapter"](
        config=api["MarketDataOperationalConfig"](),
        credential_resolver=resolver,
        transport=transport,
    )
    request = api["ProviderSnapshotRequest"].create(
        provider_id="provider.alpha",
        symbol="NVDA",
        requested_at_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
    )

    with pytest.raises(api["OperationalBlocker"], match="market_data_operation_offline"):
        adapter.fetch(request)

    assert resolver.calls == []
    assert transport.calls == []


def test_validation_provider_uses_hermetic_transport_and_retains_source_material() -> None:
    api = _api()
    resolver = _Resolver("validation-secret")
    transport = _MarketTransport()
    config = api["MarketDataOperationalConfig"](
        mode=api["OperationalMode"].VALIDATION,
        provider_id="provider.alpha",
        environment="sandbox",
        endpoint="https://sandbox.provider.invalid/snapshot",
        credential_reference="NVDA_PROVIDER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id="approval:provider-validation:1",
    )
    request = api["ProviderSnapshotRequest"].create(
        provider_id="provider.alpha",
        symbol="NVDA",
        requested_at_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
    )
    receipt = api["LiveMarketDataAdapter"](
        config=config, credential_resolver=resolver, transport=transport
    ).fetch(request)

    assert receipt.operational_mode == "validation"
    assert receipt.network_fetch_proven is False
    assert receipt.raw_material.startswith(b"{")
    assert receipt.content_sha256
    assert resolver.calls == ["NVDA_PROVIDER_TOKEN"]
    assert len(transport.calls) == 1
    assert "validation-secret" not in repr(receipt)


def test_live_provider_missing_credential_and_endpoint_failure_are_hard_blockers() -> None:
    api = _api()
    request = api["ProviderSnapshotRequest"].create(
        provider_id="provider.alpha",
        symbol="NVDA",
        requested_at_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
    )
    config = api["MarketDataOperationalConfig"](
        mode=api["OperationalMode"].LIVE,
        provider_id="provider.alpha",
        environment="live",
        endpoint="https://provider.invalid/snapshot",
        credential_reference="NVDA_PROVIDER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id="approval:provider-live:1",
    )
    transport = _MarketTransport(fail=True)
    transport.transport_kind = "network"
    missing = _Resolver(None)
    adapter = api["LiveMarketDataAdapter"](
        config=config, credential_resolver=missing, transport=transport
    )
    with pytest.raises(api["OperationalBlocker"], match="market_data_credential_unavailable"):
        adapter.fetch(request)
    assert transport.calls == []

    available = _Resolver("secret")
    adapter = api["LiveMarketDataAdapter"](
        config=config, credential_resolver=available, transport=transport
    )
    with pytest.raises(api["OperationalBlocker"], match="market_data_endpoint_unavailable"):
        adapter.fetch(request)
    assert len(transport.calls) == 1


def test_validation_broker_submission_is_hermetic_and_never_claims_live_execution() -> None:
    api = _api()
    intent = _live_intent()
    resolver = _Resolver("validation-secret")
    transport = _BrokerTransport()
    config = api["BrokerOperationalConfig"](
        mode=api["OperationalMode"].VALIDATION,
        broker_id=intent.broker_id,
        environment="paper",
        endpoint="https://paper.broker.invalid/orders",
        account_id=intent.account_id,
        expected_account_id=intent.account_id,
        credential_reference="NVDA_BROKER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id=intent.live_authorisation_id,
    )
    receipt = api["LiveBrokerAdapter"](
        config=config, credential_resolver=resolver, transport=transport
    ).submit(intent, submitted_at_utc=datetime(2026, 8, 1, 1, 2, tzinfo=UTC))

    assert receipt.status == "accepted"
    assert receipt.operational_mode == "validation"
    assert receipt.network_submission_proven is False
    assert receipt.live_execution_proven is False
    assert len(transport.calls) == 1
    assert "validation-secret" not in repr(receipt)


def test_live_broker_kill_switch_account_mismatch_and_missing_credential_block_pre_transport() -> (
    None
):
    api = _api()
    intent = _live_intent()
    transport = _BrokerTransport()

    common = dict(
        mode=api["OperationalMode"].LIVE,
        broker_id=intent.broker_id,
        environment="live",
        endpoint="https://broker.invalid/orders",
        account_id=intent.account_id,
        expected_account_id=intent.account_id,
        credential_reference="NVDA_BROKER_TOKEN",
        live_authorisation_id=intent.live_authorisation_id,
    )
    for config, resolver, reason in (
        (
            api["BrokerOperationalConfig"](**common, kill_switch_engaged=True),
            _Resolver("secret"),
            "broker_kill_switch_engaged",
        ),
        (
            api["BrokerOperationalConfig"](
                **{**common, "expected_account_id": "account.live.other"},
                kill_switch_engaged=False,
            ),
            _Resolver("secret"),
            "broker_account_environment_mismatch",
        ),
        (
            api["BrokerOperationalConfig"](**common, kill_switch_engaged=False),
            _Resolver(None),
            "broker_credential_unavailable",
        ),
    ):
        adapter = api["LiveBrokerAdapter"](
            config=config, credential_resolver=resolver, transport=transport
        )
        with pytest.raises(api["OperationalBlocker"], match=reason):
            adapter.submit(intent, submitted_at_utc=datetime(2026, 8, 1, 1, 2, tzinfo=UTC))
    assert transport.calls == []


def test_live_broker_endpoint_failure_is_not_retried_or_converted_to_paper() -> None:
    api = _api()
    intent = _live_intent()
    transport = _BrokerTransport(fail=True)
    transport.transport_kind = "network"
    config = api["BrokerOperationalConfig"](
        mode=api["OperationalMode"].LIVE,
        broker_id=intent.broker_id,
        environment="live",
        endpoint="https://broker.invalid/orders",
        account_id=intent.account_id,
        expected_account_id=intent.account_id,
        credential_reference="NVDA_BROKER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id=intent.live_authorisation_id,
    )
    adapter = api["LiveBrokerAdapter"](
        config=config, credential_resolver=_Resolver("secret"), transport=transport
    )

    with pytest.raises(api["OperationalBlocker"], match="broker_endpoint_unavailable"):
        adapter.submit(intent, submitted_at_utc=datetime(2026, 8, 1, 1, 2, tzinfo=UTC))

    assert len(transport.calls) == 1


def test_environment_credential_resolver_reads_only_the_named_reference(monkeypatch) -> None:
    api = _api()
    monkeypatch.setenv("NVDA_TEST_SECRET", "secret-value")
    resolver = api["EnvironmentCredentialResolver"]()
    assert resolver.resolve("NVDA_TEST_SECRET") == "secret-value"
    assert resolver.resolve("MISSING_SECRET") is None


def test_live_transport_mode_does_not_by_itself_prove_network_or_execution() -> None:
    api = _api()
    intent = _live_intent()
    broker_transport = _BrokerTransport(network_proven=False)
    broker_transport.transport_kind = "network"
    broker_config = api["BrokerOperationalConfig"](
        mode=api["OperationalMode"].LIVE,
        broker_id=intent.broker_id,
        environment="live",
        endpoint="https://broker.invalid/orders",
        account_id=intent.account_id,
        expected_account_id=intent.account_id,
        credential_reference="NVDA_BROKER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id=intent.live_authorisation_id,
    )
    receipt = api["LiveBrokerAdapter"](
        config=broker_config,
        credential_resolver=_Resolver("secret"),
        transport=broker_transport,
    ).submit(intent, submitted_at_utc=datetime(2026, 8, 1, 1, 2, tzinfo=UTC))

    assert receipt.network_submission_proven is False
    assert receipt.live_execution_proven is False


def test_provider_receipt_raw_material_is_bound_by_content_hash() -> None:
    api = _api()
    transport = _MarketTransport()
    config = api["MarketDataOperationalConfig"](
        mode=api["OperationalMode"].VALIDATION,
        provider_id="provider.alpha",
        environment="sandbox",
        endpoint="https://sandbox.provider.invalid/snapshot",
        credential_reference="NVDA_PROVIDER_TOKEN",
        kill_switch_engaged=False,
        live_authorisation_id="approval:provider-validation:1",
    )
    request = api["ProviderSnapshotRequest"].create(
        provider_id="provider.alpha",
        symbol="NVDA",
        requested_at_utc=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
    )
    receipt = api["LiveMarketDataAdapter"](
        config=config, credential_resolver=_Resolver("secret"), transport=transport
    ).fetch(request)

    forged = receipt.model_dump(mode="python")
    forged["raw_material"] = b'{"symbol":"NVDA","price":"999.99"}'
    with pytest.raises(ValueError, match="provider_snapshot_content_hash_mismatch"):
        api["ProviderSnapshotReceipt"].model_validate(forged)
