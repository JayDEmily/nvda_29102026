from __future__ import annotations

import contextlib
from datetime import UTC, datetime
from decimal import Decimal
from struct import pack, unpack
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    build_owner,
    copy_with,
    observation,
    required_symbol,
)

from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence

_FIXED_NOW = datetime(2026, 9, 20, 12, 5, tzinfo=UTC)


def _dsn() -> str:
    import os

    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for Stage-3 real PostgreSQL proof")
    return value


def _fresh_owner(*, durability_port: Any | None = None) -> Any:
    port = durability_port or create_postgres_persistence(_dsn())
    return build_owner(durability_port=port, utc_now=lambda: _FIXED_NOW)


@pytest.fixture(autouse=True)
def _clean_stage3_tables() -> None:
    psycopg = pytest.importorskip("psycopg")
    assert psycopg.__version__ == "3.3.4"
    create_postgres_persistence(_dsn())
    with psycopg.connect(_dsn()) as connection:
        connection.execute(
            "TRUNCATE rsot_capture_receipt_presence_assessment_v1, "
            "rsot_raw_observation_occurrence_v1, "
            "rsot_scheduled_capture_occurrence_v1, "
            "rsot_capture_scope_policy_v1 CASCADE"
        )
        connection.commit()


def _observation_id(value: str) -> Any:
    return required_symbol("observation_occurrence_id")(value)


def test_stage3_fresh_owner_reads_exact_complete_observation_and_native_value_v1() -> None:
    nan_payload = unpack("!d", bytes.fromhex("7ff8000000000042"))[0]
    native = {
        "none": None,
        "bool": True,
        "int": 10**80,
        "negative-zero": -0.0,
        "nan": nan_payload,
        "decimal": Decimal("123.4500"),
        "decimal-nan": Decimal("-NaN"),
        "decimal-snan": Decimal("sNaN"),
        "decimal-infinity": Decimal("-Infinity"),
        "string": "provider-native::Δ",
        "bytes": b"\x00\xffnative",
        "list": [1, Decimal("2.00"), {"nested": b"x"}],
        "tuple": (False, "two", 3.0),
        "mapping": {"z": 1, "a": (2, 3)},
    }
    original = observation(
        observation_occurrence_id="stage3-fidelity",
        delivery_artifact_ref="stage3-delivery",
        source_provider="provider.stage3",
        raw_signal_catalogue_ids=("R001", "R323"),
        native_record=native,
        source_product_api="stage3-product-api",
        source_endpoint_callback="stage3-callback",
        native_identifier="stage3-native-id",
        native_tick_series_identifier="stage3-tick-series",
        source_variant="stage3-variant",
        subject_instrument="NVDA",
        native_units="USD",
        availability_session="regular",
        source_status_native="published",
        revision_vintage_native="rev-7",
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, 654321, tzinfo=UTC),
        received_epoch_ns=1_758_369_605_654_321_987,
        ingestion_sequence=77,
        ingestion_sequence_scope="stage3-fidelity-scope",
        source_temporal_kind="true_instant",
        source_timestamp_raw="2026-09-20T12:00:04.999999999Z",
        source_timezone_native="UTC",
        market_timezone_iana="America/New_York",
        market_session_native="regular-market",
    )

    stored = admit_observation(_fresh_owner(), original)
    reread = _fresh_owner().reads.get_raw_observation_occurrence(
        _observation_id("stage3-fidelity")
    )

    assert reread is not None
    assert reread.observation_occurrence_id == stored.observation_occurrence_id
    assert reread.delivery_artifact_ref == stored.delivery_artifact_ref
    assert reread.source_provider == stored.source_provider
    assert reread.received_ts_utc == stored.received_ts_utc
    assert reread.received_epoch_ns == stored.received_epoch_ns
    assert reread.ingestion_sequence == stored.ingestion_sequence
    assert reread.ingestion_sequence_scope == stored.ingestion_sequence_scope
    assert reread.source_temporal_kind == stored.source_temporal_kind
    assert reread.raw_signal_catalogue_ids == stored.raw_signal_catalogue_ids
    for field in (
        "source_product_api",
        "source_endpoint_callback",
        "native_identifier",
        "native_tick_series_identifier",
        "source_variant",
        "subject_instrument",
        "native_units",
        "availability_session",
        "source_status_native",
        "revision_vintage_native",
        "source_timestamp_raw",
        "source_timezone_native",
        "market_timezone_iana",
        "market_session_native",
    ):
        assert getattr(reread, field) == getattr(stored, field)

    assert reread.native_record["none"] is None
    assert type(reread.native_record["bool"]) is bool
    assert type(reread.native_record["int"]) is int
    assert reread.native_record["int"] == 10**80
    assert type(reread.native_record["negative-zero"]) is float
    assert pack("!d", reread.native_record["negative-zero"]) == pack("!d", -0.0)
    assert type(reread.native_record["nan"]) is float
    assert pack("!d", reread.native_record["nan"]) == pack("!d", native["nan"])
    assert type(reread.native_record["decimal"]) is Decimal
    assert reread.native_record["decimal"].as_tuple() == Decimal("123.4500").as_tuple()
    assert reread.native_record["decimal-nan"].as_tuple() == Decimal("-NaN").as_tuple()
    assert reread.native_record["decimal-snan"].as_tuple() == Decimal("sNaN").as_tuple()
    assert reread.native_record["decimal-infinity"].as_tuple() == Decimal(
        "-Infinity"
    ).as_tuple()
    assert type(reread.native_record["string"]) is str
    assert type(reread.native_record["bytes"]) is bytes
    assert type(reread.native_record["list"]) is list
    assert type(reread.native_record["tuple"]) is tuple
    assert isinstance(reread.native_record["mapping"], dict)

    retry = admit_observation(_fresh_owner(), original)
    assert retry.observation_occurrence_id == original.observation_occurrence_id


def test_stage3_same_identity_retry_and_conflict_bind_to_durable_original() -> None:
    original = observation(
        observation_occurrence_id="stage3-idempotent",
        native_record={"number": 1, "nested": (Decimal("2.00"), b"x")},
        ingestion_sequence=10,
        ingestion_sequence_scope="stage3-idempotent-scope",
    )
    admit_observation(_fresh_owner(), original)

    retry = admit_observation(_fresh_owner(), original)
    assert retry.observation_occurrence_id == original.observation_occurrence_id
    assert retry.native_record["number"] == 1
    assert type(retry.native_record["number"]) is int

    conflicting = copy_with(original, native_record={"number": 1.0})
    with pytest.raises(ValueError, match="different content"):
        admit_observation(_fresh_owner(), conflicting)

    reread = _fresh_owner().reads.get_raw_observation_occurrence(
        _observation_id("stage3-idempotent")
    )
    assert reread is not None
    assert type(reread.native_record["number"]) is int


def test_stage3_scope_local_high_water_survives_restart() -> None:
    admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-a-10",
            ingestion_sequence=10,
            ingestion_sequence_scope="stage3-scope-a",
        ),
    )
    admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-b-1",
            ingestion_sequence=1,
            ingestion_sequence_scope="stage3-scope-b",
        ),
    )

    with pytest.raises(ValueError, match="must not decrease"):
        admit_observation(
            _fresh_owner(),
            observation(
                observation_occurrence_id="stage3-a-9",
                ingestion_sequence=9,
                ingestion_sequence_scope="stage3-scope-a",
            ),
        )

    equal = admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-a-10-equal",
            ingestion_sequence=10,
            ingestion_sequence_scope="stage3-scope-a",
        ),
    )
    higher = admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-a-11",
            ingestion_sequence=11,
            ingestion_sequence_scope="stage3-scope-a",
        ),
    )
    independent = admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-b-2",
            ingestion_sequence=2,
            ingestion_sequence_scope="stage3-scope-b",
        ),
    )

    assert equal.ingestion_sequence == 10
    assert higher.ingestion_sequence == 11
    assert independent.ingestion_sequence == 2


class _FaultingTransaction:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def append_observation(self, value: Any) -> None:
        self._inner.append_observation(value)
        if self._fail_after == "observation":
            raise RuntimeError("stage3 injected observation write failure")


class _FaultingPort:
    def __init__(self, inner: Any, fail_after: str) -> None:
        self._inner = inner
        self._fail_after = fail_after

    @contextlib.contextmanager
    def transaction(self, *, write: bool) -> Any:
        with self._inner.transaction(write=write) as transaction:
            yield _FaultingTransaction(transaction, self._fail_after)
            if self._fail_after == "transaction_exit":
                raise RuntimeError("stage3 injected transaction exit failure")


def test_stage3_failed_observation_write_rolls_back_fact_and_high_water() -> None:
    faulting = _fresh_owner(
        durability_port=_FaultingPort(create_postgres_persistence(_dsn()), "observation")
    )
    with pytest.raises(RuntimeError, match="observation write failure"):
        admit_observation(
            faulting,
            observation(
                observation_occurrence_id="stage3-rolled-back",
                ingestion_sequence=10,
                ingestion_sequence_scope="stage3-rollback-scope",
            ),
        )

    assert (
        _fresh_owner().reads.get_raw_observation_occurrence(
            _observation_id("stage3-rolled-back")
        )
        is None
    )
    accepted = admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage3-after-rollback",
            ingestion_sequence=1,
            ingestion_sequence_scope="stage3-rollback-scope",
        ),
    )
    assert accepted.ingestion_sequence == 1


def test_stage3_public_success_waits_for_observation_commit_acknowledgement() -> None:
    faulting = _fresh_owner(
        durability_port=_FaultingPort(create_postgres_persistence(_dsn()), "transaction_exit")
    )
    with pytest.raises(RuntimeError, match="transaction exit failure"):
        admit_observation(
            faulting,
            observation(
                observation_occurrence_id="stage3-unacknowledged",
                ingestion_sequence=3,
                ingestion_sequence_scope="stage3-commit-scope",
            ),
        )

    assert (
        _fresh_owner().reads.get_raw_observation_occurrence(
            _observation_id("stage3-unacknowledged")
        )
        is None
    )
