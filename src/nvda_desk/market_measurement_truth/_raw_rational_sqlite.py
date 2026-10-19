"""Isolated D014 exact-ratio SQLite profile, transactions and complete typed recovery."""

from __future__ import annotations

import hashlib
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import _Configuration, _key
from ._evaluation import timestamp
from ._rational import canonical, decode
from ._raw_rational import (
    NAMESPACE,
    _Memory,
    admission_check,
    expected_configuration,
    expected_definition,
    validate_occurrence,
)
from ._sqlite import _path

_APP_ID = 0x4E560004
_DEF = "mmt_raw_ratio_definition_v1"
_CFG = "mmt_raw_ratio_configuration_v1"
_OCC = "mmt_raw_ratio_occurrence_v1"
_CONTENT = "payload BLOB NOT NULL, content_sha256 TEXT NOT NULL"
_DDL = (
    f"CREATE TABLE {_DEF} (owner_namespace TEXT NOT NULL, derived_signal_id TEXT NOT NULL, "
    f"calculation_definition_version TEXT NOT NULL, {_CONTENT}, "
    "PRIMARY KEY(owner_namespace,derived_signal_id,calculation_definition_version)) STRICT",
    f"CREATE TABLE {_CFG} (owner_namespace TEXT NOT NULL, kind TEXT NOT NULL "
    "CHECK(kind IN ('parameter','selection','unit','raw_mapping')), context_id TEXT NOT NULL, "
    f"version TEXT NOT NULL, {_CONTENT}, "
    "PRIMARY KEY(owner_namespace,kind,context_id,version)) STRICT",
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
        "BEGIN SELECT RAISE(ABORT,'immutable raw-ratio record'); END"
        for table in (_DEF, _CFG, _OCC)
        for action in ("UPDATE", "DELETE")
    ),
)
_SCHEMA = {statement.split()[2]: statement for statement in _DDL}
_KINDS: dict[str, type[_Configuration]] = {
    "parameter": f.CalculationParameterSetV1,
    "selection": f.InputSelectionPolicyVersionV1,
    "unit": f.UnitConventionVersionV1,
    "raw_mapping": raw_api.RawSignalProjectionMappingV1,
}


def _hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _schema(connection: sqlite3.Connection) -> None:
    if connection.execute("PRAGMA application_id").fetchone()[0] != _APP_ID:
        raise f.PersistenceFailureV1("wrong raw-ratio file owner")
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise f.PersistenceFailureV1("unsupported raw-ratio schema version")
    actual = dict(
        connection.execute("SELECT name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%'")
    )
    if actual != _SCHEMA or connection.execute("PRAGMA foreign_key_check").fetchall():
        raise f.PersistenceFailureV1("raw-ratio declared schema or reference integrity failure")


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
        if write:
            if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
                raise f.PersistenceFailureV1("raw-ratio journal policy mismatch")
            connection.execute("PRAGMA synchronous=EXTRA")
        else:
            connection.execute("PRAGMA query_only=ON")
        required: dict[str, int | str] = {
            "foreign_keys": 1,
            "busy_timeout": 0,
            "journal_mode": "delete",
            "synchronous" if write else "query_only": 3 if write else 1,
        }
        for key, value in required.items():
            if connection.execute("PRAGMA " + key).fetchone()[0] != value:
                raise f.PersistenceFailureV1("raw-ratio connection policy mismatch")
        return connection
    except BaseException:
        connection.close()
        raise


@contextmanager
def _transaction(
    path: str, *, write: bool, initialise: bool = False
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
            exc, (sqlite3.Error, OSError, ValueError, TypeError, KeyError, OverflowError)
        ):
            raise f.PersistenceFailureV1(
                "raw-ratio SQLite operation failed", outcome_uncertain=uncertain
            ) from exc
        raise
    finally:
        if connection is not None:
            connection.close()


def _definition_index(value: f.CalculationDefinitionV1) -> tuple[str, ...]:
    return NAMESPACE, value.derived_signal_id, value.calculation_definition_version


def _configuration_index(value: _Configuration) -> tuple[str, ...]:
    kind, identity, version = _key(value)
    return NAMESPACE, kind, identity, str(version)


def _occurrence_index(value: f.RawRatioOccurrenceV1) -> tuple[str, ...]:
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
    value: f.CalculationDefinitionV1 | _Configuration,
) -> None:
    names = {
        _DEF: ("owner_namespace", "derived_signal_id", "calculation_definition_version"),
        _CFG: ("owner_namespace", "kind", "context_id", "version"),
    }[table]
    old = connection.execute(
        "SELECT payload,content_sha256 FROM "
        + table
        + " WHERE "
        + " AND ".join(name + "=?" for name in names),
        index,
    ).fetchone()
    payload = canonical(value)
    if old is not None:
        if old != (payload, _hash(payload)):
            raise ValueError("immutable raw-ratio registration conflict")
        return
    values = (*index, payload, _hash(payload))
    connection.execute(f"INSERT INTO {table} VALUES ({','.join('?' for _ in values)})", values)


def _load(connection: sqlite3.Connection) -> _Memory:
    state = _Memory()
    for row in connection.execute(f"SELECT * FROM {_DEF}"):
        definition = decode(row[-2], f.CalculationDefinitionV1)
        if row[:-2] != _definition_index(definition) or row[-1] != _hash(row[-2]):
            raise ValueError("raw-ratio definition index/content hash mismatch")
        if canonical(definition) != canonical(expected_definition(definition)):
            raise ValueError("unsupported stored raw-ratio definition")
        state.definitions[
            (definition.derived_signal_id, definition.calculation_definition_version)
        ] = definition
    for row in connection.execute(f"SELECT * FROM {_CFG}"):
        configuration = decode(row[-2], _KINDS[row[1]])
        if row[:-2] != _configuration_index(configuration) or row[-1] != _hash(row[-2]):
            raise ValueError("raw-ratio configuration index/content hash mismatch")
        if canonical(configuration) != canonical(expected_configuration(configuration)):
            raise ValueError("unsupported stored raw-ratio configuration")
        state.configuration[_key(configuration)] = configuration
    for row in connection.execute(f"SELECT * FROM {_OCC}"):
        occurrence = decode(row[-2], f.RawRatioOccurrenceV1)
        if (
            row[:9] != _occurrence_index(occurrence)
            or row[-1] != _hash(row[-2])
            or row[10] != _hash(row[9])
        ):
            raise ValueError("raw-ratio occurrence index/content/logical hash mismatch")
        validate_occurrence(state, occurrence, row[9])
        state.occurrences[occurrence.derived_occurrence_id] = occurrence
        state.logical[occurrence.derived_occurrence_id] = row[9]
    return state


class _SQLiteState:
    def __init__(self, path: str, admission: f.OwnerAdmissionV1) -> None:
        admission_check(admission)
        self.path, self.admission = _path(path), admission

    def snapshot(self) -> _Memory:
        with _transaction(self.path, write=False) as connection:
            return _load(connection)

    def append(self, occurrence: f.RawRatioOccurrenceV1, logical: bytes) -> f.RawRatioOccurrenceV1:
        with _transaction(self.path, write=True) as connection:
            state = _load(connection)
            validate_occurrence(state, occurrence, logical)
            old = state.occurrences.get(occurrence.derived_occurrence_id)
            if old is not None:
                if state.logical[old.derived_occurrence_id] != logical or canonical(
                    old
                ) != canonical(replace(occurrence, calculated_at_utc=old.calculated_at_utc)):
                    raise ValueError("immutable raw-ratio occurrence conflict")
                result = old
            else:
                values = (
                    *_occurrence_index(occurrence),
                    logical,
                    _hash(logical),
                    canonical(occurrence),
                    _hash(canonical(occurrence)),
                )
                connection.execute(
                    f"INSERT INTO {_OCC} VALUES ({','.join('?' for _ in values)})", values
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
            raise f.PersistenceFailureV1("raw-ratio exclusive creation failed") from exc
        with _transaction(state.path, write=True, initialise=True) as connection:
            connection.execute(f"PRAGMA application_id={_APP_ID}")
            connection.execute("PRAGMA user_version=1")
            for statement in _DDL:
                connection.execute(statement)
            _schema(connection)
    with _transaction(state.path, write=True) as connection:
        _load(connection)
        for definition in registration.definitions.values():
            _insert(connection, _DEF, _definition_index(definition), definition)
        for configuration in registration.configuration.values():
            _insert(connection, _CFG, _configuration_index(configuration), configuration)
    return state
