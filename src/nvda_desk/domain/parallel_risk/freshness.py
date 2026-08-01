"""Deterministic source freshness helpers for the Parallel Risk Lane.

Freshness is a neutral state-of-play input. A stale source does not imply a trade action;
it lowers confidence in the current environmental read until downstream authority decides how
or whether to use that information.
"""

from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.parallel_risk import FreshnessRegisterEntry, ParallelRiskFreshnessState

DEFAULT_MAX_ALLOWED_AGE_SECONDS = 60


def build_freshness_register_entry(
    *,
    signal_id: str,
    source_time_utc: datetime | None = None,
    captured_at_utc: datetime | None = None,
    persisted_at_utc: datetime | None = None,
    generated_at_utc: datetime | None = None,
    max_allowed_age_seconds: int = DEFAULT_MAX_ALLOWED_AGE_SECONDS,
    source_refs: list[str] | None = None,
) -> FreshnessRegisterEntry:
    """Return a deterministic freshness register entry without config or workbook reads."""

    observed_age_seconds: int | None = None
    if source_time_utc is not None and generated_at_utc is not None:
        observed_age_seconds = max(
            0,
            int(
                (
                    _utc_compatible(generated_at_utc) - _utc_compatible(source_time_utc)
                ).total_seconds()
            ),
        )

    state = _classify_freshness(
        observed_age_seconds=observed_age_seconds,
        max_allowed_age_seconds=max_allowed_age_seconds,
    )
    return FreshnessRegisterEntry(
        signal_id=signal_id,
        source_time_utc=source_time_utc,
        captured_at_utc=captured_at_utc,
        persisted_at_utc=persisted_at_utc,
        generated_at_utc=generated_at_utc,
        max_allowed_age_seconds=max_allowed_age_seconds,
        observed_age_seconds=observed_age_seconds,
        freshness_state=state,
        impact_on_profile=_impact_for_state(state),
        source_refs=list(source_refs or []),
    )


def _classify_freshness(
    *, observed_age_seconds: int | None, max_allowed_age_seconds: int
) -> ParallelRiskFreshnessState:
    if observed_age_seconds is None:
        return "unknown"
    if observed_age_seconds <= max_allowed_age_seconds:
        return "fresh"
    if observed_age_seconds <= max_allowed_age_seconds * 2:
        return "ageing"
    return "stale"


def _impact_for_state(state: ParallelRiskFreshnessState) -> str:
    return {
        "fresh": "freshness_supports_current_state_read",
        "ageing": "freshness_ageing_uncertainty_contribution",
        "stale": "freshness_stale_uncertainty_contribution",
        "unknown": "freshness_unknown_state_of_play",
    }[state]


def _utc_compatible(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
