"""Independent reference harness for M09 K11/K14 capital-authority proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal, ROUND_FLOOR
from hashlib import sha256
from typing import Any, Callable, Final

JOIN_POLICY_VERSION: Final = "m09.final-risk-join.v1"
CAPITAL_POLICY_VERSION: Final = "m09.capital-policy.v1"
CLOSED_AUTHORITIES: Final = (
    "broker_order",
    "execution",
    "position_inventory",
    "lifecycle",
    "durable_transaction",
    "replay",
)


def fingerprint(value: Any) -> str:
    def normalise(item: Any) -> Any:
        if isinstance(item, datetime):
            return item.astimezone(UTC).isoformat().replace("+00:00", "Z")
        if isinstance(item, Decimal):
            if item == 0:
                return "0"
            return format(item.normalize(), "f")
        if hasattr(item, "model_dump"):
            return normalise(item.model_dump(mode="python"))
        if hasattr(item, "__dict__") and not isinstance(item, type):
            return normalise(vars(item))
        if isinstance(item, dict):
            return {str(k): normalise(v) for k, v in sorted(item.items())}
        if isinstance(item, (tuple, list)):
            return [normalise(v) for v in item]
        return item

    return sha256(
        json.dumps(normalise(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class SerialBranch:
    result_id: str = "serial.result.001"
    candidate_id: str | None = "serial.candidate.001"
    status: str = "formed"
    prepared_id: str = "prepared.001"
    prepared_fingerprint: str = "a" * 64
    semantic_fingerprint: str = "b" * 64
    confidence: Decimal = Decimal("0.90")
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class ParallelBranch:
    assessment_id: str = "parallel.assessment.001"
    state: str = "observe"
    prepared_id: str = "prepared.001"
    prepared_fingerprint: str = "a" * 64
    semantic_fingerprint: str = "c" * 64
    hard_blocks: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModifierReceipt:
    receipt_id: str = "modifier.receipt.001"
    source_decision_fingerprint: str = "d" * 64
    decision_status: str = "no_modifier_members"
    kill_switches: tuple[str, ...] = ()
    vetoes: tuple[str, ...] = ()
    posture_scale: Decimal = Decimal("0.10")


@dataclass(frozen=True)
class CapitalStateCase:
    state_id: str = "capital.state.001"
    state_version: str = "1"
    available_capital: Decimal = Decimal("100000")
    reserved_capital: Decimal = Decimal("10000")
    max_fresh_deployable_pct: Decimal = Decimal("12.00")
    effective_at_utc: datetime = datetime(2026, 8, 1, 0, 0, tzinfo=UTC)


@dataclass(frozen=True)
class JoinPolicy:
    version: str = JOIN_POLICY_VERSION
    cautions_prohibit: bool = False


@dataclass(frozen=True)
class CapitalPolicy:
    version: str = CAPITAL_POLICY_VERSION
    target_pct: Decimal = Decimal("10.00")
    hard_max_pct: Decimal = Decimal("15.00")
    caution_multiplier: Decimal = Decimal("0.50")
    rounding_quantum: Decimal = Decimal("0.01")


@dataclass(frozen=True)
class ReferenceResult:
    final_action: str
    capital_action: str
    authorised_pct: Decimal
    authorised_notional: Decimal
    reasons: tuple[str, ...]
    final_decision_id: str
    capital_decision_id: str
    receipt_id: str
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES


def _id(prefix: str, material: Any) -> str:
    return f"{prefix}.{fingerprint(material)[:20]}"


def evaluate_reference(
    serial: SerialBranch | None,
    parallel: ParallelBranch | None,
    modifier: ModifierReceipt | None,
    capital: CapitalStateCase | None,
    join_policy: JoinPolicy = JoinPolicy(),
    capital_policy: CapitalPolicy = CapitalPolicy(),
    *,
    emitted_at_utc: datetime = datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
) -> ReferenceResult:
    del emitted_at_utc  # occurrence metadata is deliberately outside semantic identity
    reasons: list[str] = []
    eligible = True
    if join_policy.version != JOIN_POLICY_VERSION:
        reasons.append("unsupported_join_policy")
        eligible = False
    if serial is None or parallel is None:
        reasons.append("mandatory_branch_missing")
        eligible = False
    else:
        if serial.status != "formed" or not serial.candidate_id:
            reasons.append("serial_not_formed")
            eligible = False
        if parallel.state in {"block", "unknown"}:
            reasons.append(f"parallel_{parallel.state}")
            eligible = False
        if parallel.hard_blocks:
            reasons.append("parallel_hard_block")
            eligible = False
        if parallel.unknowns:
            reasons.append("parallel_unknown_authority")
            eligible = False
        if serial.prepared_id != parallel.prepared_id or serial.prepared_fingerprint != parallel.prepared_fingerprint:
            reasons.append("prepared_lineage_conflict")
            eligible = False
        if parallel.cautions and join_policy.cautions_prohibit:
            reasons.append("caution_prohibited")
            eligible = False
    final_action = "eligible_for_capital_assessment" if eligible else "stand_down"
    final_material = {
        "serial": serial,
        "parallel": parallel,
        "policy": join_policy,
        "action": final_action,
        "reasons": tuple(sorted(reasons)),
    }
    final_id = _id("final-risk", final_material)

    action = "block"
    pct = Decimal("0")
    notional = Decimal("0")
    if eligible:
        policy_domain_valid = (
            capital_policy.version == CAPITAL_POLICY_VERSION
            and Decimal("0") <= capital_policy.target_pct <= Decimal("100")
            and Decimal("0") <= capital_policy.hard_max_pct <= Decimal("100")
            and Decimal("0") <= capital_policy.caution_multiplier <= Decimal("1")
            and Decimal("0") < capital_policy.rounding_quantum <= Decimal("100")
        )
        capital_domain_valid = (
            capital is not None
            and capital.available_capital >= 0
            and capital.reserved_capital >= 0
            and Decimal("0") <= capital.max_fresh_deployable_pct <= Decimal("100")
            and capital.effective_at_utc.tzinfo is not None
            and capital.effective_at_utc.utcoffset() == timedelta(0)
        )
        if not policy_domain_valid:
            reasons.append("invalid_or_unsupported_capital_policy")
        elif modifier is None or capital is None:
            reasons.append("capital_authority_missing")
        elif not capital_domain_valid:
            reasons.append("invalid_capital_state")
        elif modifier.decision_status == "rejected" or modifier.kill_switches or modifier.vetoes:
            reasons.append("modifier_block")
        elif capital.available_capital == 0:
            action = "no_trade"
        else:
            pct = min(
                capital_policy.target_pct,
                capital_policy.hard_max_pct,
                capital.max_fresh_deployable_pct,
            )
            if parallel and parallel.cautions:
                pct *= capital_policy.caution_multiplier
            pct = (
                max(Decimal("0"), pct) / capital_policy.rounding_quantum
            ).to_integral_value(rounding=ROUND_FLOOR) * capital_policy.rounding_quantum
            notional = (
                capital.available_capital * pct / Decimal("100")
            ).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
            if pct == 0 or notional == 0:
                action = "no_trade"
                pct = Decimal("0")
                notional = Decimal("0")
            elif pct < capital_policy.target_pct:
                action = "reduce"
            else:
                action = "continue"
    capital_material = {
        "final_id": final_id,
        "modifier": modifier,
        "capital": capital,
        "policy": capital_policy,
        "action": action,
        "pct": pct,
        "notional": notional,
        "reasons": tuple(sorted(set(reasons))),
    }
    capital_id = _id("capital-decision", capital_material)
    receipt_id = _id("capital-receipt", capital_material)
    return ReferenceResult(
        final_action=final_action,
        capital_action=action,
        authorised_pct=pct,
        authorised_notional=notional,
        reasons=tuple(sorted(set(reasons))),
        final_decision_id=final_id,
        capital_decision_id=capital_id,
        receipt_id=receipt_id,
    )


def validate_result_law(
    result: ReferenceResult,
    serial: SerialBranch | None,
    parallel: ParallelBranch | None,
    modifier: ModifierReceipt | None,
    capital: CapitalStateCase | None,
    join_policy: JoinPolicy = JoinPolicy(),
    capital_policy: CapitalPolicy = CapitalPolicy(),
) -> None:
    expected = evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)
    if result != expected:
        raise ValueError("m09_reference_law_mismatch")
    if result.closed_authority_classes != CLOSED_AUTHORITIES:
        raise ValueError("foreign_authority_claimed")


class MissingBranchPass:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        return evaluate_reference(serial or SerialBranch(), parallel or ParallelBranch(), modifier, capital, join_policy, capital_policy)


class ConfidenceOverridesBlock:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        if serial and serial.confidence >= Decimal("0.8") and parallel:
            parallel = replace(parallel, state="observe", hard_blocks=(), unknowns=())
        return evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)


class LineageMismatchPass:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        if serial and parallel:
            parallel = replace(parallel, prepared_id=serial.prepared_id, prepared_fingerprint=serial.prepared_fingerprint)
        return evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)


class PostureScaleSizesCapital:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        result = evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)
        if result.final_action == "eligible_for_capital_assessment" and modifier and capital:
            pct = (capital_policy.target_pct * modifier.posture_scale).quantize(Decimal("0.01"))
            return replace(result, authorised_pct=pct, authorised_notional=(capital.available_capital*pct/Decimal("100")).quantize(Decimal("0.01")))
        return result


class IgnoresHardMaximum:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        result = evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)
        if result.final_action == "eligible_for_capital_assessment" and capital:
            pct = min(capital_policy.target_pct, capital.max_fresh_deployable_pct)
            return replace(result, authorised_pct=pct, authorised_notional=(capital.available_capital*pct/Decimal("100")).quantize(Decimal("0.01")))
        return result


class AcceptsFuturePolicy:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        return evaluate_reference(serial, parallel, modifier, capital, replace(join_policy, version=JOIN_POLICY_VERSION), replace(capital_policy, version=CAPITAL_POLICY_VERSION))


class EmissionTimeChangesIdentity:
    def __call__(self, serial, parallel, modifier, capital, join_policy=JoinPolicy(), capital_policy=CapitalPolicy()):
        result = evaluate_reference(serial, parallel, modifier, capital, join_policy, capital_policy)
        return replace(result, receipt_id=_id("capital-receipt", {"base": result.receipt_id, "time": datetime.now(tz=UTC)}))


MUTANTS: Final[dict[str, Callable[..., ReferenceResult]]] = {
    "missing_branch_pass": MissingBranchPass(),
    "confidence_overrides_block": ConfidenceOverridesBlock(),
    "lineage_mismatch_pass": LineageMismatchPass(),
    "posture_scale_sizes_capital": PostureScaleSizesCapital(),
    "ignores_hard_maximum": IgnoresHardMaximum(),
    "accepts_future_policy": AcceptsFuturePolicy(),
    "emission_time_changes_identity": EmissionTimeChangesIdentity(),
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m09_capital_authority")
    required = (
        "FinalRiskDecision",
        "CapitalState",
        "CapitalDeploymentDecision",
        "CapitalDeploymentReceipt",
        "FinalRiskJoinPolicy",
        "CapitalDeploymentPolicy",
        "CapitalAuthorityService",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M09 package is missing exports: {missing}")
    return {name: getattr(module, name) for name in required}


def production_serial_candidate(*, prepared_id: str, prepared_fingerprint: str):
    from tests.support.m05_k08_k09_contract_harness import (
        SERIAL_STAGE_ORDER,
        fingerprint as m05_fingerprint,
        production_api as m05_api,
        production_context_payload,
        production_handlers,
        production_stage_input_payload,
        valid_context,
        valid_inputs,
    )

    api = m05_api()
    case = valid_context(
        prepared_id=prepared_id,
        prepared_fingerprint=prepared_fingerprint,
    )
    context = api["StageContext"].model_validate(production_context_payload(case))
    stage_inputs = []
    for item in valid_inputs(case, order=tuple(reversed(SERIAL_STAGE_ORDER))):
        if item.stage in {"temporal", "regime", "options_flow"}:
            authority_refs = ((
                "m03",
                prepared_id,
                case.prepared_schema_version,
                prepared_fingerprint,
            ),)
            item = replace(
                item,
                authority_refs=authority_refs,
                carrier_fingerprint=m05_fingerprint(
                    {
                        "stage": item.stage,
                        "context": case.semantic_fingerprint,
                        "authority_refs": authority_refs,
                    }
                ),
            )
        stage_inputs.append(
            api["StageInput"].model_validate(production_stage_input_payload(item))
        )
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=case.runner_version,
        stage_order_version=case.serial_order_version,
    )
    return runner.run(context=context, stage_inputs=tuple(stage_inputs))


def production_parallel_assessment(*, vix_level: float = 20.0):
    from tests.support.m06_k10_contract_harness import make_prepared
    import nvda_desk.m06_parallel_risk as m06
    from nvda_desk.m06_parallel_risk.contracts import (
        EXPECTED_FAMILIES,
        parallel_risk_assessment_fingerprint,
        parallel_risk_observation_fingerprint,
    )

    risk_input = m06.ParallelRiskInput.from_prepared(
        make_prepared(vix_level=vix_level),
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=("m07:caution:v1", "m07:block:v1"),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
    )
    base = m06.ParallelRiskEvaluator().evaluate(risk_input)
    source_references = base.observations[0].source_references
    observations = []
    admitted_observe_reasons = {
        "concentration": "concentration_within_admitted_limit",
        "inventory_stress": "inventory_stress_within_admitted_limit",
        "liquidity": "liquidity_within_admitted_limit",
    }
    for item in base.observations:
        if item.family not in admitted_observe_reasons:
            observations.append(item)
            continue
        payload = {
            "observation_id": "pending",
            "family": item.family,
            "state": "observe",
            "reason": admitted_observe_reasons[item.family],
            "source_fields": item.source_fields,
            "source_references": source_references,
            "limitation": None,
            "semantic_fingerprint": "0" * 64,
        }
        provisional = m06.ParallelRiskObservation.model_construct(**payload)
        observation_fp = parallel_risk_observation_fingerprint(provisional)
        payload["semantic_fingerprint"] = observation_fp
        payload["observation_id"] = f"parallel-risk-observation:{observation_fp[:24]}"
        observations.append(m06.ParallelRiskObservation.model_validate(payload))
    observations = tuple(sorted(observations, key=lambda item: EXPECTED_FAMILIES.index(item.family)))
    cautions = tuple(item.reason for item in observations if item.state == "caution")
    blocks = tuple(item.reason for item in observations if item.state == "block")
    unknowns = tuple(item.family for item in observations if item.state == "unknown")
    limitations = tuple(
        sorted(
            set(base.prepared_limitations)
            | set(base.missing_optional_enrichments)
            | {item.limitation for item in observations if item.limitation}
        )
    )
    state = "block" if blocks else "caution" if cautions else "unknown" if unknowns else "observe"
    payload = {
        **base.model_dump(mode="python"),
        "assessment_id": "pending",
        "state": state,
        "observations": observations,
        "caution_flags": cautions,
        "hard_blocks": blocks,
        "unknown_families": unknowns,
        "limitations": limitations,
        "semantic_fingerprint": "0" * 64,
    }
    provisional = m06.ParallelRiskAssessment.model_construct(**payload)
    assessment_fp = parallel_risk_assessment_fingerprint(provisional)
    payload["semantic_fingerprint"] = assessment_fp
    payload["assessment_id"] = f"parallel-risk-assessment:{assessment_fp[:24]}"
    return m06.ParallelRiskAssessment.model_validate(payload)


def production_modifier_receipt(*, kill_switch: bool = False):
    from nvda_desk.m07_coefficient_modifier_authority import ModifierApplicationReceipt
    from nvda_desk.m07_coefficient_modifier_authority.contracts import CLOSED_AUTHORITY_CLASSES

    return ModifierApplicationReceipt.model_validate(
        {
            "receipt_id": "m07.receipt.001",
            "application_id": "m07.application.001",
            "source_decision_id": "m07.decision.001",
            "source_decision_fingerprint": "d" * 64,
            "bundle_id": "m07.bundle.001",
            "bundle_version": "1.0.0",
            "schema_version": "1.0.0",
            "authority_id": "m07.authority",
            "authority_version": "1.0.0",
            "resolution_law_version": "m07.k12.v1",
            "owner_stage": "posture",
            "input_context_id": "context.001",
            "input_context_version": "1.0.0",
            "input_effective_at_utc": datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
            "input_fingerprint": "e" * 64,
            "decision_status": "applied" if kill_switch else "no_modifier_members",
            "applied_modifiers": (),
            "skipped_modifiers": (),
            "coefficient_results": (
                {
                    "coefficient_id": "posture.exposure_scale",
                    "coefficient_version": "1.0.0",
                    "baseline_value": "1.0",
                    "pre_clamp_candidate": "0" if kill_switch else "1.0",
                    "hard_lower_bound": "0",
                    "hard_upper_bound": "1",
                    "effective_value": "0" if kill_switch else "1.0",
                    "bound_disposition": "within_bounds",
                },
            ),
            "conflict_dispositions": (),
            "veto_dispositions": (),
            "kill_switch_dispositions": ("hard_kill",) if kill_switch else (),
            "no_op_class": None if kill_switch else "no_modifier_members",
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "limitations": ("resolution_only", "external_state_mutation_not_proven"),
            "external_mutation_proven": False,
            "emitted_at_utc": datetime(2026, 8, 1, 0, 1, tzinfo=UTC),
        }
    )
