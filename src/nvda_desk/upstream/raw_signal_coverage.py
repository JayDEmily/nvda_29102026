"""Native upstream-signal coverage map and fail-closed scope-lock validation."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.upstream_signal import (
    UpstreamSignalCoverageEntry,
    UpstreamSignalCoverageMap,
)


class UpstreamSignalScopeLockError(ValueError):
    """Raised when an upstream signal family is outside the admitted coverage map."""


def build_upstream_signal_coverage_map(
    entries: Iterable[UpstreamSignalCoverageEntry],
) -> UpstreamSignalCoverageMap:
    """Build a deterministic coverage map from admitted upstream signal entries."""

    sorted_entries = sorted(list(entries), key=lambda entry: entry.signal_family_id)
    seen: set[str] = set()
    for entry in sorted_entries:
        if entry.signal_family_id in seen:
            raise UpstreamSignalScopeLockError(f"duplicate_signal_family:{entry.signal_family_id}")
        seen.add(entry.signal_family_id)
    return UpstreamSignalCoverageMap(entries=sorted_entries)


def validate_upstream_signal_scope(
    *,
    signal_family_id: str,
    coverage_map: UpstreamSignalCoverageMap,
) -> UpstreamSignalCoverageEntry:
    """Return the admitted coverage entry or fail closed for unlisted signal families."""

    try:
        return coverage_map.require(signal_family_id)
    except KeyError as exc:
        raise UpstreamSignalScopeLockError(f"unlisted_signal_family:{signal_family_id}") from exc
