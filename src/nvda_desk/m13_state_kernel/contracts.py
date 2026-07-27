"""Immutable public contract values for the bounded M13 transaction seam."""

from __future__ import annotations

from dataclasses import dataclass


class IdempotencyConflictError(ValueError):
    """A committed scoped key was reused for a different command identity."""


class StateVersionConflictError(ValueError):
    """A fresh command targeted a state version that is no longer current."""


def _require_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class IdempotencyKey:
    """Caller-issued key scoped by command type and consistency-unit identity."""

    value: str
    command_type: str
    consistency_unit_id: str

    def __post_init__(self) -> None:
        _require_non_empty_string(self.value, "idempotency key value")
        _require_non_empty_string(self.command_type, "command_type")
        _require_non_empty_string(self.consistency_unit_id, "consistency_unit_id")


@dataclass(frozen=True, slots=True)
class TransactionCommand:
    """Typed transaction request preserving identity, input and version facts."""

    command_id: str
    idempotency_key: IdempotencyKey
    input_fingerprint: str
    expected_state_version: int
    policy_version: str

    def __post_init__(self) -> None:
        _require_non_empty_string(self.command_id, "command_id")
        if not isinstance(self.idempotency_key, IdempotencyKey):
            raise TypeError("idempotency_key must be an IdempotencyKey")
        _require_non_empty_string(self.input_fingerprint, "input_fingerprint")
        if (
            not isinstance(self.expected_state_version, int)
            or isinstance(self.expected_state_version, bool)
            or self.expected_state_version < 0
        ):
            raise ValueError("expected_state_version must be a non-negative integer")
        _require_non_empty_string(self.policy_version, "policy_version")


@dataclass(frozen=True, slots=True)
class AtomicReceipt:
    """Immutable success truth for one committed owner-declared transaction."""

    receipt_id: str
    result_id: str
    command_id: str
    command_type: str
    consistency_unit_id: str
    idempotency_key: IdempotencyKey
    input_fingerprint: str
    policy_version: str
    prior_state_version: int
    resulting_state_version: int
    sequence: int
    duplicate_replay: bool = False

    def __post_init__(self) -> None:
        _require_non_empty_string(self.receipt_id, "receipt_id")
        _require_non_empty_string(self.result_id, "result_id")
        _require_non_empty_string(self.command_id, "command_id")
        _require_non_empty_string(self.command_type, "command_type")
        _require_non_empty_string(self.consistency_unit_id, "consistency_unit_id")
        if not isinstance(self.idempotency_key, IdempotencyKey):
            raise TypeError("idempotency_key must be an IdempotencyKey")
        if self.command_type != self.idempotency_key.command_type:
            raise ValueError("command_type must match the idempotency key scope")
        if self.consistency_unit_id != self.idempotency_key.consistency_unit_id:
            raise ValueError("consistency_unit_id must match the idempotency key scope")
        _require_non_empty_string(self.input_fingerprint, "input_fingerprint")
        _require_non_empty_string(self.policy_version, "policy_version")
        if type(self.prior_state_version) is not int or self.prior_state_version < 0:
            raise ValueError("prior_state_version must be a non-negative integer")
        if type(self.resulting_state_version) is not int or self.resulting_state_version < 1:
            raise ValueError("resulting_state_version must be a positive integer")
        if self.resulting_state_version != self.prior_state_version + 1:
            raise ValueError("resulting_state_version must advance exactly once")
        if type(self.sequence) is not int or self.sequence < 1:
            raise ValueError("sequence must be a positive integer")
        if type(self.duplicate_replay) is not bool:
            raise TypeError("duplicate_replay must be a bool")
