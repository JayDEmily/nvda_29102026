"""Contracts for governed playbook registry and metadata receipts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PLAYBOOK_FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "authorised_notional_usd",
        "authorised_deployable_percentage",
        "broker_order",
        "broker_placement",
        "capital_deployment",
        "coefficient_authority",
        "cognition_playbook_action",
        "cognition_playbook_decision",
        "cognition_runtime_service",
        "downstream_shell_request_contract",
        "execution_expression_service",
        "external_network_client",
        "hidden_coefficient_ownership",
        "import_registry_row_contract",
        "live_order_execution",
        "playbook_eligibility_service",
        "playbook_family_candidate",
        "raw_source",
        "raw_source_ingestion",
        "replay_compare_service",
        "review_eligibility_surface",
        "review_failure_class",
        "setup_variant_candidate",
        "strategy_mutation",
    }
)


def _normalise_identifier(value: str, *, field_name: str) -> str:
    normalised = value.strip()
    if not normalised:
        raise ValueError(f"{field_name} must not be blank")
    return normalised


def _find_forbidden_authority_key(value: Any, *, path: str = "root") -> str | None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in PLAYBOOK_FORBIDDEN_AUTHORITY_KEYS:
                return f"{path}.{key_text}"
            found = _find_forbidden_authority_key(nested, path=f"{path}.{key_text}")
            if found:
                return found
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, nested in enumerate(value):
            found = _find_forbidden_authority_key(nested, path=f"{path}[{index}]")
            if found:
                return found
    return None


def reject_hidden_playbook_authority(value: Any) -> Any:
    """Reject payloads that try to smuggle closed authority into playbook material."""

    found = _find_forbidden_authority_key(value)
    if found:
        raise ValueError(f"hidden playbook authority key rejected: {found}")
    return value


def playbook_payload_fingerprint(payload: Mapping[str, Any]) -> str:
    """Return one deterministic fingerprint for playbook registry payloads."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class PlaybookEligibilityConstraint(BaseModel):
    """One bounded eligibility constraint owned by playbook metadata."""

    model_config = ConfigDict(extra="forbid")
    constraint_id: str
    constraint_type: str
    allowed_values: tuple[str, ...] = Field(default_factory=tuple)
    required: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("constraint_id", "constraint_type")
    @classmethod
    def _normalise_identifiers(cls, value: str) -> str:
        return _normalise_identifier(value, field_name="playbook constraint identifier")

    @field_validator("allowed_values")
    @classmethod
    def _normalise_allowed_values(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        normalised = tuple(
            _normalise_identifier(value, field_name="allowed_values") for value in values
        )
        if len(set(normalised)) != len(normalised):
            raise ValueError("duplicate allowed value")
        return normalised

    @field_validator("metadata")
    @classmethod
    def _reject_hidden_metadata_authority(cls, value: dict[str, Any]) -> dict[str, Any]:
        reject_hidden_playbook_authority(value)
        return deepcopy(dict(value))


class PlaybookDefinition(BaseModel):
    """One governed playbook definition from the playbook-library registry."""

    model_config = ConfigDict(extra="forbid")
    playbook_id: str
    setup_family: str
    setup_variant_ids: tuple[str, ...]
    eligibility_constraints: tuple[PlaybookEligibilityConstraint, ...] = Field(
        default_factory=tuple
    )
    selection_metadata: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True

    @field_validator("playbook_id", "setup_family")
    @classmethod
    def _normalise_identifiers(cls, value: str) -> str:
        return _normalise_identifier(value, field_name="playbook identifier")

    @field_validator("setup_variant_ids")
    @classmethod
    def _validate_setup_variant_ids(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        normalised = tuple(
            _normalise_identifier(value, field_name="setup_variant_id") for value in values
        )
        if not normalised:
            raise ValueError("setup_variant_ids must not be empty")
        duplicates = sorted({value for value in normalised if normalised.count(value) > 1})
        if duplicates:
            raise ValueError(f"duplicate setup_variant_id: {duplicates[0]}")
        return normalised

    @field_validator("selection_metadata")
    @classmethod
    def _reject_hidden_selection_authority(cls, value: dict[str, Any]) -> dict[str, Any]:
        reject_hidden_playbook_authority(value)
        return deepcopy(dict(value))

    @model_validator(mode="after")
    def _constraints_are_unique(self) -> "PlaybookDefinition":
        constraint_ids = tuple(
            constraint.constraint_id for constraint in self.eligibility_constraints
        )
        duplicates = sorted({value for value in constraint_ids if constraint_ids.count(value) > 1})
        if duplicates:
            raise ValueError(f"duplicate eligibility constraint_id: {duplicates[0]}")
        return self


class PlaybookMetadataReceipt(BaseModel):
    """Proofable playbook metadata receipt emitted without capital or broker authority."""

    model_config = ConfigDict(extra="forbid")
    receipt_id: str
    registry_id: str
    playbook_id: str
    setup_family: str
    setup_variant_id: str
    eligibility_constraint_ids: tuple[str, ...] = Field(default_factory=tuple)
    selection_metadata: dict[str, Any] = Field(default_factory=dict)
    source_registry_fingerprint: str

    @field_validator("receipt_id", "registry_id", "playbook_id", "setup_family", "setup_variant_id")
    @classmethod
    def _normalise_identifiers(cls, value: str) -> str:
        return _normalise_identifier(value, field_name="playbook metadata receipt identifier")

    @field_validator("selection_metadata")
    @classmethod
    def _reject_hidden_selection_authority(cls, value: dict[str, Any]) -> dict[str, Any]:
        reject_hidden_playbook_authority(value)
        return deepcopy(dict(value))
