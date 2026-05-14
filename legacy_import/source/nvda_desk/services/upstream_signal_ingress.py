"""Helpers for bounded upstream signal promotion into prepared-runtime ingress.

These helpers keep upstream promotion explicit and inspectable without creating
new business stages or hidden inference paths.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import MarketRegimeContextInput
from nvda_desk.schemas.dataset import (
    PreparedParticipationBaselinePacket,
    PreparedRuntimeRegimePacket,
)
from nvda_desk.services.upstream_signal_checkpointing import (
    CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
    CHECKPOINT_PARTICIPATION_PROXY_BASELINE_OBSERVED,
    CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT,
    CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION,
    append_unique_observation,
    checkpoint_observation,
    raise_checkpoint_failure,
)


def session_bucket_label(ts: datetime, settings: Settings) -> str:
    """Return one bounded session bucket label in market-local time.

    Purpose:
        Classify one timestamp into the bounded session buckets admitted by the
        upstream signal tranche.
    Inputs:
        One timezone-aware timestamp and live settings carrying market hours.
    Outputs:
        One stable session-bucket label.
    Side Effects:
        None.
    Failure Modes:
        Delegates timezone conversion failures from the standard library if the
        timestamp or configured timezone are invalid.
    Checkpoints:
        This helper supports the participation-baseline checkpoints but does not
        raise checkpoint failures itself.
    """

    local_ts = ts.astimezone(ZoneInfo(settings.market_timezone))
    minutes = local_ts.hour * 60 + local_ts.minute
    open_minutes = settings.regular_open_hour * 60 + settings.regular_open_minute
    close_minutes = settings.regular_close_hour * 60 + settings.regular_close_minute
    if minutes < open_minutes:
        return "pre_market"
    if minutes >= close_minutes:
        return "after_hours"
    if minutes < open_minutes + 45:
        return "open_drive"
    if 12 * 60 <= minutes < 14 * 60:
        return "lunch"
    if minutes >= close_minutes - 15:
        return "close_auction"
    if minutes >= close_minutes - 60:
        return "power_hour"
    return "mid_session"


def build_market_regime_input(
    packet: PreparedRuntimeRegimePacket | None,
) -> MarketRegimeContextInput | None:
    """Build live regime ingress only when the promoted packet is complete.

    Purpose:
        Convert one promoted regime packet into the live Step-2 regime ingress
        contract without inventing missing breadth or concentration truth.
    Inputs:
        One optional `PreparedRuntimeRegimePacket`.
    Outputs:
        `MarketRegimeContextInput` when the packet is complete enough for live
        ingress; otherwise `None`.
    Side Effects:
        Appends one bounded checkpoint observation to the supplied packet when a
        packet is present.
    Failure Modes:
        Raises `UpstreamSignalCheckpointError` if a packet claims live-ingress
        completeness while breadth or concentration truth is absent.
    Checkpoints:
        `upstream_signal.regime_packet.complete_requires_breadth_concentration`
        guards the no-fake-completeness boundary.
    """

    if packet is None:
        return None
    input_snapshot = {
        "completeness_state": packet.completeness_state,
        "breadth_score_present": packet.breadth_score is not None,
        "concentration_score_present": packet.concentration_score is not None,
        "source_symbols": packet.source_symbols,
    }
    if (
        packet.completeness_state == "complete_for_live_ingress"
        and (packet.breadth_score is None or packet.concentration_score is None)
    ):
        raise_checkpoint_failure(
            checkpoint_name=CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION,
            detail="complete regime packets must carry breadth and concentration truth",
            input_snapshot=input_snapshot,
            output_snapshot={"regime_input_present": False},
            timestamp=packet.observed_at,
        )
    core_fields_present = all(
        value is not None
        for value in (
            packet.nq_return_pct,
            packet.es_return_pct,
            packet.sox_return_pct,
            packet.vix_level,
            packet.vvix_level,
            packet.us10y,
            packet.us2y,
            packet.usdjpy,
        )
    )
    if packet.breadth_score is None or packet.concentration_score is None or not core_fields_present:
        append_unique_observation(
            packet.checkpoint_observations,
            checkpoint_observation(
                checkpoint_name=CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION,
                input_snapshot=input_snapshot,
                output_snapshot={
                    "regime_input_present": False,
                    "fallback_reason": (
                        "breadth_or_concentration_deferred"
                        if packet.breadth_score is None or packet.concentration_score is None
                        else "core_regime_sources_missing"
                    ),
                    "core_fields_present": core_fields_present,
                },
                timestamp=packet.observed_at,
            ),
        )
        return None
    regime_input = MarketRegimeContextInput(
        nvda_return_pct=packet.nvda_return_pct,
        nq_return_pct=packet.nq_return_pct,
        es_return_pct=packet.es_return_pct,
        sox_return_pct=packet.sox_return_pct,
        breadth_score=packet.breadth_score,
        concentration_score=packet.concentration_score,
        vix_level=packet.vix_level,
        vvix_level=packet.vvix_level,
        us10y=packet.us10y,
        us2y=packet.us2y,
        usdjpy=packet.usdjpy,
    )
    append_unique_observation(
        packet.checkpoint_observations,
        checkpoint_observation(
            checkpoint_name=CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION,
            input_snapshot=input_snapshot,
            output_snapshot={
                "regime_input_present": True,
                "breadth_score": packet.breadth_score,
                "concentration_score": packet.concentration_score,
            },
            timestamp=packet.observed_at,
        ),
    )
    return regime_input


def build_participation_baseline_packet(
    *,
    ts: datetime,
    interval_volume_shares: float | None,
    relative_volume_ratio: float | None,
    settings: Settings,
    calendar_owner_present: bool,
    observed_spread_bps: float | None = None,
    baseline_spread_bps: float | None = None,
    observed_trade_count: int | None = None,
    baseline_trade_count: float | None = None,
) -> PreparedParticipationBaselinePacket:
    """Build one bounded participation packet from currently admitted runtime truth.

    Purpose:
        Reconstruct the lawful same-bucket participation proxy admitted by
        current runtime truth without inventing absent historical same-bucket,
        spread, or trade-count history.
    Inputs:
        One timestamp, observed interval volume, optional relative-volume ratio,
        optional spread/trade-count values, and market settings.
    Outputs:
        One `PreparedParticipationBaselinePacket` with explicit proxy-baseline
        checkpoint observations.
    Side Effects:
        None.
    Failure Modes:
        Raises `UpstreamSignalCheckpointError` if a present relative-volume
        ratio is non-positive or if a packet claims baseline availability while
        lacking a baseline interval-volume value.
    Checkpoints:
        `upstream_signal.participation_baseline.relative_volume_ratio_positive_when_present`
        and
        `upstream_signal.participation_baseline.available_requires_baseline_volume`
        guard the reconstruction boundary.
    """

    input_snapshot = {
        "interval_volume_shares_present": interval_volume_shares is not None,
        "relative_volume_ratio": relative_volume_ratio,
        "calendar_owner_present": calendar_owner_present,
        "observed_spread_bps_present": observed_spread_bps is not None,
        "observed_trade_count_present": observed_trade_count is not None,
    }
    if relative_volume_ratio is not None and relative_volume_ratio <= 0.0:
        raise_checkpoint_failure(
            checkpoint_name=CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT,
            detail="relative volume ratio must be positive when present",
            input_snapshot=input_snapshot,
            output_snapshot={"baseline_available": False},
            timestamp=ts,
        )

    baseline_interval_volume_share = None
    baseline_available = False
    fallback_state = "proxy_baseline_absent_not_historical_same_bucket"
    if interval_volume_shares is not None and relative_volume_ratio is not None:
        baseline_interval_volume_share = round(interval_volume_shares / relative_volume_ratio, 4)
        baseline_available = True
        fallback_state = "proxy_reconstructed_from_relative_volume_ratio_not_historical_same_bucket"
    packet = PreparedParticipationBaselinePacket(
        observed_at=ts,
        session_bucket_label=session_bucket_label(ts, settings),
        calendar_owner=(
            "financial_calendar_reference_bundle"
            if calendar_owner_present
            else "session_clock_fallback"
        ),
        observed_interval_volume_share=interval_volume_shares,
        baseline_interval_volume_share=baseline_interval_volume_share,
        relative_volume_ratio=relative_volume_ratio,
        observed_spread_bps=observed_spread_bps,
        baseline_spread_bps=baseline_spread_bps,
        observed_trade_count=observed_trade_count,
        baseline_trade_count=baseline_trade_count,
        baseline_available=baseline_available,
        fallback_state=fallback_state,
    )
    if packet.baseline_available and packet.baseline_interval_volume_share is None:
        raise_checkpoint_failure(
            checkpoint_name=CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
            detail="baseline_available packets must carry a baseline interval-volume value",
            input_snapshot=input_snapshot,
            output_snapshot={
                "baseline_available": packet.baseline_available,
                "baseline_interval_volume_share": packet.baseline_interval_volume_share,
            },
            timestamp=ts,
        )
    append_unique_observation(
        packet.checkpoint_observations,
        checkpoint_observation(
            checkpoint_name=CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT,
            input_snapshot=input_snapshot,
            output_snapshot={
                "baseline_available": packet.baseline_available,
                "baseline_interval_volume_share": packet.baseline_interval_volume_share,
                "fallback_state": packet.fallback_state,
            },
            timestamp=ts,
        ),
    )
    append_unique_observation(
        packet.checkpoint_observations,
        checkpoint_observation(
            checkpoint_name=CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
            input_snapshot=input_snapshot,
            output_snapshot={
                "baseline_available": packet.baseline_available,
                "baseline_interval_volume_share": packet.baseline_interval_volume_share,
                "calendar_owner": packet.calendar_owner,
            },
            timestamp=ts,
        ),
    )
    append_unique_observation(
        packet.checkpoint_observations,
        checkpoint_observation(
            checkpoint_name=CHECKPOINT_PARTICIPATION_PROXY_BASELINE_OBSERVED,
            input_snapshot=input_snapshot,
            output_snapshot={
                "baseline_available": packet.baseline_available,
                "baseline_interval_volume_share": packet.baseline_interval_volume_share,
                "fallback_state": packet.fallback_state,
                "historical_same_bucket_claim": False,
            },
            timestamp=ts,
        ),
    )
    return packet
