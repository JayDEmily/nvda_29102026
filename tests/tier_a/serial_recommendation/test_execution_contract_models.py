from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_execution_contract_models_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.execution")
    assert contracts.__name__ == "nvda_desk.contracts.execution"

    for attr_name in (
        "ExecutionExpressionInput",
        "ExecutionExpressionOutput",
        "StageLocalHandoffSurface",
    ):
        assert _require_attr(contracts, attr_name) is getattr(contracts, attr_name)


def test_execution_contract_boundary_fields_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.execution")
    assert contracts.__name__ == "nvda_desk.contracts.execution"

    output_model = _require_attr(contracts, "ExecutionExpressionOutput")
    assert output_model is getattr(contracts, "ExecutionExpressionOutput")
    handoff_model = _require_attr(contracts, "StageLocalHandoffSurface")
    assert handoff_model is getattr(contracts, "StageLocalHandoffSurface")

    assert hasattr(output_model, "model_fields")
    assert hasattr(handoff_model, "model_fields")
    assert "lead_playbook_id" in output_model.model_fields
    assert "scaling_plan" in output_model.model_fields
    assert "final_risk_join" in output_model.model_fields
    assert "execution_post_modifier_pre_final_risk" in handoff_model.model_fields


def test_execution_expression_output_rejects_capital_authority_fields() -> None:
    contracts = _require_module("nvda_desk.contracts.execution")
    assert contracts.__name__ == "nvda_desk.contracts.execution"
    output_model = _require_attr(contracts, "ExecutionExpressionOutput")
    assert output_model is getattr(contracts, "ExecutionExpressionOutput")

    with pytest.raises(ValidationError):
        output_model(
            lead_playbook_id="playbook::demo",
            authorised_notional_usd=1000.0,
        )


def test_execution_contract_models_detach_nested_serial_payloads_from_callers() -> None:
    contracts = _require_module("nvda_desk.contracts.execution")

    input_model = _require_attr(contracts, "ExecutionExpressionInput")
    output_model = _require_attr(contracts, "ExecutionExpressionOutput")
    handoff_model = _require_attr(contracts, "StageLocalHandoffSurface")

    temporal_payload = {"stage": {"trace": ["source"]}}
    final_risk_join = {"join": {"components": ["serial_expression"]}}
    handoff_payload = {"handoff": {"lineage": ["execution_stage"]}}

    execution_input = input_model(temporal=temporal_payload)
    execution_output = output_model(final_risk_join=final_risk_join)
    stage_handoff = handoff_model(
        execution_post_modifier_pre_final_risk=handoff_payload,
    )

    temporal_payload["stage"]["trace"].append("capital_deployment_authority")
    final_risk_join["join"]["components"].append("capital_deployment_authority")
    handoff_payload["handoff"]["lineage"].append("capital_deployment_authority")

    assert execution_input.temporal == {"stage": {"trace": ["source"]}}
    assert execution_output.final_risk_join == {"join": {"components": ["serial_expression"]}}
    assert stage_handoff.execution_post_modifier_pre_final_risk == {
        "handoff": {"lineage": ["execution_stage"]}
    }
