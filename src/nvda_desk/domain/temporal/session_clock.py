from __future__ import annotations

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def classify_session_state(
    source_time_utc: datetime,
    *,
    source_timezone_raw: str | None = None,
) -> str:
    """Return the governed session state for one source observation timestamp.

    ``source_time_utc`` remains the UTC source-observation truth. Session wall-clock
    thresholds are evaluated only after explicit conversion into the admitted source
    timezone. When no source timezone is supplied, UTC is used explicitly rather than
    silently treating a UTC wall clock as an exchange/session wall clock.
    """

    observed_time = _source_observation_wall_time(
        source_time_utc=source_time_utc,
        source_timezone_raw=source_timezone_raw,
    )
    if observed_time < time(9, 30):
        return "pre_open"
    if observed_time < time(10, 30):
        return "opening"
    if observed_time < time(15, 30):
        return "mid_session"
    if observed_time < time(16, 0):
        return "closing"
    return "post_close"


def _source_observation_wall_time(
    *,
    source_time_utc: datetime,
    source_timezone_raw: str | None,
) -> time:
    timezone_name = source_timezone_raw or "UTC"
    try:
        source_timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown_source_timezone_raw:{timezone_name}") from exc

    if source_time_utc.tzinfo is None:
        utc_observation = source_time_utc.replace(tzinfo=UTC)
    else:
        utc_observation = source_time_utc.astimezone(UTC)
    return utc_observation.astimezone(source_timezone).timetz().replace(tzinfo=None)
