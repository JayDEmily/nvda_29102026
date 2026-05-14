"""Tier A tests for bounded state-conditioned modifier runtime behaviour."""

from __future__ import annotations

import importlib
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml

AUTHORITY_PATH = Path("config/coefficient_authority.v1.yaml")


def _require_module(module_path: str):
    """Import a required module or fail with an explicit missing-surface error."""

    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    """Fetch a required attribute from a module or fail with its dotted name."""

    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def _load_authority_payload() -> dict[str, Any]:
    """Load the governed coefficient-authority fixture payload."""

    return yaml.safe_load(AUTHORITY_PATH.read_text(encoding="utf-8"))


def _write_authority_payload(tmp_path: Path, payload: dict[str, Any]) -> Path:
    """Write a temporary coefficient-authority payload and return its path."""

    authority_path = tmp_path / "coefficient_authority.v1.yaml"
    authority_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return authority_path


def test_modifier_home_surfaces_are_present() -> None:
    """The bounded modifier module exposes the admitted service and helper surfaces."""

    modifier_module = _require_module("nvda_desk.cognition.modifiers.state_conditioned")
    assert modifier_module.__name__ == "nvda_desk.cognition.modifiers.state_conditioned"

    assert _require_attr(modifier_module, "StateConditionedModifierService") is getattr(modifier_module, "StateConditionedModifierService")
    assert _require_attr(modifier_module, "build_modifier_packet") is getattr(modifier_module, "build_modifier_packet")
    assert _require_attr(modifier_module, "apply_posture_modifiers") is getattr(modifier_module, "apply_posture_modifiers")
    assert _require_attr(modifier_module, "apply_execution_modifiers") is getattr(modifier_module, "apply_execution_modifiers")


def test_modifier_home_builds_packet_and_applies_posture_lineage() -> None:
    """Active negative-gamma stress resolves bounded effective posture coefficients."""

    modifier_module = _require_module("nvda_desk.cognition.modifiers.state_conditioned")
    assert modifier_module.__name__ == "nvda_desk.cognition.modifiers.state_conditioned"
    posture_contracts = _require_module("nvda_desk.contracts.posture")
    assert posture_contracts.__name__ == "nvda_desk.contracts.posture"

    service = _require_attr(modifier_module, "StateConditionedModifierService")()
    permission_state = _require_attr(posture_contracts, "PermissionState")
    assert permission_state is getattr(posture_contracts, "PermissionState")
    posture_output = _require_attr(posture_contracts, "PostureRiskOutput")
    assert posture_output is getattr(posture_contracts, "PostureRiskOutput")

    packet = service.build_packet(
        active_modifier_ids=["negative_gamma_stress"], owner_stage="posture"
    )
    assert packet.active_modifier_ids == ["negative_gamma_stress"]
    effective = {item.coefficient_id: item for item in packet.resolved_coefficients}
    assert effective["max_risk_per_trade"].effective_value == 0.25
    assert effective["hedge_required"].effective_value is True

    adjusted = service.apply_posture_modifiers(
        posture=posture_output(
            permission_state=permission_state.ALLOW, local_envelope={"max_risk_per_trade": 0.35}
        ),
        modifier_packet=packet,
    )
    assert adjusted.local_envelope["active_modifier_ids"] == ["negative_gamma_stress"]
    assert adjusted.local_envelope["max_risk_per_trade"] == 0.25
    assert adjusted.local_envelope["hedge_required"] is True


def test_modifier_home_rejects_unknown_or_duplicate_modifier_ids() -> None:
    """Runtime resolution must not silently ignore unknown or duplicated policy requests."""

    modifier_module = _require_module("nvda_desk.cognition.modifiers.state_conditioned")
    assert modifier_module.__name__ == "nvda_desk.cognition.modifiers.state_conditioned"
    service = _require_attr(modifier_module, "StateConditionedModifierService")()

    with pytest.raises(ValueError, match="unknown modifier policies"):
        service.build_packet(active_modifier_ids=["not_admitted"], owner_stage="posture")

    with pytest.raises(ValueError, match="duplicate modifier policies"):
        service.build_packet(
            active_modifier_ids=["negative_gamma_stress", "negative_gamma_stress"],
            owner_stage="posture",
        )


def test_coefficient_authority_rejects_out_of_bounds_modifier_effect(tmp_path: Path) -> None:
    """Governed modifier policies cannot push numeric effective values outside hard bounds."""

    payload = deepcopy(_load_authority_payload())
    payload["modifier_policies"][0]["effects"][0]["effective_value"] = 0.01
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="outside hard bounds"):
        service.load_document()


def test_coefficient_authority_rejects_policy_targeting_baseline_only_surface(
    tmp_path: Path,
) -> None:
    """Modifier policies cannot target baseline-only surfaces as mutable runtime effects."""

    payload = deepcopy(_load_authority_payload())
    payload["modifier_policies"][0]["admitted_surfaces"].append("risk_vix_caution_threshold")
    payload["modifier_policies"][0]["effects"].append(
        {
            "coefficient_id": "risk_vix_caution_threshold",
            "transform_family": "baseline_only_so_far",
            "effective_value": 30.0,
            "rationale": "Invalid test effect against baseline-only authority.",
        }
    )
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="surface_class=baseline_only_surface"):
        service.load_document()


def test_coefficient_authority_rejects_cross_stage_policy_effect(tmp_path: Path) -> None:
    """Modifier policies cannot cross owner-stage boundaries while resolving effects."""

    payload = deepcopy(_load_authority_payload())
    payload["records"][2]["owner_stage"] = "eligibility"
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="crosses owner_stage"):
        service.load_document()


def test_coefficient_authority_rejects_duplicate_coefficient_ids(tmp_path: Path) -> None:
    payload = deepcopy(_load_authority_payload())
    payload["records"].append(deepcopy(payload["records"][0]))
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="coefficient_id values must be unique"):
        service.load_document()


def test_coefficient_authority_rejects_duplicate_policy_effect_coefficients(
    tmp_path: Path,
) -> None:
    payload = deepcopy(_load_authority_payload())
    payload["modifier_policies"][0]["effects"].append(
        deepcopy(payload["modifier_policies"][0]["effects"][0])
    )
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="duplicate modifier effect coefficients"):
        service.load_document()


def test_coefficient_authority_rejects_unknown_policy_admitted_surface(tmp_path: Path) -> None:
    payload = deepcopy(_load_authority_payload())
    payload["modifier_policies"][0]["admitted_surfaces"].append("unknown_coefficient")
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="unknown admitted surfaces"):
        service.load_document()


def test_coefficient_authority_rejects_non_boolean_effect_on_boolean_surface(
    tmp_path: Path,
) -> None:
    payload = deepcopy(_load_authority_payload())
    payload["modifier_policies"][0]["effects"][1]["effective_value"] = 1.0
    authority_path = _write_authority_payload(tmp_path, payload)

    authority_module = _require_module("nvda_desk.config.coefficient_authority")
    assert authority_module.__name__ == "nvda_desk.config.coefficient_authority"
    service_cls = _require_attr(authority_module, "CoefficientAuthorityService")
    assert service_cls is getattr(authority_module, "CoefficientAuthorityService")
    service = service_cls(authority_path)

    with pytest.raises(ValueError, match="requires boolean effective_value"):
        service.load_document()


def test_apply_posture_modifiers_detaches_nested_envelope_from_input() -> None:
    """Modifier application must not share nested caller envelope state."""

    modifier_module = _require_module("nvda_desk.cognition.modifiers.state_conditioned")
    posture_contracts = _require_module("nvda_desk.contracts.posture")

    service = _require_attr(modifier_module, "StateConditionedModifierService")()
    permission_state = _require_attr(posture_contracts, "PermissionState")
    posture_output = _require_attr(posture_contracts, "PostureRiskOutput")
    packet = service.build_packet(
        active_modifier_ids=["negative_gamma_stress"], owner_stage="posture"
    )
    original = posture_output(
        permission_state=permission_state.ALLOW,
        local_envelope={"source_context": {"source": "fixture"}},
    )

    adjusted = service.apply_posture_modifiers(posture=original, modifier_packet=packet)
    adjusted.local_envelope["source_context"]["source"] = "mutated"

    assert original.local_envelope["source_context"] == {"source": "fixture"}
