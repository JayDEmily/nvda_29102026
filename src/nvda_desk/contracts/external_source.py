"""Authority-readiness contracts for external source and API ingress boundaries."""

from __future__ import annotations

from copy import deepcopy
from enum import StrEnum
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExternalSourceFamily(StrEnum):
    """Admitted outer-source families before native preparation."""

    MARKET = "market"
    OPTIONS = "options"
    BROKER = "broker"
    CALENDAR = "calendar"
    REFERENCE = "reference"
    OPERATOR_BUNDLE = "operator_bundle"


class ExternalIngressMode(StrEnum):
    """Non-network ingress modes admitted by the current authority-readiness gate."""

    OPERATOR_BUNDLE = "operator_bundle"
    CHECKED_IN_REFERENCE = "checked_in_reference"
    RECORDED_API_RESPONSE = "recorded_api_response"
    RECORDED_BROKER_RESPONSE = "recorded_broker_response"
    OFFLINE_FIXTURE = "offline_fixture"


class ExternalSourceBoundaryError(ValueError):
    """Raised when a payload tries to cross the source boundary unlawfully."""


_FORBIDDEN_PAYLOAD_KEYS = frozenset(
    {
        "account_id",
        "api_key",
        "auth_header",
        "authorised_deployable_pct",
        "authorised_notional_usd",
        "bearer_token",
        "brokerage_order",
        "credential",
        "execution_receipt",
        "order_qty",
        "password",
        "persistence_write_path",
        "position_size",
        "private_key",
        "secret",
        "token",
        "trade_allowed",
    }
)


def _find_forbidden_payload_keys(value: Any) -> tuple[str, ...]:
    """Return forbidden boundary-authority keys anywhere inside a payload tree."""

    found: set[str] = set()

    def visit(candidate: Any) -> None:
        if isinstance(candidate, Mapping):
            for key, nested_value in candidate.items():
                if isinstance(key, str) and key in _FORBIDDEN_PAYLOAD_KEYS:
                    found.add(key)
                visit(nested_value)
        elif isinstance(candidate, (list, tuple, set, frozenset)):
            for nested_value in candidate:
                visit(nested_value)

    visit(value)
    return tuple(sorted(found))


class ExternalSourceInterfaceSpec(BaseModel):
    """Declared source boundary with no concrete network/client authority."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    source_id: str = Field(min_length=1)
    source_family: ExternalSourceFamily
    ingress_mode: ExternalIngressMode
    typed_carrier_name: str = Field(min_length=1)
    network_enabled: bool = False
    credential_fields: tuple[str, ...] = ()

    @field_validator("network_enabled")
    @classmethod
    def _network_must_remain_closed(cls, value: bool) -> bool:
        if value:
            raise ValueError("external_network_clients_not_admitted")
        return value

    @field_validator("credential_fields")
    @classmethod
    def _credentials_must_remain_closed(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if value:
            raise ValueError("external_credentials_not_admitted")
        return value


class ExternalPayloadCarrier(BaseModel):
    """Typed ingress carrier for already-obtained external payload material."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    interface: ExternalSourceInterfaceSpec
    payload: dict[str, Any]
    source_timestamp: str | None = None
    source_reference: str | None = None

    @field_validator("payload")
    @classmethod
    def _payload_must_not_smuggle_authority(cls, value: Mapping[str, Any]) -> dict[str, Any]:
        forbidden = _find_forbidden_payload_keys(value)
        if forbidden:
            raise ValueError("forbidden_external_payload_keys:" + ",".join(forbidden))
        return deepcopy(dict(value))

    def payload_copy(self) -> dict[str, Any]:
        """Return a detached payload copy for downstream validation."""

        return deepcopy(self.payload)


class ExternalSourceValidationResult(BaseModel):
    """Deterministic source-boundary validation result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    accepted: bool
    source_id: str
    source_family: ExternalSourceFamily
    ingress_mode: ExternalIngressMode
    rejection_reason: str | None = None
    rejected_keys: tuple[str, ...] = ()


def validate_external_payload_boundary(
    *,
    interface: ExternalSourceInterfaceSpec,
    payload: Mapping[str, Any],
) -> ExternalSourceValidationResult:
    """Validate one external payload without running clients or mutating state."""

    rejected_keys = _find_forbidden_payload_keys(payload)
    if rejected_keys:
        return ExternalSourceValidationResult(
            accepted=False,
            source_id=interface.source_id,
            source_family=interface.source_family,
            ingress_mode=interface.ingress_mode,
            rejection_reason="forbidden_external_payload_keys",
            rejected_keys=rejected_keys,
        )

    # Build the carrier to prove the exact same validation and copy semantics are usable by callers.
    ExternalPayloadCarrier(interface=interface, payload=dict(payload))
    return ExternalSourceValidationResult(
        accepted=True,
        source_id=interface.source_id,
        source_family=interface.source_family,
        ingress_mode=interface.ingress_mode,
    )


__all__ = [
    "ExternalIngressMode",
    "ExternalPayloadCarrier",
    "ExternalSourceBoundaryError",
    "ExternalSourceFamily",
    "ExternalSourceInterfaceSpec",
    "ExternalSourceValidationResult",
    "validate_external_payload_boundary",
]
