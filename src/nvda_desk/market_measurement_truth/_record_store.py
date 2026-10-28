"""Reusable owner-local immutable typed record storage, independent of calculation law."""

from __future__ import annotations

import hashlib
import os
import sqlite3
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any

from . import api as f
from ._evaluation import canonical
from ._sqlite import _path

_DDL = (
    "CREATE TABLE mmt_record_v1 (derived_occurrence_id TEXT PRIMARY KEY, "
    "logical_payload BLOB NOT NULL, content_sha256 TEXT NOT NULL) STRICT",
    *(
        f"CREATE TRIGGER mmt_record_v1_{action.lower()} BEFORE {action} ON mmt_record_v1 "
        "BEGIN SELECT RAISE(ABORT,'immutable measurement record'); END"
        for action in ("UPDATE", "DELETE")
    ),
)
_SCHEMA = {statement.split()[2]: statement for statement in _DDL}


def _schema(c: sqlite3.Connection) -> None:
    if (
        c.execute("PRAGMA application_id").fetchone()[0] != 0x4E560006
        or c.execute("PRAGMA user_version").fetchone()[0] != 1
        or dict(c.execute("SELECT name,sql FROM sqlite_schema WHERE name NOT LIKE 'sqlite_%'"))
        != _SCHEMA
        or c.execute("PRAGMA foreign_key_check").fetchall()
    ):
        raise f.PersistenceFailureV1("measurement record profile/schema mismatch")


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
        if any(c.execute("PRAGMA " + k).fetchone()[0] != v for k, v in expected.items()):
            raise f.PersistenceFailureV1("measurement connection policy mismatch")
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
                "measurement record operation failed", outcome_uncertain=uncertain
            ) from exc
        raise
    finally:
        if c is not None:
            c.close()


class RecordState:
    """Private callback-based storage; public owners retain exact typed boundaries."""

    def __init__(
        self,
        storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1,
        decode: Callable[[bytes], Any],
        validate: Callable[[Any], None],
        *,
        encode: Callable[[Any], bytes] = canonical,
        identity_field: str = "derived_occurrence_id",
    ) -> None:
        self.decode, self.validate = decode, validate
        self.encode, self.identity_field = encode, identity_field
        self.memory: dict[str, Any] = {}
        self.path = None if isinstance(storage, f.MemoryStorageV1) else _path(storage.database_path)
        if type(storage) is f.SQLiteStorageV1 and storage.create:
            assert self.path is not None
            try:
                fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                os.close(fd)
            except OSError as exc:
                raise f.PersistenceFailureV1("measurement exclusive creation failed") from exc
            with _transaction(self.path, write=True, initialise=True) as c:
                c.execute("PRAGMA application_id=1314258950")
                c.execute("PRAGMA user_version=1")
                for statement in _DDL:
                    c.execute(statement)
                _schema(c)
        self.all()

    def _load(self, c: sqlite3.Connection) -> tuple[Any, ...]:
        result = []
        for identity, payload, digest in c.execute("SELECT * FROM mmt_record_v1"):
            if type(payload) is not bytes or hashlib.sha256(payload).hexdigest() != digest:
                raise f.PersistenceFailureV1("measurement record hash mismatch")
            value = self.decode(payload)
            self.validate(value)
            if getattr(value, self.identity_field) != identity:
                raise f.PersistenceFailureV1("measurement row identity mismatch")
            result.append(value)
        return tuple(result)

    def all(self) -> tuple[Any, ...]:
        if self.path is None:
            return tuple(self.memory.values())
        with _transaction(self.path, write=False) as c:
            return self._load(c)

    def _existing(self, values: tuple[Any, ...], value: Any) -> Any:
        for old in values:
            if getattr(old, self.identity_field) == getattr(value, self.identity_field):
                if self.encode(old) != self.encode(
                    replace(value, calculated_at_utc=old.calculated_at_utc)
                ):
                    raise f.PersistenceFailureV1("immutable measurement identity conflict")
                return old
        return None

    def append(self, value: Any) -> Any:
        self.validate(value)
        if self.path is None:
            old = self._existing(self.all(), value)
            if old is not None:
                return old
            self.memory[getattr(value, self.identity_field)] = value
            return value
        with _transaction(self.path, write=True) as c:
            old = self._existing(self._load(c), value)
            if old is not None:
                return old
            payload = self.encode(value)
            c.execute(
                "INSERT INTO mmt_record_v1 VALUES (?,?,?)",
                (getattr(value, self.identity_field), payload, hashlib.sha256(payload).hexdigest()),
            )
            recovered = next(
                v for v in self._load(c)
                if getattr(v, self.identity_field) == getattr(value, self.identity_field)
            )
            if self.encode(recovered) != payload:
                raise f.PersistenceFailureV1("measurement readback mismatch")
            return recovered

    def append_many(self, values: tuple[Any, ...]) -> tuple[Any, ...]:
        """Admit a complete immutable occurrence batch in one storage transaction."""
        if type(values) is not tuple or not values:
            raise ValueError("nonempty exact occurrence batch required")
        identities = tuple(getattr(v, self.identity_field) for v in values)
        if len(set(identities)) != len(identities):
            raise ValueError("duplicate identities in atomic occurrence batch")
        for value in values:
            self.validate(value)
        if self.path is None:
            existing = self.all()
            resolved = tuple(self._existing(existing, value) or value for value in values)
            for value in resolved:
                self.memory[getattr(value, self.identity_field)] = value
            return resolved
        with _transaction(self.path, write=True) as c:
            existing = self._load(c)
            resolved = tuple(self._existing(existing, value) or value for value in values)
            for value in resolved:
                if not any(getattr(old, self.identity_field) == getattr(value, self.identity_field)
                           for old in existing):
                    payload = self.encode(value)
                    c.execute(
                        "INSERT INTO mmt_record_v1 VALUES (?,?,?)",
                        (
                            getattr(value, self.identity_field), payload,
                            hashlib.sha256(payload).hexdigest(),
                        ),
                    )
            readback = {getattr(v, self.identity_field): v for v in self._load(c)}
            for value in resolved:
                if self.encode(readback[getattr(value, self.identity_field)]) != self.encode(value):
                    raise f.PersistenceFailureV1("atomic batch readback mismatch")
            return tuple(readback[identity] for identity in identities)
