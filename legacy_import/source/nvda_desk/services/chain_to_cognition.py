"""Prepared-runtime to cognition-input conversion service.

This service converts prepared runtime snapshots into the typed temporal and
options-flow inputs that feed the desk cognition runtime.
"""

from __future__ import annotations

from nvda_desk.schemas.checkpoints import CheckpointObservation
from nvda_desk.schemas.cognition import (
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.services.upstream_signal_checkpointing import (
    CHECKPOINT_CHAIN_TO_COGNITION_PARTICIPATION_MAPPING,
    CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING,
    CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
    append_unique_observation,
    checkpoint_observation,
    raise_checkpoint_failure,
)
from nvda_desk.services.upstream_signal_ingress import build_market_regime_input
from nvda_desk.schemas.dataset import (
    PreparedRuntimeDataset,
    PreparedRuntimeSnapshot,
    RealDataCognitionInputs,
)


class ChainToCognitionService:
    """Convert prepared runtime snapshots into cognition-ready inputs.

    Purpose:
        Bridge prepared-runtime outputs into the typed cognition ingress packets
        consumed by the desk runtime.
    Inputs:
        `PreparedRuntimeSnapshot` or `PreparedRuntimeDataset` objects.
    Outputs:
        `RealDataCognitionInputs` packets containing typed temporal, regime,
        and options-flow inputs plus checkpoint observations.
    Side Effects:
        None.
    Failure Modes:
        Raises `UpstreamSignalCheckpointError` if mutated participation packets
        claim baseline availability without a baseline value.
    Checkpoints:
        `upstream_signal.chain_to_cognition.regime_mapping_observed` and
        `upstream_signal.chain_to_cognition.participation_mapping_observed`
        expose the final wiring boundary.
    """

    def convert_snapshot(self, snapshot: PreparedRuntimeSnapshot) -> RealDataCognitionInputs:
        """Convert one prepared runtime snapshot into cognition-ready inputs.

        Purpose:
            Translate one prepared-runtime snapshot into the typed cognition
            inputs expected by the seven-stage desk runtime.
        Inputs:
            One `PreparedRuntimeSnapshot`.
        Outputs:
            One `RealDataCognitionInputs` packet with checkpoint observations.
        Side Effects:
            Appends bounded checkpoint observations to mutable upstream packets
            when they are present.
        Failure Modes:
            Raises `UpstreamSignalCheckpointError` if a mutated participation
            packet claims baseline availability without a baseline value.
        Checkpoints:
            `upstream_signal.chain_to_cognition.regime_mapping_observed` and
            `upstream_signal.chain_to_cognition.participation_mapping_observed`
            guard the final upstream wiring boundary.
        """

        checkpoint_observations: list[CheckpointObservation] = []
        if (
            snapshot.participation_baseline_packet is not None
            and snapshot.participation_baseline_packet.baseline_available
            and snapshot.participation_baseline_packet.baseline_interval_volume_share is None
        ):
            raise_checkpoint_failure(
                checkpoint_name=CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
                detail=(
                    'chain_to_cognition received a participation packet that claims baseline availability '
                    'without baseline interval-volume truth'
                ),
                input_snapshot={
                    'snapshot_ts': snapshot.ts.isoformat(),
                    'baseline_available': snapshot.participation_baseline_packet.baseline_available,
                    'baseline_interval_volume_share': snapshot.participation_baseline_packet.baseline_interval_volume_share,
                },
                output_snapshot={'real_data_cognition_inputs_created': False},
                timestamp=snapshot.ts,
            )

        temporal_input = TemporalContextInput(
            ts=snapshot.ts,
            next_expiry=snapshot.front_expiry,
            next_event_at=snapshot.next_event_at,
            live_event_snapshot=snapshot.live_event_snapshot,
            precursor_runtime_packet=snapshot.precursor_runtime_packet,
            desk_calendar_authority=snapshot.desk_calendar_authority,
            prior_session_return_pct=snapshot.prior_session_return_pct,
            intraday_move_pct=snapshot.intraday_move_pct,
            prior_close_price=snapshot.prior_close_price,
            official_open_price=snapshot.session_open_price,
            last_price=snapshot.spot_price,
            interval_volume_shares=snapshot.interval_volume_shares,
            cumulative_session_volume=snapshot.cumulative_session_volume,
            session_vwap=snapshot.session_vwap,
            distance_to_vwap_pct=snapshot.distance_to_vwap_pct,
            vwap_slope_5m_pct=snapshot.vwap_slope_5m_pct,
            opening_range_high_5m=snapshot.opening_range_high_5m,
            opening_range_low_5m=snapshot.opening_range_low_5m,
            opening_range_break_count=snapshot.opening_range_break_count,
            price_realised_vol_5m_pct=snapshot.price_realised_vol_5m_pct,
            price_realised_vol_15m_pct=snapshot.price_realised_vol_15m_pct,
            relative_volume_ratio=snapshot.relative_volume_ratio,
            session_bucket_label=(
                snapshot.participation_baseline_packet.session_bucket_label
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_interval_volume_share=(
                snapshot.participation_baseline_packet.observed_interval_volume_share
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_interval_volume_share_baseline=(
                snapshot.participation_baseline_packet.baseline_interval_volume_share
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_baseline_available=(
                snapshot.participation_baseline_packet.baseline_available
                if snapshot.participation_baseline_packet is not None
                else False
            ),
            rolling_range_5m_pct=snapshot.rolling_range_5m_pct,
            impulse_age_bars=snapshot.impulse_age_bars,
        )
        options_flow_input = OptionsFlowContextInput(
            spot_price=snapshot.spot_price,
            front_dte=snapshot.front_dte,
            next_dte=snapshot.next_dte,
            front_atm_iv=snapshot.front_atm_iv,
            next_atm_iv=snapshot.next_atm_iv,
            put_call_skew=snapshot.put_call_skew,
            gamma_pressure_score=snapshot.gamma_pressure_score,
            call_put_imbalance=snapshot.call_put_imbalance,
            oi_concentration=snapshot.oi_concentration,
            atm_straddle_value=snapshot.atm_straddle_value,
            front_realised_vol=snapshot.front_realised_vol,
            next_realised_vol=snapshot.next_realised_vol,
            spot_to_pin_distance_pct=snapshot.spot_to_pin_distance_pct,
            call_oi_near_spot=snapshot.call_oi_near_spot,
            put_oi_near_spot=snapshot.put_oi_near_spot,
            front_volume_near_spot=snapshot.front_volume_near_spot,
            next_volume_near_spot=snapshot.next_volume_near_spot,
            same_bucket_spread_bps=(
                snapshot.participation_baseline_packet.observed_spread_bps
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_spread_baseline_bps=(
                snapshot.participation_baseline_packet.baseline_spread_bps
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_trade_count=(
                snapshot.participation_baseline_packet.observed_trade_count
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            same_bucket_trade_count_baseline=(
                snapshot.participation_baseline_packet.baseline_trade_count
                if snapshot.participation_baseline_packet is not None
                else None
            ),
            nearby_strike_clusters=[
                StrikeClusterObservation(
                    strike=cluster.strike,
                    side=cluster.side,
                    open_interest=cluster.open_interest,
                    volume=cluster.volume,
                    distance_to_spot_pct=cluster.distance_to_spot_pct,
                )
                for cluster in snapshot.nearby_strike_clusters
            ],
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=point.ts,
                    front_atm_iv=point.front_atm_iv,
                    next_atm_iv=point.next_atm_iv,
                    put_call_skew=point.put_call_skew,
                    gamma_pressure_score=point.gamma_pressure_score,
                    spot_to_pin_distance_pct=point.spot_to_pin_distance_pct,
                )
                for point in snapshot.repeated_snapshot_sequence
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=point.tenor_dte, atm_iv=point.atm_iv)
                for point in snapshot.tenor_iv_curve
            ],
            pin_progression_sequence=[
                PinProgressionPoint(ts=point.ts, distance_to_pin_pct=point.distance_to_pin_pct)
                for point in snapshot.pin_progression_sequence
            ],
            surface_anchor_to_spot_pct=snapshot.surface_anchor_to_spot_pct,
        )
        regime_input = build_market_regime_input(snapshot.promoted_regime_packet)
        if snapshot.promoted_regime_packet is not None:
            for observation in snapshot.promoted_regime_packet.checkpoint_observations:
                append_unique_observation(checkpoint_observations, observation)
            append_unique_observation(
                checkpoint_observations,
                checkpoint_observation(
                    checkpoint_name=CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING,
                    input_snapshot={
                        'snapshot_ts': snapshot.ts.isoformat(),
                        'promoted_regime_packet_present': True,
                        'completeness_state': snapshot.promoted_regime_packet.completeness_state,
                    },
                    output_snapshot={
                        'regime_input_present': regime_input is not None,
                        'source_symbols': snapshot.promoted_regime_packet.source_symbols,
                    },
                    timestamp=snapshot.ts,
                ),
            )
        if snapshot.participation_baseline_packet is not None:
            for observation in snapshot.participation_baseline_packet.checkpoint_observations:
                append_unique_observation(checkpoint_observations, observation)
            append_unique_observation(
                checkpoint_observations,
                checkpoint_observation(
                    checkpoint_name=CHECKPOINT_CHAIN_TO_COGNITION_PARTICIPATION_MAPPING,
                    input_snapshot={
                        'snapshot_ts': snapshot.ts.isoformat(),
                        'participation_packet_present': True,
                        'session_bucket_label': snapshot.participation_baseline_packet.session_bucket_label,
                    },
                    output_snapshot={
                        'temporal_bucket': temporal_input.session_bucket_label,
                        'same_bucket_interval_volume_share_baseline': temporal_input.same_bucket_interval_volume_share_baseline,
                        'same_bucket_spread_bps': options_flow_input.same_bucket_spread_bps,
                        'same_bucket_trade_count': options_flow_input.same_bucket_trade_count,
                    },
                    timestamp=snapshot.ts,
                ),
            )
        return RealDataCognitionInputs(
            snapshot_ts=snapshot.ts,
            lineage=snapshot.lineage,
            temporal_input=temporal_input,
            regime_input=regime_input,
            options_flow_input=options_flow_input,
            normalised_features=snapshot.normalised_features,
            checkpoint_observations=checkpoint_observations,
        )

    def convert_dataset(
        self, prepared_dataset: PreparedRuntimeDataset
    ) -> list[RealDataCognitionInputs]:
        """Convert a prepared runtime dataset into cognition-ready input packets."""

        return [self.convert_snapshot(snapshot) for snapshot in prepared_dataset.snapshots]
