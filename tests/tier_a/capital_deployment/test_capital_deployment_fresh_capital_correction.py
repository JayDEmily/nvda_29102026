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


def test_capital_authority_depends_on_final_join_surfaces() -> None:
    capital_contracts = _require_module("nvda_desk.contracts.capital")
    assert capital_contracts.__name__ == "nvda_desk.contracts.capital"
    risk_contracts = _require_module("nvda_desk.contracts.risk")
    assert risk_contracts.__name__ == "nvda_desk.contracts.risk"
    authority = _require_module("nvda_desk.capital.authority")
    assert authority.__name__ == "nvda_desk.capital.authority"
    final_risk = _require_module("nvda_desk.services.final_risk_service")
    assert final_risk.__name__ == "nvda_desk.services.final_risk_service"

    assert _require_attr(capital_contracts, "CapitalDeploymentDecision") is getattr(capital_contracts, "CapitalDeploymentDecision")
    assert _require_attr(risk_contracts, "FinalRiskJoinReceipt") is getattr(risk_contracts, "FinalRiskJoinReceipt")
    assert _require_attr(authority, "CapitalDeploymentAuthorityService") is getattr(authority, "CapitalDeploymentAuthorityService")
    assert _require_attr(final_risk, "FinalRiskService") is getattr(final_risk, "FinalRiskService")
