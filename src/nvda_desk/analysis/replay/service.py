"""Replay and comparison services for the bounded analysis-only subsystem."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from nvda_desk.contracts.replay import ReplayPacketLineage

DEFAULT_REPLAY_FIXTURE_ROOT = Path("fixtures/replay")


@dataclass(frozen=True)
class ReplayFixtureSource:
    """Describe the admitted replay fixture root without invoking live runtime flows."""

    fixture_root: Path
    readme_path: Path


@dataclass(frozen=True)
class ReplayComparisonResult:
    """Hold deterministic comparison output for bounded replay/evaluation work."""

    baseline_name: str
    candidate_name: str
    differing_fields: tuple[str, ...]
    baseline_only_fields: tuple[str, ...]
    candidate_only_fields: tuple[str, ...]
    baseline_snapshot: dict[str, Any]
    candidate_snapshot: dict[str, Any]


class ReplayEvaluationService:
    """Build replay lineage and compare prepared or fixture-backed artefacts."""

    def describe_fixture_source(
        self, fixture_root: Path = DEFAULT_REPLAY_FIXTURE_ROOT
    ) -> ReplayFixtureSource:
        resolved_root = fixture_root.resolve()
        return ReplayFixtureSource(
            fixture_root=resolved_root,
            readme_path=(resolved_root / "README.md").resolve(),
        )

    def build_lineage(
        self,
        *,
        packet_ids: list[str],
        replay_run_id: str | None = None,
    ) -> ReplayPacketLineage:
        return ReplayPacketLineage(packet_ids=list(packet_ids), replay_run_id=replay_run_id)

    def compare_outputs(
        self,
        *,
        baseline: Mapping[str, Any],
        candidate: Mapping[str, Any],
        baseline_name: str = "baseline",
        candidate_name: str = "candidate",
    ) -> ReplayComparisonResult:
        baseline_snapshot = deepcopy(dict(baseline))
        candidate_snapshot = deepcopy(dict(candidate))
        baseline_keys = set(baseline_snapshot)
        candidate_keys = set(candidate_snapshot)
        shared_keys = baseline_keys & candidate_keys
        differing_fields = tuple(
            sorted(key for key in shared_keys if baseline_snapshot[key] != candidate_snapshot[key])
        )
        return ReplayComparisonResult(
            baseline_name=baseline_name,
            candidate_name=candidate_name,
            differing_fields=differing_fields,
            baseline_only_fields=tuple(sorted(baseline_keys - candidate_keys)),
            candidate_only_fields=tuple(sorted(candidate_keys - baseline_keys)),
            baseline_snapshot=baseline_snapshot,
            candidate_snapshot=candidate_snapshot,
        )


def describe_replay_fixture_source(
    fixture_root: Path = DEFAULT_REPLAY_FIXTURE_ROOT,
) -> ReplayFixtureSource:
    """Describe the admitted replay fixture root via the bounded analysis service."""

    return ReplayEvaluationService().describe_fixture_source(fixture_root)
