"""Separate foundation SQLite file, immutable transactions and typed recovery."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import NAMESPACE, _Configuration, _enabled, _expected, _key, _Memory
from ._evaluation import canonical, decode, digest, midpoint, spread, timestamp, untagged
from ._selection import eligible

_DEF = "mmt_definition_v1"
_CFG = "mmt_configuration_v1"
_OCC = "mmt_occurrence_v1"
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
        "BEGIN SELECT RAISE(ABORT,'immutable foundation record'); END"
        for table in (_DEF, _CFG, _OCC)
        for action in ("UPDATE", "DELETE")
    ),
)
_SCHEMA = {statement.split()[2]: statement for statement in _DDL}
_KINDS = {
    "parameter": f.CalculationParameterSetV1,
    "selection": f.InputSelectionPolicyVersionV1,
    "unit": f.UnitConventionVersionV1,
    "raw_mapping": raw_api.RawSignalProjectionMappingV1,
}


def _path(value: str) -> str:
    path = Path(value)
    if (
        not path.is_absolute()
        or value.startswith("file:")
        or "?" in value
        or "\x00" in value
        or path.is_symlink()
        or not path.parent.is_dir()
        or (path.exists() and not path.is_file())
    ):
        raise f.PersistenceFailureV1("foundation requires a local regular-file path")
    return str(path.resolve())


def _schema(c: sqlite3.Connection) -> None:
    if c.execute("PRAGMA application_id").fetchone()[0] != 0x4E560002:
        raise f.PersistenceFailureV1("wrong foundation file owner")
    if c.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise f.PersistenceFailureV1("unsupported foundation schema version")
    actual = dict(c.execute("SELECT name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%'"))
    if actual != _SCHEMA or c.execute("PRAGMA foreign_key_check").fetchall():
        raise f.PersistenceFailureV1("foundation schema or reference integrity failure")


def _connect(path: str, *, write: bool) -> sqlite3.Connection:
    _path(path)
    c = sqlite3.connect(
        Path(path).as_uri() + ("?mode=rw" if write else "?mode=ro"),
        uri=True,
        isolation_level=None,
        timeout=0,
    )
    try:
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA busy_timeout=0")
        if write:
            # Existing policy is validated before connection-local settings.
            if c.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
                raise f.PersistenceFailureV1("foundation journal policy mismatch")
            c.execute("PRAGMA synchronous=EXTRA")
        else:
            c.execute("PRAGMA query_only=ON")
        required = {"foreign_keys": 1, "journal_mode": "delete", "busy_timeout": 0}
        required["synchronous" if write else "query_only"] = 3 if write else 1
        for key, expected in required.items():
            if c.execute("PRAGMA " + key).fetchone()[0] != expected:
                raise f.PersistenceFailureV1("foundation connection policy mismatch")
        return c
    except BaseException:
        c.close()
        raise


@contextmanager
def _transaction(
    path: str, *, write: bool, initialise: bool = False
) -> Iterator[sqlite3.Connection]:
    c = None
    committing = False
    try:
        c = _connect(path, write=write)
        c.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        if not initialise:
            _schema(c)
        yield c
        committing = True
        c.execute("COMMIT")
    except BaseException as exc:
        uncertain = bool(committing and c is not None and not c.in_transaction)
        if c is not None and c.in_transaction:
            try:
                c.execute("ROLLBACK")
            except sqlite3.Error:
                uncertain = True
        if isinstance(
            exc, (sqlite3.Error, OSError, ValueError, TypeError, KeyError, OverflowError)
        ):
            raise f.PersistenceFailureV1(
                "foundation SQLite operation failed", outcome_uncertain=uncertain
            ) from exc
        raise
    finally:
        if c is not None:
            c.close()


def _hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _definition_index(value: f.CalculationDefinitionV1) -> tuple[str, ...]:
    return NAMESPACE, value.derived_signal_id, value.calculation_definition_version


def _configuration_index(value: Any) -> tuple[str, ...]:
    kind, identity, version = _key(value)
    return NAMESPACE, kind, identity, str(version)


def _occurrence_index(value: f.DerivedSignalOccurrenceV1) -> tuple[str, ...]:
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


def _insert(c: sqlite3.Connection, table: str, index: tuple[str, ...], value: Any) -> None:
    names = {
        _DEF: ("owner_namespace", "derived_signal_id", "calculation_definition_version"),
        _CFG: ("owner_namespace", "kind", "context_id", "version"),
    }[table]
    where = " AND ".join(name + "=?" for name in names)
    old = c.execute(f"SELECT payload,content_sha256 FROM {table} WHERE {where}", index).fetchone()
    payload = canonical(value)
    if old is not None:
        if old != (payload, _hash(payload)):
            raise f.PersistenceFailureV1("immutable registration conflict")
        return
    values = (*index, payload, _hash(payload))
    c.execute(f"INSERT INTO {table} VALUES ({','.join('?' for _ in values)})", values)


def _validate_occurrence(
    state: _Memory,
    occurrence: f.DerivedSignalOccurrenceV1,
    logical: bytes,
    admission: f.OwnerAdmissionV1,
) -> None:
    document = json.loads(logical)
    req = untagged(document["request"], f.CalculationRequestV1)
    definition = state.definitions[(req.derived_signal_id, req.calculation_definition_version)]
    parameter = state.configuration[
        ("parameter", req.parameter_set_ref.context_id, req.parameter_set_ref.version)
    ]
    policy = state.configuration[
        (
            "selection",
            req.input_selection_policy_ref.context_id,
            req.input_selection_policy_ref.version,
        )
    ]
    if type(policy) is not f.InputSelectionPolicyVersionV1:
        raise ValueError("selection reference mismatch")
    mappings = tuple(
        state.configuration[
            ("raw_mapping", b.projection_mapping_ref.context_id, b.projection_mapping_ref.version)
        ]
        for b in req.raw_input_bindings
    )
    units = {
        (b.unit_convention_ref.context_id, b.unit_convention_ref.version): state.configuration[
            ("unit", b.unit_convention_ref.context_id, b.unit_convention_ref.version)
        ]
        for b in req.raw_input_bindings
    }
    conventions = tuple(units[key] for key in sorted(units))
    if (
        not _enabled(req.derived_signal_id, admission)
        or req.subject_instrument != "NVDA"
        or req.context_refs
        or not req.as_of_utc <= req.knowledge_cutoff_utc <= occurrence.calculated_at_utc
        or tuple(b.raw_signal_id for b in req.raw_input_bindings) != ("R034", "R035")
        or len(occurrence.raw_input_lineage) != 2
    ):
        raise ValueError("invalid stored controlled request")
    for binding, mapping, lineage in zip(
        req.raw_input_bindings, mappings, occurrence.raw_input_lineage, strict=True
    ):
        if type(mapping) is not raw_api.RawSignalProjectionMappingV1:
            raise ValueError("raw mapping reference mismatch")
        when = eligible(lineage.projection, mapping, policy, req)
        if (
            when is None
            or when != lineage.event_time_utc
            or binding.raw_signal_id != lineage.raw_signal_id
            or binding.subject_instrument != "NVDA"
            or binding.projection_mapping_ref != lineage.projection_mapping_ref
            or binding.unit_convention_ref != lineage.unit_convention_ref
            or canonical(lineage.canonical_value) != canonical(lineage.projection.native_value)
        ):
            raise ValueError("stored lineage/reference mismatch")
    selected_lineage = occurrence.raw_input_lineage
    if (
        abs(selected_lineage[0].event_time_utc - selected_lineage[1].event_time_utc)
        > policy.maximum_skew
    ):
        raise ValueError("stored selected skew mismatch")
    expected_payload = dict(
        owner_object_id=admission.object_id,
        owner_namespace=NAMESPACE,
        implementation_brief_sha256=admission.implementation_brief_sha256,
        request=req,
        definition_content_sha256=digest(definition),
        parameter_set=parameter,
        input_selection_policy=policy,
        unit_conventions=conventions,
        projection_mappings=mappings,
        raw_input_lineage=selected_lineage,
    )
    if canonical(expected_payload) != logical:
        raise ValueError("logical identity/reference content mismatch")
    evaluate = spread if req.derived_signal_id == "D012" else midpoint
    result = evaluate(selected_lineage[0].canonical_value, selected_lineage[1].canonical_value)
    if result is None:
        raise ValueError("unrepresentable stored result")
    expected = f.DerivedSignalOccurrenceV1(
        admission.object_id,
        NAMESPACE,
        admission.implementation_brief_sha256,
        req.derived_signal_id,
        "mmt1:" + _hash(logical),
        definition.calculation_definition_version,
        digest(definition),
        (req.parameter_set_ref, req.input_selection_policy_ref),
        "NVDA",
        None,
        req.as_of_utc,
        None,
        req.knowledge_cutoff_utc,
        occurrence.calculated_at_utc,
        result,
        "price",
        "scalar_decimal",
        selected_lineage,
        (),
        tuple(f.VersionRefV1(key[0], key[1]) for key in sorted(units)),
        None,
    )
    if canonical(occurrence) != canonical(expected):
        raise ValueError("complete occurrence disagrees with its logical content")


def _load(c: sqlite3.Connection, admission: f.OwnerAdmissionV1) -> _Memory:
    state = _Memory()
    for row in c.execute(f"SELECT * FROM {_DEF}"):
        value = decode(row[-2], f.CalculationDefinitionV1)
        if row[:-2] != _definition_index(value) or row[-1] != _hash(row[-2]):
            raise ValueError("definition index/hash mismatch")
        if canonical(value) != canonical(_expected(value, admission)):
            raise ValueError("unsupported stored definition")
        state.definitions[(value.derived_signal_id, value.calculation_definition_version)] = value
    for row in c.execute(f"SELECT * FROM {_CFG}"):
        value = decode(row[-2], _KINDS[row[1]])
        if row[:-2] != _configuration_index(value) or row[-1] != _hash(row[-2]):
            raise ValueError("configuration index/hash mismatch")
        if canonical(value) != canonical(_expected(value, admission)):
            raise ValueError("unsupported stored configuration")
        state.configuration[_key(value)] = value
    for row in c.execute(f"SELECT * FROM {_OCC}"):
        value = decode(row[-2], f.DerivedSignalOccurrenceV1)
        if (
            row[:9] != _occurrence_index(value)
            or row[-1] != _hash(row[-2])
            or row[10] != _hash(row[9])
        ):
            raise ValueError("occurrence index/hash mismatch")
        _validate_occurrence(state, value, row[9], admission)
        state.occurrences[value.derived_occurrence_id] = value
        state.logical[value.derived_occurrence_id] = row[9]
    return state


class _SQLiteState:
    def __init__(self, path: str, admission: f.OwnerAdmissionV1) -> None:
        self.path, self.admission = _path(path), admission

    def snapshot(self) -> _Memory:
        with _transaction(self.path, write=False) as c:
            return _load(c, self.admission)

    @property
    def definitions(self) -> dict[tuple[str, str], f.CalculationDefinitionV1]:
        return self.snapshot().definitions

    @property
    def configuration(self) -> dict[tuple[str, str, int], _Configuration]:
        return self.snapshot().configuration

    @property
    def occurrences(self) -> dict[str, f.DerivedSignalOccurrenceV1]:
        return self.snapshot().occurrences

    def append(
        self, occurrence: f.DerivedSignalOccurrenceV1, payload: bytes
    ) -> f.DerivedSignalOccurrenceV1:
        with _transaction(self.path, write=True) as c:
            state = _load(c, self.admission)
            _validate_occurrence(state, occurrence, payload, self.admission)
            old = state.occurrences.get(occurrence.derived_occurrence_id)
            if old is not None:
                if state.logical[occurrence.derived_occurrence_id] != payload or canonical(
                    old
                ) != canonical(replace(occurrence, calculated_at_utc=old.calculated_at_utc)):
                    raise ValueError("immutable occurrence conflict")
                result = old
            else:
                values = (
                    *_occurrence_index(occurrence),
                    payload,
                    _hash(payload),
                    canonical(occurrence),
                    digest(occurrence),
                )
                c.execute(f"INSERT INTO {_OCC} VALUES ({','.join('?' for _ in values)})", values)
                result = occurrence
        return result


def create_state(
    storage: f.SQLiteStorageV1, admission: f.OwnerAdmissionV1, registration: _Memory
) -> _SQLiteState:
    state = _SQLiteState(storage.database_path, admission)
    if storage.create:
        try:
            fd = os.open(state.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
        except OSError as exc:
            raise f.PersistenceFailureV1("foundation exclusive creation failed") from exc
        with _transaction(state.path, write=True, initialise=True) as c:
            c.execute("PRAGMA application_id=1314258946")
            c.execute("PRAGMA user_version=1")
            for statement in _DDL:
                c.execute(statement)
            _schema(c)
    with _transaction(state.path, write=True) as c:
        _load(c, admission)
        for value in registration.definitions.values():
            _insert(c, _DEF, _definition_index(value), value)
        for configuration in registration.configuration.values():
            _insert(c, _CFG, _configuration_index(configuration), configuration)
    return state
