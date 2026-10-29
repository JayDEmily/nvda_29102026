from __future__ import annotations

import importlib
import os
from typing import Any

import pytest

M00_DSN_ENV = "NVDA_TEST_M00_POSTGRES_DSN"
M01_DSN_ENV = "NVDA_TEST_M01_POSTGRES_DSN"
M00_TABLE = "rsot_raw_observation_occurrence_v1"


def _dsn(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(f"DS-T01-R03 PostgreSQL privilege proof requires {name}")
    return value


def _psycopg() -> Any:
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail(
            "DS-T01-R03 PostgreSQL privilege proof requires psycopg==3.3.4",
            pytrace=False,
        )


def _identity(dsn: str) -> tuple[str, str]:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute("SELECT current_user, current_schema()").fetchone()
        assert row is not None and row[1] is not None
        return str(row[0]), str(row[1])


def _private() -> tuple[Any, Any]:
    private = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    boundary_type = getattr(private, "PostgresBoundaryIdentityV1", None)
    factory = getattr(private, "create_postgres_persistence", None)
    assert boundary_type is not None
    assert callable(factory)
    return boundary_type, factory


def _prepare_m00() -> tuple[str, str, str, str, Any]:
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
    boundary_type, factory = _private()
    boundary = boundary_type(writer_role=m00_user, schema=m00_schema)
    return m00_dsn, m01_dsn, m01_user, f"{m00_schema}.{M00_TABLE}", (boundary, factory)


def _set_privileges(*, m00_dsn: str, m01_user: str, privilege_sql: str, grant: bool) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    _, m00_schema = _identity(m00_dsn)
    verb = "GRANT" if grant else "REVOKE"
    tail = "TO" if grant else "FROM"
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL(f"{verb} USAGE ON SCHEMA {{}} {tail} {{}}").format(
                sql.Identifier(m00_schema), sql.Identifier(m01_user)
            )
        )
        connection.execute(
            sql.SQL(f"{verb} {privilege_sql} ON TABLE {{}}.{{}} {tail} {{}}").format(
                sql.Identifier(m00_schema),
                sql.Identifier(M00_TABLE),
                sql.Identifier(m01_user),
            )
        )


def _effective_privilege(dsn: str, qualified_table: str, privilege: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_table_privilege(current_user, %s, %s)",
            (qualified_table, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


def test_factory_refuses_effective_select_privilege_on_m00_relation() -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    _set_privileges(m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql="SELECT", grant=True)
    try:
        assert _effective_privilege(m01_dsn, qualified, "SELECT") is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_privileges(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql="SELECT", grant=False
        )


@pytest.mark.parametrize("privilege", ["INSERT", "UPDATE", "DELETE"])
def test_factory_refuses_effective_write_privilege_on_m00_relation(privilege: str) -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    _set_privileges(
        m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql=privilege, grant=True
    )
    try:
        assert _effective_privilege(m01_dsn, qualified, privilege) is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_privileges(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql=privilege, grant=False
        )


def test_operation_refuses_privilege_drift_after_lawful_construction() -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    persistence = factory(m01_dsn, m00_boundary=boundary)
    _set_privileges(m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql="SELECT", grant=True)
    try:
        assert _effective_privilege(m01_dsn, qualified, "SELECT") is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            persistence.get_occurrence("ds-t01-r03-unknown")
    finally:
        _set_privileges(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege_sql="SELECT", grant=False
        )
