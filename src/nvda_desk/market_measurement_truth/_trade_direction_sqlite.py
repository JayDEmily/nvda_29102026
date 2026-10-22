"""Owner-local D015 immutable store; no old store or codec is modified."""

from __future__ import annotations

import hashlib
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

from . import api as f
from ._rational import canonical
from ._sqlite import _path
from ._trade_direction import decode, validate

_TABLE = "mmt_trade_direction_occurrence_v1"
_DDL = (
    f"CREATE TABLE {_TABLE} (derived_occurrence_id TEXT PRIMARY KEY, "
    "logical_payload BLOB NOT NULL, content_sha256 TEXT NOT NULL) STRICT",
    *(
        f"CREATE TRIGGER {_TABLE}_{action.lower()} BEFORE {action} ON {_TABLE} "
        "BEGIN SELECT RAISE(ABORT,'immutable trade-direction record'); END"
        for action in ("UPDATE", "DELETE")
    ),
)
_SCHEMA = {statement.split()[2]: statement for statement in _DDL}


def _hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _schema(c: sqlite3.Connection) -> None:
    if (
        c.execute("PRAGMA application_id").fetchone()[0] != 0x4E560005
        or c.execute("PRAGMA user_version").fetchone()[0] != 1
        or dict(c.execute("SELECT name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%'"))
        != _SCHEMA
        or c.execute("PRAGMA foreign_key_check").fetchall()
    ):
        raise f.PersistenceFailureV1("trade-direction profile/schema integrity failure")


@contextmanager
def _transaction(
    path: str, *, write: bool, initialise: bool = False
) -> Iterator[sqlite3.Connection]:
    c = None
    committing = False
    try:
        _path(path)
        c = sqlite3.connect(
            Path(path).as_uri() + ("?mode=rw" if write else "?mode=ro"),
            uri=True,
            isolation_level=None,
            timeout=0,
        )
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA busy_timeout=0")
        c.execute("PRAGMA synchronous=EXTRA" if write else "PRAGMA query_only=ON")
        expected = {"foreign_keys": 1, "busy_timeout": 0, "journal_mode": "delete"}
        expected["synchronous" if write else "query_only"] = 3 if write else 1
        for name, value in expected.items():
            if c.execute("PRAGMA " + name).fetchone()[0] != value:
                raise f.PersistenceFailureV1("trade-direction connection policy mismatch")
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
            exc,
            (sqlite3.Error, OSError, ValueError, TypeError, KeyError, ArithmeticError, MemoryError),
        ):
            raise f.PersistenceFailureV1(
                "trade-direction SQLite operation failed",
                outcome_uncertain=uncertain,
            ) from exc
        raise
    finally:
        if c is not None:
            c.close()


def _load(c: sqlite3.Connection) -> tuple[f.TradeDirectionOccurrenceV1, ...]:
    result = []
    for identity, payload, digest in c.execute(
        f"SELECT derived_occurrence_id,logical_payload,content_sha256 FROM {_TABLE}"
    ):
        if type(payload) is not bytes or type(digest) is not str or _hash(payload) != digest:
            raise f.PersistenceFailureV1("trade-direction content integrity failure")
        value = decode(payload)
        if value.derived_occurrence_id != identity:
            raise f.PersistenceFailureV1("trade-direction row identity mismatch")
        result.append(value)
    return tuple(result)


class _SQLiteState:
    def __init__(self, path: str) -> None:
        self.path = _path(path)

    def all(self) -> tuple[f.TradeDirectionOccurrenceV1, ...]:
        with _transaction(self.path, write=False) as c:
            return _load(c)

    def append(self, value: f.TradeDirectionOccurrenceV1) -> f.TradeDirectionOccurrenceV1:
        with _transaction(self.path, write=True) as c:
            validate(value)
            for old in _load(c):
                if old.derived_occurrence_id == value.derived_occurrence_id:
                    if canonical(old) != canonical(
                        replace(
                            value,
                            calculated_at_utc=old.calculated_at_utc,
                        )
                    ):
                        raise f.PersistenceFailureV1("immutable trade-direction identity conflict")
                    return old
            payload = canonical(value)
            c.execute(
                f"INSERT INTO {_TABLE} VALUES (?,?,?)",
                (
                    value.derived_occurrence_id,
                    payload,
                    _hash(payload),
                ),
            )
            recovered = next(
                v for v in _load(c) if v.derived_occurrence_id == value.derived_occurrence_id
            )
            if canonical(recovered) != payload:
                raise f.PersistenceFailureV1("trade-direction complete-content readback mismatch")
            return recovered


def create_state(storage: f.SQLiteStorageV1) -> _SQLiteState:
    state = _SQLiteState(storage.database_path)
    if storage.create:
        try:
            fd = os.open(state.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
        except OSError as exc:
            raise f.PersistenceFailureV1("trade-direction exclusive creation failed") from exc
        with _transaction(state.path, write=True, initialise=True) as c:
            c.execute("PRAGMA application_id=1314258949")
            c.execute("PRAGMA user_version=1")
            for statement in _DDL:
                c.execute(statement)
            _schema(c)
    state.all()
    return state
