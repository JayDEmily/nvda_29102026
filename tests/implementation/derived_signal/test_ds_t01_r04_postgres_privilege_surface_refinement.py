from __future__ import annotations

import importlib
import os
from typing import Any

import pytest

M00_DSN_ENV = "NVDA_TEST_M00_POSTGRES_DSN"
M01_DSN_ENV = "NVDA_TEST_M01_POSTGRES_DSN"
M00_TABLE = "rsot_raw_observation_occurrence_v1"
M00_COLUMN = "observation_occurrence_id"
TABLE_PRIVILEGES = (
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
    "TRUNCATE",
    "REFERENCES",
    "TRIGGER",
    "MAINTAIN",
)
COLUMN_PRIVILEGES = ("SELECT", "INSERT", "UPDATE", "REFERENCES")


def _dsn(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.fail(f"DS-T01-R04 PostgreSQL privilege-surface proof requires {name}")
    return value


def _psycopg() -> Any:
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail(
            "DS-T01-R04 PostgreSQL privilege-surface proof requires psycopg==3.3.4",
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


def _set_schema_usage(*, m00_dsn: str, m01_user: str, grant: bool) -> None:
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


def _set_table_privilege(
    *, m00_dsn: str, m01_user: str, privilege: str, grant: bool
) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    _, m00_schema = _identity(m00_dsn)
    verb = "GRANT" if grant else "REVOKE"
    tail = "TO" if grant else "FROM"
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL(f"{verb} {privilege} ON TABLE {{}}.{{}} {tail} {{}}").format(
                sql.Identifier(m00_schema),
                sql.Identifier(M00_TABLE),
                sql.Identifier(m01_user),
            )
        )


def _set_column_privilege(
    *, m00_dsn: str, m01_user: str, privilege: str, grant: bool
) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    _, m00_schema = _identity(m00_dsn)
    verb = "GRANT" if grant else "REVOKE"
    tail = "TO" if grant else "FROM"
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL(f"{verb} {privilege} ({{}}) ON TABLE {{}}.{{}} {tail} {{}}").format(
                sql.Identifier(M00_COLUMN),
                sql.Identifier(m00_schema),
                sql.Identifier(M00_TABLE),
                sql.Identifier(m01_user),
            )
        )


def _effective_table_privilege(dsn: str, qualified_table: str, privilege: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_table_privilege(current_user, %s, %s)",
            (qualified_table, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


def _effective_column_privilege(dsn: str, qualified_table: str, privilege: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_column_privilege(current_user, %s, %s, %s)",
            (qualified_table, M00_COLUMN, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


@pytest.mark.parametrize("privilege", TABLE_PRIVILEGES)
def test_factory_refuses_every_effective_table_privilege_on_m00_relation(
    privilege: str,
) -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=True)
    _set_table_privilege(
        m00_dsn=m00_dsn, m01_user=m01_user, privilege=privilege, grant=True
    )
    try:
        assert _effective_table_privilege(m01_dsn, qualified, privilege) is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_table_privilege(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege=privilege, grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=False)


@pytest.mark.parametrize("privilege", COLUMN_PRIVILEGES)
def test_factory_refuses_every_effective_column_privilege_on_m00_relation(
    privilege: str,
) -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=True)
    _set_column_privilege(
        m00_dsn=m00_dsn, m01_user=m01_user, privilege=privilege, grant=True
    )
    try:
        assert _effective_table_privilege(m01_dsn, qualified, privilege) is False
        assert _effective_column_privilege(m01_dsn, qualified, privilege) is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_column_privilege(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege=privilege, grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=False)


def test_operation_refuses_destructive_table_privilege_drift() -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    persistence = factory(m01_dsn, m00_boundary=boundary)
    _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=True)
    _set_table_privilege(
        m00_dsn=m00_dsn, m01_user=m01_user, privilege="TRUNCATE", grant=True
    )
    try:
        assert _effective_table_privilege(m01_dsn, qualified, "TRUNCATE") is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            persistence.get_occurrence("ds-t01-r04-truncate-drift")
    finally:
        _set_table_privilege(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege="TRUNCATE", grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=False)


def test_operation_refuses_column_select_privilege_drift() -> None:
    m00_dsn, m01_dsn, m01_user, qualified, pair = _prepare_m00()
    boundary, factory = pair
    persistence = factory(m01_dsn, m00_boundary=boundary)
    _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=True)
    _set_column_privilege(
        m00_dsn=m00_dsn, m01_user=m01_user, privilege="SELECT", grant=True
    )
    try:
        assert _effective_table_privilege(m01_dsn, qualified, "SELECT") is False
        assert _effective_column_privilege(m01_dsn, qualified, "SELECT") is True
        with pytest.raises(ValueError, match=r"privilege|M00"):
            persistence.get_occurrence("ds-t01-r04-column-drift")
    finally:
        _set_column_privilege(
            m00_dsn=m00_dsn, m01_user=m01_user, privilege="SELECT", grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, m01_user=m01_user, grant=False)
