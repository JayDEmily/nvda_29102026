"""M09-owned immutable contracts for final-risk and fresh-capital authority."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal, ROUND_FLOOR
from hashlib import sha256
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

FinalRiskAction = Literal["eligible_for_capital_assessment", "stand_down"]
CapitalAction = Literal["block", "no_trade", "reduce", "continue"]

FINAL_RISK_JOIN_POLICY_VERSION: Final = "m09.final-risk-join.v1"
CAPITAL_DEPLOYMENT_POLICY_VERSION: Final = "m09.capital-policy.v1"
CLOSED_AUTHORITY_CLASSES: Final[tuple[str, ...]] = (
    "broker_order",
    "execution",
    "position_inventory",
    "lifecycle",
    "durable_transaction",
    "replay",
)


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        if value == 0:
            return "0"
        return format(value.normalize(), "f")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    """Return a deterministic SHA-256 fingerprint for semantic material."""

    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _require_hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _require_utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


def _normalise_texts(values: tuple[str, ...], reason: str) -> tuple[str, ...]:
    if any(not value for value in values):
        raise ValueError(reason)
    if values != tuple(sorted(set(values))):
        raise ValueError(reason)
    return values


class FinalRiskJoinPolicy(BaseModel):
    """Versioned categorical policy for the one lawful M09 K11 join."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy_version: Literal["m09.final-risk-join.v1"] = FINAL_RISK_JOIN_POLICY_VERSION
    cautions_prohibit: bool = False

    @property
    def policy_fingerprint(self) -> str:
        return semantic_fingerprint(self.model_dump(mode="python"))


class CapitalDeploymentPolicy(BaseModel):
    """Versioned bounded sizing policy owned by M09 K14."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy_version: Literal["m09.capital-policy.v1"] = CAPITAL_DEPLOYMENT_POLICY_VERSION
    target_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    hard_max_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    caution_multiplier: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    rounding_quantum: Decimal = Field(gt=Decimal("0"), le=Decimal("100"))

    @property
    def policy_fingerprint(self) -> str:
        return semantic_fingerprint(self.model_dump(mode="python"))


class CapitalState(BaseModel):
    """Immutable versioned capital snapshot admitted for one M09 decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    state_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
    state_version: int = Field(ge=0)
    effective_at_utc: datetime
    available_capital: Decimal = Field(ge=Decimal("0"))
    reserved_capital: Decimal = Field(ge=Decimal("0"))
    max_fresh_deployable_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    source_authority_ref: str = Field(min_length=1)
    semantic_fingerprint: str

    @field_validator("effective_at_utc")
    @classmethod
    def _effective_at_utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "capital_state_effective_at_must_be_utc")

    @model_validator(mode="after")
    def _validate_law(self) -> "CapitalState":
        material = self.model_dump(mode="python")
        material.pop("semantic_fingerprint")
        if self.semantic_fingerprint != semantic_fingerprint(material):
            raise ValueError("capital_state_fingerprint_mismatch")
        return self

    @classmethod
    def create(
        cls,
        *,
        state_id: str,
        account_id: str,
        state_version: int,
        effective_at_utc: datetime,
        available_capital: Decimal,
        reserved_capital: Decimal,
        max_fresh_deployable_pct: Decimal,
        source_authority_ref: str,
    ) -> "CapitalState":
        material = {
            "state_id": state_id,
            "account_id": account_id,
            "state_version": state_version,
            "effective_at_utc": effective_at_utc,
            "available_capital": available_capital,
            "reserved_capital": reserved_capital,
            "max_fresh_deployable_pct": max_fresh_deployable_pct,
            "source_authority_ref": source_authority_ref,
        }
        return cls(**material, semantic_fingerprint=semantic_fingerprint(material))


class FinalRiskDecision(BaseModel):
    """Immutable K11 categorical join of exact M05 and M06 owner products."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    final_decision_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    action: FinalRiskAction
    policy_version: Literal["m09.final-risk-join.v1"]
    join_policy_fingerprint: str
    cautions_prohibit: bool

    serial_result_id: str | None
    serial_candidate_id: str | None
    serial_candidate_fingerprint: str | None
    serial_context_id: str | None
    serial_context_fingerprint: str | None
    serial_prepared_id: str | None
    serial_prepared_fingerprint: str | None
    serial_expression_id: str | None
    serial_expression_version: str | None
    serial_expression_fingerprint: str | None

    parallel_assessment_id: str | None
    parallel_assessment_fingerprint: str | None
    parallel_input_id: str | None
    parallel_input_fingerprint: str | None
    parallel_prepared_id: str | None
    parallel_prepared_fingerprint: str | None
    parallel_evaluator_version: str | None
    parallel_policy_version: str | None
    parallel_aggregation_version: str | None
    parallel_state: str | None

    hard_blocks: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    missing_authority_reasons: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    capital_authority_granted: Literal[False] = False
    execution_authority_granted: Literal[False] = False
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _validate_law(self) -> "FinalRiskDecision":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("final_risk_foreign_authority_claimed")
        for field_name in (
            "hard_blocks",
            "cautions",
            "unknowns",
            "reasons",
            "conflicts",
            "missing_authority_reasons",
            "limitations",
        ):
            _normalise_texts(getattr(self, field_name), f"{field_name}_must_be_canonical")
        _require_hash(self.join_policy_fingerprint, "join_policy_fingerprint_invalid")
        expected_policy_fingerprint = semantic_fingerprint(
            {
                "policy_version": self.policy_version,
                "cautions_prohibit": self.cautions_prohibit,
            }
        )
        if self.join_policy_fingerprint != expected_policy_fingerprint:
            raise ValueError("join_policy_fingerprint_mismatch")
        if self.parallel_state not in {None, "observe", "caution", "block", "unknown"}:
            raise ValueError("parallel_state_invalid")
        if self.parallel_state == "observe" and (self.cautions or self.hard_blocks or self.unknowns):
            raise ValueError("parallel_observe_state_evidence_mismatch")
        if self.parallel_state == "caution" and (not self.cautions or self.hard_blocks or self.unknowns):
            raise ValueError("parallel_caution_state_evidence_mismatch")
        if self.parallel_state == "block" and not self.hard_blocks:
            raise ValueError("parallel_block_state_requires_hard_block")
        if self.parallel_state == "unknown" and not self.unknowns:
            raise ValueError("parallel_unknown_state_requires_unknown_family")
        for field_name in (
            "serial_candidate_fingerprint",
            "serial_context_fingerprint",
            "serial_prepared_fingerprint",
            "serial_expression_fingerprint",
            "parallel_assessment_fingerprint",
            "parallel_input_fingerprint",
            "parallel_prepared_fingerprint",
        ):
            value = getattr(self, field_name)
            if value is not None:
                _require_hash(value, f"{field_name}_invalid")
        if self.action == "eligible_for_capital_assessment":
            required = (
                self.serial_result_id,
                self.serial_candidate_id,
                self.serial_candidate_fingerprint,
                self.serial_context_id,
                self.serial_context_fingerprint,
                self.serial_prepared_id,
                self.serial_prepared_fingerprint,
                self.serial_expression_id,
                self.serial_expression_version,
                self.serial_expression_fingerprint,
                self.parallel_assessment_id,
                self.parallel_assessment_fingerprint,
                self.parallel_input_id,
                self.parallel_input_fingerprint,
                self.parallel_prepared_id,
                self.parallel_prepared_fingerprint,
                self.parallel_evaluator_version,
                self.parallel_policy_version,
                self.parallel_aggregation_version,
                self.parallel_state,
            )
            if any(value is None or value == "" for value in required):
                raise ValueError("eligible_final_risk_requires_complete_lineage")
            if self.hard_blocks or self.unknowns or self.conflicts or self.missing_authority_reasons:
                raise ValueError("eligible_final_risk_cannot_carry_prohibiting_evidence")
            if self.parallel_state not in {"observe", "caution"}:
                raise ValueError("eligible_final_risk_requires_nonprohibiting_parallel_state")
            if self.cautions and self.cautions_prohibit:
                raise ValueError("eligible_final_risk_caution_policy_mismatch")
            if (
                self.serial_prepared_id != self.parallel_prepared_id
                or self.serial_prepared_fingerprint != self.parallel_prepared_fingerprint
            ):
                raise ValueError("eligible_final_risk_prepared_lineage_mismatch")
        else:
            if not (
                self.reasons
                or self.hard_blocks
                or self.unknowns
                or self.conflicts
                or self.missing_authority_reasons
            ):
                raise ValueError("stand_down_requires_explicit_reason")
        material = self.model_dump(mode="python")
        material.pop("final_decision_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("final_risk_decision_fingerprint_mismatch")
        if self.final_decision_id != f"final-risk.{expected[:20]}":
            raise ValueError("final_risk_decision_id_mismatch")
        return self


class CapitalDeploymentDecision(BaseModel):
    """Immutable K14 bounded fresh-capital action and sizing result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decision_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    action: CapitalAction
    authorised_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    authorised_notional: Decimal = Field(ge=Decimal("0"))
    policy_version: Literal["m09.capital-policy.v1"]
    capital_policy_fingerprint: str
    policy_target_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    policy_hard_max_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    policy_caution_multiplier: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    policy_rounding_quantum: Decimal = Field(gt=Decimal("0"))

    final_decision_id: str
    final_decision_fingerprint: str
    serial_result_id: str | None
    serial_candidate_id: str | None
    serial_candidate_fingerprint: str | None
    parallel_assessment_id: str | None
    parallel_assessment_fingerprint: str | None
    capital_state_id: str
    capital_state_version: int = Field(ge=0)
    capital_state_fingerprint: str
    capital_state_available_capital: Decimal = Field(ge=Decimal("0"))
    capital_state_max_fresh_deployable_pct: Decimal = Field(
        ge=Decimal("0"), le=Decimal("100")
    )
    modifier_receipt_id: str
    modifier_decision_fingerprint: str
    modifier_bundle_id: str
    modifier_bundle_version: str
    modifier_authority_id: str
    modifier_authority_version: str
    modifier_resolution_law_version: str

    reasons: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    placement_authority_granted: Literal[False] = False
    broker_authority_granted: Literal[False] = False
    execution_authority_granted: Literal[False] = False
    position_mutation_authority_granted: Literal[False] = False
    durable_commit_proven: Literal[False] = False
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    semantic_fingerprint: str

    @model_validator(mode="after")
    def _validate_law(self) -> "CapitalDeploymentDecision":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("capital_decision_foreign_authority_claimed")
        _require_hash(self.final_decision_fingerprint, "final_decision_fingerprint_invalid")
        _require_hash(self.capital_policy_fingerprint, "capital_policy_fingerprint_invalid")
        _require_hash(self.capital_state_fingerprint, "capital_state_fingerprint_invalid")
        _require_hash(self.modifier_decision_fingerprint, "modifier_decision_fingerprint_invalid")
        if self.serial_candidate_fingerprint is not None:
            _require_hash(self.serial_candidate_fingerprint, "serial_candidate_fingerprint_invalid")
        if self.parallel_assessment_fingerprint is not None:
            _require_hash(self.parallel_assessment_fingerprint, "parallel_assessment_fingerprint_invalid")
        expected_policy_fingerprint = semantic_fingerprint(
            {
                "policy_version": self.policy_version,
                "target_pct": self.policy_target_pct,
                "hard_max_pct": self.policy_hard_max_pct,
                "caution_multiplier": self.policy_caution_multiplier,
                "rounding_quantum": self.policy_rounding_quantum,
            }
        )
        if self.capital_policy_fingerprint != expected_policy_fingerprint:
            raise ValueError("capital_policy_fingerprint_mismatch")
        bounded_pct = min(
            self.policy_target_pct,
            self.policy_hard_max_pct,
            self.capital_state_max_fresh_deployable_pct,
        )
        if self.authorised_pct > bounded_pct:
            raise ValueError("capital_percentage_exceeds_bound")
        if self.authorised_pct % self.policy_rounding_quantum != 0:
            raise ValueError("capital_percentage_not_on_policy_quantum")
        _normalise_texts(self.reasons, "capital_decision_reasons_must_be_canonical")
        _normalise_texts(self.limitations, "capital_decision_limitations_must_be_canonical")
        if self.action in {"block", "no_trade"} and (
            self.authorised_pct != 0 or self.authorised_notional != 0
        ):
            raise ValueError("zero_authority_action_must_carry_zero_sizing")
        if self.action in {"reduce", "continue"} and (
            self.authorised_pct <= 0 or self.authorised_notional <= 0
        ):
            raise ValueError("positive_authority_action_requires_positive_sizing")
        if self.action == "reduce" and self.authorised_pct >= self.policy_target_pct:
            raise ValueError("reduce_requires_below_target_percentage")
        if self.action == "continue" and self.authorised_pct != self.policy_target_pct:
            raise ValueError("continue_requires_full_target_percentage")
        if self.action == "block" and not self.reasons:
            raise ValueError("blocked_capital_decision_requires_reason")
        expected_notional = (
            self.capital_state_available_capital
            * self.authorised_pct
            / Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
        if self.authorised_notional != expected_notional:
            raise ValueError("capital_notional_does_not_match_bounded_percentage")
        if self.authorised_notional > self.capital_state_available_capital:
            raise ValueError("capital_notional_exceeds_available_capital")
        material = self.model_dump(mode="python")
        material.pop("decision_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("capital_deployment_decision_fingerprint_mismatch")
        if self.decision_id != f"capital-decision.{expected[:20]}":
            raise ValueError("capital_deployment_decision_id_mismatch")
        return self


class CapitalDeploymentReceipt(BaseModel):
    """Immutable K14 evidence for one bounded capital decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    decision_id: str
    decision_fingerprint: str
    final_decision_id: str
    final_decision_fingerprint: str
    capital_state_id: str
    capital_state_fingerprint: str
    capital_state_available_capital: Decimal = Field(ge=Decimal("0"))
    capital_state_max_fresh_deployable_pct: Decimal = Field(
        ge=Decimal("0"), le=Decimal("100")
    )
    modifier_receipt_id: str
    modifier_decision_fingerprint: str
    policy_version: Literal["m09.capital-policy.v1"]
    capital_policy_fingerprint: str
    serial_result_id: str | None
    serial_candidate_id: str | None
    serial_candidate_fingerprint: str | None
    parallel_assessment_id: str | None
    parallel_assessment_fingerprint: str | None
    action: CapitalAction
    authorised_pct: Decimal = Field(ge=Decimal("0"), le=Decimal("100"))
    authorised_notional: Decimal = Field(ge=Decimal("0"))
    reasons: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    emitted_at_utc: datetime
    placement_authority_granted: Literal[False] = False
    broker_authority_granted: Literal[False] = False
    execution_authority_granted: Literal[False] = False
    position_mutation_authority_granted: Literal[False] = False
    durable_commit_proven: Literal[False] = False
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    semantic_fingerprint: str

    @field_validator("emitted_at_utc")
    @classmethod
    def _emitted_at_utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "capital_receipt_emitted_at_must_be_utc")

    @model_validator(mode="after")
    def _validate_law(self) -> "CapitalDeploymentReceipt":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("capital_receipt_foreign_authority_claimed")
        for value, reason in (
            (self.decision_fingerprint, "capital_receipt_decision_fingerprint_invalid"),
            (self.final_decision_fingerprint, "capital_receipt_final_fingerprint_invalid"),
            (self.capital_policy_fingerprint, "capital_receipt_policy_fingerprint_invalid"),
            (self.capital_state_fingerprint, "capital_receipt_state_fingerprint_invalid"),
            (self.modifier_decision_fingerprint, "capital_receipt_modifier_fingerprint_invalid"),
        ):
            _require_hash(value, reason)
        if self.serial_candidate_fingerprint is not None:
            _require_hash(self.serial_candidate_fingerprint, "capital_receipt_serial_fingerprint_invalid")
        if self.parallel_assessment_fingerprint is not None:
            _require_hash(self.parallel_assessment_fingerprint, "capital_receipt_parallel_fingerprint_invalid")
        if self.authorised_pct > self.capital_state_max_fresh_deployable_pct:
            raise ValueError("capital_receipt_percentage_exceeds_state_bound")
        _normalise_texts(self.reasons, "capital_receipt_reasons_must_be_canonical")
        _normalise_texts(self.limitations, "capital_receipt_limitations_must_be_canonical")
        if self.action in {"block", "no_trade"} and (
            self.authorised_pct != 0 or self.authorised_notional != 0
        ):
            raise ValueError("capital_receipt_zero_authority_action_must_carry_zero_sizing")
        if self.action in {"reduce", "continue"} and (
            self.authorised_pct <= 0 or self.authorised_notional <= 0
        ):
            raise ValueError("capital_receipt_positive_action_requires_positive_sizing")
        expected_notional = (
            self.capital_state_available_capital
            * self.authorised_pct
            / Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
        if self.authorised_notional != expected_notional:
            raise ValueError("capital_receipt_notional_mismatch")
        if self.authorised_notional > self.capital_state_available_capital:
            raise ValueError("capital_receipt_notional_exceeds_available_capital")
        material = self.model_dump(mode="python")
        material.pop("receipt_id")
        material.pop("semantic_fingerprint")
        material.pop("emitted_at_utc")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("capital_deployment_receipt_fingerprint_mismatch")
        if self.receipt_id != f"capital-receipt.{expected[:20]}":
            raise ValueError("capital_deployment_receipt_id_mismatch")
        return self
