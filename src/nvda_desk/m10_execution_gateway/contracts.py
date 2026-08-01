"""Immutable M10 K15 placement and execution-evidence contracts."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import ROUND_FLOOR, Decimal
from hashlib import sha256
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PLACEMENT_POLICY_VERSION: Final = "m10.paper-placement.v1"
PAPER_PORT_VERSION: Final = "m10.paper-port.v1"


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("decimal_must_be_finite")
        return "0" if value == 0 else format(value.normalize(), "f")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(k): _canonical(v) for k, v in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


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


def _material(model: BaseModel, *, exclude: set[str]) -> dict[str, Any]:
    return model.model_dump(mode="python", exclude=exclude)


class PlacementPolicy(BaseModel):
    """Closed alpha policy for one paper-only NVDA limit placement."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    policy_version: Literal["m10.paper-placement.v1"] = PLACEMENT_POLICY_VERSION
    symbol: Literal["NVDA"] = "NVDA"
    side: Literal["buy"] = "buy"
    order_type: Literal["limit"] = "limit"
    time_in_force: Literal["day"] = "day"
    adapter_mode: Literal["paper"] = "paper"
    quantity_quantum: Decimal = Field(gt=Decimal("0"))

    @property
    def policy_fingerprint(self) -> str:
        return semantic_fingerprint(self.model_dump(mode="python"))


class PlacementIntent(BaseModel):
    """Exact M09-derived paper placement with no broker or portfolio authority."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    intent_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    capital_receipt_id: str = Field(min_length=1)
    capital_receipt_fingerprint: str
    capital_decision_id: str = Field(min_length=1)
    capital_decision_fingerprint: str
    final_decision_id: str = Field(min_length=1)
    final_decision_fingerprint: str
    capital_state_id: str = Field(min_length=1)
    capital_state_fingerprint: str
    modifier_receipt_id: str = Field(min_length=1)
    modifier_decision_fingerprint: str
    m09_policy_version: str = Field(min_length=1)
    m09_policy_fingerprint: str
    serial_result_id: str = Field(min_length=1)
    serial_candidate_id: str = Field(min_length=1)
    serial_candidate_fingerprint: str
    parallel_assessment_id: str | None
    parallel_assessment_fingerprint: str | None
    capital_action: Literal["continue", "reduce"]
    authorised_pct: Decimal = Field(gt=Decimal("0"))
    authorised_notional: Decimal = Field(gt=Decimal("0"))
    capital_receipt_emitted_at_utc: datetime

    placement_policy_version: Literal["m10.paper-placement.v1"]
    placement_policy_fingerprint: str
    symbol: Literal["NVDA"]
    side: Literal["buy"]
    order_type: Literal["limit"]
    time_in_force: Literal["day"]
    limit_price: Decimal = Field(gt=Decimal("0"))
    quantity_quantum: Decimal = Field(gt=Decimal("0"))
    quantity: Decimal = Field(gt=Decimal("0"))
    planned_notional: Decimal = Field(gt=Decimal("0"))
    intent_at_utc: datetime

    paper_only: Literal[True] = True
    live_execution_allowed: Literal[False] = False
    market_price_discovery_allowed: Literal[False] = False
    portfolio_mutation_authority: Literal[False] = False
    lifecycle_authority: Literal[False] = False
    durable_commit_proven: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("capital_receipt_emitted_at_utc", "intent_at_utc")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "m10_datetime_must_be_utc")

    @model_validator(mode="after")
    def _validate_law(self) -> "PlacementIntent":
        for name in (
            "capital_receipt_fingerprint",
            "capital_decision_fingerprint",
            "final_decision_fingerprint",
            "capital_state_fingerprint",
            "modifier_decision_fingerprint",
            "m09_policy_fingerprint",
            "serial_candidate_fingerprint",
            "placement_policy_fingerprint",
        ):
            _require_hash(getattr(self, name), f"{name}_invalid")
        if self.parallel_assessment_fingerprint is not None:
            _require_hash(
                self.parallel_assessment_fingerprint, "parallel_assessment_fingerprint_invalid"
            )
        if (self.parallel_assessment_id is None) != (self.parallel_assessment_fingerprint is None):
            raise ValueError("parallel_assessment_lineage_incomplete")
        expected_policy = semantic_fingerprint(
            {
                "policy_version": self.placement_policy_version,
                "symbol": self.symbol,
                "side": self.side,
                "order_type": self.order_type,
                "time_in_force": self.time_in_force,
                "adapter_mode": "paper",
                "quantity_quantum": self.quantity_quantum,
            }
        )
        if self.placement_policy_fingerprint != expected_policy:
            raise ValueError("placement_policy_fingerprint_mismatch")
        if self.intent_at_utc < self.capital_receipt_emitted_at_utc:
            raise ValueError("intent_precedes_capital_receipt")
        if self.quantity % self.quantity_quantum != 0:
            raise ValueError("quantity_not_quantum_multiple")
        if self.quantity * self.limit_price > self.authorised_notional:
            raise ValueError("placement_exceeds_m09_authority")
        expected_notional = (self.quantity * self.limit_price).quantize(
            Decimal("0.01"), rounding=ROUND_FLOOR
        )
        if self.planned_notional != expected_notional:
            raise ValueError("planned_notional_mismatch")
        material = _material(self, exclude={"intent_id", "semantic_fingerprint"})
        expected_fp = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected_fp:
            raise ValueError("placement_intent_fingerprint_mismatch")
        if self.intent_id != f"placement-intent:{expected_fp[:24]}":
            raise ValueError("placement_intent_id_mismatch")
        return self


class ExecutionEvent(BaseModel):
    """One immutable paper acknowledgement or fill occurrence."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    event_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    sequence: Literal[1, 2]
    event_type: Literal["order_accepted", "fill_recorded"]
    intent: PlacementIntent
    intent_id: str = Field(min_length=1)
    intent_fingerprint: str
    port_id: str = Field(min_length=1)
    port_version: Literal["m10.paper-port.v1"]
    port_fingerprint: str
    order_id: str = Field(min_length=1)
    fill_id: str | None
    quantity: Decimal = Field(gt=Decimal("0"))
    price: Decimal = Field(gt=Decimal("0"))
    notional: Decimal = Field(gt=Decimal("0"))
    occurred_at_utc: datetime
    paper_only: Literal[True] = True
    network_execution_proven: Literal[False] = False
    position_mutation_proven: Literal[False] = False
    lifecycle_mutation_proven: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("occurred_at_utc")
    @classmethod
    def _event_utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "execution_event_time_must_be_utc")

    @model_validator(mode="after")
    def _validate_event(self) -> "ExecutionEvent":
        _require_hash(self.intent_fingerprint, "intent_fingerprint_invalid")
        _require_hash(self.port_fingerprint, "port_fingerprint_invalid")
        intent = PlacementIntent.model_validate(self.intent.model_dump(mode="python"))
        if (
            self.intent_id != intent.intent_id
            or self.intent_fingerprint != intent.semantic_fingerprint
        ):
            raise ValueError("execution_event_intent_binding_mismatch")
        if (self.quantity, self.price, self.notional) != (
            intent.quantity,
            intent.limit_price,
            intent.planned_notional,
        ):
            raise ValueError("execution_event_exceeds_or_differs_from_intent")
        if self.occurred_at_utc < intent.intent_at_utc:
            raise ValueError("execution_event_precedes_intent")
        if self.sequence == 1 and (self.event_type != "order_accepted" or self.fill_id is not None):
            raise ValueError("order_event_shape_invalid")
        if self.sequence == 2 and (self.event_type != "fill_recorded" or not self.fill_id):
            raise ValueError("fill_event_shape_invalid")
        expected_notional = (self.quantity * self.price).quantize(
            Decimal("0.01"), rounding=ROUND_FLOOR
        )
        if self.notional != expected_notional:
            raise ValueError("execution_event_notional_mismatch")
        material = _material(self, exclude={"event_id", "semantic_fingerprint"})
        expected_fp = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected_fp:
            raise ValueError("execution_event_fingerprint_mismatch")
        if self.event_id != f"execution-event:{expected_fp[:24]}":
            raise ValueError("execution_event_id_mismatch")
        return self


class ExecutionReceipt(BaseModel):
    """Terminal M10 paper evidence bound to exact events and M13 sequence facts."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    receipt_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    status: Literal["filled"] = "filled"
    intent: PlacementIntent
    intent_id: str = Field(min_length=1)
    intent_fingerprint: str
    port_id: str = Field(min_length=1)
    port_version: Literal["m10.paper-port.v1"]
    port_fingerprint: str
    order_event: ExecutionEvent
    fill_event: ExecutionEvent
    order_event_id: str = Field(min_length=1)
    order_event_fingerprint: str
    fill_event_id: str = Field(min_length=1)
    fill_event_fingerprint: str
    order_id: str = Field(min_length=1)
    fill_id: str = Field(min_length=1)
    executed_quantity: Decimal = Field(gt=Decimal("0"))
    executed_price: Decimal = Field(gt=Decimal("0"))
    executed_notional: Decimal = Field(gt=Decimal("0"))
    executed_at_utc: datetime
    transaction_receipt_id: str = Field(min_length=1)
    transaction_command_id: str = Field(min_length=1)
    transaction_command_type: Literal["m10.paper_execute"] = "m10.paper_execute"
    transaction_consistency_unit_id: str = Field(min_length=1)
    transaction_input_fingerprint: str
    transaction_policy_version: Literal["m10.paper-port.v1"]
    transaction_prior_state_version: int = Field(ge=0)
    transaction_resulting_state_version: int = Field(ge=1)
    transaction_sequence: int = Field(ge=1)
    durability: Literal["non_durable_in_memory"] = "non_durable_in_memory"
    paper_only: Literal[True] = True
    live_execution_proven: Literal[False] = False
    network_execution_proven: Literal[False] = False
    position_mutation_proven: Literal[False] = False
    lifecycle_mutation_proven: Literal[False] = False
    durable_commit_proven: Literal[False] = False
    semantic_fingerprint: str

    @field_validator("executed_at_utc")
    @classmethod
    def _receipt_utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "execution_receipt_time_must_be_utc")

    @model_validator(mode="after")
    def _validate_receipt(self) -> "ExecutionReceipt":
        _require_hash(self.intent_fingerprint, "intent_fingerprint_invalid")
        _require_hash(self.port_fingerprint, "port_fingerprint_invalid")
        _require_hash(self.transaction_input_fingerprint, "transaction_input_fingerprint_invalid")
        intent = PlacementIntent.model_validate(self.intent.model_dump(mode="python"))
        if (
            self.intent_id != intent.intent_id
            or self.intent_fingerprint != intent.semantic_fingerprint
        ):
            raise ValueError("execution_receipt_intent_binding_mismatch")
        if self.transaction_input_fingerprint != intent.semantic_fingerprint:
            raise ValueError("transaction_input_fingerprint_mismatch")
        if (
            self.transaction_consistency_unit_id != self.port_id
            or self.transaction_policy_version != self.port_version
        ):
            raise ValueError("transaction_port_scope_mismatch")
        if self.transaction_command_id != f"m10.execute:{intent.intent_id}":
            raise ValueError("transaction_command_id_mismatch")
        order = ExecutionEvent.model_validate(self.order_event.model_dump(mode="python"))
        fill = ExecutionEvent.model_validate(self.fill_event.model_dump(mode="python"))
        if (order.sequence, fill.sequence) != (1, 2):
            raise ValueError("execution_event_order_invalid")
        for event in (order, fill):
            if (
                event.intent_id != self.intent_id
                or event.intent_fingerprint != self.intent_fingerprint
            ):
                raise ValueError("execution_receipt_intent_lineage_mismatch")
            if event.port_id != self.port_id or event.port_fingerprint != self.port_fingerprint:
                raise ValueError("execution_receipt_port_lineage_mismatch")
        if (
            self.order_event_id != order.event_id
            or self.order_event_fingerprint != order.semantic_fingerprint
        ):
            raise ValueError("order_event_binding_mismatch")
        if (
            self.fill_event_id != fill.event_id
            or self.fill_event_fingerprint != fill.semantic_fingerprint
        ):
            raise ValueError("fill_event_binding_mismatch")
        if (
            self.order_id != order.order_id
            or self.order_id != fill.order_id
            or self.fill_id != fill.fill_id
        ):
            raise ValueError("order_fill_identity_mismatch")
        if (self.executed_quantity, self.executed_price, self.executed_notional) != (
            fill.quantity,
            fill.price,
            fill.notional,
        ):
            raise ValueError("execution_fill_values_mismatch")
        if (self.executed_quantity, self.executed_price, self.executed_notional) != (
            intent.quantity,
            intent.limit_price,
            intent.planned_notional,
        ):
            raise ValueError("execution_receipt_exceeds_or_differs_from_intent")
        if (
            self.executed_at_utc != fill.occurred_at_utc
            or order.occurred_at_utc != fill.occurred_at_utc
        ):
            raise ValueError("execution_event_time_mismatch")
        if self.transaction_resulting_state_version != self.transaction_prior_state_version + 1:
            raise ValueError("transaction_version_progression_invalid")
        material = _material(
            self, exclude={"receipt_id", "transaction_receipt_id", "semantic_fingerprint"}
        )
        expected_fp = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected_fp:
            raise ValueError("execution_receipt_fingerprint_mismatch")
        expected_id = f"execution-receipt:{expected_fp[:24]}"
        if self.receipt_id != expected_id or self.transaction_receipt_id != expected_id:
            raise ValueError("execution_receipt_id_mismatch")
        return self
