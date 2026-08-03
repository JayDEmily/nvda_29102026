"""M05 K08/K09 proof for common stage context and ordered serial candidate law."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from typing import Any

import pytest
from tests.support.m05_k08_k09_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    SERIAL_STAGE_ORDER,
    ReferenceRunner,
    fingerprint,
    production_api,
    production_context_payload,
    production_handlers,
    production_stage_input_payload,
    valid_context,
    valid_handlers,
    valid_inputs,
    validate_result_law,
)


def test_reference_formed_result_is_exact_order_deterministic_and_lineage_complete() -> None:
    context = valid_context()
    runner = ReferenceRunner()
    reversed_inputs = valid_inputs(context, order=tuple(reversed(SERIAL_STAGE_ORDER)))

    first = runner.run(context, reversed_inputs, valid_handlers())
    second = runner.run(context, valid_inputs(context), valid_handlers())

    validate_result_law(first, context)
    validate_result_law(second, context)
    assert first == second
    assert first.status == "formed"
    assert tuple(item.stage for item in first.stage_outputs) == SERIAL_STAGE_ORDER
    assert first.candidate_id == f"serial.{first.semantic_fingerprint[:16]}"
    assert {item[0] for item in first.m07_authority_refs} == {"m07"}
    assert {item[0] for item in first.m08_authority_refs} == {"m08"}
    assert first.selected_playbook_id == "playbook.breakout"
    assert first.expression_id == "expression.breakout.001"
    assert dict(first.lifecycle_intent)["handoff_schema"] == "m11.intent.1.0.0"


def test_reference_context_binds_material_versions_time_and_closed_authority() -> None:
    context = valid_context()
    runner = ReferenceRunner()

    runner.run(context, valid_inputs(context), valid_handlers())

    with pytest.raises(ValueError, match="context_fingerprint_mismatch"):
        runner.run(
            replace(context, runner_version="serial-runner.2.0.0"),
            valid_inputs(context),
            valid_handlers(),
        )
    with pytest.raises(ValueError, match="context_effective_at_must_be_timezone_aware"):
        naive = replace(context, effective_at_utc=datetime(2026, 7, 31, 8, 0))
        runner.run(naive, valid_inputs(naive), valid_handlers())
    with pytest.raises(ValueError, match="context_foreign_authority_claimed"):
        forged = replace(
            context,
            closed_authority_classes=tuple(
                item for item in CLOSED_AUTHORITIES if item != "capital"
            ),
            foreign_authority_claimed=True,
        )
        runner.run(forged, valid_inputs(forged), valid_handlers())


def test_reference_requires_exact_stage_input_set_and_matching_typed_carriers() -> None:
    context = valid_context()
    runner = ReferenceRunner()
    inputs = valid_inputs(context)

    with pytest.raises(ValueError, match="exact_six_stage_inputs_required"):
        runner.run(context, inputs[:-1], valid_handlers())
    with pytest.raises(ValueError, match="carrier_stage_mismatch"):
        runner.run(
            context,
            (replace(inputs[0], carrier_stage="regime"), *inputs[1:]),
            valid_handlers(),
        )
    with pytest.raises(ValueError, match="stage_input_context_mismatch"):
        runner.run(
            context,
            (replace(inputs[0], context_id="other.context"), *inputs[1:]),
            valid_handlers(),
        )


def test_reference_stage_outputs_require_exact_dependency_and_authority_lineage() -> None:
    context = valid_context()
    runner = ReferenceRunner()
    handlers = valid_handlers()
    normal = handlers["posture"]

    def bad_posture(stage_input, dependencies):
        output = normal(stage_input, dependencies)
        return replace(output, dependency_output_ids=())

    handlers["posture"] = bad_posture
    with pytest.raises(ValueError, match="stage_output_dependency_lineage_mismatch"):
        runner.run(context, valid_inputs(context), handlers)

    handlers = valid_handlers()
    normal_eligibility = handlers["eligibility"]

    def bad_eligibility(stage_input, dependencies):
        output = normal_eligibility(stage_input, dependencies)
        return replace(output, consumed_authority_refs=())

    handlers["eligibility"] = bad_eligibility
    with pytest.raises(ValueError, match="stage_output_authority_lineage_mismatch"):
        runner.run(context, valid_inputs(context), handlers)


def test_reference_lawful_stand_down_is_explicit_and_emits_no_candidate() -> None:
    context = valid_context()
    runner = ReferenceRunner()

    posture = runner.run(
        context,
        valid_inputs(context),
        valid_handlers(terminal_stage="posture"),
    )
    validate_result_law(posture, context)
    assert posture.status == "stand_down"
    assert posture.failed_stage == "posture"
    assert posture.candidate_id is None
    assert tuple(item.stage for item in posture.stage_outputs) == SERIAL_STAGE_ORDER[:4]

    eligibility = runner.run(
        context,
        valid_inputs(context),
        valid_handlers(terminal_stage="eligibility"),
    )
    validate_result_law(eligibility, context)
    assert eligibility.status == "stand_down"
    assert eligibility.failed_stage == "eligibility"
    assert eligibility.candidate_id is None
    assert tuple(item.stage for item in eligibility.stage_outputs) == SERIAL_STAGE_ORDER[:5]


def test_reference_withheld_and_rejected_are_terminal_without_binding_candidate() -> None:
    context = valid_context()
    runner = ReferenceRunner()

    withheld = runner.run(
        context,
        valid_inputs(context),
        valid_handlers(terminal_stage="options_flow", terminal_status="withheld"),
    )
    validate_result_law(withheld, context)
    assert withheld.status == "withheld"
    assert withheld.failed_stage == "options_flow"
    assert withheld.candidate_id is None

    rejected = runner.run(
        context,
        valid_inputs(context),
        valid_handlers(terminal_stage="regime", terminal_status="rejected"),
    )
    validate_result_law(rejected, context)
    assert rejected.status == "rejected"
    assert rejected.failed_stage == "regime"
    assert rejected.candidate_id is None


@pytest.mark.parametrize("mutant_name", sorted(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    context = valid_context()
    runner = MUTANTS[mutant_name]()
    inputs = valid_inputs(
        context,
        order=(
            tuple(reversed(SERIAL_STAGE_ORDER))
            if mutant_name == "caller_order"
            else SERIAL_STAGE_ORDER
        ),
    )
    submitted = tuple(item.stage for item in inputs)
    if mutant_name == "partial_success":
        inputs = inputs[:-1]
        submitted = tuple(item.stage for item in inputs)

    result = runner.run(context, inputs, valid_handlers())
    with pytest.raises(ValueError):
        validate_result_law(result, context, submitted_stages=submitted)


# Production-facing assertions below are intentionally exact red at C-PROOF until
# the canonical nvda_desk.m05_serial_cognition package exists.


def _production_context_and_inputs(api: dict[str, Any]):
    context_case = valid_context()
    context = api["StageContext"].model_validate(production_context_payload(context_case))
    inputs = tuple(
        api["StageInput"].model_validate(production_stage_input_payload(item))
        for item in valid_inputs(context_case, order=tuple(reversed(SERIAL_STAGE_ORDER)))
    )
    return context_case, context, inputs


def test_production_exports_exact_frozen_public_contracts() -> None:
    api = production_api()
    assert set(api) == {
        "StageContext",
        "StageInput",
        "StageOutput",
        "SerialCandidate",
        "SerialRunner",
    }
    for name in ("StageContext", "StageInput", "StageOutput", "SerialCandidate"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"

    assert set(api["StageInput"].model_fields) == {
        "stage",
        "context_id",
        "context_fingerprint",
        "contract_version",
        "carrier_stage",
        "carrier_id",
        "carrier_contract_version",
        "carrier_schema_version",
        "carrier_facts",
        "carrier_fingerprint",
        "authority_refs",
        "missing_state",
    }


def test_production_stage_context_revalidates_lineage_and_forbids_foreign_authority() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )

    assert runner.run(context=context, stage_inputs=inputs).status == "formed"

    forged = context.model_copy(update={"runner_version": "serial-runner.2.0.0"})
    with pytest.raises(ValueError, match="context_fingerprint_mismatch"):
        runner.run(context=forged, stage_inputs=inputs)

    foreign = context.model_copy(update={"foreign_authority_claimed": True})
    with pytest.raises(ValueError, match="context_foreign_authority_claimed"):
        runner.run(context=foreign, stage_inputs=inputs)


def test_production_stage_input_is_narrow_tagged_and_context_bound() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)

    with pytest.raises(ValueError):
        api["StageInput"].model_validate(
            {
                **production_stage_input_payload(valid_inputs(context_case)[0]),
                "payload": {"whole_prepared_envelope": "not_allowed"},
            }
        )

    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    bad = inputs[0].model_copy(update={"carrier_stage": "regime"})
    with pytest.raises(ValueError, match="carrier_stage_mismatch"):
        runner.run(context=context, stage_inputs=(bad, *inputs[1:]))


def test_production_runner_forms_exact_six_stage_candidate_independent_of_input_order() -> None:
    api = production_api()
    context_case, context, reversed_inputs = _production_context_and_inputs(api)
    ordered_inputs = tuple(
        api["StageInput"].model_validate(production_stage_input_payload(item))
        for item in valid_inputs(context_case)
    )
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )

    first = runner.run(context=context, stage_inputs=reversed_inputs)
    second = runner.run(context=context, stage_inputs=ordered_inputs)

    assert isinstance(first, api["SerialCandidate"])
    assert first == second
    assert first.status == "formed"
    assert tuple(item.stage for item in first.stage_outputs) == SERIAL_STAGE_ORDER
    assert first.serial_result_id == f"serial-result.{first.semantic_fingerprint[:16]}"
    assert first.candidate_id == f"serial.{first.semantic_fingerprint[:16]}"
    assert first.serial_result_id != first.candidate_id
    assert first.prepared_id == context.prepared_id
    assert first.context_fingerprint == context.semantic_fingerprint
    assert first.m07_authority_refs and first.m08_authority_refs
    assert first.selected_playbook_id == "playbook.breakout"
    assert first.expression_id == "expression.breakout.001"


def test_production_runner_preserves_lawful_stand_down_without_later_stage_execution() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)

    posture_runner = api["SerialRunner"](
        handlers=production_handlers(api, terminal_stage="posture"),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    posture = posture_runner.run(context=context, stage_inputs=inputs)
    assert posture.status == "stand_down"
    assert posture.failed_stage == "posture"
    assert posture.candidate_id is None
    assert tuple(item.stage for item in posture.stage_outputs) == SERIAL_STAGE_ORDER[:4]

    eligibility_runner = api["SerialRunner"](
        handlers=production_handlers(api, terminal_stage="eligibility"),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    eligibility = eligibility_runner.run(context=context, stage_inputs=inputs)
    assert eligibility.status == "stand_down"
    assert eligibility.failed_stage == "eligibility"
    assert eligibility.candidate_id is None
    assert tuple(item.stage for item in eligibility.stage_outputs) == SERIAL_STAGE_ORDER[:5]


def test_production_runner_rejects_partial_duplicate_and_dependency_forgery() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )

    with pytest.raises(ValueError, match="exact_six_stage_inputs_required"):
        runner.run(context=context, stage_inputs=inputs[:-1])
    with pytest.raises(ValueError, match="stage_input_identity_set_invalid"):
        runner.run(context=context, stage_inputs=(inputs[0], *inputs[:-1]))

    handlers = production_handlers(api)
    normal = handlers["posture"]

    def forged_handler(stage_input, dependencies):
        output = normal(stage_input, dependencies)
        return output.model_copy(update={"dependency_output_ids": ()})

    handlers["posture"] = forged_handler
    forged_runner = api["SerialRunner"](
        handlers=handlers,
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    with pytest.raises(ValueError, match="stage_output_dependency_lineage_mismatch"):
        forged_runner.run(context=context, stage_inputs=inputs)


def test_production_candidate_fingerprint_binds_complete_lineage_and_closed_authority() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)

    assert candidate.closed_authority_classes == CLOSED_AUTHORITIES
    assert candidate.foreign_authority_claimed is False
    assert {item[0] for item in candidate.m07_authority_refs} == {"m07"}
    assert {item[0] for item in candidate.m08_authority_refs} == {"m08"}
    assert dict(candidate.lifecycle_intent)["handoff_schema"] == "m11.intent.1.0.0"

    forged = candidate.model_copy(update={"m07_authority_refs": ()})
    with pytest.raises(ValueError, match="candidate_fingerprint_mismatch"):
        api["SerialCandidate"].model_validate(forged.model_dump(mode="python"))


def _refingerprint_stage_input(
    api: dict[str, Any],
    stage_input: Any,
    **updates: Any,
):
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    payload = stage_input.model_dump(mode="python")
    payload.update(updates)
    payload["carrier_facts"] = tuple(
        item.model_dump(mode="python") if hasattr(item, "model_dump") else item
        for item in payload["carrier_facts"]
    )
    material = dict(payload)
    material.pop("carrier_fingerprint")
    payload["carrier_fingerprint"] = fingerprint(material)
    return api["StageInput"].model_validate(payload)


def _refingerprint_output(api: dict[str, Any], output: Any, **updates: Any):
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    payload = output.model_dump(mode="python")
    payload.update(updates)
    material = dict(payload)
    material.pop("output_id")
    material.pop("semantic_fingerprint")
    output_fingerprint = fingerprint(material)
    payload["semantic_fingerprint"] = output_fingerprint
    payload["output_id"] = f"stage.{payload['stage']}.{output_fingerprint[:16]}"
    return api["StageOutput"].model_validate(payload)


def _refingerprint_candidate(api: dict[str, Any], candidate: Any, **updates: Any):
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    payload = candidate.model_dump(mode="python")
    payload.update(updates)
    payload["stage_outputs"] = tuple(
        item.model_dump(mode="python") if hasattr(item, "model_dump") else item
        for item in payload["stage_outputs"]
    )
    material = dict(payload)
    material.pop("serial_result_id")
    material.pop("candidate_id")
    material.pop("semantic_fingerprint")
    candidate_fingerprint = fingerprint(material)
    payload["semantic_fingerprint"] = candidate_fingerprint
    payload["serial_result_id"] = f"serial-result.{candidate_fingerprint[:16]}"
    payload["candidate_id"] = (
        f"serial.{candidate_fingerprint[:16]}" if payload["status"] == "formed" else None
    )
    return api["SerialCandidate"].model_validate(payload)


def test_production_candidate_rejects_refingerprinted_nested_context_forgery() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)
    forged_temporal = _refingerprint_output(
        api,
        candidate.stage_outputs[0],
        context_id="context.forged",
    )
    outputs = (forged_temporal, *candidate.stage_outputs[1:])

    with pytest.raises(ValueError, match="candidate_stage_context_lineage_mismatch"):
        _refingerprint_candidate(api, candidate, stage_outputs=outputs)


def test_production_candidate_rejects_refingerprinted_dependency_graph_forgery() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)
    forged_temporal = _refingerprint_output(
        api,
        candidate.stage_outputs[0],
        dependency_output_ids=("stage.regime.forged0000000",),
        dependency_fingerprints=("9" * 64,),
    )
    outputs = (forged_temporal, *candidate.stage_outputs[1:])

    with pytest.raises(ValueError, match="candidate_stage_dependency_lineage_mismatch"):
        _refingerprint_candidate(api, candidate, stage_outputs=outputs)


def test_production_candidate_rejects_refingerprinted_aggregated_authority_forgery() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)

    with pytest.raises(ValueError, match="candidate_authority_lineage_mismatch"):
        _refingerprint_candidate(
            api,
            candidate,
            m07_authority_refs=(("m07", "forged.m07", "1.0.0", "9" * 64),),
        )


def test_production_terminal_candidate_rejects_refingerprinted_formed_payload() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api, terminal_stage="posture"),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)

    with pytest.raises(ValueError, match="terminal_candidate_contains_formed_payload"):
        _refingerprint_candidate(
            api,
            candidate,
            expression_id="expression.forged",
            expression_version="1.0.0",
            expression_fingerprint="9" * 64,
        )


def test_production_runner_rejects_stage_input_foreign_owner_authority() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    forged = _refingerprint_stage_input(
        api,
        inputs[0],
        authority_refs=(("m07", "forged.m07", "1.0.0", "9" * 64),),
    )

    with pytest.raises(ValueError, match="stage_input_foreign_authority_ref"):
        runner.run(context=context, stage_inputs=(forged, *inputs[1:]))


def test_production_context_rejects_refingerprinted_noncanonical_source_order() -> None:
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    api = production_api()
    payload = production_context_payload(valid_context())
    payload["source_capture_refs"] = tuple(reversed(payload["source_capture_refs"]))
    material = dict(payload)
    material.pop("semantic_fingerprint")
    payload["semantic_fingerprint"] = fingerprint(material)

    with pytest.raises(ValueError, match="source_capture_refs_not_canonical"):
        api["StageContext"].model_validate(payload)


def test_production_stage_input_carries_bounded_facts_and_binds_them_to_fingerprint() -> None:
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    temporal = next(item for item in inputs if item.stage == "temporal")
    fact = temporal.carrier_facts[0]
    fact_payload = fact.model_dump(mode="python")
    fact_payload["value"] = datetime(2026, 7, 31, 9, 0, tzinfo=fact.value.tzinfo)
    fact_material = dict(fact_payload)
    fact_material.pop("semantic_fingerprint")
    fact_payload["semantic_fingerprint"] = fingerprint(fact_material)
    changed = _refingerprint_stage_input(
        api,
        temporal,
        carrier_facts=(fact_payload,),
    )

    handlers = production_handlers(api)
    normal = handlers["temporal"]

    def fact_aware_handler(stage_input, dependencies):
        output = normal(stage_input, dependencies)
        value = next(
            item.value for item in stage_input.carrier_facts if item.fact_id == "effective_at_utc"
        )
        return _refingerprint_output(
            api,
            output,
            result_refs=(("temporal_effective_at", value.isoformat()),),
        )

    handlers["temporal"] = fact_aware_handler
    runner = api["SerialRunner"](
        handlers=handlers,
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    first = runner.run(context=context, stage_inputs=inputs)
    changed_inputs = tuple(changed if item.stage == "temporal" else item for item in inputs)
    second = runner.run(context=context, stage_inputs=changed_inputs)

    assert first.semantic_fingerprint != second.semantic_fingerprint
    assert first.stage_outputs[0].input_carrier_fingerprint == temporal.carrier_fingerprint
    assert second.stage_outputs[0].input_carrier_fingerprint == changed.carrier_fingerprint


def test_production_stage_input_rejects_unadmitted_or_unbound_carrier_fact() -> None:
    from tests.support.m05_k08_k09_contract_harness import fingerprint

    api = production_api()
    _, _, inputs = _production_context_and_inputs(api)
    regime = next(item for item in inputs if item.stage == "regime")
    fact_payload = regime.carrier_facts[0].model_dump(mode="python")
    fact_payload["fact_id"] = "whole_prepared_payload"
    fact_material = dict(fact_payload)
    fact_material.pop("semantic_fingerprint")
    fact_payload["semantic_fingerprint"] = fingerprint(fact_material)

    with pytest.raises(ValueError, match="carrier_fact_not_admitted_for_stage"):
        _refingerprint_stage_input(api, regime, carrier_facts=(fact_payload,))

    forged = regime.model_copy(update={"carrier_facts": ()})
    with pytest.raises(ValueError, match="carrier_facts_or_missing_state_required"):
        api["StageInput"].model_validate(forged.model_dump(mode="python"))


def test_production_runner_rejects_refingerprinted_output_input_carrier_forgery() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    handlers = production_handlers(api)
    normal = handlers["regime"]

    def forged_handler(stage_input, dependencies):
        output = normal(stage_input, dependencies)
        return _refingerprint_output(
            api,
            output,
            input_carrier_id="carrier.regime.forged",
            input_carrier_fingerprint="9" * 64,
        )

    handlers["regime"] = forged_handler
    runner = api["SerialRunner"](
        handlers=handlers,
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    with pytest.raises(ValueError, match="stage_output_input_carrier_lineage_mismatch"):
        runner.run(context=context, stage_inputs=inputs)


def test_production_candidate_binds_ordered_eligibility_and_lead() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )
    candidate = runner.run(context=context, stage_inputs=inputs)

    assert candidate.ordered_eligible_candidate_ids == ("playbook.breakout",)
    assert candidate.eligibility_lead_id == "playbook.breakout"
    with pytest.raises(ValueError, match="candidate_eligibility_lineage_mismatch"):
        _refingerprint_candidate(
            api,
            candidate,
            ordered_eligible_candidate_ids=("playbook.forged",),
            eligibility_lead_id="playbook.forged",
        )


def test_production_runner_rejects_terminal_stage_binding_payload() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    handlers = production_handlers(
        api,
        terminal_stage="execution",
        terminal_status="withheld",
    )
    normal = handlers["execution"]

    def forged_handler(stage_input, dependencies):
        output = normal(stage_input, dependencies)
        return _refingerprint_output(
            api,
            output,
            result_refs=(("expression_id", "expression.forged"),),
        )

    handlers["execution"] = forged_handler
    runner = api["SerialRunner"](
        handlers=handlers,
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )

    with pytest.raises(
        ValueError,
        match="terminal_stage_output_contains_binding_payload",
    ):
        runner.run(context=context, stage_inputs=inputs)


def test_production_execution_withheld_preserves_prior_eligibility_without_candidate() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    runner = api["SerialRunner"](
        handlers=production_handlers(
            api,
            terminal_stage="execution",
            terminal_status="withheld",
        ),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    )

    result = runner.run(context=context, stage_inputs=inputs)

    assert result.status == "withheld"
    assert result.failed_stage == "execution"
    assert result.candidate_id is None
    assert result.ordered_eligible_candidate_ids == ("playbook.breakout",)
    assert result.eligibility_lead_id == "playbook.breakout"
    assert result.expression_id is None
    assert result.lifecycle_intent == ()


def test_repair_stage_context_rejects_unknown_prepared_state() -> None:
    api = production_api()
    payload = production_context_payload(valid_context())
    payload["prepared_validation_state"] = "banana"
    material = dict(payload)
    material.pop("semantic_fingerprint")
    payload["semantic_fingerprint"] = fingerprint(material)
    with pytest.raises(ValueError):
        api["StageContext"].model_validate(payload)


def test_repair_stage_context_requires_exact_valid_complete_state() -> None:
    api = production_api()
    payload = production_context_payload(valid_context())
    payload["limitations"] = ("contradictory_gap",)
    material = dict(payload)
    material.pop("semantic_fingerprint")
    payload["semantic_fingerprint"] = fingerprint(material)
    with pytest.raises(ValueError, match="valid_context_must_be_complete_without_gaps"):
        api["StageContext"].model_validate(payload)


def test_repair_terminal_result_requires_failed_stage_output() -> None:
    api = production_api()
    assert "serial_result_id" in api["SerialCandidate"].model_fields
    payload = {
        "status": "withheld",
        "reasons": ("temporal_unavailable",),
        "failed_stage": "temporal",
        "serial_result_id": "",
        "candidate_id": None,
        "candidate_contract_version": "1.0.0",
        "candidate_schema_version": "1.0.0",
        "context_id": "context.1",
        "context_fingerprint": "a" * 64,
        "prepared_id": "prepared.1",
        "prepared_fingerprint": "b" * 64,
        "stage_order_version": "order.v1",
        "stage_outputs": (),
        "posture_status": None,
        "posture_reasons": (),
        "m07_authority_refs": (),
        "m08_authority_refs": (),
        "ordered_eligible_candidate_ids": (),
        "eligibility_lead_id": None,
        "selected_playbook_family_id": None,
        "selected_playbook_family_version": None,
        "selected_playbook_id": None,
        "selected_playbook_version": None,
        "selected_setup_variant_id": None,
        "selected_setup_variant_version": None,
        "expression_id": None,
        "expression_version": None,
        "expression_fingerprint": None,
        "lifecycle_intent": (),
        "limitations": (),
        "closed_authority_classes": CLOSED_AUTHORITIES,
        "foreign_authority_claimed": False,
        "semantic_fingerprint": "",
    }
    material = dict(payload)
    material.pop("serial_result_id")
    material.pop("candidate_id")
    material.pop("semantic_fingerprint")
    candidate_fingerprint = fingerprint(material)
    payload["semantic_fingerprint"] = candidate_fingerprint
    payload["serial_result_id"] = f"serial-result.{candidate_fingerprint[:16]}"
    with pytest.raises(ValueError, match="candidate_terminal_output_required"):
        api["SerialCandidate"].model_validate(payload)


def test_repair_all_terminal_results_have_stable_distinct_result_identity() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    cases = (
        production_handlers(api),
        production_handlers(api, terminal_stage="posture"),
        production_handlers(
            api,
            terminal_stage="options_flow",
            terminal_status="withheld",
        ),
        production_handlers(api, terminal_stage="regime", terminal_status="rejected"),
    )
    results = tuple(
        api["SerialRunner"](
            handlers=handlers,
            runner_version=context_case.runner_version,
            stage_order_version=context_case.serial_order_version,
        ).run(context=context, stage_inputs=inputs)
        for handlers in cases
    )
    for result in results:
        assert result.serial_result_id == (f"serial-result.{result.semantic_fingerprint[:16]}")
        assert result.serial_result_id not in {
            result.context_id,
            result.prepared_id,
            result.candidate_id,
        }


def test_repair_serial_result_identity_rejects_forged_copy() -> None:
    api = production_api()
    context_case, context, inputs = _production_context_and_inputs(api)
    result = api["SerialRunner"](
        handlers=production_handlers(api),
        runner_version=context_case.runner_version,
        stage_order_version=context_case.serial_order_version,
    ).run(context=context, stage_inputs=inputs)
    forged = result.model_copy(update={"serial_result_id": result.context_id})
    with pytest.raises(ValueError, match="serial_result_identity_invalid"):
        api["SerialCandidate"].model_validate(forged.model_dump(mode="python"))


def test_semantic_continuity_public_service_requires_exact_m03_m07_m08_authority() -> None:
    import inspect

    import nvda_desk.m05_serial_cognition as m05

    assert hasattr(m05, "SerialCognitionRequest")
    assert hasattr(m05, "SerialCognitionService")
    fields = m05.SerialCognitionRequest.model_fields
    assert "prepared_data" in fields
    assert "modifier_bundle" in fields
    assert "playbook_catalogue" in fields
    assert "serial_context" not in fields
    assert "stage_inputs" not in fields
    signature = inspect.signature(m05.SerialCognitionService.run)
    assert tuple(signature.parameters) == ("self", "request")


def test_semantic_continuity_m05_request_cannot_carry_prepared_or_owner_decision_values() -> None:
    import nvda_desk.m05_serial_cognition as m05

    assert set(m05.SerialCognitionRequest.model_fields).isdisjoint(
        {
            "spot_price",
            "vix_level",
            "regime_output",
            "options_flow_output",
            "modifier_decision",
            "eligibility_decision",
            "authority_refs",
        }
    )


class _RecordingOwnerService:
    def __init__(self, delegate: Any) -> None:
        self.delegate = delegate
        self.calls: list[Any] = []

    def evaluate(self, value: Any) -> Any:
        self.calls.append(value)
        return self.delegate.evaluate(value)


def test_semantic_continuity_real_owners_receive_exact_m03_values_and_bind_owner_products() -> None:
    from tests.support.m00_application_shell_contract_harness import (
        production_serial_cognition_request,
    )
    from tests.support.m06_k10_contract_harness import make_prepared

    import nvda_desk.m05_serial_cognition as m05
    from nvda_desk.services.options_flow_context_service import OptionsFlowContextService
    from nvda_desk.services.regime_context_service import RegimeContextService
    from nvda_desk.services.temporal_context_service import TemporalContextService

    prepared = make_prepared(vix_level=20.0)
    request = production_serial_cognition_request(prepared, suffix="semantic-exact")
    temporal = _RecordingOwnerService(TemporalContextService())
    regime = _RecordingOwnerService(RegimeContextService())
    options = _RecordingOwnerService(OptionsFlowContextService())

    outcome = m05.SerialCognitionService(
        temporal_service=temporal,
        regime_service=regime,
        options_flow_service=options,
    ).run(request)

    assert len(temporal.calls) == len(regime.calls) == len(options.calls) == 1
    assert temporal.calls[0].source_time_utc == prepared.payload.source_time_utc
    assert regime.calls[0].nvda_return_pct == prepared.payload.nvda_return_pct
    assert regime.calls[0].nq_return_pct == prepared.payload.nq_return_pct
    assert regime.calls[0].vix_level == prepared.payload.vix_level
    assert options.calls[0].spot_price == prepared.payload.spot_price == 190.0
    assert options.calls[0].front_dte == prepared.payload.front_dte
    assert options.calls[0].next_dte == prepared.payload.next_dte

    assert outcome.candidate.status == "formed"
    assert outcome.modifier_receipt is not None
    assert outcome.eligibility_decision is not None
    assert outcome.eligibility_decision.status == "eligible"
    assert (
        "m07",
        outcome.modifier_decision.decision_id,
        outcome.modifier_decision.schema_version,
        outcome.modifier_decision.semantic_fingerprint,
    ) in outcome.candidate.m07_authority_refs
    assert (
        "m07",
        outcome.modifier_receipt.receipt_id,
        outcome.modifier_receipt.schema_version,
        m05.contracts.semantic_fingerprint(outcome.modifier_receipt.model_dump(mode="python")),
    ) in outcome.candidate.m07_authority_refs
    assert (
        "m08",
        outcome.eligibility_decision.decision_id,
        outcome.eligibility_decision.decision_schema_version,
        outcome.eligibility_decision.semantic_fingerprint,
    ) in outcome.candidate.m08_authority_refs
    material_facts = {
        item.fact_ref: item.value for item in outcome.eligibility_decision.material_fact_lineage
    }
    assert material_facts["spot_price"] == prepared.payload.spot_price
    assert material_facts["gamma_state"] == "active"


def test_semantic_continuity_caller_value_substitution_fails_before_owner_call() -> None:
    from tests.support.m00_application_shell_contract_harness import (
        production_serial_cognition_request,
    )
    from tests.support.m06_k10_contract_harness import make_prepared

    import nvda_desk.m05_serial_cognition as m05
    from nvda_desk.services.options_flow_context_service import OptionsFlowContextService

    prepared = make_prepared(vix_level=20.0)
    request = production_serial_cognition_request(prepared, suffix="semantic-forgery")
    options = _RecordingOwnerService(OptionsFlowContextService())
    service = m05.SerialCognitionService(options_flow_service=options)
    payload = request.model_dump(mode="python")
    payload["spot_price"] = 999.0

    with pytest.raises(ValueError, match="spot_price|extra"):
        forged = m05.SerialCognitionRequest.model_validate(payload)
        service.run(forged)

    assert options.calls == []


def test_semantic_continuity_m05_request_rejects_missing_required_m07_coefficient() -> None:
    from tests.support.m00_application_shell_contract_harness import (
        production_serial_cognition_request,
    )
    from tests.support.m06_k10_contract_harness import make_prepared

    import nvda_desk.m05_serial_cognition as m05

    request = production_serial_cognition_request(
        make_prepared(vix_level=20.0),
        suffix="semantic-missing-coefficient",
    )
    bundle = request.modifier_bundle.model_copy(
        update={
            "coefficients": tuple(
                item
                for item in request.modifier_bundle.coefficients
                if item.coefficient_id != "hedge_required"
            )
        }
    )

    with pytest.raises(ValueError, match="m07_required_coefficient_missing:hedge_required"):
        m05.SerialCognitionRequest.model_validate(
            {
                **request.model_dump(mode="python"),
                "modifier_bundle": bundle,
            }
        )


def test_semantic_continuity_m05_rejects_inverted_effective_vix_thresholds() -> None:
    from tests.support.m00_application_shell_contract_harness import (
        production_serial_cognition_request,
    )
    from tests.support.m06_k10_contract_harness import make_prepared

    import nvda_desk.m05_serial_cognition as m05

    request = production_serial_cognition_request(
        make_prepared(vix_level=20.0),
        suffix="semantic-inverted-thresholds",
    )
    coefficients = tuple(
        (
            item.model_copy(update={"baseline_value": Decimal("40")})
            if item.coefficient_id == "risk_vix_caution_threshold"
            else item
        )
        for item in request.modifier_bundle.coefficients
    )
    bundle = request.modifier_bundle.model_copy(update={"coefficients": coefficients})
    inverted = m05.SerialCognitionRequest.model_validate(
        {
            **request.model_dump(mode="python"),
            "modifier_bundle": bundle,
        }
    )

    with pytest.raises(ValueError, match="m07_effective_vix_threshold_order_invalid"):
        m05.SerialCognitionService().run(inverted)
