from __future__ import annotations

from typing import Annotated, Any

from pydantic import BeforeValidator


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        value = cleaned
    return float(value)


def normalise_optional_vol_fraction(value: Any) -> float | None:
    """Normalise obvious percent-style volatility inputs to decimal fractions."""

    coerced = _coerce_float(value)
    if coerced is None:
        return None
    if abs(coerced) >= 5.0:
        return round(coerced / 100.0, 6)
    return coerced


def normalise_required_vol_fraction(value: Any) -> float:
    """Require one volatility-like value and normalise obvious percent-style input."""

    normalised = normalise_optional_vol_fraction(value)
    if normalised is None:
        raise ValueError("volatility-like value is required")
    return normalised


VolFraction = Annotated[float, BeforeValidator(normalise_required_vol_fraction)]
OptionalVolFraction = Annotated[float | None, BeforeValidator(normalise_optional_vol_fraction)]
