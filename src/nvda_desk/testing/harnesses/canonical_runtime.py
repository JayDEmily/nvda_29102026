"""Assemble the bounded canonical specimen path without invoking live runtime flows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nvda_desk.analysis.replay import ReplayEvaluationService
from nvda_desk.contracts.replay import ReplayPacketLineage
from nvda_desk.contracts.trace_review import (
    BoundedTraceFixturePack,
    BoundedTraceScenario,
)

DEFAULT_DMP_V3_FIXTURE_ROOT = Path("fixtures/dmp_v3")
DEFAULT_REPLAY_FIXTURE_ROOT = Path("fixtures/replay")
DEFAULT_TRACE_REVIEW_FIXTURE_ROOT = Path("fixtures/trace_review")


@dataclass(frozen=True)
class CanonicalRuntimeHarnessPaths:
    """Describe the admitted specimen-path fixture roots."""

    replay_root: Path
    trace_review_root: Path
    dmp_v3_root: Path


@dataclass(frozen=True)
class CanonicalRuntimeSpecimen:
    """Hold the bounded specimen-path inputs assembled by the harness."""

    fixture_paths: CanonicalRuntimeHarnessPaths
    replay_lineage: ReplayPacketLineage
    trace_review_pack: BoundedTraceFixturePack


class CanonicalRuntimeHarness:
    """Build the admitted specimen-path bundle from existing fixture roots only."""

    def describe_fixture_paths(self) -> CanonicalRuntimeHarnessPaths:
        return CanonicalRuntimeHarnessPaths(
            replay_root=DEFAULT_REPLAY_FIXTURE_ROOT.resolve(),
            trace_review_root=DEFAULT_TRACE_REVIEW_FIXTURE_ROOT.resolve(),
            dmp_v3_root=DEFAULT_DMP_V3_FIXTURE_ROOT.resolve(),
        )

    def build_specimen(
        self,
        *,
        packet_ids: list[str],
        replay_run_id: str | None = None,
        scenario_ids: list[str] | None = None,
    ) -> CanonicalRuntimeSpecimen:
        fixture_paths = self.describe_fixture_paths()
        replay_service = ReplayEvaluationService()
        lineage = replay_service.build_lineage(packet_ids=packet_ids, replay_run_id=replay_run_id)
        scenario_ids = list(scenario_ids or [])
        trace_review_pack = BoundedTraceFixturePack(
            scenario_ids=scenario_ids,
            scenarios=[
                BoundedTraceScenario(scenario_id=scenario_id) for scenario_id in scenario_ids
            ],
        )
        return CanonicalRuntimeSpecimen(
            fixture_paths=fixture_paths,
            replay_lineage=lineage,
            trace_review_pack=trace_review_pack,
        )


def build_canonical_runtime_specimen(
    *,
    packet_ids: list[str],
    replay_run_id: str | None = None,
    scenario_ids: list[str] | None = None,
) -> CanonicalRuntimeSpecimen:
    """Build the bounded canonical specimen bundle via the test-only harness."""

    return CanonicalRuntimeHarness().build_specimen(
        packet_ids=packet_ids,
        replay_run_id=replay_run_id,
        scenario_ids=scenario_ids,
    )
