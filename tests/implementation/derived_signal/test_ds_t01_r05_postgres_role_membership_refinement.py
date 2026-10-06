from __future__ import annotations

import importlib
import os
from typing import Any

import pytest

ADMIN_DSN_ENV = "NVDA_TEST_POSTGRES_DSN"
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
        pytest.fail(f"DS-T01-R05 PostgreSQL role-membership proof requires {name}")
    return value


def _psycopg() -> Any:
    try:
        return importlib.import_module("psycopg")
    except ModuleNotFoundError:
        pytest.fail(
            "DS-T01-R05 PostgreSQL role-membership proof requires psycopg==3.3.4",
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


def _prepare_m00() -> tuple[str, str, str, str, str, Any]:
    admin_dsn = _dsn(ADMIN_DSN_ENV)
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
    psycopg = _psycopg()
    with psycopg.connect(m00_dsn) as connection:
        row = connection.execute(
            """
            SELECT c.oid
            FROM pg_catalog.pg_class AS c
            JOIN pg_catalog.pg_namespace AS n ON n.oid = c.relnamespace
            WHERE n.nspname = %s AND c.relname = %s
            """,
            (m00_schema, M00_TABLE),
        ).fetchone()
        assert row is not None
        relation_oid = int(row[0])
    return admin_dsn, m00_dsn, m01_dsn, m00_user, m01_user, (relation_oid, boundary, factory)


def _set_membership(
    *,
    admin_dsn: str,
    granted_role: str,
    member_role: str,
    grant: bool,
    inherit: bool = False,
    set_role: bool = True,
) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(admin_dsn) as connection:
        if grant:
            connection.execute(
                sql.SQL("GRANT {} TO {} WITH INHERIT {}, SET {}").format(
                    sql.Identifier(granted_role),
                    sql.Identifier(member_role),
                    sql.SQL("TRUE" if inherit else "FALSE"),
                    sql.SQL("TRUE" if set_role else "FALSE"),
                )
            )
        else:
            connection.execute(
                sql.SQL("REVOKE {} FROM {}").format(
                    sql.Identifier(granted_role), sql.Identifier(member_role)
                )
            )


def _create_helper_role(*, admin_dsn: str, role: str) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(admin_dsn) as connection:
        connection.execute(sql.SQL("CREATE ROLE {} NOLOGIN").format(sql.Identifier(role)))


def _drop_helper_role(*, admin_dsn: str, role: str) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(admin_dsn) as connection:
        connection.execute(sql.SQL("DROP ROLE {}").format(sql.Identifier(role)))


def _set_schema_usage(*, m00_dsn: str, role: str, grant: bool) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    _, m00_schema = _identity(m00_dsn)
    verb = "GRANT" if grant else "REVOKE"
    tail = "TO" if grant else "FROM"
    with psycopg.connect(m00_dsn) as connection:
        connection.execute(
            sql.SQL(f"{verb} USAGE ON SCHEMA {{}} {tail} {{}}").format(
                sql.Identifier(m00_schema), sql.Identifier(role)
            )
        )


def _set_table_privilege(
    *, m00_dsn: str, role: str, privilege: str, grant: bool
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
                sql.Identifier(role),
            )
        )


def _set_column_privilege(
    *, m00_dsn: str, role: str, privilege: str, grant: bool
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
                sql.Identifier(role),
            )
        )


def _can_set_role(dsn: str, role: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT pg_has_role(session_user, %s, 'SET')", (role,)
        ).fetchone()
        assert row is not None
        return bool(row[0])


def _current_table_privilege(dsn: str, relation_oid: int, privilege: str) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_table_privilege(current_user, %s::oid, %s)",
            (relation_oid, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


def _role_table_privilege(
    dsn: str, role: str, relation_oid: int, privilege: str
) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_table_privilege(%s, %s::oid, %s)",
            (role, relation_oid, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


def _role_column_privilege(
    dsn: str, role: str, relation_oid: int, privilege: str
) -> bool:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        row = connection.execute(
            "SELECT has_column_privilege(%s, %s::oid, %s, %s)",
            (role, relation_oid, M00_COLUMN, privilege),
        ).fetchone()
        assert row is not None
        return bool(row[0])


def test_factory_refuses_direct_set_role_path_to_m00_writer() -> None:
    admin_dsn, _m00_dsn, m01_dsn, m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    _set_membership(
        admin_dsn=admin_dsn,
        granted_role=m00_user,
        member_role=m01_user,
        grant=True,
        inherit=False,
        set_role=True,
    )
    try:
        assert _current_table_privilege(m01_dsn, relation_oid, "SELECT") is False
        assert _can_set_role(m01_dsn, m00_user) is True
        assert _role_table_privilege(m01_dsn, m00_user, relation_oid, "SELECT") is True
        with pytest.raises(ValueError, match=r"role|M00|SET"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=m00_user,
            member_role=m01_user,
            grant=False,
        )


def test_factory_refuses_transitive_set_role_path_to_m00_writer() -> None:
    admin_dsn, _m00_dsn, m01_dsn, m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    bridge_role = "nvda_ds_r05_set_bridge"
    _create_helper_role(admin_dsn=admin_dsn, role=bridge_role)
    try:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=m00_user,
            member_role=bridge_role,
            grant=True,
            inherit=False,
            set_role=True,
        )
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=bridge_role,
            member_role=m01_user,
            grant=True,
            inherit=False,
            set_role=True,
        )
        assert _current_table_privilege(m01_dsn, relation_oid, "SELECT") is False
        assert _can_set_role(m01_dsn, bridge_role) is True
        assert _can_set_role(m01_dsn, m00_user) is True
        with pytest.raises(ValueError, match=r"role|M00|SET"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=bridge_role,
            member_role=m01_user,
            grant=False,
        )
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=m00_user,
            member_role=bridge_role,
            grant=False,
        )
        _drop_helper_role(admin_dsn=admin_dsn, role=bridge_role)


@pytest.mark.parametrize("privilege", TABLE_PRIVILEGES)
def test_factory_refuses_settable_role_with_m00_table_privilege(privilege: str) -> None:
    admin_dsn, m00_dsn, m01_dsn, _m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    helper_role = f"nvda_ds_r05_table_{privilege.lower()}"
    _create_helper_role(admin_dsn=admin_dsn, role=helper_role)
    _set_schema_usage(m00_dsn=m00_dsn, role=helper_role, grant=True)
    _set_table_privilege(
        m00_dsn=m00_dsn, role=helper_role, privilege=privilege, grant=True
    )
    _set_membership(
        admin_dsn=admin_dsn,
        granted_role=helper_role,
        member_role=m01_user,
        grant=True,
        inherit=False,
        set_role=True,
    )
    try:
        assert _can_set_role(m01_dsn, helper_role) is True
        assert _role_table_privilege(m01_dsn, helper_role, relation_oid, privilege) is True
        assert _current_table_privilege(m01_dsn, relation_oid, privilege) is False
        with pytest.raises(ValueError, match=r"role|privilege|M00|SET"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=helper_role,
            member_role=m01_user,
            grant=False,
        )
        _set_table_privilege(
            m00_dsn=m00_dsn, role=helper_role, privilege=privilege, grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, role=helper_role, grant=False)
        _drop_helper_role(admin_dsn=admin_dsn, role=helper_role)


@pytest.mark.parametrize("privilege", COLUMN_PRIVILEGES)
def test_factory_refuses_settable_role_with_m00_column_privilege(privilege: str) -> None:
    admin_dsn, m00_dsn, m01_dsn, _m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    helper_role = f"nvda_ds_r05_column_{privilege.lower()}"
    _create_helper_role(admin_dsn=admin_dsn, role=helper_role)
    _set_schema_usage(m00_dsn=m00_dsn, role=helper_role, grant=True)
    _set_column_privilege(
        m00_dsn=m00_dsn, role=helper_role, privilege=privilege, grant=True
    )
    _set_membership(
        admin_dsn=admin_dsn,
        granted_role=helper_role,
        member_role=m01_user,
        grant=True,
        inherit=False,
        set_role=True,
    )
    try:
        assert _can_set_role(m01_dsn, helper_role) is True
        assert _role_table_privilege(m01_dsn, helper_role, relation_oid, privilege) is False
        assert _role_column_privilege(m01_dsn, helper_role, relation_oid, privilege) is True
        assert _current_table_privilege(m01_dsn, relation_oid, privilege) is False
        with pytest.raises(ValueError, match=r"role|privilege|M00|SET"):
            factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=helper_role,
            member_role=m01_user,
            grant=False,
        )
        _set_column_privilege(
            m00_dsn=m00_dsn, role=helper_role, privilege=privilege, grant=False
        )
        _set_schema_usage(m00_dsn=m00_dsn, role=helper_role, grant=False)
        _drop_helper_role(admin_dsn=admin_dsn, role=helper_role)


def test_non_inherited_membership_without_set_authority_remains_lawful() -> None:
    admin_dsn, _m00_dsn, m01_dsn, m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    _set_membership(
        admin_dsn=admin_dsn,
        granted_role=m00_user,
        member_role=m01_user,
        grant=True,
        inherit=False,
        set_role=False,
    )
    try:
        assert _current_table_privilege(m01_dsn, relation_oid, "SELECT") is False
        assert _can_set_role(m01_dsn, m00_user) is False
        factory(m01_dsn, m00_boundary=boundary)
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=m00_user,
            member_role=m01_user,
            grant=False,
        )


def test_operation_refuses_set_role_authority_drift_after_lawful_construction() -> None:
    admin_dsn, _m00_dsn, m01_dsn, m00_user, m01_user, prepared = _prepare_m00()
    relation_oid, boundary, factory = prepared
    persistence = factory(m01_dsn, m00_boundary=boundary)
    _set_membership(
        admin_dsn=admin_dsn,
        granted_role=m00_user,
        member_role=m01_user,
        grant=True,
        inherit=False,
        set_role=True,
    )
    try:
        assert _current_table_privilege(m01_dsn, relation_oid, "SELECT") is False
        assert _can_set_role(m01_dsn, m00_user) is True
        with pytest.raises(ValueError, match=r"role|M00|SET"):
            persistence.get_occurrence("ds-t01-r05-role-authority-drift")
    finally:
        _set_membership(
            admin_dsn=admin_dsn,
            granted_role=m00_user,
            member_role=m01_user,
            grant=False,
        )
