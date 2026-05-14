"""Translate prepared runtime snapshots into options-flow contracts."""

from __future__ import annotations

from typing import Any, Mapping

from nvda_desk.contracts.options_flow import OptionsFlowContextInput


def build_options_flow_input(snapshot: Mapping[str, Any]) -> OptionsFlowContextInput:
    """Return one typed options-flow input from a prepared runtime snapshot mapping."""

    missing_fields: list[str] = []
    values: dict[str, float | int | None] = {}
    for field_name, caster in (("spot_price", float), ("front_dte", int), ("next_dte", int)):
        raw_value = snapshot.get(field_name)
        if raw_value is None:
            missing_fields.append(field_name)
            values[field_name] = None
            continue
        try:
            values[field_name] = caster(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Prepared snapshot field '{field_name}' must be {caster.__name__} compatible when present."
            ) from exc
    return OptionsFlowContextInput(missing_fields=missing_fields, **values)
