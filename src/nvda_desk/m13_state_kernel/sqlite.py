"""SQLite durable state and evidence adapters for the M13 public ports."""

from __future__ import annotations

import importlib
import sqlite3
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .codec import dumps_durable, loads_durable
from .contracts import (
    AtomicReceipt,
    DurableEvidenceRecord,
    IdempotencyConflictError,
    IdempotencyKey,
    StateVersionConflictError,
    TransactionCommand,
)
from .ports import EvidenceRepositoryPort, TransactionalStatePort


class SqliteUnitOfWork(TransactionalStatePort):
    """Atomic durable M13 state/receipt store with restart-safe idempotency."""

    durability = "durable_sqlite"

    def __init__(self, *, database_path: str | Path, initial_state: Any) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initial_state_json = dumps_durable(initial_state)
        self._active_attempt = False
        self._initialise()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=30, isolation_level=None)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    def _initialise(self) -> None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS kernel_state (
                    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                    state_json TEXT NOT NULL,
                    state_version INTEGER NOT NULL CHECK (state_version >= 0),
                    committed_sequence INTEGER NOT NULL CHECK (committed_sequence >= 0)
                )
                """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS atomic_receipts (
                    sequence INTEGER PRIMARY KEY CHECK (sequence >= 1),
                    scope_value TEXT NOT NULL,
                    command_type TEXT NOT NULL,
                    consistency_unit_id TEXT NOT NULL,
                    command_id TEXT NOT NULL,
                    input_fingerprint TEXT NOT NULL,
                    policy_version TEXT NOT NULL,
                    receipt_json TEXT NOT NULL,
                    UNIQUE (scope_value, command_type, consistency_unit_id)
                )
                """)
            connection.execute(
                "INSERT OR IGNORE INTO kernel_state VALUES (1, ?, 0, 0)",
                (self._initial_state_json,),
            )
            connection.commit()

    @property
    def state_version(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT state_version FROM kernel_state WHERE singleton = 1"
            ).fetchone()
        assert row is not None
        return int(row[0])

    @property
    def committed_sequence(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT committed_sequence FROM kernel_state WHERE singleton = 1"
            ).fetchone()
        assert row is not None
        return int(row[0])

    def snapshot_state(self) -> Any:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT state_json FROM kernel_state WHERE singleton = 1"
            ).fetchone()
        assert row is not None
        return deepcopy(loads_durable(row[0]))

    def list_receipts(self) -> tuple[AtomicReceipt, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT receipt_json FROM atomic_receipts ORDER BY sequence"
            ).fetchall()
        return tuple(self._receipt_from_json(row[0]) for row in rows)

    def execute(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        if not isinstance(command, TransactionCommand):
            raise TypeError("command must be a TransactionCommand")
        if not callable(mutation):
            raise TypeError("mutation must be callable")
        if self._active_attempt:
            raise RuntimeError("UnitOfWork.execute attempt is already active")
        self._active_attempt = True
        try:
            return self._execute_active(command=command, mutation=mutation)
        finally:
            self._active_attempt = False

    def _execute_active(
        self,
        *,
        command: TransactionCommand,
        mutation: Callable[[Any], Mapping[str, str]],
    ) -> AtomicReceipt:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            duplicate = connection.execute(
                """
                SELECT command_id, input_fingerprint, policy_version, receipt_json
                FROM atomic_receipts
                WHERE scope_value = ? AND command_type = ? AND consistency_unit_id = ?
                """,
                (
                    command.idempotency_key.value,
                    command.idempotency_key.command_type,
                    command.idempotency_key.consistency_unit_id,
                ),
            ).fetchone()
            if duplicate is not None:
                if duplicate[:3] != (
                    command.command_id,
                    command.input_fingerprint,
                    command.policy_version,
                ):
                    raise IdempotencyConflictError("conflicting idempotency-key reuse")
                connection.rollback()
                return replace(self._receipt_from_json(duplicate[3]), duplicate_replay=True)

            row = connection.execute(
                "SELECT state_json, state_version, committed_sequence FROM kernel_state WHERE singleton = 1"
            ).fetchone()
            assert row is not None
            state_json, prior_version, prior_sequence = row
            if command.expected_state_version != prior_version:
                raise StateVersionConflictError("stale expected state version")

            working_state = loads_durable(state_json)
            mutation_result = mutation(working_state)
            receipt = self._build_receipt(
                command=command,
                mutation_result=mutation_result,
                prior_version=prior_version,
                resulting_version=prior_version + 1,
                sequence=prior_sequence + 1,
            )
            connection.execute(
                "UPDATE kernel_state SET state_json = ?, state_version = ?, committed_sequence = ? WHERE singleton = 1",
                (dumps_durable(working_state), receipt.resulting_state_version, receipt.sequence),
            )
            connection.execute(
                """
                INSERT INTO atomic_receipts (
                    sequence, scope_value, command_type, consistency_unit_id,
                    command_id, input_fingerprint, policy_version, receipt_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    receipt.sequence,
                    command.idempotency_key.value,
                    command.idempotency_key.command_type,
                    command.idempotency_key.consistency_unit_id,
                    command.command_id,
                    command.input_fingerprint,
                    command.policy_version,
                    self._receipt_to_json(receipt),
                ),
            )
            connection.commit()
            return receipt
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _build_receipt(
        *,
        command: TransactionCommand,
        mutation_result: Mapping[str, str],
        prior_version: int,
        resulting_version: int,
        sequence: int,
    ) -> AtomicReceipt:
        if not isinstance(mutation_result, Mapping):
            raise TypeError("receipt result must be a mapping")
        receipt_id = mutation_result.get("receipt_id")
        result_id = mutation_result.get("result_id")
        if not isinstance(receipt_id, str) or not receipt_id.strip():
            raise ValueError("receipt_id must be a non-empty receipt identifier")
        if not isinstance(result_id, str) or not result_id.strip():
            raise ValueError("receipt result_id must be non-empty")
        return AtomicReceipt(
            receipt_id=receipt_id,
            result_id=result_id,
            command_id=command.command_id,
            command_type=command.idempotency_key.command_type,
            consistency_unit_id=command.idempotency_key.consistency_unit_id,
            idempotency_key=command.idempotency_key,
            input_fingerprint=command.input_fingerprint,
            policy_version=command.policy_version,
            prior_state_version=prior_version,
            resulting_state_version=resulting_version,
            sequence=sequence,
        )

    @staticmethod
    def _receipt_to_json(receipt: AtomicReceipt) -> str:
        return dumps_durable(asdict(receipt))

    @staticmethod
    def _receipt_from_json(payload: str) -> AtomicReceipt:
        data = loads_durable(payload)
        data["idempotency_key"] = IdempotencyKey(**data["idempotency_key"])
        return AtomicReceipt(**data)


class SqliteEvidenceRepository(EvidenceRepositoryPort):
    """Durable typed evidence occurrence store without domain interpretation."""

    def __init__(self, *, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS evidence_records (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id TEXT NOT NULL UNIQUE,
                    owner_module TEXT NOT NULL,
                    occurrence_id TEXT NOT NULL UNIQUE,
                    contract_path TEXT NOT NULL,
                    content_json TEXT NOT NULL,
                    content_fingerprint TEXT NOT NULL
                )
                """)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=30)
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    def store(
        self,
        *,
        owner_module: str,
        occurrence_id: str,
        content: BaseModel,
    ) -> DurableEvidenceRecord:
        if not isinstance(content, BaseModel):
            raise TypeError("typed_pydantic_evidence_required")
        contract_path = f"{type(content).__module__}:{type(content).__qualname__}"
        content_json = dumps_durable(content.model_dump(mode="python"))
        content_fingerprint = sha256(content_json.encode()).hexdigest()
        identity_material = dumps_durable(
            {
                "owner_module": owner_module,
                "occurrence_id": occurrence_id,
                "contract_path": contract_path,
                "content_fingerprint": content_fingerprint,
            }
        )
        record_id = f"durable-evidence:{sha256(identity_material.encode()).hexdigest()[:24]}"
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT record_id, owner_module, occurrence_id, contract_path, content_fingerprint, sequence FROM evidence_records WHERE occurrence_id = ?",
                (occurrence_id,),
            ).fetchone()
            if existing is not None:
                record = DurableEvidenceRecord(*existing)
                if (
                    record.owner_module,
                    record.contract_path,
                    record.content_fingerprint,
                ) != (owner_module, contract_path, content_fingerprint):
                    raise IdempotencyConflictError("conflicting durable evidence occurrence")
                return record
            cursor = connection.execute(
                """
                INSERT INTO evidence_records (
                    record_id, owner_module, occurrence_id, contract_path,
                    content_json, content_fingerprint
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    owner_module,
                    occurrence_id,
                    contract_path,
                    content_json,
                    content_fingerprint,
                ),
            )
            connection.commit()
            sequence = int(cursor.lastrowid)
        return DurableEvidenceRecord(
            record_id=record_id,
            owner_module=owner_module,
            occurrence_id=occurrence_id,
            contract_path=contract_path,
            content_fingerprint=content_fingerprint,
            sequence=sequence,
        )

    def load(self, occurrence_id: str) -> BaseModel:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT contract_path, content_json, content_fingerprint FROM evidence_records WHERE occurrence_id = ?",
                (occurrence_id,),
            ).fetchone()
        if row is None:
            raise KeyError(occurrence_id)
        contract_path, content_json, content_fingerprint = row
        if sha256(content_json.encode()).hexdigest() != content_fingerprint:
            raise ValueError("durable_evidence_content_fingerprint_mismatch")
        module_name, qualname = contract_path.split(":", 1)
        contract_type: Any = importlib.import_module(module_name)
        for token in qualname.split("."):
            contract_type = getattr(contract_type, token)
        if not isinstance(contract_type, type) or not issubclass(contract_type, BaseModel):
            raise ValueError("durable_evidence_contract_not_pydantic")
        return contract_type.model_validate(loads_durable(content_json))

    def list_records(self) -> tuple[DurableEvidenceRecord, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT record_id, owner_module, occurrence_id, contract_path, content_fingerprint, sequence FROM evidence_records ORDER BY sequence"
            ).fetchall()
        return tuple(DurableEvidenceRecord(*row) for row in rows)


__all__ = ["SqliteEvidenceRepository", "SqliteUnitOfWork"]
