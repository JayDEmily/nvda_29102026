"""Translate prepared runtime snapshots into options-flow contracts."""

from __future__ import annotations

from typing import Any

from nvda_desk.contracts.options_flow import OptionsEvidenceEnvelope, OptionsFlowContextInput
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeSnapshot


def build_options_flow_input(
    snapshot: PreparedRuntimeSnapshot | OptionsEvidenceEnvelope,
    *,
    common_context_ref: str | None = None,
) -> OptionsFlowContextInput:
    """Return typed options-stage primitives from repository-owned options authority."""

    if isinstance(snapshot, OptionsEvidenceEnvelope):
        source: Any = snapshot
        evidence_ref = snapshot.evidence_id
    elif isinstance(snapshot, PreparedRuntimeSnapshot):
        source = snapshot
        evidence_ref = None
    else:
        raise TypeError("typed options evidence envelope or prepared snapshot authority required")

    missing_fields: list[str] = []
    values: dict[str, float | int | None] = {}
    for field_name, caster in (("spot_price", float), ("front_dte", int), ("next_dte", int)):
        raw_value = getattr(source, field_name, None)
        if isinstance(source, PreparedRuntimeSnapshot):
            raw_value = source.get(field_name)
        if raw_value is None:
            missing_fields.append(field_name)
            values[field_name] = None
            continue
        try:
            values[field_name] = caster(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Prepared options authority field '{field_name}' must be {caster.__name__} compatible when present."
            ) from exc
    return OptionsFlowContextInput(
        common_context_ref=common_context_ref,
        options_evidence_ref=evidence_ref,
        missing_fields=missing_fields,
        **values,
    )
