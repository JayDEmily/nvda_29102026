"""Translate prepared runtime snapshots into regime contracts."""

from __future__ import annotations

from typing import Any, Mapping

from nvda_desk.contracts.regime import MarketRegimeContextInput


def build_regime_input(snapshot: Mapping[str, Any]) -> MarketRegimeContextInput:
    """Return one typed regime input from a prepared runtime snapshot mapping."""

    missing_fields: list[str] = []
    values: dict[str, float | None] = {}
    for field_name in ("nvda_return_pct", "nq_return_pct", "vix_level"):
        raw_value = snapshot.get(field_name)
        if raw_value is None:
            missing_fields.append(field_name)
            values[field_name] = None
            continue
        try:
            values[field_name] = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Prepared snapshot field '{field_name}' must be numeric when present."
            ) from exc
    return MarketRegimeContextInput(missing_fields=missing_fields, **values)
