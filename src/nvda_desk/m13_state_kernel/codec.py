"""Deterministic JSON codec for M13-owned state and evidence persistence."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

_TYPE = "__nvda_type__"


def _encode(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("durable_decimal_must_be_finite")
        return {_TYPE: "decimal", "value": format(value, "f")}
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
            raise ValueError("durable_datetime_must_be_utc")
        return {_TYPE: "datetime", "value": value.isoformat().replace("+00:00", "Z")}
    if isinstance(value, tuple):
        return {_TYPE: "tuple", "items": [_encode(item) for item in value]}
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("durable_mapping_keys_must_be_strings")
        return {key: _encode(value[key]) for key in sorted(value)}
    raise TypeError(f"unsupported_durable_value_type:{type(value).__name__}")


def _decode(value: Any) -> Any:
    if isinstance(value, list):
        return [_decode(item) for item in value]
    if isinstance(value, dict):
        tag = value.get(_TYPE)
        if tag == "decimal" and set(value) == {_TYPE, "value"}:
            return Decimal(value["value"])
        if tag == "datetime" and set(value) == {_TYPE, "value"}:
            return datetime.fromisoformat(value["value"].replace("Z", "+00:00"))
        if tag == "tuple" and set(value) == {_TYPE, "items"}:
            return tuple(_decode(item) for item in value["items"])
        if tag is not None:
            raise ValueError("unknown_durable_type_tag")
        return {key: _decode(item) for key, item in value.items()}
    return value


def dumps_durable(value: Any) -> str:
    """Encode the supported state subset into canonical compact JSON."""

    return json.dumps(_encode(value), sort_keys=True, separators=(",", ":"))


def loads_durable(payload: str) -> Any:
    """Decode canonical durable JSON into detached Python values."""

    return _decode(json.loads(payload))


__all__ = ["dumps_durable", "loads_durable"]
