"""Capital deployment authority contract models."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CAPITAL_DEPLOYMENT_DECISION_DATASCHEMA = (
    "urn:nvda:schema:capital_deployment_authority.decision:1.0.0"
)

_CAPITAL_RECEIPT_OPENING_OR_BROKER_AUTHORITY_KEYS = frozenset(
    {
        "broker_order_id",
        "execution_allowed",
        "opening_authorisation",
        "order_intent_preview",
        "placement_handoff",
        "readiness_state",
    }
)


def _payload_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _payload_keys(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _payload_keys(child)


def _reject_opening_or_broker_authority_payload(value: Any):
    observed = set(_payload_keys(value))
    forbidden = observed & _CAPITAL_RECEIPT_OPENING_OR_BROKER_AUTHORITY_KEYS
    if forbidden:
        joined = ", ".join(sorted(forbidden))
        raise ValueError(
            "capital deployment receipt emitted_output cannot carry opening or "
            f"broker authority keys: {joined}"
        )
    return value


class CapitalDeploymentAuthorityAction(StrEnum):
    """Closed Sequence 9 decision set emitted by capital deployment authority."""

    NO_TRADE = "no_trade"
    REDUCE = "reduce"
    CONTINUE = "continue"
    BLOCK = "block"


class CapitalDeploymentInputTrace(BaseModel):
    """Receipt trace for the inputs consumed by capital deployment authority."""

    model_config = ConfigDict(extra="forbid")

    serial_candidate_id: str
    downstream_pre_deployment_receipt_id: str
    parallel_risk_packet_id: str | None = None
    final_risk_receipt_id: str
    capital_state_snapshot_id: str
    bounded_policy_id: str
    consumed_inputs: list[str] = Field(default_factory=list)


class CapitalDeploymentAuthorityInput(BaseModel):
    """Inputs consumed by downstream capital deployment authority.

    The model consumes preserved serial-candidate truth, downstream
    pre-deployment truth, parallel-risk envelope truth, final-risk truth,
    explicit capital state, bounded policy, coefficient/modifier bounds, and
    temporal/context signals. Serial confidence is accepted only as auditable
    candidate metadata and is not used as a position-size or notional-sizing
    input.
    """

    model_config = ConfigDict(extra="forbid")

    final_risk_action: str
    final_risk_receipt_id: str
    serial_candidate_id: str
    serial_candidate_eligible: bool = True
    serial_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    downstream_pre_deployment_allowed: bool = True
    downstream_pre_deployment_receipt_id: str
    parallel_risk_packet_id: str | None = None
    parallel_risk_envelope_state: str = "broad"
    parallel_risk_hard_blocks: list[str] = Field(default_factory=list)
    parallel_risk_caution_flags: list[str] = Field(default_factory=list)
    coefficient_min_deployable_floor_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    temporal_event_window_active: bool = False
    temporal_event_risk: str = "normal"
    capital_state_snapshot_id: str
    available_capital_usd: float = Field(ge=0.0)
    bounded_policy_id: str
    requested_deployable_pct: float = Field(ge=0.0, le=100.0)
    max_deployable_pct: float = Field(ge=0.0, le=100.0)
    inventory_pct: float = Field(default=0.0, ge=0.0, le=100.0)

    @field_validator(
        "final_risk_action",
        "final_risk_receipt_id",
        "serial_candidate_id",
        "downstream_pre_deployment_receipt_id",
        "capital_state_snapshot_id",
        "bounded_policy_id",
    )
    @classmethod
    def validate_required_token(cls, value: str) -> str:
        """Require trace tokens to be explicit and non-empty."""
        token = str(value).strip()
        if not token:
            raise ValueError("capital deployment authority trace tokens must be non-empty")
        if token == "unknown":
            raise ValueError("capital deployment authority trace tokens must not be 'unknown'")
        return token

    @field_validator("parallel_risk_packet_id")
    @classmethod
    def validate_optional_trace_token(cls, value: str | None) -> str | None:
        """Require optional trace tokens to be non-empty when present."""
        if value is None:
            return None
        token = str(value).strip()
        if not token:
            raise ValueError("optional trace tokens must be non-empty when present")
        if token == "unknown":
            raise ValueError("optional trace tokens must not be 'unknown'")
        return token

    @model_validator(mode="after")
    def validate_deployable_floor(self) -> "CapitalDeploymentAuthorityInput":
        """Ensure the coefficient floor does not exceed the risk-authorised cap."""
        if (
            self.coefficient_min_deployable_floor_pct > 0.0
            and self.max_deployable_pct > 0.0
            and self.coefficient_min_deployable_floor_pct > self.max_deployable_pct
        ):
            raise ValueError(
                "coefficient_min_deployable_floor_pct cannot exceed max_deployable_pct"
            )
        return self


class CapitalDeploymentDecision(BaseModel):
    """Auditable downstream capital deployment decision."""

    model_config = ConfigDict(extra="forbid")

    action: CapitalDeploymentAuthorityAction
    authorised_deployable_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    authorised_notional_usd: float = Field(default=0.0, ge=0.0)
    consumed_inputs: list[str] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    input_trace: CapitalDeploymentInputTrace | None = None
    capital_deployment_receipt_id: str | None = None


class CapitalDeploymentReceipt(BaseModel):
    """Receipt tying one capital deployment authority decision to its inputs."""

    model_config = ConfigDict(extra="forbid")

    receipt_id: str
    decision: CapitalDeploymentDecision
    input_trace: CapitalDeploymentInputTrace
    emitted_output: dict[str, Any]
    placement_authority_opened: bool = False

    @field_validator("emitted_output", mode="before")
    @classmethod
    def reject_opening_or_broker_authority_payload(cls, value):
        """Keep receipt output bounded to capital deployment authority output."""
        return _reject_opening_or_broker_authority_payload(value)
