from __future__ import annotations

import importlib.util
import io
import json
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / ".codex/hooks/gate0_attest.py"
HOOKS_PATH = ROOT / ".codex/hooks.json"
CONFIG_PATH = ROOT / ".codex/config.toml"
RUNTIME_PATH = ROOT / "tools/gate0_runtime_evidence.py"
VALIDATOR_PATH = ROOT / "tools/validate_gate0.py"
MANIFEST_PATH = ROOT / "docs/governance/GATE0_ADMISSION_MANIFEST.json"


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


def validator():
    return load_module(VALIDATOR_PATH, "validate_gate0_policy_test")


def declared_policy_inputs():
    manifest = json.loads(MANIFEST_PATH.read_text())
    config = tomllib.loads(CONFIG_PATH.read_text())
    hooks = json.loads(HOOKS_PATH.read_text())["hooks"]
    return manifest, config, hooks


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
    assert config["default_permissions"] == ":read-only"
    assert "sandbox_mode" not in config
    assert "sandbox_workspace_write" not in config
    assert config["web_search"] == "disabled"
    assert config["tools"]["view_image"] is False
    assert config["apps"]["_default"]["enabled"] is False
    assert config["features"]["apps"] is False
    assert config["features"]["remote_plugin"] is False
    for role in ("integration-auditor", "semantic-reviewer"):
        agent = tomllib.loads((ROOT / ".codex/agents" / f"{role}.toml").read_text())
        assert agent["default_permissions"] == ":read-only"
        assert "sandbox_mode" not in agent
        assert "sandbox_workspace_write" not in agent


def run_sessionstart(monkeypatch, *, permission_mode):
    module = hook()
    outputs = []
    failures = []
    events = []
    payload = {
        "hook_event_name": "SessionStart",
        "session_id": "session-1",
        "cwd": "/repo",
        "permission_mode": permission_mode,
        "source": "startup",
    }
    arm = {"run_nonce": "run-1", "head": "a" * 40}
    monkeypatch.setattr(module.sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(module, "output", outputs.append)
    monkeypatch.setattr(module.rt, "repo_root", lambda: Path("/repo"))
    monkeypatch.setattr(module.rt, "load_active_arm", lambda root: arm)
    monkeypatch.setattr(module.rt, "current_binding", lambda root, value: (True, None))
    monkeypatch.setattr(module.rt, "load_failure", lambda root: None)
    monkeypatch.setattr(module.rt, "append_event", lambda root, value: events.append(value))
    monkeypatch.setattr(
        module.rt,
        "record_failure",
        lambda root, stage, reason: failures.append((stage, reason)),
    )
    monkeypatch.setattr(
        module.rt,
        "expected_probe_commands",
        lambda root, value: {"__parent__": "exact-probe"},
    )
    assert module.main() == 0
    return outputs, failures, events


def test_sessionstart_accepts_default_permission_mode_but_still_requires_probe(monkeypatch):
    outputs, failures, events = run_sessionstart(monkeypatch, permission_mode="default")
    assert failures == []
    assert events[0]["permission_mode"] == "default"
    assert "exact-probe" in outputs[0]["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize(
    "permission_mode", ["acceptEdits", "plan", "dontAsk", "bypassPermissions", None]
)
def test_sessionstart_fails_before_probe_for_incompatible_permission_mode(
    monkeypatch, permission_mode
):
    outputs, failures, events = run_sessionstart(
        monkeypatch, permission_mode=permission_mode
    )
    assert events[0]["permission_mode"] == permission_mode
    assert failures[0][0] == "SESSION_PERMISSION_MODE"
    assert outputs[0]["continue"] is False
    assert "exact-probe" not in json.dumps(outputs[0])


def test_spawn_policy_requires_explicit_agent_type_not_task_name_alias():
    module = hook()
    assert module.spawn_agent_role({"agent_type": "integration_auditor"}) == "integration_auditor"
    assert module.spawn_agent_role({"task_name": "integration_auditor"}) is None
    assert module.spawn_agent_role({"message": "integration_auditor"}) is None


def run_pretool(monkeypatch, *, tool_name, tool_input):
    module = hook()
    outputs = []
    failures = []
    events = []
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_use_id": "tool-1",
    }
    monkeypatch.setattr(module.sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(module, "output", outputs.append)
    monkeypatch.setattr(module.rt, "repo_root", lambda: Path("/repo"))
    monkeypatch.setattr(module.rt, "load_active_arm", lambda root: {"run_nonce": "run-1"})
    monkeypatch.setattr(module.rt, "current_binding", lambda root, arm: (True, None))
    monkeypatch.setattr(module.rt, "load_failure", lambda root: None)
    monkeypatch.setattr(module.rt, "load_events", lambda root: [])
    monkeypatch.setattr(module.rt, "wait_agent_allowed", lambda current_events, run_nonce: True)
    monkeypatch.setattr(
        module.rt,
        "expected_next_spawn_role",
        lambda current_events, run_nonce: "integration_auditor",
    )
    monkeypatch.setattr(module.rt, "append_event", lambda root, value: events.append(value))
    monkeypatch.setattr(
        module.rt,
        "record_failure",
        lambda root, stage, reason: failures.append((stage, reason)),
    )
    assert module.main() == 0
    return outputs, failures, events


def run_posttool(monkeypatch, *, tool_name):
    module = hook()
    outputs = []
    failures = []
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": tool_name,
        "tool_input": {},
        "tool_use_id": "tool-1",
    }
    monkeypatch.setattr(module.sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(module, "output", outputs.append)
    monkeypatch.setattr(module.rt, "repo_root", lambda: Path("/repo"))
    monkeypatch.setattr(module.rt, "load_active_arm", lambda root: {"run_nonce": "run-1"})
    monkeypatch.setattr(module.rt, "current_binding", lambda root, arm: (True, None))
    monkeypatch.setattr(module.rt, "load_failure", lambda root: None)
    monkeypatch.setattr(
        module.rt,
        "record_failure",
        lambda root, stage, reason: failures.append((stage, reason)),
    )
    assert module.main() == 0
    return outputs, failures


def test_observed_namespaced_spawn_is_canonicalised_and_keeps_exact_role_check(monkeypatch):
    outputs, failures, events = run_pretool(
        monkeypatch,
        tool_name="collaborationspawn_agent",
        tool_input={"agent_type": "integration_auditor"},
    )
    assert failures == []
    assert events == [
        {
            "type": "SpawnRequest",
            "role": "integration_auditor",
            "run_nonce": "run-1",
            "tool_use_id": "tool-1",
        }
    ]
    assert outputs[0]["hookSpecificOutput"]["hookEventName"] == "PreToolUse"


def test_namespaced_spawn_with_wrong_role_is_denied(monkeypatch):
    outputs, failures, events = run_pretool(
        monkeypatch,
        tool_name="collaborationspawn_agent",
        tool_input={"agent_type": "semantic_reviewer"},
    )
    assert events == []
    assert failures[0][0] == "SPAWN_REQUEST:integration_auditor"
    assert outputs[0]["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_current_namespaced_wait_is_canonicalised_without_broadening_policy(monkeypatch):
    outputs, failures, events = run_pretool(
        monkeypatch,
        tool_name="collaborationwait_agent",
        tool_input={"timeout_ms": 10_000},
    )
    assert failures == []
    assert events == [
        {
            "type": "PreToolUse",
            "role": "__orchestration__",
            "run_nonce": "run-1",
            "tool_use_id": "tool-1",
            "tool_name": "wait_agent",
        }
    ]
    assert outputs[0]["hookSpecificOutput"]["hookEventName"] == "PreToolUse"


@pytest.mark.parametrize(
    "tool_name",
    [
        "collaborationfollowup_task",
        "collaborationinterrupt_agent",
        "collaborationspawn_agent_extra",
        "prefix_collaborationspawn_agent",
        "collaborationspawn_agent_suffix",
    ],
)
def test_arbitrary_collaboration_and_spawn_lookalikes_are_denied(monkeypatch, tool_name):
    outputs, failures, events = run_pretool(
        monkeypatch,
        tool_name=tool_name,
        tool_input={"agent_type": "integration_auditor"},
    )
    assert events == []
    assert failures[0][0] == f"UNEXPECTED_LOCAL_TOOL:{tool_name}"
    assert outputs[0]["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_namespaced_aliases_are_exact():
    module = hook()
    assert module.canonical_tool_name("collaborationspawn_agent") == "spawn_agent"
    assert module.canonical_tool_name("collaborationwait_agent") == "wait_agent"
    for lookalike in (
        "collaborationwait_agent_extra",
        "prefix_collaborationwait_agent",
        "collaborationwait_agent_suffix",
    ):
        assert module.canonical_tool_name(lookalike) == lookalike


@pytest.mark.parametrize("tool_name", ["collaborationspawn_agent", "collaborationwait_agent"])
def test_posttool_uses_the_same_exact_namespaced_canonicalisation(monkeypatch, tool_name):
    outputs, failures = run_posttool(monkeypatch, tool_name=tool_name)
    assert failures == []
    assert outputs == [{}]


def test_posttool_namespaced_lookalike_remains_denied(monkeypatch):
    tool_name = "collaborationspawn_agent_suffix"
    outputs, failures = run_posttool(monkeypatch, tool_name=tool_name)
    assert failures[0][0] == f"UNEXPECTED_POST_TOOL:{tool_name}"
    assert outputs[0]["continue"] is False


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


def test_wait_agent_is_allowed_only_while_the_exact_authorised_child_is_in_progress():
    module = runtime()
    events = [
        event("SessionStart", head="a" * 40, cwd="/repo", source="startup"),
        event("ProbeResult", role="__parent__", passed=True),
        event("SpawnRequest", role="integration_auditor"),
    ]
    assert module.wait_agent_allowed(events, run_nonce="run-1") is True
    events.extend(
        [
            event("SubagentStart", role="integration_auditor", agent_id="a"),
            event("ProbeResult", role="integration_auditor", agent_id="a", passed=True),
            event("SubagentStop", role="integration_auditor", agent_id="a"),
        ]
    )
    assert module.wait_agent_allowed(events, run_nonce="run-1") is False


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


def test_static_validator_composes_full_declared_gate0_tool_policy():
    module = validator()
    manifest, config, hooks = declared_policy_inputs()
    module.validate_declared_runtime_policy(manifest, config, hooks)


def test_static_validator_rejects_reenabled_tool_surface():
    module = validator()
    manifest, config, hooks = declared_policy_inputs()
    config["features"]["apps"] = True
    try:
        module.validate_declared_runtime_policy(manifest, config, hooks)
    except module.ValidationError as exc:
        assert "apps feature" in str(exc)
    else:
        raise AssertionError("Gate 0 static validator accepted re-enabled apps")


def test_static_validator_rejects_mixed_permission_configuration():
    module = validator()
    manifest, config, hooks = declared_policy_inputs()
    config["sandbox_mode"] = "read-only"
    with pytest.raises(module.ValidationError, match="mixes permission profiles"):
        module.validate_declared_runtime_policy(manifest, config, hooks)


def test_static_validator_rejects_narrowed_pretool_matcher():
    module = validator()
    manifest, config, hooks = declared_policy_inputs()
    hooks["PreToolUse"][0]["matcher"] = "Bash"
    try:
        module.validate_declared_runtime_policy(manifest, config, hooks)
    except module.ValidationError as exc:
        assert "PreToolUse" in str(exc)
    else:
        raise AssertionError("Gate 0 static validator accepted incomplete local-tool coverage")
