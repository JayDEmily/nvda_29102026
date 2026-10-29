"""Versioned controlled D123 M00 public projection into genuine M01 PostgreSQL."""

from __future__ import annotations

import os
from decimal import Decimal

import psycopg
import pytest
from tests.product.derived_signal.test_m01_f4_d123_controlled_public import BASE, _public

from nvda_desk.derived_signal_calculation_truth._postgres import (
    PostgresBoundaryIdentityV1,
    create_postgres_persistence,
)
from nvda_desk.raw_signal_occurrence_truth._postgres import (
    create_postgres_persistence as create_m00_postgres,
)


def test_d123_controlled_public_result_persists_exact_postgresql_raw_lineage() -> None:
    m00_dsn = os.environ.get("NVDA_TEST_M00_POSTGRES_DSN")
    m01_dsn = os.environ.get("NVDA_TEST_M01_POSTGRES_DSN")
    if not m00_dsn or not m01_dsn:
        pytest.fail("D123 durability proof requires distinct M00/M01 PostgreSQL role DSNs")
    create_m00_postgres(m00_dsn)
    with psycopg.connect(m00_dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None
        boundary = PostgresBoundaryIdentityV1(str(row[0]), str(row[1]))
    pg = create_postgres_persistence(m01_dsn, m00_boundary=boundary)
    owner, request = _public(BASE, persistence=pg)
    output = owner.materialise(request)
    assert output is not None and output.result == Decimal(25)
    restored = pg.get_occurrence(output.derived_occurrence_id)
    assert restored == output
    assert restored.selection_identity == output.selection_identity
    assert {entry.observation_occurrence_id for entry in restored.raw_input_lineage} == {
        "controlled-prior",
        "controlled-current",
    }
    assert {entry.projection_mapping_version for entry in restored.raw_input_lineage} == {1}
    assert {entry.unit_convention_version for entry in restored.raw_input_lineage} == {1}
    assert owner.materialise(request) == output
