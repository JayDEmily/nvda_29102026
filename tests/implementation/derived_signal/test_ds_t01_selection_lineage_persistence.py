from __future__ import annotations

import importlib
import os
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest

from nvda_desk.derived_signal_calculation_truth.api import DerivedSignalOccurrenceV1
from nvda_desk.raw_signal_occurrence_truth.api import RawSelectionIdentityV1

M00_DSN_ENV = "NVDA_TEST_M00_POSTGRES_DSN"
M01_DSN_ENV = "NVDA_TEST_M01_POSTGRES_DSN"


def _dsn(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(f"Leaf 1 PostgreSQL durability proof requires {name}")
    return value


def _psycopg() -> Any:
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail(
            "Leaf 1 PostgreSQL durability proof requires psycopg==3.3.4",
            pytrace=False,
        )


def _boundary_identity(dsn: str) -> object:
    private = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    boundary_type = getattr(private, "PostgresBoundaryIdentityV1")
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None and row[1] is not None
        return boundary_type(writer_role=str(row[0]), schema=str(row[1]))


def test_leaf1_postgres_roundtrip_preserves_exact_selection_identity() -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    m01_dsn = _dsn(M01_DSN_ENV)
    importlib.import_module(
        "nvda_desk.raw_signal_occurrence_truth._postgres"
    ).create_postgres_persistence(m00_dsn)
    private = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    persistence = private.create_postgres_persistence(
        m01_dsn,
        m00_boundary=_boundary_identity(m00_dsn),
    )

    identity = RawSelectionIdentityV1(
        values=(
            ("contract_id", "NVDA-2026-12-18-150-C"),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", Decimal("150")),
            ("option_right", "call"),
        )
    )
    now = datetime(2026, 10, 8, 1, 0, tzinfo=UTC)
    occurrence = DerivedSignalOccurrenceV1(
        derived_signal_id="D087",
        derived_occurrence_id="leaf1-selection-identity-postgres-roundtrip-v1",
        calculation_definition_version="calc-v1",
        parameter_context_refs=(),
        subject_instrument="NVDA",
        universe=None,
        effective_as_of_utc=now,
        window=None,
        knowledge_cutoff_utc=now,
        calculated_at_utc=now,
        result=Decimal("150.25"),
        units="currency",
        result_shape="scalar",
        raw_input_lineage=(),
        predecessor_occurrence_ids=(),
        convention_refs=(),
        selection_identity=identity,
        supersedes_derived_occurrence_id=None,
    )

    persistence.append_occurrence(occurrence)
    reloaded = persistence.get_occurrence(occurrence.derived_occurrence_id)

    assert reloaded is not None
    assert reloaded == occurrence
    assert reloaded.selection_identity == identity
    assert type(reloaded.selection_identity.value_for("strike")) is Decimal
