"""Frozen M00 public DTO adapter for the bounded M02 native compatibility proofs.

This reads selected actual M00 output bytes, not M00's fixture input or private
store. The pagination wrapper exposes the two already-public M00 methods.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "handoff/downstream_reconciliation/authority/fixtures/FROZEN_M00_PUBLIC_OUTPUT_V1.jsonl"


def instant(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def native(value):
    if type(value) is dict and set(value) == {"native_type", "value"}:
        kind, item = value["native_type"], value["value"]
        if kind == "NoneType":
            return None
        if kind == "int":
            return int(item)
        if kind == "Decimal":
            return Decimal(item)
        if kind == "datetime":
            return instant(item)
        if kind == "bool":
            return item == "True" if type(item) is str else item
        if kind == "str":
            return item
        raise ValueError("unadmitted frozen native value")
    if type(value) is dict:
        return {k: native(v) for k, v in value.items()}
    if type(value) is list:
        return [native(v) for v in value]
    return value


def observation(value: dict) -> raw.RawObservationOccurrenceV1:
    opaque = {
        "concept_id": raw.concept_id,
        "contract_id": raw.contract_id,
        "observation_occurrence_id": raw.observation_occurrence_id,
        "delivery_artifact_ref": raw.delivery_artifact_ref,
        "source_provider": raw.provider_id,
        "ingestion_sequence_scope": raw.ingestion_sequence_scope,
    }
    data = dict(value)
    for key, factory in opaque.items():
        data[key] = factory(data[key])
    for key in ("received_ts_utc",):
        data[key] = instant(data[key])
    if data.get("raw_signal_catalogue_ids") is not None:
        data["raw_signal_catalogue_ids"] = tuple(raw.RawSignalCatalogueId(x)
                                                  for x in data["raw_signal_catalogue_ids"])
    data["native_record"] = native(data["native_record"])
    return raw.RawObservationOccurrenceV1(**data)


def projection(value: dict) -> raw.ProjectedRawValueV1:
    data = dict(value)
    data["raw_signal_catalogue_id"] = raw.RawSignalCatalogueId(data["raw_signal_catalogue_id"])
    data["observation_occurrence_id"] = raw.observation_occurrence_id(data["observation_occurrence_id"])
    data["native_field_path"] = tuple(data["native_field_path"])
    data["native_value"] = native(data["native_value"])
    data["received_ts_utc"] = instant(data["received_ts_utc"])
    data["ingestion_sequence_scope"] = raw.ingestion_sequence_scope(data["ingestion_sequence_scope"])
    if data["selection_identity"] is not None:
        data["selection_identity"] = raw.RawSelectionIdentityV1(tuple(
            (key, native(item)) for key, item in data["selection_identity"].items()
        ))
    return raw.ProjectedRawValueV1(**data)


def at_path(value, path):
    for key in path:
        if not isinstance(value, Mapping) or key not in value:
            return None
        value = value[key]
    return value


class PublicDtoReader:
    """Exact public method signatures over frozen public DTOs, with page-size one."""

    def __init__(self, scenarios=("A2", "A3", "A4", "C1", "C2")):
        rows = [json.loads(x) for x in OUTPUT.read_text().splitlines()]
        self.observations = [observation(x["value"]) for x in rows if x["kind"] == "observation"
                             and x["scenario_id"] in scenarios]
        self.projections = [projection(x["value"]) for x in rows if x["kind"] == "projection"
                            and x["scenario_id"] in scenarios]
        self.event_filters = []
        self.control_queries = 0

    def list_projected_raw_history(self, raw_signal_catalogue_id, *, mappings,
            subject_instrument, received_at_or_before_utc,
            event_at_or_before_utc=None, limit, cursor):
        self.event_filters.append(event_at_or_before_utc)
        mapping = mappings[0]
        items = [x for x in self.projections if x.raw_signal_catalogue_id == raw_signal_catalogue_id
                 and x.projection_mapping_id == mapping.mapping_id
                 and x.projection_mapping_version == mapping.version
                 and x.subject_instrument == subject_instrument
                 and x.received_ts_utc <= received_at_or_before_utc]
        items.sort(key=lambda x: (x.received_ts_utc, x.ingestion_sequence,
                                  x.observation_occurrence_id.value))
        offset = int(cursor or "0")
        page = items[offset:offset+limit]
        return raw.ProjectedRawHistoryPageV1(tuple(page),
             str(offset+len(page)) if offset+len(page) < len(items) else None)

    def list_raw_observation_history(self, *, subject_instrument, source_provider,
            source_variant, received_at_or_before_utc, native_identity_selectors=(),
            limit, cursor):
        if any(path == ("_collector", "control", "generation_after")
               for path, _ in native_identity_selectors):
            self.control_queries += 1
        items = [x for x in self.observations
                 if x.subject_instrument == subject_instrument
                 and x.source_provider.value == source_provider
                 and x.source_variant == source_variant
                 and x.received_ts_utc <= received_at_or_before_utc
                 and all(at_path(x.native_record, path) == expected
                         for path, expected in native_identity_selectors)]
        items.sort(key=lambda x: (x.received_ts_utc, x.ingestion_sequence,
                                  x.observation_occurrence_id.value))
        offset = int(cursor or "0")
        page = items[offset:offset+limit]
        return raw.RawObservationHistoryPageV1(tuple(page),
             str(offset+len(page)) if offset+len(page) < len(items) else None)
