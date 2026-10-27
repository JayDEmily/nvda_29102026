"""Typed fixture transport and actual public M00 reads; contains no expected answers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import fields
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "handoff/m00_brief2"
META = ("fixture_id", "fixture_version", "family", "scenario_id", "mapping_group")


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def inputs() -> list[dict[str, Any]]:
    return [
        row
        for family in ("A", "B", "C")
        for row in jsonl(ART / f"fixtures/{family}/synthetic_input_v1.jsonl")
    ]


def expected() -> list[dict[str, Any]]:
    return [
        row
        for family in ("A", "B", "C")
        for row in jsonl(ART / f"fixtures/{family}/expected_m00_output_v1.jsonl")
    ]


def utc(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() != UTC.utcoffset(result):
        raise ValueError("UTC datetime required")
    return result


def stamp(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def decode(value: Any) -> Any:
    if not isinstance(value, dict):
        raise TypeError("native fixture requires exact tags")
    if "native_type" not in value:
        return {key: decode(item) for key, item in value.items()}
    tag, data = value["native_type"], value["value"]
    if tag == "Decimal":
        return Decimal(data)
    if tag == "datetime":
        return utc(data)
    if tag == "int":
        return int(data)
    if tag == "bool" and type(data) is bool:
        return data
    if tag == "str" and type(data) is str:
        return data
    if tag == "NoneType" and data is None:
        return None
    raise ValueError("unsupported or malformed native tag")


def encode(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: encode(item) for key, item in value.items()}
    if type(value) is datetime:
        return {"native_type": "datetime", "value": stamp(value)}
    if type(value) is Decimal:
        return {"native_type": "Decimal", "value": str(value)}
    if type(value) is int:
        return {"native_type": "int", "value": str(value)}
    if value is None or type(value) in (str, bool):
        return {"native_type": type(value).__name__, "value": value}
    raise TypeError(f"unsupported output native type:{type(value).__name__}")


def observation(row: dict[str, Any]) -> r.RawObservationOccurrenceV1:
    data = dict(row["observation"])
    for field in (
        "concept_id",
        "contract_id",
        "observation_occurrence_id",
        "delivery_artifact_ref",
        "source_provider",
        "ingestion_sequence_scope",
    ):
        factory = r.provider_id if field == "source_provider" else getattr(r, field)
        data[field] = factory(data[field])
    data["native_record"] = decode(data["native_record"])
    data["received_ts_utc"] = utc(data["received_ts_utc"])
    ids = data["raw_signal_catalogue_ids"]
    data["raw_signal_catalogue_ids"] = (
        tuple(r.RawSignalCatalogueId(item) for item in ids) if ids is not None else None
    )
    return r.RawObservationOccurrenceV1(**data)


def mapping_group(group: str) -> dict[str, r.RawSignalProjectionMappingV1]:
    groups = json.loads((ART / "mapping_manifest_v1.json").read_text())["groups"]
    result = {}
    for raw_id, entry in groups[group].items():
        data = dict(entry)
        data["raw_signal_catalogue_id"] = r.RawSignalCatalogueId(raw_id)
        data["native_field_path"] = tuple(data["native_field_path"])
        data["selection_identity_field_paths"] = tuple(
            (key, tuple(path)) for key, path in data["selection_identity_field_paths"]
        )
        result[raw_id] = r.RawSignalProjectionMappingV1(**data)
    return result


def owner(path: Path, *, create: bool = False):
    return r.create_owner(durability_port=create_sqlite_persistence(str(path), create=create))


def dump_observation(value: r.RawObservationOccurrenceV1) -> dict[str, Any]:
    result = {}
    for field in fields(value):
        item = getattr(value, field.name)
        if field.name == "native_record":
            item = encode(item)
        elif field.name == "received_ts_utc":
            item = stamp(item)
        elif field.name == "raw_signal_catalogue_ids":
            item = [x.value for x in item] if item is not None else None
        elif hasattr(item, "value"):
            item = item.value
        result[field.name] = item
    return result


def dump_projection(value: r.ProjectedRawValueV1) -> dict[str, Any]:
    result = {}
    for field in fields(value):
        item = getattr(value, field.name)
        if field.name == "native_value":
            item = encode(item)
        elif field.name == "selection_identity":
            item = dict(item.values) if item is not None else None
        elif field.name == "received_ts_utc":
            item = stamp(item)
        elif field.name == "native_field_path":
            item = list(item)
        elif hasattr(item, "value"):
            item = item.value
        result[field.name] = item
    return result


def row(meta: dict[str, Any], kind: str, value: dict[str, Any]) -> dict[str, Any]:
    return {"kind": kind, **{key: meta[key] for key in META}, "value": value}


def canonical(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))


def read_rows(raw, queries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for query in queries:
        value = raw.reads.get_raw_observation_occurrence(r.observation_occurrence_id(query["id"]))
        if value is None:
            raise ValueError("missing persisted observation")
        result.append(row(query, "observation", dump_observation(value)))
        maps = mapping_group(query["mapping_group"])
        for raw_id, mapping in sorted(maps.items()):
            projection = raw.reads.project_raw_value(
                r.RawSignalCatalogueId(raw_id), value.observation_occurrence_id, mappings=(mapping,)
            )
            if projection is not None:
                result.append(row(query, "projection", dump_projection(projection)))
    return canonical(result)


def queries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {**{key: item[key] for key in META}, "id": item["observation"]["observation_occurrence_id"]}
        for item in rows
    ]


def fresh_rows(path: Path, query: list[dict[str, Any]]) -> list[dict[str, Any]]:
    code = """
import json, sys
from pathlib import Path
from m00_fixture_io import owner, read_rows
print(json.dumps(read_rows(owner(Path(sys.argv[1])), json.loads(sys.argv[2])), sort_keys=True))
"""
    env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(ROOT / "tools"), str(ROOT / "src"))))
    completed = subprocess.run(
        [sys.executable, "-c", code, str(path), json.dumps(query)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return json.loads(completed.stdout)
