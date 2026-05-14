"""Pure posture permission evaluation."""

from __future__ import annotations

from collections.abc import Mapping

from nvda_desk.contracts.posture import PermissionState, PostureRiskOutput
from nvda_desk.contracts.regime import MarketRegimeContextOutput

DEFAULT_POSTURE_COEFFICIENTS: dict[str, float | bool] = {
    "risk_vix_caution_threshold": 24.0,
    "risk_vix_hot_threshold": 32.0,
    "max_risk_per_trade": 0.35,
    "hedge_required": False,
}


def evaluate_permission(
    *,
    regime: MarketRegimeContextOutput,
    hard_invariants: list[str] | None = None,
    coefficient_values: Mapping[str, float | bool] | None = None,
) -> PostureRiskOutput:
    """Return one bounded posture envelope from regime context, invariants, and promoted coefficients."""

    invariants = list(hard_invariants or [])
    reasons = list(regime.reasons)
    values = dict(DEFAULT_POSTURE_COEFFICIENTS)
    if coefficient_values is not None:
        values.update(coefficient_values)

    caution_threshold = float(values["risk_vix_caution_threshold"])
    hot_threshold = float(values["risk_vix_hot_threshold"])
    max_risk_per_trade = float(values["max_risk_per_trade"])
    hedge_required = bool(values["hedge_required"])

    if regime.vix_level is None:
        permission = PermissionState.DERISK
        reasons.append("vix_level_unavailable")
        reasons.append("regime_incomplete_derisk")
    elif regime.vix_level >= hot_threshold:
        permission = PermissionState.BLOCK
        reasons.append("vix_hot_threshold")
    elif regime.vix_level >= caution_threshold or regime.volatility_regime in {
        "high_volatility",
        "unknown",
    }:
        permission = PermissionState.DERISK
        if regime.vix_level >= caution_threshold:
            reasons.append("vix_caution_threshold")
        if regime.volatility_regime == "high_volatility":
            reasons.append("volatility_derisk")
        if regime.volatility_regime == "unknown":
            reasons.append("unknown_regime_derisk")
    else:
        permission = PermissionState.ALLOW

    return PostureRiskOutput(
        permission_state=permission,
        local_envelope={
            "volatility_regime": regime.volatility_regime,
            "vix_level": regime.vix_level,
            "risk_vix_caution_threshold": caution_threshold,
            "risk_vix_hot_threshold": hot_threshold,
            "max_risk_per_trade": max_risk_per_trade,
            "hedge_required": hedge_required,
        },
        hard_invariants=invariants,
        reasons=reasons,
    )
