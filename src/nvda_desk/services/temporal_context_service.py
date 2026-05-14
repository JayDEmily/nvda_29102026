"""Translate temporal inputs into bounded temporal stage outputs."""

from __future__ import annotations

from nvda_desk.contracts.temporal import (
    TemporalContextInput,
    TemporalContextOutput,
    build_source_temporal_payload,
)
from nvda_desk.domain.temporal.event_windows import active_window_tags, next_event_time_utc
from nvda_desk.domain.temporal.session_clock import classify_session_state


class TemporalContextService:
    """Coordinate temporal classification without absorbing temporal domain logic."""

    def evaluate(self, context: TemporalContextInput) -> TemporalContextOutput:
        if context.source_time_utc is None:
            raise ValueError("Temporal context requires source_time_utc for stage evaluation.")
        return TemporalContextOutput(
            **build_source_temporal_payload(
                source_time_utc=context.source_time_utc,
                source_date=context.source_date,
                source_time_raw=context.source_time_raw,
                source_time_kind=context.source_time_kind,
                source_timezone_raw=context.source_timezone_raw,
                captured_at_utc=context.captured_at_utc,
                persisted_at_utc=context.persisted_at_utc,
                source_provider=context.source_provider,
                source_channel=context.source_channel,
                time_granularity=context.time_granularity,
            ),
            session_state=classify_session_state(
                context.source_time_utc,
                source_timezone_raw=context.source_timezone_raw,
            ),
            active_tags=active_window_tags(context.source_time_utc, context.windows),
            next_event_time_utc=context.next_event_time_utc
            or next_event_time_utc(context.source_time_utc, context.windows),
            windows=list(context.windows),
        )
