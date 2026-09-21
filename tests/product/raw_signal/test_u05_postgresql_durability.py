from __future__ import annotations

import ast
import contextlib
import functools
import importlib
import inspect
import json
import os
import select
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import is_dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    append_assessment,
    as_mapping,
    assessment_contract,
    build_owner,
    capture_contract,
    observation,
    policy,
    realise_capture,
    register_policy,
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


def _postgres_socket_dir(dsn: str) -> str:
    conninfo = importlib.import_module("psycopg.conninfo")
    values = conninfo.conninfo_to_dict(dsn)
    host = values.get("host")
    if not host or not host.startswith("/"):
        pytest.fail(
            "exclusive persistence proof requires a PostgreSQL Unix-domain socket DSN; "
            f"received host={host!r}"
        )
    return host


def _isolated_command(dsn: str, *, pid_namespace: bool = False) -> list[str]:
    unshare = shutil.which("unshare")
    if unshare is None:
        pytest.fail("unshare is required for the exclusive persistence proof boundary")
    socket_dir = _postgres_socket_dir(dsn)
    script = r"""
set -eu
ROOTFS="$(mktemp -d /tmp/nvda-proof-root.XXXXXX)"
mount -t tmpfs -o mode=0755 tmpfs "$ROOTFS"
for d in usr lib lib64 opt etc mnt/data tmp var/tmp dev dev/shm proc run home root; do
    mkdir -p "$ROOTFS/$d"
done
for d in /usr /lib /lib64 /opt /etc /mnt/data; do
    if [ -e "$d" ]; then
        mount --rbind "$d" "$ROOTFS$d"
        mount --make-rslave "$ROOTFS$d"
        findmnt -Rrn -o TARGET "$ROOTFS$d" | while IFS= read -r target; do
            mount -o remount,ro,bind "$target"
        done
    fi
done
mount -t tmpfs -o mode=1777 tmpfs "$ROOTFS/tmp"
mount -t tmpfs -o mode=1777 tmpfs "$ROOTFS/var/tmp"
mount -t tmpfs -o mode=1777 tmpfs "$ROOTFS/dev/shm"
mount -t tmpfs -o mode=0755 tmpfs "$ROOTFS/run"
for node in null zero random urandom; do
    : > "$ROOTFS/dev/$node"
    mount --bind "/dev/$node" "$ROOTFS/dev/$node"
    mount -o remount,ro,bind "$ROOTFS/dev/$node"
done
SOCKET_DIR="$3"
case "$SOCKET_DIR" in
    /mnt/data|/mnt/data/*)
        ;;
    *)
        mkdir -p "$ROOTFS$SOCKET_DIR"
        mount --bind "$SOCKET_DIR" "$ROOTFS$SOCKET_DIR"
        mount -o remount,ro,bind "$ROOTFS$SOCKET_DIR"
        ;;
esac
mkdir -p "$ROOTFS/run/proof-home" "$ROOTFS/run/proof-xdg" \
    "$ROOTFS/run/proof-tmp" "$ROOTFS/run/proof-work"
cat /proc/self/mountinfo > "$ROOTFS/run/proof-mountinfo"
export NVDA_PROOF_ROOTFS="$ROOTFS"
export NVDA_PROOF_PID_NAMESPACE="$4"
cd "$ROOTFS/run/proof-work"
if [ "$4" = "1" ]; then
    # Keep PID 1 as a proof supervisor. The Python writer runs as a non-init child so
    # SIGSTOP has ordinary semantics at the exact public-return boundary.
    chroot "$ROOTFS" "$1" "$2"
else
    exec chroot "$ROOTFS" "$1" "$2"
fi
"""
    command = [
        unshare,
        "--user",
        "--map-root-user",
        "--mount",
        "--net",
    ]
    if pid_namespace:
        command.append("--pid")
    command.extend(
        [
            "--fork",
            "sh",
            "-c",
            script,
            "sh",
            sys.executable,
            str(PROBE),
            socket_dir,
            "1" if pid_namespace else "0",
        ]
    )
    return command


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
    env["HOME"] = "/run/proof-home"
    env["TMPDIR"] = "/run/proof-tmp"
    env["XDG_DATA_HOME"] = "/run/proof-xdg"
    return env


def _json_transport_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return {"__nvda_proof_decimal__": str(value)}
    raise TypeError(f"proof transport cannot JSON-encode {type(value)!r}")


def _probe_process(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    isolated_filesystem: bool = True,
    **extra: Any,
) -> subprocess.CompletedProcess[str]:
    payload = (
        json.dumps(
            {"action": action, "dsn": dsn, "token": token, **extra}, default=_json_transport_default
        )
        + "\n"
    )
    workdir = tmp_path / f"{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    command = _isolated_command(dsn) if isolated_filesystem else [sys.executable, str(PROBE)]
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
        _isolated_command(dsn),
        cwd=ROOT,
        env=_probe_env(workdir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    payload = json.dumps({"action": action, "dsn": dsn, "token": token, "hold_open": True, **extra})
    process.stdin.write(payload + "\n")
    process.stdin.flush()
    first = process.stdout.readline().strip()
    if not first:
        stderr = process.stderr.read() if process.stderr is not None else ""
        raise AssertionError(f"hold-open probe produced no success result: {stderr}")
    result = json.loads(first)
    assert process.poll() is None, "writer exited before command-success visibility check"
    return process, result


def _spawn_return_boundary_probe(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    **extra: Any,
) -> subprocess.Popen[str]:
    """Start a PID-isolated public-return probe without consuming its return marker."""

    workdir = tmp_path / f"return-{action}-{uuid.uuid4().hex}"
    workdir.mkdir()
    process = subprocess.Popen(
        _isolated_command(dsn, pid_namespace=True),
        cwd=ROOT,
        env=_probe_env(workdir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write(
        json.dumps(
            {"action": action, "dsn": dsn, "token": token, **extra},
            default=_json_transport_default,
        )
        + "\n"
    )
    process.stdin.flush()
    return process


def _read_return_boundary_marker(
    process: subprocess.Popen[str], *, timeout: float = 10.0
) -> dict[str, Any]:
    assert process.stdout is not None
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = max(0.0, deadline - time.monotonic())
        readable, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))
        if readable:
            line = process.stdout.readline().strip()
            if not line:
                continue
            candidate = json.loads(line)
            if candidate.get("event") == "public_method_return":
                return candidate
        if process.poll() is not None:
            stderr = process.stderr.read() if process.stderr is not None else ""
            raise AssertionError(f"return-boundary probe exited before marker: {stderr}")
    stderr = ""
    if process.poll() is not None and process.stderr is not None:
        stderr = process.stderr.read()
    raise AssertionError(f"return-boundary probe produced no marker before timeout: {stderr}")


def _start_return_boundary_probe(
    tmp_path: Path,
    action: str,
    *,
    dsn: str,
    token: str,
    **extra: Any,
) -> tuple[subprocess.Popen[str], dict[str, Any]]:
    """Pause the child at the proof-owned profile hook for the public method return event."""

    process = _spawn_return_boundary_probe(tmp_path, action, dsn=dsn, token=token, **extra)
    marker = _read_return_boundary_marker(process)
    assert process.poll() is None, "writer exited before public-return boundary inspection"
    namespace_pid = marker.get("_pid")
    assert isinstance(namespace_pid, int), marker
    _wait_for_stopped_process_tree(process, namespace_pid)
    return process, marker


def _direct_child_pids(parent_pid: int) -> list[int]:
    """Return host-visible children by PPid, including across a nested PID namespace."""

    children: list[int] = []
    for proc_dir in Path("/proc").iterdir():
        if not proc_dir.name.isdigit():
            continue
        try:
            status = (proc_dir / "status").read_text(encoding="utf-8")
            ppid_line = next(line for line in status.splitlines() if line.startswith("PPid:"))
        except (FileNotFoundError, ProcessLookupError, StopIteration, PermissionError):
            continue
        if int(ppid_line.split()[1]) == parent_pid:
            children.append(int(proc_dir.name))
    return children


def _descendant_pids(root_pid: int) -> list[int]:
    """Return all live descendants of a host-visible process, depth first."""

    found: list[int] = []
    pending = [root_pid]
    seen = {root_pid}
    while pending:
        parent = pending.pop()
        for child in _direct_child_pids(parent):
            if child in seen:
                continue
            seen.add(child)
            found.append(child)
            pending.append(child)
    return found


def _process_is_stopped(pid: int) -> bool:
    try:
        status = Path(f"/proc/{pid}/status").read_text(encoding="utf-8")
    except FileNotFoundError:
        return False
    state = next((line for line in status.splitlines() if line.startswith("State:")), "")
    return "T (stopped)" in state or "t (tracing stop)" in state


def _namespace_pid(pid: int) -> int | None:
    try:
        status = Path(f"/proc/{pid}/status").read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    nspid = next((line for line in status.splitlines() if line.startswith("NSpid:")), "")
    values = nspid.split()[1:]
    return int(values[-1]) if values else None


def _writer_pid(process: subprocess.Popen[str], namespace_pid: int) -> int | None:
    for pid in _descendant_pids(process.pid):
        if _namespace_pid(pid) == namespace_pid:
            return pid
    return None


def _writer_process_tree(process: subprocess.Popen[str], namespace_pid: int) -> list[int]:
    writer = _writer_pid(process, namespace_pid)
    if writer is None:
        return []
    return [writer, *_descendant_pids(writer)]


def _wait_for_stopped_process_tree(
    process: subprocess.Popen[str], namespace_pid: int, *, timeout: float = 5.0
) -> list[int]:
    deadline = time.monotonic() + timeout
    last_tree: list[int] = []
    while time.monotonic() < deadline:
        last_tree = _writer_process_tree(process, namespace_pid)
        if last_tree and all(_process_is_stopped(pid) for pid in last_tree):
            return last_tree
        if process.poll() is not None:
            pytest.fail("return-boundary writer tree exited before it could be frozen")
        time.sleep(0.01)
    states = {pid: _process_is_stopped(pid) for pid in last_tree}
    pytest.fail(
        "return-boundary writer tree did not enter whole-tree SIGSTOP: "
        f"namespace_pid={namespace_pid}, tree={last_tree}, stopped={states}"
    )


def _signal_writer_tree(
    process: subprocess.Popen[str], namespace_pid: int, sig: signal.Signals
) -> None:
    for pid in reversed(_writer_process_tree(process, namespace_pid)):
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, sig)


def _release_return_boundary_probe(
    process: subprocess.Popen[str], marker: dict[str, Any]
) -> dict[str, Any]:
    namespace_pid = marker.get("_pid")
    assert isinstance(namespace_pid, int), marker
    _signal_writer_tree(process, namespace_pid, signal.SIGCONT)
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode == 0, stdout + stderr
    lines = [line for line in stdout.splitlines() if line.strip()]
    assert lines, "return-boundary probe produced no post-release record"
    return json.loads(lines[-1])


def _kill_return_boundary_probe(process: subprocess.Popen[str], marker: dict[str, Any]) -> None:
    namespace_pid = marker.get("_pid")
    assert isinstance(namespace_pid, int), marker
    _signal_writer_tree(process, namespace_pid, signal.SIGKILL)
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode is not None
    assert process.returncode != 0, stdout + stderr


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


def _set_synchronous_standby_names(dsn: str, value: str | None) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    admin_dsn = _admin_dsn(dsn)
    with psycopg.connect(admin_dsn, autocommit=True) as connection, connection.cursor() as cursor:
        if value is None:
            cursor.execute("alter system reset synchronous_standby_names")
        else:
            cursor.execute(
                sql.SQL("alter system set synchronous_standby_names = {}").format(
                    sql.Literal(value)
                )
            )
        cursor.execute("select pg_reload_conf()")
        assert cursor.fetchone()[0] is True


def _current_synchronous_standby_names(dsn: str) -> str:
    psycopg = _psycopg()
    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute("show synchronous_standby_names")
        return str(cursor.fetchone()[0])


def _wait_for_synchronous_standby_setting(dsn: str, expected: str, *, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    observed = ""
    while time.monotonic() < deadline:
        observed = _current_synchronous_standby_names(dsn)
        if observed == expected:
            return
        time.sleep(0.02)
    pytest.fail(
        f"PostgreSQL did not reload synchronous_standby_names={expected!r}; observed {observed!r}"
    )


def _backend_wait_event(dsn: str, application_name: str) -> tuple[str | None, str | None] | None:
    psycopg = _psycopg()
    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            """
            select wait_event_type, wait_event
            from pg_stat_activity
            where application_name = %s and pid <> pg_backend_pid()
            """,
            (application_name,),
        )
        row = cursor.fetchone()
    if row is None:
        return None
    return row[0], row[1]


def _wait_for_sync_rep_without_public_return(
    process: subprocess.Popen[str],
    *,
    dsn: str,
    application_name: str,
    timeout: float = 10.0,
) -> None:
    """Observe server-side SyncRep wait while proving the public return marker is absent."""

    assert process.stdout is not None
    deadline = time.monotonic() + timeout
    last_wait: tuple[str | None, str | None] | None = None
    while time.monotonic() < deadline:
        readable, _, _ = select.select([process.stdout], [], [], 0)
        if readable:
            line = process.stdout.readline().strip()
            raise AssertionError(
                "public method returned before PostgreSQL COMMIT acknowledgement; "
                f"marker={line!r}, last_wait={last_wait!r}"
            )
        if process.poll() is not None:
            stderr = process.stderr.read() if process.stderr is not None else ""
            raise AssertionError(
                f"commit-barrier writer exited before server SyncRep wait: {stderr}"
            )
        last_wait = _backend_wait_event(dsn, application_name)
        if last_wait == ("IPC", "SyncRep"):
            readable, _, _ = select.select([process.stdout], [], [], 0.1)
            assert not readable, (
                "public method return became visible while PostgreSQL backend was still "
                "waiting for synchronous commit acknowledgement",
                last_wait,
            )
            return
        time.sleep(0.01)
    pytest.fail(
        "writer backend did not enter PostgreSQL SyncRep wait under proof commit barrier; "
        f"last_wait={last_wait!r}"
    )


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
    if value is None or isinstance(value, (str, bool)):
        return value
    if type(value) is int:
        return {"__numeric_type__": "int", "value": value}
    if type(value) is float:
        return {"__numeric_type__": "float", "value": repr(value)}
    if isinstance(value, Decimal):
        decimal_tuple = value.as_tuple()
        return {
            "__numeric_type__": "Decimal",
            "value": str(value),
            "tuple": [
                decimal_tuple.sign,
                list(decimal_tuple.digits),
                decimal_tuple.exponent,
            ],
        }
    if isinstance(value, dict):
        return {
            str(k): _canonical(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))
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
        "raw_signal_catalogue_ids": ["R033", "R034"],
        "native_record": {
            "Bid Size": 0,
            "Bid Price": 123.45678901234567,
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
        raw_signal_catalogue_ids=tuple(facts["raw_signal_catalogue_ids"]),
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


def test_postgresql_sync_commit_barrier_itself_waits_for_server_acknowledgement() -> None:
    """Canary the proof-owned server barrier independently of absent product symbols."""

    dsn = _dsn()
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    table = f"nvda_sync_barrier_{uuid.uuid4().hex}"
    application_name = f"nvda-proof-sync-canary-{uuid.uuid4().hex}"
    writer_dsn = _dsn_with_application_name(dsn, application_name)
    original_setting = _current_synchronous_standby_names(dsn)
    barrier_name = f"nvda_proof_no_standby_{uuid.uuid4().hex}"
    returned = threading.Event()
    errors: list[BaseException] = []
    thread: threading.Thread | None = None
    barrier_active = False

    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            sql.SQL("create table {} (value text not null)").format(sql.Identifier(table))
        )

    def writer() -> None:
        try:
            with psycopg.connect(writer_dsn) as connection, connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("insert into {} (value) values (%s)").format(sql.Identifier(table)),
                    ("commit-ack-canary",),
                )
                connection.commit()
        except BaseException as exc:  # pragma: no cover - surfaced in parent assertion
            errors.append(exc)
        finally:
            returned.set()

    try:
        _set_synchronous_standby_names(dsn, f"FIRST 1 ({barrier_name})")
        _wait_for_synchronous_standby_setting(dsn, f"FIRST 1 ({barrier_name})")
        barrier_active = True
        thread = threading.Thread(target=writer, name="nvda-sync-commit-canary", daemon=True)
        thread.start()

        deadline = time.monotonic() + 10.0
        observed: tuple[str | None, str | None] | None = None
        while time.monotonic() < deadline:
            assert not returned.is_set(), (
                "client observed commit completion before the server-side SyncRep barrier",
                observed,
                errors,
            )
            observed = _backend_wait_event(dsn, application_name)
            if observed == ("IPC", "SyncRep"):
                break
            time.sleep(0.01)
        assert observed == ("IPC", "SyncRep"), observed
        assert not returned.is_set()

        _set_synchronous_standby_names(dsn, original_setting or None)
        _wait_for_synchronous_standby_setting(dsn, original_setting)
        barrier_active = False
        thread.join(timeout=10)
        assert not thread.is_alive()
        assert not errors, errors
        assert returned.is_set()

        with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
            cursor.execute(sql.SQL("select value from {}").format(sql.Identifier(table)))
            assert cursor.fetchall() == [("commit-ack-canary",)]
    finally:
        if barrier_active:
            _set_synchronous_standby_names(dsn, original_setting or None)
            _wait_for_synchronous_standby_setting(dsn, original_setting)
        if thread is not None and thread.is_alive():
            thread.join(timeout=10)
        with (
            psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute(sql.SQL("drop table if exists {}").format(sql.Identifier(table)))


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
    boundary = _without_pid(result)
    assert boundary["ephemeral_write_ok"] is True
    assert boundary["host_write_blocked"] is True
    assert boundary["writable_mounts"], "exclusive process root must expose ephemeral mounts"
    assert {item["filesystem"] for item in boundary["writable_mounts"]} <= {"tmpfs", "proc"}
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

        assert (
            _run_probe(tmp_path, "read_policy", dsn=clone_dsn, token=token)["record"]
            == (expected["policy"])
        )
        assert (
            _run_probe(tmp_path, "read_capture", dsn=clone_dsn, token=token)["record"]
            == (expected["capture"])
        )
        assert (
            _run_probe(tmp_path, "read_observation", dsn=clone_dsn, token=token)["record"]
            == (expected["observation"])
        )
        chain = _run_probe(tmp_path, "read_assessment_chain", dsn=clone_dsn, token=token)
        assert chain["records"] == [expected["zero"], expected["one"]]

        source_read = _probe_process(tmp_path, "read_observation", dsn=source_dsn, token=token)
        assert source_read.returncode != 0
    finally:
        _drop_database(admin_dsn, clone_db)
        _drop_database(admin_dsn, source_db)


def test_public_return_barrier_stops_separate_session_descendant_process(
    tmp_path: Path,
) -> None:
    process, marker = _start_return_boundary_probe(
        tmp_path,
        "boundary_descendant_canary",
        dsn=_dsn(),
        token=_token("descendant-canary"),
    )
    try:
        namespace_pid = marker.get("_pid")
        assert isinstance(namespace_pid, int), marker
        descendants = _wait_for_stopped_process_tree(process, namespace_pid)
        assert len(descendants) >= 2, (
            "canary requires both the PID-namespace probe and its separate-session descendant",
            descendants,
        )
        assert process.stdout is not None
        readable, _, _ = select.select([process.stdout], [], [], 0.25)
        assert not readable, (
            "separate-session descendant emitted output after the public-return boundary; "
            "whole execution tree was not frozen"
        )
        result = _release_return_boundary_probe(process, marker)
        assert result["value"] == "returned"
    finally:
        if process.poll() is None:
            _kill_return_boundary_probe(process, marker)


def test_public_success_return_requires_postgresql_commit_acknowledgement(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    token = _token("commit-ack")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    # Warm the production PostgreSQL path before installing the server-side barrier so schema
    # bootstrap or unrelated first-use work cannot satisfy this discriminator.
    _run_probe(
        tmp_path,
        "write_observation_only",
        dsn=dsn,
        token=_token("commit-ack-warm"),
        facts=_authoritative_facts(),
    )

    original_setting = _current_synchronous_standby_names(dsn)
    barrier_name = f"nvda_proof_no_standby_{uuid.uuid4().hex}"
    application_name = f"nvda-proof-commit-ack-{uuid.uuid4().hex}"
    writer_dsn = _dsn_with_application_name(dsn, application_name)
    process: subprocess.Popen[str] | None = None
    marker: dict[str, Any] | None = None
    barrier_active = False
    try:
        _set_synchronous_standby_names(dsn, f"FIRST 1 ({barrier_name})")
        _wait_for_synchronous_standby_setting(dsn, f"FIRST 1 ({barrier_name})")
        barrier_active = True

        process = _spawn_return_boundary_probe(
            tmp_path,
            "boundary_write_observation",
            dsn=writer_dsn,
            token=token,
            facts=facts,
        )
        _wait_for_sync_rep_without_public_return(
            process, dsn=dsn, application_name=application_name
        )

        # Release server-side COMMIT, then and only then may the profiled public return appear.
        _set_synchronous_standby_names(dsn, original_setting or None)
        _wait_for_synchronous_standby_setting(dsn, original_setting)
        barrier_active = False
        marker = _read_return_boundary_marker(process)
        namespace_pid = marker.get("_pid")
        assert isinstance(namespace_pid, int), marker
        _wait_for_stopped_process_tree(process, namespace_pid)
        _assert_no_open_writer_transaction(dsn, application_name)
        fresh = _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)
        assert fresh["record"] == expected["observation"]
        result = _release_return_boundary_probe(process, marker)
        assert result["record"] == expected["observation"]
    finally:
        if barrier_active:
            _set_synchronous_standby_names(dsn, original_setting or None)
            _wait_for_synchronous_standby_setting(dsn, original_setting)
        if process is not None and process.poll() is None:
            if marker is not None:
                _kill_return_boundary_probe(process, marker)
            else:
                process.kill()
                process.communicate(timeout=10)


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
        process, marker = _start_return_boundary_probe(
            tmp_path,
            action,
            dsn=dsn,
            token=token,
            **(write_extra or {}),
        )
        _kill_return_boundary_probe(process, marker)
        fresh = _run_probe(
            tmp_path,
            read_action,
            dsn=dsn,
            token=token,
            **(read_extra or {}),
        )
        assert fresh["record"] == expected[expected_key]

    kill_then_read(
        "boundary_write_policy",
        "read_policy",
        "policy",
        write_extra={"facts": facts},
    )
    kill_then_read("boundary_write_capture", "read_capture", "capture")
    kill_then_read(
        "boundary_write_zero_assessment",
        "read_assessment",
        "zero",
        read_extra={"which": "zero"},
    )
    kill_then_read(
        "boundary_write_observation",
        "read_observation",
        "observation",
        write_extra={"facts": facts},
    )
    _run_probe(tmp_path, "derive_relation_only", dsn=dsn, token=token)
    kill_then_read(
        "boundary_write_one_assessment",
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
        process, marker = _start_return_boundary_probe(
            tmp_path,
            action,
            dsn=writer_dsn,
            token=token,
            **(write_extra or {}),
        )
        assert marker["event"] == "public_method_return"
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
        assert process.poll() is None, "writer resumed before proof released the return boundary"
        result = _release_return_boundary_probe(process, marker)
        assert result["record"] == expected[expected_key]
        return result

    hold_and_read(
        "boundary_write_policy",
        "read_policy",
        "policy",
        write_extra={"facts": facts},
    )
    hold_and_read("boundary_write_capture", "read_capture", "capture")
    hold_and_read(
        "boundary_write_zero_assessment",
        "read_assessment",
        "zero",
        read_extra={"which": "zero"},
    )
    hold_and_read(
        "boundary_write_observation",
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
        "boundary_write_one_assessment",
        "read_assessment",
        "one",
        read_extra={"which": "one"},
    )

    faulted_capture = _run_probe(tmp_path, "fault_capture", dsn=dsn, token=token)
    assert faulted_capture["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_capture_absent", dsn=dsn, token=token)
    ) == {"absent": True}

    faulted_observation = _run_probe(tmp_path, "fault_observation", dsn=dsn, token=token)
    assert faulted_observation["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_observation_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert (
        _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)["record"]
        == (expected["observation"])
    )

    faulted_assessment = _run_probe(tmp_path, "fault_assessment", dsn=dsn, token=token)
    assert faulted_assessment["failed"] is True
    assert _without_pid(
        _run_probe(tmp_path, "read_fault_assessment_absent", dsn=dsn, token=token)
    ) == {"absent": True}
    assert (
        _run_probe(tmp_path, "read_assessment", dsn=dsn, token=token, which="one")["record"]
        == expected["one"]
    )


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


@pytest.mark.parametrize(
    ("catalogue_id", "field", "value", "units"),
    [
        ("R038", "Last Size", Decimal("0.00100"), "contracts/shares"),
        ("R084", "Bid Option Computation.impliedVolatility", -0.000000000123456789, "volatility"),
        ("R246", "DGS3MO", -0.375, "Percent"),
    ],
)
def test_postgresql_restart_preserves_catalogue_id_numeric_sign_precision_type_and_null(
    tmp_path: Path,
    catalogue_id: str,
    field: str,
    value: float | Decimal,
    units: str,
) -> None:
    token = _token(f"numeric-{catalogue_id.lower()}")
    facts = _authoritative_facts()
    facts.update(
        {
            "raw_signal_catalogue_ids": [catalogue_id],
            "native_record": {field: value, "Provider Null": None},
            "native_units": units,
        }
    )
    if catalogue_id == "R246":
        facts.update(
            {
                "source_temporal_kind": "date_only",
                "source_timestamp_raw": "2026-09-20",
                "source_timezone_native": None,
            }
        )
    written = _run_probe(tmp_path, "write_observation_only", dsn=_dsn(), token=token, facts=facts)
    reread = _run_probe(tmp_path, "read_observation", dsn=_dsn(), token=token)
    expected = _expected_records(token, facts)["observation"]
    assert written["record"] == expected
    assert reread["record"] == expected
    expected_numeric = _canonical(value)
    assert reread["record"]["native_record"][field] == expected_numeric
    if isinstance(value, Decimal):
        assert expected_numeric == {
            "__numeric_type__": "Decimal",
            "value": "0.00100",
            "tuple": [0, [1, 0, 0], -5],
        }
    assert reread["record"]["native_record"]["Provider Null"] is None


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
    zero = _run_probe(tmp_path, "write_zero_assessment_only", dsn=dsn, token=token)
    zero_retry = _run_probe(tmp_path, "retry_zero_assessment", dsn=dsn, token=token)
    assert zero_retry["record"] == zero["record"]
    assert _without_pid(_run_probe(tmp_path, "conflict_zero_assessment", dsn=dsn, token=token)) == {
        "rejected": True
    }
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
    assert immediate["record"]["supersedes_assessment_ref"]["value"] == (f"assessment-one::{token}")
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

    other_scope = _run_probe(
        tmp_path,
        "admit_low_sequence_other_scope",
        dsn=dsn,
        token=token,
    )
    assert other_scope["record"]["ingestion_sequence"] == 1

    assert _without_pid(
        _run_probe(tmp_path, "admit_low_sequence_same_scope", dsn=dsn, token=token)
    ) == {"rejected": True}
    next_same_scope = _run_probe(
        tmp_path,
        "admit_next_sequence_same_scope",
        dsn=dsn,
        token=token,
    )
    assert next_same_scope["record"]["ingestion_sequence"] == 43


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


_STORAGE_PROTOCOL_BOUND_ARITY = {
    "append_policy": 1,
    "get_policy": 2,
    "append_capture": 1,
    "get_capture": 1,
    "append_observation": 1,
    "get_observation": 1,
    "append_assessment": 1,
    "get_assessment": 1,
    "list_assessments": 1,
}


class _RecordOnlyPersistenceProxy:
    """Expose only the admitted record protocol while forwarding to real PostgreSQL storage."""

    def __init__(self, inner: Any) -> None:
        self._inner = inner
        self._calls: list[str] = []

    @property
    def calls(self) -> tuple[str, ...]:
        return tuple(self._calls)

    def clear_calls(self) -> None:
        self._calls.clear()

    def append_policy(self, value: Any) -> Any:
        self._calls.append("append_policy")
        return self._inner.append_policy(value)

    def get_policy(self, policy_id: Any, version: int) -> Any:
        self._calls.append("get_policy")
        return self._inner.get_policy(policy_id, version)

    def append_capture(self, value: Any) -> Any:
        self._calls.append("append_capture")
        return self._inner.append_capture(value)

    def get_capture(self, capture_id: Any) -> Any:
        self._calls.append("get_capture")
        return self._inner.get_capture(capture_id)

    def append_observation(self, value: Any) -> Any:
        self._calls.append("append_observation")
        return self._inner.append_observation(value)

    def get_observation(self, observation_id: Any) -> Any:
        self._calls.append("get_observation")
        return self._inner.get_observation(observation_id)

    def append_assessment(self, value: Any) -> Any:
        self._calls.append("append_assessment")
        return self._inner.append_assessment(value)

    def get_assessment(self, assessment_id: Any) -> Any:
        self._calls.append("get_assessment")
        return self._inner.get_assessment(assessment_id)

    def list_assessments(self, capture_id: Any) -> Any:
        self._calls.append("list_assessments")
        return self._inner.list_assessments(capture_id)


def _rewire_production_graph_reference(root: Any, target: Any, replacement: Any) -> int:
    """Replace the concrete adapter while rejecting cached private semantic capabilities."""

    replaced = 0
    seen: set[int] = set()

    def bound_target_method(value: Any) -> str | None:
        if inspect.ismethod(value) and value.__self__ is target:
            return str(value.__name__)
        return None

    def function_captures_forbidden_target(value: Any) -> bool:
        closure = getattr(value, "__closure__", None)
        if not closure:
            return False
        for cell in closure:
            try:
                captured = cell.cell_contents
            except ValueError:
                continue
            if captured is target:
                return True
            method_name = bound_target_method(captured)
            if method_name is not None and method_name not in _STORAGE_PROTOCOL_BOUND_ARITY:
                return True
        return False

    def rewrite_child(child: Any) -> tuple[Any, bool]:
        nonlocal replaced
        if child is target:
            replaced += 1
            return replacement, True

        method_name = bound_target_method(child)
        if method_name is not None:
            assert method_name in _STORAGE_PROTOCOL_BOUND_ARITY, (
                "owner cached a private PostgreSQL adapter capability",
                method_name,
            )
            replaced += 1
            return getattr(replacement, method_name), True

        if isinstance(child, functools.partial):
            partial_method = bound_target_method(child.func)
            assert child.func is not target, "owner partial captures concrete PostgreSQL adapter"
            assert all(item is not target for item in child.args), (
                "owner partial captures concrete PostgreSQL adapter",
                child,
            )
            assert all(item is not target for item in (child.keywords or {}).values()), (
                "owner partial captures concrete PostgreSQL adapter",
                child,
            )
            if partial_method is not None:
                assert partial_method in _STORAGE_PROTOCOL_BOUND_ARITY, (
                    "owner cached a private PostgreSQL adapter capability",
                    partial_method,
                )
                replaced += 1
                return (
                    functools.partial(
                        getattr(replacement, partial_method),
                        *child.args,
                        **(child.keywords or {}),
                    ),
                    True,
                )

        assert not function_captures_forbidden_target(child), (
            "owner closure captures concrete/private PostgreSQL adapter capability",
            child,
        )
        return child, False

    def visit(value: Any) -> None:
        if value is replacement or id(value) in seen:
            return
        seen.add(id(value))

        if isinstance(value, list):
            for index, child in enumerate(tuple(value)):
                new_child, changed = rewrite_child(child)
                if changed:
                    value[index] = new_child
                else:
                    visit(child)
            return
        if isinstance(value, dict):
            for key, child in tuple(value.items()):
                new_child, changed = rewrite_child(child)
                if changed:
                    value[key] = new_child
                else:
                    visit(child)
            return
        if isinstance(value, tuple):
            for child in value:
                assert child is not target, "immutable owner tuple captures concrete adapter"
                method_name = bound_target_method(child)
                assert method_name is None or method_name in _STORAGE_PROTOCOL_BOUND_ARITY, (
                    "immutable owner tuple captures private adapter capability",
                    method_name,
                )
                assert not function_captures_forbidden_target(child)
            return

        try:
            items = list(vars(value).items())
        except TypeError:
            return
        for name, child in items:
            new_child, changed = rewrite_child(child)
            if changed:
                object.__setattr__(value, name, new_child)
                continue
            if type(child).__module__.startswith("nvda_desk.raw_signal_occurrence_truth"):
                visit(child)

    visit(root)
    return replaced


def _production_graph_contains_identity(root: Any, target: Any) -> bool:
    seen: set[int] = set()

    def visit(value: Any) -> bool:
        if id(value) in seen:
            return False
        seen.add(id(value))
        try:
            children = list(vars(value).values())
        except TypeError:
            return False
        for child in children:
            if child is target:
                return True
            if type(child).__module__.startswith("nvda_desk.raw_signal_occurrence_truth") and visit(
                child
            ):
                return True
        return False

    return visit(root)


def test_record_only_proxy_rewrite_rejects_cached_private_adapter_capability() -> None:
    """Canary the exact T009-F002 escape before exercising the production owner graph."""

    class AdapterCanary:
        def _semantic_decision(self) -> bool:
            return True

    class OwnerCanary:
        def __init__(self, adapter: AdapterCanary) -> None:
            self._port = adapter
            self._cached_private = adapter._semantic_decision

    adapter = AdapterCanary()
    owner = OwnerCanary(adapter)
    proxy = _RecordOnlyPersistenceProxy(adapter)
    with pytest.raises(AssertionError, match="private PostgreSQL adapter capability"):
        _rewire_production_graph_reference(owner, adapter, proxy)


def test_default_postgresql_path_exposes_exact_record_only_storage_protocol() -> None:
    owner = build_owner(postgres_dsn=_dsn())
    ports = _find_default_persistence_ports(owner)
    assert ports, "default PostgreSQL owner path hides its technical persistence port"
    for port in ports:
        public_callables = {
            name for name in dir(port) if not name.startswith("_") and callable(getattr(port, name))
        }
        assert public_callables == set(_STORAGE_PROTOCOL_BOUND_ARITY), (
            type(port),
            public_callables,
        )
        for name, arity in _STORAGE_PROTOCOL_BOUND_ARITY.items():
            signature = inspect.signature(getattr(port, name))
            parameters = tuple(signature.parameters.values())
            assert len(parameters) == arity, (type(port), name, signature)
            assert all(
                parameter.kind
                not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                for parameter in parameters
            ), (type(port), name, signature)


def test_default_postgresql_storage_port_preserves_owner_decided_assessment_without_rederiving(
    tmp_path: Path,
) -> None:
    del tmp_path  # signature keeps this proof visibly in the real-PostgreSQL family
    token = _token("storage-only")
    owner = build_owner(postgres_dsn=_dsn(), eligibility_resolver=lambda _o, _p: True)
    stored_policy = register_policy(
        owner,
        policy(
            scope_policy_id=f"scope::{token}",
            eligibility_policy_ref=f"eligibility::{token}",
        ),
    )
    capture = realise_capture(
        owner,
        scope_policy_ref=f"{stored_policy.scope_policy_id}@{stored_policy.scope_policy_version}",
        capture_occurrence_id=f"capture::{token}",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    admit_observation(
        owner,
        observation(
            observation_occurrence_id=f"observation::{token}",
            delivery_artifact_ref=f"delivery::{token}",
            source_provider=f"provider::{token}",
            ingestion_sequence_scope=f"collector::{token}",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
        ),
    )

    # This canary deliberately supplies storage with a complete semantic assessment record whose
    # outcome disagrees with what an owner would derive from the visible eligible observation.
    # A technical storage translator must preserve that already-decided field exactly rather than
    # inspecting observations/eligibility and choosing Raw Signal meaning itself.
    canary = assessment_contract(
        assessment_occurrence_id=f"assessment-storage-canary::{token}",
        capture_occurrence_ref=capture.capture_occurrence_id,
        outcome="zero_received",
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    ports = _find_default_persistence_ports(owner)
    assert len(ports) == 1, "proof requires one inspectable default PostgreSQL storage protocol"
    port = ports[0]
    stored = port.append_assessment(canary)
    reread = port.get_assessment(canary.assessment_occurrence_id)
    assert stored == canary
    assert reread == canary
    assert reread.outcome == "zero_received"

    # Discard the entire owner/adapter object graph and read the same record through a newly
    # constructed default PostgreSQL storage port. This prevents a technically named adapter
    # from returning the owner-decided canary from process memory while persisting a re-derived
    # outcome underneath it.
    fresh_owner = build_owner(postgres_dsn=_dsn(), eligibility_resolver=lambda _o, _p: False)
    fresh_ports = _find_default_persistence_ports(fresh_owner)
    assert len(fresh_ports) == 1
    fresh = fresh_ports[0].get_assessment(canary.assessment_occurrence_id)
    assert fresh == canary
    assert fresh.outcome == "zero_received"


def test_default_postgresql_storage_is_invariant_under_opposing_eligibility_authority(
    tmp_path: Path,
) -> None:
    del tmp_path
    base_dsn = _dsn()
    admin_dsn = _admin_dsn(base_dsn)
    suffix = uuid.uuid4().hex[:12]
    source_db = f"nvda_i9_src_{suffix}"
    true_db = f"nvda_i9_true_{suffix}"
    false_db = f"nvda_i9_false_{suffix}"
    source_dsn = _dsn_with_database(base_dsn, source_db)
    true_dsn = _dsn_with_database(base_dsn, true_db)
    false_dsn = _dsn_with_database(base_dsn, false_db)
    token = _token("eligibility-invariance")
    facts = _authoritative_facts()

    _create_database(admin_dsn, source_db)
    try:
        source_owner = build_owner(
            postgres_dsn=source_dsn, eligibility_resolver=lambda _o, _p: True
        )
        stored_policy = register_policy(
            source_owner,
            policy(
                scope_policy_id=f"scope::{token}",
                eligibility_policy_ref=facts["eligibility_policy_ref"],
            ),
        )
        stored_capture = realise_capture(
            source_owner,
            scope_policy_ref=f"scope::{token}@1",
            capture_occurrence_id=f"capture::{token}",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )
        stored_observation = admit_observation(
            source_owner,
            observation(
                observation_occurrence_id=f"observation::{token}",
                delivery_artifact_ref=facts["delivery_artifact_ref"],
                source_provider=facts["source_provider"],
                raw_signal_catalogue_ids=tuple(facts["raw_signal_catalogue_ids"]),
                native_identifier=facts["native_identifier"],
                native_record=facts["native_record"],
                native_units=facts["native_units"],
                received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
                ingestion_sequence=41,
                ingestion_sequence_scope=facts["ingestion_sequence_scope"],
            ),
        )
        _terminate_database_connections(admin_dsn, source_db)
        _create_database(admin_dsn, true_db, template=source_db)
        _create_database(admin_dsn, false_db, template=source_db)

        true_owner = build_owner(postgres_dsn=true_dsn, eligibility_resolver=lambda _o, _p: True)
        false_owner = build_owner(postgres_dsn=false_dsn, eligibility_resolver=lambda _o, _p: False)
        true_ports = _find_default_persistence_ports(true_owner)
        false_ports = _find_default_persistence_ports(false_owner)
        assert len(true_ports) == len(false_ports) == 1
        true_concrete_port = true_ports[0]
        false_concrete_port = false_ports[0]
        true_proxy = _RecordOnlyPersistenceProxy(true_concrete_port)
        false_proxy = _RecordOnlyPersistenceProxy(false_concrete_port)
        assert _rewire_production_graph_reference(true_owner, true_concrete_port, true_proxy) > 0
        assert _rewire_production_graph_reference(false_owner, false_concrete_port, false_proxy) > 0
        assert not _production_graph_contains_identity(true_owner, true_concrete_port)
        assert not _production_graph_contains_identity(false_owner, false_concrete_port)

        def storage_state(port: Any) -> dict[str, Any]:
            return {
                "policy": _canonical(
                    port.get_policy(
                        stored_policy.scope_policy_id, stored_policy.scope_policy_version
                    )
                ),
                "capture": _canonical(port.get_capture(stored_capture.capture_occurrence_id)),
                "observation": _canonical(
                    port.get_observation(stored_observation.observation_occurrence_id)
                ),
            }

        before_true = storage_state(true_proxy)
        before_false = storage_state(false_proxy)
        assert before_true == before_false
        true_proxy.clear_calls()
        false_proxy.clear_calls()

        true_relation = true_owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=stored_observation.observation_occurrence_id,
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            scope_policy_ref=stored_capture.scope_policy_ref,
        )
        false_relation = false_owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=stored_observation.observation_occurrence_id,
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            scope_policy_ref=stored_capture.scope_policy_ref,
        )
        assert true_relation is not None
        assert false_relation is None

        true_assessment = append_assessment(
            true_owner,
            assessment_occurrence_id=f"assessment-eligibility::{token}",
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        )
        false_assessment = append_assessment(
            false_owner,
            assessment_occurrence_id=f"assessment-eligibility::{token}",
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        )
        assert str(true_assessment.outcome) == "one_or_more_received"
        assert str(false_assessment.outcome) == "zero_received"
        assert true_proxy.calls
        assert false_proxy.calls
        assert set(true_proxy.calls).issubset(_STORAGE_PROTOCOL_BOUND_ARITY)
        assert set(false_proxy.calls).issubset(_STORAGE_PROTOCOL_BOUND_ARITY)
        assert storage_state(true_proxy) == before_true
        assert storage_state(false_proxy) == before_false
        assert storage_state(true_proxy) == storage_state(false_proxy)
    finally:
        for dbname in (false_db, true_db, source_db):
            _drop_database(admin_dsn, dbname)


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
        "concurrent",
        "posix",
        "pty",
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
                        assert node.func.attr not in {
                            "open",
                            "write",
                            "pwrite",
                            "fork",
                            "forkpty",
                            "posix_spawn",
                            "posix_spawnp",
                            "system",
                            "popen",
                        }, path
                    assert node.func.attr != "ProcessPoolExecutor", path
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
