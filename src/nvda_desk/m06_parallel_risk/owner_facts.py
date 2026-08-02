"""Exact owner-issued facts consumed by the M06 parallel-risk evaluator."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.contracts.prepared_data import SourceCaptureReference

OwnerRiskCondition = Literal["observe", "caution", "block"]


def _require_utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


def _require_hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _material(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode="python", exclude={"fact_id", "semantic_fingerprint"})


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        return _require_utc(value, "owner_fact_time_must_be_utc").isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("decimal_must_be_finite")
        return "0" if value == 0 else format(value.normalize(), "f")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def owner_fact_fingerprint(value: Any) -> str:
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_owner_fact(model_type: type[BaseModel], prefix: str, payload: dict[str, Any]):
    provisional = model_type.model_construct(
        **payload, fact_id="pending", semantic_fingerprint="0" * 64
    )
    fp = owner_fact_fingerprint(_material(provisional))
    return model_type.model_validate(
        {
            **payload,
            "fact_id": f"{prefix}:{fp[:24]}",
            "semantic_fingerprint": fp,
        }
    )


class _OwnerFactBase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    fact_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    owner_policy_version: str = Field(min_length=1)
    as_of_utc: datetime
    valid_until_utc: datetime
    authority_references: tuple[str, ...] = Field(min_length=1)
    semantic_fingerprint: str

    @field_validator("as_of_utc", "valid_until_utc")
    @classmethod
    def _times(cls, value: datetime) -> datetime:
        return _require_utc(value, "owner_fact_time_must_be_utc")

    @field_validator("authority_references", mode="before")
    @classmethod
    def _references(cls, value: Any) -> tuple[str, ...]:
        return tuple(sorted(str(item) for item in value))

    def _validate_common(self, prefix: str) -> None:
        if self.valid_until_utc < self.as_of_utc:
            raise ValueError("owner_fact_validity_precedes_as_of")
        if len(self.authority_references) != len(set(self.authority_references)):
            raise ValueError("duplicate_owner_fact_authority_reference")
        expected = owner_fact_fingerprint(_material(self))
        if self.semantic_fingerprint != expected:
            raise ValueError("owner_fact_fingerprint_mismatch")
        if self.fact_id != f"{prefix}:{expected[:24]}":
            raise ValueError("owner_fact_id_mismatch")

    def is_current_at(self, effective_at_utc: datetime) -> bool:
        effective = _require_utc(effective_at_utc, "owner_fact_effective_time_must_be_utc")
        return self.as_of_utc <= effective <= self.valid_until_utc


class ConcentrationOwnerFact(_OwnerFactBase):
    """M11-issued portfolio concentration fact with explicit owner limits."""

    owner_module: Literal["M11"] = "M11"
    portfolio_snapshot_id: str = Field(min_length=1)
    portfolio_snapshot_fingerprint: str
    portfolio_state_version: int = Field(ge=1)
    symbol: Literal["NVDA"] = "NVDA"
    position_market_value: Decimal = Field(ge=Decimal("0"))
    portfolio_gross_market_value: Decimal = Field(gt=Decimal("0"))
    concentration_ratio: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    warning_ratio: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    block_ratio: Decimal = Field(gt=Decimal("0"), le=Decimal("1"))
    condition: OwnerRiskCondition

    @model_validator(mode="after")
    def _law(self) -> "ConcentrationOwnerFact":
        _require_hash(self.portfolio_snapshot_fingerprint, "portfolio_snapshot_fingerprint_invalid")
        if not all(item.startswith("m11:") for item in self.authority_references):
            raise ValueError("concentration_fact_requires_m11_authority")
        if self.warning_ratio >= self.block_ratio:
            raise ValueError("concentration_owner_limit_order_invalid")
        if (
            self.concentration_ratio
            != self.position_market_value / self.portfolio_gross_market_value
        ):
            raise ValueError("concentration_ratio_mismatch")
        expected_condition: OwnerRiskCondition = (
            "block"
            if self.concentration_ratio >= self.block_ratio
            else "caution" if self.concentration_ratio >= self.warning_ratio else "observe"
        )
        if self.condition != expected_condition:
            raise ValueError("concentration_condition_mismatch")
        self._validate_common("concentration-owner-fact")
        return self


class InventoryStressOwnerFact(_OwnerFactBase):
    """M11-issued position availability fact with exact snapshot lineage."""

    owner_module: Literal["M11"] = "M11"
    portfolio_snapshot_id: str = Field(min_length=1)
    portfolio_snapshot_fingerprint: str
    portfolio_state_version: int = Field(ge=1)
    position_id: Literal["position:NVDA:long"] = "position:NVDA:long"
    position_quantity: Decimal = Field(gt=Decimal("0"))
    unencumbered_quantity: Decimal = Field(ge=Decimal("0"))
    coverage_ratio: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    warning_coverage_ratio: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    block_coverage_ratio: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    condition: OwnerRiskCondition

    @model_validator(mode="after")
    def _law(self) -> "InventoryStressOwnerFact":
        _require_hash(self.portfolio_snapshot_fingerprint, "portfolio_snapshot_fingerprint_invalid")
        if not all(item.startswith("m11:") for item in self.authority_references):
            raise ValueError("inventory_fact_requires_m11_authority")
        if self.unencumbered_quantity > self.position_quantity:
            raise ValueError("unencumbered_quantity_exceeds_position")
        if self.block_coverage_ratio >= self.warning_coverage_ratio:
            raise ValueError("inventory_owner_limit_order_invalid")
        if self.coverage_ratio != self.unencumbered_quantity / self.position_quantity:
            raise ValueError("inventory_coverage_ratio_mismatch")
        expected_condition: OwnerRiskCondition = (
            "block"
            if self.coverage_ratio <= self.block_coverage_ratio
            else "caution" if self.coverage_ratio <= self.warning_coverage_ratio else "observe"
        )
        if self.condition != expected_condition:
            raise ValueError("inventory_condition_mismatch")
        self._validate_common("inventory-owner-fact")
        return self


class LiquidityOwnerFact(_OwnerFactBase):
    """M01/provider-issued executable-liquidity coverage fact."""

    owner_module: Literal["M01"] = "M01"
    provider_id: str = Field(min_length=1)
    symbol: Literal["NVDA"] = "NVDA"
    source_capture_refs: tuple[SourceCaptureReference, ...] = Field(min_length=1)
    required_notional: Decimal = Field(gt=Decimal("0"))
    available_notional: Decimal = Field(ge=Decimal("0"))
    coverage_ratio: Decimal = Field(ge=Decimal("0"))
    warning_coverage_ratio: Decimal = Field(ge=Decimal("0"))
    block_coverage_ratio: Decimal = Field(ge=Decimal("0"))
    condition: OwnerRiskCondition

    @field_validator("source_capture_refs", mode="before")
    @classmethod
    def _captures(cls, value: Any) -> tuple[SourceCaptureReference, ...]:
        return tuple(
            sorted(
                (
                    SourceCaptureReference.model_validate(
                        item.model_dump(mode="python") if isinstance(item, BaseModel) else item
                    )
                    for item in value
                ),
                key=lambda item: (item.capture_id, item.source_artifact_id),
            )
        )

    @classmethod
    def issue(
        cls,
        *,
        provider_id: str,
        source_capture_refs: tuple[SourceCaptureReference, ...],
        as_of_utc: datetime,
        valid_until_utc: datetime,
        required_notional: Decimal,
        available_notional: Decimal,
        warning_coverage_ratio: Decimal,
        block_coverage_ratio: Decimal,
        owner_policy_version: str,
    ) -> "LiquidityOwnerFact":
        governed_refs = tuple(
            sorted(
                (
                    SourceCaptureReference.model_validate(item.model_dump(mode="python"))
                    for item in source_capture_refs
                ),
                key=lambda item: (item.capture_id, item.source_artifact_id),
            )
        )
        coverage_ratio = available_notional / required_notional
        condition: OwnerRiskCondition = (
            "block"
            if coverage_ratio <= block_coverage_ratio
            else "caution" if coverage_ratio <= warning_coverage_ratio else "observe"
        )
        payload = {
            "owner_policy_version": owner_policy_version,
            "as_of_utc": as_of_utc,
            "valid_until_utc": valid_until_utc,
            "authority_references": tuple(
                sorted(f"m01:{item.capture_id}:{item.input_fingerprint}" for item in governed_refs)
            ),
            "provider_id": provider_id,
            "source_capture_refs": governed_refs,
            "required_notional": required_notional,
            "available_notional": available_notional,
            "coverage_ratio": coverage_ratio,
            "warning_coverage_ratio": warning_coverage_ratio,
            "block_coverage_ratio": block_coverage_ratio,
            "condition": condition,
        }
        return build_owner_fact(cls, "liquidity-owner-fact", payload)

    @model_validator(mode="after")
    def _law(self) -> "LiquidityOwnerFact":
        if not all(item.startswith("m01:") for item in self.authority_references):
            raise ValueError("liquidity_fact_requires_m01_authority")
        if self.block_coverage_ratio >= self.warning_coverage_ratio:
            raise ValueError("liquidity_owner_limit_order_invalid")
        if self.coverage_ratio != self.available_notional / self.required_notional:
            raise ValueError("liquidity_coverage_ratio_mismatch")
        expected_condition: OwnerRiskCondition = (
            "block"
            if self.coverage_ratio <= self.block_coverage_ratio
            else "caution" if self.coverage_ratio <= self.warning_coverage_ratio else "observe"
        )
        if self.condition != expected_condition:
            raise ValueError("liquidity_condition_mismatch")
        capture_refs = {
            f"m01:{item.capture_id}:{item.input_fingerprint}" for item in self.source_capture_refs
        }
        if not capture_refs.issubset(set(self.authority_references)):
            raise ValueError("liquidity_source_capture_authority_missing")
        self._validate_common("liquidity-owner-fact")
        return self


class ParallelRiskOwnerFacts(BaseModel):
    """Optional exact owner-fact bundle for M06's three previously unknown families."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    concentration: ConcentrationOwnerFact | None = None
    inventory_stress: InventoryStressOwnerFact | None = None
    liquidity: LiquidityOwnerFact | None = None
    semantic_fingerprint: str

    @field_validator("concentration", mode="before")
    @classmethod
    def _concentration(cls, value: Any) -> ConcentrationOwnerFact | None:
        if value is None:
            return None
        return ConcentrationOwnerFact.model_validate(
            value.model_dump(mode="python") if isinstance(value, BaseModel) else value
        )

    @field_validator("inventory_stress", mode="before")
    @classmethod
    def _inventory(cls, value: Any) -> InventoryStressOwnerFact | None:
        if value is None:
            return None
        return InventoryStressOwnerFact.model_validate(
            value.model_dump(mode="python") if isinstance(value, BaseModel) else value
        )

    @field_validator("liquidity", mode="before")
    @classmethod
    def _liquidity(cls, value: Any) -> LiquidityOwnerFact | None:
        if value is None:
            return None
        return LiquidityOwnerFact.model_validate(
            value.model_dump(mode="python") if isinstance(value, BaseModel) else value
        )

    @model_validator(mode="after")
    def _law(self) -> "ParallelRiskOwnerFacts":
        expected = owner_fact_fingerprint(
            self.model_dump(mode="python", exclude={"semantic_fingerprint"})
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("parallel_risk_owner_facts_fingerprint_mismatch")
        return self

    @classmethod
    def build(
        cls,
        *,
        concentration: ConcentrationOwnerFact | None = None,
        inventory_stress: InventoryStressOwnerFact | None = None,
        liquidity: LiquidityOwnerFact | None = None,
    ) -> "ParallelRiskOwnerFacts":
        payload = {
            "concentration": concentration,
            "inventory_stress": inventory_stress,
            "liquidity": liquidity,
        }
        return cls.model_validate(
            {**payload, "semantic_fingerprint": owner_fact_fingerprint(payload)}
        )


__all__ = [
    "ConcentrationOwnerFact",
    "InventoryStressOwnerFact",
    "LiquidityOwnerFact",
    "OwnerRiskCondition",
    "ParallelRiskOwnerFacts",
    "build_owner_fact",
    "owner_fact_fingerprint",
]
