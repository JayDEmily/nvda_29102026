"""Owner-local nonsemantic SQLite translation of already decided M00 records."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from . import api
from ._native_codec import _decode_native_record, _encode_native_record

_POLICY = "rsot_capture_scope_policy_v1"
_CAPTURE = "rsot_scheduled_capture_occurrence_v1"
_OBSERVATION = "rsot_raw_observation_occurrence_v1"
_ASSESSMENT = "rsot_capture_receipt_presence_assessment_v1"
_APP_ID = 0x4E560001
_CONTENT = "payload BLOB NOT NULL, content_sha256 TEXT NOT NULL"

_SCHEMA = (
    f"CREATE TABLE {_POLICY} (scope_policy_id TEXT NOT NULL, "
    "scope_policy_version TEXT NOT NULL, scope_policy_ref TEXT NOT NULL UNIQUE, "
    "activation_ts_utc TEXT NOT NULL, deactivation_ts_utc TEXT, "
    f"eligibility_policy_ref TEXT NOT NULL, {_CONTENT}, "
    "PRIMARY KEY(scope_policy_id,scope_policy_version), "
    "CHECK(deactivation_ts_utc IS NULL OR deactivation_ts_utc > activation_ts_utc)) STRICT",
    f"CREATE TABLE {_CAPTURE} (capture_occurrence_id TEXT NOT NULL PRIMARY KEY, "
    f"scope_policy_ref TEXT NOT NULL REFERENCES {_POLICY}(scope_policy_ref), "
    f"slot_start_utc TEXT NOT NULL, slot_end_utc TEXT NOT NULL, {_CONTENT}, "
    "UNIQUE(scope_policy_ref,slot_start_utc)) STRICT",
    f"CREATE TABLE {_OBSERVATION} (observation_occurrence_id TEXT NOT NULL PRIMARY KEY, "
    "received_ts_utc TEXT NOT NULL, ingestion_sequence_scope TEXT NOT NULL, "
    f"ingestion_sequence TEXT NOT NULL, ingestion_sort_key BLOB NOT NULL, {_CONTENT}) STRICT",
    f"CREATE TABLE {_ASSESSMENT} (assessment_occurrence_id TEXT NOT NULL PRIMARY KEY, "
    f"capture_occurrence_ref TEXT NOT NULL REFERENCES {_CAPTURE}(capture_occurrence_id), "
    "outcome TEXT NOT NULL CHECK(outcome IN "
    "('unknown_not_established','zero_received','one_or_more_received')), "
    "evidence_as_of_ts_utc TEXT NOT NULL, supersedes_assessment_ref TEXT UNIQUE "
    f"REFERENCES {_ASSESSMENT}(assessment_occurrence_id), {_CONTENT}) STRICT",
    f"CREATE UNIQUE INDEX rsot_assessment_one_root_per_capture_v1 ON {_ASSESSMENT}"
    "(capture_occurrence_ref) WHERE supersedes_assessment_ref IS NULL",
)
_TABLE_TYPES: dict[str, type[Any]] = {
    _POLICY: api.CaptureScopePolicyV1,
    _CAPTURE: api.ScheduledCaptureOccurrenceV1,
    _OBSERVATION: api.RawObservationOccurrenceV1,
    _ASSESSMENT: api.CaptureReceiptPresenceAssessmentV1,
}
_COLUMNS = {
    _POLICY: (
        "scope_policy_id",
        "scope_policy_version",
        "scope_policy_ref",
        "activation_ts_utc",
        "deactivation_ts_utc",
        "eligibility_policy_ref",
    ),
    _CAPTURE: ("capture_occurrence_id", "scope_policy_ref", "slot_start_utc", "slot_end_utc"),
    _OBSERVATION: (
        "observation_occurrence_id",
        "received_ts_utc",
        "ingestion_sequence_scope",
        "ingestion_sequence",
        "ingestion_sort_key",
    ),
    _ASSESSMENT: (
        "assessment_occurrence_id",
        "capture_occurrence_ref",
        "outcome",
        "evidence_as_of_ts_utc",
        "supersedes_assessment_ref",
    ),
}
_FACTORIES: dict[str, Callable[[str], api._OpaqueIdentity]] = {
    name: getattr(api, name)
    for name in (
        "concept_id",
        "contract_id",
        "scope_policy_id",
        "scope_policy_ref",
        "eligibility_policy_ref",
        "capture_occurrence_id",
        "observation_occurrence_id",
        "assessment_occurrence_id",
        "provider_id",
        "delivery_artifact_ref",
        "ingestion_sequence_scope",
        "RawSignalCatalogueId",
    )
}
_IDENTITY_NAMES = {
    type(factory("R001" if name == "RawSignalCatalogueId" else "codec")): name
    for name, factory in _FACTORIES.items()
}
_TRIGGERS = tuple(
    f"CREATE TRIGGER {table}_{action.lower()} BEFORE {action} ON {table} "
    "BEGIN SELECT RAISE(ABORT,'immutable M00 record'); END"
    for table in _TABLE_TYPES
    for action in ("UPDATE", "DELETE")
)
_DDL = (*_SCHEMA, *_TRIGGERS)


def _timestamp(value: datetime) -> str:
    return (
        f"{value.year:04d}-{value.month:02d}-{value.day:02d}T"
        f"{value.hour:02d}:{value.minute:02d}:{value.second:02d}.{value.microsecond:06d}Z"
    )


def _integer_key(value: int) -> bytes:
    digits = str(abs(value))
    if value >= 0:
        return b"\x01" + len(digits).to_bytes(8, "big") + digits.encode("ascii")
    complemented = "".join(str(9 - int(digit)) for digit in digits)
    return b"\x00" + (2**64 - 1 - len(digits)).to_bytes(8, "big") + complemented.encode("ascii")


def _metadata(value: Any) -> Any:
    if value is None or type(value) is str:
        return value
    if type(value) is int:
        return {"kind": "integer", "value": str(value)}
    if type(value) is datetime:
        return _timestamp(value)
    if type(value) in _IDENTITY_NAMES:
        return {"kind": _IDENTITY_NAMES[type(value)], "value": value.value}
    if type(value) is tuple:
        return [_metadata(item) for item in value]
    raise TypeError("unsupported M00 metadata representation")


def _encode(value: Any) -> bytes:
    content = {
        f.name: (
            _encode_native_record(value.native_record).hex()
            if f.name == "native_record"
            else _metadata(getattr(value, f.name))
        )
        for f in fields(value)
    }
    return json.dumps(content, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate M00 payload key")
        result[key] = value
    return result


def _decode_metadata(value: Any) -> Any:
    if type(value) is dict:
        if set(value) != {"kind", "value"} or type(value["value"]) is not str:
            raise ValueError("invalid tagged M00 metadata")
        if value["kind"] == "integer":
            number = int(value["value"])
            if str(number) != value["value"]:
                raise ValueError("noncanonical integer metadata")
            return number
        return _FACTORIES[value["kind"]](value["value"])
    if type(value) is list:
        return tuple(_decode_metadata(item) for item in value)
    if value is None or type(value) is str:
        return value
    raise ValueError("untyped M00 payload metadata")


def _decode(table: str, payload: bytes, digest: str) -> Any:
    if type(payload) is not bytes or hashlib.sha256(payload).hexdigest() != digest:
        raise ValueError("M00 payload digest mismatch")
    data = json.loads(payload, object_pairs_hook=_unique_object)
    cls = _TABLE_TYPES[table]
    if type(data) is not dict or set(data) != {f.name for f in fields(cls)}:
        raise ValueError("M00 payload fields do not match the exact v1 record")
    values: dict[str, Any] = {}
    for key, item in data.items():
        if key == "native_record":
            values[key] = _decode_native_record(bytes.fromhex(item))
        elif key.endswith("_utc") and item is not None:
            parsed = datetime.strptime(item, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
            if _timestamp(parsed) != item:
                raise ValueError("noncanonical UTC metadata")
            values[key] = parsed
        else:
            values[key] = _decode_metadata(item)
    result = cls(**values)
    if _encode(result) != payload:
        raise ValueError("noncanonical M00 payload")
    return result


def _index(table: str, value: Any) -> tuple[Any, ...]:
    if table == _POLICY:
        return (
            value.scope_policy_id.value,
            str(value.scope_policy_version),
            f"{value.scope_policy_id.value}@{value.scope_policy_version}",
            _timestamp(value.activation_ts_utc),
            None if value.deactivation_ts_utc is None else _timestamp(value.deactivation_ts_utc),
            value.eligibility_policy_ref.value,
        )
    if table == _CAPTURE:
        return (
            value.capture_occurrence_id.value,
            value.scope_policy_ref.value,
            _timestamp(value.slot_start_utc),
            _timestamp(value.slot_end_utc),
        )
    if table == _OBSERVATION:
        return (
            value.observation_occurrence_id.value,
            _timestamp(value.received_ts_utc),
            value.ingestion_sequence_scope.value,
            str(value.ingestion_sequence),
            _integer_key(value.ingestion_sequence),
        )
    return (
        value.assessment_occurrence_id.value,
        value.capture_occurrence_ref.value,
        value.outcome,
        _timestamp(value.evidence_as_of_ts_utc),
        None if value.supersedes_assessment_ref is None else value.supersedes_assessment_ref.value,
    )


def _validate_schema(connection: sqlite3.Connection) -> None:
    if connection.execute("PRAGMA application_id").fetchone()[0] != _APP_ID:
        raise ValueError("wrong M00 SQLite owner")
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise ValueError("unsupported M00 SQLite schema version")
    actual = {
        sql.strip()
        for name, sql in connection.execute(
            "SELECT name,sql FROM sqlite_schema WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'"
        )
    }
    if actual != set(_DDL):
        raise ValueError("M00 SQLite schema/constraints/index/trigger mismatch")
    if connection.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("M00 SQLite foreign-key integrity failure")
    if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
        raise ValueError("M00 SQLite structural integrity failure")


def _connect(path: str, *, write: bool, initialise: bool = False) -> sqlite3.Connection:
    connection = sqlite3.connect(
        Path(path).as_uri() + ("?mode=rw" if write else "?mode=ro"),
        uri=True,
        isolation_level=None,
        timeout=0,
    )
    try:
        if not initialise:
            _validate_schema(connection)
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA busy_timeout=0")
        if initialise:
            connection.execute("PRAGMA journal_mode=DELETE")
        if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
            raise ValueError("unsupported M00 SQLite journal policy")
        if write:
            connection.execute("PRAGMA synchronous=EXTRA")
            if connection.execute("PRAGMA synchronous").fetchone()[0] != 3:
                raise ValueError("M00 SQLite synchronisation unavailable")
        else:
            connection.execute("PRAGMA query_only=ON")
            if connection.execute("PRAGMA query_only").fetchone()[0] != 1:
                raise ValueError("M00 SQLite read-only mode unavailable")
        if (
            connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1
            or connection.execute("PRAGMA busy_timeout").fetchone()[0] != 0
        ):
            raise ValueError("M00 SQLite connection settings unavailable")
        return connection
    except BaseException:
        connection.close()
        raise


class _SQLiteTransaction:
    __slots__ = ("__connection", "__write")

    def __init__(self, connection: sqlite3.Connection, *, write: bool) -> None:
        self.__connection, self.__write = connection, write

    def __rows(self, table: str) -> list[Any]:
        columns = ",".join((*_COLUMNS[table], "payload", "content_sha256"))
        result = []
        for row in self.__connection.execute(f"SELECT {columns} FROM {table}"):
            try:
                value = _decode(table, row[-2], row[-1])
                if tuple(row[:-2]) != _index(table, value):
                    raise ValueError("M00 index/payload disagreement")
                result.append(value)
            except (ValueError, TypeError, KeyError, OverflowError) as exc:
                raise api.PersistenceFailureV1("M00 payload/index integrity failure") from exc
        return result

    def __append(self, table: str, value: Any) -> None:
        if not self.__write:
            raise api.PersistenceFailureV1("read-only M00 transaction cannot append")
        payload = _encode(value)
        values = (*_index(table, value), payload, hashlib.sha256(payload).hexdigest())
        columns = ",".join((*_COLUMNS[table], "payload", "content_sha256"))
        placeholders = ",".join("?" for _ in values)
        self.__connection.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values
        )

    def get_policy(
        self, scope_policy_id: api._ScopePolicyId, scope_policy_version: int
    ) -> api.CaptureScopePolicyV1 | None:
        return next(
            (
                p
                for p in self.__rows(_POLICY)
                if p.scope_policy_id == scope_policy_id
                and p.scope_policy_version == scope_policy_version
            ),
            None,
        )

    def get_policy_by_ref(
        self, scope_policy_ref: api._ScopePolicyRef
    ) -> api.CaptureScopePolicyV1 | None:
        return next(
            (
                p
                for p in self.__rows(_POLICY)
                if f"{p.scope_policy_id.value}@{p.scope_policy_version}" == scope_policy_ref.value
            ),
            None,
        )

    def list_policies(self) -> Sequence[api.CaptureScopePolicyV1]:
        return tuple(self.__rows(_POLICY))

    def append_policy(
        self, value: api.CaptureScopePolicyV1, scope_policy_ref: api._ScopePolicyRef
    ) -> None:
        if _index(_POLICY, value)[2] != scope_policy_ref.value:
            raise ValueError("policy reference does not match stored policy identity/version")
        self.__append(_POLICY, value)

    def get_capture(
        self, capture_occurrence_id: api._CaptureOccurrenceId
    ) -> api.ScheduledCaptureOccurrenceV1 | None:
        return next(
            (v for v in self.__rows(_CAPTURE) if v.capture_occurrence_id == capture_occurrence_id),
            None,
        )

    def get_capture_by_slot(
        self, scope_policy_ref: api._ScopePolicyRef, slot_start_utc: datetime
    ) -> api.ScheduledCaptureOccurrenceV1 | None:
        return next(
            (
                v
                for v in self.__rows(_CAPTURE)
                if v.scope_policy_ref == scope_policy_ref and v.slot_start_utc == slot_start_utc
            ),
            None,
        )

    def append_capture(self, value: api.ScheduledCaptureOccurrenceV1) -> None:
        self.__append(_CAPTURE, value)

    def get_observation(
        self, observation_occurrence_id: api._ObservationOccurrenceId
    ) -> api.RawObservationOccurrenceV1 | None:
        return next(
            (
                v
                for v in self.__rows(_OBSERVATION)
                if v.observation_occurrence_id == observation_occurrence_id
            ),
            None,
        )

    def get_observation_high_water(
        self, ingestion_sequence_scope: api._IngestionSequenceScope
    ) -> int | None:
        return max(
            (
                v.ingestion_sequence
                for v in self.__rows(_OBSERVATION)
                if v.ingestion_sequence_scope == ingestion_sequence_scope
            ),
            default=None,
        )

    def list_observations_received_between(
        self, slot_start_utc: datetime, slot_end_utc: datetime
    ) -> Sequence[api.RawObservationOccurrenceV1]:
        return tuple(
            v
            for v in self.__rows(_OBSERVATION)
            if slot_start_utc <= v.received_ts_utc < slot_end_utc
        )

    def append_observation(self, value: api.RawObservationOccurrenceV1) -> None:
        self.__append(_OBSERVATION, value)

    def get_assessment(
        self, assessment_occurrence_id: api._AssessmentOccurrenceId
    ) -> api.CaptureReceiptPresenceAssessmentV1 | None:
        return next(
            (
                v
                for v in self.__rows(_ASSESSMENT)
                if v.assessment_occurrence_id == assessment_occurrence_id
            ),
            None,
        )

    def list_assessments(
        self, capture_occurrence_id: api._CaptureOccurrenceId
    ) -> Sequence[api.CaptureReceiptPresenceAssessmentV1]:
        return tuple(
            v for v in self.__rows(_ASSESSMENT) if v.capture_occurrence_ref == capture_occurrence_id
        )

    def append_assessment(self, value: api.CaptureReceiptPresenceAssessmentV1) -> None:
        self.__append(_ASSESSMENT, value)


class _SQLitePort:
    __slots__ = ("__path",)

    def __init__(self, path: str) -> None:
        self.__path = path

    @contextmanager
    def transaction(self, *, write: bool) -> Iterator[api._PersistenceTransaction]:
        if type(write) is not bool:
            raise TypeError("write must be an exact bool")
        connection = None
        committing = False
        try:
            connection = _connect(self.__path, write=write)
            connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            yield _SQLiteTransaction(connection, write=write)
            committing = True
            connection.execute("COMMIT")
        except BaseException as exc:
            uncertain = bool(
                committing and connection is not None and not connection.in_transaction
            )
            if connection is not None and connection.in_transaction:
                try:
                    connection.execute("ROLLBACK")
                except sqlite3.Error:
                    uncertain = True
            if isinstance(exc, (sqlite3.Error, OSError)):
                raise api.PersistenceFailureV1(
                    "M00 SQLite operation failed", outcome_uncertain=uncertain
                ) from exc
            if isinstance(exc, ValueError) and connection is None:
                raise api.PersistenceFailureV1(
                    "M00 SQLite identity/schema/settings failure"
                ) from exc
            raise
        finally:
            if connection is not None:
                connection.close()


def create_sqlite_persistence(database_path: str, *, create: bool = False) -> api._PersistencePort:
    if type(database_path) is not str or type(create) is not bool:
        raise TypeError("SQLite path must be str and create must be bool")
    if (
        not database_path
        or not Path(database_path).is_absolute()
        or any(token in database_path for token in ("?", "#", "\x00"))
    ):
        raise ValueError("SQLite path must be a nonempty absolute regular-file path")
    path = Path(database_path)
    if path.is_symlink() or not path.parent.is_dir() or (path.exists() and not path.is_file()):
        raise ValueError("SQLite path cannot be a symlink or nonregular file")
    canonical = str(path.resolve())
    try:
        if create:
            descriptor = os.open(canonical, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(descriptor)
            connection = _connect(canonical, write=True, initialise=True)
            try:
                connection.execute("BEGIN IMMEDIATE")
                for sql in _DDL:
                    connection.execute(sql)
                connection.execute(f"PRAGMA application_id={_APP_ID}")
                connection.execute("PRAGMA user_version=1")
                connection.execute("COMMIT")
            finally:
                connection.close()
        connection = _connect(canonical, write=True)
        connection.close()
    except (OSError, sqlite3.Error, ValueError, TypeError) as exc:
        raise api.PersistenceFailureV1("M00 SQLite construction failed") from exc
    return cast(api._PersistencePort, _SQLitePort(canonical))
