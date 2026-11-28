"""Bounded lossless option-time envelope; unchanged legacy native codec."""

from __future__ import annotations

import hashlib
from dataclasses import fields
from typing import Any

from . import _native_codec as native
from . import api as f

_TAG = "OptionTimeOccurrenceV1"


def _record(value: Any, cls: type[Any]) -> dict[str, Any]:
    if type(value) is not cls:
        raise TypeError("exact option-time carrier required")
    return {field.name: getattr(value, field.name) for field in fields(cls)}


def _rebuild(content: Any, cls: type[Any]) -> Any:
    if type(content) is not dict or set(content) != {field.name for field in fields(cls)}:
        raise ValueError("option-time field set mismatch")
    return cls(**content)


def _content(value: f.OptionTimeOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.OptionTimeOccurrenceV1)
    content["request"] = _record(value.request, f.OptionTimeRequestV1)
    return content


def _envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _TAG, "version": 1, "content": content})


def encode(value: f.OptionTimeOccurrenceV1) -> bytes:
    return _envelope(_content(value))


def identity(value: f.OptionTimeOccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtoptiontime1:" + hashlib.sha256(_envelope(content)).hexdigest()


def decode(payload: bytes) -> f.OptionTimeOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"} or envelope["record"] != _TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("unadmitted option-time envelope")
    content = envelope["content"]
    if type(content) is not dict:
        raise ValueError("option-time content must be a mapping")
    content["request"] = _rebuild(content["request"], f.OptionTimeRequestV1)
    value = _rebuild(content, f.OptionTimeOccurrenceV1)
    if encode(value) != payload:
        raise ValueError("option-time canonical readback mismatch")
    return value
