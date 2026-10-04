"""Private PostgreSQL mechanism for Derived Signal occurrence persistence."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from typing import Any

from .api import (
    DerivedSignalOccurrenceV1,
    RawInputLineageV1,
    VersionRefV1,
)

_TABLE = "dsct_derived_signal_occurrence_v1"


def _psycopg() -> Any:
    import psycopg

    return psycopg


def _encode_value(value: object) -> object:
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is Decimal:
        return {"__kind__": "decimal", "value": str(value)}
    if type(value) is datetime:
        return {"__kind__": "datetime", "value": value.isoformat()}
    if type(value) is tuple:
        return {"__kind__": "tuple", "items": [_encode_value(item) for item in value]}
    raise TypeError("derived result contains an unsupported value")


def _decode_value(value: object) -> object:
    if not isinstance(value, dict) or "__kind__" not in value:
        return value
    kind = value["__kind__"]
    if kind == "decimal":
        return Decimal(str(value["value"]))
    if kind == "datetime":
        return datetime.fromisoformat(str(value["value"]))
    if kind == "tuple":
        items = value.get("items")
        if not isinstance(items, list):
            raise ValueError("invalid tuple encoding")
        return tuple(_decode_value(item) for item in items)
    raise ValueError("unknown persisted result encoding")


def _version_refs(value: tuple[VersionRefV1, ...]) -> str:
    return json.dumps([{"context_id": item.context_id, "version": item.version} for item in value])


def _raw_lineage(value: tuple[RawInputLineageV1, ...]) -> str:
    return json.dumps(
        [
            {
                "raw_signal_id": item.raw_signal_id,
                "observation_occurrence_id": item.observation_occurrence_id,
                "projection_mapping_id": item.projection_mapping_id,
                "projection_mapping_version": item.projection_mapping_version,
                "unit_convention_id": item.unit_convention_id,
                "unit_convention_version": item.unit_convention_version,
                "native_units": item.native_units,
                "canonical_units": item.canonical_units,
            }
            for item in value
        ]
    )


def _decode_refs(value: object) -> tuple[VersionRefV1, ...]:
    rows = value if isinstance(value, list) else json.loads(str(value))
    return tuple(
        VersionRefV1(context_id=str(row["context_id"]), version=int(row["version"]))
        for row in rows
    )


def _decode_raw_lineage(value: object) -> tuple[RawInputLineageV1, ...]:
    rows = value if isinstance(value, list) else json.loads(str(value))
    return tuple(
        RawInputLineageV1(
            raw_signal_id=str(row["raw_signal_id"]),
            observation_occurrence_id=str(row["observation_occurrence_id"]),
            projection_mapping_id=str(row["projection_mapping_id"]),
            projection_mapping_version=int(row["projection_mapping_version"]),
            unit_convention_id=str(row["unit_convention_id"]),
            unit_convention_version=int(row["unit_convention_version"]),
            native_units=str(row["native_units"]),
            canonical_units=str(row["canonical_units"]),
        )
        for row in rows
    )


class _PostgresPersistenceV1:
    __slots__ = ("_dsn",)

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def append_occurrence(self, value: DerivedSignalOccurrenceV1) -> DerivedSignalOccurrenceV1:
        psycopg = _psycopg()
        payload = json.dumps(_encode_value(value.result))
        with psycopg.connect(self._dsn) as connection:
            existing = self.get_occurrence(value.derived_occurrence_id)
            if existing is not None:
                if existing != value:
                    raise ValueError("derived occurrence identity already has different content")
                return existing
            connection.execute(
                f"""
                INSERT INTO {_TABLE} (
                    derived_occurrence_id, derived_signal_id, calculation_definition_version,
                    parameter_context_refs, subject_instrument, universe, effective_as_of_utc,
                    window_value, knowledge_cutoff_utc, calculated_at_utc, result_value, units,
                    result_shape, raw_input_lineage, predecessor_occurrence_ids, convention_refs,
                    supersedes_derived_occurrence_id
                ) VALUES (
                    %s, %s, %s, %s::jsonb, %s, %s::jsonb, %s, %s, %s, %s, %s::jsonb, %s,
                    %s, %s::jsonb, %s::jsonb, %s::jsonb, %s
                )
                """,
                (
                    value.derived_occurrence_id,
                    value.derived_signal_id,
                    value.calculation_definition_version,
                    _version_refs(value.parameter_context_refs),
                    value.subject_instrument,
                    json.dumps(value.universe),
                    value.effective_as_of_utc,
                    value.window,
                    value.knowledge_cutoff_utc,
                    value.calculated_at_utc,
                    payload,
                    value.units,
                    value.result_shape,
                    _raw_lineage(value.raw_input_lineage),
                    json.dumps(value.predecessor_occurrence_ids),
                    _version_refs(value.convention_refs),
                    value.supersedes_derived_occurrence_id,
                ),
            )
        return value

    def _from_row(self, row: tuple[object, ...]) -> DerivedSignalOccurrenceV1:
        universe_raw = row[5]
        universe_list = (
            universe_raw
            if isinstance(universe_raw, list)
            else json.loads(str(universe_raw))
        )
        predecessor_raw = row[14]
        predecessor_list = (
            predecessor_raw
            if isinstance(predecessor_raw, list)
            else json.loads(str(predecessor_raw))
        )
        result_raw = row[10]
        if isinstance(result_raw, str):
            result_raw = json.loads(result_raw)
        return DerivedSignalOccurrenceV1(
            derived_occurrence_id=str(row[0]),
            derived_signal_id=str(row[1]),
            calculation_definition_version=str(row[2]),
            parameter_context_refs=_decode_refs(row[3]),
            subject_instrument=str(row[4]),
            universe=None if universe_list is None else tuple(str(item) for item in universe_list),
            effective_as_of_utc=row[6],  # type: ignore[arg-type]
            window=None if row[7] is None else str(row[7]),
            knowledge_cutoff_utc=row[8],  # type: ignore[arg-type]
            calculated_at_utc=row[9],  # type: ignore[arg-type]
            result=_decode_value(result_raw),  # type: ignore[arg-type]
            units=str(row[11]),
            result_shape=str(row[12]),
            raw_input_lineage=_decode_raw_lineage(row[13]),
            predecessor_occurrence_ids=tuple(str(item) for item in predecessor_list),
            convention_refs=_decode_refs(row[15]),
            supersedes_derived_occurrence_id=None if row[16] is None else str(row[16]),
        )

    def get_occurrence(self, derived_occurrence_id: str) -> DerivedSignalOccurrenceV1 | None:
        psycopg = _psycopg()
        with psycopg.connect(self._dsn) as connection:
            row = connection.execute(
                f"""
                SELECT derived_occurrence_id, derived_signal_id, calculation_definition_version,
                       parameter_context_refs, subject_instrument, universe, effective_as_of_utc,
                       window_value, knowledge_cutoff_utc, calculated_at_utc, result_value, units,
                       result_shape, raw_input_lineage, predecessor_occurrence_ids, convention_refs,
                       supersedes_derived_occurrence_id
                FROM {_TABLE}
                WHERE derived_occurrence_id = %s
                """,
                (derived_occurrence_id,),
            ).fetchone()
        return None if row is None else self._from_row(row)

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit must be a positive integer")
        psycopg = _psycopg()
        with psycopg.connect(self._dsn) as connection:
            rows = connection.execute(
                f"""
                SELECT derived_occurrence_id, derived_signal_id, calculation_definition_version,
                       parameter_context_refs, subject_instrument, universe, effective_as_of_utc,
                       window_value, knowledge_cutoff_utc, calculated_at_utc, result_value, units,
                       result_shape, raw_input_lineage, predecessor_occurrence_ids, convention_refs,
                       supersedes_derived_occurrence_id
                FROM {_TABLE}
                WHERE derived_signal_id = %s AND subject_instrument = %s
                ORDER BY effective_as_of_utc, derived_occurrence_id
                LIMIT %s
                """,
                (derived_signal_id, subject_instrument, limit),
            ).fetchall()
        return tuple(self._from_row(row) for row in rows)


def create_postgres_persistence(dsn: str) -> _PostgresPersistenceV1:
    if type(dsn) is not str or not dsn:
        raise ValueError("dsn must be a non-empty string")
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        schema_row = connection.execute("SELECT current_schema()").fetchone()
        if schema_row is None or schema_row[0] is None:
            raise ValueError("PostgreSQL connection must resolve one current schema")
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE} (
                derived_occurrence_id TEXT PRIMARY KEY,
                derived_signal_id TEXT NOT NULL,
                calculation_definition_version TEXT NOT NULL,
                parameter_context_refs JSONB NOT NULL,
                subject_instrument TEXT NOT NULL,
                universe JSONB,
                effective_as_of_utc TIMESTAMPTZ NOT NULL,
                window_value TEXT,
                knowledge_cutoff_utc TIMESTAMPTZ NOT NULL,
                calculated_at_utc TIMESTAMPTZ NOT NULL,
                result_value JSONB NOT NULL,
                units TEXT NOT NULL,
                result_shape TEXT NOT NULL,
                raw_input_lineage JSONB NOT NULL,
                predecessor_occurrence_ids JSONB NOT NULL,
                convention_refs JSONB NOT NULL,
                supersedes_derived_occurrence_id TEXT
            )
            """
        )
    return _PostgresPersistenceV1(dsn)


__all__ = ["create_postgres_persistence"]
