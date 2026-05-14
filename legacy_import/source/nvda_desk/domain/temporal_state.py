from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from enum import StrEnum
from functools import lru_cache
from math import fabs
from pathlib import Path
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.config_models import (
    CoefficientAuthorityDocument,
    TemporalThresholdId,
    TimingParameterId,
)
from nvda_desk.domain.session_clock import SessionClockPhase


class ClockEnvelope(StrEnum):
    PRE_MARKET = "pre_market"
    REGULAR_HOURS = "regular_hours"
    AFTER_HOURS = "after_hours"
    CLOSED = "closed"


@dataclass(frozen=True)
class TemporalSignalInput:
    ts: datetime
    prior_session_return_pct: float = 0.0
    intraday_move_pct: float = 0.0
    prior_close_price: float | None = None
    official_open_price: float | None = None
    last_price: float | None = None
    interval_volume_shares: float | None = None
    cumulative_session_volume: float | None = None
    session_vwap: float | None = None
    distance_to_vwap_pct: float | None = None
    vwap_slope_5m_pct: float | None = None
    opening_range_high_5m: float | None = None
    opening_range_low_5m: float | None = None
    opening_range_break_count: int | None = None
    price_realised_vol_5m_pct: float | None = None
    price_realised_vol_15m_pct: float | None = None
    relative_volume_ratio: float | None = None
    rolling_range_5m_pct: float | None = None
    impulse_age_bars: int | None = None


@dataclass(frozen=True)
class TemporalState:
    phase: SessionClockPhase
    behavioural_phase: SessionClockPhase
    clock_envelope: ClockEnvelope
    market_timezone: str
    ts_market: datetime
    minutes_since_open: int | None
    minutes_to_close: int | None
    is_pre_market: bool
    is_regular_hours: bool
    is_power_hour: bool
    phase_confidence: float
    signal_coverage_ratio: float
    evidence_tags: tuple[str, ...]




@lru_cache(maxsize=8)
def _load_governed_coefficient_authority(path: str) -> CoefficientAuthorityDocument:
    """Load the governed coefficient authority document from one resolved path."""

    return CoefficientAuthorityDocument.from_yaml_path(Path(path))


class TemporalStateClassifier:
    """Signal-aware Step-1 temporal classifier.

    The clock remains the prior. Behavioural phase may override the legacy
    bucket when sufficient primitive Step-1 evidence is available.
    """

    _SIGNAL_FIELDS: tuple[str, ...] = (
        "distance_to_vwap_pct",
        "vwap_slope_5m_pct",
        "opening_range_break_count",
        "price_realised_vol_5m_pct",
        "price_realised_vol_15m_pct",
        "relative_volume_ratio",
        "rolling_range_5m_pct",
        "impulse_age_bars",
    )

    def __init__(self, settings: Settings):
        self._tz = ZoneInfo(settings.market_timezone)
        self._market_timezone = settings.market_timezone
        self._pre_market_start = time(hour=settings.pre_market_start_hour)
        self._regular_open = time(
            hour=settings.regular_open_hour,
            minute=settings.regular_open_minute,
        )
        self._regular_close = time(
            hour=settings.regular_close_hour,
            minute=settings.regular_close_minute,
        )
        self._after_hours_end = time(hour=settings.after_hours_end_hour)
        authority_document = _load_governed_coefficient_authority(
            str(Path(settings.coefficient_authority_path).resolve())
        )
        self._authority_version = authority_document.authority_version
        self._thresholds = {
            threshold.threshold_id: float(threshold.baseline)
            for threshold in authority_document.temporal_thresholds
            if threshold.activation_gate == "Gate 126"
        }
        self._timing_parameters = {
            parameter.parameter_id: int(parameter.baseline)
            for parameter in authority_document.timing_parameters
            if parameter.activation_gate == "Gate 126"
        }

    def classify(self, payload: TemporalSignalInput) -> TemporalState:
        market_ts = (
            payload.ts.astimezone(self._tz)
            if payload.ts.tzinfo
            else payload.ts.replace(tzinfo=self._tz)
        )
        now_min = market_ts.hour * 60 + market_ts.minute
        pre_market_start_min = self._minutes_from_midnight(self._pre_market_start)
        regular_open_min = self._minutes_from_midnight(self._regular_open)
        regular_close_min = self._minutes_from_midnight(self._regular_close)
        after_hours_end_min = self._minutes_from_midnight(self._after_hours_end)

        minutes_since_open: int | None = None
        minutes_to_close: int | None = None
        is_pre_market = False
        is_regular_hours = False
        is_power_hour = False
        evidence: list[str] = []
        coverage_ratio = self._signal_coverage_ratio(payload)

        if now_min < pre_market_start_min or now_min >= after_hours_end_min:
            phase = SessionClockPhase.CLOSED
            envelope = ClockEnvelope.CLOSED
            confidence = 1.0
        elif pre_market_start_min <= now_min < regular_open_min:
            phase = SessionClockPhase.PRE_MARKET
            envelope = ClockEnvelope.PRE_MARKET
            confidence = 0.98
            is_pre_market = True
        elif regular_open_min <= now_min < regular_close_min:
            envelope = ClockEnvelope.REGULAR_HOURS
            is_regular_hours = True
            minutes_since_open = now_min - regular_open_min
            minutes_to_close = regular_close_min - now_min
            legacy_phase = self._legacy_phase(
                minutes_since_open=minutes_since_open, minutes_to_close=minutes_to_close
            )
            phase, evidence = self._behavioural_phase(
                payload,
                minutes_since_open=minutes_since_open,
                minutes_to_close=minutes_to_close,
                legacy_phase=legacy_phase,
                coverage_ratio=coverage_ratio,
            )
            confidence = self._phase_confidence(
                legacy_phase=legacy_phase,
                phase=phase,
                coverage_ratio=coverage_ratio,
                evidence=evidence,
            )
            is_power_hour = phase is SessionClockPhase.POWER_HOUR
        else:
            phase = SessionClockPhase.AFTER_HOURS
            envelope = ClockEnvelope.AFTER_HOURS
            confidence = 0.95

        return TemporalState(
            phase=phase,
            behavioural_phase=phase,
            clock_envelope=envelope,
            market_timezone=self._market_timezone,
            ts_market=market_ts,
            minutes_since_open=minutes_since_open,
            minutes_to_close=minutes_to_close,
            is_pre_market=is_pre_market,
            is_regular_hours=is_regular_hours,
            is_power_hour=is_power_hour,
            phase_confidence=confidence,
            signal_coverage_ratio=coverage_ratio,
            evidence_tags=tuple(evidence),
        )

    def _behavioural_phase(
        self,
        payload: TemporalSignalInput,
        *,
        minutes_since_open: int,
        minutes_to_close: int,
        legacy_phase: SessionClockPhase,
        coverage_ratio: float,
    ) -> tuple[SessionClockPhase, list[str]]:
        if minutes_to_close <= self._timing_parameter(TimingParameterId.UNWIND_WINDOW_MIN):
            return SessionClockPhase.DEALER_UNWIND_CLOSE, [
                "close_window:dealer_unwind",
                f"timing_authority_version:{self._authority_version}",
            ]
        if minutes_to_close <= self._timing_parameter(TimingParameterId.POWER_HOUR_WINDOW_MIN):
            evidence = [
                "close_window:power_hour",
                f"timing_authority_version:{self._authority_version}",
            ]
            if (payload.relative_volume_ratio or 0.0) >= 1.1:
                evidence.append("power_hour:active_volume")
            return SessionClockPhase.POWER_HOUR, evidence

        if coverage_ratio < 0.375:
            return legacy_phase, [
                "signal_coverage:insufficient",
                f"fallback_phase:{legacy_phase.value}",
            ]

        rv5_bps = self._pct_to_bps(payload.price_realised_vol_5m_pct)
        rel_volume = payload.relative_volume_ratio or 0.0
        vwap_distance_bps = self._pct_to_bps_abs(payload.distance_to_vwap_pct)
        vwap_slope_bps = self._pct_to_bps_abs(payload.vwap_slope_5m_pct)
        range5_bps = self._pct_to_bps(payload.rolling_range_5m_pct)
        break_count = payload.opening_range_break_count or 0
        impulse_age_minutes = (
            int(payload.impulse_age_bars) if payload.impulse_age_bars is not None else 999
        )

        if minutes_since_open <= 75:
            disorder_hits = sum(
                (
                    break_count >= 2,
                    rel_volume >= self._threshold(TemporalThresholdId.OPEN_DISORDER_RELVOL_MIN),
                    vwap_distance_bps >= self._threshold(TemporalThresholdId.OPEN_DISORDER_VWAP_DIST_BPS_MIN),
                    range5_bps >= 80.0,
                    rv5_bps >= self._threshold(TemporalThresholdId.OPEN_DISORDER_RV5_BPS_MIN),
                    impulse_age_minutes <= 2,
                )
            )
            if disorder_hits >= 3:
                return SessionClockPhase.OPEN_DISORDER, [
                    "behavioural_phase:signal_override",
                    f"open_disorder_hits:{disorder_hits}",
                    f"threshold_authority_version:{self._authority_version}",
                ]

        if 10 <= minutes_since_open <= 120:
            anchor_hits = sum(
                (
                    vwap_distance_bps <= self._threshold(TemporalThresholdId.ANCHOR_VWAP_DIST_BPS_MAX),
                    rv5_bps <= self._threshold(TemporalThresholdId.ANCHOR_RV5_BPS_MAX),
                    break_count <= 1,
                    self._threshold(TemporalThresholdId.ANCHOR_RELVOL_MIN)
                    <= rel_volume
                    <= self._threshold(TemporalThresholdId.ANCHOR_RELVOL_MAX),
                    impulse_age_minutes >= self._threshold(TemporalThresholdId.ANCHOR_IMPULSE_AGE_MIN),
                )
            )
            if anchor_hits >= 4:
                return SessionClockPhase.EARLY_ANCHOR, [
                    "behavioural_phase:signal_override",
                    f"early_anchor_hits:{anchor_hits}",
                    f"threshold_authority_version:{self._authority_version}",
                ]

        if minutes_since_open >= 90:
            compression_hits = sum(
                (
                    vwap_distance_bps <= self._threshold(TemporalThresholdId.COMPRESSION_VWAP_DIST_BPS_MAX),
                    range5_bps <= self._threshold(TemporalThresholdId.COMPRESSION_RANGE5_BPS_MAX),
                    rel_volume <= self._threshold(TemporalThresholdId.COMPRESSION_RELVOL_MAX),
                    rv5_bps <= self._threshold(TemporalThresholdId.COMPRESSION_RV5_BPS_MAX),
                    impulse_age_minutes >= 6,
                )
            )
            if compression_hits >= 4:
                return SessionClockPhase.MIDDAY_COMPRESSION, [
                    "behavioural_phase:signal_override",
                    f"midday_compression_hits:{compression_hits}",
                    f"threshold_authority_version:{self._authority_version}",
                ]

        if minutes_since_open >= 45:
            trend_hits = sum(
                (
                    vwap_distance_bps >= self._threshold(TemporalThresholdId.TREND_VWAP_DIST_BPS_MIN),
                    vwap_slope_bps >= self._threshold(TemporalThresholdId.TREND_VWAP_SLOPE_BPS_MIN),
                    rel_volume >= self._threshold(TemporalThresholdId.TREND_RELVOL_MIN),
                    range5_bps >= 45.0,
                    impulse_age_minutes <= self._threshold(TemporalThresholdId.TREND_IMPULSE_AGE_MAX),
                )
            )
            if trend_hits >= 4:
                return (
                    (
                        SessionClockPhase.INSTITUTIONAL_REPRICING
                        if minutes_since_open < 180
                        else SessionClockPhase.POST_LUNCH_DRIFT
                    ),
                    [
                        "behavioural_phase:signal_override",
                        f"trend_hits:{trend_hits}",
                        f"threshold_authority_version:{self._authority_version}",
                    ],
                )

        return legacy_phase, [f"fallback_phase:{legacy_phase.value}"]

    def _legacy_phase(self, *, minutes_since_open: int, minutes_to_close: int) -> SessionClockPhase:
        if minutes_to_close <= self._timing_parameter(TimingParameterId.UNWIND_WINDOW_MIN):
            return SessionClockPhase.DEALER_UNWIND_CLOSE
        if minutes_to_close <= self._timing_parameter(TimingParameterId.POWER_HOUR_WINDOW_MIN):
            return SessionClockPhase.POWER_HOUR
        if minutes_since_open < 30:
            return SessionClockPhase.OPEN_DISORDER
        if minutes_since_open < 90:
            return SessionClockPhase.EARLY_ANCHOR
        if minutes_since_open < 150:
            return SessionClockPhase.INSTITUTIONAL_REPRICING
        if minutes_since_open < 240:
            return SessionClockPhase.MIDDAY_COMPRESSION
        return SessionClockPhase.POST_LUNCH_DRIFT

    def _phase_confidence(
        self,
        *,
        legacy_phase: SessionClockPhase,
        phase: SessionClockPhase,
        coverage_ratio: float,
        evidence: list[str],
    ) -> float:
        if phase == legacy_phase and coverage_ratio < 0.375:
            return 0.72
        base = 0.82 if phase == legacy_phase else 0.88
        if any(
            tag.startswith("open_disorder_hits:")
            or tag.startswith("early_anchor_hits:")
            or tag.startswith("midday_compression_hits:")
            or tag.startswith("trend_hits:")
            for tag in evidence
        ):
            base += 0.04
        return min(0.98, round(base + min(0.08, coverage_ratio * 0.1), 4))

    def _threshold(self, threshold_id: TemporalThresholdId) -> float:
        return self._thresholds[threshold_id]

    def _timing_parameter(self, parameter_id: TimingParameterId) -> int:
        return self._timing_parameters[parameter_id]

    def _pct_to_bps(self, value: float | None) -> float:
        return (value or 0.0) * 100.0

    def _pct_to_bps_abs(self, value: float | None) -> float:
        return fabs(value or 0.0) * 100.0

    def _signal_coverage_ratio(self, payload: TemporalSignalInput) -> float:
        present = sum(1 for field in self._SIGNAL_FIELDS if getattr(payload, field) is not None)
        return round(present / len(self._SIGNAL_FIELDS), 4)

    def _minutes_from_midnight(self, value: time) -> int:
        return value.hour * 60 + value.minute
