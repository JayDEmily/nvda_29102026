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
from pathlib import Path
from typing import Any

import pytest
from tests.product.raw_signal._support import build_owner, required_symbol

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
mount --bind / /
mount -o remount,ro,bind /
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
        "--fork",
        "sh",
        "-c",
        script,
        "sh",
        sys.executable,
        str(PROBE),
    ]


def _probe_process(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    isolated_filesystem: bool = True,
    **extra: Any,
) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"action": action, "dsn": dsn, "token": token, **extra})
    workdir = tmp_path / f"{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT)])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["HOME"] = str(workdir)
    env["TMPDIR"] = str(workdir)
    env["XDG_DATA_HOME"] = str(workdir / "xdg-data")
    command = _isolated_command() if isolated_filesystem else [sys.executable, str(PROBE)]
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
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


def test_each_occurrence_and_assessment_is_independently_committed_and_exactly_readable(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("own-tx")

    policy_written = _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token)
    policy_read = _run_probe(tmp_path, "read_policy", dsn=dsn, token=token)
    assert policy_written["_pid"] != policy_read["_pid"]
    assert policy_read["record"] == policy_written["record"]

    capture_written = _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    capture_read = _run_probe(tmp_path, "read_capture", dsn=dsn, token=token)
    assert capture_written["_pid"] != capture_read["_pid"]
    assert capture_read["record"] == capture_written["record"]

    zero_written = _run_probe(tmp_path, "write_zero_assessment_only", dsn=dsn, token=token)
    zero_read = _run_probe(tmp_path, "read_assessment", dsn=dsn, token=token, which="zero")
    assert zero_written["_pid"] != zero_read["_pid"]
    assert zero_read["record"] == zero_written["record"]

    observation_written = _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token)
    observation_read = _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)
    assert observation_written["_pid"] != observation_read["_pid"]
    assert observation_read["record"] == observation_written["record"]

    faulted_observation = _run_probe(tmp_path, "fault_observation", dsn=dsn, token=token)
    assert faulted_observation["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_observation_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)["record"] == (
        observation_written["record"]
    )

    one_written = _run_probe(
        tmp_path, "write_relation_and_one_assessment", dsn=dsn, token=token
    )
    one_read = _run_probe(tmp_path, "read_assessment", dsn=dsn, token=token, which="one")
    assert one_written["_pid"] != one_read["_pid"]
    assert one_read["record"] == one_written["record"]

    faulted_assessment = _run_probe(tmp_path, "fault_assessment", dsn=dsn, token=token)
    assert faulted_assessment["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_assessment_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert _run_probe(tmp_path, "read_assessment", dsn=dsn, token=token, which="one")[
        "record"
    ] == one_written["record"]


def test_postgresql_contains_correlated_semantic_facts_and_is_required_for_fresh_read(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("semantic-source")
    _run_probe(tmp_path, "write_policy_only", dsn=dsn, token=token)
    _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=token)
    observation_written = _run_probe(tmp_path, "write_observation_only", dsn=dsn, token=token)

    hits = _postgres_fact_hits(dsn, _semantic_markers(token))
    assert all(count > 0 for count in hits.values()), hits

    fresh = _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)
    assert fresh["record"] == observation_written["record"]

    deleted = _delete_postgres_rows_containing_marker(dsn, f"native-record::{token}")
    assert deleted > 0, "no correlated PostgreSQL semantic row could be invalidated"
    after_semantic_delete = _probe_process(
        tmp_path,
        "read_observation",
        dsn=dsn,
        token=token,
    )
    if after_semantic_delete.returncode == 0:
        result = json.loads(
            [line for line in after_semantic_delete.stdout.splitlines() if line.strip()][-1]
        )
        assert result["record"] != observation_written["record"], (
            "fresh reader reproduced the exact semantic fact after its correlated PostgreSQL "
            "state was deleted; PostgreSQL participation is not proven to be the semantic source"
        )

    poisoned = _probe_process(
        tmp_path,
        "read_observation",
        dsn=_poisoned_dsn(dsn),
        token=token,
    )
    assert poisoned.returncode != 0, (
        "fresh semantic read unexpectedly succeeded when PostgreSQL was unavailable"
    )


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
    one = _run_probe(tmp_path, "write_relation_and_one_assessment", dsn=dsn, token=token)
    chain = _run_probe(tmp_path, "read_assessment_chain", dsn=dsn, token=token)
    assert chain["records"] == [zero["record"], one["record"]]


def test_restart_reconciliation_crosses_processes_and_yields_unknown_not_zero(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("restart")
    _run_probe(tmp_path, "write_policy_for_reconcile", dsn=dsn, token=token)
    reconciled = _run_probe(tmp_path, "reconcile", dsn=dsn, token=token)
    fresh = _run_probe(tmp_path, "read_reconcile", dsn=dsn, token=token)
    assert reconciled["_pid"] != fresh["_pid"]
    assert "unknown_not_established" in json.dumps(reconciled["assessment"])
    assert fresh["capture"] is not None
    assert fresh["assessment"] == reconciled["assessment"]


def test_public_owner_accepts_explicit_technical_persistence_port_injection() -> None:
    builder = required_symbol("create_owner")
    assert "persistence_port" in inspect.signature(builder).parameters


def test_production_persistence_mechanisms_contain_no_raw_signal_decision_logic() -> None:
    required_symbol("create_owner")
    candidates = [
        path
        for path in OWNER_PACKAGE.rglob("*.py")
        if any(
            token in path.stem.lower()
            for token in ("persist", "postgres", "repository", "adapter")
        )
    ]
    assert candidates, "production persistence/adapter implementation is not present"
    forbidden_literals = {
        "zero_received",
        "one_or_more_received",
        "unknown_not_established",
        "evidences_receipt_presence_only",
    }
    forbidden_names = {
        "derive_capture_receipt_evidence_relation",
        "derive_relation",
        "decide_relation",
        "decide_outcome",
        "assess_outcome",
        "eligibility_resolver",
        "classify_outcome",
    }
    for path in candidates:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        string_literals = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        names = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        } | {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        } | {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert not forbidden_literals.intersection(string_literals), path
        assert not forbidden_names.intersection(names), path


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
