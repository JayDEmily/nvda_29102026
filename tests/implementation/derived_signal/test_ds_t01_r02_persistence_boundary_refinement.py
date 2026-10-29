from __future__ import annotations

import importlib
import os
from typing import Any

import pytest

M00_DSN_ENV = "NVDA_TEST_M00_POSTGRES_DSN"
M01_DSN_ENV = "NVDA_TEST_M01_POSTGRES_DSN"
_TABLE = "dsct_derived_signal_occurrence_v1"


def _dsn(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(f"DS-T01-R02 PostgreSQL boundary proof requires {name}")
    return value


def _psycopg() -> Any:
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail(
            "DS-T01-R02 PostgreSQL boundary proof requires psycopg==3.3.4",
            pytrace=False,
        )


def _private() -> tuple[Any, Any]:
    private = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    boundary_type = getattr(private, "PostgresBoundaryIdentityV1", None)
    if boundary_type is None:
        pytest.fail(
            "DS-T01-R02 requires an explicit private M00 persistence-boundary identity contract",
            pytrace=False,
        )
    factory = getattr(private, "create_postgres_persistence", None)
    assert callable(factory)
    return boundary_type, factory


def _identity(dsn: str) -> tuple[str, str]:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None and row[1] is not None
        return str(row[0]), str(row[1])


def _boundary(dsn: str) -> Any:
    boundary_type, _ = _private()
    writer_role, schema = _identity(dsn)
    return boundary_type(writer_role=writer_role, schema=schema)


def _with_search_path(dsn: str, schema: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    return str(conninfo.make_conninfo(dsn, options=f"-csearch_path={schema}"))


def _table_exists(dsn: str, schema: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute("SELECT to_regclass(%s)", (f"{schema}.{_TABLE}",)).fetchone()
        assert row is not None
        return row[0] is not None


def _drop_derived_table(dsn: str, schema: str) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(dsn) as connection:
        connection.execute(
            sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                sql.Identifier(schema), sql.Identifier(_TABLE)
            )
        )


def test_lawful_separate_m01_writer_and_schema_can_construct_persistence() -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    m01_dsn = _dsn(M01_DSN_ENV)
    _, factory = _private()
    boundary = _boundary(m00_dsn)
    m00_user, m00_schema = _identity(m00_dsn)
    m01_user, m01_schema = _identity(m01_dsn)
    assert m01_user != m00_user
    assert m01_schema != m00_schema

    _drop_derived_table(m01_dsn, m01_schema)
    factory(m01_dsn, m00_boundary=boundary)
    assert _table_exists(m01_dsn, m01_schema)


def test_exact_m00_writer_schema_boundary_is_refused_before_table_creation() -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    _, factory = _private()
    boundary = _boundary(m00_dsn)
    _, m00_schema = _identity(m00_dsn)
    _drop_derived_table(m00_dsn, m00_schema)

    with pytest.raises(ValueError, match=r"separate.*M00|M00.*separate"):
        factory(m00_dsn, m00_boundary=boundary)
    assert not _table_exists(m00_dsn, m00_schema)


def test_same_m00_writer_with_different_schema_is_refused() -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    _, factory = _private()
    boundary = _boundary(m00_dsn)
    m00_user, m00_schema = _identity(m00_dsn)
    probe_schema = f"{m00_schema}_writer_probe"
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {} AUTHORIZATION {}").format(
                sql.Identifier(probe_schema), sql.Identifier(m00_user)
            )
        )
    adverse_dsn = _with_search_path(m00_dsn, probe_schema)
    _drop_derived_table(adverse_dsn, probe_schema)

    with pytest.raises(ValueError, match=r"separate.*M00|M00.*separate"):
        factory(adverse_dsn, m00_boundary=boundary)
    assert not _table_exists(adverse_dsn, probe_schema)


def test_different_writer_on_m00_schema_is_refused() -> None:
    m00_dsn = _dsn(M00_DSN_ENV)
    m01_dsn = _dsn(M01_DSN_ENV)
    _, factory = _private()
    boundary = _boundary(m00_dsn)
    _, m00_schema = _identity(m00_dsn)
    m01_user, _ = _identity(m01_dsn)
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")

    _drop_derived_table(m00_dsn, m00_schema)
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL("GRANT USAGE, CREATE ON SCHEMA {} TO {}").format(
                sql.Identifier(m00_schema), sql.Identifier(m01_user)
            )
        )
    adverse_dsn = _with_search_path(m01_dsn, m00_schema)
    try:
        assert _identity(adverse_dsn)[1] == m00_schema
        with pytest.raises(ValueError, match=r"separate.*M00|M00.*separate"):
            factory(adverse_dsn, m00_boundary=boundary)
        assert not _table_exists(m00_dsn, m00_schema)
    finally:
        with psycopg.connect(m00_dsn) as connection:
            connection.execute(
                sql.SQL("REVOKE CREATE, USAGE ON SCHEMA {} FROM {}").format(
                    sql.Identifier(m00_schema), sql.Identifier(m01_user)
                )
            )
