from __future__ import annotations

import argparse
import hashlib
import json
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
) -> tuple[bool, str | None]:
    if arm.get("branch") != current_branch:
        return False, "BRANCH"
    if arm.get("head") != current_head:
        return False, "HEAD"
    if arm.get("manifest_sha256") != current_manifest_sha256:
        return False, "MANIFEST_HASH"
    if arm.get("guarded_hashes") != dict(sorted(current_guarded_hashes.items())):
        return False, "GUARDED_HASHES"
    return True, None


def _evidence_digest(events: list[dict[str, Any]]) -> str:
    return _sha256_bytes(json.dumps(events, sort_keys=True, separators=(",", ":")).encode())


def derive_attestation(arm: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    run_nonce = arm.get("run_nonce")
    head = arm.get("head")
    evidence = [e for e in events if e.get("type") not in {"PreToolUse", "PostToolUse"}]

    def fail(name: str) -> dict[str, Any]:
        return {"passed": False, "first_failure": name, "evidence_sha256": _evidence_digest(events)}

    if not evidence or evidence[0].get("type") != "SessionStart":
        return fail("SESSION_START")
    session = evidence[0]
    if session.get("run_nonce") != run_nonce or session.get("head") != head:
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
            f"{py} -B {probe} --role __parent__ "
            f"--nonce {run_nonce} --run-nonce {run_nonce}"
        )
    }
    nonces_path = state_dir(root) / "agent_nonces.json"
    if nonces_path.is_file():
        data = _read_json(nonces_path)
        for role, item in data.get("roles", {}).items():
            result[role] = (
                f"{py} -B {probe} --role {role} "
                f"--nonce {item['nonce']} --run-nonce {run_nonce}"
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
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise Gate0Error("Gate 0 programme policy requires Linux x86_64")
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
    for stale in (sd / "derived.json",):
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
    )


def derive_repository() -> dict[str, Any]:
    root = repo_root()
    arm = load_arm(root)
    ok, failure = current_binding(root, arm)
    if not ok:
        raise Gate0Error(f"armed binding invalid: {failure}")
    result = derive_attestation(arm, load_events(root))
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
    if arm.get("state") != "SEALED":
        raise Gate0Error("Gate 0 must be SEALED before admission")
    derived = _read_json(state_dir(root) / "derived.json")
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["arm", "derive", "seal", "admit"])
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
        else:
            result = admit_repository()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (Gate0Error, subprocess.CalledProcessError, OSError, ValueError, KeyError) as exc:
        print(f"GATE0_FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
