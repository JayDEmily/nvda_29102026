"""Options-and-flow classification service for the Desk Cognition Grammar.

This service transforms chain-level inputs into deterministic options context,
including term structure, skew, gamma state, repeated-snapshot progression,
and live strike-cluster pressure.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    GammaState,
    OptionsFlowContextInput,
    OptionsFlowContextOutput,
    PinProgressionPoint,
    SkewState,
    StrikeClusterObservation,
    TermStructureState,
)


class OptionsFlowContextService:
    """Build deterministic options-and-flow context from chain snapshots.

    Purpose:
        Convert one options snapshot or snapshot sequence into a typed desk state.
    Inputs:
        `OptionsFlowContextInput` containing IV, skew, gamma, repeated snapshots,
        tenor points, strike clusters, and optional VIX/VVIX context.
    Outputs:
        `OptionsFlowContextOutput` with explicit cluster, progression, IV-vs-RV,
        VIX spread, and behaviour-cluster states for downstream logic.
    Determinism:
        Uses fixed thresholds and stable ordering; no hidden state is retained.
    """

    def evaluate(self, payload: OptionsFlowContextInput) -> OptionsFlowContextOutput:
        """Classify options and flow state for one snapshot."""

        term_structure_spread = payload.front_atm_iv - payload.next_atm_iv
        term_structure_state = self._term_structure_state(term_structure_spread)
        skew_state = self._skew_state(payload.put_call_skew)
        gamma_state = self._gamma_state(payload.gamma_pressure_score)
        implied_move_envelope_pct = round(
            (payload.atm_straddle_value / max(payload.spot_price, 1.0)) * 100.0, 4
        )
        iv_rv_front_state = self._iv_rv_state(payload.front_atm_iv, payload.front_realised_vol)
        iv_rv_next_state = self._iv_rv_state(payload.next_atm_iv, payload.next_realised_vol)
        iv_rv_curve_state = self._iv_rv_curve_state(iv_rv_front_state, iv_rv_next_state)
        vix_spread_state = self._vix_spread_state(payload.vix_level, payload.vvix_level)
        pin_risk_state = self._pin_risk_state(
            payload.spot_to_pin_distance_pct, payload.oi_concentration
        )
        dealer_pressure_state = self._dealer_pressure_state(
            payload.gamma_pressure_score,
            payload.vanna_proxy,
            payload.charm_proxy,
            payload.call_put_imbalance,
        )
        strike_cluster_state, dominant_strike = self._strike_cluster_state(
            payload.nearby_strike_clusters,
            payload.oi_concentration,
            payload.spot_to_pin_distance_pct,
        )
        repeated_snapshot_state = self._repeated_snapshot_state(payload)
        skew_evolution_state = self._skew_evolution_state(payload)
        tenor_curve_state = self._tenor_curve_state(payload)
        pin_progression_state, pin_progression_velocity = self._pin_progression_state(
            payload.pin_progression_sequence
        )
        surface_anchor_state = self._surface_anchor_state(payload.surface_anchor_to_spot_pct)
        options_behavior_cluster = self._options_behavior_cluster(
            gamma_state=gamma_state,
            skew_state=skew_state,
            dealer_pressure_state=dealer_pressure_state,
            pin_risk_state=pin_risk_state,
            strike_cluster_state=strike_cluster_state,
            repeated_snapshot_state=repeated_snapshot_state,
            tenor_curve_state=tenor_curve_state,
            vix_spread_state=vix_spread_state,
            iv_rv_front_state=iv_rv_front_state,
            pin_progression_state=pin_progression_state,
            surface_anchor_state=surface_anchor_state,
        )
        flow_tension_score = round(
            min(
                1.0,
                max(
                    0.0,
                    (payload.gamma_pressure_score * 0.30)
                    + (min(abs(payload.put_call_skew), 1.0) * 0.10)
                    + (payload.oi_concentration * 0.10)
                    + (min(abs(payload.vanna_proxy), 1.0) * 0.05)
                    + (min(abs(payload.charm_proxy), 1.0) * 0.05)
                    + (0.15 if repeated_snapshot_state == "escalating_pressure" else 0.0)
                    + (0.10 if pin_risk_state in {"pin_risk_present", "pin_risk_high"} else 0.0)
                    + (0.15 if vix_spread_state in {"vvix_elevated", "vvix_dislocation"} else 0.0),
                ),
            ),
            4,
        )
        reasons = [
            f"term_structure_state:{term_structure_state.value}",
            f"skew_state:{skew_state.value}",
            f"gamma_state:{gamma_state.value}",
            f"iv_rv_front_state:{iv_rv_front_state}",
            f"iv_rv_next_state:{iv_rv_next_state}",
            f"iv_rv_curve_state:{iv_rv_curve_state}",
            f"pin_risk_state:{pin_risk_state}",
            f"dealer_pressure_state:{dealer_pressure_state}",
            f"vix_spread_state:{vix_spread_state}",
            f"strike_cluster_state:{strike_cluster_state}",
            f"repeated_snapshot_state:{repeated_snapshot_state}",
            f"skew_evolution_state:{skew_evolution_state}",
            f"tenor_curve_state:{tenor_curve_state}",
            f"pin_progression_state:{pin_progression_state}",
            f"surface_anchor_state:{surface_anchor_state}",
            f"options_behavior_cluster:{options_behavior_cluster}",
            f"implied_move_envelope_pct:{implied_move_envelope_pct}",
        ]
        return OptionsFlowContextOutput(
            term_structure_state=term_structure_state,
            skew_state=skew_state,
            gamma_state=gamma_state,
            implied_move_envelope_pct=implied_move_envelope_pct,
            iv_rv_front_state=iv_rv_front_state,
            iv_rv_next_state=iv_rv_next_state,
            iv_rv_curve_state=iv_rv_curve_state,
            pin_risk_state=pin_risk_state,
            dealer_pressure_state=dealer_pressure_state,
            vix_spread_state=vix_spread_state,
            options_behavior_cluster=options_behavior_cluster,
            flow_tension_score=flow_tension_score,
            strike_cluster_state=strike_cluster_state,
            dominant_strike=dominant_strike,
            repeated_snapshot_state=repeated_snapshot_state,
            skew_evolution_state=skew_evolution_state,
            tenor_curve_state=tenor_curve_state,
            pin_progression_state=pin_progression_state,
            pin_progression_velocity=pin_progression_velocity,
            surface_anchor_state=surface_anchor_state,
            reasons=reasons,
        )

    def _term_structure_state(self, spread: float) -> TermStructureState:
        if spread >= 0.01:
            return TermStructureState.FRONT_PREMIUM
        if spread <= -0.01:
            return TermStructureState.BACK_PREMIUM
        return TermStructureState.FLAT

    def _skew_state(self, put_call_skew: float) -> SkewState:
        if put_call_skew >= 0.4:
            return SkewState.DOWNSIDE_HEAVY
        if put_call_skew <= -0.4:
            return SkewState.UPSIDE_CHASE
        return SkewState.BALANCED

    def _gamma_state(self, gamma_pressure_score: float) -> GammaState:
        if gamma_pressure_score >= 0.65:
            return GammaState.DESTABILISING
        if gamma_pressure_score <= 0.35:
            return GammaState.SUPPORTIVE
        return GammaState.NEUTRAL

    def _iv_rv_state(self, implied_vol: float, realised_vol: float) -> str:
        if realised_vol <= 0.0:
            return "iv_context_unset"
        ratio = implied_vol / realised_vol
        if ratio >= 1.2:
            return "iv_rich"
        if ratio <= 0.9:
            return "iv_soft"
        return "iv_balanced"

    def _iv_rv_curve_state(self, front_state: str, next_state: str) -> str:
        if front_state == "iv_rich" and next_state == "iv_rich":
            return "both_expiries_rich"
        if front_state == "iv_soft" and next_state == "iv_soft":
            return "both_expiries_soft"
        if front_state == "iv_rich":
            return "front_expiry_rich"
        if next_state == "iv_rich":
            return "next_expiry_rich"
        return "iv_curve_balanced"

    def _vix_spread_state(self, vix_level: float, vvix_level: float) -> str:
        if vix_level <= 0.0 or vvix_level <= 0.0:
            return "vix_spread_unset"
        spread = vvix_level - vix_level
        if vvix_level >= 120.0 or spread >= 80.0:
            return "vvix_dislocation"
        if vvix_level >= 100.0 or spread >= 60.0:
            return "vvix_elevated"
        if vix_level <= 20.0 and spread <= 40.0:
            return "spread_calm"
        return "spread_moderate"

    def _pin_risk_state(self, spot_to_pin_distance_pct: float, oi_concentration: float) -> str:
        if abs(spot_to_pin_distance_pct) <= 0.35 and oi_concentration >= 0.60:
            return "pin_risk_high"
        if abs(spot_to_pin_distance_pct) <= 0.75 and oi_concentration >= 0.45:
            return "pin_risk_present"
        return "pin_risk_low"

    def _dealer_pressure_state(
        self,
        gamma_pressure_score: float,
        vanna_proxy: float,
        charm_proxy: float,
        call_put_imbalance: float,
    ) -> str:
        flow_pressure = (
            gamma_pressure_score
            + max(vanna_proxy, 0.0)
            + max(charm_proxy, 0.0)
            + abs(call_put_imbalance)
        )
        if flow_pressure >= 1.6:
            return "dealer_destabilising"
        if flow_pressure <= 0.45:
            return "dealer_supportive"
        return "dealer_mixed"

    def _strike_cluster_state(
        self,
        clusters: list[StrikeClusterObservation],
        oi_concentration: float,
        spot_to_pin_distance_pct: float,
    ) -> tuple[str, float | None]:
        if clusters:
            ordered = sorted(
                clusters,
                key=lambda cluster: cluster.open_interest + cluster.volume,
                reverse=True,
            )
            dominant_cluster = ordered[0]
            unique_strikes = {round(cluster.strike, 2) for cluster in ordered}
            if abs(dominant_cluster.distance_to_spot_pct) <= 0.35:
                return "live_pin_cluster", dominant_cluster.strike
            if len(unique_strikes) >= 3:
                return "distributed_cluster", dominant_cluster.strike
            return "isolated_cluster", dominant_cluster.strike
        if oi_concentration >= 0.65 and abs(spot_to_pin_distance_pct) <= 0.35:
            return "inferred_pin_cluster", None
        return "cluster_unset", None

    def _repeated_snapshot_state(self, payload: OptionsFlowContextInput) -> str:
        sequence = payload.repeated_snapshot_sequence
        if len(sequence) < 2:
            return "single_snapshot_only"
        first = sequence[0]
        last = sequence[-1]
        gamma_delta = last.gamma_pressure_score - first.gamma_pressure_score
        skew_delta = last.put_call_skew - first.put_call_skew
        iv_delta = last.front_atm_iv - first.front_atm_iv
        if gamma_delta >= 0.08 and (skew_delta >= 0.05 or iv_delta >= 0.01):
            return "escalating_pressure"
        if gamma_delta <= -0.08 and (skew_delta <= -0.05 or iv_delta <= -0.01):
            return "cooling_pressure"
        if last.spot_to_pin_distance_pct < first.spot_to_pin_distance_pct - 0.15:
            return "pinning_build"
        return "stable_recheck"

    def _skew_evolution_state(self, payload: OptionsFlowContextInput) -> str:
        sequence = payload.repeated_snapshot_sequence
        if len(sequence) < 2:
            return "skew_untracked"
        skew_delta = sequence[-1].put_call_skew - sequence[0].put_call_skew
        if skew_delta >= 0.08:
            return "downside_skew_expanding"
        if skew_delta <= -0.08:
            return "upside_skew_expanding"
        return "skew_stable"

    def _tenor_curve_state(self, payload: OptionsFlowContextInput) -> str:
        curve = payload.tenor_iv_curve
        if len(curve) >= 3:
            ordered_curve = sorted(curve, key=lambda point: point.tenor_dte)
            front = ordered_curve[0].atm_iv
            mid = ordered_curve[len(ordered_curve) // 2].atm_iv
            back = ordered_curve[-1].atm_iv
            if front > mid > back:
                return "backwardated_curve"
            if front < mid < back:
                return "contango_curve"
            if mid > max(front, back):
                return "hump_curve"
            return "flat_curve"
        if payload.front_atm_iv - payload.next_atm_iv >= 0.01:
            return "front_loaded_curve"
        if payload.next_atm_iv - payload.front_atm_iv >= 0.01:
            return "back_loaded_curve"
        return "two_point_flat_curve"

    def _pin_progression_state(
        self, sequence: list[PinProgressionPoint]
    ) -> tuple[str, float | None]:
        if len(sequence) < 2:
            return "untracked", None
        ordered = sorted(sequence, key=lambda point: point.ts)
        first = ordered[0].distance_to_pin_pct
        last = ordered[-1].distance_to_pin_pct
        delta = round(last - first, 4)
        if last <= 0.25 and abs(delta) <= 0.15:
            return "pin_stable", delta
        if delta <= -0.15:
            return "pinning_in", delta
        if delta >= 0.15:
            return "releasing_from_pin", delta
        return "pin_noise", delta

    def _surface_anchor_state(self, surface_anchor_to_spot_pct: float | None) -> str:
        if surface_anchor_to_spot_pct is None:
            return "surface_anchor_unset"
        if abs(surface_anchor_to_spot_pct) >= 0.75:
            return "anchored_away"
        if abs(surface_anchor_to_spot_pct) <= 0.35:
            return "anchored_to_spot"
        return "anchor_transitional"

    def _options_behavior_cluster(
        self,
        *,
        gamma_state: GammaState,
        skew_state: SkewState,
        dealer_pressure_state: str,
        pin_risk_state: str,
        strike_cluster_state: str,
        repeated_snapshot_state: str,
        tenor_curve_state: str,
        vix_spread_state: str,
        iv_rv_front_state: str,
        pin_progression_state: str,
        surface_anchor_state: str,
    ) -> str:
        if (
            vix_spread_state in {"vvix_dislocation", "vvix_elevated"}
            and iv_rv_front_state == "iv_rich"
        ):
            return "event_suppressed"
        if (
            gamma_state is GammaState.DESTABILISING
            and repeated_snapshot_state == "escalating_pressure"
            and skew_state is SkewState.DOWNSIDE_HEAVY
        ):
            return "negative_gamma_flush"
        if (
            strike_cluster_state in {"live_pin_cluster", "inferred_pin_cluster"}
            and pin_risk_state in {"pin_risk_high", "pin_risk_present"}
            and pin_progression_state in {"pinning_in", "pin_stable"}
            and dealer_pressure_state != "dealer_destabilising"
        ):
            return "pin_reversion_ready"
        if (
            gamma_state is GammaState.SUPPORTIVE
            and repeated_snapshot_state in {"cooling_pressure", "stable_recheck"}
            and tenor_curve_state
            in {
                "contango_curve",
                "flat_curve",
                "two_point_flat_curve",
                "back_loaded_curve",
            }
        ):
            return "compression_breakout_ready"
        if dealer_pressure_state == "dealer_destabilising":
            return "dealer_flow_tension"
        if surface_anchor_state == "anchored_away":
            return "anchored_translation_tension"
        return "balanced_options_state"
