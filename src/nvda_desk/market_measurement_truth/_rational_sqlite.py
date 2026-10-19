"""Isolated immutable exact-ratio SQLite profile; no original store is migrated."""

from __future__ import annotations

import hashlib
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any

from . import api as f
from ._evaluation import timestamp
from ._rational import (
    NAMESPACE,
    _admission,
    _Memory,
    canonical,
    decode,
    expected_definition,
    expected_parameter,
    validate_occurrence,
)
from ._sqlite import _path

_DEF = "mmt_ratio_definition_v1"
_PARAM = "mmt_ratio_parameter_v1"
_OCC = "mmt_ratio_occurrence_v1"
_CONTENT = "payload BLOB NOT NULL, content_sha256 TEXT NOT NULL"
_DDL = (
    f"CREATE TABLE {_DEF} (owner_namespace TEXT NOT NULL, derived_signal_id TEXT NOT NULL, "
    f"calculation_definition_version TEXT NOT NULL, {_CONTENT}, "
    "PRIMARY KEY(owner_namespace,derived_signal_id,calculation_definition_version)) STRICT",
    f"CREATE TABLE {_PARAM} (owner_namespace TEXT NOT NULL, context_id TEXT NOT NULL, "
    f"version TEXT NOT NULL, {_CONTENT}, PRIMARY KEY(owner_namespace,context_id,version)) STRICT",
    f"CREATE TABLE {_OCC} (derived_occurrence_id TEXT NOT NULL PRIMARY KEY, "
    "owner_object_id TEXT NOT NULL, owner_namespace TEXT NOT NULL, "
    "implementation_brief_sha256 TEXT NOT NULL, derived_signal_id TEXT NOT NULL, "
    "calculation_definition_version TEXT NOT NULL, subject_instrument TEXT NOT NULL, "
    "effective_as_of_utc TEXT NOT NULL, knowledge_cutoff_utc TEXT NOT NULL, "
    f"logical_identity_payload BLOB NOT NULL, logical_identity_sha256 TEXT NOT NULL, {_CONTENT}, "
    "FOREIGN KEY(owner_namespace,derived_signal_id,calculation_definition_version) "
    f"REFERENCES {_DEF}(owner_namespace,derived_signal_id,calculation_definition_version)) STRICT",
    *(
        f"CREATE TRIGGER {table}_{action.lower()} BEFORE {action} ON {table} "
        "BEGIN SELECT RAISE(ABORT,'immutable exact-ratio record'); END"
        for table in (_DEF, _PARAM, _OCC)
        for action in ("UPDATE", "DELETE")
    ),
)
_SCHEMA = {statement.split()[2]: statement for statement in _DDL}


def _hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _schema(connection: sqlite3.Connection) -> None:
    if connection.execute("PRAGMA application_id").fetchone()[0] != 0x4E560003:
        raise f.PersistenceFailureV1("wrong exact-ratio file owner")
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise f.PersistenceFailureV1("unsupported exact-ratio schema version")
    actual = dict(
        connection.execute("SELECT name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%'")
    )
    if actual != _SCHEMA or connection.execute("PRAGMA foreign_key_check").fetchall():
        raise f.PersistenceFailureV1("exact-ratio schema/reference integrity failure")


def _connect(path: str, *, write: bool) -> sqlite3.Connection:
    _path(path)
    connection = sqlite3.connect(
        Path(path).as_uri() + ("?mode=rw" if write else "?mode=ro"),
        uri=True,
        isolation_level=None,
        timeout=0,
    )
    try:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=0")
        if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
            raise f.PersistenceFailureV1("exact-ratio journal policy mismatch")
        if write:
            connection.execute("PRAGMA synchronous=EXTRA")
        else:
            connection.execute("PRAGMA query_only=ON")
        expected = {"foreign_keys": 1, "journal_mode": "delete", "busy_timeout": 0}
        expected["synchronous" if write else "query_only"] = 3 if write else 1
        for name, value in expected.items():
            if connection.execute("PRAGMA " + name).fetchone()[0] != value:
                raise f.PersistenceFailureV1("exact-ratio connection policy mismatch")
        return connection
    except BaseException:
        connection.close()
        raise


@contextmanager
def _transaction(
    path: str,
    *,
    write: bool,
    initialise: bool = False,
) -> Iterator[sqlite3.Connection]:
    connection = None
    committing = False
    try:
        connection = _connect(path, write=write)
        connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        if not initialise:
            _schema(connection)
        yield connection
        committing = True
        connection.execute("COMMIT")
    except BaseException as exc:
        uncertain = bool(committing and connection is not None and not connection.in_transaction)
        if connection is not None and connection.in_transaction:
            try:
                connection.execute("ROLLBACK")
            except sqlite3.Error:
                uncertain = True
        if isinstance(
            exc,
            (sqlite3.Error, OSError, ValueError, TypeError, KeyError, ArithmeticError, MemoryError),
        ):
            raise f.PersistenceFailureV1(
                "exact-ratio SQLite operation failed",
                outcome_uncertain=uncertain,
            ) from exc
        raise
    finally:
        if connection is not None:
            connection.close()


def _definition_index(value: f.CalculationDefinitionV1) -> tuple[str, ...]:
    return NAMESPACE, value.derived_signal_id, value.calculation_definition_version


def _parameter_index(value: f.CalculationParameterSetV1) -> tuple[str, ...]:
    return NAMESPACE, value.context_id, str(value.version)


def _occurrence_index(value: f.RatioOccurrenceV1) -> tuple[str, ...]:
    return (
        value.derived_occurrence_id,
        value.owner_object_id,
        value.owner_namespace,
        value.implementation_brief_sha256,
        value.derived_signal_id,
        value.calculation_definition_version,
        value.subject_instrument,
        timestamp(value.effective_as_of_utc),
        timestamp(value.knowledge_cutoff_utc),
    )


def _insert(
    connection: sqlite3.Connection,
    table: str,
    index: tuple[str, ...],
    value: Any,
) -> None:
    names = {
        _DEF: ("owner_namespace", "derived_signal_id", "calculation_definition_version"),
        _PARAM: ("owner_namespace", "context_id", "version"),
    }[table]
    where = " AND ".join(name + "=?" for name in names)
    old = connection.execute(
        f"SELECT payload,content_sha256 FROM {table} WHERE {where}",
        index,
    ).fetchone()
    payload = canonical(value)
    if old is not None:
        if old != (payload, _hash(payload)):
            raise f.PersistenceFailureV1("immutable exact-ratio registration conflict")
        return
    values = (*index, payload, _hash(payload))
    connection.execute(f"INSERT INTO {table} VALUES ({','.join('?' for _ in values)})", values)


def _load(connection: sqlite3.Connection) -> _Memory:
    state = _Memory()
    for row in connection.execute(f"SELECT * FROM {_DEF}"):
        definition = decode(row[-2], f.CalculationDefinitionV1)
        if row[:-2] != _definition_index(definition) or row[-1] != _hash(row[-2]):
            raise ValueError("exact-ratio definition index/hash mismatch")
        if canonical(definition) != canonical(expected_definition(definition)):
            raise ValueError("unadmitted stored exact-ratio definition")
        state.definitions[
            (definition.derived_signal_id, definition.calculation_definition_version)
        ] = definition
    for row in connection.execute(f"SELECT * FROM {_PARAM}"):
        parameter = decode(row[-2], f.CalculationParameterSetV1)
        if row[:-2] != _parameter_index(parameter) or row[-1] != _hash(row[-2]):
            raise ValueError("exact-ratio parameter index/hash mismatch")
        if canonical(parameter) != canonical(expected_parameter(parameter)):
            raise ValueError("unadmitted stored exact-ratio parameter")
        state.parameters[(parameter.context_id, parameter.version)] = parameter
    for row in connection.execute(f"SELECT * FROM {_OCC}"):
        occurrence = decode(row[-2], f.RatioOccurrenceV1)
        if (
            row[:9] != _occurrence_index(occurrence)
            or row[10] != _hash(row[9])
            or row[-1] != _hash(row[-2])
        ):
            raise ValueError("exact-ratio occurrence index/hash mismatch")
        validate_occurrence(state, occurrence, row[9])
        state.occurrences[occurrence.derived_occurrence_id] = occurrence
        state.logical[occurrence.derived_occurrence_id] = row[9]
    return state


class _SQLiteState:
    def __init__(self, path: str, admission: f.OwnerAdmissionV1) -> None:
        _admission(admission)
        self.path = _path(path)

    def snapshot(self) -> _Memory:
        with _transaction(self.path, write=False) as connection:
            return _load(connection)

    @property
    def definitions(self) -> dict[tuple[str, str], f.CalculationDefinitionV1]:
        return self.snapshot().definitions

    @property
    def parameters(self) -> dict[tuple[str, int], f.CalculationParameterSetV1]:
        return self.snapshot().parameters

    @property
    def occurrences(self) -> dict[str, f.RatioOccurrenceV1]:
        return self.snapshot().occurrences

    def append(self, occurrence: f.RatioOccurrenceV1, logical: bytes) -> f.RatioOccurrenceV1:
        with _transaction(self.path, write=True) as connection:
            state = _load(connection)
            validate_occurrence(state, occurrence, logical)
            old = state.occurrences.get(occurrence.derived_occurrence_id)
            if old is not None:
                if state.logical[old.derived_occurrence_id] != logical or canonical(old) != (
                    canonical(replace(occurrence, calculated_at_utc=old.calculated_at_utc))
                ):
                    raise ValueError("immutable exact-ratio occurrence conflict")
                result = old
            else:
                payload = canonical(occurrence)
                values = (
                    *_occurrence_index(occurrence),
                    logical,
                    _hash(logical),
                    payload,
                    _hash(payload),
                )
                connection.execute(
                    f"INSERT INTO {_OCC} VALUES ({','.join('?' for _ in values)})",
                    values,
                )
                result = occurrence
        return result


def create_state(
    storage: f.SQLiteStorageV1,
    admission: f.OwnerAdmissionV1,
    registration: _Memory,
) -> _SQLiteState:
    state = _SQLiteState(storage.database_path, admission)
    if storage.create:
        try:
            descriptor = os.open(state.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(descriptor)
        except OSError as exc:
            raise f.PersistenceFailureV1("exact-ratio exclusive creation failed") from exc
        with _transaction(state.path, write=True, initialise=True) as connection:
            connection.execute("PRAGMA application_id=1314258947")
            connection.execute("PRAGMA user_version=1")
            for statement in _DDL:
                connection.execute(statement)
            _schema(connection)
    with _transaction(state.path, write=True) as connection:
        _load(connection)
        for definition in registration.definitions.values():
            _insert(connection, _DEF, _definition_index(definition), definition)
        for parameter in registration.parameters.values():
            _insert(connection, _PARAM, _parameter_index(parameter), parameter)
    return state
