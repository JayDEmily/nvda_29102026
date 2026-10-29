from __future__ import annotations

import ast
import contextlib
import functools
import importlib
import inspect
import json
import multiprocessing
import os
import select
import shutil
import signal
import subprocess
import sys
import threading
import time
import types
import uuid
import weakref
from collections.abc import Mapping
from dataclasses import is_dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
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

from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence

ROOT = Path(__file__).resolve().parents[3]
PROBE = ROOT / "tests/product/raw_signal/_process_probe.py"
OWNER_PACKAGE = ROOT / "src/nvda_desk/raw_signal_occurrence_truth"
DEGRADED_TCP_ENV = "NVDA_U05_DEGRADED_TCP"
DEGRADED_TCP_BOUNDARY = "DEGRADED TCP VALIDATION"
_EXTERNAL_CAPABILITY_CANARY: Any = None


def _dsn() -> str:
    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for real PostgreSQL product proof")
    return value


def _durable_owner(*, dsn: str | None = None, **kwargs: Any) -> Any:
    """Construct the production owner with the authorised injected PostgreSQL port."""

    return build_owner(
        durability_port=create_postgres_persistence(dsn or _dsn()),
        **kwargs,
    )


def _psycopg() -> Any:
    try:
        module = importlib.import_module("psycopg")
    except ModuleNotFoundError as exc:
        pytest.fail(f"psycopg 3.3.4 proof dependency is missing: {exc}")
    assert module.__version__ == "3.3.4"
    return module


def _truncate_u05_semantic_store(dsn: str) -> None:
    create_postgres_persistence(dsn)
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        connection.execute(
            "TRUNCATE rsot_capture_receipt_presence_assessment_v1, "
            "rsot_raw_observation_occurrence_v1, "
            "rsot_scheduled_capture_occurrence_v1, "
            "rsot_capture_scope_policy_v1 CASCADE"
        )
        connection.commit()


@pytest.fixture(autouse=True)
def _isolate_u05_semantic_store() -> None:
    """Keep independent proof cases from becoming each other's durable policy universe."""

    _truncate_u05_semantic_store(_dsn())


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


def _degraded_tcp_enabled() -> bool:
    return os.environ.get(DEGRADED_TCP_ENV) == "1"


def _degraded_tcp_active(dsn: str) -> bool:
    if not _degraded_tcp_enabled():
        return False
    conninfo = importlib.import_module("psycopg.conninfo")
    host = conninfo.conninfo_to_dict(dsn).get("host")
    return bool(host and not host.startswith("/"))


def _require_pid_namespace_boundary(dsn: str) -> None:
    if _degraded_tcp_active(dsn):
        pytest.fail(
            f"{DEGRADED_TCP_BOUNDARY}: UNPROVED dedicated PID namespace at the "
            "public-return boundary; TCP execution cannot satisfy this proposition"
        )


def _isolated_command(dsn: str, *, pid_namespace: bool = False) -> list[str]:
    if _degraded_tcp_active(dsn):
        if pid_namespace:
            _require_pid_namespace_boundary(dsn)
        return [sys.executable, str(PROBE)]
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
    PostgreSQL DSN is delivered only in the JSON payload. The authoritative path makes the local
    filesystem ephemeral/read-only; explicitly degraded TCP execution receives task-local
    writable directories without claiming filesystem isolation.
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
    if _degraded_tcp_enabled():
        locations = {
            "HOME": workdir / "proof-home",
            "TMPDIR": workdir / "proof-tmp",
            "XDG_DATA_HOME": workdir / "proof-xdg",
        }
        for location in locations.values():
            location.mkdir()
        env.update({key: str(value) for key, value in locations.items()})
    else:
        env["HOME"] = "/run/proof-home"
        env["TMPDIR"] = "/run/proof-tmp"
        env["XDG_DATA_HOME"] = "/run/proof-xdg"
    return env


def _probe_cwd(workdir: Path) -> Path:
    return workdir if _degraded_tcp_enabled() else ROOT


def test_tcp_probe_requires_explicit_degraded_opt_in(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("NVDA_U05_DEGRADED_TCP", raising=False)
    with pytest.raises(
        pytest.fail.Exception,
        match="exclusive persistence proof requires a PostgreSQL Unix-domain socket DSN",
    ):
        _isolated_command("host=127.0.0.1 port=55444 dbname=postgres user=nobody")


def test_tcp_probe_uses_direct_process_only_under_explicit_degraded_opt_in(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NVDA_U05_DEGRADED_TCP", "1")
    command = _isolated_command("host=127.0.0.1 port=55444 dbname=postgres user=nobody")
    assert command == [sys.executable, str(PROBE)]


def test_degraded_tcp_pid_namespace_probe_is_explicitly_unproved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("NVDA_U05_DEGRADED_TCP", "1")
    with pytest.raises(
        pytest.fail.Exception,
        match=(
            "DEGRADED TCP VALIDATION: UNPROVED dedicated PID namespace at the "
            "public-return boundary"
        ),
    ):
        _isolated_command(
            "host=127.0.0.1 port=55444 dbname=postgres user=nobody",
            pid_namespace=True,
        )


def test_degraded_tcp_probe_uses_confined_work_directories(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("NVDA_U05_DEGRADED_TCP", "1")
    workdir = tmp_path / "probe"
    workdir.mkdir()
    env = _probe_env(workdir)
    assert env["HOME"] == str(workdir / "proof-home")
    assert env["TMPDIR"] == str(workdir / "proof-tmp")
    assert env["XDG_DATA_HOME"] == str(workdir / "proof-xdg")
    assert all(Path(env[key]).is_dir() for key in ("HOME", "TMPDIR", "XDG_DATA_HOME"))


def test_each_commit_ack_action_prepares_owner_before_ready_and_write() -> None:
    """Bind every durable-success probe to owner construction, READY/GO, then semantic write."""

    module = ast.parse(PROBE.read_text(encoding="utf-8"))
    functions = {
        node.name: node
        for node in module.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for action in (
        "boundary_write_policy",
        "boundary_write_capture",
        "boundary_write_observation",
        "boundary_write_zero_assessment",
        "boundary_write_one_assessment",
    ):
        function = functions[action]
        calls = {
            node.func.id: node.lineno
            for node in ast.walk(function)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id
            in {"_owner", "_await_semantic_write_release", "_observe_public_method_return"}
        }
        assert calls.keys() == {
            "_owner",
            "_await_semantic_write_release",
            "_observe_public_method_return",
        }, (action, calls)
        assert (
            calls["_owner"]
            < calls["_await_semantic_write_release"]
            < calls["_observe_public_method_return"]
        ), (action, calls)


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
        cwd=_probe_cwd(workdir),
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
        cwd=_probe_cwd(workdir),
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
        cwd=_probe_cwd(workdir),
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
    return _read_probe_event(process, "public_method_return", timeout=timeout)


def _read_probe_event(
    process: subprocess.Popen[str], event: str, *, timeout: float = 10.0
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
            if candidate.get("event") == event:
                return candidate
        if process.poll() is not None:
            stderr = process.stderr.read() if process.stderr is not None else ""
            raise AssertionError(f"probe exited before {event!r} marker: {stderr}")
    stderr = ""
    if process.poll() is not None and process.stderr is not None:
        stderr = process.stderr.read()
    raise AssertionError(f"probe produced no {event!r} marker before timeout: {stderr}")


def _release_semantic_write(process: subprocess.Popen[str]) -> None:
    assert process.stdin is not None
    process.stdin.write("go\n")
    process.stdin.flush()


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
    state = _backend_wait_state(dsn, application_name)
    return None if state is None else state[:2]


def _backend_wait_state(
    dsn: str, application_name: str
) -> tuple[str | None, str | None, str | None] | None:
    """Return the unique writer wait state and its server transaction identity."""

    psycopg = _psycopg()
    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            """
            select wait_event_type, wait_event, backend_xid::text
            from pg_stat_activity
            where application_name = %s and pid <> pg_backend_pid()
            """,
            (application_name,),
        )
        rows = cursor.fetchall()
    if not rows:
        return None
    assert len(rows) == 1, (application_name, rows)
    row = rows[0]
    return row[0], row[1], row[2]


def _wait_for_sync_rep_without_public_return(
    process: subprocess.Popen[str],
    *,
    dsn: str,
    application_name: str,
    timeout: float = 10.0,
) -> str:
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
        state = _backend_wait_state(dsn, application_name)
        last_wait = None if state is None else state[:2]
        if last_wait == ("IPC", "SyncRep"):
            readable, _, _ = select.select([process.stdout], [], [], 0.1)
            assert not readable, (
                "public method return became visible while PostgreSQL backend was still "
                "waiting for synchronous commit acknowledgement",
                last_wait,
            )
            assert state is not None and state[2] is not None, state
            return state[2]
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
    if isinstance(value, Mapping):
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
        source_temporal_kind=facts.get("source_temporal_kind", "true_instant"),
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


def _postgres_marker_xids(dsn: str, marker: str) -> set[str]:
    """Return PostgreSQL transaction identities for every row carrying one exact marker."""

    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    xids: set[str] = set()
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
            relation = sql.SQL("{}.{}").format(sql.Identifier(schema), sql.Identifier(table))
            query = sql.SQL(
                "select distinct t.xmin::text from {} as t where row_to_json(t)::text like %s"
            ).format(relation)
            cursor.execute(query, (f"%{marker}%",))
            xids.update(str(row[0]) for row in cursor.fetchall())
    return xids


def _semantic_marker_xids_are_transaction_bound(
    synchronous_wait_xid: str, marker_xids: set[str]
) -> bool:
    """Require the expected semantic identity to originate only in the waited transaction."""

    return marker_xids == {synchronous_wait_xid}


def _semantic_write_xids_are_transaction_bound(
    synchronous_wait_xid: str, write_xids: set[str]
) -> bool:
    """Require every post-GO database write to use the transaction seen in SyncRep."""

    return write_xids == {synchronous_wait_xid}


def _install_postgresql_write_trace(dsn: str) -> str:
    """Trace every existing non-system table and record the exact covered relation set."""

    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    suffix = uuid.uuid4().hex[:16]
    schema_name = f"nvda_proof_trace_{suffix}"
    trigger_name = f"nvda_proof_capture_{suffix}"

    schema = sql.Identifier(schema_name)
    capture_function = sql.SQL("{}.capture_write").format(schema)
    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.execute(sql.SQL("create schema {}").format(schema))
        cursor.execute(
            sql.SQL(
                """
                create table {}.events (
                    application_name text not null,
                    transaction_id text not null,
                    table_schema text not null,
                    table_name text not null,
                    operation text not null
                )
                """
            ).format(schema)
        )
        cursor.execute(
            sql.SQL(
                "create table {}.relations (relation_oid oid primary key, "
                "table_schema text not null, table_name text not null)"
            ).format(schema)
        )
        cursor.execute(
            sql.SQL(
                """
                create function {}() returns trigger language plpgsql as $$
                begin
                    insert into {}.events (
                        application_name,
                        transaction_id,
                        table_schema,
                        table_name,
                        operation
                    ) values (
                        current_setting('application_name', true),
                        pg_current_xact_id()::text,
                        TG_TABLE_SCHEMA,
                        TG_TABLE_NAME,
                        TG_OP
                    );
                    return null;
                end
                $$
                """
            ).format(capture_function, schema)
        )
        cursor.execute(
            """
            select relation.oid, namespace.nspname, relation.relname
            from pg_catalog.pg_class as relation
            join pg_catalog.pg_namespace as namespace
              on namespace.oid = relation.relnamespace
            where relation.relkind = 'r'
              and namespace.nspname not in ('pg_catalog', 'information_schema', %s)
              and namespace.nspname not like 'pg_toast%%'
            order by namespace.nspname, relation.relname
            """,
            (schema_name,),
        )
        tables = cursor.fetchall()
        assert tables, "semantic-write tracing requires an existing durable product relation"
        for relation_oid, table_schema, table_name in tables:
            relation = sql.SQL("{}.{}").format(
                sql.Identifier(table_schema), sql.Identifier(table_name)
            )
            cursor.execute(
                sql.SQL(
                    "create trigger {} after insert or update or delete on {} "
                    "for each row execute function {}()"
                ).format(sql.Identifier(trigger_name), relation, capture_function)
            )
            cursor.execute(
                sql.SQL(
                    "insert into {}.relations (relation_oid, table_schema, table_name) "
                    "values (%s, %s, %s)"
                ).format(schema),
                (relation_oid, table_schema, table_name),
            )
    return schema_name


def _postgresql_write_trace_xids(dsn: str, schema_name: str) -> set[str]:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
        cursor.execute(
            sql.SQL(
                """
                select namespace.nspname, relation.relname
                from pg_catalog.pg_class as relation
                join pg_catalog.pg_namespace as namespace
                  on namespace.oid = relation.relnamespace
                where relation.relkind = 'r'
                  and namespace.nspname not in ('pg_catalog', 'information_schema', {})
                  and namespace.nspname not like 'pg_toast%%'
                  and not exists (
                      select 1 from {}.relations as traced
                      where traced.relation_oid = relation.oid
                  )
                order by namespace.nspname, relation.relname
                """
            ).format(sql.Literal(schema_name), sql.Identifier(schema_name))
        )
        untraced = cursor.fetchall()
        assert not untraced, (
            "post-GO semantic command created untraced durable relations",
            untraced,
        )
        cursor.execute(
            sql.SQL("select distinct transaction_id from {}.events").format(
                sql.Identifier(schema_name)
            )
        )
        return {str(row[0]) for row in cursor.fetchall()}


def _drop_postgresql_write_trace(dsn: str, schema_name: str) -> None:
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    with psycopg.connect(dsn, autocommit=True) as connection, connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("drop schema if exists {} cascade").format(sql.Identifier(schema_name))
        )


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


def test_semantic_write_handshake_excludes_owner_setup_transaction(tmp_path: Path) -> None:
    """Prove only the post-READY/GO transaction can satisfy the SyncRep discriminator."""

    dsn = _dsn()
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    table = f"nvda_semantic_handshake_{uuid.uuid4().hex}"
    application_name = f"nvda-proof-semantic-handshake-{uuid.uuid4().hex}"
    writer_dsn = _dsn_with_application_name(dsn, application_name)
    original_setting = _current_synchronous_standby_names(dsn)
    barrier_name = f"nvda_proof_no_standby_{uuid.uuid4().hex}"
    barrier_active = False
    process: subprocess.Popen[str] | None = None

    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            sql.SQL("create table {} (phase text not null)").format(sql.Identifier(table))
        )

    try:
        workdir = tmp_path / f"semantic-handshake-{uuid.uuid4().hex}"
        workdir.mkdir()
        process = subprocess.Popen(
            _isolated_command(writer_dsn),
            cwd=_probe_cwd(workdir),
            env=_probe_env(workdir),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert process.stdin is not None
        process.stdin.write(
            json.dumps(
                {
                    "action": "sync_rep_handshake_canary",
                    "dsn": writer_dsn,
                    "token": _token("semantic-handshake"),
                    "table": table,
                    "semantic_write_handshake": True,
                }
            )
            + "\n"
        )
        process.stdin.flush()
        _read_probe_event(process, "semantic_write_ready")

        with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
            cursor.execute(sql.SQL("select phase from {}").format(sql.Identifier(table)))
            assert cursor.fetchall() == [("owner_setup",)]

        _set_synchronous_standby_names(dsn, f"FIRST 1 ({barrier_name})")
        _wait_for_synchronous_standby_setting(dsn, f"FIRST 1 ({barrier_name})")
        barrier_active = True
        _release_semantic_write(process)
        _wait_for_sync_rep_without_public_return(
            process, dsn=dsn, application_name=application_name
        )

        _set_synchronous_standby_names(dsn, original_setting or None)
        _wait_for_synchronous_standby_setting(dsn, original_setting)
        barrier_active = False
        stdout, stderr = process.communicate(timeout=10)
        assert process.returncode == 0, stdout + stderr
        result = json.loads([line for line in stdout.splitlines() if line.strip()][-1])
        assert result["phase"] == "semantic_write_committed"

        with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("select phase from {} order by phase").format(sql.Identifier(table))
            )
            assert cursor.fetchall() == [("owner_setup",), ("semantic_write",)]
    finally:
        if barrier_active:
            _set_synchronous_standby_names(dsn, original_setting or None)
            _wait_for_synchronous_standby_setting(dsn, original_setting)
        if process is not None and process.poll() is None:
            process.kill()
            process.communicate(timeout=10)
        with (
            psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute(sql.SQL("drop table if exists {}").format(sql.Identifier(table)))


def test_semantic_write_trace_rejects_split_marker_surrogate_payload_in_postgresql() -> None:
    """T013-F001: trace both commits when only the audit row contains the identity marker."""

    dsn = _dsn()
    psycopg = _psycopg()
    sql = importlib.import_module("psycopg.sql")
    suffix = uuid.uuid4().hex
    audit_table = f"nvda_semantic_audit_{suffix}"
    payload_table = f"nvda_semantic_payload_{suffix}"
    marker = f"semantic-record::{uuid.uuid4().hex}"
    application_name = f"nvda-proof-split-semantic-{uuid.uuid4().hex}"
    writer_dsn = _dsn_with_application_name(dsn, application_name)
    observed_xids: list[str] = []
    audit_id: int | None = None
    trace_schema: str | None = None

    with (
        psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            sql.SQL(
                "create table {} ("
                "audit_id bigint generated always as identity, "
                "marker text not null, primary key (audit_id))"
            ).format(sql.Identifier(audit_table))
        )
        cursor.execute(
            sql.SQL(
                "create table {} ("
                "audit_id bigint not null references {} (audit_id), "
                "payload text not null)"
            ).format(sql.Identifier(payload_table), sql.Identifier(audit_table))
        )

    try:
        trace_schema = _install_postgresql_write_trace(dsn)
        with psycopg.connect(writer_dsn) as connection, connection.cursor() as cursor:
            cursor.execute("select pg_current_xact_id()::text")
            observed_xids.append(str(cursor.fetchone()[0]))
            cursor.execute(
                sql.SQL("insert into {} (marker) values (%s) returning audit_id").format(
                    sql.Identifier(audit_table)
                ),
                (marker,),
            )
            audit_id = int(cursor.fetchone()[0])
            connection.commit()

        with psycopg.connect(writer_dsn) as connection, connection.cursor() as cursor:
            cursor.execute("select pg_current_xact_id()::text")
            observed_xids.append(str(cursor.fetchone()[0]))
            cursor.execute(
                sql.SQL("insert into {} (audit_id, payload) values (%s, %s)").format(
                    sql.Identifier(payload_table)
                ),
                (audit_id, "SEMANTIC_PAYLOAD"),
            )
            connection.commit()

        assert len(set(observed_xids)) == 2
        marker_xids = _postgres_marker_xids(dsn, marker)
        assert marker_xids == {observed_xids[0]}, (
            "canary requires the prior literal-marker discriminator to miss the payload commit",
            marker_xids,
            observed_xids,
        )
        assert _semantic_marker_xids_are_transaction_bound(observed_xids[0], marker_xids)
        trace_xids = _postgresql_write_trace_xids(dsn, trace_schema)
        assert trace_xids == set(observed_xids)
        assert not _semantic_write_xids_are_transaction_bound(observed_xids[0], trace_xids)

        with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "select a.marker, p.payload from {} as a join {} as p using (audit_id)"
                ).format(sql.Identifier(audit_table), sql.Identifier(payload_table))
            )
            assert cursor.fetchall() == [(marker, "SEMANTIC_PAYLOAD")]
    finally:
        if trace_schema is not None:
            _drop_postgresql_write_trace(dsn, trace_schema)
        with (
            psycopg.connect(_admin_dsn(dsn), autocommit=True) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute(
                sql.SQL("drop table if exists {}").format(sql.Identifier(payload_table))
            )
            cursor.execute(
                sql.SQL("drop table if exists {}").format(sql.Identifier(audit_table))
            )


def test_semantic_marker_xid_binding_rejects_setup_then_semantic_commits() -> None:
    assert not _semantic_marker_xids_are_transaction_bound("4101", {"4101", "4102"})


def test_semantic_write_trace_rejects_split_marker_surrogate_payload_transactions() -> None:
    """T013-F001: post-GO database writes may not span the waited and later XIDs."""

    assert not _semantic_write_xids_are_transaction_bound("779", {"779", "780"})


def test_public_factory_uses_same_semantic_owner_type_with_and_without_postgresql() -> None:
    assert type(build_owner()) is type(_durable_owner())


def test_process_boundary_forbids_shared_local_file_persistence(tmp_path: Path) -> None:
    dsn = _dsn()
    if _degraded_tcp_active(dsn):
        pytest.fail(
            f"{DEGRADED_TCP_BOUNDARY}: UNPROVED mapped mount/network namespace and "
            "exclusive filesystem boundary; TCP execution cannot satisfy this proposition"
        )
    host_path = ROOT / f".forbidden-proof-store-{uuid.uuid4().hex}"
    result = _run_probe(
        tmp_path,
        "filesystem_boundary",
        dsn=dsn,
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
    _require_pid_namespace_boundary(_dsn())
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


@pytest.mark.parametrize(
    ("action", "expected_key", "read_action", "assessment_which"),
    [
        ("boundary_write_policy", "policy", "read_policy", None),
        ("boundary_write_capture", "capture", "read_capture", None),
        ("boundary_write_observation", "observation", "read_observation", None),
        ("boundary_write_zero_assessment", "zero", "read_assessment", "zero"),
        ("boundary_write_one_assessment", "one", "read_assessment", "one"),
    ],
)
def test_public_success_return_requires_postgresql_commit_acknowledgement(
    tmp_path: Path,
    action: str,
    expected_key: str,
    read_action: str,
    assessment_which: str | None,
) -> None:
    dsn = _dsn()
    _require_pid_namespace_boundary(dsn)
    token = _token(f"commit-ack-{expected_key}")
    facts = _authoritative_facts()
    expected = _expected_records(token, facts)

    def establish_prerequisites(case_token: str, case_facts: dict[str, Any]) -> None:
        if action in {
            "boundary_write_capture",
            "boundary_write_zero_assessment",
            "boundary_write_one_assessment",
        }:
            _run_probe(
                tmp_path,
                "write_policy_only",
                dsn=dsn,
                token=case_token,
                facts=case_facts,
            )
        if action in {"boundary_write_zero_assessment", "boundary_write_one_assessment"}:
            _run_probe(tmp_path, "write_capture_only", dsn=dsn, token=case_token)
        if action == "boundary_write_one_assessment":
            _run_probe(tmp_path, "write_zero_assessment_only", dsn=dsn, token=case_token)
            _run_probe(
                tmp_path,
                "write_observation_only",
                dsn=dsn,
                token=case_token,
                facts=case_facts,
            )
            _run_probe(tmp_path, "derive_relation_only", dsn=dsn, token=case_token)

    # Warm the same public command path selected for the discriminator. Warming only the
    # observation path would let a command-specific first-use COMMIT satisfy SyncRep before the
    # selected durable write executes.
    warm_token = _token(f"commit-ack-{expected_key}-warm")
    warm_facts = _authoritative_facts()
    establish_prerequisites(warm_token, warm_facts)
    warm_action = {
        "boundary_write_policy": "write_policy_only",
        "boundary_write_capture": "write_capture_only",
        "boundary_write_observation": "write_observation_only",
        "boundary_write_zero_assessment": "write_zero_assessment_only",
        "boundary_write_one_assessment": "write_one_assessment_only",
    }[action]
    warm_extra = {"facts": warm_facts} if expected_key in {"policy", "observation"} else {}
    _run_probe(tmp_path, warm_action, dsn=dsn, token=warm_token, **warm_extra)
    # Warm-up facts are proof setup only. Remove them before the discriminator so they cannot
    # enter the semantic policy universe or satisfy any prerequisite for the command under test.
    _truncate_u05_semantic_store(dsn)

    # Establish only semantic prerequisites that must pre-exist for the command under test.
    # The command named by ``action`` remains the sole write performed under the SyncRep barrier.
    establish_prerequisites(token, facts)

    original_setting = _current_synchronous_standby_names(dsn)
    barrier_name = f"nvda_proof_no_standby_{uuid.uuid4().hex}"
    # PostgreSQL truncates application_name to 63 bytes; keep the discriminator exact.
    application_name = f"nvda-u05-ack-{expected_key}-{uuid.uuid4().hex[:16]}"
    writer_dsn = _dsn_with_application_name(dsn, application_name)
    process: subprocess.Popen[str] | None = None
    marker: dict[str, Any] | None = None
    trace_schema: str | None = None
    barrier_active = False
    try:
        write_extra = {"facts": facts} if expected_key in {"policy", "observation"} else {}
        process = _spawn_return_boundary_probe(
            tmp_path,
            action,
            dsn=writer_dsn,
            token=token,
            semantic_write_handshake=True,
            **write_extra,
        )
        _read_probe_event(process, "semantic_write_ready")

        # Install the trace only after READY, so owner/schema setup is excluded. Row triggers on
        # every existing user relation cover normalised/surrogate-linked rows; the readback helper
        # fails closed if the command creates any new untraced durable relation after GO.
        trace_schema = _install_postgresql_write_trace(dsn)

        _set_synchronous_standby_names(dsn, f"FIRST 1 ({barrier_name})")
        _wait_for_synchronous_standby_setting(dsn, f"FIRST 1 ({barrier_name})")
        barrier_active = True
        _release_semantic_write(process)
        semantic_write_xid = _wait_for_sync_rep_without_public_return(
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
        read_extra = {"which": assessment_which} if assessment_which is not None else {}
        fresh = _run_probe(
            tmp_path,
            read_action,
            dsn=dsn,
            token=token,
            **read_extra,
        )
        assert fresh["record"] == expected[expected_key]
        assert trace_schema is not None
        write_xids = _postgresql_write_trace_xids(dsn, trace_schema)
        assert _semantic_write_xids_are_transaction_bound(semantic_write_xid, write_xids), (
            "post-GO database writes were not confined to the transaction observed in SyncRep",
            semantic_write_xid,
            write_xids,
        )
        result = _release_return_boundary_probe(process, marker)
        assert result["record"] == expected[expected_key]
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
        if trace_schema is not None:
            _drop_postgresql_write_trace(dsn, trace_schema)


def test_command_return_is_durable_if_writer_is_killed_immediately_after_success(
    tmp_path: Path,
) -> None:
    dsn = _dsn()
    _require_pid_namespace_boundary(dsn)
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
    _require_pid_namespace_boundary(dsn)
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

    # NativeValueV1 is deliberately encoded as binary, so its high-entropy payload need not be
    # plaintext-searchable. Remove the authoritative durable observation row by domain identity
    # and prove a fresh process can no longer reproduce the record.
    psycopg = _psycopg()
    with psycopg.connect(dsn) as connection:
        deleted = connection.execute(
            "delete from rsot_raw_observation_occurrence_v1 "
            "where observation_occurrence_id = %s",
            (f"observation::{token}",),
        ).rowcount
        connection.commit()
    assert deleted == 1
    after_delete = _run_probe(tmp_path, "read_observation", dsn=dsn, token=token)
    assert after_delete["record"] is None

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
    assert high_same_scope["record"]["ingestion_sequence"] == _canonical(42)

    other_scope = _run_probe(
        tmp_path,
        "admit_low_sequence_other_scope",
        dsn=dsn,
        token=token,
    )
    assert other_scope["record"]["ingestion_sequence"] == _canonical(1)

    assert _without_pid(
        _run_probe(tmp_path, "admit_low_sequence_same_scope", dsn=dsn, token=token)
    ) == {"rejected": True}
    next_same_scope = _run_probe(
        tmp_path,
        "admit_next_sequence_same_scope",
        dsn=dsn,
        token=token,
    )
    assert next_same_scope["record"]["ingestion_sequence"] == _canonical(43)


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
    assert "durability_port" in inspect.signature(builder).parameters
    owner = builder(durability_port=create_postgres_persistence(_dsn()))
    assert type(owner) is type(build_owner())


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

_DURABILITY_TRANSACTION_METHODS = {
    "get_policy",
    "get_policy_by_ref",
    "list_policies",
    "append_policy",
    "get_capture",
    "get_capture_by_slot",
    "append_capture",
    "get_observation",
    "get_observation_high_water",
    "list_observations_received_between",
    "append_observation",
    "get_assessment",
    "list_assessments",
    "append_assessment",
}


class _RecordOnlyPersistenceProxy:
    """Capability-free replacement used only by graph-rewrite unit canaries."""

    def __init__(self) -> None:
        self._calls: list[str] = []

    @property
    def calls(self) -> tuple[str, ...]:
        return tuple(self._calls)

    def clear_calls(self) -> None:
        self._calls.clear()

    def append_policy(self, value: Any) -> Any:
        self._calls.append("append_policy")
        return value

    def get_policy(self, policy_id: Any, version: int) -> Any:
        self._calls.append("get_policy")
        return policy_id, version

    def append_capture(self, value: Any) -> Any:
        self._calls.append("append_capture")
        return value

    def get_capture(self, capture_id: Any) -> Any:
        self._calls.append("get_capture")
        return capture_id

    def append_observation(self, value: Any) -> Any:
        self._calls.append("append_observation")
        return value

    def get_observation(self, observation_id: Any) -> Any:
        self._calls.append("get_observation")
        return observation_id

    def append_assessment(self, value: Any) -> Any:
        self._calls.append("append_assessment")
        return value

    def get_assessment(self, assessment_id: Any) -> Any:
        self._calls.append("get_assessment")
        return assessment_id

    def list_assessments(self, capture_id: Any) -> Any:
        self._calls.append("list_assessments")
        return (capture_id,)


def _record_only_persistence_server(connection: Any, adapter_factory: Any) -> None:
    """Own the concrete adapter in a separate address space behind a strict allowlist."""

    try:
        adapter = adapter_factory()
        missing = [
            name
            for name in _STORAGE_PROTOCOL_BOUND_ARITY
            if not callable(getattr(adapter, name, None))
        ]
        if missing:
            raise AssertionError(
                f"record-only server adapter is missing protocol methods: {missing}"
            )
        connection.send(("ready", None))
        while True:
            request = connection.recv()
            operation = request[0]
            if operation == "stop":
                connection.send(("stopped", None))
                return
            _, method_name, args, kwargs = request
            if method_name not in _STORAGE_PROTOCOL_BOUND_ARITY:
                connection.send(
                    (
                        "forbidden",
                        f"{method_name!r} is outside the record-only persistence protocol",
                    )
                )
                continue
            try:
                result = getattr(adapter, method_name)(*args, **kwargs)
            except BaseException as exc:  # pragma: no cover - surfaced in the parent process
                connection.send(("error", type(exc).__qualname__, str(exc)))
            else:
                connection.send(("result", result))
    except EOFError:
        return
    finally:
        connection.close()


class _ForkedRecordOnlyPersistencePort:
    """Expose only record operations while the concrete adapter exists in a child process."""

    def __init__(self, adapter_factory: Any) -> None:
        assert "fork" in multiprocessing.get_all_start_methods(), (
            "record-only proof requires a forked address-space boundary"
        )
        context = multiprocessing.get_context("fork")
        parent_connection, child_connection = context.Pipe()
        process = context.Process(
            target=_record_only_persistence_server,
            args=(child_connection, adapter_factory),
            name=f"nvda-record-only-{uuid.uuid4().hex}",
            daemon=True,
        )
        process.start()
        child_connection.close()
        status = parent_connection.recv()
        assert status == ("ready", None), status
        self._connection = parent_connection
        self._process = process
        self._calls: list[str] = []

    @property
    def calls(self) -> tuple[str, ...]:
        return tuple(self._calls)

    def _clear_calls(self) -> None:
        self._calls.clear()

    def _request(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        self._connection.send(("call", method_name, args, kwargs))
        response = self._connection.recv()
        if response[0] == "result":
            self._calls.append(method_name)
            return response[1]
        if response[0] == "forbidden":
            raise AssertionError(response[1])
        if response[0] == "error":
            raise RuntimeError(f"remote {response[1]}: {response[2]}")
        raise AssertionError(f"unexpected record-only server response: {response!r}")

    def _close(self) -> None:
        if self._connection.closed:
            return
        if self._process.is_alive():
            self._connection.send(("stop",))
            assert self._connection.recv() == ("stopped", None)
        self._connection.close()
        self._process.join(timeout=10)
        assert not self._process.is_alive()

    def append_policy(self, value: Any) -> Any:
        return self._request("append_policy", value)

    def get_policy(self, policy_id: Any, version: int) -> Any:
        return self._request("get_policy", policy_id, version)

    def append_capture(self, value: Any) -> Any:
        return self._request("append_capture", value)

    def get_capture(self, capture_id: Any) -> Any:
        return self._request("get_capture", capture_id)

    def append_observation(self, value: Any) -> Any:
        return self._request("append_observation", value)

    def get_observation(self, observation_id: Any) -> Any:
        return self._request("get_observation", observation_id)

    def append_assessment(self, value: Any) -> Any:
        return self._request("append_assessment", value)

    def get_assessment(self, assessment_id: Any) -> Any:
        return self._request("get_assessment", assessment_id)

    def list_assessments(self, capture_id: Any) -> Any:
        return self._request("list_assessments", capture_id)


def _forked_postgresql_record_only_port(dsn: str) -> _ForkedRecordOnlyPersistencePort:
    def adapter_factory() -> Any:
        donor_owner = build_owner(postgres_dsn=dsn)
        ports = _find_default_persistence_ports(donor_owner)
        assert len(ports) == 1, ports
        return ports[0]

    return _ForkedRecordOnlyPersistencePort(adapter_factory)


def _is_weak_target_capability(value: Any, target: Any) -> bool:
    """Detect live weak references, weak methods and weak proxies to the adapter."""

    if isinstance(value, weakref.ReferenceType):
        referenced = value()
        return referenced is target or (
            inspect.ismethod(referenced) and referenced.__self__ is target
        )
    if isinstance(value, weakref.ProxyTypes):
        return any(value is candidate for candidate in weakref.getweakrefs(target))
    return False


def _rewire_production_graph_reference(root: Any, target: Any, replacement: Any) -> int:
    """Replace concrete-adapter capabilities throughout the reachable owner object graph."""

    replaced = 0
    seen: set[int] = set()

    def bound_target_method(value: Any) -> str | None:
        if inspect.ismethod(value) and value.__self__ is target:
            return str(value.__name__)
        return None

    def object_state_items(value: Any) -> list[tuple[str, Any]]:
        """Return instance dictionary and slot state without invoking descriptors."""

        items: dict[str, Any] = {}
        with contextlib.suppress(TypeError):
            items.update(vars(value))
        for owner_type in type(value).__mro__:
            declared = vars(owner_type).get("__slots__", ())
            slot_names = (declared,) if isinstance(declared, str) else declared
            for name in slot_names:
                if name in {"__dict__", "__weakref__"} or name in items:
                    continue
                try:
                    items[name] = object.__getattribute__(value, name)
                except (AttributeError, TypeError):
                    continue
        return list(items.items())

    def contains_target_capability(value: Any, local_seen: set[int] | None = None) -> bool:
        """Detect concrete adapter identity/capability through admitted caching forms."""

        if value is target:
            return True
        if bound_target_method(value) is not None:
            return True
        if _is_weak_target_capability(value, target):
            return True

        if local_seen is None:
            local_seen = set()
        value_id = id(value)
        if value_id in local_seen:
            return False
        local_seen.add(value_id)

        if isinstance(value, functools.partial):
            return (
                contains_target_capability(value.func, local_seen)
                or any(contains_target_capability(item, local_seen) for item in value.args)
                or any(
                    contains_target_capability(item, local_seen)
                    for item in (value.keywords or {}).values()
                )
            )
        if isinstance(value, dict):
            return any(
                contains_target_capability(key, local_seen)
                or contains_target_capability(child, local_seen)
                for key, child in value.items()
            )
        if isinstance(value, (list, tuple, set, frozenset)):
            return any(contains_target_capability(child, local_seen) for child in value)
        if inspect.isfunction(value):
            defaults = value.__defaults__ or ()
            kwdefaults = (value.__kwdefaults__ or {}).values()
            closure = value.__closure__ or ()
            if any(contains_target_capability(item, local_seen) for item in defaults):
                return True
            if any(contains_target_capability(item, local_seen) for item in kwdefaults):
                return True
            for cell in closure:
                try:
                    captured = cell.cell_contents
                except ValueError:
                    continue
                if contains_target_capability(captured, local_seen):
                    return True
            for name in value.__code__.co_names:
                if name in value.__globals__ and contains_target_capability(
                    value.__globals__[name], local_seen
                ):
                    return True
            return False
        if inspect.ismodule(value):
            return any(
                contains_target_capability(child, local_seen)
                for child in vars(value).values()
                if not inspect.ismodule(child)
            )
        if inspect.isclass(value):
            return any(
                contains_target_capability(child, local_seen)
                for owner_type in value.__mro__
                for name, child in vars(owner_type).items()
                if name not in {"__dict__", "__weakref__"}
            )
        if contains_target_capability(type(value), local_seen):
            return True
        return any(
            contains_target_capability(child, local_seen) for _, child in object_state_items(value)
        )

    def rewrite(value: Any) -> tuple[Any, bool]:
        nonlocal replaced

        if value is replacement:
            return value, False
        if value is target:
            replaced += 1
            return replacement, True

        method_name = bound_target_method(value)
        if method_name is not None:
            assert method_name in _STORAGE_PROTOCOL_BOUND_ARITY, (
                "owner cached a private PostgreSQL adapter capability",
                method_name,
            )
            replaced += 1
            return getattr(replacement, method_name), True

        assert not _is_weak_target_capability(value, target), (
            "owner retains a weak PostgreSQL adapter capability",
            value,
        )

        value_id = id(value)
        if value_id in seen:
            return value, False
        seen.add(value_id)

        if inspect.isfunction(value):
            assert not contains_target_capability(value), (
                "owner closure/default captures concrete/private PostgreSQL adapter capability",
                value,
            )
            return value, False

        if isinstance(value, functools.partial):
            new_func, func_changed = rewrite(value.func)
            new_args: list[Any] = []
            args_changed = False
            for child in value.args:
                new_child, changed = rewrite(child)
                new_args.append(new_child)
                args_changed = args_changed or changed
            new_keywords: dict[str, Any] = {}
            keywords_changed = False
            for key, child in (value.keywords or {}).items():
                new_child, changed = rewrite(child)
                new_keywords[key] = new_child
                keywords_changed = keywords_changed or changed
            if func_changed or args_changed or keywords_changed:
                rebuilt = functools.partial(new_func, *new_args, **new_keywords)
                rebuilt.__dict__.update(value.__dict__)
                return rebuilt, True
            return value, False

        if isinstance(value, list):
            changed_any = False
            for index, child in enumerate(tuple(value)):
                new_child, changed = rewrite(child)
                if changed:
                    value[index] = new_child
                    changed_any = True
            return value, changed_any

        if isinstance(value, dict):
            rewritten: list[tuple[Any, Any]] = []
            changed_any = False
            for key, child in tuple(value.items()):
                new_key, key_changed = rewrite(key)
                new_child, child_changed = rewrite(child)
                rewritten.append((new_key, new_child))
                changed_any = changed_any or key_changed or child_changed
            if changed_any:
                value.clear()
                value.update(rewritten)
            return value, changed_any

        if isinstance(value, tuple):
            rewritten_items: list[Any] = []
            changed_any = False
            for child in value:
                new_child, changed = rewrite(child)
                rewritten_items.append(new_child)
                changed_any = changed_any or changed
            return (tuple(rewritten_items), True) if changed_any else (value, False)

        if isinstance(value, set):
            rewritten_items: list[Any] = []
            changed_any = False
            for child in value:
                new_child, changed = rewrite(child)
                rewritten_items.append(new_child)
                changed_any = changed_any or changed
            if changed_any:
                value.clear()
                value.update(rewritten_items)
            return value, changed_any

        if isinstance(value, frozenset):
            rewritten_items = []
            changed_any = False
            for child in value:
                new_child, changed = rewrite(child)
                rewritten_items.append(new_child)
                changed_any = changed_any or changed
            return (frozenset(rewritten_items), True) if changed_any else (value, False)

        if inspect.ismodule(value) or inspect.isclass(value):
            assert not contains_target_capability(value), (
                "owner class/module retains concrete/private PostgreSQL adapter capability",
                value,
            )
            return value, False
        assert not contains_target_capability(type(value)), (
            "owner class/global retains concrete/private PostgreSQL adapter capability",
            type(value),
        )
        items = object_state_items(value)

        changed_any = False
        for name, child in items:
            new_child, changed = rewrite(child)
            if changed:
                object.__setattr__(value, name, new_child)
                changed_any = True
        return value, changed_any

    assert not contains_target_capability(replacement), (
        "record-only replacement retains concrete/private PostgreSQL adapter capability",
        replacement,
    )
    rewrite(root)
    return replaced


def _production_graph_contains_identity(root: Any, target: Any) -> bool:
    """Detect concrete adapter identity/capability through the reachable owner graph."""

    seen: set[int] = set()

    def object_state(value: Any) -> list[Any]:
        children: dict[str, Any] = {}
        with contextlib.suppress(TypeError):
            children.update(vars(value))
        for owner_type in type(value).__mro__:
            declared = vars(owner_type).get("__slots__", ())
            slot_names = (declared,) if isinstance(declared, str) else declared
            for name in slot_names:
                if name in {"__dict__", "__weakref__"} or name in children:
                    continue
                try:
                    children[name] = object.__getattribute__(value, name)
                except (AttributeError, TypeError):
                    continue
        return list(children.values())

    def visit(value: Any) -> bool:
        if value is target:
            return True
        if inspect.ismethod(value) and value.__self__ is target:
            return True
        if _is_weak_target_capability(value, target):
            return True

        value_id = id(value)
        if value_id in seen:
            return False
        seen.add(value_id)

        if isinstance(value, functools.partial):
            return (
                visit(value.func)
                or any(visit(item) for item in value.args)
                or any(visit(item) for item in (value.keywords or {}).values())
            )
        if isinstance(value, dict):
            return any(visit(key) or visit(child) for key, child in value.items())
        if isinstance(value, (list, tuple, set, frozenset)):
            return any(visit(child) for child in value)
        if inspect.isfunction(value):
            if any(visit(item) for item in value.__defaults__ or ()):
                return True
            if any(visit(item) for item in (value.__kwdefaults__ or {}).values()):
                return True
            for cell in value.__closure__ or ():
                try:
                    captured = cell.cell_contents
                except ValueError:
                    continue
                if visit(captured):
                    return True
            return any(
                visit(value.__globals__[name])
                for name in value.__code__.co_names
                if name in value.__globals__
            )
        if inspect.ismodule(value):
            return any(
                visit(child) for child in vars(value).values() if not inspect.ismodule(child)
            )
        if inspect.isclass(value):
            return any(
                visit(child)
                for owner_type in value.__mro__
                for name, child in vars(owner_type).items()
                if name not in {"__dict__", "__weakref__"}
            )
        return visit(type(value)) or any(visit(child) for child in object_state(value))

    return visit(root)


def test_record_only_proxy_rewrite_rejects_cached_private_adapter_capability() -> None:
    """Canary the direct private-capability escape before exercising the production graph."""

    class AdapterCanary:
        def _semantic_decision(self) -> bool:
            return True

    class OwnerCanary:
        def __init__(self, adapter: AdapterCanary) -> None:
            self._port = adapter
            self._cached_private = adapter._semantic_decision

    adapter = AdapterCanary()
    owner = OwnerCanary(adapter)
    proxy = _RecordOnlyPersistenceProxy()
    with pytest.raises(AssertionError, match="private PostgreSQL adapter capability"):
        _rewire_production_graph_reference(owner, adapter, proxy)


@pytest.mark.parametrize(
    "cache_kind",
    [
        "list",
        "dict",
        "tuple",
        "partial_function",
        "partial_argument",
        "partial_keyword",
        "closure",
    ],
)
def test_record_only_proxy_rewrite_rejects_nested_private_adapter_capability(
    cache_kind: str,
) -> None:
    """Canary T010-F002 across ordinary containers and unrewritable closure caching."""

    class AdapterCanary:
        def _semantic_decision(self) -> bool:
            return True

    class OwnerCanary:
        def __init__(self, adapter: AdapterCanary, cached: Any) -> None:
            self._port = adapter
            self._cached = cached

    adapter = AdapterCanary()
    private_capability = adapter._semantic_decision
    if cache_kind == "list":
        cached: Any = [{"nested": (private_capability,)}]
    elif cache_kind == "dict":
        cached = {"nested": [private_capability]}
    elif cache_kind == "tuple":
        cached = ({"nested": [private_capability]},)
    elif cache_kind == "partial_function":
        cached = functools.partial(private_capability)
    elif cache_kind == "partial_argument":
        cached = functools.partial(lambda capability: capability, private_capability)
    elif cache_kind == "partial_keyword":
        cached = functools.partial(lambda **kwargs: kwargs, capability=private_capability)
    else:
        captured = {"nested": [private_capability]}

        def cached_closure() -> bool:
            return captured["nested"][0]()

        cached = cached_closure

    owner = OwnerCanary(adapter, cached)
    proxy = _RecordOnlyPersistenceProxy()
    with pytest.raises(AssertionError, match="PostgreSQL adapter capability"):
        _rewire_production_graph_reference(owner, adapter, proxy)


@pytest.mark.parametrize("cache_kind", ["class", "slots", "global", "module"])
def test_record_only_proxy_rewrite_rejects_external_private_adapter_capability(
    cache_kind: str,
) -> None:
    """Canary T011-F002 outside the ordinary instance ``__dict__`` graph."""

    class AdapterCanary:
        def _semantic_decision(self) -> bool:
            return True

    adapter = AdapterCanary()

    if cache_kind == "class":

        class OwnerCanary:
            def __init__(self, concrete: AdapterCanary) -> None:
                self._port = concrete
                type(self)._cached = concrete._semantic_decision

        owner: Any = OwnerCanary(adapter)
    elif cache_kind == "slots":

        class OwnerCanary:
            __slots__ = ("_cached", "_port")

            def __init__(self, concrete: AdapterCanary) -> None:
                self._port = concrete
                self._cached = concrete._semantic_decision

        owner = OwnerCanary(adapter)
    elif cache_kind == "global":
        global _EXTERNAL_CAPABILITY_CANARY
        _EXTERNAL_CAPABILITY_CANARY = adapter._semantic_decision

        def cached_global() -> bool:
            assert _EXTERNAL_CAPABILITY_CANARY is not None
            return _EXTERNAL_CAPABILITY_CANARY()

        class OwnerCanary:
            def __init__(self, concrete: AdapterCanary) -> None:
                self._port = concrete
                self._cached = cached_global

        owner = OwnerCanary(adapter)
    else:
        cache_module = types.ModuleType("nvda_adapter_capability_canary")
        cache_module._cached = adapter._semantic_decision

        class OwnerCanary:
            def __init__(self, concrete: AdapterCanary) -> None:
                self._port = concrete
                self._cache_module = cache_module

        owner = OwnerCanary(adapter)

    proxy = _RecordOnlyPersistenceProxy()
    try:
        with pytest.raises(AssertionError, match="PostgreSQL adapter capability"):
            _rewire_production_graph_reference(owner, adapter, proxy)
    finally:
        if cache_kind == "class":
            delattr(type(owner), "_cached")
        if cache_kind == "global":
            _EXTERNAL_CAPABILITY_CANARY = None


@pytest.mark.parametrize("weak_kind", ["ref", "method", "proxy", "callable_proxy"])
def test_record_only_proxy_rewrite_rejects_weak_adapter_capability(weak_kind: str) -> None:
    """Canary T012-F002 across dereferenceable weak references and proxies."""

    class AdapterCanary:
        def _semantic_decision(self) -> bool:
            return True

    class CallableAdapterCanary(AdapterCanary):
        def __call__(self) -> bool:
            return True

    class OwnerCanary:
        def __init__(self, adapter: AdapterCanary, cached: Any) -> None:
            self._port = adapter
            self._cached = cached

    adapter = CallableAdapterCanary() if weak_kind == "callable_proxy" else AdapterCanary()
    if weak_kind == "ref":
        cached: Any = weakref.ref(adapter)
    elif weak_kind == "method":
        cached = weakref.WeakMethod(adapter._semantic_decision)
    else:
        cached = weakref.proxy(adapter)

    owner = OwnerCanary(adapter, cached)
    proxy = _RecordOnlyPersistenceProxy()
    owner._port = proxy
    assert _production_graph_contains_identity(owner, adapter)
    with pytest.raises(AssertionError, match="weak PostgreSQL adapter capability"):
        _rewire_production_graph_reference(owner, adapter, proxy)


def test_injected_record_only_port_rejects_private_adapter_recovery() -> None:
    """T013-F002: the injected capability cannot reveal or dispatch private adapter state."""

    class AdapterCanary:
        def append_policy(self, value: Any) -> Any:
            return value

        def get_policy(self, policy_id: Any, version: int) -> tuple[Any, int]:
            return policy_id, version

        def append_capture(self, value: Any) -> Any:
            return value

        def get_capture(self, capture_id: Any) -> Any:
            return capture_id

        def append_observation(self, value: Any) -> Any:
            return value

        def get_observation(self, observation_id: Any) -> Any:
            return observation_id

        def append_assessment(self, value: Any) -> Any:
            return value

        def get_assessment(self, assessment_id: Any) -> Any:
            return assessment_id

        def list_assessments(self, capture_id: Any) -> tuple[Any, ...]:
            return (capture_id,)

        def _semantic_decision(self) -> str:
            return "adapter-owned-semantic-decision"

    port = _ForkedRecordOnlyPersistencePort(AdapterCanary)
    try:
        public_callables = {
            name for name in dir(port) if not name.startswith("_") and callable(getattr(port, name))
        }
        assert public_callables == set(_STORAGE_PROTOCOL_BOUND_ARITY)
        assert port.append_policy("record") == "record"
        with pytest.raises(AttributeError):
            object.__getattribute__(port, "_inner")
        with pytest.raises(AssertionError, match="outside the record-only persistence protocol"):
            port._request("_semantic_decision")
    finally:
        port._close()


def test_graph_checker_does_not_treat_adapter_holding_record_proxy_as_opaque() -> None:
    """T013-F002: the exact prior ``proxy._inner`` escape is visible and rejected."""

    class AdapterCanary:
        def _semantic_decision(self) -> str:
            return "adapter-owned-semantic-decision"

    class OwnerCanary:
        def __init__(self, port: Any) -> None:
            self._port = port

    adapter = AdapterCanary()
    unsafe_proxy = _RecordOnlyPersistenceProxy()
    unsafe_proxy._inner = adapter
    owner = OwnerCanary(unsafe_proxy)

    assert _production_graph_contains_identity(owner, adapter)
    with pytest.raises(AssertionError, match="replacement retains concrete/private"):
        _rewire_production_graph_reference(owner, adapter, unsafe_proxy)


def test_record_only_proxy_rewrite_rewrites_nested_public_storage_capabilities() -> None:
    """Prove admitted bound methods cannot retain a hidden concrete-adapter receiver."""

    class AdapterCanary:
        def append_policy(self, value: Any) -> Any:
            return value

        def get_policy(self, policy_id: Any, version: int) -> tuple[Any, int]:
            return policy_id, version

        def append_capture(self, value: Any) -> Any:
            return value

        def get_capture(self, capture_id: Any) -> Any:
            return capture_id

    class OwnerCanary:
        def __init__(self, adapter: AdapterCanary) -> None:
            self._port = adapter
            self._nested = [
                adapter.append_policy,
                {"reader": adapter.get_policy},
                (adapter.append_capture,),
                functools.partial(adapter.get_capture, "capture-id"),
            ]

    adapter = AdapterCanary()
    owner = OwnerCanary(adapter)
    proxy = _RecordOnlyPersistenceProxy()
    replaced = _rewire_production_graph_reference(owner, adapter, proxy)

    assert replaced == 5
    assert owner._port is proxy
    assert owner._nested[0].__self__ is proxy
    assert owner._nested[1]["reader"].__self__ is proxy
    assert owner._nested[2][0].__self__ is proxy
    assert isinstance(owner._nested[3], functools.partial)
    assert owner._nested[3].func.__self__ is proxy
    assert not _production_graph_contains_identity(owner, adapter)


def test_postgresql_durability_port_exposes_only_authorised_transaction_query_contract() -> None:
    port = create_postgres_persistence(_dsn())
    public_port_callables = {
        name for name in dir(port) if not name.startswith("_") and callable(getattr(port, name))
    }
    assert public_port_callables == {"transaction"}

    with port.transaction(write=False) as transaction:
        public_transaction_callables = {
            name
            for name in dir(transaction)
            if not name.startswith("_") and callable(getattr(transaction, name))
        }
    assert public_transaction_callables == _DURABILITY_TRANSACTION_METHODS

    owner = build_owner(durability_port=port)
    assert _find_default_persistence_ports(owner) == []
    for facet in (owner, owner.commands, owner.reads):
        assert not hasattr(facet, "transaction")


def test_postgresql_adapter_preserves_owner_decided_assessment_without_rederiving() -> None:
    token = _token("storage-only")
    port = create_postgres_persistence(_dsn())
    owner = build_owner(durability_port=port, eligibility_resolver=lambda _o, _p: True)
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

    # The technical adapter receives an already-decided semantic record and must preserve it.
    # The deliberately counterfactual zero outcome proves the adapter does not inspect durable
    # observations or eligibility authority and silently replace M00's semantic decision.
    canary = assessment_contract(
        assessment_occurrence_id=f"assessment-storage-canary::{token}",
        capture_occurrence_ref=capture.capture_occurrence_id,
        outcome="zero_received",
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    with port.transaction(write=True) as transaction:
        transaction.append_assessment(canary)

    fresh_port = create_postgres_persistence(_dsn())
    with fresh_port.transaction(write=False) as transaction:
        reread = transaction.get_assessment(canary.assessment_occurrence_id)
    assert reread == canary
    assert reread.outcome == "zero_received"


def test_postgresql_adapter_is_invariant_under_opposing_eligibility_authority() -> None:
    token = _token("eligibility-invariance")
    facts = _authoritative_facts()
    seed_owner = _durable_owner(eligibility_resolver=lambda _o, _p: True)
    stored_policy = register_policy(
        seed_owner,
        policy(
            scope_policy_id=f"scope::{token}",
            eligibility_policy_ref=facts["eligibility_policy_ref"],
        ),
    )
    stored_capture = realise_capture(
        seed_owner,
        scope_policy_ref=f"scope::{token}@1",
        capture_occurrence_id=f"capture::{token}",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    stored_observation = admit_observation(
        seed_owner,
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

    true_owner = _durable_owner(eligibility_resolver=lambda _o, _p: True)
    false_owner = _durable_owner(eligibility_resolver=lambda _o, _p: False)

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

    # The same durable facts remain unchanged. Eligibility is an owner-side authority decision,
    # not a PostgreSQL adapter decision or materialised relation state.
    reader = create_postgres_persistence(_dsn())
    with reader.transaction(write=False) as transaction:
        assert transaction.get_policy(
            stored_policy.scope_policy_id, stored_policy.scope_policy_version
        ) == stored_policy
        assert transaction.get_capture(stored_capture.capture_occurrence_id) == stored_capture
        assert (
            transaction.get_observation(stored_observation.observation_occurrence_id)
            == stored_observation
        )

    postgres_source = (
        ROOT / "src/nvda_desk/raw_signal_occurrence_truth/_postgres.py"
    ).read_text(encoding="utf-8")
    for semantic_name in ("eligibility_resolver", "derive_capture_receipt_evidence_relation"):
        assert semantic_name not in postgres_source


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
    owner = _durable_owner()
    for forbidden in (
        "cross_kind_atomic",
        "replay_equivalent",
        "rto",
        "rpo",
        "retention_duration",
        "recovery_deadline",
    ):
        assert not hasattr(owner, forbidden)
