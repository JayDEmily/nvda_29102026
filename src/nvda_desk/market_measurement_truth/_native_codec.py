"""Owner-local lossless codec for versioned native M02 records and public M00 DTOs."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import api as f

_IDENTITIES = {
    "RawSignalCatalogueId": raw.RawSignalCatalogueId,
    "observation_occurrence_id": raw.observation_occurrence_id,
    "ingestion_sequence_scope": raw.ingestion_sequence_scope,
    "concept_id": raw.concept_id,
    "contract_id": raw.contract_id,
    "delivery_artifact_ref": raw.delivery_artifact_ref,
    "provider_id": raw.provider_id,
}
_ID_TYPES = {
    type(factory("R001" if name == "RawSignalCatalogueId" else "id")): name
    for name, factory in _IDENTITIES.items()
}
_CLASSES = {
    cls.__name__: cls
    for cls in (
        raw.RawObservationOccurrenceV1,
        raw.ProjectedRawValueV1,
        raw.RawSelectionIdentityV1,
        raw.RawSignalProjectionMappingV1,
        f.VersionRefV1,
        f.AuthorityArtifactRefV1,
        f.CalculationDefinitionV1,
        f.NativeSourceProfileV1,
        f.NativeSourceRequestV1,
        f.NativeRawLineageV1,
        f.NativeControlLineageV1,
        f.NativeBookRowV1,
        f.NativeSourceSnapshotV1,
        f.NativeQuoteAssemblyV1,
        f.NativeCalculationRequestV1,
        f.NativeMeasurementOccurrenceV1,
        f.DerivedSignalOccurrenceV1,
        f.RawInputLineageV1,
        f.ExactRatioV1,
        f.BookSlopePairV1,
        f.BookRatePairV1,
        f.VenueConcentrationV1,
    )
}


def _tag(value: Any) -> Any:
    if type(value) in _ID_TYPES:
        return {"t": "identity", "n": _ID_TYPES[type(value)], "v": value.value}
    if value is None:
        return {"t": "none"}
    if type(value) is bool:
        return {"t": "bool", "v": value}
    if type(value) is int:
        return {"t": "int", "v": str(value)}
    if type(value) is str:
        return {"t": "str", "v": value}
    if type(value) is Decimal:
        sign, digits, exponent = value.as_tuple()
        return {"t": "decimal", "s": sign, "d": list(digits), "e": exponent}
    if type(value) is datetime:
        f._utc(value)
        return {"t": "datetime", "v": value.isoformat()}
    if type(value) is timedelta:
        return {
            "t": "duration",
            "v": (value.days * 86400 + value.seconds) * 1000000 + value.microseconds,
        }
    if type(value) is bytes:
        return {"t": "bytes", "v": value.hex()}
    if type(value) is float:
        return {"t": "float", "v": value.hex()}
    if type(value) in (tuple, list):
        return {"t": "tuple" if type(value) is tuple else "list", "v": [_tag(x) for x in value]}
    if isinstance(value, Mapping):
        if any(type(k) is not str for k in value):
            raise TypeError("native mappings require exact string keys")
        return {"t": "mapping", "v": {k: _tag(x) for k, x in value.items()}}
    if (
        is_dataclass(value)
        and type(value).__name__ in _CLASSES
        and _CLASSES[type(value).__name__] is type(value)
    ):
        return {
            "t": "record",
            "n": type(value).__name__,
            "v": {field.name: _tag(getattr(value, field.name)) for field in fields(value)},
        }
    raise TypeError("unadmitted native carrier")


def canonical(value: Any) -> bytes:
    return json.dumps(
        _tag(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("utf-8")


def _read(value: Any) -> Any:
    if type(value) is not dict or type(value.get("t")) is not str:
        raise ValueError("invalid native codec tag")
    kind = value["t"]
    if kind == "none" and set(value) == {"t"}:
        return None
    if kind == "identity" and set(value) == {"t", "n", "v"} and value["n"] in _IDENTITIES:
        return _IDENTITIES[value["n"]](value["v"])
    if kind in ("bool", "int", "str", "datetime", "duration", "bytes", "float") and set(value) == {
        "t",
        "v",
    }:
        raw_value = value["v"]
        if kind == "bool" and type(raw_value) is bool:
            return raw_value
        if kind == "int" and type(raw_value) is str:
            n = int(raw_value)
            if str(n) == raw_value:
                return n
        if kind == "str" and type(raw_value) is str:
            return raw_value
        if kind == "datetime" and type(raw_value) is str:
            dt = datetime.fromisoformat(raw_value)
            f._utc(dt)
            if dt.isoformat() == raw_value:
                return dt
        if kind == "duration" and type(raw_value) is int:
            return timedelta(microseconds=raw_value)
        if kind == "bytes" and type(raw_value) is str:
            return bytes.fromhex(raw_value)
        if kind == "float" and type(raw_value) is str:
            return float.fromhex(raw_value)
    if (
        kind == "decimal"
        and set(value) == {"t", "s", "d", "e"}
        and type(value["s"]) is int
        and value["s"] in (0, 1)
        and type(value["d"]) is list
        and value["d"]
        and all(type(x) is int and 0 <= x <= 9 for x in value["d"])
        and type(value["e"]) is int
    ):
        return Decimal((value["s"], tuple(value["d"]), value["e"]))
    if kind in ("tuple", "list") and set(value) == {"t", "v"} and type(value["v"]) is list:
        items = [_read(x) for x in value["v"]]
        return tuple(items) if kind == "tuple" else items
    if kind == "mapping" and set(value) == {"t", "v"} and type(value["v"]) is dict:
        return {k: _read(x) for k, x in value["v"].items()}
    if kind == "record" and set(value) == {"t", "n", "v"} and value["n"] in _CLASSES:
        cls = _CLASSES[value["n"]]
        content = value["v"]
        if type(content) is dict and set(content) == {field.name for field in fields(cls)}:
            return cls(**{k: _read(x) for k, x in content.items()})
    raise ValueError("invalid or unadmitted native representation")


def decode(payload: bytes, expected: type[Any]) -> Any:
    value = _read(json.loads(payload))
    if type(value) is not expected or canonical(value) != payload:
        raise ValueError("native readback type or canonical bytes mismatch")
    return value
