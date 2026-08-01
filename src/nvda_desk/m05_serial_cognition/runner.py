"""Deterministic side-effect-free coordinator for M05 K08/K09 authority."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from pydantic import ValidationError

from .contracts import (
    ALLOWED_STAGE_AUTHORITY_OWNERS,
    CLOSED_AUTHORITY_CLASSES,
    SERIAL_STAGE_DEPENDENCIES,
    SERIAL_STAGE_ORDER,
    STAGE_OWNER_IDS,
    SerialCandidate,
    StageContext,
    StageInput,
    StageOutput,
    semantic_fingerprint,
)

StageHandler = Callable[
    [StageInput, tuple[StageOutput, ...]],
    StageOutput | Mapping[str, Any],
]


def _revalidate(model_type: type[Any], value: Any) -> Any:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="python")
    return model_type.model_validate(value)


def _deduplicate(
    items: Sequence[tuple[str, str, str, str]],
) -> tuple[tuple[str, str, str, str], ...]:
    return tuple(dict.fromkeys(items))


class SerialRunner:
    """Validate and execute exactly one governed six-stage serial graph."""

    def __init__(
        self,
        *,
        handlers: Mapping[str, StageHandler],
        runner_version: str,
        stage_order_version: str,
    ) -> None:
        if not runner_version:
            raise ValueError("runner_version_required")
        if not stage_order_version:
            raise ValueError("stage_order_version_required")
        if set(handlers) != set(SERIAL_STAGE_ORDER) or len(handlers) != len(SERIAL_STAGE_ORDER):
            raise ValueError("exact_six_stage_handlers_required")
        if any(not callable(handlers[stage]) for stage in SERIAL_STAGE_ORDER):
            raise TypeError("stage_handler_must_be_callable")
        self._handlers = {stage: handlers[stage] for stage in SERIAL_STAGE_ORDER}
        self._runner_version = runner_version
        self._stage_order_version = stage_order_version

    def run(
        self,
        *,
        context: StageContext | Mapping[str, Any],
        stage_inputs: Sequence[StageInput | Mapping[str, Any]],
    ) -> SerialCandidate:
        """Return one formed or explicit terminal result without side effects."""

        governed_context = _revalidate(StageContext, context)
        if governed_context.runner_version != self._runner_version:
            raise ValueError("runner_version_mismatch")
        if governed_context.serial_order_version != self._stage_order_version:
            raise ValueError("stage_order_version_mismatch")
        inputs = self._normalise_inputs(governed_context, stage_inputs)

        outputs: dict[str, StageOutput] = {}
        for stage in SERIAL_STAGE_ORDER:
            dependencies = tuple(outputs[name] for name in SERIAL_STAGE_DEPENDENCIES[stage])
            raw_output = self._handlers[stage](inputs[stage], dependencies)
            output = _revalidate(StageOutput, raw_output)
            self._validate_output(
                governed_context,
                inputs[stage],
                dependencies,
                output,
            )
            outputs[stage] = output
            ordered = tuple(outputs[name] for name in SERIAL_STAGE_ORDER if name in outputs)
            if output.status == "stand_down":
                if stage not in {"posture", "eligibility"}:
                    raise ValueError("stand_down_stage_not_authorised")
                return self._build_candidate(
                    governed_context,
                    ordered,
                    status="stand_down",
                    reasons=output.reasons,
                    failed_stage=stage,
                )
            if output.status in {"withheld", "rejected"}:
                return self._build_candidate(
                    governed_context,
                    ordered,
                    status=output.status,
                    reasons=output.reasons,
                    failed_stage=stage,
                )
            if output.status != "complete":
                raise ValueError("unknown_stage_output_status")

        return self._build_candidate(
            governed_context,
            tuple(outputs[stage] for stage in SERIAL_STAGE_ORDER),
            status="formed",
            reasons=(),
            failed_stage=None,
        )

    @staticmethod
    def _normalise_inputs(
        context: StageContext,
        stage_inputs: Sequence[StageInput | Mapping[str, Any]],
    ) -> dict[str, StageInput]:
        if len(stage_inputs) != len(SERIAL_STAGE_ORDER):
            raise ValueError("exact_six_stage_inputs_required")
        try:
            governed = tuple(_revalidate(StageInput, item) for item in stage_inputs)
        except (ValidationError, TypeError, ValueError) as exc:
            message = str(exc)
            if "carrier_stage_mismatch" in message:
                raise ValueError("carrier_stage_mismatch") from exc
            raise ValueError("invalid_stage_input") from exc
        by_stage = {item.stage: item for item in governed}
        if set(by_stage) != set(SERIAL_STAGE_ORDER) or len(by_stage) != len(governed):
            raise ValueError("stage_input_identity_set_invalid")
        for stage, item in by_stage.items():
            if item.carrier_stage != stage:
                raise ValueError("carrier_stage_mismatch")
            if (
                item.context_id != context.context_id
                or item.context_fingerprint != context.semantic_fingerprint
            ):
                raise ValueError("stage_input_context_mismatch")
            owners = {ref[0] for ref in item.authority_refs}
            if not owners <= ALLOWED_STAGE_AUTHORITY_OWNERS[stage]:
                raise ValueError("stage_input_foreign_authority_ref")
            if not item.authority_refs and item.missing_state is None:
                raise ValueError("stage_input_authority_or_missing_state_required")
        return by_stage

    @staticmethod
    def _validate_output(
        context: StageContext,
        stage_input: StageInput,
        dependencies: tuple[StageOutput, ...],
        output: StageOutput,
    ) -> None:
        if output.stage != stage_input.stage:
            raise ValueError("stage_output_identity_mismatch")
        if output.owner_id != STAGE_OWNER_IDS[stage_input.stage]:
            raise ValueError("stage_output_owner_mismatch")
        if (
            output.context_id != context.context_id
            or output.context_fingerprint != context.semantic_fingerprint
        ):
            raise ValueError("stage_output_context_mismatch")
        if (
            output.input_carrier_id != stage_input.carrier_id
            or output.input_carrier_fingerprint != stage_input.carrier_fingerprint
        ):
            raise ValueError("stage_output_input_carrier_lineage_mismatch")
        expected_ids = tuple(item.output_id for item in dependencies)
        expected_fingerprints = tuple(item.semantic_fingerprint for item in dependencies)
        if (
            output.dependency_output_ids != expected_ids
            or output.dependency_fingerprints != expected_fingerprints
        ):
            raise ValueError("stage_output_dependency_lineage_mismatch")
        if output.consumed_authority_refs != stage_input.authority_refs:
            raise ValueError("stage_output_authority_lineage_mismatch")
        if (
            output.closed_authority_classes != CLOSED_AUTHORITY_CLASSES
            or output.foreign_authority_claimed
        ):
            raise ValueError("stage_output_foreign_authority_claimed")
        if output.status != "complete":
            binding_keys = {
                "eligibility_lead_id",
                "playbook_family_id",
                "playbook_family_version",
                "playbook_id",
                "playbook_version",
                "setup_variant_id",
                "setup_variant_version",
                "expression_id",
                "expression_version",
                "expression_fingerprint",
            }
            if any(
                key in binding_keys
                or key.startswith("eligible_candidate.")
                or key.startswith("lifecycle.")
                for key, _ in output.result_refs
            ):
                raise ValueError("terminal_stage_output_contains_binding_payload")

    @staticmethod
    def _build_candidate(
        context: StageContext,
        outputs: tuple[StageOutput, ...],
        *,
        status: str,
        reasons: tuple[str, ...],
        failed_stage: str | None,
    ) -> SerialCandidate:
        by_stage = {item.stage: item for item in outputs}
        posture = by_stage.get("posture")
        eligibility = by_stage.get("eligibility")
        execution = by_stage.get("execution")
        posture_refs = dict(posture.result_refs) if posture else {}
        eligibility_refs = dict(eligibility.result_refs) if eligibility else {}
        execution_refs = dict(execution.result_refs) if execution else {}
        ordered_eligible_candidate_ids = tuple(
            value
            for key, value in sorted(eligibility_refs.items())
            if key.startswith("eligible_candidate.")
        )
        eligibility_lead_id = eligibility_refs.get("eligibility_lead_id")

        m07_refs = _deduplicate(
            tuple(
                ref
                for ref in (posture.consumed_authority_refs if posture else ())
                if ref[0] == "m07"
            )
        )
        m08_refs = _deduplicate(
            tuple(
                ref
                for output in (eligibility, execution)
                if output is not None
                for ref in output.consumed_authority_refs
                if ref[0] == "m08"
            )
        )
        formed = status == "formed"
        if formed:
            if tuple(item.stage for item in outputs) != SERIAL_STAGE_ORDER:
                raise ValueError("formed_result_requires_all_six_outputs")
            if posture_refs.get("posture_status") != "permitted":
                raise ValueError("formed_result_requires_permitted_posture")
            if eligibility_refs.get("eligibility_status") != "eligible":
                raise ValueError("formed_result_requires_eligible_playbook")
            if (
                not ordered_eligible_candidate_ids
                or eligibility_lead_id != ordered_eligible_candidate_ids[0]
            ):
                raise ValueError("formed_result_eligibility_lineage_incomplete")
            if not m07_refs or not m08_refs:
                raise ValueError("formed_result_authority_lineage_incomplete")
            required_execution = {
                "playbook_family_id",
                "playbook_family_version",
                "playbook_id",
                "playbook_version",
                "setup_variant_id",
                "setup_variant_version",
                "expression_id",
                "expression_version",
                "expression_fingerprint",
            }
            if not required_execution <= set(execution_refs):
                raise ValueError("formed_result_expression_lineage_incomplete")
            if execution_refs.get("playbook_id") != eligibility_lead_id:
                raise ValueError("formed_result_expression_lead_mismatch")

        lifecycle_intent = tuple(
            (key.removeprefix("lifecycle."), value)
            for key, value in execution_refs.items()
            if key.startswith("lifecycle.")
        )
        payload: dict[str, Any] = {
            "status": status,
            "reasons": reasons,
            "failed_stage": failed_stage,
            "serial_result_id": "",
            "candidate_id": None,
            "candidate_contract_version": "1.0.0",
            "candidate_schema_version": "1.0.0",
            "context_id": context.context_id,
            "context_fingerprint": context.semantic_fingerprint,
            "prepared_id": context.prepared_id,
            "prepared_fingerprint": context.prepared_fingerprint,
            "stage_order_version": context.serial_order_version,
            "stage_outputs": outputs,
            "posture_status": posture_refs.get("posture_status"),
            "posture_reasons": posture.reasons if posture else (),
            "m07_authority_refs": m07_refs,
            "m08_authority_refs": m08_refs,
            "ordered_eligible_candidate_ids": ordered_eligible_candidate_ids,
            "eligibility_lead_id": eligibility_lead_id,
            "selected_playbook_family_id": (
                execution_refs.get("playbook_family_id") if formed else None
            ),
            "selected_playbook_family_version": (
                execution_refs.get("playbook_family_version") if formed else None
            ),
            "selected_playbook_id": execution_refs.get("playbook_id") if formed else None,
            "selected_playbook_version": execution_refs.get("playbook_version") if formed else None,
            "selected_setup_variant_id": execution_refs.get("setup_variant_id") if formed else None,
            "selected_setup_variant_version": (
                execution_refs.get("setup_variant_version") if formed else None
            ),
            "expression_id": execution_refs.get("expression_id") if formed else None,
            "expression_version": execution_refs.get("expression_version") if formed else None,
            "expression_fingerprint": (
                execution_refs.get("expression_fingerprint") if formed else None
            ),
            "lifecycle_intent": lifecycle_intent if formed else (),
            "limitations": context.limitations,
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "foreign_authority_claimed": False,
            "semantic_fingerprint": "",
        }
        material = dict(payload)
        material.pop("serial_result_id")
        material.pop("candidate_id")
        material.pop("semantic_fingerprint")
        fingerprint = semantic_fingerprint(material)
        payload["semantic_fingerprint"] = fingerprint
        payload["serial_result_id"] = f"serial-result.{fingerprint[:16]}"
        payload["candidate_id"] = f"serial.{fingerprint[:16]}" if formed else None
        return SerialCandidate.model_validate(payload)


__all__ = ["SerialRunner"]
