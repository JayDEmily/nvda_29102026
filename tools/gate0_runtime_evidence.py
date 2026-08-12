from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import secrets
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

AUTOMATIC_FINAL_SUBAGENT_STOP_CLOSURE = False
EXPECTED_ROLES = ("integration_auditor", "semantic_reviewer")
STATE_DIR_NAME = "nvda_gate0_runtime"


class Gate0Error(RuntimeError):
    pass


def _utcnow() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _run(root: Path, *args: str) -> str:
    return subprocess.check_output(args, cwd=root, text=True).strip()


def repo_root() -> Path:
    return Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    ).resolve()


def git_dir(root: Path) -> Path:
    raw = _run(root, "git", "rev-parse", "--git-dir")
    p = Path(raw)
    return (p if p.is_absolute() else root / p).resolve()


def state_dir(root: Path) -> Path:
    return git_dir(root) / STATE_DIR_NAME


def load_manifest(root: Path) -> dict[str, Any]:
    return json.loads((root / "docs/governance/GATE0_ADMISSION_MANIFEST.json").read_text())


def guarded_hashes(root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for rel in manifest["guarded_paths"]:
        p = root / rel
        if not p.is_file():
            raise Gate0Error(f"guarded path missing: {rel}")
        result[rel] = sha256_file(p)
    return result


def validate_host_policy(
    *,
    system: str,
    machine: str,
    wsl_distro: str | None,
    kernel_release: str,
    repo_root: str,
) -> None:
    if system != "Linux" or machine != "x86_64":
        raise Gate0Error("Gate 0 programme policy requires Linux x86_64")
    if not wsl_distro:
        raise Gate0Error("Gate 0 programme policy requires WSL2")
    release = kernel_release.lower()
    if "microsoft" not in release or "wsl2" not in release:
        raise Gate0Error("Gate 0 programme policy requires a WSL2 kernel")
    resolved = Path(repo_root).resolve()
    if resolved == Path("/mnt") or Path("/mnt") in resolved.parents:
        raise Gate0Error("Gate 0 programme policy requires native WSL storage outside /mnt")
    if resolved == Path("/") or Path("/home") not in resolved.parents:
        raise Gate0Error("Gate 0 programme policy requires a repository under /home/...")


def make_arm_record(
    *,
    branch: str,
    head: str,
    manifest_sha256: str,
    guarded_hashes: dict[str, str],
    run_nonce: str,
    worktree_clean: bool,
) -> dict[str, Any]:
    if not worktree_clean:
        raise Gate0Error("dirty worktree cannot arm Gate 0")
    return {
        "schema_version": "1.0.0",
        "state": "ARMED",
        "branch": branch,
        "head": head,
        "manifest_sha256": manifest_sha256,
        "guarded_hashes": dict(sorted(guarded_hashes.items())),
        "run_nonce": run_nonce,
        "immediate_roles": list(EXPECTED_ROLES),
    }


def validate_arm_binding(
    arm: dict[str, Any],
    *,
    current_branch: str,
    current_head: str,
    current_manifest_sha256: str,
    current_guarded_hashes: dict[str, str],
    current_worktree_clean: bool,
) -> tuple[bool, str | None]:
    if arm.get("branch") != current_branch:
        return False, "BRANCH"
    if arm.get("head") != current_head:
        return False, "HEAD"
    if arm.get("manifest_sha256") != current_manifest_sha256:
        return False, "MANIFEST_HASH"
    if arm.get("guarded_hashes") != dict(sorted(current_guarded_hashes.items())):
        return False, "GUARDED_HASHES"
    if not current_worktree_clean:
        return False, "WORKTREE_DIRTY"
    return True, None


def validate_probe_payload(
    arm: dict[str, Any],
    *,
    role: str,
    expected_nonce: str,
    probe: dict[str, Any],
) -> tuple[bool, str | None]:
    if probe.get("gate0_probe") is not True:
        return False, "PROBE_MARKER"
    if probe.get("role") != role:
        return False, "ROLE"
    if probe.get("nonce") != expected_nonce:
        return False, "NONCE"
    if probe.get("run_nonce") != arm.get("run_nonce"):
        return False, "RUN_NONCE"
    if probe.get("head") != arm.get("head"):
        return False, "HEAD"
    if probe.get("repo_root") != arm.get("repo_root"):
        return False, "REPO_ROOT"
    platform_data = probe.get("platform") or {}
    if (
        platform_data.get("system") != "Linux"
        or platform_data.get("machine") != "x86_64"
        or not platform_data.get("wsl_distro")
        or "microsoft" not in str(platform_data.get("kernel_release", "")).lower()
        or "wsl2" not in str(platform_data.get("kernel_release", "")).lower()
    ):
        return False, "PLATFORM"
    probes = probe.get("probes")
    required = {"repository", "git_metadata", "slash_tmp", "home"}
    if not isinstance(probes, dict) or set(probes) != required:
        return False, "PROBE_SET"
    if any((probes[name] or {}).get("write_allowed") is not False for name in required):
        return False, "WRITE_BOUNDARY"
    if probe.get("passed") is not True:
        return False, "PROBE_REPORTED_FAILURE"
    return True, None


def _evidence_digest(events: list[dict[str, Any]]) -> str:
    return _sha256_bytes(json.dumps(events, sort_keys=True, separators=(",", ":")).encode())


def meaningful_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [e for e in events if e.get("type") not in {"PreToolUse", "PostToolUse"}]


def expected_next_spawn_role(events: list[dict[str, Any]], *, run_nonce: str) -> str | None:
    evidence = meaningful_events(events)
    if any(e.get("type") == "Gate0Failure" for e in evidence):
        raise Gate0Error("Gate 0 already has a recorded first failure")
    if len(evidence) < 2 or not (
        evidence[0].get("type") == "SessionStart"
        and evidence[0].get("run_nonce") == run_nonce
        and evidence[1].get("type") == "ProbeResult"
        and evidence[1].get("role") == "__parent__"
        and evidence[1].get("run_nonce") == run_nonce
        and evidence[1].get("passed") is True
    ):
        raise Gate0Error("parent capability proof is not complete")

    cursor = 2
    for role in EXPECTED_ROLES:
        if len(evidence) == cursor:
            return role
        if len(evidence) < cursor + 4:
            raise Gate0Error(f"{role} is still in progress")
        spawn, start, probe, stop = evidence[cursor : cursor + 4]
        if not (
            spawn.get("type") == "SpawnRequest"
            and spawn.get("role") == role
            and spawn.get("run_nonce") == run_nonce
            and start.get("type") == "SubagentStart"
            and start.get("role") == role
            and start.get("run_nonce") == run_nonce
            and probe.get("type") == "ProbeResult"
            and probe.get("role") == role
            and probe.get("run_nonce") == run_nonce
            and probe.get("passed") is True
            and stop.get("type") == "SubagentStop"
            and stop.get("role") == role
            and stop.get("run_nonce") == run_nonce
        ):
            raise Gate0Error(f"invalid completed Gate 0 sequence for {role}")
        cursor += 4
    if len(evidence) == cursor:
        return None
    raise Gate0Error("Gate 0 evidence contains an unexpected event")


def wait_agent_allowed(events: list[dict[str, Any]], *, run_nonce: str) -> bool:
    """Return true only while one admitted Gate-0 child is in progress.

    The public Codex documentation names `wait_agent` but does not guarantee a stable
    target-argument schema. Gate 0 therefore constrains the temporal state instead of
    claiming an undocumented target-input binding. A fresh Gate-0 session is sequential,
    so exactly one admitted child can be in progress at a time.
    """
    evidence = meaningful_events(events)
    if any(e.get("type") == "Gate0Failure" for e in evidence):
        return False
    if len(evidence) < 2 or not (
        evidence[0].get("type") == "SessionStart"
        and evidence[0].get("run_nonce") == run_nonce
        and evidence[1].get("type") == "ProbeResult"
        and evidence[1].get("role") == "__parent__"
        and evidence[1].get("run_nonce") == run_nonce
        and evidence[1].get("passed") is True
    ):
        return False
    cursor = 2
    for role in EXPECTED_ROLES:
        if len(evidence) == cursor:
            return False
        spawn = evidence[cursor]
        if not (
            spawn.get("type") == "SpawnRequest"
            and spawn.get("role") == role
            and spawn.get("run_nonce") == run_nonce
        ):
            return False
        if len(evidence) < cursor + 4:
            return True
        start, probe, stop = evidence[cursor + 1 : cursor + 4]
        if not (
            start.get("type") == "SubagentStart"
            and start.get("role") == role
            and start.get("run_nonce") == run_nonce
            and probe.get("type") == "ProbeResult"
            and probe.get("role") == role
            and probe.get("run_nonce") == run_nonce
            and probe.get("passed") is True
            and stop.get("type") == "SubagentStop"
            and stop.get("role") == role
            and stop.get("run_nonce") == run_nonce
        ):
            return False
        cursor += 4
    return False


def expected_next_start_role(events: list[dict[str, Any]], *, run_nonce: str) -> str | None:
    evidence = meaningful_events(events)
    for role, index in (("integration_auditor", 2), ("semantic_reviewer", 6)):
        if len(evidence) == index + 1:
            event = evidence[index]
            if (
                event.get("type") == "SpawnRequest"
                and event.get("role") == role
                and event.get("run_nonce") == run_nonce
            ):
                return role
    return None


def derive_attestation(arm: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    run_nonce = arm.get("run_nonce")
    head = arm.get("head")
    evidence = meaningful_events(events)

    def fail(name: str) -> dict[str, Any]:
        return {"passed": False, "first_failure": name, "evidence_sha256": _evidence_digest(events)}

    first_failure = next((e for e in evidence if e.get("type") == "Gate0Failure"), None)
    if first_failure is not None:
        return fail(str(first_failure.get("stage") or "GATE0_FAILURE"))

    if not evidence or evidence[0].get("type") != "SessionStart":
        return fail("SESSION_START")
    session = evidence[0]
    if (
        session.get("run_nonce") != run_nonce
        or session.get("head") != head
        or session.get("cwd") != arm.get("repo_root")
        or session.get("source") != "startup"
        or session.get("permission_mode") != "default"
    ):
        return fail("SESSION_START")
    i = 1
    if (
        i >= len(evidence)
        or evidence[i].get("type") != "ProbeResult"
        or evidence[i].get("role") != "__parent__"
        or evidence[i].get("run_nonce") != run_nonce
        or evidence[i].get("passed") is not True
    ):
        return fail("PARENT_PROBE")
    i += 1
    identities: set[str] = set()
    for role in EXPECTED_ROLES:
        if (
            i >= len(evidence)
            or evidence[i].get("type") != "SpawnRequest"
            or evidence[i].get("role") != role
            or evidence[i].get("run_nonce") != run_nonce
        ):
            return fail(f"SPAWN_REQUEST:{role}")
        i += 1
        if (
            i >= len(evidence)
            or evidence[i].get("type") != "SubagentStart"
            or evidence[i].get("role") != role
            or evidence[i].get("run_nonce") != run_nonce
        ):
            return fail(f"SUBAGENT_START:{role}")
        agent_id = evidence[i].get("agent_id")
        if not isinstance(agent_id, str) or not agent_id:
            return fail(f"SUBAGENT_START:{role}")
        if agent_id in identities:
            return fail("DISTINCT_CHILD_IDENTITY")
        identities.add(agent_id)
        i += 1
        if (
            i >= len(evidence)
            or evidence[i].get("type") != "ProbeResult"
            or evidence[i].get("role") != role
            or evidence[i].get("agent_id") != agent_id
            or evidence[i].get("run_nonce") != run_nonce
            or evidence[i].get("passed") is not True
        ):
            return fail(f"PROBE:{role}")
        i += 1
        if (
            i >= len(evidence)
            or evidence[i].get("type") != "SubagentStop"
            or evidence[i].get("role") != role
            or evidence[i].get("agent_id") != agent_id
            or evidence[i].get("run_nonce") != run_nonce
        ):
            return fail(f"SUBAGENT_STOP:{role}")
        i += 1
    if i != len(evidence):
        return fail("UNEXPECTED_EVENT")
    return {"passed": True, "first_failure": None, "evidence_sha256": _evidence_digest(events)}


def validate_final_admission_evidence(
    arm: dict[str, Any],
    *,
    derived: dict[str, Any],
    recomputed: dict[str, Any],
    binding_ok: bool,
) -> None:
    if arm.get("state") != "SEALED":
        raise Gate0Error("Gate 0 evidence must be SEALED before admission")
    if not binding_ok:
        raise Gate0Error("Gate 0 Git/control binding is no longer valid")
    if derived != recomputed:
        raise Gate0Error("stored Gate 0 evidence does not match recomputed evidence")
    if derived.get("passed") is not True:
        raise Gate0Error("Gate 0 evidence is not passing")


def build_admission_record(
    *, arm: dict[str, Any], derived: dict[str, Any], admission_id: str, admitted_at_utc: str
) -> dict[str, Any]:
    if derived.get("passed") is not True:
        raise Gate0Error("cannot admit a non-passing Gate 0 derivation")
    return {
        "schema_version": "1.0.0",
        "admission_id": admission_id,
        "proposition_id": "GATE0_MINIMAL_RUNTIME_ADMISSION_V1",
        "run_nonce": arm["run_nonce"],
        "proven_commit": arm["head"],
        "manifest_sha256": arm["manifest_sha256"],
        "guarded_hashes": arm["guarded_hashes"],
        "evidence_sha256": derived["evidence_sha256"],
        "disposition": "GATE0_PASS",
        "admitted_at_utc": admitted_at_utc,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def load_arm(root: Path) -> dict[str, Any]:
    path = state_dir(root) / "arm.json"
    if not path.is_file():
        raise Gate0Error("Gate 0 is not armed")
    return _read_json(path)


def load_active_arm(root: Path) -> dict[str, Any] | None:
    path = state_dir(root) / "arm.json"
    if not path.is_file():
        return None
    arm = _read_json(path)
    return arm if arm.get("state") == "ARMED" else None


def load_failure(root: Path) -> dict[str, Any] | None:
    path = state_dir(root) / "failure.json"
    return _read_json(path) if path.is_file() else None


def record_failure(root: Path, *, stage: str, reason: str) -> dict[str, Any]:
    existing = load_failure(root)
    if existing is not None:
        return existing
    arm = load_arm(root)
    record = {
        "run_nonce": arm.get("run_nonce"),
        "head": arm.get("head"),
        "stage": stage,
        "reason": reason,
        "recorded_at_utc": _utcnow(),
    }
    _write_json(state_dir(root) / "failure.json", record)
    append_event(
        root,
        {
            "type": "Gate0Failure",
            "run_nonce": arm.get("run_nonce"),
            "stage": stage,
            "reason": reason,
        },
    )
    return record


def load_events(root: Path) -> list[dict[str, Any]]:
    path = state_dir(root) / "events.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_event(root: Path, event: dict[str, Any]) -> None:
    event = {**event, "recorded_at_utc": _utcnow()}
    _append_jsonl(state_dir(root) / "events.jsonl", event)


def expected_probe_commands(root: Path, arm: dict[str, Any]) -> dict[str, str]:
    py = root / ".venv/bin/python"
    probe = root / "tools/gate0_probe.py"
    run_nonce = arm["run_nonce"]
    result = {
        "__parent__": (
            f"{py} -B {probe} --role __parent__ --nonce {run_nonce} --run-nonce {run_nonce}"
        )
    }
    nonces_path = state_dir(root) / "agent_nonces.json"
    if nonces_path.is_file():
        data = _read_json(nonces_path)
        for role, item in data.get("roles", {}).items():
            result[role] = (
                f"{py} -B {probe} --role {role} --nonce {item['nonce']} --run-nonce {run_nonce}"
            )
    return result


def command_role(root: Path, arm: dict[str, Any], command: str) -> str | None:
    for role, expected in expected_probe_commands(root, arm).items():
        if command == expected:
            return role
    return None


def arm_repository() -> dict[str, Any]:
    root = repo_root()
    clean = not bool(_run(root, "git", "status", "--porcelain=v1", "--untracked-files=all"))
    branch = _run(root, "git", "branch", "--show-current")
    head = _run(root, "git", "rev-parse", "HEAD")
    manifest_path = root / "docs/governance/GATE0_ADMISSION_MANIFEST.json"
    manifest = load_manifest(root)
    validate_host_policy(
        system=platform.system(),
        machine=platform.machine(),
        wsl_distro=os.environ.get("WSL_DISTRO_NAME"),
        kernel_release=platform.release(),
        repo_root=str(root),
    )
    project_python = root / ".venv/bin/python"
    if not project_python.is_file():
        raise Gate0Error("project .venv/bin/python is required before arming")
    py_version = subprocess.check_output(
        [str(project_python), "-c", "import platform;print(platform.python_version())"], text=True
    ).strip()
    if py_version != "3.13.5":
        raise Gate0Error(f"expected project Python 3.13.5, got {py_version}")
    record = make_arm_record(
        branch=branch,
        head=head,
        manifest_sha256=sha256_file(manifest_path),
        guarded_hashes=guarded_hashes(root, manifest),
        run_nonce=secrets.token_hex(16),
        worktree_clean=clean,
    )
    record.update(
        {"repo_root": str(root), "armed_at_utc": _utcnow(), "project_python": str(project_python)}
    )
    sd = state_dir(root)
    sd.mkdir(parents=True, exist_ok=True)
    _write_json(sd / "arm.json", record)
    _write_json(sd / "agent_nonces.json", {"run_nonce": record["run_nonce"], "roles": {}})
    (sd / "events.jsonl").write_text("")
    for stale in (sd / "derived.json", sd / "failure.json"):
        if stale.exists():
            stale.unlink()
    return record


def current_binding(root: Path, arm: dict[str, Any]) -> tuple[bool, str | None]:
    manifest_path = root / "docs/governance/GATE0_ADMISSION_MANIFEST.json"
    manifest = load_manifest(root)
    return validate_arm_binding(
        arm,
        current_branch=_run(root, "git", "branch", "--show-current"),
        current_head=_run(root, "git", "rev-parse", "HEAD"),
        current_manifest_sha256=sha256_file(manifest_path),
        current_guarded_hashes=guarded_hashes(root, manifest),
        current_worktree_clean=not bool(
            _run(root, "git", "status", "--porcelain=v1", "--untracked-files=all")
        ),
    )


def derive_repository() -> dict[str, Any]:
    root = repo_root()
    arm = load_arm(root)
    ok, failure = current_binding(root, arm)
    if not ok:
        raise Gate0Error(f"armed binding invalid: {failure}")
    events = load_events(root)
    recorded_failure = load_failure(root)
    if recorded_failure is not None:
        result = {
            "passed": False,
            "first_failure": str(recorded_failure.get("stage") or "GATE0_FAILURE"),
            "evidence_sha256": _evidence_digest(events),
            "failure_record_sha256": sha256_file(state_dir(root) / "failure.json"),
        }
    else:
        result = derive_attestation(arm, events)
    _write_json(state_dir(root) / "derived.json", result)
    return result


def seal_repository() -> dict[str, Any]:
    root = repo_root()
    arm = load_arm(root)
    if arm.get("state") != "ARMED":
        raise Gate0Error("Gate 0 arm is not in ARMED state")
    result = derive_repository()
    if result.get("passed") is not True:
        raise Gate0Error(f"cannot seal failed Gate 0 evidence: {result.get('first_failure')}")
    arm["state"] = "SEALED"
    arm["sealed_at_utc"] = _utcnow()
    _write_json(state_dir(root) / "arm.json", arm)
    return arm


def admit_repository() -> dict[str, Any]:
    root = repo_root()
    arm = load_arm(root)
    binding_ok, _ = current_binding(root, arm)
    derived = _read_json(state_dir(root) / "derived.json")
    recomputed = derive_attestation(arm, load_events(root))
    validate_final_admission_evidence(
        arm, derived=derived, recomputed=recomputed, binding_ok=binding_ok
    )
    record = build_admission_record(
        arm=arm,
        derived=derived,
        admission_id=f"GATE0-{arm['run_nonce'][:12]}",
        admitted_at_utc=_utcnow(),
    )
    dest = root / "docs/governance/admissions" / f"{record['admission_id']}.json"
    _write_json(dest, record)
    state_path = root / "docs/governance/ADMITTED_STATE.json"
    state = _read_json(state_path)
    state.update(
        {
            "operational_status": "GATE0_PASS",
            "active_gate": "GATE1A",
            "candidate_control_commit": arm["head"],
            "gate0_proven_commit": arm["head"],
            "latest_admission_id": record["admission_id"],
            "first_blocker": None,
        }
    )
    _write_json(state_path, state)
    return record


def validate_admission_control_commit(
    root: Path,
    *,
    proven_commit: str,
    control_commit: str,
    admission_id: str,
) -> None:
    """Prove the post-admission Git commit contains only admitted control-state bytes."""
    parent = _run(root, "git", "rev-parse", f"{control_commit}^")
    if parent != proven_commit:
        raise Gate0Error("Gate 0 admission-control commit parent is not the proven commit")
    admission_path = f"docs/governance/admissions/{admission_id}.json"
    expected_paths = {"docs/governance/ADMITTED_STATE.json", admission_path}
    changed_paths = set(
        subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", control_commit],
            cwd=root,
            text=True,
        ).splitlines()
    )
    if changed_paths != expected_paths:
        raise Gate0Error(
            "Gate 0 admission-control commit changed unexpected paths: "
            + ", ".join(sorted(changed_paths ^ expected_paths))
        )
    try:
        state = json.loads(
            subprocess.check_output(
                ["git", "show", f"{control_commit}:docs/governance/ADMITTED_STATE.json"],
                cwd=root,
            )
        )
        admission = json.loads(
            subprocess.check_output(
                ["git", "show", f"{control_commit}:{admission_path}"], cwd=root
            )
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise Gate0Error("Gate 0 admission-control commit contains invalid state") from exc
    if state.get("operational_status") != "GATE0_PASS":
        raise Gate0Error("admission-control state does not record GATE0_PASS")
    if state.get("active_gate") != "GATE1A":
        raise Gate0Error("admission-control state does not unlock Gate 1A")
    if state.get("candidate_control_commit") != proven_commit:
        raise Gate0Error("admission-control state candidate does not bind the proven commit")
    if state.get("gate0_proven_commit") != proven_commit:
        raise Gate0Error("admission-control state Gate 0 proof does not bind the proven commit")
    if state.get("latest_admission_id") != admission_id:
        raise Gate0Error("admission-control state does not bind the Gate 0 admission ID")
    if admission.get("admission_id") != admission_id:
        raise Gate0Error("admission-control record ID mismatch")
    if admission.get("disposition") != "GATE0_PASS":
        raise Gate0Error("admission-control record is not a Gate 0 PASS")
    if admission.get("proven_commit") != proven_commit:
        raise Gate0Error("admission-control record does not bind the proven commit")


def commit_admission_control() -> dict[str, Any]:
    """Advance accepted Git state after explicit Gate 0 admission, from ordinary WSL only."""
    root = repo_root()
    arm = load_arm(root)
    if arm.get("state") != "SEALED":
        raise Gate0Error("Gate 0 must be SEALED before admission-control commit")
    proven_commit = arm["head"]
    if _run(root, "git", "rev-parse", "HEAD") != proven_commit:
        raise Gate0Error("Git HEAD changed before Gate 0 admission-control commit")
    admission_id = f"GATE0-{arm['run_nonce'][:12]}"
    admission_path = f"docs/governance/admissions/{admission_id}.json"
    expected_paths = {"docs/governance/ADMITTED_STATE.json", admission_path}
    status_lines = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, text=True
    ).splitlines()
    changed_paths = {line[3:] for line in status_lines if len(line) >= 4}
    if changed_paths != expected_paths:
        raise Gate0Error(
            "Gate 0 admission worktree contains unexpected changes before control commit: "
            + ", ".join(sorted(changed_paths ^ expected_paths))
        )
    record = _read_json(root / admission_path)
    state = _read_json(root / "docs/governance/ADMITTED_STATE.json")
    manifest = load_manifest(root)
    binding_ok, binding_failure = validate_arm_binding(
        arm,
        current_branch=_run(root, "git", "branch", "--show-current"),
        current_head=proven_commit,
        current_manifest_sha256=sha256_file(
            root / "docs/governance/GATE0_ADMISSION_MANIFEST.json"
        ),
        current_guarded_hashes=guarded_hashes(root, manifest),
        # The only worktree dirtiness at this phase is the expected admission/state pair,
        # which was checked exactly above.  Do not let that expected transition invalidate
        # the otherwise unchanged arm binding.
        current_worktree_clean=True,
    )
    if not binding_ok:
        raise Gate0Error(f"Gate 0 binding changed before control commit: {binding_failure}")
    derived = _read_json(state_dir(root) / "derived.json")
    recomputed = derive_attestation(arm, load_events(root))
    validate_final_admission_evidence(
        arm, derived=derived, recomputed=recomputed, binding_ok=True
    )
    expected_record = build_admission_record(
        arm=arm,
        derived=derived,
        admission_id=admission_id,
        admitted_at_utc=record.get("admitted_at_utc", ""),
    )
    if record != expected_record:
        raise Gate0Error("Gate 0 admission record changed after evidence admission")
    try:
        base_state = json.loads(
            subprocess.check_output(
                ["git", "show", f"{proven_commit}:docs/governance/ADMITTED_STATE.json"],
                cwd=root,
            )
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise Gate0Error("cannot recover pre-admission ADMITTED_STATE from proven Git") from exc
    expected_state = dict(base_state)
    expected_state.update(
        {
            "operational_status": "GATE0_PASS",
            "active_gate": "GATE1A",
            "candidate_control_commit": proven_commit,
            "gate0_proven_commit": proven_commit,
            "latest_admission_id": admission_id,
            "first_blocker": None,
        }
    )
    if state != expected_state:
        raise Gate0Error("ADMITTED_STATE changed beyond the authorised Gate 0 transition")

    subprocess.run(["git", "add", "--", *sorted(expected_paths)], cwd=root, check=True)
    staged = set(
        subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], cwd=root, text=True
        ).splitlines()
    )
    if staged != expected_paths:
        raise Gate0Error("staged Gate 0 admission-control paths are incomplete or contaminated")
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=NVDA Gate 0 Control",
            "-c",
            "user.email=nvda-gate0@local.invalid",
            "commit",
            "-m",
            f"governance: admit Gate 0 {admission_id}",
        ],
        cwd=root,
        check=True,
    )
    control_commit = _run(root, "git", "rev-parse", "HEAD")
    validate_admission_control_commit(
        root,
        proven_commit=proven_commit,
        control_commit=control_commit,
        admission_id=admission_id,
    )
    if _run(root, "git", "status", "--porcelain=v1", "--untracked-files=all"):
        raise Gate0Error("worktree is not clean after Gate 0 admission-control commit")
    arm["state"] = "ADMITTED"
    arm["admission_control_commit"] = control_commit
    arm["admitted_at_utc"] = _utcnow()
    _write_json(state_dir(root) / "arm.json", arm)
    return {
        "admission_id": admission_id,
        "proven_commit": proven_commit,
        "admission_control_commit": control_commit,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["arm", "derive", "seal", "admit", "commit-admission"]
    )
    args = parser.parse_args(argv)
    try:
        if args.action == "arm":
            result = arm_repository()
        elif args.action == "derive":
            result = derive_repository()
            if result.get("passed") is not True:
                print(json.dumps(result, sort_keys=True))
                return 2
        elif args.action == "seal":
            result = seal_repository()
        elif args.action == "admit":
            result = admit_repository()
        else:
            result = commit_admission_control()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (Gate0Error, subprocess.CalledProcessError, OSError, ValueError, KeyError) as exc:
        print(f"GATE0_FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
