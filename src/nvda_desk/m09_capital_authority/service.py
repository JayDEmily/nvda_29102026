"""M09 owner service for K11 final-risk and K14 bounded fresh capital."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from typing import Any

from pydantic import ValidationError

from nvda_desk.contracts.packets import (
    DeskModulePacketV3,
    K07_COMMON_CHECKS,
    K07_ROLE_CHECKS,
    dmp_v3_carriage_fingerprint,
)
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
        serial_packet: DeskModulePacketV3,
        parallel_packet: DeskModulePacketV3,
        policy: FinalRiskJoinPolicy,
    ) -> FinalRiskDecision:
        """Validate the canonical DMPV3 seam before applying pure K11 law."""

        serial_envelope, serial = self._validated_packet(
            serial_packet,
            expected_role="stage_packet",
            expected_module="m05_serial_cognition",
            expected_grammar="serial_cognition",
            expected_stage="serial_candidate",
            payload_type=SerialCandidate,
            label="serial",
        )
        parallel_envelope, parallel = self._validated_packet(
            parallel_packet,
            expected_role="parallel_risk_packet",
            expected_module="m06_parallel_risk",
            expected_grammar="parallel_risk_lane",
            expected_stage=None,
            payload_type=ParallelRiskAssessment,
            label="parallel",
        )
        if (serial_envelope.traceid, serial_envelope.runid, serial_envelope.scenarioid) != (
            parallel_envelope.traceid,
            parallel_envelope.runid,
            parallel_envelope.scenarioid,
        ):
            raise ValueError("packet_execution_context_mismatch")
        serial_prepared = self._prepared_attestation(serial_envelope, "serial")
        parallel_prepared = self._prepared_attestation(parallel_envelope, "parallel")
        if serial_prepared != parallel_prepared:
            raise ValueError("prepared_context_packet_mismatch")
        if serial_envelope.lineage.parentids != [serial_prepared[0]]:
            raise ValueError("serial_prepared_parent_lineage_invalid")
        if parallel_envelope.lineage.parentids != [parallel_prepared[0]]:
            raise ValueError("parallel_prepared_parent_lineage_invalid")
        if (serial.prepared_id, serial.prepared_fingerprint) != serial_prepared[2:]:
            raise ValueError("serial_prepared_attestation_mismatch")
        if (parallel.prepared_id, parallel.prepared_fingerprint) != parallel_prepared[2:]:
            raise ValueError("parallel_prepared_attestation_mismatch")
        if serial_envelope.lineage.inputfingerprint != serial.context_fingerprint:
            raise ValueError("serial_packet_input_fingerprint_mismatch")
        if parallel_envelope.lineage.inputfingerprint != parallel.input_fingerprint:
            raise ValueError("parallel_packet_input_fingerprint_mismatch")
        if serial_envelope.lineage.derivedfrom != serial.serial_result_id:
            raise ValueError("serial_packet_domain_identity_mismatch")
        if parallel_envelope.lineage.derivedfrom != parallel.assessment_id:
            raise ValueError("parallel_packet_domain_identity_mismatch")
        carriage = {
            "carriage_validated": True,
            "trace_id": serial_envelope.traceid,
            "run_id": serial_envelope.runid,
            "scenario_id": serial_envelope.scenarioid,
            "prepared_context_packet_id": serial_prepared[0],
            "prepared_context_carriage_fingerprint": serial_prepared[1],
            "serial_packet_id": serial_envelope.id,
            "serial_packet_carriage_fingerprint": dmp_v3_carriage_fingerprint(serial_envelope),
            "parallel_packet_id": parallel_envelope.id,
            "parallel_packet_carriage_fingerprint": dmp_v3_carriage_fingerprint(parallel_envelope),
        }
        return self._join_domain_products(serial, parallel, policy, carriage=carriage)

    def join_final_risk_domain_for_compatibility(
        self,
        serial_candidate: SerialCandidate | None,
        parallel_assessment: ParallelRiskAssessment | None,
        policy: FinalRiskJoinPolicy,
    ) -> FinalRiskDecision:
        """Non-canonical domain-only adapter; its result cannot authorise capital."""

        return self._join_domain_products(
            serial_candidate,
            parallel_assessment,
            policy,
            carriage={
                "carriage_validated": False,
                "trace_id": None,
                "run_id": None,
                "scenario_id": None,
                "prepared_context_packet_id": None,
                "prepared_context_carriage_fingerprint": None,
                "serial_packet_id": None,
                "serial_packet_carriage_fingerprint": None,
                "parallel_packet_id": None,
                "parallel_packet_carriage_fingerprint": None,
            },
        )

    @staticmethod
    def _validated_packet(
        value: Any,
        *,
        expected_role: str,
        expected_module: str,
        expected_grammar: str,
        expected_stage: str | None,
        payload_type,
        label: str,
    ):
        if not isinstance(value, DeskModulePacketV3):
            raise TypeError("canonical_dmpv3_packet_required")
        try:
            packet = DeskModulePacketV3.model_validate(value.model_dump(mode="python"))
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError(f"{label}_packet_contract_invalid") from exc
        if packet.packetrole != expected_role:
            raise ValueError(f"{label}_packet_role_invalid")
        if (
            packet.producer.module_id != expected_module
            or packet.producer.grammar_role != expected_grammar
            or packet.producer.stage_name != expected_stage
        ):
            raise ValueError(f"{label}_packet_producer_invalid")
        if packet.validation.status != "valid" or packet.validation.violations:
            raise ValueError(f"{label}_packet_validation_invalid")
        expected_checks = (*K07_COMMON_CHECKS, *K07_ROLE_CHECKS[expected_role])
        observed = tuple(check.name for check in packet.validation.checks if check.passed)
        if observed != expected_checks or any(not check.passed for check in packet.validation.checks):
            raise ValueError(f"{label}_packet_validation_incomplete")
        try:
            payload = payload_type.model_validate(packet.data)
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError(f"{label}_packet_payload_invalid") from exc
        return packet, payload

    @staticmethod
    def _prepared_attestation(packet: DeskModulePacketV3, label: str) -> tuple[str, str, str, str]:
        try:
            prepared = packet.dmpextensions["nvda"]["prepared_context"]
            values = (
                prepared["packet_id"],
                prepared["carriage_fingerprint"],
                prepared["prepared_id"],
                prepared["prepared_fingerprint"],
            )
        except (KeyError, TypeError) as exc:
            raise ValueError(f"{label}_prepared_context_attestation_missing") from exc
        if any(not isinstance(value, str) or not value for value in values):
            raise ValueError(f"{label}_prepared_context_attestation_invalid")
        if len(values[1]) != 64 or len(values[3]) != 64:
            raise ValueError(f"{label}_prepared_context_attestation_invalid")
        return values

    def _join_domain_products(
        self,
        serial_candidate: SerialCandidate | None,
        parallel_assessment: ParallelRiskAssessment | None,
        policy: FinalRiskJoinPolicy,
        *,
        carriage: dict[str, Any],
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
        action = "eligible_for_capital_assessment" if eligible else "stand_down"
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
            **carriage,
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
                "broker_order", "execution", "position_inventory", "lifecycle",
                "durable_transaction", "replay",
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

        if not final.carriage_validated:
            raise ValueError("canonical_packet_carriage_required")

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
            "carriage_validated": final.carriage_validated,
            "trace_id": final.trace_id,
            "run_id": final.run_id,
            "scenario_id": final.scenario_id,
            "prepared_context_packet_id": final.prepared_context_packet_id,
            "prepared_context_carriage_fingerprint": final.prepared_context_carriage_fingerprint,
            "serial_packet_id": final.serial_packet_id,
            "serial_packet_carriage_fingerprint": final.serial_packet_carriage_fingerprint,
            "parallel_packet_id": final.parallel_packet_id,
            "parallel_packet_carriage_fingerprint": final.parallel_packet_carriage_fingerprint,
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
            "carriage_validated": final.carriage_validated,
            "trace_id": final.trace_id,
            "run_id": final.run_id,
            "scenario_id": final.scenario_id,
            "prepared_context_packet_id": final.prepared_context_packet_id,
            "prepared_context_carriage_fingerprint": final.prepared_context_carriage_fingerprint,
            "serial_packet_id": final.serial_packet_id,
            "serial_packet_carriage_fingerprint": final.serial_packet_carriage_fingerprint,
            "parallel_packet_id": final.parallel_packet_id,
            "parallel_packet_carriage_fingerprint": final.parallel_packet_carriage_fingerprint,
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
