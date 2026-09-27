"""Technical PostgreSQL persistence mechanism for Raw Signal Occurrence Truth.

This module is intentionally outside the public semantic seam. It stores and retrieves already
validated owner records; it does not decide schedule, eligibility, assessment outcome, or
supersession meaning.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from struct import pack, unpack
from typing import Any, cast

import psycopg

from .api import (
    AssessmentOutcome,
    CaptureReceiptPresenceAssessmentV1,
    CaptureScopePolicyV1,
    NativeValueV1,
    RawObservationOccurrenceV1,
    RawSignalCatalogueId,
    ScheduledCaptureOccurrenceV1,
    SourceTemporalKind,
    _AssessmentOccurrenceId,
    _CaptureOccurrenceId,
    _IngestionSequenceScope,
    _ObservationOccurrenceId,
    _PersistencePort,
    _PersistenceTransaction,
    _ScopePolicyId,
    _ScopePolicyRef,
    assessment_occurrence_id,
    capture_occurrence_id,
    concept_id,
    contract_id,
    delivery_artifact_ref,
    eligibility_policy_ref,
    ingestion_sequence_scope,
    observation_occurrence_id,
    provider_id,
    scope_policy_id,
    scope_policy_ref,
)

_POLICY_TABLE = "rsot_capture_scope_policy_v1"
_CAPTURE_TABLE = "rsot_scheduled_capture_occurrence_v1"
_OBSERVATION_TABLE = "rsot_raw_observation_occurrence_v1"
_ASSESSMENT_TABLE = "rsot_capture_receipt_presence_assessment_v1"

_NATIVE_CODEC_PREFIX = b"NVDA-NATIVE-V1\x00"

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
    CREATE TABLE IF NOT EXISTS {_OBSERVATION_TABLE} (
        observation_occurrence_id TEXT PRIMARY KEY,
        delivery_artifact_ref TEXT NOT NULL,
        source_provider TEXT NOT NULL,
        native_record BYTEA NOT NULL,
        received_ts_utc TIMESTAMPTZ(6) NOT NULL,
        received_epoch_ns NUMERIC,
        ingestion_sequence NUMERIC NOT NULL,
        ingestion_sequence_scope TEXT NOT NULL,
        source_temporal_kind TEXT NOT NULL CHECK (
            source_temporal_kind IN ('true_instant', 'date_only', 'receipt_only')
        ),
        raw_signal_catalogue_ids TEXT[],
        source_product_api TEXT,
        source_endpoint_callback TEXT,
        native_identifier TEXT,
        native_tick_series_identifier TEXT,
        source_variant TEXT,
        subject_instrument TEXT,
        native_units TEXT,
        availability_session TEXT,
        source_status_native TEXT,
        revision_vintage_native TEXT,
        source_timestamp_raw TEXT,
        source_timezone_native TEXT,
        market_timezone_iana TEXT,
        market_session_native TEXT
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


def _encode_length(value: int) -> bytes:
    if value < 0:
        raise ValueError("native codec length cannot be negative")
    return value.to_bytes(8, "big", signed=False)


def _encode_native_value(value: NativeValueV1) -> bytes:
    if value is None:
        return b"n"
    if type(value) is bool:
        return b"b\x01" if value else b"b\x00"
    if type(value) is int:
        payload = str(value).encode("ascii")
        return b"i" + _encode_length(len(payload)) + payload
    if type(value) is float:
        return b"f" + pack("!d", value)
    if type(value) is Decimal:
        value_tuple = value.as_tuple()
        digits = bytes(value_tuple.digits)
        exponent = str(value_tuple.exponent).encode("ascii")
        return (
            b"d"
            + bytes((value_tuple.sign,))
            + _encode_length(len(digits))
            + digits
            + _encode_length(len(exponent))
            + exponent
        )
    if type(value) is str:
        payload = value.encode("utf-8")
        return b"s" + _encode_length(len(payload)) + payload
    if type(value) is bytes:
        return b"y" + _encode_length(len(value)) + value
    if type(value) is list:
        parts = [b"l", _encode_length(len(value))]
        parts.extend(_encode_native_value(item) for item in value)
        return b"".join(parts)
    if type(value) is tuple:
        parts = [b"t", _encode_length(len(value))]
        parts.extend(_encode_native_value(item) for item in value)
        return b"".join(parts)
    if isinstance(value, Mapping):
        items = sorted(value.items(), key=lambda item: item[0].encode("utf-8"))
        parts = [b"m", _encode_length(len(items))]
        for key, item in items:
            key_payload = key.encode("utf-8")
            parts.extend(
                (
                    _encode_length(len(key_payload)),
                    key_payload,
                    _encode_native_value(item),
                )
            )
        return b"".join(parts)
    raise TypeError("native codec received a value outside NativeValueV1")


class _NativeCodecReader:
    __slots__ = ("_payload", "_position")

    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._position = 0

    @property
    def at_end(self) -> bool:
        return self._position == len(self._payload)

    def take(self, size: int) -> bytes:
        end = self._position + size
        if size < 0 or end > len(self._payload):
            raise ValueError("native codec payload is truncated")
        result = self._payload[self._position : end]
        self._position = end
        return result

    def length(self) -> int:
        return int.from_bytes(self.take(8), "big", signed=False)

    def value(self) -> NativeValueV1:
        tag = self.take(1)
        if tag == b"n":
            return None
        if tag == b"b":
            raw = self.take(1)
            if raw not in (b"\x00", b"\x01"):
                raise ValueError("native bool codec payload is invalid")
            return raw == b"\x01"
        if tag == b"i":
            return int(self.take(self.length()).decode("ascii"))
        if tag == b"f":
            return unpack("!d", self.take(8))[0]
        if tag == b"d":
            sign_raw = self.take(1)[0]
            if sign_raw not in (0, 1):
                raise ValueError("native Decimal sign is invalid")
            digits = tuple(self.take(self.length()))
            if any(digit > 9 for digit in digits):
                raise ValueError("native Decimal digit is invalid")
            exponent_text = self.take(self.length()).decode("ascii")
            sign_prefix = "-" if sign_raw else ""
            diagnostic = "".join(str(digit) for digit in digits)
            if exponent_text == "F":
                if digits != (0,):
                    raise ValueError("native Infinity Decimal payload is invalid")
                return Decimal(f"{sign_prefix}Infinity")
            if exponent_text == "n":
                return Decimal(f"{sign_prefix}NaN{diagnostic}")
            if exponent_text == "N":
                return Decimal(f"{sign_prefix}sNaN{diagnostic}")
            exponent = int(exponent_text)
            return Decimal((sign_raw, digits, exponent))
        if tag == b"s":
            return self.take(self.length()).decode("utf-8")
        if tag == b"y":
            return self.take(self.length())
        if tag == b"l":
            return [self.value() for _ in range(self.length())]
        if tag == b"t":
            return tuple(self.value() for _ in range(self.length()))
        if tag == b"m":
            result: dict[str, NativeValueV1] = {}
            for _ in range(self.length()):
                key = self.take(self.length()).decode("utf-8")
                if key in result:
                    raise ValueError("native mapping codec contains a duplicate key")
                result[key] = self.value()
            return result
        raise ValueError("native codec contains an unknown type tag")


def _encode_native_record(value: Mapping[str, NativeValueV1]) -> bytes:
    return _NATIVE_CODEC_PREFIX + _encode_native_value(cast(NativeValueV1, value))


def _decode_native_record(value: object) -> Mapping[str, NativeValueV1]:
    if isinstance(value, memoryview):
        payload = value.tobytes()
    elif type(value) is bytes:
        payload = value
    else:
        raise TypeError("native_record did not round-trip as PostgreSQL bytea")
    if not payload.startswith(_NATIVE_CODEC_PREFIX):
        raise ValueError("native_record codec version is not supported")
    reader = _NativeCodecReader(payload[len(_NATIVE_CODEC_PREFIX) :])
    decoded = reader.value()
    if not reader.at_end:
        raise ValueError("native_record codec contains trailing bytes")
    if not isinstance(decoded, Mapping):
        raise ValueError("native_record codec root must be a mapping")
    return cast(Mapping[str, NativeValueV1], decoded)


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


def _optional_text_from_row(value: object, field_name: str) -> str | None:
    if value is None or type(value) is str:
        return cast(str | None, value)
    raise TypeError(f"{field_name} did not round-trip as PostgreSQL text/NULL")


def _catalogue_ids_from_row(value: object) -> tuple[RawSignalCatalogueId, ...] | None:
    if value is None:
        return None
    if type(value) is not list or not value:
        raise TypeError("raw_signal_catalogue_ids did not round-trip as a non-empty text[]")
    if any(type(item) is not str for item in value):
        raise TypeError("raw_signal_catalogue_ids contained a non-text PostgreSQL value")
    return tuple(RawSignalCatalogueId(cast(str, item)) for item in cast(list[object], value))


def _observation_from_row(row: Sequence[object]) -> RawObservationOccurrenceV1:
    temporal_kind = str(row[8])
    if temporal_kind not in ("true_instant", "date_only", "receipt_only"):
        raise ValueError("source_temporal_kind did not round-trip as an accepted v1 value")
    received_epoch_ns = row[5]
    return RawObservationOccurrenceV1(
        concept_id=concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=observation_occurrence_id(str(row[0])),
        delivery_artifact_ref=delivery_artifact_ref(str(row[1])),
        source_provider=provider_id(str(row[2])),
        native_record=_decode_native_record(row[3]),
        received_ts_utc=(
            row[4] if isinstance(row[4], datetime) else _bad_datetime("received_ts_utc")
        ),
        received_epoch_ns=(
            None
            if received_epoch_ns is None
            else _integer_from_numeric(received_epoch_ns, "received_epoch_ns")
        ),
        ingestion_sequence=_integer_from_numeric(row[6], "ingestion_sequence"),
        ingestion_sequence_scope=ingestion_sequence_scope(str(row[7])),
        source_temporal_kind=cast(SourceTemporalKind, temporal_kind),
        raw_signal_catalogue_ids=_catalogue_ids_from_row(row[9]),
        source_product_api=_optional_text_from_row(row[10], "source_product_api"),
        source_endpoint_callback=_optional_text_from_row(
            row[11], "source_endpoint_callback"
        ),
        native_identifier=_optional_text_from_row(row[12], "native_identifier"),
        native_tick_series_identifier=_optional_text_from_row(
            row[13], "native_tick_series_identifier"
        ),
        source_variant=_optional_text_from_row(row[14], "source_variant"),
        subject_instrument=_optional_text_from_row(row[15], "subject_instrument"),
        native_units=_optional_text_from_row(row[16], "native_units"),
        availability_session=_optional_text_from_row(row[17], "availability_session"),
        source_status_native=_optional_text_from_row(row[18], "source_status_native"),
        revision_vintage_native=_optional_text_from_row(row[19], "revision_vintage_native"),
        source_timestamp_raw=_optional_text_from_row(row[20], "source_timestamp_raw"),
        source_timezone_native=_optional_text_from_row(row[21], "source_timezone_native"),
        market_timezone_iana=_optional_text_from_row(row[22], "market_timezone_iana"),
        market_session_native=_optional_text_from_row(row[23], "market_session_native"),
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

    def get_observation(
        self, observation_occurrence_id_value: _ObservationOccurrenceId
    ) -> RawObservationOccurrenceV1 | None:
        row = self.__connection.execute(
            f"""
            SELECT observation_occurrence_id, delivery_artifact_ref, source_provider,
                   native_record, received_ts_utc, received_epoch_ns,
                   ingestion_sequence, ingestion_sequence_scope, source_temporal_kind,
                   raw_signal_catalogue_ids, source_product_api, source_endpoint_callback,
                   native_identifier, native_tick_series_identifier, source_variant,
                   subject_instrument, native_units, availability_session,
                   source_status_native, revision_vintage_native, source_timestamp_raw,
                   source_timezone_native, market_timezone_iana, market_session_native
            FROM {_OBSERVATION_TABLE}
            WHERE observation_occurrence_id = %s
            """,
            (observation_occurrence_id_value.value,),
        ).fetchone()
        return None if row is None else _observation_from_row(row)

    def get_observation_high_water(
        self, ingestion_sequence_scope_value: _IngestionSequenceScope
    ) -> int | None:
        self.__lock_table_for_write(_OBSERVATION_TABLE)
        row = self.__connection.execute(
            f"""
            SELECT MAX(ingestion_sequence)
            FROM {_OBSERVATION_TABLE}
            WHERE ingestion_sequence_scope = %s
            """,
            (ingestion_sequence_scope_value.value,),
        ).fetchone()
        if row is None or row[0] is None:
            return None
        return _integer_from_numeric(row[0], "ingestion_sequence high-water")

    def append_observation(self, value: RawObservationOccurrenceV1) -> None:
        if not self.__write:
            raise RuntimeError("read-only persistence transaction cannot append an observation")
        self.__connection.execute(
            f"""
            INSERT INTO {_OBSERVATION_TABLE} (
                observation_occurrence_id, delivery_artifact_ref, source_provider,
                native_record, received_ts_utc, received_epoch_ns,
                ingestion_sequence, ingestion_sequence_scope, source_temporal_kind,
                raw_signal_catalogue_ids, source_product_api, source_endpoint_callback,
                native_identifier, native_tick_series_identifier, source_variant,
                subject_instrument, native_units, availability_session,
                source_status_native, revision_vintage_native, source_timestamp_raw,
                source_timezone_native, market_timezone_iana, market_session_native
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                value.observation_occurrence_id.value,
                value.delivery_artifact_ref.value,
                value.source_provider.value,
                _encode_native_record(value.native_record),
                value.received_ts_utc,
                value.received_epoch_ns,
                value.ingestion_sequence,
                value.ingestion_sequence_scope.value,
                value.source_temporal_kind,
                None
                if value.raw_signal_catalogue_ids is None
                else [item.value for item in value.raw_signal_catalogue_ids],
                value.source_product_api,
                value.source_endpoint_callback,
                value.native_identifier,
                value.native_tick_series_identifier,
                value.source_variant,
                value.subject_instrument,
                value.native_units,
                value.availability_session,
                value.source_status_native,
                value.revision_vintage_native,
                value.source_timestamp_raw,
                value.source_timezone_native,
                value.market_timezone_iana,
                value.market_session_native,
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
