"""D116 PostgreSQL public seam: exact 300/1000 and two-versioned-R lineage."""

from __future__ import annotations

import os
from decimal import Decimal

import psycopg
import pytest
from tests.product.derived_signal.test_m01_f4_d116_authorised_public import public

from nvda_desk.derived_signal_calculation_truth._postgres import (
    PostgresBoundaryIdentityV1,
    create_postgres_persistence,
)
from nvda_desk.raw_signal_occurrence_truth._postgres import (
    create_postgres_persistence as create_m00_postgres,
)


@pytest.mark.parametrize("right,oi", (("call", "R047"), ("put", "R048")))
def test_d116_exact_postgres_public_ratio_and_reconstructable_lineage(
    right: str,
    oi: str,
) -> None:
    m00_dsn = os.environ.get("NVDA_TEST_M00_POSTGRES_DSN")
    m01_dsn = os.environ.get("NVDA_TEST_M01_POSTGRES_DSN")
    if not m00_dsn or not m01_dsn:
        pytest.fail("D116 durability proof requires distinct M00/M01 PostgreSQL role DSNs")
    create_m00_postgres(m00_dsn)
    with psycopg.connect(m00_dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None
        boundary = PostgresBoundaryIdentityV1(str(row[0]), str(row[1]))
    persistence = create_postgres_persistence(m01_dsn, m00_boundary=boundary)
    owner, request = public(right=right, r075=True, opposing=True, persistence=persistence)
    output = owner.materialise(request)
    assert output is not None and output.result == Decimal("0.3")
    restored = persistence.get_occurrence(output.derived_occurrence_id)
    assert restored == output
    assert {item.raw_signal_id for item in restored.raw_input_lineage} == {"R041", oi}
    assert {item.observation_occurrence_id for item in restored.raw_input_lineage} == {
        "d116-1",
        "d116-2",
    }
    assert {item.projection_mapping_version for item in restored.raw_input_lineage} == {1}
    assert {item.unit_convention_version for item in restored.raw_input_lineage} == {1}
    assert owner.materialise(request) == output
