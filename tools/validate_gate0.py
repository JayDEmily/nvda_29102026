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


def validate_declared_runtime_policy(manifest: dict, config: dict, hooks: dict) -> None:
    policy = manifest.get("runtime_policy", {})
    if policy.get("sandbox_mode") != "read-only" or policy.get("approval_policy") != "on-request":
        raise ValidationError("Gate 0 permission policy mismatch")
    if config.get("sandbox_mode") != policy["sandbox_mode"]:
        raise ValidationError("project Codex sandbox mode does not match Gate 0 policy")
    if config.get("approval_policy") != policy["approval_policy"]:
        raise ValidationError("project Codex approval policy does not match Gate 0 policy")
    if config.get("web_search") != policy.get("web_search"):
        raise ValidationError("project Codex web-search policy does not match Gate 0 policy")
    if config.get("tools", {}).get("view_image") is not policy.get("view_image_enabled"):
        raise ValidationError("project Codex view_image policy does not match Gate 0 policy")
    if config.get("apps", {}).get("_default", {}).get("enabled") is not policy.get("apps_enabled"):
        raise ValidationError("project Codex app policy does not match Gate 0 policy")
    if config.get("features", {}).get("apps") is not policy.get("apps_enabled"):
        raise ValidationError("project Codex apps feature does not match Gate 0 policy")
    if config.get("features", {}).get("remote_plugin") is not False:
        raise ValidationError("remote plugin catalogue must be disabled for Gate 0")
    if policy.get("pretool_matcher") != "*":
        raise ValidationError(
            "Gate 0 policy does not require full supported local-tool hook coverage"
        )
    for event in ("PreToolUse", "PostToolUse"):
        groups = hooks.get(event, [])
        if not groups or any(group.get("matcher") != "*" for group in groups):
            raise ValidationError(f"{event} does not match every supported local tool")
    if policy.get("spawn_must_name_exact_agent_type") is not True:
        raise ValidationError("Gate 0 policy does not require exact custom agent_type at spawn")
    if policy.get("known_hook_exempt_specialised_tools_must_be_absent_or_gate0_blocks") is not True:
        raise ValidationError("Gate 0 policy does not fail closed on hook-exempt specialised tools")
    expected_live_tools = [
        "Bash:exact_nonce_bound_probe_only",
        "spawn_agent:exact_next_agent_type_only",
        "wait_agent:authorised_child_only",
    ]
    if manifest.get("allowed_live_local_tools") != expected_live_tools:
        raise ValidationError("Gate 0 allowed live local-tool set is not the admitted minimal set")


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
    if (
        manifest.get("closure_actor") != "ordinary_wsl"
        or manifest.get("automatic_final_subagent_stop_closure") is not False
    ):
        raise ValidationError("Gate 0 closure policy mismatch")
    config = tomllib.loads((root / ".codex/config.toml").read_text())
    for role in ("integration-auditor", "semantic-reviewer"):
        data = tomllib.loads((root / ".codex/agents" / f"{role}.toml").read_text())
        if data.get("sandbox_mode") != "read-only":
            raise ValidationError(f"{role} is not read-only")
    hooks = json.loads((root / ".codex/hooks.json").read_text()).get("hooks", {})
    for event in ("SessionStart", "SubagentStart", "PreToolUse", "PostToolUse", "SubagentStop"):
        if event not in hooks:
            raise ValidationError(f"missing hook event: {event}")
    validate_declared_runtime_policy(manifest, config, hooks)
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
