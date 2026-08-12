from __future__ import annotations

import importlib.util
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / ".codex/hooks/gate0_attest.py"
HOOKS_PATH = ROOT / ".codex/hooks.json"
CONFIG_PATH = ROOT / ".codex/config.toml"
RUNTIME_PATH = ROOT / "tools/gate0_runtime_evidence.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime():
    return load_module(RUNTIME_PATH, "gate0_runtime_evidence_policy_test")


def hook():
    return load_module(HOOK_PATH, "gate0_attest_policy_test")


def event(type_: str, **kwargs):
    return {"type": type_, "run_nonce": "run-1", **kwargs}


def test_pretool_denial_uses_supported_hook_specific_shape():
    value = hook().deny_pretool("no")
    assert value == {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "no",
        }
    }
    assert "continue" not in value


def test_posttool_failure_uses_supported_stop_shape_not_block_decision():
    value = hook().stop_posttool("stop")
    assert value["continue"] is False
    assert value["stopReason"] == "stop"
    assert "decision" not in value


def test_pre_and_post_tool_hooks_cover_all_supported_local_tools():
    hooks = json.loads(HOOKS_PATH.read_text())["hooks"]
    assert all(group.get("matcher") == "*" for group in hooks["PreToolUse"])
    assert all(group.get("matcher") == "*" for group in hooks["PostToolUse"])


def test_gate0_config_removes_known_hosted_and_app_tool_surfaces():
    config = tomllib.loads(CONFIG_PATH.read_text())
    assert config["web_search"] == "disabled"
    assert config["tools"]["view_image"] is False
    assert config["apps"]["_default"]["enabled"] is False
    assert config["features"]["apps"] is False
    assert config["features"]["remote_plugin"] is False


def test_spawn_policy_requires_explicit_agent_type_not_task_name_alias():
    module = hook()
    assert module.spawn_agent_role({"agent_type": "integration_auditor"}) == "integration_auditor"
    assert module.spawn_agent_role({"task_name": "integration_auditor"}) is None
    assert module.spawn_agent_role({"message": "integration_auditor"}) is None


def test_spawn_order_has_explicit_pre_spawn_boundary_for_each_role():
    module = runtime()
    events = [
        event("SessionStart", head="a" * 40, cwd="/repo", source="startup"),
        event("ProbeResult", role="__parent__", passed=True),
    ]
    assert module.expected_next_spawn_role(events, run_nonce="run-1") == "integration_auditor"
    events.extend(
        [
            event("SpawnRequest", role="integration_auditor"),
            event("SubagentStart", role="integration_auditor", agent_id="a"),
            event("ProbeResult", role="integration_auditor", agent_id="a", passed=True),
            event("SubagentStop", role="integration_auditor", agent_id="a"),
        ]
    )
    assert module.expected_next_spawn_role(events, run_nonce="run-1") == "semantic_reviewer"


def test_recorded_gate0_failure_is_non_admissible_evidence():
    module = runtime()
    arm = {"run_nonce": "run-1", "head": "a" * 40, "repo_root": "/repo"}
    events = [
        event("SessionStart", head="a" * 40, cwd="/repo", source="startup"),
        event("ProbeResult", role="__parent__", passed=True),
        event("Gate0Failure", stage="UNEXPECTED_LOCAL_TOOL:apply_patch", reason="blocked"),
    ]
    result = module.derive_attestation(arm, events)
    assert result["passed"] is False
    assert result["first_failure"] == "UNEXPECTED_LOCAL_TOOL:apply_patch"
