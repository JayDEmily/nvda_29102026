"""Explicit versioned envelopes for new scalar straddle occurrences.

The legacy codecs and their registries remain unchanged. Only declared
scalar records are composed here; supported nested values retain the
existing lossless native representation.
"""

from __future__ import annotations

import hashlib
from typing import Any

from . import _native_codec as native
from . import api as f

_D091_TAG = "ScalarD091OccurrenceV1"
_REQUEST_KEYS = (
    "derived_signal_id", "subject_instrument", "as_of_utc", "knowledge_cutoff_utc",
    "calculation_definition_version", "source_profile_ref", "rule_profile_ref",
    "projection_mapping_ref", "unit_convention_ref", "core_manifest_sha256",
)
_OCCURRENCE_KEYS = (
    "owner_object_id", "owner_namespace", "implementation_brief_sha256",
    "derived_signal_id", "derived_occurrence_id", "request", "definition",
    "source_policy_sha256", "core_manifest_sha256", "original_observation",
    "selected_projection", "signed_delta", "result", "units", "result_shape",
    "effective_as_of_utc", "knowledge_cutoff_utc", "calculated_at_utc",
)


def _mapping(value: Any, keys: tuple[str, ...]) -> dict[str, Any]:
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError("unexpected scalar envelope fields")
    return value


def _request_content(request: f.ScalarD091RequestV1) -> dict[str, Any]:
    if type(request) is not f.ScalarD091RequestV1:
        raise TypeError("exact scalar D091 request required")
    return {key: getattr(request, key) for key in _REQUEST_KEYS}


def _content(value: f.ScalarD091OccurrenceV1) -> dict[str, Any]:
    if type(value) is not f.ScalarD091OccurrenceV1:
        raise TypeError("exact scalar D091 occurrence required")
    result = {key: getattr(value, key) for key in _OCCURRENCE_KEYS}
    result["request"] = _request_content(value.request)
    return result


def _envelope(content: dict[str, Any]) -> dict[str, Any]:
    return {"record": _D091_TAG, "version": 1, "content": content}


def encode_d091(value: f.ScalarD091OccurrenceV1) -> bytes:
    return native.canonical(_envelope(_content(value)))


def decode_d091(payload: bytes) -> f.ScalarD091OccurrenceV1:
    envelope = _mapping(native.decode(payload, dict), ("record", "version", "content"))
    if (
        type(envelope["record"]) is not str or envelope["record"] != _D091_TAG
        or type(envelope["version"]) is not int or envelope["version"] != 1
    ):
        raise ValueError("scalar D091 envelope identity/version mismatch")
    content = dict(_mapping(envelope["content"], _OCCURRENCE_KEYS))
    request = f.ScalarD091RequestV1(**_mapping(content["request"], _REQUEST_KEYS))
    content["request"] = request
    value = f.ScalarD091OccurrenceV1(**content)
    if encode_d091(value) != payload:
        raise ValueError("scalar D091 exact reconstructed bytes mismatch")
    return value


def identity_d091(value: f.ScalarD091OccurrenceV1) -> str:
    content = _content(value)
    del content["derived_occurrence_id"]
    del content["calculated_at_utc"]
    return "mmtd091scalar1:" + hashlib.sha256(
        native.canonical(_envelope(content)),
    ).hexdigest()
