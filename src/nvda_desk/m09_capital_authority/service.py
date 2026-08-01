"""M09 owner service for K11 final-risk and K14 bounded fresh capital."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from typing import Any

from pydantic import ValidationError

from nvda_desk.m05_serial_cognition import SerialCandidate
from nvda_desk.m06_parallel_risk import ParallelRiskAssessment
from nvda_desk.m07_coefficient_modifier_authority import ModifierApplicationReceipt

from .contracts import (
    CapitalDeploymentDecision,
    CapitalDeploymentPolicy,
    CapitalDeploymentReceipt,
    CapitalState,
    FinalRiskDecision,
    FinalRiskJoinPolicy,
    semantic_fingerprint,
)


def _revalidate(model_type, value: Any, reason: str):
    if not isinstance(value, model_type):
        raise TypeError(reason)
    try:
        return model_type.model_validate(value.model_dump(mode="python"))
    except (ValidationError, ValueError, TypeError) as exc:
        raise ValueError(reason) from exc


def _canonical_texts(*groups: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted({item for group in groups for item in group if item}))


def _build_final_decision(payload: dict[str, Any]) -> FinalRiskDecision:
    material = dict(payload)
    material["semantic_fingerprint"] = semantic_fingerprint(material)
    material["final_decision_id"] = f"final-risk.{material['semantic_fingerprint'][:20]}"
    return FinalRiskDecision.model_validate(material)


def _build_capital_decision(payload: dict[str, Any]) -> CapitalDeploymentDecision:
    material = dict(payload)
    material["semantic_fingerprint"] = semantic_fingerprint(material)
    material["decision_id"] = f"capital-decision.{material['semantic_fingerprint'][:20]}"
    return CapitalDeploymentDecision.model_validate(material)


class CapitalAuthorityService:
    """Coordinate M09 without opening execution, position or durable authority."""

    def join_final_risk(
        self,
        serial_candidate: SerialCandidate | None,
        parallel_assessment: ParallelRiskAssessment | None,
        policy: FinalRiskJoinPolicy,
    ) -> FinalRiskDecision:
        try:
            policy = FinalRiskJoinPolicy.model_validate(policy.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("unsupported_final_risk_join_policy") from exc

        missing: list[str] = []
        reasons: list[str] = []
        conflicts: list[str] = []
        hard_blocks: tuple[str, ...] = ()
        cautions: tuple[str, ...] = ()
        unknowns: tuple[str, ...] = ()
        limitations: tuple[str, ...] = ()

        serial: SerialCandidate | None = None
        parallel: ParallelRiskAssessment | None = None
        if serial_candidate is None:
            missing.append("missing_serial_candidate_authority")
        else:
            serial = _revalidate(
                SerialCandidate,
                serial_candidate,
                "serial_candidate_contract_invalid",
            )
        if parallel_assessment is None:
            missing.append("missing_parallel_risk_authority")
        else:
            parallel = _revalidate(
                ParallelRiskAssessment,
                parallel_assessment,
                "parallel_risk_assessment_contract_invalid",
            )

        if serial is not None and serial.status != "formed":
            reasons.append(f"serial_{serial.status}")
        if serial is not None and not serial.candidate_id:
            reasons.append("serial_candidate_identity_missing")
        if parallel is not None:
            hard_blocks = tuple(sorted(parallel.hard_blocks))
            cautions = tuple(sorted(parallel.caution_flags))
            unknowns = tuple(sorted(parallel.unknown_families))
            if parallel.state in {"block", "unknown"}:
                reasons.append(f"parallel_{parallel.state}")
            if hard_blocks:
                reasons.append("parallel_hard_block")
            if unknowns:
                reasons.append("parallel_unknown_authority")
            if cautions and policy.cautions_prohibit:
                reasons.append("parallel_caution_prohibited")
        if serial is not None and parallel is not None:
            if (
                serial.prepared_id != parallel.prepared_id
                or serial.prepared_fingerprint != parallel.prepared_fingerprint
            ):
                conflicts.append("prepared_lineage_conflict")

        eligible = not (missing or reasons or conflicts or hard_blocks or unknowns)
        action = (
            "eligible_for_capital_assessment" if eligible else "stand_down"
        )
        if action == "stand_down" and not (missing or reasons or conflicts or hard_blocks or unknowns):
            reasons.append("final_risk_not_eligible")

        if serial is not None:
            limitations = _canonical_texts(limitations, serial.limitations)
        if parallel is not None:
            limitations = _canonical_texts(
                limitations,
                parallel.prepared_limitations,
                parallel.limitations,
            )

        payload = {
            "contract_version": "1.0.0",
            "action": action,
            "policy_version": policy.policy_version,
            "join_policy_fingerprint": policy.policy_fingerprint,
            "cautions_prohibit": policy.cautions_prohibit,
            "serial_result_id": serial.serial_result_id if serial else None,
            "serial_candidate_id": serial.candidate_id if serial else None,
            "serial_candidate_fingerprint": serial.semantic_fingerprint if serial else None,
            "serial_context_id": serial.context_id if serial else None,
            "serial_context_fingerprint": serial.context_fingerprint if serial else None,
            "serial_prepared_id": serial.prepared_id if serial else None,
            "serial_prepared_fingerprint": serial.prepared_fingerprint if serial else None,
            "serial_expression_id": serial.expression_id if serial else None,
            "serial_expression_version": serial.expression_version if serial else None,
            "serial_expression_fingerprint": serial.expression_fingerprint if serial else None,
            "parallel_assessment_id": parallel.assessment_id if parallel else None,
            "parallel_assessment_fingerprint": parallel.semantic_fingerprint if parallel else None,
            "parallel_input_id": parallel.input_id if parallel else None,
            "parallel_input_fingerprint": parallel.input_fingerprint if parallel else None,
            "parallel_prepared_id": parallel.prepared_id if parallel else None,
            "parallel_prepared_fingerprint": parallel.prepared_fingerprint if parallel else None,
            "parallel_evaluator_version": parallel.evaluator_version if parallel else None,
            "parallel_policy_version": parallel.evaluator_policy_version if parallel else None,
            "parallel_aggregation_version": parallel.aggregation_version if parallel else None,
            "parallel_state": parallel.state if parallel else None,
            "hard_blocks": tuple(sorted(hard_blocks)),
            "cautions": tuple(sorted(cautions)),
            "unknowns": tuple(sorted(unknowns)),
            "reasons": tuple(sorted(set(reasons))),
            "conflicts": tuple(sorted(set(conflicts))),
            "missing_authority_reasons": tuple(sorted(set(missing))),
            "limitations": limitations,
            "capital_authority_granted": False,
            "execution_authority_granted": False,
            "closed_authority_classes": (
                "broker_order",
                "execution",
                "position_inventory",
                "lifecycle",
                "durable_transaction",
                "replay",
            ),
        }
        return _build_final_decision(payload)

    def evaluate_capital(
        self,
        final_decision: FinalRiskDecision,
        capital_state: CapitalState,
        modifier_receipt: ModifierApplicationReceipt,
        policy: CapitalDeploymentPolicy,
    ) -> CapitalDeploymentDecision:
        final = _revalidate(
            FinalRiskDecision,
            final_decision,
            "final_risk_decision_contract_invalid",
        )
        state = _revalidate(CapitalState, capital_state, "capital_state_contract_invalid")
        modifier = _revalidate(
            ModifierApplicationReceipt,
            modifier_receipt,
            "modifier_application_receipt_contract_invalid",
        )
        try:
            policy = CapitalDeploymentPolicy.model_validate(
                policy.model_dump(mode="python")
            )
        except Exception as exc:
            raise ValueError("unsupported_capital_policy") from exc

        reasons: list[str] = []
        action = "block"
        pct = Decimal("0")
        notional = Decimal("0")
        if final.action != "eligible_for_capital_assessment":
            reasons.append("final_risk_not_eligible")
        elif modifier.kill_switch_dispositions or modifier.veto_dispositions:
            reasons.append("modifier_block")
        elif state.available_capital == 0:
            action = "no_trade"
            reasons.append("no_available_capital")
        else:
            pct = min(
                policy.target_pct,
                policy.hard_max_pct,
                state.max_fresh_deployable_pct,
            )
            if final.cautions:
                pct *= policy.caution_multiplier
            pct = (
                pct / policy.rounding_quantum
            ).to_integral_value(rounding=ROUND_FLOOR) * policy.rounding_quantum
            notional = (
                state.available_capital * pct / Decimal("100")
            ).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
            if pct == 0 or notional == 0:
                action = "no_trade"
                pct = Decimal("0")
                notional = Decimal("0")
                reasons.append("no_positive_fresh_capital")
            elif pct < policy.target_pct:
                action = "reduce"
                reasons.append("bounded_below_policy_target")
            else:
                action = "continue"
                reasons.append("bounded_policy_target_authorised")

        limitations = _canonical_texts(
            final.limitations,
            modifier.limitations,
            ("capital_decision_only", "no_fund_reservation_or_execution"),
        )
        payload = {
            "contract_version": "1.0.0",
            "action": action,
            "authorised_pct": pct,
            "authorised_notional": notional,
            "policy_version": policy.policy_version,
            "capital_policy_fingerprint": policy.policy_fingerprint,
            "policy_target_pct": policy.target_pct,
            "policy_hard_max_pct": policy.hard_max_pct,
            "policy_caution_multiplier": policy.caution_multiplier,
            "policy_rounding_quantum": policy.rounding_quantum,
            "final_decision_id": final.final_decision_id,
            "final_decision_fingerprint": final.semantic_fingerprint,
            "serial_result_id": final.serial_result_id,
            "serial_candidate_id": final.serial_candidate_id,
            "serial_candidate_fingerprint": final.serial_candidate_fingerprint,
            "parallel_assessment_id": final.parallel_assessment_id,
            "parallel_assessment_fingerprint": final.parallel_assessment_fingerprint,
            "capital_state_id": state.state_id,
            "capital_state_version": state.state_version,
            "capital_state_fingerprint": state.semantic_fingerprint,
            "capital_state_available_capital": state.available_capital,
            "capital_state_max_fresh_deployable_pct": state.max_fresh_deployable_pct,
            "modifier_receipt_id": modifier.receipt_id,
            "modifier_decision_fingerprint": modifier.source_decision_fingerprint,
            "modifier_bundle_id": modifier.bundle_id,
            "modifier_bundle_version": modifier.bundle_version,
            "modifier_authority_id": modifier.authority_id,
            "modifier_authority_version": modifier.authority_version,
            "modifier_resolution_law_version": modifier.resolution_law_version,
            "reasons": tuple(sorted(set(reasons))),
            "limitations": limitations,
            "placement_authority_granted": False,
            "broker_authority_granted": False,
            "execution_authority_granted": False,
            "position_mutation_authority_granted": False,
            "durable_commit_proven": False,
            "closed_authority_classes": (
                "broker_order",
                "execution",
                "position_inventory",
                "lifecycle",
                "durable_transaction",
                "replay",
            ),
        }
        return _build_capital_decision(payload)

    def build_receipt(
        self,
        decision: CapitalDeploymentDecision,
        final_decision: FinalRiskDecision,
        capital_state: CapitalState,
        modifier_receipt: ModifierApplicationReceipt,
        policy: CapitalDeploymentPolicy,
        *,
        emitted_at_utc: datetime,
    ) -> CapitalDeploymentReceipt:
        decision = _revalidate(
            CapitalDeploymentDecision,
            decision,
            "capital_deployment_decision_contract_invalid",
        )
        final = _revalidate(
            FinalRiskDecision,
            final_decision,
            "final_risk_decision_contract_invalid",
        )
        state = _revalidate(CapitalState, capital_state, "capital_state_contract_invalid")
        modifier = _revalidate(
            ModifierApplicationReceipt,
            modifier_receipt,
            "modifier_application_receipt_contract_invalid",
        )
        try:
            policy = CapitalDeploymentPolicy.model_validate(
                policy.model_dump(mode="python")
            )
        except Exception as exc:
            raise ValueError("unsupported_capital_policy") from exc
        expected_decision = self.evaluate_capital(final, state, modifier, policy)
        if decision.semantic_fingerprint != expected_decision.semantic_fingerprint:
            raise ValueError("capital_receipt_decision_input_mismatch")
        if (
            decision.final_decision_id != final.final_decision_id
            or decision.final_decision_fingerprint != final.semantic_fingerprint
            or decision.capital_state_id != state.state_id
            or decision.capital_state_fingerprint != state.semantic_fingerprint
            or decision.modifier_receipt_id != modifier.receipt_id
            or decision.modifier_decision_fingerprint != modifier.source_decision_fingerprint
            or decision.policy_version != policy.policy_version
        ):
            raise ValueError("capital_receipt_lineage_mismatch")
        payload = {
            "contract_version": "1.0.0",
            "decision_id": decision.decision_id,
            "decision_fingerprint": decision.semantic_fingerprint,
            "final_decision_id": final.final_decision_id,
            "final_decision_fingerprint": final.semantic_fingerprint,
            "capital_state_id": state.state_id,
            "capital_state_fingerprint": state.semantic_fingerprint,
            "capital_state_available_capital": state.available_capital,
            "capital_state_max_fresh_deployable_pct": state.max_fresh_deployable_pct,
            "modifier_receipt_id": modifier.receipt_id,
            "modifier_decision_fingerprint": modifier.source_decision_fingerprint,
            "policy_version": policy.policy_version,
            "capital_policy_fingerprint": policy.policy_fingerprint,
            "serial_result_id": decision.serial_result_id,
            "serial_candidate_id": decision.serial_candidate_id,
            "serial_candidate_fingerprint": decision.serial_candidate_fingerprint,
            "parallel_assessment_id": decision.parallel_assessment_id,
            "parallel_assessment_fingerprint": decision.parallel_assessment_fingerprint,
            "action": decision.action,
            "authorised_pct": decision.authorised_pct,
            "authorised_notional": decision.authorised_notional,
            "reasons": decision.reasons,
            "limitations": decision.limitations,
            "placement_authority_granted": False,
            "broker_authority_granted": False,
            "execution_authority_granted": False,
            "position_mutation_authority_granted": False,
            "durable_commit_proven": False,
            "closed_authority_classes": (
                "broker_order",
                "execution",
                "position_inventory",
                "lifecycle",
                "durable_transaction",
                "replay",
            ),
        }
        semantic = semantic_fingerprint(payload)
        return CapitalDeploymentReceipt.model_validate(
            {
                **payload,
                "receipt_id": f"capital-receipt.{semantic[:20]}",
                "emitted_at_utc": emitted_at_utc,
                "semantic_fingerprint": semantic,
            }
        )
