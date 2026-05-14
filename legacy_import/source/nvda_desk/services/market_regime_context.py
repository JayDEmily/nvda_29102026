"""Market-regime classification service for the Desk Cognition Grammar.

This service transforms beta, breadth, volatility, rates, and FX inputs into
bounded market-regime state for posture, playbook, and execution layers.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    BreadthState,
    MarketRegimeContextInput,
    MarketRegimeContextOutput,
    VolatilityRegime,
)


class MarketRegimeContextService:
    """Classify market-regime state from cross-asset inputs.

    Purpose:
        Convert beta, breadth, volatility, rates, and FX into an explicit desk regime.
    Inputs:
        `MarketRegimeContextInput` carrying NVDA, index, rates, volatility, and FX context.
    Outputs:
        `MarketRegimeContextOutput` with leadership, concentration, vol, rates, FX,
        and conflict state labels.
    Determinism:
        Applies fixed bounded rules with no learned or hidden state.
    """

    def evaluate(self, payload: MarketRegimeContextInput) -> MarketRegimeContextOutput:
        """Build deterministic regime context for one snapshot."""

        nvda_vs_nq = round(payload.nvda_return_pct - payload.nq_return_pct, 4)
        nvda_vs_es = round(payload.nvda_return_pct - payload.es_return_pct, 4)
        sox_vs_nq = round(payload.sox_return_pct - payload.nq_return_pct, 4)
        beta_leadership_score = round(((nvda_vs_nq + nvda_vs_es) / 2.0) + (sox_vs_nq * 0.5), 4)
        volatility_regime = self._volatility_regime(payload.vix_level, payload.vvix_level)
        breadth_state = self._breadth_state(payload.breadth_score)
        breadth_concentration_state = self._breadth_concentration_state(
            payload.breadth_score,
            payload.concentration_score,
        )
        vol_of_vol_state = self._vol_of_vol_state(payload.vvix_level)
        sector_leadership_state = self._sector_leadership_state(payload)
        curve_10s2s = round(payload.us10y - payload.us2y, 4)
        rates_regime_state = self._rates_regime_state(payload.us10y, curve_10s2s)
        fx_stress_state = self._fx_stress_state(payload.usdjpy)
        vix_vvix_spread = round(payload.vvix_level - payload.vix_level, 4)
        signal_conflict_state = self._signal_conflict_state(
            sector_leadership_state=sector_leadership_state,
            breadth_state=breadth_state,
            breadth_concentration_state=breadth_concentration_state,
            volatility_regime=volatility_regime,
            nvda_vs_nq=nvda_vs_nq,
        )
        cross_asset_pressure = self._cross_asset_pressure(
            volatility_regime=volatility_regime,
            breadth_state=breadth_state,
            breadth_concentration_state=breadth_concentration_state,
            rates_regime_state=rates_regime_state,
            fx_stress_state=fx_stress_state,
            signal_conflict_state=signal_conflict_state,
        )
        reasons = [
            f"nvda_vs_nq:{nvda_vs_nq}",
            f"nvda_vs_es:{nvda_vs_es}",
            f"beta_leadership_score:{beta_leadership_score}",
            f"volatility_regime:{volatility_regime.value}",
            f"vol_of_vol_state:{vol_of_vol_state}",
            f"breadth_state:{breadth_state.value}",
            f"breadth_concentration_state:{breadth_concentration_state}",
            f"sector_leadership_state:{sector_leadership_state}",
            f"rates_regime_state:{rates_regime_state}",
            f"fx_stress_state:{fx_stress_state}",
            f"signal_conflict_state:{signal_conflict_state}",
            f"curve_10s2s:{curve_10s2s}",
            f"vix_vvix_spread:{vix_vvix_spread}",
        ]
        return MarketRegimeContextOutput(
            nvda_vs_nq_residual_pct=nvda_vs_nq,
            nvda_vs_es_residual_pct=nvda_vs_es,
            beta_leadership_score=beta_leadership_score,
            volatility_regime=volatility_regime,
            vol_of_vol_state=vol_of_vol_state,
            breadth_state=breadth_state,
            breadth_concentration_state=breadth_concentration_state,
            sector_leadership_state=sector_leadership_state,
            rates_regime_state=rates_regime_state,
            fx_stress_state=fx_stress_state,
            signal_conflict_state=signal_conflict_state,
            curve_10s2s=curve_10s2s,
            vix_vvix_spread=vix_vvix_spread,
            cross_asset_pressure_score=round(cross_asset_pressure, 4),
            reasons=reasons,
        )

    def _volatility_regime(self, vix_level: float, vvix_level: float) -> VolatilityRegime:
        if vix_level >= 28.0 or vvix_level >= 110.0:
            return VolatilityRegime.STRESSED
        if vix_level >= 20.0 or vvix_level >= 90.0:
            return VolatilityRegime.CAUTION
        return VolatilityRegime.CALM

    def _breadth_state(self, breadth_score: float) -> BreadthState:
        if breadth_score >= 0.65:
            return BreadthState.SUPPORTIVE
        if breadth_score >= 0.45:
            return BreadthState.MIXED
        return BreadthState.WEAK

    def _breadth_concentration_state(self, breadth_score: float, concentration_score: float) -> str:
        if breadth_score >= 0.65 and concentration_score <= 0.55:
            return "broad_risk_on"
        if breadth_score >= 0.55 and concentration_score > 0.70:
            return "narrow_leadership"
        if breadth_score < 0.45 and concentration_score >= 0.70:
            return "narrow_stress"
        if breadth_score < 0.45:
            return "broad_risk_off"
        return "mixed_participation"

    def _vol_of_vol_state(self, vvix_level: float) -> str:
        if vvix_level >= 120.0:
            return "vol_of_vol_extreme"
        if vvix_level >= 100.0:
            return "vol_of_vol_hot"
        if vvix_level >= 90.0:
            return "vol_of_vol_elevated"
        return "vol_of_vol_calm"

    def _sector_leadership_state(self, payload: MarketRegimeContextInput) -> str:
        if (
            payload.nvda_return_pct > payload.nq_return_pct
            and payload.sox_return_pct > payload.nq_return_pct
        ):
            return "semis_leading"
        if (
            payload.nvda_return_pct < payload.nq_return_pct
            and payload.sox_return_pct < payload.nq_return_pct
        ):
            return "semis_lagging"
        if (
            payload.nvda_return_pct > payload.nq_return_pct
            and payload.sox_return_pct <= payload.nq_return_pct
        ):
            return "nvda_only_leadership"
        return "leadership_mixed"

    def _rates_regime_state(self, us10y: float, curve_10s2s: float) -> str:
        if us10y >= 4.6 or curve_10s2s <= -0.25:
            return "rates_shock_headwind"
        if curve_10s2s < 0.0:
            return "inverted_curve_headwind"
        if curve_10s2s >= 0.15 and us10y <= 4.35:
            return "steepening_relief"
        return "rates_neutral"

    def _fx_stress_state(self, usdjpy: float) -> str:
        if usdjpy < 145.0:
            return "yen_carry_unwind"
        if usdjpy < 147.0:
            return "fx_caution"
        if usdjpy > 152.0:
            return "usd_stretch"
        return "fx_neutral"

    def _signal_conflict_state(
        self,
        *,
        sector_leadership_state: str,
        breadth_state: BreadthState,
        breadth_concentration_state: str,
        volatility_regime: VolatilityRegime,
        nvda_vs_nq: float,
    ) -> str:
        if (
            sector_leadership_state in {"semis_leading", "nvda_only_leadership"}
            and breadth_state is BreadthState.WEAK
        ):
            return "leadership_without_breadth"
        if sector_leadership_state == "semis_lagging" and breadth_state is BreadthState.SUPPORTIVE:
            return "index_support_nvda_lag"
        if volatility_regime is VolatilityRegime.STRESSED and nvda_vs_nq > 1.0:
            return "panic_tape_with_single_name_resilience"
        if breadth_concentration_state == "narrow_leadership":
            return "narrow_leadership_conflict"
        return "aligned_regime"

    def _cross_asset_pressure(
        self,
        *,
        volatility_regime: VolatilityRegime,
        breadth_state: BreadthState,
        breadth_concentration_state: str,
        rates_regime_state: str,
        fx_stress_state: str,
        signal_conflict_state: str,
    ) -> float:
        score = 0.0
        if volatility_regime is VolatilityRegime.CAUTION:
            score += 0.20
        if volatility_regime is VolatilityRegime.STRESSED:
            score += 0.35
        if breadth_state is BreadthState.WEAK:
            score += 0.20
        if breadth_concentration_state in {"narrow_stress", "narrow_leadership"}:
            score += 0.15
        if rates_regime_state in {"rates_shock_headwind", "inverted_curve_headwind"}:
            score += 0.15
        if fx_stress_state in {"yen_carry_unwind", "fx_caution"}:
            score += 0.10
        if signal_conflict_state != "aligned_regime":
            score += 0.15
        return min(score, 1.0)
