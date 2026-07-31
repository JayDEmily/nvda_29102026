"""M05 K08/K09 proof for common stage context and ordered serial candidate law."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Any

import pytest

from tests.support.m05_k08_k09_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    SERIAL_STAGE_ORDER,
    ReferenceRunner,
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
        order=tuple(reversed(SERIAL_STAGE_ORDER))
        if mutant_name == "caller_order"
        else SERIAL_STAGE_ORDER,
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
    assert first.candidate_id == f"serial.{first.semantic_fingerprint[:16]}"
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
