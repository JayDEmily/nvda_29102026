"""Coordinate bounded ingress translation into typed stage inputs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from nvda_desk.contracts.stage_inputs import CommonStageContext, StageInputBundle
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
    common_context = _build_common_context(prepared_snapshot)
    common_context_ref = None if common_context is None else common_context.context_id
    temporal = build_temporal_input(prepared_snapshot)
    regime = build_regime_input(prepared_snapshot)
    if common_context_ref is not None:
        temporal = temporal.model_copy(update={"common_context_ref": common_context_ref})
        regime = regime.model_copy(update={"common_context_ref": common_context_ref})
    return StageInputBundle(
        common_context=common_context,
        temporal=temporal,
        regime=regime,
        options_flow=build_options_flow_input(
            prepared_snapshot, common_context_ref=common_context_ref
        ),
    )


def _normalise_prepared_snapshot(
    snapshot: Mapping[str, Any] | PreparedRuntimeDataset,
) -> Mapping[str, Any] | PreparedRuntimeSnapshot:
    if isinstance(snapshot, PreparedRuntimeDataset):
        return snapshot.primary_snapshot
    return snapshot


def _build_common_context(
    snapshot: Mapping[str, Any] | PreparedRuntimeSnapshot,
) -> CommonStageContext | None:
    if not isinstance(snapshot, PreparedRuntimeSnapshot) or snapshot.prepared_envelope is None:
        return None
    authority = snapshot.prepared_envelope
    return CommonStageContext(
        context_id=f"stage-context::{authority.prepared_id}",
        prepared_id=authority.prepared_id,
        prepared_fingerprint=authority.prepared_fingerprint,
        input_schema_versions=dict(authority.input_schema_versions),
        preparation_policy_version=authority.preparation_policy_version,
        temporal_reference_id=authority.prepared_id,
        completeness_state=authority.completeness_state,
        resolution_receipt_ids=tuple(
            receipt.receipt_id for receipt in authority.resolution_receipts
        ),
    )
