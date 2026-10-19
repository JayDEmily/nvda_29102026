"""Owner-local exact controlled arithmetic and canonical identity representation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

_FACTORIES = {
    "RawSignalCatalogueId": raw_api.RawSignalCatalogueId,
    "observation_occurrence_id": raw_api.observation_occurrence_id,
    "ingestion_sequence_scope": raw_api.ingestion_sequence_scope,
}
_IDENTITIES = {
    type(factory("R034" if name == "RawSignalCatalogueId" else "identity")): name
    for name, factory in _FACTORIES.items()
}


def timestamp(value: datetime) -> str:
    return (
        f"{value.year:04d}-{value.month:02d}-{value.day:02d}T"
        f"{value.hour:02d}:{value.minute:02d}:{value.second:02d}.{value.microsecond:06d}Z"
    )


def tagged(value: Any) -> Any:
    if type(value) in _IDENTITIES:
        return {"kind": _IDENTITIES[type(value)], "value": value.value}
    if type(value) is Decimal:
        sign, digits, exponent = value.as_tuple()
        return {
            "kind": "decimal",
            "sign": sign,
            "digits": "".join(str(item) for item in digits),
            "exponent": exponent,
        }
    if type(value) is datetime:
        return timestamp(value)
    if type(value) is timedelta:
        return (value.days * 86400 + value.seconds) * 1000000 + value.microseconds
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: tagged(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [tagged(item) for item in value]
    if type(value) is dict:
        return {key: tagged(item) for key, item in value.items()}
    if value is None or type(value) in (bool, int, str):
        return value
    raise TypeError("unsupported controlled measurement representation")


def canonical(value: Any) -> bytes:
    return json.dumps(
        tagged(value), sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def midpoint(bid: Decimal, ask: Decimal) -> Decimal | None:
    """Exact coefficient alignment/division; no ambient Decimal arithmetic."""
    try:
        if not bid.is_finite() or not ask.is_finite():
            return None

        def coefficient(value: Decimal) -> tuple[int, int]:
            sign, digits, exponent = value.as_tuple()
            n = 0
            for digit in digits:
                n = n * 10 + digit
            return (-n if sign else n), int(exponent)

        a, ae = coefficient(bid)
        b, be = coefficient(ask)
        exponent = min(ae, be)
        numerator = a * 10 ** (ae - exponent) + b * 10 ** (be - exponent)
        if numerator % 2:
            number, exponent = numerator * 5, exponent - 1
        else:
            number = numerator // 2
        sign, number = int(number < 0), abs(number)
        digits = []
        while number:
            number, digit = divmod(number, 10)
            digits.append(digit)
        return Decimal((sign, tuple(reversed(digits)) if digits else (0,), exponent))
    except (ArithmeticError, ValueError, MemoryError):
        return None
