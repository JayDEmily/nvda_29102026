from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

import pytest
from tests.product.raw_signal._support import build_owner

ROOT = Path(__file__).resolve().parents[3]
PROBE = ROOT / "tests/product/raw_signal/_process_probe.py"


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
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _probe_process(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"action": action, "dsn": dsn, "token": token})
    workdir = tmp_path / f"{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), str(ROOT)])
    env["HOME"] = str(workdir)
    env["TMPDIR"] = str(workdir)
    env["XDG_DATA_HOME"] = str(workdir / "xdg-data")
    return subprocess.run(
        [sys.executable, str(PROBE)],
        cwd=workdir,
        env=env,
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )


def _run_probe(tmp_path: Path, action: str, *, dsn: str, token: str) -> dict[str, Any]:
    completed = _probe_process(tmp_path, action, dsn=dsn, token=token)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    assert lines, "fresh-process probe produced no JSON result"
    return json.loads(lines[-1])


def _without_pid(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "_pid"}


def _user_row_count(dsn: str) -> int:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    total = 0
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
        for schema, table in tables:
            cursor.execute(
                sql.SQL("select count(*) from {}.{}").format(
                    sql.Identifier(schema), sql.Identifier(table)
                )
            )
            total += int(cursor.fetchone()[0])
    return total


def _poisoned_dsn(dsn: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    values = conninfo.conninfo_to_dict(dsn)
    values["dbname"] = f"nvda_missing_{uuid.uuid4().hex}"
    return conninfo.make_conninfo(**values)


def test_proof_environment_is_real_postgresql_17_9() -> None:
    psycopg = _psycopg()
    with psycopg.connect(_dsn()) as connection, connection.cursor() as cursor:
        cursor.execute("show server_version")
        version = cursor.fetchone()[0]
    assert version.startswith("17.9")


def test_public_factory_uses_same_semantic_owner_type_with_and_without_postgresql() -> None:
    assert type(build_owner()) is type(build_owner(postgres_dsn=_dsn()))


def test_committed_facts_cross_process_boundary_and_mutate_postgresql(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("core")
    before = _user_row_count(dsn)
    written = _run_probe(tmp_path, "write_core", dsn=dsn, token=token)
    after = _user_row_count(dsn)
    readback = _run_probe(tmp_path, "read_core", dsn=dsn, token=token)

    assert written["observation_id"] == f"observation-{token}"
    assert written["_pid"] != readback["_pid"]
    assert after > before
    assert _without_pid(readback) == {
        "capture": True,
        "observation": True,
        "observation_id": f"observation-{token}",
        "policy": True,
    }

    poisoned = _probe_process(
        tmp_path,
        "read_core",
        dsn=_poisoned_dsn(dsn),
        token=token,
    )
    assert poisoned.returncode != 0, (
        "fresh semantic read unexpectedly succeeded with deliberately invalid PostgreSQL DSN"
    )


def test_assessment_history_is_append_only_across_separate_processes(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("assessment")
    written = _run_probe(tmp_path, "write_assessment_chain", dsn=dsn, token=token)
    assert _without_pid(written) == {"one": "one_or_more_received", "zero": "zero_received"}

    chain = _run_probe(tmp_path, "read_assessment_chain", dsn=dsn, token=token)
    assert written["_pid"] != chain["_pid"]
    assert chain["ids"] == [
        f"assessment-zero-{token}",
        f"assessment-one-{token}",
    ]
    assert chain["outcomes"] == ["zero_received", "one_or_more_received"]
    assert chain["supersedes"] == [None, f"assessment-zero-{token}"]


def test_durable_retry_and_conflicting_reuse_cross_process_boundaries(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("retry")
    written = _run_probe(tmp_path, "write_core", dsn=dsn, token=token)
    retry = _run_probe(tmp_path, "retry_observation", dsn=dsn, token=token)
    conflict = _run_probe(tmp_path, "conflict_observation", dsn=dsn, token=token)
    assert retry["observation_id"] == f"observation-{token}"
    assert len({written["_pid"], retry["_pid"], conflict["_pid"]}) == 3
    assert _without_pid(conflict) == {"rejected": True}


def test_failed_commit_is_absent_from_postgresql_and_fresh_process(tmp_path: Path) -> None:
    dsn = _dsn()
    token = _token("fault")
    fault = _run_probe(tmp_path, "fault_write", dsn=dsn, token=token)
    fresh = _run_probe(tmp_path, "read_absent", dsn=dsn, token=token)
    assert fault["failed"] is True
    assert fault["_pid"] != fresh["_pid"]
    assert _without_pid(fresh) == {"absent": True}


def test_restart_reconciliation_crosses_processes_and_yields_unknown_not_zero(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("restart")
    _run_probe(tmp_path, "write_policy", dsn=dsn, token=token)
    reconciled = _run_probe(tmp_path, "reconcile", dsn=dsn, token=token)
    fresh = _run_probe(tmp_path, "read_reconcile", dsn=dsn, token=token)
    assert _without_pid(reconciled) == {"count": 1, "outcome": "unknown_not_established"}
    assert reconciled["_pid"] != fresh["_pid"]
    assert _without_pid(fresh) == {
        "assessment": True,
        "capture": True,
        "outcome": "unknown_not_established",
    }


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
