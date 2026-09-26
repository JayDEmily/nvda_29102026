"""Technical PostgreSQL persistence mechanism for Raw Signal Occurrence Truth.

This module is intentionally outside the public semantic seam. It stores and retrieves already
validated owner records; it does not decide schedule, eligibility, assessment outcome, or
supersession meaning.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from typing import Any, cast

import psycopg

from .api import (
    AssessmentOutcome,
    CaptureReceiptPresenceAssessmentV1,
    CaptureScopePolicyV1,
    ScheduledCaptureOccurrenceV1,
    _AssessmentOccurrenceId,
    _CaptureOccurrenceId,
    _PersistencePort,
    _PersistenceTransaction,
    _ScopePolicyId,
    _ScopePolicyRef,
    assessment_occurrence_id,
    capture_occurrence_id,
    concept_id,
    contract_id,
    eligibility_policy_ref,
    scope_policy_id,
    scope_policy_ref,
)

_POLICY_TABLE = "rsot_capture_scope_policy_v1"
_CAPTURE_TABLE = "rsot_scheduled_capture_occurrence_v1"
_ASSESSMENT_TABLE = "rsot_capture_receipt_presence_assessment_v1"

_SCHEMA_STATEMENTS = (
    f"""
    CREATE TABLE IF NOT EXISTS {_POLICY_TABLE} (
        scope_policy_id TEXT NOT NULL,
        scope_policy_version NUMERIC NOT NULL,
        scope_policy_ref TEXT NOT NULL UNIQUE,
        activation_ts_utc TIMESTAMPTZ(6) NOT NULL,
        deactivation_ts_utc TIMESTAMPTZ(6),
        eligibility_policy_ref TEXT NOT NULL,
        PRIMARY KEY (scope_policy_id, scope_policy_version),
        CHECK (scope_policy_version > 0),
        CHECK (deactivation_ts_utc IS NULL OR deactivation_ts_utc > activation_ts_utc)
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {_CAPTURE_TABLE} (
        capture_occurrence_id TEXT PRIMARY KEY,
        scope_policy_ref TEXT NOT NULL REFERENCES {_POLICY_TABLE}(scope_policy_ref),
        slot_start_utc TIMESTAMPTZ(6) NOT NULL,
        slot_end_utc TIMESTAMPTZ(6) NOT NULL,
        UNIQUE (scope_policy_ref, slot_start_utc)
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS {_ASSESSMENT_TABLE} (
        assessment_occurrence_id TEXT PRIMARY KEY,
        capture_occurrence_ref TEXT NOT NULL REFERENCES {_CAPTURE_TABLE}(capture_occurrence_id),
        outcome TEXT NOT NULL CHECK (
            outcome IN ('unknown_not_established', 'zero_received', 'one_or_more_received')
        ),
        evidence_as_of_ts_utc TIMESTAMPTZ(6) NOT NULL,
        supersedes_assessment_ref TEXT UNIQUE
            REFERENCES {_ASSESSMENT_TABLE}(assessment_occurrence_id)
    )
    """,
    f"""
    CREATE UNIQUE INDEX IF NOT EXISTS rsot_assessment_one_root_per_capture_v1
    ON {_ASSESSMENT_TABLE}(capture_occurrence_ref)
    WHERE supersedes_assessment_ref IS NULL
    """,
)


def _integer_from_numeric(value: object, field_name: str) -> int:
    if type(value) is int:
        return value
    if type(value) is Decimal and value == value.to_integral_value():
        return int(value)
    raise TypeError(f"{field_name} did not round-trip as an integral PostgreSQL numeric")


def _policy_from_row(row: Sequence[object]) -> CaptureScopePolicyV1:
    return CaptureScopePolicyV1(
        concept_id=concept_id("raw_signal.capture_scope_policy"),
        contract_id=contract_id("nvda.raw_signal.CaptureScopePolicy.v1"),
        units="not_applicable",
        scope_policy_id=scope_policy_id(str(row[0])),
        scope_policy_version=_integer_from_numeric(row[1], "scope_policy_version"),
        activation_ts_utc=row[3] if isinstance(row[3], datetime) else _bad_datetime("activation"),
        deactivation_ts_utc=(
            row[4]
            if row[4] is None or isinstance(row[4], datetime)
            else _bad_datetime("deactivation")
        ),
        eligibility_policy_ref=eligibility_policy_ref(str(row[5])),
    )


def _capture_from_row(row: Sequence[object]) -> ScheduledCaptureOccurrenceV1:
    return ScheduledCaptureOccurrenceV1(
        concept_id=concept_id("raw_signal.scheduled_capture_occurrence"),
        contract_id=contract_id("nvda.raw_signal.ScheduledCaptureOccurrence.v1"),
        units="not_applicable",
        capture_occurrence_id=capture_occurrence_id(str(row[0])),
        scope_policy_ref=scope_policy_ref(str(row[1])),
        slot_start_utc=row[2] if isinstance(row[2], datetime) else _bad_datetime("slot_start"),
        slot_end_utc=row[3] if isinstance(row[3], datetime) else _bad_datetime("slot_end"),
    )


def _assessment_from_row(row: Sequence[object]) -> CaptureReceiptPresenceAssessmentV1:
    outcome = str(row[2])
    if outcome not in (
        "unknown_not_established",
        "zero_received",
        "one_or_more_received",
    ):
        raise ValueError("assessment outcome did not round-trip as an accepted v1 value")
    supersedes = row[4]
    return CaptureReceiptPresenceAssessmentV1(
        concept_id=concept_id("raw_signal.capture_receipt_presence_assessment"),
        contract_id=contract_id("nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"),
        units="not_applicable",
        assessment_occurrence_id=assessment_occurrence_id(str(row[0])),
        capture_occurrence_ref=capture_occurrence_id(str(row[1])),
        outcome=cast(AssessmentOutcome, outcome),
        evidence_as_of_ts_utc=(
            row[3] if isinstance(row[3], datetime) else _bad_datetime("evidence_as_of")
        ),
        supersedes_assessment_ref=(
            None if supersedes is None else assessment_occurrence_id(str(supersedes))
        ),
    )


def _bad_datetime(field_name: str) -> Any:
    raise TypeError(f"{field_name} did not round-trip as a PostgreSQL timestamptz")


class _PostgresTransaction:
    __slots__ = ("__connection", "__write", "__write_locked_tables")

    def __init__(self, connection: Any, *, write: bool) -> None:
        self.__connection = connection
        self.__write = write
        self.__write_locked_tables: set[str] = set()

    def __lock_table_for_write(self, table: str) -> None:
        if not self.__write or table in self.__write_locked_tables:
            return
        self.__connection.execute(f"LOCK TABLE {table} IN SHARE ROW EXCLUSIVE MODE")
        self.__write_locked_tables.add(table)

    def get_policy(
        self, scope_policy_id_value: _ScopePolicyId, scope_policy_version: int
    ) -> CaptureScopePolicyV1 | None:
        row = self.__connection.execute(
            f"""
            SELECT scope_policy_id, scope_policy_version, scope_policy_ref,
                   activation_ts_utc, deactivation_ts_utc, eligibility_policy_ref
            FROM {_POLICY_TABLE}
            WHERE scope_policy_id = %s AND scope_policy_version = %s
            """,
            (scope_policy_id_value.value, scope_policy_version),
        ).fetchone()
        return None if row is None else _policy_from_row(row)

    def get_policy_by_ref(
        self, scope_policy_ref_value: _ScopePolicyRef
    ) -> CaptureScopePolicyV1 | None:
        row = self.__connection.execute(
            f"""
            SELECT scope_policy_id, scope_policy_version, scope_policy_ref,
                   activation_ts_utc, deactivation_ts_utc, eligibility_policy_ref
            FROM {_POLICY_TABLE}
            WHERE scope_policy_ref = %s
            """,
            (scope_policy_ref_value.value,),
        ).fetchone()
        return None if row is None else _policy_from_row(row)

    def list_policies(self) -> Sequence[CaptureScopePolicyV1]:
        self.__lock_table_for_write(_POLICY_TABLE)
        rows = self.__connection.execute(
            f"""
            SELECT scope_policy_id, scope_policy_version, scope_policy_ref,
                   activation_ts_utc, deactivation_ts_utc, eligibility_policy_ref
            FROM {_POLICY_TABLE}
            """
        ).fetchall()
        return tuple(_policy_from_row(row) for row in rows)

    def append_policy(
        self, value: CaptureScopePolicyV1, scope_policy_ref_value: _ScopePolicyRef
    ) -> None:
        if not self.__write:
            raise RuntimeError("read-only persistence transaction cannot append a policy")
        self.__connection.execute(
            f"""
            INSERT INTO {_POLICY_TABLE} (
                scope_policy_id, scope_policy_version, scope_policy_ref,
                activation_ts_utc, deactivation_ts_utc, eligibility_policy_ref
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                value.scope_policy_id.value,
                value.scope_policy_version,
                scope_policy_ref_value.value,
                value.activation_ts_utc,
                value.deactivation_ts_utc,
                value.eligibility_policy_ref.value,
            ),
        )

    def get_capture(
        self, capture_occurrence_id_value: _CaptureOccurrenceId
    ) -> ScheduledCaptureOccurrenceV1 | None:
        row = self.__connection.execute(
            f"""
            SELECT capture_occurrence_id, scope_policy_ref, slot_start_utc, slot_end_utc
            FROM {_CAPTURE_TABLE}
            WHERE capture_occurrence_id = %s
            """,
            (capture_occurrence_id_value.value,),
        ).fetchone()
        return None if row is None else _capture_from_row(row)

    def get_capture_by_slot(
        self, scope_policy_ref_value: _ScopePolicyRef, slot_start_utc: datetime
    ) -> ScheduledCaptureOccurrenceV1 | None:
        self.__lock_table_for_write(_CAPTURE_TABLE)
        row = self.__connection.execute(
            f"""
            SELECT capture_occurrence_id, scope_policy_ref, slot_start_utc, slot_end_utc
            FROM {_CAPTURE_TABLE}
            WHERE scope_policy_ref = %s AND slot_start_utc = %s
            """,
            (scope_policy_ref_value.value, slot_start_utc),
        ).fetchone()
        return None if row is None else _capture_from_row(row)

    def append_capture(self, value: ScheduledCaptureOccurrenceV1) -> None:
        if not self.__write:
            raise RuntimeError("read-only persistence transaction cannot append a capture")
        self.__connection.execute(
            f"""
            INSERT INTO {_CAPTURE_TABLE} (
                capture_occurrence_id, scope_policy_ref, slot_start_utc, slot_end_utc
            ) VALUES (%s, %s, %s, %s)
            """,
            (
                value.capture_occurrence_id.value,
                value.scope_policy_ref.value,
                value.slot_start_utc,
                value.slot_end_utc,
            ),
        )

    def get_assessment(
        self, assessment_occurrence_id_value: _AssessmentOccurrenceId
    ) -> CaptureReceiptPresenceAssessmentV1 | None:
        row = self.__connection.execute(
            f"""
            SELECT assessment_occurrence_id, capture_occurrence_ref, outcome,
                   evidence_as_of_ts_utc, supersedes_assessment_ref
            FROM {_ASSESSMENT_TABLE}
            WHERE assessment_occurrence_id = %s
            """,
            (assessment_occurrence_id_value.value,),
        ).fetchone()
        return None if row is None else _assessment_from_row(row)

    def list_assessments(
        self, capture_occurrence_id_value: _CaptureOccurrenceId
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        self.__lock_table_for_write(_ASSESSMENT_TABLE)
        rows = self.__connection.execute(
            f"""
            SELECT assessment_occurrence_id, capture_occurrence_ref, outcome,
                   evidence_as_of_ts_utc, supersedes_assessment_ref
            FROM {_ASSESSMENT_TABLE}
            WHERE capture_occurrence_ref = %s
            """,
            (capture_occurrence_id_value.value,),
        ).fetchall()
        return tuple(_assessment_from_row(row) for row in rows)

    def append_assessment(self, value: CaptureReceiptPresenceAssessmentV1) -> None:
        if not self.__write:
            raise RuntimeError("read-only persistence transaction cannot append an assessment")
        self.__connection.execute(
            f"""
            INSERT INTO {_ASSESSMENT_TABLE} (
                assessment_occurrence_id, capture_occurrence_ref, outcome,
                evidence_as_of_ts_utc, supersedes_assessment_ref
            ) VALUES (%s, %s, %s, %s, %s)
            """,
            (
                value.assessment_occurrence_id.value,
                value.capture_occurrence_ref.value,
                value.outcome,
                value.evidence_as_of_ts_utc,
                None
                if value.supersedes_assessment_ref is None
                else value.supersedes_assessment_ref.value,
            ),
        )


class _PostgresPersistence:
    __slots__ = ("__dsn",)

    def __init__(self, dsn: str) -> None:
        if type(dsn) is not str or not dsn.strip():
            raise ValueError("PostgreSQL DSN must be a non-empty string")
        self.__dsn = dsn
        self.__ensure_schema()

    def __connect(self) -> Any:
        return psycopg.connect(self.__dsn)

    def __ensure_schema(self) -> None:
        connection = self.__connect()
        try:
            for statement in _SCHEMA_STATEMENTS:
                connection.execute(statement)
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @contextmanager
    def transaction(self, *, write: bool) -> Iterator[_PersistenceTransaction]:
        connection = self.__connect()
        try:
            if write:
                connection.execute("SET LOCAL synchronous_commit TO on")
            else:
                connection.execute("SET TRANSACTION READ ONLY")
            transaction = _PostgresTransaction(connection, write=write)
            yield transaction
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()


def create_postgres_persistence(dsn: str) -> _PersistencePort:
    """Construct the private technical PostgreSQL persistence dependency for A00 injection."""

    return _PostgresPersistence(dsn)
