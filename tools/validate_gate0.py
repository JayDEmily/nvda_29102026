from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml


class ValidationError(RuntimeError):
    pass


def root_path() -> Path:
    return Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    ).resolve()


def runtime_module(root: Path):
    path = root / "tools/gate0_runtime_evidence.py"
    spec = importlib.util.spec_from_file_location("gate0_runtime_evidence", path)
    if not spec or not spec.loader:
        raise ValidationError("cannot load Gate 0 runtime evidence module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_static(root: Path, *, require_clean: bool = True) -> None:
    if require_clean:
        status = subprocess.check_output(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, text=True
        )
        if status.strip():
            raise ValidationError("worktree is not clean")
    manifest = json.loads((root / "docs/governance/GATE0_ADMISSION_MANIFEST.json").read_text())
    if manifest.get("immediate_roles") != ["integration_auditor", "semantic_reviewer"]:
        raise ValidationError("immediate role set is not the admitted Gate 0 set")
    policy = manifest.get("runtime_policy", {})
    if policy.get("sandbox_mode") != "read-only" or policy.get("approval_policy") != "on-request":
        raise ValidationError("Gate 0 permission policy mismatch")
    if (
        manifest.get("closure_actor") != "ordinary_wsl"
        or manifest.get("automatic_final_subagent_stop_closure") is not False
    ):
        raise ValidationError("Gate 0 closure policy mismatch")
    config = tomllib.loads((root / ".codex/config.toml").read_text())
    if config.get("sandbox_mode") != "read-only" or config.get("approval_policy") != "on-request":
        raise ValidationError("project Codex permission defaults mismatch")
    for role in ("integration-auditor", "semantic-reviewer"):
        data = tomllib.loads((root / ".codex/agents" / f"{role}.toml").read_text())
        if data.get("sandbox_mode") != "read-only":
            raise ValidationError(f"{role} is not read-only")
    hooks = json.loads((root / ".codex/hooks.json").read_text()).get("hooks", {})
    for event in ("SessionStart", "SubagentStart", "PreToolUse", "PostToolUse", "SubagentStop"):
        if event not in hooks:
            raise ValidationError(f"missing hook event: {event}")
    meta = yaml.safe_load(
        (root / ".agents/skills/nvda-semantic-orchestrator/agents/openai.yaml").read_text()
    )
    if meta.get("policy", {}).get("allow_implicit_invocation") is not False:
        raise ValidationError("semantic skill implicit invocation is not disabled")
    for rel in manifest.get("guarded_paths", []):
        if not (root / rel).is_file():
            raise ValidationError(f"guarded path missing: {rel}")


def validate_runtime(root: Path) -> None:
    rt = runtime_module(root)
    arm = rt.load_arm(root)
    ok, failure = rt.current_binding(root, arm)
    if not ok:
        raise ValidationError(f"armed binding mismatch: {failure}")
    derived_path = rt.state_dir(root) / "derived.json"
    if not derived_path.is_file():
        raise ValidationError("derived Gate 0 evidence is absent")
    derived = json.loads(derived_path.read_text())
    if derived.get("passed") is not True:
        raise ValidationError(f"Gate 0 evidence failed: {derived.get('first_failure')}")
    recomputed = rt.derive_attestation(arm, rt.load_events(root))
    if recomputed != derived:
        raise ValidationError("derived evidence does not match protected journal")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--static", action="store_true")
    group.add_argument("--runtime", action="store_true")
    args = parser.parse_args(argv)
    root = root_path()
    try:
        if args.static:
            validate_static(root)
        else:
            validate_runtime(root)
        print("PASS: Gate 0 validation")
        return 0
    except (ValidationError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
