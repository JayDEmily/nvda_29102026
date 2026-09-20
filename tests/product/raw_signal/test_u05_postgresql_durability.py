from __future__ import annotations

import ast
import importlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import uuid
from dataclasses import is_dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    as_mapping,
    assessment_contract,
    build_owner,
    capture_contract,
    observation,
    policy,
    required_symbol,
)

ROOT = Path(__file__).resolve().parents[3]
PROBE = ROOT / "tests/product/raw_signal/_process_probe.py"
OWNER_PACKAGE = ROOT / "src/nvda_desk/raw_signal_occurrence_truth"


def _dsn() -> str:
    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for real PostgreSQL product proof")
    return value


def _psycopg() -> Any:
    try:
        module = importlib.import_module("psycopg")
    except ModuleNotFoundError as exc:
        pytest.fail(f"psycopg 3.3.4 proof dependency is missing: {exc}")
    assert module.__version__ == "3.3.4"
    return module


def _token(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def _isolated_command() -> list[str]:
    unshare = shutil.which("unshare")
    if unshare is None:
        pytest.fail("unshare is required for the no-shared-local-persistence proof boundary")
    script = r"""
set -eu
mount --bind /mnt/data /mnt/data
mount -o remount,ro,bind /mnt/data
mount -t tmpfs tmpfs /tmp
mount -t tmpfs tmpfs /var/tmp
mount -t tmpfs tmpfs /dev/shm
mkdir -p /tmp/proof-home /tmp/proof-xdg /tmp/proof-work
cd /tmp/proof-work
exec "$1" "$2"
"""
    return [
        unshare,
        "--user",
        "--map-root-user",
        "--mount",
        "--net",
        "--fork",
        "sh",
        "-c",
        script,
        "sh",
        sys.executable,
        str(PROBE),
    ]


def _probe_env(workdir: Path) -> dict[str, str]:
    """Return a deliberately narrow child environment.

    The child receives no cloud/service credentials or alternate database configuration. The
    PostgreSQL DSN is delivered only in the JSON payload, while the local filesystem is made
    ephemeral/read-only by `_isolated_command`.
    """

    allowed = (
        "PATH",
        "LANG",
        "LC_ALL",
        "LD_LIBRARY_PATH",
        "VIRTUAL_ENV",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
    )
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT)])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["HOME"] = "/tmp/proof-home"
    env["TMPDIR"] = "/tmp"
    env["XDG_DATA_HOME"] = "/tmp/proof-xdg"
    return env


def _probe_process(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    isolated_filesystem: bool = True,
    **extra: Any,
) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"action": action, "dsn": dsn, "token": token, **extra}) + "\n"
    workdir = tmp_path / f"{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    command = _isolated_command() if isolated_filesystem else [sys.executable, str(PROBE)]
    return subprocess.run(
        command,
        cwd=ROOT,
        env=_probe_env(workdir),
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )


def _run_probe(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    isolated_filesystem: bool = True,
    **extra: Any,
) -> dict[str, Any]:
    completed = _probe_process(
        tmp_path,
        action,
        dsn=dsn,
        token=token,
        isolated_filesystem=isolated_filesystem,
        **extra,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    assert lines, "fresh-process probe produced no JSON result"
    return json.loads(lines[-1])


def _start_hold_probe(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    **extra: Any,
) -> tuple[subprocess.Popen[str], dict[str, Any]]:
    workdir = tmp_path / f"hold-{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    process = subprocess.Popen(
        _isolated_command(),
        cwd=ROOT,
        env=_probe_env(workdir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    payload = json.dumps(
        {"action": action, "dsn": dsn, "token": token, "hold_open": True, **extra}
    )
    process.stdin.write(payload + "\n")
    process.stdin.flush()
    first = process.stdout.readline().strip()
    if not first:
        stderr = process.stderr.read() if process.stderr is not None else ""
        raise AssertionError(f"hold-open probe produced no success result: {stderr}")
    result = json.loads(first)
    assert process.poll() is None, "writer exited before command-success visibility check"
    return process, result


def _release_hold_probe(process: subprocess.Popen[str]) -> None:
    assert process.stdin is not None
    process.stdin.write("release\n")
    process.stdin.flush()
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode == 0, stdout + stderr


def _kill_hold_probe(process: subprocess.Popen[str]) -> None:
    process.kill()
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode is not None
    assert process.returncode != 0, stdout + stderr


def _dsn_with_application_name(dsn: str, application_name: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    values = conninfo.conninfo_to_dict(dsn)
    values["application_name"] = application_name
    return conninfo.make_conninfo(**values)


def _assert_no_open_writer_transaction(dsn: str, application_name: str) -> None:
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            select state, xact_start
            from pg_stat_activity
            where application_name = %s and pid <> pg_backend_pid()
            """,
            (application_name,),
        )
        rows = cursor.fetchall()
    assert not any(xact_start is not None for _, xact_start in rows), rows


def _dsn_with_database(dsn: str, dbname: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    values = conninfo.conninfo_to_dict(dsn)
    values["dbname"] = dbname
    return conninfo.make_conninfo(**values)


def _admin_dsn(dsn: str) -> str:
    return _dsn_with_database(dsn, "postgres")


def _terminate_database_connections(admin_dsn: str, dbname: str) -> None:
    psycopg = _psycopg()
    with psycopg.connect(admin_dsn, autocommit=True) as connection, connection.cursor() as cursor:
        cursor.execute(
            "select pg_terminate_backend(pid) from pg_stat_activity "
            "where datname = %s and pid <> pg_backend_pid()",
            (dbname,),
        )


def _create_database(admin_dsn: str, dbname: str, *, template: str = "template0") -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(admin_dsn, autocommit=True) as connection, connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("create database {} template {}").format(
                sql.Identifier(dbname),
                sql.Identifier(template),
            )
        )


def _drop_database(admin_dsn: str, dbname: str) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    _terminate_database_connections(admin_dsn, dbname)
    with psycopg.connect(admin_dsn, autocommit=True) as connection, connection.cursor() as cursor:
        cursor.execute(sql.SQL("drop database if exists {}").format(sql.Identifier(dbname)))


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        return {"__datetime__": value.isoformat()}
    if isinstance(value, Enum):
        return {"__enum_type__": type(value).__qualname__, "value": _canonical(value.value)}
    if type(value) is not str and isinstance(value, str):
        return {"__identity_type__": type(value).__qualname__, "value": str(value)}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {
            str(k): _canonical(v)
            for k, v in sorted(value.items(), key=lambda item: str(item[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    if hasattr(value, "model_dump") or is_dataclass(value) or hasattr(value, "__dict__"):
        return {key: _canonical(item) for key, item in sorted(as_mapping(value).items())}
    return {"__type__": type(value).__qualname__, "value": str(value)}


def _authoritative_facts() -> dict[str, Any]:
    entropy = uuid.uuid4().hex
    return {
        "eligibility_policy_ref": f"eligibility-authority-{uuid.uuid4().hex}",
        "delivery_artifact_ref": f"delivery-authority-{uuid.uuid4().hex}",
        "source_provider": f"provider-authority-{uuid.uuid4().hex}",
        "native_identifier": f"native-authority-{uuid.uuid4().hex}",
        "native_record": {
            "High Entropy Alpha": uuid.uuid4().hex,
            "High Entropy Beta": uuid.uuid4().hex,
            "Provider Null": None,
        },
        "source_product_api": f"api-authority-{uuid.uuid4().hex}",
        "source_endpoint_callback": f"callback-authority-{uuid.uuid4().hex}",
        "native_tick_series_identifier": f"tick-authority-{uuid.uuid4().hex}",
        "source_variant": f"variant-authority-{uuid.uuid4().hex}",
        "subject_instrument": f"NVDA-authority-{entropy}",
        "native_units": f"units-authority-{uuid.uuid4().hex}",
        "availability_session": f"session-authority-{uuid.uuid4().hex}",
        "source_status_native": f"status-authority-{uuid.uuid4().hex}",
        "revision_vintage_native": f"revision-authority-{uuid.uuid4().hex}",
        "ingestion_sequence_scope": f"scope-authority-{uuid.uuid4().hex}",
        "source_timestamp_raw": f"provider-time-{uuid.uuid4().hex}",
        "source_timezone_native": f"timezone-authority-{uuid.uuid4().hex}",
        "market_timezone_iana": "America/New_York",
        "market_session_native": f"market-session-authority-{uuid.uuid4().hex}",
    }


def _expected_records(token: str, facts: dict[str, Any]) -> dict[str, Any]:
    policy_value = policy(
        scope_policy_id=f"scope::{token}",
        eligibility_policy_ref=facts["eligibility_policy_ref"],
    )
    capture_value = capture_contract(
        capture_occurrence_id=f"capture::{token}",
        scope_policy_ref=f"scope::{token}@1",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        slot_end_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
    )
    observation_value = observation(
        observation_occurrence_id=f"observation::{token}",
        delivery_artifact_ref=facts["delivery_artifact_ref"],
        source_provider=facts["source_provider"],
        native_identifier=facts["native_identifier"],
        native_record=facts["native_record"],
        source_product_api=facts["source_product_api"],
        source_endpoint_callback=facts["source_endpoint_callback"],
        native_tick_series_identifier=facts["native_tick_series_identifier"],
        source_variant=facts["source_variant"],
        subject_instrument=facts["subject_instrument"],
        native_units=facts["native_units"],
        availability_session=facts["availability_session"],
        source_status_native=facts["source_status_native"],
        revision_vintage_native=facts["revision_vintage_native"],
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, 654321, tzinfo=UTC),
        received_epoch_ns=1_758_369_605_654_321_987,
        ingestion_sequence=41,
        ingestion_sequence_scope=facts["ingestion_sequence_scope"],
        source_temporal_kind="true_instant",
        source_timestamp_raw=facts["source_timestamp_raw"],
        source_timezone_native=facts["source_timezone_native"],
        market_timezone_iana=facts["market_timezone_iana"],
        market_session_native=facts["market_session_native"],
    )
    zero_value = assessment_contract(
        assessment_occurrence_id=f"assessment-zero::{token}",
        capture_occurrence_ref=f"capture::{token}",
        outcome="zero_received",
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, 111111, tzinfo=UTC),
    )
    one_value = assessment_contract(
        assessment_occurrence_id=f"assessment-one::{token}",
        capture_occurrence_ref=f"capture::{token}",
        outcome="one_or_more_received",
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, 222222, tzinfo=UTC),
        supersedes_assessment_ref=f"assessment-zero::{token}",
    )
    return {
        "policy": _canonical(policy_value),
        "capture": _canonical(capture_value),
        "observation": _canonical(observation_value),
        "zero": _canonical(zero_value),
        "one": _canonical(one_value),
    }

def _without_pid(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "_pid"}


def _poisoned_dsn(dsn: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    values = conninfo.conninfo_to_dict(dsn)
    values["dbname"] = f"nvda_missing_{uuid.uuid4().hex}"
    return conninfo.make_conninfo(**values)


def _postgres_fact_hits(dsn: str, markers: list[str]) -> dict[str, int]:
    """Search all non-system PostgreSQL rows without assuming physical schema names."""

    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    hits = {marker: 0 for marker in markers}
    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            select table_schema, table_name
            from information_schema.tables
            where table_type = 'BASE TABLE'
              and table_schema not in ('pg_catalog', 'information_schema')
            order by table_schema, table_name
            """
        )
        tables = cursor.fetchall()
        assert tables, "real PostgreSQL proof contains no user tables after semantic writes"
        for schema, table in tables:
            relation = sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))
            for marker in markers:
                query = sql.SQL(
                    "select count(*) from {} as t where row_to_json(t)::text like %s"
                ).format(relation)
                cursor.execute(query, (f"%{marker}%",))
                hits[marker] += int(cursor.fetchone()[0])
    return hits


def _semantic_markers(token: str) -> list[str]:
    return [
        f"scope::{token}",
        f"capture::{token}",
        f"observation::{token}",
        f"delivery::{token}",
        f"eligibility-lineage::{token}",
        f"native-record::{token}",
        f"revision::{token}",
    ]


def _delete_postgres_rows_containing_marker(dsn: str, marker: str) -> int:
    """Delete only rows whose durable PostgreSQL representation contains marker.

    The proof intentionally discovers physical relations at runtime instead of prescribing a
    product table/schema. A semantic reader that merely requires PostgreSQL participation but
    reconstructs facts elsewhere will keep returning the record after this deletion and fail.
    """

    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    deleted = 0
    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            select table_schema, table_name
            from information_schema.tables
            where table_type = 'BASE TABLE'
              and table_schema not in ('pg_catalog', 'information_schema')
            order by table_schema, table_name
            """
        )
        for schema, table in cursor.fetchall():
            relation = sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))
            query = sql.SQL(
                "delete from {} as t where row_to_json(t)::text like %s returning 1"
            ).format(relation)
            cursor.execute(query, (f"%{marker}%",))
            deleted += len(cursor.fetchall())
    return deleted


def test_proof_environment_is_real_postgresql_17_9() -> None:
    psycopg = _psycopg()
    with psycopg.connect(_dsn()) as connection, connection.cursor() as cursor:
        cursor.execute("show server_version")
        version = cursor.fetchone()[0]
    assert version.startswith("17.9")


def test_public_factory_uses_same_semantic_owner_type_with_and_without_postgresql() -> None:
    assert type(build_owner()) is type(build_owner(postgres_dsn=_dsn()))


def test_process_boundary_forbids_shared_local_file_persistence(tmp_path: Path) -> None:
    host_path = ROOT / f".forbidden-proof-store-{uuid.uuid4().hex}"
    result = _run_probe(
        tmp_path,
        "filesystem_boundary",
        dsn=_dsn(),
        token=_token("fs-boundary"),
        host_path=str(host_path),
    )
    assert _without_pid(result) == {
        "ephemeral_write_ok": True,
        "host_write_blocked": True,
    }
    assert not host_path.exists()


def test_semantic_state_moves_with_postgresql_database_clone_and_not_original_process_state(
    tmp_path: Path,
) -> None:
    base_dsn = _dsn()
    admin_dsn = _admin_dsn(base_dsn)
    source_db = f"nvda_proof_src_{uuid.uuid4().hex}"
    clone_db = f"nvda_proof_clone_{uuid.uuid4().hex}"
    source_dsn = _dsn_with_database(base_dsn, source_db)
    clone_dsn = _dsn_with_database(base_dsn, clone_db)
    token = _token("pg-clone")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    _create_database(admin_dsn, source_db)
    try:
        _run_probe(tmp_path, "write_policy_only", dsn=source_dsn, token=token, facts=facts)
        _run_probe(tmp_path, "write_capture_only", dsn=source_dsn, token=token)
        _run_probe(tmp_path, "write_zero_assessment_only", dsn=source_dsn, token=token)
        _run_probe(tmp_path, "write_observation_only", dsn=source_dsn, token=token, facts=facts)
        _run_probe(tmp_path, "derive_relation_only", dsn=source_dsn, token=token)
        _run_probe(tmp_path, "write_one_assessment_only", dsn=source_dsn, token=token)

        _terminate_database_connections(admin_dsn, source_db)
        _create_database(admin_dsn, clone_db, template=source_db)
        _drop_database(admin_dsn, source_db)

        assert _run_probe(tmp_path, "read_policy", dsn=clone_dsn, token=token)["record"] == (
            expected["policy"]
        )
        assert _run_probe(tmp_path, "read_capture", dsn=clone_dsn, token=token)["record"] == (
            expected["capture"]
        )
        assert _run_probe(tmp_path, "read_observation", dsn=clone_dsn, token=token)["record"] == (
            expected["observation"]
        )
        chain = _run_probe(tmp_path, "read_assessment_chain", dsn=clone_dsn, token=token)
        assert chain["records"] == [expected["zero"], expected["one"]]

        source_read = _probe_process(tmp_path, "read_observation", dsn=source_dsn, token=token)
        assert source_read.returncode != 0
    finally:
        _drop_database(admin_dsn, clone_db)
        _drop_database(admin_dsn, source_db)


def test_command_return_is_durable_if_writer_is_killed_immediately_after_success(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("kill-after-return")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    def kill_then_read(
        action: str,
        read_action: str,
        expected_key: str,
        *,
        read_extra: dict[str, Any] | None = None,
        write_extra: dict[str, Any] | None = None,
    ) -> None:
        process, _ = _start_hold_probe(
            tmp_path,
            action,
            dsn=dsn,
            token=token,
            **(write_extra or {}),
        )
        _kill_hold_probe(process)
        fresh = _run_probe(
            tmp_path,
            read_action,
            dsn=dsn,
            token=token,
            **(read_extra or {}),
        )
        assert fresh["record"] == expected[expected_key]

    kill_then_read(
        "write_policy_only",
        "read_policy",
        "policy",
        write_extra={"facts": facts},
    )
    kill_then_read("write_capture_only", "read_capture", "capture")
    kill_then_read(
        "write_zero_assessment_only",
        "read_assessment",
        "zero",
        read_extra={"which": "zero"},
    )
    kill_then_read(
        "write_observation_only",
        "read_observation",
        "observation",
        write_extra={"facts": facts},
    )
    _run_probe(tmp_path, "derive_relation_only", dsn=dsn, token=token)
    kill_then_read(
        "write_one_assessment_only",
        "read_assessment",
        "one",
        read_extra={"which": "one"},
    )


def test_each_command_is_visible_before_writer_shutdown_and_matches_prewrite_authority(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("own-tx")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    def hold_and_read(
        action: str,
        read_action: str,
        expected_key: str,
        *,
        read_extra: dict[str, Any] | None = None,
        write_extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        application_name = f"nvda-proof-{action}-{uuid.uuid4().hex}"
        writer_dsn = _dsn_with_application_name(dsn, application_name)
        process, result = _start_hold_probe(
            tmp_path,
            action,
            dsn=writer_dsn,
            token=token,
            **(write_extra or {}),
        )
        try:
            assert process.poll() is None
            _assert_no_open_writer_transaction(dsn, application_name)
            fresh = _run_probe(
                tmp_path,
                read_action,
                dsn=dsn,
                token=token,
                **(read_extra or {}),
            )
            assert fresh["record"] == expected[expected_key]
            assert process.poll() is None, "writer exited before fresh read completed"
            return result
        finally:
            _release_hold_probe(process)

    hold_and_read(
        "write_policy_only",
        "read_policy",
        "policy",
        write_extra={"facts": facts},
    )
    hold_and_read("write_capture_only", "read_capture", "capture")
    hold_and_read(
        "write_zero_assessment_only",
        "read_assessment",
        "zero",
        read_extra={"which": "zero"},
    )
    hold_and_read(
        "write_observation_only",
        "read_observation",
        "observation",
        write_extra={"facts": facts},
    )

    relation_app = f"nvda-proof-relation-{uuid.uuid4().hex}"
    relation_process, relation_result = _start_hold_probe(
        tmp_path,
        "derive_relation_only",
        dsn=_dsn_with_application_name(dsn, relation_app),
        token=token,
    )
    try:
        assert relation_result["relation"] is not None
        _assert_no_open_writer_transaction(dsn, relation_app)
    finally:
        _release_hold_probe(relation_process)

    hold_and_read(
        "write_one_assessment_only",
        "read_assessment",
        "one",
        read_extra={"which": "one"},
    )

    faulted_observation = _run_probe(tmp_path, "fault_observation", dsn=dsn, token=token)
    assert faulted_observation["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_observation_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)["record"] == (
        expected["observation"]
    )

    faulted_assessment = _run_probe(tmp_path, "fault_assessment", dsn=dsn, token=token)
    assert faulted_assessment["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_assessment_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert _run_probe(tmp_path, "read_assessment", dsn=dsn, token=token, which="one")[
        "record"
    ] == expected["one"]


def test_postgresql_is_only_configured_cross_process_semantic_source_for_complete_facts(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("semantic-source")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token, facts=facts)
    _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token, facts=facts)

    high_entropy_markers = [
        facts["eligibility_policy_ref"],
        facts["delivery_artifact_ref"],
        facts["source_provider"],
        facts["native_identifier"],
        *facts["native_record"].values(),
        facts["revision_vintage_native"],
        facts["ingestion_sequence_scope"],
    ]
    high_entropy_markers = [item for item in high_entropy_markers if isinstance(item, str)]
    hits = _postgres_fact_hits(dsn, high_entropy_markers)
    assert all(count > 0 for count in hits.values()), hits

    # The reader receives only the DSN + domain query identity. It does not receive `facts` or
    # any writer-returned semantic object, so exact recovery cannot be reconstructed from the
    # opaque ID/token convention.
    fresh_policy = _run_probe(tmp_path, "read_policy", dsn=dsn, token=token)
    fresh_capture = _run_probe(tmp_path, "read_capture", dsn=dsn, token=token)
    fresh_observation = _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)
    assert fresh_policy["record"] == expected["policy"]
    assert fresh_capture["record"] == expected["capture"]
    assert fresh_observation["record"] == expected["observation"]

    deleted = _delete_postgres_rows_containing_marker(
        dsn, facts["native_record"]["High Entropy Alpha"]
    )
    assert deleted > 0, "no PostgreSQL row carrying authoritative observation facts was found"
    after_delete = _probe_process(tmp_path, "read_observation", dsn=dsn, token=token)
    if after_delete.returncode == 0:
        result = json.loads([line for line in after_delete.stdout.splitlines() if line.strip()][-1])
        assert result["record"] != expected["observation"], (
            "fresh reader reproduced complete authoritative observation facts after the "
            "correlated PostgreSQL state was removed"
        )

    poisoned = _probe_process(tmp_path, "read_observation", dsn=_poisoned_dsn(dsn), token=token)
    assert poisoned.returncode != 0


def test_durable_retry_and_conflicting_reuse_cross_process_boundaries(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("retry")
    _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    written = _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token)
    retry = _run_probe(tmp_path, "retry_observation", dsn=dsn, token=token)
    conflict = _run_probe(tmp_path, "conflict_observation", dsn=dsn, token=token)
    assert retry["record"] == written["record"]
    assert len({written["_pid"], retry["_pid"], conflict["_pid"]}) == 3
    assert _without_pid(conflict) == {"rejected": True}


def test_append_only_assessment_chain_is_exact_across_fresh_processes(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("assessment-chain")
    _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    zero = _run_probe(tmp_path, "write_zero_assessment_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "derive_relation_only", dsn=dsn, token=token)
    one = _run_probe(tmp_path, "write_one_assessment_only", dsn=dsn, token=token)
    chain = _run_probe(tmp_path, "read_assessment_chain", dsn=dsn, token=token)
    assert chain["records"] == [zero["record"], one["record"]]


def test_restart_preserves_policy_capture_assessment_and_scope_high_water_invariants(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("restart-invariants")
    _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_zero_assessment_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "derive_relation_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_one_assessment_only", dsn=dsn, token=token)

    assert _run_probe(tmp_path, "read_policy", dsn=dsn, token=token)["record"] is not None
    assert _run_probe(tmp_path, "read_capture", dsn=dsn, token=token)["record"] is not None
    assert _without_pid(
        _run_probe(tmp_path, "reregister_policy_conflict", dsn=dsn, token=token)
    ) == {"rejected": True}

    capture_conflict = _run_probe(
        tmp_path,
        "realise_conflicting_capture_for_existing_slot",
        dsn=dsn,
        token=token,
    )
    assert capture_conflict["rejected"] is True or (
        capture_conflict["capture_id"] == capture_conflict["original_id"]
    )

    immediate = _run_probe(
        tmp_path,
        "append_immediate_predecessor_assessment",
        dsn=dsn,
        token=token,
    )
    assert immediate["record"]["supersedes_assessment_ref"]["value"] == (
        f"assessment-one::{token}"
    )
    assert _without_pid(
        _run_probe(tmp_path, "append_stale_predecessor_assessment", dsn=dsn, token=token)
    ) == {"rejected": True}

    high_same_scope = _run_probe(
        tmp_path,
        "admit_high_sequence_same_scope",
        dsn=dsn,
        token=token,
    )
    assert high_same_scope["record"]["ingestion_sequence"] == 42
    assert _without_pid(
        _run_probe(tmp_path, "admit_low_sequence_same_scope", dsn=dsn, token=token)
    ) == {"rejected": True}

    other_scope = _run_probe(
        tmp_path,
        "admit_low_sequence_other_scope",
        dsn=dsn,
        token=token,
    )
    assert other_scope["record"]["ingestion_sequence"] == 1


def test_restart_reconciliation_commits_capture_before_assessment_and_recovers_exact_facts(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("restart")
    _run_probe(tmp_path, "write_policy_for_reconcile", dsn=dsn, token=token)

    faulted = _run_probe(tmp_path, "reconcile_fault_after_capture", dsn=dsn, token=token)
    assert faulted["failed"] is True
    after_fault = _run_probe(tmp_path, "read_reconcile", dsn=dsn, token=token)

    expected_capture = _canonical(
        capture_contract(
            capture_occurrence_id=f"recovered-capture::{token}",
            scope_policy_ref=f"scope::{token}@1",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            slot_end_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        )
    )
    assert after_fault["capture"] == expected_capture
    assert after_fault["assessment"] is None

    reconciled = _run_probe(tmp_path, "reconcile", dsn=dsn, token=token)
    fresh = _run_probe(tmp_path, "read_reconcile", dsn=dsn, token=token)
    assessment_shape = _canonical(
        assessment_contract(
            assessment_occurrence_id=f"recovered-assessment::{token}",
            capture_occurrence_ref=f"recovered-capture::{token}",
            outcome="unknown_not_established",
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )
    )
    assert reconciled["_pid"] != fresh["_pid"]
    assert fresh["capture"] == expected_capture
    assert fresh["assessment"] == assessment_shape
    assert reconciled["assessment"] == assessment_shape


def test_public_owner_accepts_explicit_technical_persistence_port_injection() -> None:
    builder = required_symbol("create_owner")
    assert "persistence_port" in inspect.signature(builder).parameters


def _module_name(path: Path) -> str:
    rel = path.relative_to(OWNER_PACKAGE).with_suffix("")
    if rel.name == "__init__":
        rel = rel.parent
    return ".".join(rel.parts)


def _local_import_targets(tree: ast.AST) -> set[str]:
    targets: set[str] = set()
    prefix = "nvda_desk.raw_signal_occurrence_truth"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == prefix:
                    targets.add("")
                elif alias.name.startswith(prefix + "."):
                    targets.add(alias.name[len(prefix) + 1 :])
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                if node.module:
                    targets.add(node.module)
                else:
                    targets.update(alias.name for alias in node.names)
            elif node.module == prefix:
                targets.update(alias.name for alias in node.names)
            elif node.module and node.module.startswith(prefix + "."):
                targets.add(node.module[len(prefix) + 1 :])
    return targets


def _technical_module_closure() -> dict[str, tuple[Path, ast.AST]]:
    modules: dict[str, tuple[Path, ast.AST]] = {}
    for path in OWNER_PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules[_module_name(path)] = (path, tree)

    owner = build_owner(postgres_dsn=_dsn())
    ports = _find_default_persistence_ports(owner)
    assert ports, "default PostgreSQL owner path hides its technical persistence port"
    prefix = "nvda_desk.raw_signal_occurrence_truth"
    runtime_seed_modules: set[str] = set()
    seen: set[int] = set()

    def visit_runtime(value: Any, depth: int) -> None:
        if depth > 6 or id(value) in seen:
            return
        seen.add(id(value))
        module = getattr(value, "__module__", type(value).__module__)
        if module == prefix:
            runtime_seed_modules.add("")
        elif module.startswith(prefix + "."):
            runtime_seed_modules.add(module[len(prefix) + 1 :])
        if depth == 6 or isinstance(value, (str, bytes, int, float, bool, type(None))):
            return
        try:
            children = vars(value).values()
        except TypeError:
            return
        for child in children:
            if callable(child) or type(child).__module__.startswith(prefix):
                visit_runtime(child, depth + 1)

    for port in ports:
        visit_runtime(port, 0)

    psycopg_seeds = {
        name
        for name, (path, tree) in modules.items()
        if any(
            (isinstance(node, ast.Import) and any(a.name.startswith("psycopg") for a in node.names))
            or (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
                and node.module.startswith("psycopg")
            )
            for node in ast.walk(tree)
        )
        or "psycopg" in path.read_text(encoding="utf-8")
    }
    seeds = {name for name in runtime_seed_modules | psycopg_seeds if name in modules}
    assert seeds, "default PostgreSQL technical mechanism is not present"
    closure = set(seeds)
    frontier = list(seeds)
    while frontier:
        current = frontier.pop()
        _, tree = modules[current]
        for target in _local_import_targets(tree):
            matches = [
                name
                for name in modules
                if name == target or name.startswith(target + ".")
            ]
            for match in matches:
                if match not in closure:
                    closure.add(match)
                    frontier.append(match)
    return {name: modules[name] for name in closure}


def test_complete_technical_persistence_closure_contains_no_semantic_decision_logic() -> None:
    required_symbol("create_owner")
    closure = _technical_module_closure()
    forbidden_function_names = {
        "derive_capture_receipt_evidence_relation",
        "derive_relation",
        "decide_relation",
        "decide_outcome",
        "assess_outcome",
        "classify_outcome",
        "is_eligible",
    }
    forbidden_semantic_literals = {
        "zero_received",
        "one_or_more_received",
        "unknown_not_established",
        "evidences_receipt_presence_only",
    }
    for _, (path, tree) in closure.items():
        function_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert not forbidden_function_names.intersection(function_names), path
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in {"__import__", "import_module"}, path
                if isinstance(node.func, ast.Attribute):
                    assert not (
                        isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "importlib"
                        and node.func.attr == "import_module"
                    ), path
            if isinstance(node, (ast.If, ast.Match, ast.Compare)):
                literals = {
                    child.value
                    for child in ast.walk(node)
                    if isinstance(child, ast.Constant) and isinstance(child.value, str)
                }
                assert not forbidden_semantic_literals.intersection(literals), path
            if isinstance(node, ast.Name):
                assert node.id != "eligibility_resolver", path
            if isinstance(node, ast.Attribute):
                assert node.attr != "eligibility_resolver", path


def test_owner_package_has_no_alternate_durable_backend_or_external_semantic_service() -> None:
    disallowed_import_roots = {
        "sqlite3",
        "shelve",
        "dbm",
        "redis",
        "sqlalchemy",
        "asyncpg",
        "boto3",
        "requests",
        "httpx",
        "aiohttp",
        "urllib",
        "socket",
        "subprocess",
        "multiprocessing",
        "mmap",
        "ctypes",
        "importlib",
    }
    for path in OWNER_PACKAGE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "open":
                    mode = None
                    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                        mode = node.args[1].value
                    for keyword in node.keywords:
                        if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                            mode = keyword.value.value
                    if isinstance(mode, str):
                        assert not any(flag in mode for flag in ("w", "a", "x", "+")), path
                if isinstance(node.func, ast.Attribute):
                    assert node.func.attr not in {"write_text", "write_bytes"}, path
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                        assert node.func.attr not in {"open", "write", "pwrite"}, path
                    if node.func.attr == "open":
                        mode = None
                        if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                            mode = node.args[1].value
                        for keyword in node.keywords:
                            if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                                mode = keyword.value.value
                        if isinstance(mode, str):
                            assert not any(flag in mode for flag in ("w", "a", "x", "+")), path
        assert not disallowed_import_roots.intersection(imported), (path, imported)


def _find_default_persistence_ports(owner: Any) -> list[Any]:
    required_methods = {
        "append_policy",
        "get_policy",
        "append_capture",
        "get_capture",
        "append_observation",
        "get_observation",
        "append_assessment",
        "get_assessment",
        "list_assessments",
    }
    found: list[Any] = []
    seen: set[int] = set()

    def visit(value: Any, depth: int) -> None:
        if depth > 4 or id(value) in seen:
            return
        seen.add(id(value))
        if all(hasattr(value, name) for name in required_methods):
            found.append(value)
        if depth == 4 or isinstance(value, (str, bytes, int, float, bool, type(None))):
            return
        try:
            children = vars(value).values()
        except TypeError:
            return
        for child in children:
            if type(child).__module__.startswith("nvda_desk.raw_signal_occurrence_truth"):
                visit(child, depth + 1)

    visit(owner, 0)
    return found


def test_default_postgresql_path_exposes_same_semantic_free_storage_protocol() -> None:
    owner = build_owner(postgres_dsn=_dsn())
    ports = _find_default_persistence_ports(owner)
    assert ports, "default PostgreSQL owner path hides its technical persistence port"
    forbidden = {
        "derive_relation",
        "decide_relation",
        "decide_outcome",
        "assess_outcome",
        "is_eligible",
        "classify",
    }
    for port in ports:
        assert not any(hasattr(port, name) for name in forbidden), type(port)


def test_persistence_proof_does_not_claim_cross_kind_atomicity_or_replay_sla() -> None:
    owner = build_owner(postgres_dsn=_dsn())
    for forbidden in (
        "cross_kind_atomic",
        "replay_equivalent",
        "rto",
        "rpo",
        "retention_duration",
        "recovery_deadline",
    ):
        assert not hasattr(owner, forbidden)
