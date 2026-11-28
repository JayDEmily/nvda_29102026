"""Exact aligned-history envelopes, separate from the unchanged legacy codec."""

from __future__ import annotations

import hashlib
from dataclasses import fields
from typing import Any

from . import _native_codec as native
from . import api as f

_TAG = "AlignedHistoryOccurrenceV1"
_METADATA = {
    "parameter_set": f.CalculationParameterSetV1,
    "input_selection_policy": f.InputSelectionPolicyVersionV1,
    "window_context": f.WindowContextV1,
}


def _record(value: Any, cls: type[Any]) -> dict[str, Any]:
    if type(value) is not cls:
        raise TypeError("exact aligned history typed carrier required")
    return {field.name: getattr(value, field.name) for field in fields(cls)}


def _rebuild(value: Any, cls: type[Any]) -> Any:
    if type(value) is not dict or set(value) != {field.name for field in fields(cls)}:
        raise ValueError("aligned history record field set mismatch")
    return cls(**value)


def _content(value: f.AlignedHistoryOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.AlignedHistoryOccurrenceV1)
    content["request"] = _record(value.request, f.AlignedHistoryRequestV1)
    for name, cls in _METADATA.items():
        content[name] = _record(getattr(value, name), cls)
    content["unit_conventions"] = tuple(
        _record(unit, f.UnitConventionVersionV1) for unit in value.unit_conventions
    )
    if value.derived_signal_id in ("D076", "D077"):
        expected = (
            ("D072", "D071") if value.derived_signal_id == "D076" else ("D073", "D074", "D072")
        )
        if (
            tuple(parent.derived_signal_id for parent in value.predecessors) != expected
            or any(type(parent) is not f.AlignedHistoryOccurrenceV1 for parent in value.predecessors)
        ):
            raise ValueError(f"{value.derived_signal_id} exact ordered underlying envelopes required")
        # Complete canonical parent envelopes, retaining their identities and first times.
        content["predecessors"] = tuple(encode(parent) for parent in value.predecessors)
    elif value.predecessors != ():
        raise ValueError("underlying history cannot retain derived parents")
    return content


def _envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _TAG, "version": 1, "content": content})


def encode(value: f.AlignedHistoryOccurrenceV1) -> bytes:
    return _envelope(_content(value))


def identity(value: f.AlignedHistoryOccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtahistory1:" + hashlib.sha256(_envelope(content)).hexdigest()


def decode(payload: bytes) -> f.AlignedHistoryOccurrenceV1:
    return _decode(payload, allow_relative=True)


def _decode(payload: bytes, *, allow_relative: bool) -> f.AlignedHistoryOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("unadmitted aligned history envelope")
    content = envelope["content"]
    if (
        type(content) is not dict
        or set(content) != {field.name for field in fields(f.AlignedHistoryOccurrenceV1)}
        or type(content["unit_conventions"]) is not tuple
    ):
        raise ValueError("invalid aligned history content")
    if content["derived_signal_id"] in ("D076", "D077"):
        parents = content["predecessors"]
        count = 3 if content["derived_signal_id"] == "D077" else 2
        if (
            not allow_relative or type(parents) is not tuple or len(parents) != count
            or any(type(parent) is not bytes for parent in parents)
        ):
            raise ValueError("invalid relative history envelopes")
        content["predecessors"] = tuple(
            _decode(parent, allow_relative=False) for parent in parents
        )
    elif content["predecessors"] != ():
        raise ValueError("invalid underlying history content")
    content["request"] = _rebuild(content["request"], f.AlignedHistoryRequestV1)
    for name, cls in _METADATA.items():
        content[name] = _rebuild(content[name], cls)
    content["unit_conventions"] = tuple(
        _rebuild(unit, f.UnitConventionVersionV1) for unit in content["unit_conventions"]
    )
    value = f.AlignedHistoryOccurrenceV1(**content)
    if encode(value) != payload:
        raise ValueError("aligned history canonical round-trip mismatch")
    return value
