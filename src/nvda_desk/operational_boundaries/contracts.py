"""Typed operational configuration and receipts for explicit external boundaries."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.m10_execution_gateway import LivePlacementIntent
from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint


class OperationalBlocker(RuntimeError):
    """Hard operational failure that must never be converted into a fallback."""


class OperationalMode(StrEnum):
    OFFLINE = "offline"
    VALIDATION = "validation"
    LIVE = "live"


def _utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


class MarketDataOperationalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: OperationalMode = OperationalMode.OFFLINE
    provider_id: str | None = None
    environment: Literal["sandbox", "live"] | None = None
    endpoint: str | None = None
    credential_reference: str | None = None
    kill_switch_engaged: bool = True
    live_authorisation_id: str | None = None

    @model_validator(mode="after")
    def _shape(self) -> "MarketDataOperationalConfig":
        if self.mode is OperationalMode.OFFLINE:
            return self
        for name in (
            "provider_id",
            "environment",
            "endpoint",
            "credential_reference",
            "live_authorisation_id",
        ):
            if not getattr(self, name):
                raise ValueError(f"market_data_{name}_required")
        if not str(self.endpoint).startswith("https://"):
            raise ValueError("market_data_https_endpoint_required")
        if self.mode is OperationalMode.VALIDATION and self.environment != "sandbox":
            raise ValueError("validation_market_data_requires_sandbox")
        if self.mode is OperationalMode.LIVE and self.environment != "live":
            raise ValueError("live_market_data_requires_live_environment")
        return self


class BrokerOperationalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: OperationalMode = OperationalMode.OFFLINE
    broker_id: str | None = None
    environment: Literal["paper", "live"] | None = None
    endpoint: str | None = None
    account_id: str | None = None
    expected_account_id: str | None = None
    credential_reference: str | None = None
    kill_switch_engaged: bool = True
    live_authorisation_id: str | None = None

    @model_validator(mode="after")
    def _shape(self) -> "BrokerOperationalConfig":
        if self.mode is OperationalMode.OFFLINE:
            return self
        for name in (
            "broker_id",
            "environment",
            "endpoint",
            "account_id",
            "expected_account_id",
            "credential_reference",
            "live_authorisation_id",
        ):
            if not getattr(self, name):
                raise ValueError(f"broker_{name}_required")
        if not str(self.endpoint).startswith("https://"):
            raise ValueError("broker_https_endpoint_required")
        if self.mode is OperationalMode.VALIDATION and self.environment != "paper":
            raise ValueError("validation_broker_requires_paper_environment")
        if self.mode is OperationalMode.LIVE and self.environment != "live":
            raise ValueError("live_broker_requires_live_environment")
        return self


class ProviderSnapshotRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    request_id: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    symbol: Literal["NVDA"] = "NVDA"
    requested_at_utc: datetime
    semantic_fingerprint: str

    @classmethod
    def create(
        cls, *, provider_id: str, symbol: str, requested_at_utc: datetime
    ) -> "ProviderSnapshotRequest":
        material = {
            "provider_id": provider_id,
            "symbol": symbol,
            "requested_at_utc": requested_at_utc,
        }
        fingerprint = semantic_fingerprint(material)
        return cls(
            **material,
            request_id=f"provider-snapshot-request:{fingerprint[:24]}",
            semantic_fingerprint=fingerprint,
        )

    @field_validator("requested_at_utc")
    @classmethod
    def _time(cls, value: datetime) -> datetime:
        return _utc(value, "provider_request_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "ProviderSnapshotRequest":
        expected = semantic_fingerprint(
            self.model_dump(mode="python", exclude={"request_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("provider_snapshot_request_fingerprint_mismatch")
        if self.request_id != f"provider-snapshot-request:{expected[:24]}":
            raise ValueError("provider_snapshot_request_id_mismatch")
        return self


class ProviderSnapshotReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    request: ProviderSnapshotRequest
    request_id: str = Field(min_length=1)
    request_fingerprint: str
    provider_id: str = Field(min_length=1)
    environment: Literal["sandbox", "live"]
    operational_mode: OperationalMode
    provider_request_id: str = Field(min_length=1)
    observed_at_utc: datetime
    raw_material: bytes = Field(min_length=1)
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    network_fetch_proven: bool
    semantic_fingerprint: str

    @field_validator("observed_at_utc")
    @classmethod
    def _time(cls, value: datetime) -> datetime:
        return _utc(value, "provider_observation_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "ProviderSnapshotReceipt":
        request = ProviderSnapshotRequest.model_validate(self.request.model_dump(mode="python"))
        if (self.request_id, self.request_fingerprint, self.provider_id) != (
            request.request_id,
            request.semantic_fingerprint,
            request.provider_id,
        ):
            raise ValueError("provider_snapshot_receipt_request_binding_mismatch")
        if self.content_sha256 != sha256(self.raw_material).hexdigest():
            raise ValueError("provider_snapshot_content_hash_mismatch")
        if self.operational_mode is OperationalMode.VALIDATION and self.network_fetch_proven:
            raise ValueError("validation_provider_cannot_claim_network_fetch")
        fingerprint_material = self.model_dump(
            mode="python",
            exclude={"receipt_id", "semantic_fingerprint", "raw_material"},
        )
        expected = semantic_fingerprint(fingerprint_material)
        if self.semantic_fingerprint != expected:
            raise ValueError("provider_snapshot_receipt_fingerprint_mismatch")
        if self.receipt_id != f"provider-snapshot-receipt:{expected[:24]}":
            raise ValueError("provider_snapshot_receipt_id_mismatch")
        return self


class BrokerSubmissionReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    intent: LivePlacementIntent
    intent_id: str = Field(min_length=1)
    intent_fingerprint: str
    broker_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
    environment: Literal["paper", "live"]
    operational_mode: OperationalMode
    broker_order_id: str = Field(min_length=1)
    status: Literal["accepted", "rejected"]
    acknowledged_at_utc: datetime
    network_submission_proven: bool
    live_execution_proven: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("acknowledged_at_utc")
    @classmethod
    def _time(cls, value: datetime) -> datetime:
        return _utc(value, "broker_acknowledgement_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "BrokerSubmissionReceipt":
        intent = LivePlacementIntent.model_validate(self.intent.model_dump(mode="python"))
        if (self.intent_id, self.intent_fingerprint, self.broker_id, self.account_id) != (
            intent.intent_id,
            intent.semantic_fingerprint,
            intent.broker_id,
            intent.account_id,
        ):
            raise ValueError("broker_receipt_intent_binding_mismatch")
        if self.operational_mode is OperationalMode.VALIDATION and self.network_submission_proven:
            raise ValueError("validation_broker_cannot_claim_network_submission")
        expected = semantic_fingerprint(
            self.model_dump(mode="python", exclude={"receipt_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("broker_submission_receipt_fingerprint_mismatch")
        if self.receipt_id != f"broker-submission-receipt:{expected[:24]}":
            raise ValueError("broker_submission_receipt_id_mismatch")
        return self
