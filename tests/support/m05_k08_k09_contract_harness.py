"""Reference and false-positive subjects for the bounded M05 K08/K09 proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Callable, Final

SERIAL_STAGE_ORDER: Final = (
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
)
SERIAL_STAGE_DEPENDENCIES: Final = {
    "temporal": (),
    "regime": (),
    "options_flow": (),
    "posture": ("regime",),
    "eligibility": ("posture",),
    "execution": (
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
    ),
}
CLOSED_AUTHORITIES: Final = (
    "prepared_truth",
    "packet_identity",
    "coefficient_modifier",
    "playbook_eligibility",
    "parallel_risk",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "transaction",
    "replay",
)
_EFFECTIVE_AT = datetime(2026, 7, 31, 8, 0, tzinfo=UTC)
AuthorityRef = tuple[str, str, str, str]
Pair = tuple[str, str]


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if hasattr(value, "__dataclass_fields__"):
        return _canonical(asdict(value))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def fingerprint(value: Any) -> str:
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class ContextCase:
    context_id: str
    contract_version: str
    prepared_id: str
    prepared_schema_version: str
    prepared_fingerprint: str
    prepared_input_fingerprint: str
    source_capture_refs: tuple[tuple[str, str], ...]
    preparation_policy_version: str
    alignment_policy_version: str
    fingerprint_policy_version: str
    canonicalisation_version: str
    derivation_versions: tuple[Pair, ...]
    effective_at_utc: datetime
    prepared_validation_state: str
    prepared_completeness_state: str
    serial_order_version: str
    runner_version: str
    mapping_policy_versions: tuple[Pair, ...]
    limitations: tuple[str, ...]
    unavailable_owner_facts: tuple[str, ...]
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool
    semantic_fingerprint: str


@dataclass(frozen=True)
class StageInputCase:
    stage: str
    context_id: str
    context_fingerprint: str
    contract_version: str
    carrier_stage: str
    carrier_id: str
    carrier_contract_version: str
    carrier_schema_version: str
    carrier_fingerprint: str
    authority_refs: tuple[AuthorityRef, ...]
    missing_state: str | None = None


@dataclass(frozen=True)
class StageOutputCase:
    output_id: str
    stage: str
    owner_id: str
    contract_version: str
    context_id: str
    context_fingerprint: str
    dependency_output_ids: tuple[str, ...]
    dependency_fingerprints: tuple[str, ...]
    status: str
    result_refs: tuple[Pair, ...]
    reasons: tuple[str, ...]
    consumed_authority_refs: tuple[AuthorityRef, ...]
    packet_refs: tuple[tuple[str, str], ...]
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool
    semantic_fingerprint: str


@dataclass(frozen=True)
class SerialResultCase:
    status: str
    reasons: tuple[str, ...]
    failed_stage: str | None
    candidate_id: str | None
    candidate_schema_version: str
    context_id: str
    context_fingerprint: str
    prepared_id: str
    prepared_fingerprint: str
    stage_order_version: str
    stage_outputs: tuple[StageOutputCase, ...]
    posture_status: str | None
    posture_reasons: tuple[str, ...]
    m07_authority_refs: tuple[AuthorityRef, ...]
    m08_authority_refs: tuple[AuthorityRef, ...]
    selected_playbook_family_id: str | None
    selected_playbook_family_version: str | None
    selected_playbook_id: str | None
    selected_playbook_version: str | None
    selected_setup_variant_id: str | None
    selected_setup_variant_version: str | None
    expression_id: str | None
    expression_version: str | None
    expression_fingerprint: str | None
    lifecycle_intent: tuple[Pair, ...]
    limitations: tuple[str, ...]
    closed_authority_classes: tuple[str, ...]
    foreign_authority_claimed: bool
    semantic_fingerprint: str


def _context_material(context: ContextCase) -> dict[str, Any]:
    material = asdict(context)
    material.pop("semantic_fingerprint")
    return material


def valid_context(**overrides: Any) -> ContextCase:
    base: dict[str, Any] = {
        "context_id": "context.m05.001",
        "contract_version": "1.0.0",
        "prepared_id": "prepared.m03.001",
        "prepared_schema_version": "1.0.0",
        "prepared_fingerprint": "a" * 64,
        "prepared_input_fingerprint": "b" * 64,
        "source_capture_refs": (
            ("source.market.001", "capture.market.001"),
            ("source.options.001", "capture.options.001"),
        ),
        "preparation_policy_version": "prepare.1.0.0",
        "alignment_policy_version": "alignment.1.0.0",
        "fingerprint_policy_version": "fingerprint.1.0.0",
        "canonicalisation_version": "canonical.1.0.0",
        "derivation_versions": (("nvda_return_pct", "derive.1.0.0"),),
        "effective_at_utc": _EFFECTIVE_AT,
        "prepared_validation_state": "valid",
        "prepared_completeness_state": "complete",
        "serial_order_version": "serial-order.1.0.0",
        "runner_version": "serial-runner.1.0.0",
        "mapping_policy_versions": tuple(
            (stage, f"mapping.{stage}.1.0.0") for stage in SERIAL_STAGE_ORDER
        ),
        "limitations": (),
        "unavailable_owner_facts": (),
        "closed_authority_classes": CLOSED_AUTHORITIES,
        "foreign_authority_claimed": False,
        "semantic_fingerprint": "",
    }
    base.update(overrides)
    provisional = ContextCase(**base)
    return replace(provisional, semantic_fingerprint=fingerprint(_context_material(provisional)))


def _ref(owner: str, identity: str, version: str, marker: str) -> AuthorityRef:
    return owner, identity, version, marker * 64


def valid_inputs(
    context: ContextCase | None = None,
    *,
    order: tuple[str, ...] = SERIAL_STAGE_ORDER,
) -> tuple[StageInputCase, ...]:
    context = context or valid_context()
    refs: dict[str, tuple[AuthorityRef, ...]] = {
        "temporal": (_ref("m03", context.prepared_id, context.prepared_schema_version, "a"),),
        "regime": (_ref("m03", context.prepared_id, context.prepared_schema_version, "a"),),
        "options_flow": (_ref("m03", context.prepared_id, context.prepared_schema_version, "a"),),
        "posture": (
            _ref("m07", "bundle.m07.001", "1.0.0", "c"),
            _ref("m07", "decision.m07.001", "1.0.0", "d"),
            _ref("m07", "receipt.m07.001", "1.0.0", "e"),
        ),
        "eligibility": (
            _ref("m08", "catalogue.m08.001", "1.0.0", "f"),
            _ref("m08", "eligibility.m08.001", "1.0.0", "1"),
            _ref("m08", "eligibility-lead.m08.001", "1.0.0", "2"),
        ),
        "execution": (
            _ref("m08", "eligibility.m08.001", "1.0.0", "1"),
            _ref("m08", "eligibility-lead.m08.001", "1.0.0", "2"),
        ),
    }
    return tuple(
        StageInputCase(
            stage=stage,
            context_id=context.context_id,
            context_fingerprint=context.semantic_fingerprint,
            contract_version="1.0.0",
            carrier_stage=stage,
            carrier_id=f"carrier.{stage}.001",
            carrier_contract_version=f"{stage}.contract.1.0.0",
            carrier_schema_version="1.0.0",
            carrier_fingerprint=fingerprint(
                {
                    "stage": stage,
                    "context": context.semantic_fingerprint,
                    "authority_refs": refs[stage],
                }
            ),
            authority_refs=refs[stage],
        )
        for stage in order
    )


def _output_material(output: StageOutputCase) -> dict[str, Any]:
    material = asdict(output)
    material.pop("output_id")
    material.pop("semantic_fingerprint")
    return material


def _result_material(result: SerialResultCase) -> dict[str, Any]:
    material = asdict(result)
    material.pop("candidate_id")
    material.pop("semantic_fingerprint")
    return material


class FixedHandler:
    """One deterministic stage owner used by the reference runner."""

    def __init__(self, stage: str, *, status: str = "complete", reasons: tuple[str, ...] = ()):
        self.stage = stage
        self.status = status
        self.reasons = reasons

    def __call__(
        self,
        stage_input: StageInputCase,
        dependencies: tuple[StageOutputCase, ...],
    ) -> StageOutputCase:
        result_refs: tuple[Pair, ...]
        if self.stage == "posture":
            result_refs = (
                ("posture_status", "permitted" if self.status == "complete" else "blocked"),
            )
        elif self.stage == "eligibility":
            result_refs = (
                ("eligibility_status", "eligible" if self.status == "complete" else "stand_down"),
            )
        elif self.stage == "execution":
            result_refs = (
                ("playbook_family_id", "family.breakout"),
                ("playbook_family_version", "1.0.0"),
                ("playbook_id", "playbook.breakout"),
                ("playbook_version", "1.0.0"),
                ("setup_variant_id", "variant.confirmed"),
                ("setup_variant_version", "1.0.0"),
                ("expression_id", "expression.breakout.001"),
                ("expression_version", "1.0.0"),
                ("expression_fingerprint", "3" * 64),
                ("lifecycle.horizon_class", "intraday"),
                ("lifecycle.handoff_schema", "m11.intent.1.0.0"),
            )
        else:
            result_refs = ((f"{self.stage}_context_id", f"{self.stage}.context.001"),)
        provisional = StageOutputCase(
            output_id="",
            stage=self.stage,
            owner_id={
                "temporal": "temporal_context",
                "regime": "market_regime_context",
                "options_flow": "options_flow",
                "posture": "posture_permission",
                "eligibility": "playbook_eligibility",
                "execution": "candidate_expression",
            }[self.stage],
            contract_version="1.0.0",
            context_id=stage_input.context_id,
            context_fingerprint=stage_input.context_fingerprint,
            dependency_output_ids=tuple(item.output_id for item in dependencies),
            dependency_fingerprints=tuple(item.semantic_fingerprint for item in dependencies),
            status=self.status,
            result_refs=result_refs,
            reasons=self.reasons,
            consumed_authority_refs=stage_input.authority_refs,
            packet_refs=(),
            closed_authority_classes=CLOSED_AUTHORITIES,
            foreign_authority_claimed=False,
            semantic_fingerprint="",
        )
        output_fp = fingerprint(_output_material(provisional))
        return replace(
            provisional,
            output_id=f"stage.{self.stage}.{output_fp[:16]}",
            semantic_fingerprint=output_fp,
        )


def valid_handlers(
    *,
    terminal_stage: str | None = None,
    terminal_status: str = "stand_down",
) -> dict[str, Callable[[StageInputCase, tuple[StageOutputCase, ...]], StageOutputCase]]:
    handlers: dict[
        str, Callable[[StageInputCase, tuple[StageOutputCase, ...]], StageOutputCase]
    ] = {}
    for stage in SERIAL_STAGE_ORDER:
        status = terminal_status if stage == terminal_stage else "complete"
        reasons = (f"{stage}_{status}",) if status != "complete" else ()
        handlers[stage] = FixedHandler(stage, status=status, reasons=reasons)
    return handlers


class ReferenceRunner:
    """Deterministic coordinator implementing only the admitted M05 K08/K09 law."""

    def run(
        self,
        context: ContextCase,
        stage_inputs: tuple[StageInputCase, ...],
        handlers: dict[
            str, Callable[[StageInputCase, tuple[StageOutputCase, ...]], StageOutputCase]
        ],
    ) -> SerialResultCase:
        self._validate_context(context)
        inputs = self._normalise_inputs(context, stage_inputs)
        if set(handlers) != set(SERIAL_STAGE_ORDER):
            raise ValueError("exact_six_stage_handlers_required")

        outputs: dict[str, StageOutputCase] = {}
        for stage in SERIAL_STAGE_ORDER:
            dependencies = tuple(outputs[name] for name in SERIAL_STAGE_DEPENDENCIES[stage])
            output = handlers[stage](inputs[stage], dependencies)
            self._validate_output(context, inputs[stage], dependencies, output)
            outputs[stage] = output
            if output.status == "stand_down":
                if stage not in {"posture", "eligibility"}:
                    raise ValueError("stand_down_stage_not_authorised")
                return self._build_result(
                    context,
                    tuple(outputs[name] for name in SERIAL_STAGE_ORDER if name in outputs),
                    status="stand_down",
                    reasons=output.reasons,
                    failed_stage=stage,
                )
            if output.status in {"withheld", "rejected"}:
                return self._build_result(
                    context,
                    tuple(outputs[name] for name in SERIAL_STAGE_ORDER if name in outputs),
                    status=output.status,
                    reasons=output.reasons,
                    failed_stage=stage,
                )
            if output.status != "complete":
                raise ValueError("unknown_stage_output_status")

        return self._build_result(
            context,
            tuple(outputs[stage] for stage in SERIAL_STAGE_ORDER),
            status="formed",
            reasons=(),
            failed_stage=None,
        )

    @staticmethod
    def _validate_context(context: ContextCase) -> None:
        if context.effective_at_utc.tzinfo is None or context.effective_at_utc.utcoffset() is None:
            raise ValueError("context_effective_at_must_be_timezone_aware")
        if (
            context.closed_authority_classes != CLOSED_AUTHORITIES
            or context.foreign_authority_claimed
        ):
            raise ValueError("context_foreign_authority_claimed")
        if context.semantic_fingerprint != fingerprint(_context_material(context)):
            raise ValueError("context_fingerprint_mismatch")
        if tuple(name for name, _ in context.mapping_policy_versions) != SERIAL_STAGE_ORDER:
            raise ValueError("mapping_policy_versions_must_cover_exact_stage_order")
        required = (
            context.context_id,
            context.contract_version,
            context.prepared_id,
            context.prepared_schema_version,
            context.prepared_fingerprint,
            context.prepared_input_fingerprint,
            context.preparation_policy_version,
            context.alignment_policy_version,
            context.fingerprint_policy_version,
            context.canonicalisation_version,
            context.serial_order_version,
            context.runner_version,
        )
        if any(not item for item in required) or not context.source_capture_refs:
            raise ValueError("context_lineage_incomplete")

    @staticmethod
    def _normalise_inputs(
        context: ContextCase, stage_inputs: tuple[StageInputCase, ...]
    ) -> dict[str, StageInputCase]:
        if len(stage_inputs) != len(SERIAL_STAGE_ORDER):
            raise ValueError("exact_six_stage_inputs_required")
        by_stage = {item.stage: item for item in stage_inputs}
        if set(by_stage) != set(SERIAL_STAGE_ORDER) or len(by_stage) != len(stage_inputs):
            raise ValueError("stage_input_identity_set_invalid")
        for stage, item in by_stage.items():
            if item.carrier_stage != stage:
                raise ValueError("carrier_stage_mismatch")
            if (
                item.context_id != context.context_id
                or item.context_fingerprint != context.semantic_fingerprint
            ):
                raise ValueError("stage_input_context_mismatch")
            if not all(
                (
                    item.contract_version,
                    item.carrier_id,
                    item.carrier_contract_version,
                    item.carrier_schema_version,
                    item.carrier_fingerprint,
                )
            ):
                raise ValueError("stage_input_lineage_incomplete")
        return by_stage

    @staticmethod
    def _validate_output(
        context: ContextCase,
        stage_input: StageInputCase,
        dependencies: tuple[StageOutputCase, ...],
        output: StageOutputCase,
    ) -> None:
        expected_ids = tuple(item.output_id for item in dependencies)
        expected_fps = tuple(item.semantic_fingerprint for item in dependencies)
        if output.stage != stage_input.stage:
            raise ValueError("stage_output_identity_mismatch")
        if (
            output.context_id != context.context_id
            or output.context_fingerprint != context.semantic_fingerprint
        ):
            raise ValueError("stage_output_context_mismatch")
        if (
            output.dependency_output_ids != expected_ids
            or output.dependency_fingerprints != expected_fps
        ):
            raise ValueError("stage_output_dependency_lineage_mismatch")
        if output.consumed_authority_refs != stage_input.authority_refs:
            raise ValueError("stage_output_authority_lineage_mismatch")
        if (
            output.closed_authority_classes != CLOSED_AUTHORITIES
            or output.foreign_authority_claimed
        ):
            raise ValueError("stage_output_foreign_authority_claimed")
        expected_fp = fingerprint(_output_material(output))
        if output.semantic_fingerprint != expected_fp:
            raise ValueError("stage_output_fingerprint_mismatch")
        if output.output_id != f"stage.{output.stage}.{expected_fp[:16]}":
            raise ValueError("stage_output_identity_not_deterministic")

    def _build_result(
        self,
        context: ContextCase,
        outputs: tuple[StageOutputCase, ...],
        *,
        status: str,
        reasons: tuple[str, ...],
        failed_stage: str | None,
    ) -> SerialResultCase:
        by_stage = {item.stage: item for item in outputs}
        posture = by_stage.get("posture")
        eligibility = by_stage.get("eligibility")
        execution = by_stage.get("execution")
        posture_refs = dict(posture.result_refs) if posture else {}
        execution_refs = dict(execution.result_refs) if execution else {}
        m07_refs = tuple(
            ref for ref in (posture.consumed_authority_refs if posture else ()) if ref[0] == "m07"
        )
        m08_refs = tuple(
            ref
            for output in (eligibility, execution)
            if output is not None
            for ref in output.consumed_authority_refs
            if ref[0] == "m08"
        )
        m08_refs = tuple(dict.fromkeys(m08_refs))
        formed = status == "formed"
        if formed:
            if tuple(item.stage for item in outputs) != SERIAL_STAGE_ORDER:
                raise ValueError("formed_result_requires_all_six_outputs")
            if posture_refs.get("posture_status") != "permitted":
                raise ValueError("formed_result_requires_permitted_posture")
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
        lifecycle = tuple(
            (key.removeprefix("lifecycle."), value)
            for key, value in execution_refs.items()
            if key.startswith("lifecycle.")
        )
        provisional = SerialResultCase(
            status=status,
            reasons=reasons,
            failed_stage=failed_stage,
            candidate_id=None,
            candidate_schema_version="1.0.0",
            context_id=context.context_id,
            context_fingerprint=context.semantic_fingerprint,
            prepared_id=context.prepared_id,
            prepared_fingerprint=context.prepared_fingerprint,
            stage_order_version=context.serial_order_version,
            stage_outputs=outputs,
            posture_status=posture_refs.get("posture_status"),
            posture_reasons=posture.reasons if posture else (),
            m07_authority_refs=m07_refs,
            m08_authority_refs=m08_refs,
            selected_playbook_family_id=(
                execution_refs.get("playbook_family_id") if formed else None
            ),
            selected_playbook_family_version=(
                execution_refs.get("playbook_family_version") if formed else None
            ),
            selected_playbook_id=execution_refs.get("playbook_id") if formed else None,
            selected_playbook_version=execution_refs.get("playbook_version") if formed else None,
            selected_setup_variant_id=execution_refs.get("setup_variant_id") if formed else None,
            selected_setup_variant_version=(
                execution_refs.get("setup_variant_version") if formed else None
            ),
            expression_id=execution_refs.get("expression_id") if formed else None,
            expression_version=execution_refs.get("expression_version") if formed else None,
            expression_fingerprint=execution_refs.get("expression_fingerprint") if formed else None,
            lifecycle_intent=lifecycle if formed else (),
            limitations=context.limitations,
            closed_authority_classes=CLOSED_AUTHORITIES,
            foreign_authority_claimed=False,
            semantic_fingerprint="",
        )
        result_fp = fingerprint(_result_material(provisional))
        candidate_id = f"serial.{result_fp[:16]}" if formed else None
        return replace(
            provisional,
            candidate_id=candidate_id,
            semantic_fingerprint=result_fp,
        )


def validate_result_law(
    result: SerialResultCase,
    context: ContextCase,
    *,
    submitted_stages: tuple[str, ...] = SERIAL_STAGE_ORDER,
) -> None:
    if set(submitted_stages) != set(SERIAL_STAGE_ORDER) or len(submitted_stages) != 6:
        raise ValueError("submitted_stage_set_incomplete")
    if (
        result.context_id != context.context_id
        or result.context_fingerprint != context.semantic_fingerprint
    ):
        raise ValueError("result_context_mismatch")
    if (
        result.prepared_id != context.prepared_id
        or result.prepared_fingerprint != context.prepared_fingerprint
    ):
        raise ValueError("result_prepared_lineage_mismatch")
    if result.closed_authority_classes != CLOSED_AUTHORITIES or result.foreign_authority_claimed:
        raise ValueError("result_foreign_authority_claimed")
    observed = tuple(item.stage for item in result.stage_outputs)
    if observed != SERIAL_STAGE_ORDER[: len(observed)]:
        raise ValueError("result_stage_order_invalid")
    for output in result.stage_outputs:
        if output.semantic_fingerprint != fingerprint(_output_material(output)):
            raise ValueError("result_contains_invalid_stage_output")
    expected_fp = fingerprint(_result_material(result))
    if result.semantic_fingerprint != expected_fp:
        raise ValueError("result_fingerprint_mismatch")
    if result.status == "formed":
        if observed != SERIAL_STAGE_ORDER or result.failed_stage is not None:
            raise ValueError("formed_result_incomplete")
        if result.candidate_id != f"serial.{expected_fp[:16]}":
            raise ValueError("formed_candidate_identity_invalid")
        if not result.m07_authority_refs or not result.m08_authority_refs:
            raise ValueError("formed_authority_lineage_incomplete")
        if any(
            item is None
            for item in (
                result.selected_playbook_family_id,
                result.selected_playbook_family_version,
                result.selected_playbook_id,
                result.selected_playbook_version,
                result.selected_setup_variant_id,
                result.selected_setup_variant_version,
                result.expression_id,
                result.expression_version,
                result.expression_fingerprint,
            )
        ):
            raise ValueError("formed_expression_lineage_incomplete")
    elif result.status == "stand_down":
        if result.candidate_id is not None or result.failed_stage not in {"posture", "eligibility"}:
            raise ValueError("stand_down_candidate_or_stage_invalid")
    elif result.status in {"withheld", "rejected"}:
        if result.candidate_id is not None or result.failed_stage not in SERIAL_STAGE_ORDER:
            raise ValueError("failed_result_candidate_or_stage_invalid")
    else:
        raise ValueError("unknown_serial_result_status")


class CallerOrderRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        by_stage = {item.stage: item for item in result.stage_outputs}
        return replace(result, stage_outputs=tuple(by_stage[item.stage] for item in stage_inputs))


class SkippedStageRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        return replace(
            result,
            stage_outputs=tuple(
                item for item in result.stage_outputs if item.stage != "options_flow"
            ),
        )


class PartialSuccessRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        existing = {item.stage for item in stage_inputs}
        completed = stage_inputs + tuple(
            item for item in valid_inputs(context) if item.stage not in existing
        )
        return super().run(context, completed, handlers)


class FabricatedIdentityRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        return replace(result, context_id="generated.current-time.context")


class DroppedLineageRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        return replace(result, m07_authority_refs=())


class EmptyEligibilityAuthorityRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        return replace(result, m08_authority_refs=())


class ForeignAuthorityRunner(ReferenceRunner):
    def run(self, context, stage_inputs, handlers):
        result = super().run(context, stage_inputs, handlers)
        return replace(
            result,
            closed_authority_classes=tuple(
                item for item in CLOSED_AUTHORITIES if item != "capital"
            ),
            foreign_authority_claimed=True,
        )


MUTANTS: Final = {
    "caller_order": CallerOrderRunner,
    "skipped_stage": SkippedStageRunner,
    "partial_success": PartialSuccessRunner,
    "fabricated_identity": FabricatedIdentityRunner,
    "dropped_lineage": DroppedLineageRunner,
    "empty_eligibility_authority": EmptyEligibilityAuthorityRunner,
    "foreign_authority": ForeignAuthorityRunner,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m05_serial_cognition")
    required = ("StageContext", "StageInput", "StageOutput", "SerialCandidate", "SerialRunner")
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M05 package is missing exports: {missing}")
    return {name: getattr(module, name) for name in required}


def production_context_payload(context: ContextCase | None = None) -> dict[str, Any]:
    item = context or valid_context()
    return asdict(item)


def _production_carrier_fact_payload(
    *,
    fact_id: str,
    owner_id: str,
    contract_version: str,
    value: Any,
) -> dict[str, Any]:
    payload = {
        "fact_id": fact_id,
        "owner_id": owner_id,
        "contract_version": contract_version,
        "value": value,
    }
    payload["semantic_fingerprint"] = fingerprint(payload)
    return payload


def production_stage_input_payload(stage_input: StageInputCase) -> dict[str, Any]:
    facts: dict[str, tuple[dict[str, Any], ...]] = {
        "temporal": (
            _production_carrier_fact_payload(
                fact_id="effective_at_utc",
                owner_id="m03",
                contract_version="m03.prepared.1.0.0",
                value=_EFFECTIVE_AT,
            ),
        ),
        "regime": (
            _production_carrier_fact_payload(
                fact_id="vix_level",
                owner_id="m03",
                contract_version="m03.prepared.1.0.0",
                value=18.5,
            ),
        ),
        "options_flow": (
            _production_carrier_fact_payload(
                fact_id="spot_price",
                owner_id="m03",
                contract_version="m03.prepared.1.0.0",
                value=101.0,
            ),
        ),
        "posture": (
            _production_carrier_fact_payload(
                fact_id="modifier_decision_status",
                owner_id="m07",
                contract_version="m07.modifier-decision.1.0.0",
                value="applied",
            ),
        ),
        "eligibility": (
            _production_carrier_fact_payload(
                fact_id="eligibility_status",
                owner_id="m08",
                contract_version="m08.eligibility-decision.1.0.0",
                value="eligible",
            ),
            _production_carrier_fact_payload(
                fact_id="eligibility_lead_id",
                owner_id="m08",
                contract_version="m08.eligibility-decision.1.0.0",
                value="playbook.breakout",
            ),
            _production_carrier_fact_payload(
                fact_id="ordered_eligible_candidate_ids",
                owner_id="m08",
                contract_version="m08.eligibility-decision.1.0.0",
                value=("playbook.breakout",),
            ),
        ),
        "execution": (
            _production_carrier_fact_payload(
                fact_id="eligibility_lead_id",
                owner_id="m08",
                contract_version="m08.eligibility-decision.1.0.0",
                value="playbook.breakout",
            ),
            _production_carrier_fact_payload(
                fact_id="expression_policy_ref",
                owner_id="m08",
                contract_version="m08.eligibility-decision.1.0.0",
                value="expression-policy.1.0.0",
            ),
        ),
    }
    payload = asdict(stage_input)
    payload["carrier_facts"] = facts[stage_input.stage]
    material = dict(payload)
    material.pop("carrier_fingerprint")
    payload["carrier_fingerprint"] = fingerprint(material)
    return payload


def production_output_payload(
    stage_input: Any,
    dependencies: tuple[Any, ...],
    *,
    status: str = "complete",
    reasons: tuple[str, ...] = (),
) -> dict[str, Any]:
    stage_input_payload = stage_input.model_dump(mode="python")
    case_input = StageInputCase(
        **{
            field_name: stage_input_payload[field_name]
            for field_name in StageInputCase.__dataclass_fields__
        }
    )
    case_dependencies = tuple(
        StageOutputCase(
            **{
                field_name: item.model_dump(mode="python")[field_name]
                for field_name in StageOutputCase.__dataclass_fields__
            }
        )
        for item in dependencies
    )
    case = FixedHandler(case_input.stage, status=status, reasons=reasons)(
        case_input, case_dependencies
    )
    payload = asdict(case)
    if case_input.stage == "eligibility" and status == "complete":
        payload["result_refs"] = (
            ("eligibility_status", "eligible"),
            ("eligibility_lead_id", "playbook.breakout"),
            ("eligible_candidate.000", "playbook.breakout"),
        )
    if case_input.stage == "execution" and status != "complete":
        payload["result_refs"] = ()
    payload["schema_version"] = "1.0.0"
    payload["input_carrier_id"] = stage_input.carrier_id
    payload["input_carrier_fingerprint"] = stage_input.carrier_fingerprint
    material = dict(payload)
    material.pop("output_id")
    material.pop("semantic_fingerprint")
    output_fingerprint = fingerprint(material)
    payload["semantic_fingerprint"] = output_fingerprint
    payload["output_id"] = f"stage.{case_input.stage}.{output_fingerprint[:16]}"
    return payload


def production_handlers(
    api: dict[str, Any],
    *,
    terminal_stage: str | None = None,
    terminal_status: str = "stand_down",
) -> dict[str, Callable[[Any, tuple[Any, ...]], Any]]:
    handlers: dict[str, Callable[[Any, tuple[Any, ...]], Any]] = {}
    for stage in SERIAL_STAGE_ORDER:
        status = terminal_status if stage == terminal_stage else "complete"
        reasons = (f"{stage}_{status}",) if status != "complete" else ()

        def handler(stage_input, dependencies, *, _status=status, _reasons=reasons):
            return api["StageOutput"].model_validate(
                production_output_payload(
                    stage_input,
                    dependencies,
                    status=_status,
                    reasons=_reasons,
                )
            )

        handlers[stage] = handler
    return handlers
