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
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _TAG
        or type(envelope["version"]) is not int
        or envelope["version"] != 1
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


_LOCAL_TAG = "OptionTimeLocalOccurrenceV1"


def local_datetime_facts(value: Any) -> dict[str, Any]:
    from datetime import UTC, datetime
    from zoneinfo import ZoneInfo

    if type(value) is not datetime or type(value.tzinfo) is not ZoneInfo:
        raise TypeError("exact D003 ZoneInfo datetime required")
    return {
        "iso": value.isoformat(),
        "iana": value.tzinfo.key,
        "fold": value.fold,
        "utc": value.astimezone(UTC).isoformat(),
    }


def _local_datetime(content: Any) -> Any:
    from datetime import datetime
    from zoneinfo import ZoneInfo

    if (
        type(content) is not dict or set(content) != {"iso", "iana", "fold", "utc"}
        or type(content["iso"]) is not str or type(content["utc"]) is not str
        or content["iana"] != "America/New_York"
        or type(content["fold"]) is not int or content["fold"] not in (0, 1)
    ):
        raise ValueError("unadmitted D003 local result representation")
    utc = datetime.fromisoformat(content["utc"])
    f._utc(utc)
    value = utc.astimezone(ZoneInfo(content["iana"]))
    if local_datetime_facts(value) != content:
        raise ValueError("D003 local key/fold/offset/UTC mismatch")
    return value


def _local_content(value: f.OptionTimeLocalOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.OptionTimeLocalOccurrenceV1)
    content["request"] = _record(value.request, f.OptionTimeRequestV1)
    content["predecessor"] = _content(value.predecessor)
    content["result"] = local_datetime_facts(value.result)
    return content


def _local_envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _LOCAL_TAG, "version": 1, "content": content})


def encode_local(value: f.OptionTimeLocalOccurrenceV1) -> bytes:
    return _local_envelope(_local_content(value))


def local_identity(value: f.OptionTimeLocalOccurrenceV1) -> str:
    content = _local_content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtoptiontimelocal1:" + hashlib.sha256(_local_envelope(content)).hexdigest()


def decode_local(payload: bytes) -> f.OptionTimeLocalOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _LOCAL_TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("unadmitted D003 option-time envelope")
    content = envelope["content"]
    if type(content) is not dict or set(content) != {
        field.name for field in fields(f.OptionTimeLocalOccurrenceV1)
    }:
        raise ValueError("D003 option-time field set mismatch")
    content["request"] = _rebuild(content["request"], f.OptionTimeRequestV1)
    content["predecessor"] = decode(_envelope(content["predecessor"]))
    content["result"] = _local_datetime(content["result"])
    value = _rebuild(content, f.OptionTimeLocalOccurrenceV1)
    if encode_local(value) != payload:
        raise ValueError("D003 canonical readback mismatch")
    return value


_EXPIRY_TAG = "OptionTimeExpiryOccurrenceV1"


def _expiry_content(value: f.OptionTimeExpiryOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.OptionTimeExpiryOccurrenceV1)
    content["request"] = _record(value.request, f.OptionTimeRequestV1)
    content["predecessor"] = _content(value.predecessor)
    content["result"] = _record(value.result, f.ExactRatioV1)
    return content


def _expiry_envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _EXPIRY_TAG, "version": 1, "content": content})


def encode_expiry(value: f.OptionTimeExpiryOccurrenceV1) -> bytes:
    return _expiry_envelope(_expiry_content(value))


def expiry_identity(value: f.OptionTimeExpiryOccurrenceV1) -> str:
    content = _expiry_content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtoptiontimeexpiry1:" + hashlib.sha256(_expiry_envelope(content)).hexdigest()


def decode_expiry(payload: bytes) -> f.OptionTimeExpiryOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _EXPIRY_TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("unadmitted D086 option-time envelope")
    content = envelope["content"]
    if type(content) is not dict or set(content) != {
        field.name for field in fields(f.OptionTimeExpiryOccurrenceV1)
    }:
        raise ValueError("D086 option-time field set mismatch")
    content["request"] = _rebuild(content["request"], f.OptionTimeRequestV1)
    content["predecessor"] = decode(_envelope(content["predecessor"]))
    content["result"] = _rebuild(content["result"], f.ExactRatioV1)
    value = _rebuild(content, f.OptionTimeExpiryOccurrenceV1)
    if encode_expiry(value) != payload:
        raise ValueError("D086 canonical readback mismatch")
    return value


_SESSION_TAG = "OptionTimeSessionOccurrenceV1"


def _date_facts(value: Any) -> dict[str, str]:
    from datetime import date

    if type(value) is not date:
        raise TypeError("exact D004 date required")
    return {"type": "date", "iso": value.isoformat()}


def _session_date(content: Any) -> Any:
    from datetime import date

    if (
        type(content) is not dict or set(content) != {"type", "iso"}
        or content["type"] != "date" or type(content["iso"]) is not str
    ):
        raise ValueError("unadmitted D004 date representation")
    value = date.fromisoformat(content["iso"])
    if _date_facts(value) != content:
        raise ValueError("D004 date canonical representation mismatch")
    return value


def _session_content(value: f.OptionTimeSessionOccurrenceV1) -> dict[str, Any]:
    content = _record(value, f.OptionTimeSessionOccurrenceV1)
    content["request"] = _record(value.request, f.OptionTimeRequestV1)
    content["predecessor"] = _local_content(value.predecessor)
    content["result"] = _date_facts(value.result)
    return content


def _session_envelope(content: dict[str, Any]) -> bytes:
    return native.canonical({"record": _SESSION_TAG, "version": 1, "content": content})


def encode_session(value: f.OptionTimeSessionOccurrenceV1) -> bytes:
    return _session_envelope(_session_content(value))


def session_identity(value: f.OptionTimeSessionOccurrenceV1) -> str:
    content = _session_content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtoptiontimesession1:" + hashlib.sha256(_session_envelope(content)).hexdigest()


def decode_session(payload: bytes) -> f.OptionTimeSessionOccurrenceV1:
    envelope = native.decode(payload, dict)
    if (
        set(envelope) != {"record", "version", "content"}
        or envelope["record"] != _SESSION_TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("unadmitted D004 option-time envelope")
    content = envelope["content"]
    if type(content) is not dict or set(content) != {
        field.name for field in fields(f.OptionTimeSessionOccurrenceV1)
    }:
        raise ValueError("D004 option-time field set mismatch")
    content["request"] = _rebuild(content["request"], f.OptionTimeRequestV1)
    content["predecessor"] = decode_local(_local_envelope(content["predecessor"]))
    content["result"] = _session_date(content["result"])
    value = _rebuild(content, f.OptionTimeSessionOccurrenceV1)
    if encode_session(value) != payload:
        raise ValueError("D004 canonical readback mismatch")
    return value
