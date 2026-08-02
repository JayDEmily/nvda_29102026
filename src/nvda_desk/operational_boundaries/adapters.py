"""Injected operational adapters with no default network implementation."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Mapping, Protocol, runtime_checkable

from nvda_desk.m10_execution_gateway import LivePlacementIntent
from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint

from .contracts import (
    BrokerOperationalConfig,
    BrokerSubmissionReceipt,
    MarketDataOperationalConfig,
    OperationalBlocker,
    OperationalMode,
    ProviderSnapshotReceipt,
    ProviderSnapshotRequest,
)


@runtime_checkable
class CredentialResolver(Protocol):
    def resolve(self, reference: str) -> str | None: ...


@runtime_checkable
class MarketDataTransport(Protocol):
    transport_kind: str

    def fetch_snapshot(self, **kwargs: Any) -> Mapping[str, Any]: ...


@runtime_checkable
class BrokerTransport(Protocol):
    transport_kind: str

    def submit_order(self, **kwargs: Any) -> Mapping[str, Any]: ...


class EnvironmentCredentialResolver:
    """Resolve only an explicitly named environment variable at call time."""

    def resolve(self, reference: str) -> str | None:
        value = os.environ.get(reference)
        return value if value and value.strip() else None


def _require_utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


class LiveMarketDataAdapter:
    """External market-data boundary; offline by default and transport-injected."""

    def __init__(
        self,
        *,
        config: MarketDataOperationalConfig,
        credential_resolver: CredentialResolver,
        transport: MarketDataTransport,
    ) -> None:
        if not isinstance(credential_resolver, CredentialResolver):
            raise TypeError("credential_resolver_protocol_required")
        if not isinstance(transport, MarketDataTransport):
            raise TypeError("market_data_transport_protocol_required")
        self.config = config
        self._credentials = credential_resolver
        self._transport = transport

    def fetch(self, request: ProviderSnapshotRequest) -> ProviderSnapshotReceipt:
        request = ProviderSnapshotRequest.model_validate(request.model_dump(mode="python"))
        config = self.config
        if config.mode is OperationalMode.OFFLINE:
            raise OperationalBlocker("market_data_operation_offline")
        if config.kill_switch_engaged:
            raise OperationalBlocker("market_data_kill_switch_engaged")
        if request.provider_id != config.provider_id:
            raise OperationalBlocker("market_data_provider_mismatch")
        assert config.credential_reference is not None
        credential = self._credentials.resolve(config.credential_reference)
        if not credential:
            raise OperationalBlocker("market_data_credential_unavailable")
        expected_transport = "hermetic" if config.mode is OperationalMode.VALIDATION else "network"
        if self._transport.transport_kind != expected_transport:
            raise OperationalBlocker("market_data_transport_environment_mismatch")
        try:
            response = self._transport.fetch_snapshot(
                endpoint=config.endpoint,
                credential=credential,
                provider_id=config.provider_id,
                environment=config.environment,
                request=request.model_dump(mode="python"),
            )
        except Exception as exc:
            raise OperationalBlocker("market_data_endpoint_unavailable") from exc
        try:
            provider_request_id = str(response["provider_request_id"])
            observed_at_utc = _require_utc(
                response["observed_at_utc"], "provider_observation_time_must_be_utc"
            )
            raw_material = response["raw_material"]
            if not isinstance(raw_material, bytes) or not raw_material:
                raise TypeError("provider_raw_material_must_be_nonempty_bytes")
        except Exception as exc:
            raise OperationalBlocker("market_data_response_invalid") from exc
        payload = {
            "request": request,
            "request_id": request.request_id,
            "request_fingerprint": request.semantic_fingerprint,
            "provider_id": request.provider_id,
            "environment": config.environment,
            "operational_mode": config.mode,
            "provider_request_id": provider_request_id,
            "observed_at_utc": observed_at_utc,
            "raw_material": raw_material,
            "content_sha256": sha256(raw_material).hexdigest(),
            "network_fetch_proven": (
                config.mode is OperationalMode.LIVE and response.get("network_fetch_proven") is True
            ),
        }
        fingerprint = semantic_fingerprint(
            {key: value for key, value in payload.items() if key != "raw_material"}
        )
        return ProviderSnapshotReceipt.model_validate(
            {
                **payload,
                "receipt_id": f"provider-snapshot-receipt:{fingerprint[:24]}",
                "semantic_fingerprint": fingerprint,
            }
        )


class LiveBrokerAdapter:
    """External broker submission boundary with explicit fail-closed interlocks."""

    def __init__(
        self,
        *,
        config: BrokerOperationalConfig,
        credential_resolver: CredentialResolver,
        transport: BrokerTransport,
    ) -> None:
        if not isinstance(credential_resolver, CredentialResolver):
            raise TypeError("credential_resolver_protocol_required")
        if not isinstance(transport, BrokerTransport):
            raise TypeError("broker_transport_protocol_required")
        self.config = config
        self._credentials = credential_resolver
        self._transport = transport

    def submit(
        self, intent: LivePlacementIntent, *, submitted_at_utc: datetime
    ) -> BrokerSubmissionReceipt:
        intent = LivePlacementIntent.model_validate(intent.model_dump(mode="python"))
        submitted_at_utc = _require_utc(submitted_at_utc, "broker_submission_time_must_be_utc")
        if submitted_at_utc < intent.authorised_at_utc:
            raise OperationalBlocker("broker_submission_precedes_live_authorisation")
        config = self.config
        if config.mode is OperationalMode.OFFLINE:
            raise OperationalBlocker("broker_operation_offline")
        if config.kill_switch_engaged:
            raise OperationalBlocker("broker_kill_switch_engaged")
        if (
            config.account_id != config.expected_account_id
            or config.broker_id != intent.broker_id
            or config.account_id != intent.account_id
            or config.live_authorisation_id != intent.live_authorisation_id
            or (config.mode is OperationalMode.LIVE and config.environment != intent.environment)
        ):
            raise OperationalBlocker("broker_account_environment_mismatch")
        assert config.credential_reference is not None
        credential = self._credentials.resolve(config.credential_reference)
        if not credential:
            raise OperationalBlocker("broker_credential_unavailable")
        expected_transport = "hermetic" if config.mode is OperationalMode.VALIDATION else "network"
        if self._transport.transport_kind != expected_transport:
            raise OperationalBlocker("broker_transport_environment_mismatch")
        try:
            response = self._transport.submit_order(
                endpoint=config.endpoint,
                credential=credential,
                broker_id=config.broker_id,
                account_id=config.account_id,
                environment=config.environment,
                intent=intent.model_dump(mode="python"),
                submitted_at_utc=submitted_at_utc,
            )
        except Exception as exc:
            raise OperationalBlocker("broker_endpoint_unavailable") from exc
        try:
            broker_order_id = str(response["broker_order_id"])
            status = str(response["status"])
            if status not in {"accepted", "rejected"}:
                raise ValueError("broker_status_invalid")
            acknowledged_at_utc = _require_utc(
                response["acknowledged_at_utc"], "broker_acknowledgement_time_must_be_utc"
            )
        except Exception as exc:
            raise OperationalBlocker("broker_response_invalid") from exc
        payload = {
            "intent": intent,
            "intent_id": intent.intent_id,
            "intent_fingerprint": intent.semantic_fingerprint,
            "broker_id": intent.broker_id,
            "account_id": intent.account_id,
            "environment": config.environment,
            "operational_mode": config.mode,
            "broker_order_id": broker_order_id,
            "status": status,
            "acknowledged_at_utc": acknowledged_at_utc,
            "network_submission_proven": (
                config.mode is OperationalMode.LIVE
                and response.get("network_submission_proven") is True
            ),
            "live_execution_proven": False,
        }
        fingerprint = semantic_fingerprint(payload)
        return BrokerSubmissionReceipt.model_validate(
            {
                **payload,
                "receipt_id": f"broker-submission-receipt:{fingerprint[:24]}",
                "semantic_fingerprint": fingerprint,
            }
        )
