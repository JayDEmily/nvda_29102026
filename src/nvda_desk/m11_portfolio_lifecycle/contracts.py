"""Immutable M11 K16/K17 portfolio lifecycle contracts."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint

LIFECYCLE_POLICY_VERSION: Final = "m11.lifecycle.v1"


def _utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


def _hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _material(model: BaseModel, *, exclude: set[str]) -> dict[str, Any]:
    return model.model_dump(mode="python", exclude=exclude)


class PositionState(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    position_id: Literal["position:NVDA:long"] = "position:NVDA:long"
    contract_version: Literal["1.0.0"] = "1.0.0"
    symbol: Literal["NVDA"] = "NVDA"
    side: Literal["long"] = "long"
    quantity: Decimal = Field(gt=Decimal("0"))
    average_cost: Decimal = Field(gt=Decimal("0"))
    cost_basis: Decimal = Field(gt=Decimal("0"))
    fill_ids: tuple[str, ...]
    execution_receipt_ids: tuple[str, ...]
    execution_receipt_fingerprints: tuple[str, ...]
    opened_at_utc: datetime
    updated_at_utc: datetime
    state_version: int = Field(ge=1)
    paper_only: Literal[True] = True
    live_account_truth: Literal[False] = False
    durable_commit_proven: bool = False
    semantic_fingerprint: str

    @field_validator("opened_at_utc", "updated_at_utc")
    @classmethod
    def _times(cls, value: datetime) -> datetime:
        return _utc(value, "position_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "PositionState":
        if self.updated_at_utc < self.opened_at_utc:
            raise ValueError("position_update_precedes_open")
        if not self.fill_ids or len(set(self.fill_ids)) != len(self.fill_ids):
            raise ValueError("fill_ids_must_be_nonempty_unique")
        if len(self.execution_receipt_ids) != len(self.fill_ids):
            raise ValueError("execution_receipt_lineage_count_mismatch")
        if len(self.execution_receipt_fingerprints) != len(self.fill_ids):
            raise ValueError("execution_receipt_fingerprint_count_mismatch")
        if len(set(self.execution_receipt_ids)) != len(self.execution_receipt_ids):
            raise ValueError("execution_receipt_ids_must_be_unique")
        for fp in self.execution_receipt_fingerprints:
            _hash(fp, "execution_receipt_fingerprint_invalid")
        if self.average_cost != self.cost_basis / self.quantity:
            raise ValueError("position_cost_basis_mismatch")
        if self.durable_commit_proven and self.live_account_truth:
            raise ValueError("paper_position_cannot_claim_live_account_truth")
        expected = semantic_fingerprint(_material(self, exclude={"semantic_fingerprint"}))
        if self.semantic_fingerprint != expected:
            raise ValueError("position_state_fingerprint_mismatch")
        return self


class PortfolioSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    snapshot_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    portfolio_id: Literal["portfolio:NVDA"] = "portfolio:NVDA"
    positions: tuple[PositionState, ...]
    position_ids: tuple[str, ...]
    state_version: int = Field(ge=0)
    as_of_utc: datetime
    durability: Literal["non_durable_in_memory", "durable_sqlite"] = "non_durable_in_memory"
    live_account_truth: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("as_of_utc")
    @classmethod
    def _asof(cls, value: datetime) -> datetime:
        return _utc(value, "portfolio_snapshot_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "PortfolioSnapshot":
        positions = tuple(
            PositionState.model_validate(p.model_dump(mode="python")) for p in self.positions
        )
        if tuple(p.position_id for p in positions) != self.position_ids:
            raise ValueError("portfolio_position_ids_mismatch")
        if tuple(sorted(self.position_ids)) != self.position_ids or len(
            set(self.position_ids)
        ) != len(self.position_ids):
            raise ValueError("portfolio_position_order_or_uniqueness_invalid")
        if any(p.state_version != self.state_version for p in positions):
            raise ValueError("position_state_version_must_match_portfolio")
        if any(p.updated_at_utc > self.as_of_utc for p in positions):
            raise ValueError("portfolio_snapshot_precedes_position_update")
        expected_durable = self.durability == "durable_sqlite"
        if any(p.durable_commit_proven != expected_durable for p in positions):
            raise ValueError("portfolio_position_durability_mismatch")
        expected = semantic_fingerprint(
            _material(self, exclude={"snapshot_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("portfolio_snapshot_fingerprint_mismatch")
        if self.snapshot_id != f"portfolio-snapshot:{expected[:24]}":
            raise ValueError("portfolio_snapshot_id_mismatch")
        return self


class LifecycleDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    decision_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    policy_version: Literal["m11.lifecycle.v1"] = LIFECYCLE_POLICY_VERSION
    snapshot_id: str = Field(min_length=1)
    snapshot_fingerprint: str
    snapshot_state_version: int = Field(ge=1)
    position_id: Literal["position:NVDA:long"]
    position_fingerprint: str
    position_quantity: Decimal = Field(gt=Decimal("0"))
    action: Literal["hold", "trim", "close"]
    quantity: Decimal | None
    reasons: tuple[str, ...]
    decided_at_utc: datetime
    broker_execution_allowed: Literal[False] = False
    capital_recomputation_allowed: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("decided_at_utc")
    @classmethod
    def _time(cls, value: datetime) -> datetime:
        return _utc(value, "lifecycle_decision_time_must_be_utc")

    @model_validator(mode="after")
    def _law(self) -> "LifecycleDecision":
        _hash(self.snapshot_fingerprint, "snapshot_fingerprint_invalid")
        _hash(self.position_fingerprint, "position_fingerprint_invalid")
        if not self.reasons or any(not isinstance(r, str) or not r.strip() for r in self.reasons):
            raise ValueError("lifecycle_reasons_must_be_nonempty")
        if self.action == "hold" and self.quantity is not None:
            raise ValueError("hold_carries_no_quantity")
        if self.action == "trim" and (
            self.quantity is None or self.quantity <= 0 or self.quantity >= self.position_quantity
        ):
            raise ValueError("trim_quantity_invalid")
        if self.action == "close" and self.quantity != self.position_quantity:
            raise ValueError("close_quantity_must_equal_position")
        expected = semantic_fingerprint(
            _material(self, exclude={"decision_id", "semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("lifecycle_decision_fingerprint_mismatch")
        if self.decision_id != f"lifecycle-decision:{expected[:24]}":
            raise ValueError("lifecycle_decision_id_mismatch")
        return self


class FillReconciliationReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    receipt_id: str = Field(min_length=1)
    execution_receipt_id: str = Field(min_length=1)
    execution_receipt_fingerprint: str
    fill_id: str = Field(min_length=1)
    snapshot: PortfolioSnapshot
    snapshot_id: str = Field(min_length=1)
    snapshot_fingerprint: str
    atomic_receipt_id: str = Field(min_length=1)
    atomic_command_id: str = Field(min_length=1)
    atomic_prior_state_version: int = Field(ge=0)
    atomic_resulting_state_version: int = Field(ge=1)
    atomic_sequence: int = Field(ge=1)
    duplicate_replay: bool = False
    durability: Literal["non_durable_in_memory", "durable_sqlite"] = "non_durable_in_memory"
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _law(self) -> "FillReconciliationReceipt":
        _hash(self.execution_receipt_fingerprint, "execution_receipt_fingerprint_invalid")
        _hash(self.snapshot_fingerprint, "snapshot_fingerprint_invalid")
        snap = PortfolioSnapshot.model_validate(self.snapshot.model_dump(mode="python"))
        if (self.snapshot_id, self.snapshot_fingerprint) != (
            snap.snapshot_id,
            snap.semantic_fingerprint,
        ):
            raise ValueError("fill_receipt_snapshot_binding_mismatch")
        if self.atomic_resulting_state_version != self.atomic_prior_state_version + 1:
            raise ValueError("fill_atomic_version_mismatch")
        if snap.state_version != self.atomic_resulting_state_version:
            raise ValueError("fill_snapshot_state_version_mismatch")
        if len(snap.positions) != 1:
            raise ValueError("fill_snapshot_must_contain_position")
        position = snap.positions[0]
        if position.state_version != self.atomic_resulting_state_version:
            raise ValueError("fill_position_state_version_mismatch")
        if not (
            position.fill_ids[-1] == self.fill_id
            and position.execution_receipt_ids[-1] == self.execution_receipt_id
            and position.execution_receipt_fingerprints[-1] == self.execution_receipt_fingerprint
        ):
            raise ValueError("fill_receipt_lineage_binding_mismatch")
        expected = semantic_fingerprint(
            _material(self, exclude={"receipt_id", "semantic_fingerprint", "duplicate_replay"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("fill_reconciliation_receipt_fingerprint_mismatch")
        if self.receipt_id != f"fill-reconciliation:{expected[:24]}":
            raise ValueError("fill_reconciliation_receipt_id_mismatch")
        return self


class CloseReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    receipt_id: str = Field(min_length=1)
    decision: LifecycleDecision
    decision_id: str = Field(min_length=1)
    decision_fingerprint: str
    prior_position: PositionState
    resulting_position: PositionState | None
    snapshot: PortfolioSnapshot
    atomic_receipt_id: str = Field(min_length=1)
    atomic_command_id: str = Field(min_length=1)
    atomic_prior_state_version: int = Field(ge=0)
    atomic_resulting_state_version: int = Field(ge=1)
    atomic_sequence: int = Field(ge=1)
    duplicate_replay: bool = False
    durability: Literal["non_durable_in_memory", "durable_sqlite"] = "non_durable_in_memory"
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _law(self) -> "CloseReceipt":
        decision = LifecycleDecision.model_validate(self.decision.model_dump(mode="python"))
        prior = PositionState.model_validate(self.prior_position.model_dump(mode="python"))
        if (self.decision_id, self.decision_fingerprint) != (
            decision.decision_id,
            decision.semantic_fingerprint,
        ):
            raise ValueError("close_receipt_decision_binding_mismatch")
        if prior.semantic_fingerprint != decision.position_fingerprint:
            raise ValueError("close_receipt_prior_position_mismatch")
        if prior.position_id != decision.position_id:
            raise ValueError("close_receipt_prior_position_id_mismatch")
        if prior.quantity != decision.position_quantity:
            raise ValueError("close_receipt_prior_quantity_mismatch")
        if decision.action == "close" and self.resulting_position is not None:
            raise ValueError("close_must_remove_position")
        if decision.action == "trim" and self.resulting_position is None:
            raise ValueError("trim_must_preserve_position")
        if decision.action == "hold":
            raise ValueError("hold_cannot_create_close_receipt")
        snapshot = PortfolioSnapshot.model_validate(self.snapshot.model_dump(mode="python"))
        if self.atomic_resulting_state_version != self.atomic_prior_state_version + 1:
            raise ValueError("close_atomic_version_mismatch")
        if decision.snapshot_state_version != self.atomic_prior_state_version:
            raise ValueError("close_decision_prior_version_mismatch")
        if prior.state_version != self.atomic_prior_state_version:
            raise ValueError("close_prior_position_version_mismatch")
        if snapshot.state_version != self.atomic_resulting_state_version:
            raise ValueError("close_snapshot_resulting_version_mismatch")
        if snapshot.as_of_utc != decision.decided_at_utc:
            raise ValueError("close_snapshot_time_mismatch")
        if self.atomic_command_id != f"m11.lifecycle:{decision.decision_id}":
            raise ValueError("close_atomic_command_binding_mismatch")
        if decision.action == "close":
            if snapshot.positions or snapshot.position_ids:
                raise ValueError("close_snapshot_must_be_empty")
        else:
            assert decision.action == "trim"
            assert decision.quantity is not None
            result = PositionState.model_validate(self.resulting_position.model_dump(mode="python"))
            if result.position_id != prior.position_id:
                raise ValueError("trim_position_identity_changed")
            if result.quantity != prior.quantity - decision.quantity:
                raise ValueError("trim_resulting_quantity_mismatch")
            if result.average_cost != prior.average_cost:
                raise ValueError("trim_average_cost_changed")
            if result.cost_basis != prior.average_cost * result.quantity:
                raise ValueError("trim_cost_basis_mismatch")
            if (
                result.fill_ids,
                result.execution_receipt_ids,
                result.execution_receipt_fingerprints,
                result.opened_at_utc,
            ) != (
                prior.fill_ids,
                prior.execution_receipt_ids,
                prior.execution_receipt_fingerprints,
                prior.opened_at_utc,
            ):
                raise ValueError("trim_lineage_changed")
            if result.updated_at_utc != decision.decided_at_utc:
                raise ValueError("trim_update_time_mismatch")
            if result.state_version != self.atomic_resulting_state_version:
                raise ValueError("trim_resulting_version_mismatch")
            if snapshot.positions != (result,) or snapshot.position_ids != (result.position_id,):
                raise ValueError("trim_snapshot_position_mismatch")
        expected = semantic_fingerprint(
            _material(self, exclude={"receipt_id", "semantic_fingerprint", "duplicate_replay"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("close_receipt_fingerprint_mismatch")
        if self.receipt_id != f"close-receipt:{expected[:24]}":
            raise ValueError("close_receipt_id_mismatch")
        return self
