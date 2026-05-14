"""Coordinate bounded ingress translation into typed stage inputs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeDataset, PreparedRuntimeSnapshot

from .options_mapper import build_options_flow_input
from .regime_mapper import build_regime_input
from .temporal_mapper import build_temporal_input


class CognitionIngressTranslator:
    """Translate one prepared runtime snapshot into a typed stage-input bundle."""

    def convert_snapshot(
        self, snapshot: Mapping[str, Any] | PreparedRuntimeDataset
    ) -> StageInputBundle:
        return convert_snapshot(snapshot)


def convert_snapshot(snapshot: Mapping[str, Any] | PreparedRuntimeDataset) -> StageInputBundle:
    """Return the typed stage-input bundle for one prepared substrate."""

    prepared_snapshot = _normalise_prepared_snapshot(snapshot)
    return StageInputBundle(
        temporal=build_temporal_input(prepared_snapshot),
        regime=build_regime_input(prepared_snapshot),
        options_flow=build_options_flow_input(prepared_snapshot),
    )


def _normalise_prepared_snapshot(
    snapshot: Mapping[str, Any] | PreparedRuntimeDataset,
) -> Mapping[str, Any] | PreparedRuntimeSnapshot:
    if isinstance(snapshot, PreparedRuntimeDataset):
        return snapshot.primary_snapshot
    return snapshot
