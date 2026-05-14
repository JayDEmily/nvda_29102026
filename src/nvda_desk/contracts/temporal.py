"""Temporal ingress and output contracts for the bounded runtime rebuild."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SourceTemporalStandard(BaseModel):
    """Canonical source temporal carrier admitted above packet emission time."""

    model_config = ConfigDict(extra="forbid")

    source_time_raw: str | None = None
    source_time_kind: str | None = None
    source_timezone_raw: str | None = None
    source_time_utc: datetime | None = None
    source_date: date | None = None
    captured_at_utc: datetime | None = None
    persisted_at_utc: datetime | None = None
    source_provider: str | None = None
    source_channel: str | None = None
    time_granularity: str | None = None

    @model_validator(mode="after")
    def _require_source_temporal_truth(self) -> "SourceTemporalStandard":
        if self.source_time_utc is None and self.source_date is None:
            raise ValueError("source temporal standard requires source_time_utc or source_date")
        return self


class TemporalEventWindow(BaseModel):
    """One bounded temporal event window."""

    model_config = ConfigDict(extra="forbid")

    event_id: str
    window_start_utc: datetime
    window_end_utc: datetime
    tags: list[str] = Field(default_factory=list)


class TemporalContextInput(SourceTemporalStandard):
    """Typed temporal input into the deterministic runtime spine."""

    next_event_time_utc: datetime | None = None
    windows: list[TemporalEventWindow] = Field(default_factory=list)


class TemporalContextOutput(SourceTemporalStandard):
    """Typed temporal output from the bounded temporal stage."""

    session_state: str = "unknown"
    active_tags: list[str] = Field(default_factory=list)
    next_event_time_utc: datetime | None = None
    windows: list[TemporalEventWindow] = Field(default_factory=list)


def build_source_temporal_payload(
    *,
    source_time_utc: datetime | None = None,
    source_date: date | None = None,
    source_time_raw: str | None = None,
    source_time_kind: str | None = None,
    source_timezone_raw: str | None = None,
    captured_at_utc: datetime | None = None,
    persisted_at_utc: datetime | None = None,
    source_provider: str | None = None,
    source_channel: str | None = None,
    time_granularity: str | None = None,
) -> dict[str, object | None]:
    """Return one canonical source temporal payload mapping."""

    if source_time_kind is None:
        if source_time_utc is not None:
            source_time_kind = "timestamp"
        elif source_date is not None:
            source_time_kind = "date"
    if time_granularity is None:
        if source_time_utc is not None:
            time_granularity = "timestamp"
        elif source_date is not None:
            time_granularity = "date"
    return {
        "source_time_raw": source_time_raw,
        "source_time_kind": source_time_kind,
        "source_timezone_raw": source_timezone_raw,
        "source_time_utc": source_time_utc,
        "source_date": source_date,
        "captured_at_utc": captured_at_utc,
        "persisted_at_utc": persisted_at_utc,
        "source_provider": source_provider,
        "source_channel": source_channel,
        "time_granularity": time_granularity,
    }
