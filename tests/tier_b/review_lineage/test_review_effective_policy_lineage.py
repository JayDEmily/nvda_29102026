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


def test_review_effective_policy_lineage_surfaces_are_present() -> None:
    review_contracts = _require_module("nvda_desk.contracts.review")
    modifier_contracts = _require_module("nvda_desk.contracts.modifiers")
    review_service = _require_module("nvda_desk.services.review_explanation_service")
    coefficient_contracts = _require_module("nvda_desk.contracts." + "coefficient_authority")
    coefficient_service = _require_module(
        "nvda_desk.services." + "coefficient_authority" + "_service"
    )

    _require_attr(review_contracts, "EffectivePolicySnapshot")
    _require_attr(review_contracts, "ReviewLineagePacket")
    _require_attr(modifier_contracts, "ModifierRuntimePacket")
    _require_attr(modifier_contracts, "ResolvedCoefficientValue")
    _require_attr(coefficient_contracts, "CoefficientAuthorityDocument")
    _require_attr(coefficient_service, "CoefficientAuthorityService")
    _require_attr(review_service, "ReviewExplanationService")


def test_review_effective_policy_lineage_keeps_resolved_surface_visibility() -> None:
    review_contracts = _require_module("nvda_desk.contracts.review")

    effective_policy = _require_attr(review_contracts, "EffectivePolicySnapshot")
    review_lineage = _require_attr(review_contracts, "ReviewLineagePacket")

    assert hasattr(effective_policy, "model_fields")
    assert hasattr(review_lineage, "model_fields")
    assert "resolved_surfaces" in effective_policy.model_fields
    assert "resolved_surfaces" in review_lineage.model_fields
    assert "resolved_coefficients" in effective_policy.model_fields
    assert "resolved_coefficients" in review_lineage.model_fields


def test_review_explanation_keeps_effective_coefficient_lineage_visible() -> None:
    review_contracts = _require_module("nvda_desk.contracts.review")
    modifier_contracts = _require_module("nvda_desk.contracts.modifiers")
    review_service_module = _require_module("nvda_desk.services.review_explanation_service")

    review_packet = _require_attr(review_contracts, "ReviewPacket")
    effective_policy = _require_attr(review_contracts, "EffectivePolicySnapshot")
    review_lineage = _require_attr(review_contracts, "ReviewLineagePacket")
    packet_lineage = _require_attr(review_contracts, "PacketLineageSurface")
    resolved_coefficient = _require_attr(modifier_contracts, "ResolvedCoefficientValue")
    service_class = _require_attr(review_service_module, "ReviewExplanationService")

    coefficient = resolved_coefficient(
        coefficient_id="max_risk_per_trade",
        owner_stage="posture",
        surface_class="mutable_runtime_surface",
        baseline_value=0.35,
        effective_value=0.25,
        transform_family="clamp",
        modifier_inputs=["negative_gamma_stress"],
        workbook_ref="Runtime_Surface_Drivers!B10:H10",
        runtime_mutable=True,
    )
    explanation = service_class().build_explanation(
        review_packet=review_packet(packet_id="review-1", summary="bounded review"),
        effective_policy=effective_policy(
            policy_ids=["negative_gamma_stress"],
            resolved_surfaces=["max_risk_per_trade", "hedge_required"],
            resolved_coefficients=[coefficient],
        ),
        review_lineage=review_lineage(
            event_lineage_keys=["event-1"],
            resolved_surfaces=["max_risk_per_trade", "hedge_required"],
            modifier_policy_ids=["negative_gamma_stress"],
            resolved_coefficients=[coefficient],
        ),
        packet_lineage=packet_lineage(
            **{"packet" "_ids": ["packet-1"], "source_packet" "_ids": ["source-1"]}
        ),
    )

    assert explanation["resolved_surfaces"] == ["max_risk_per_trade", "hedge_required"]
    assert explanation["resolved_coefficients"][0]["baseline_value"] == 0.35
    assert explanation["resolved_coefficients"][0]["effective_value"] == 0.25
    assert explanation["resolved_coefficients"][0]["transform_family"] == "clamp"
    assert explanation["resolved_coefficients"][0]["modifier_inputs"] == ["negative_gamma_stress"]
