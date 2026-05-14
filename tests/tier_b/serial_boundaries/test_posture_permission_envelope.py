from __future__ import annotations

import importlib

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_posture_contract_and_service_surfaces_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.posture")
    serial_module = _require_module("nvda_desk.cognition.serial.posture")
    service_module = _require_module("nvda_desk.services.posture_service")

    _require_attr(contracts, "PermissionState")
    _require_attr(contracts, "PosturePermissionEnvelope")
    output_model = _require_attr(contracts, "PostureRiskOutput")
    _require_attr(serial_module, "evaluate_posture")
    _require_attr(service_module, "PostureService")

    assert hasattr(output_model, "model_fields")


def test_posture_output_keeps_permission_envelope_separate_from_capital_decision() -> None:
    contracts = _require_module("nvda_desk.contracts.posture")
    capital_contracts = _require_module("nvda_desk.contracts.capital")

    output_model = _require_attr(contracts, "PostureRiskOutput")
    _require_attr(capital_contracts, "CapitalDeploymentDecision")

    assert "permission_state" in output_model.model_fields
    assert "local_envelope" in output_model.model_fields
    assert "hard_invariants" in output_model.model_fields
    assert "deployment_action" not in output_model.model_fields
    assert "authorised_notional_usd" not in output_model.model_fields


def test_posture_service_applies_promoted_coefficient_authority_and_bounded_modifiers() -> None:
    posture_contracts = _require_module("nvda_desk.contracts.posture")
    regime_contracts = _require_module("nvda_desk.contracts.regime")
    service_module = _require_module("nvda_desk.services.posture_service")

    permission_state = _require_attr(posture_contracts, "PermissionState")
    regime_output = _require_attr(regime_contracts, "MarketRegimeContextOutput")
    service_class = _require_attr(service_module, "PostureService")

    service = service_class()
    calm_output = service.evaluate(
        regime=regime_output(volatility_regime="stable", vix_level=20.0),
    )
    assert calm_output.permission_state == permission_state.ALLOW
    assert calm_output.local_envelope["risk_vix_caution_threshold"] == 24.0
    assert calm_output.local_envelope["risk_vix_hot_threshold"] == 32.0
    assert calm_output.local_envelope["max_risk_per_trade"] == 0.35
    assert calm_output.local_envelope["hedge_required"] is False
    assert (
        calm_output.local_envelope["effective_coefficients"]["max_risk_per_trade"]["baseline_value"]
        == 0.35
    )
    assert (
        calm_output.local_envelope["effective_coefficients"]["max_risk_per_trade"][
            "effective_value"
        ]
        == 0.35
    )
    assert (
        calm_output.local_envelope["effective_coefficients"]["max_risk_per_trade"][
            "modifier_inputs"
        ]
        == []
    )

    stressed_output = service.evaluate(
        regime=regime_output(volatility_regime="stable", vix_level=33.0),
        active_modifier_ids=["negative_gamma_stress"],
    )
    assert stressed_output.permission_state == permission_state.BLOCK
    assert stressed_output.local_envelope["max_risk_per_trade"] == 0.25
    assert stressed_output.local_envelope["hedge_required"] is True
    assert (
        stressed_output.local_envelope["effective_coefficients"]["max_risk_per_trade"][
            "baseline_value"
        ]
        == 0.35
    )
    assert (
        stressed_output.local_envelope["effective_coefficients"]["max_risk_per_trade"][
            "effective_value"
        ]
        == 0.25
    )
    assert stressed_output.local_envelope["effective_coefficients"]["max_risk_per_trade"][
        "modifier_inputs"
    ] == ["negative_gamma_stress"]
    assert (
        stressed_output.local_envelope["effective_coefficients"]["hedge_required"][
            "effective_value"
        ]
        is True
    )
