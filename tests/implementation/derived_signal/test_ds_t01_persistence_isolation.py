from __future__ import annotations

import importlib
import os

import pytest

M00_DSN_ENV = "NVDA_TEST_M00_POSTGRES_DSN"
M01_DSN_ENV = "NVDA_TEST_M01_POSTGRES_DSN"
M00_TABLES = (
    "rsot_capture_scope_policy_v1",
    "rsot_scheduled_capture_occurrence_v1",
    "rsot_raw_observation_occurrence_v1",
    "rsot_capture_receipt_presence_assessment_v1",
)


def _dsn(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(f"DS-T01 PostgreSQL boundary proof requires {name}")
    return value


def _psycopg():
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail("DS-T01 PostgreSQL boundary proof requires psycopg==3.3.4", pytrace=False)


def _identity(dsn: str) -> tuple[str, str]:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None
        return str(row[0]), str(row[1])


def test_postgresql_proof_roles_and_schemas_are_separate_and_m01_has_no_m00_table_privilege(
) -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    m01_dsn = _dsn(M01_DSN_ENV)
    create_m00 = importlib.import_module(
        "nvda_desk.raw_signal_occurrence_truth._postgres"
    ).create_postgres_persistence
    create_m00(m00_dsn)

    m00_user, m00_schema = _identity(m00_dsn)
    m01_user, m01_schema = _identity(m01_dsn)
    assert m00_user != m01_user
    assert m00_schema != m01_schema

    psycopg = _psycopg()
    with psycopg.connect(m00_dsn) as connection:
        for table in M00_TABLES:
            qualified = f"{m00_schema}.{table}"
            row = connection.execute(
                "SELECT has_table_privilege(%s, %s, 'SELECT'), "
                "has_table_privilege(%s, %s, 'INSERT,UPDATE,DELETE')",
                (m01_user, qualified, m01_user, qualified),
            ).fetchone()
            assert row == (False, False), qualified


def test_m01_postgres_persistence_factory_is_present_only_on_private_mechanism_surface() -> None:
    try:
        private = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    except ModuleNotFoundError:
        pytest.fail("DS-T01 expected M01 private PostgreSQL persistence mechanism", pytrace=False)
    assert callable(getattr(private, "create_postgres_persistence", None))

    public = importlib.import_module("nvda_desk.derived_signal_calculation_truth.api")
    assert "create_postgres_persistence" not in getattr(public, "__all__", ())
