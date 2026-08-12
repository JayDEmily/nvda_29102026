from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs/governance/GATE0_ADMISSION_MANIFEST.json"
BOOTSTRAP = ROOT / "docs/orchestration/BOOTSTRAP.md"
RUNTIME_PATH = ROOT / "tools/gate0_runtime_evidence.py"
VALIDATOR_PATH = ROOT / "tools/validate_gate0.py"


def load_runtime():
    assert RUNTIME_PATH.is_file(), (
        "Unit 4 seam: tools/gate0_runtime_evidence.py is not implemented yet"
    )
    spec = importlib.util.spec_from_file_location("gate0_runtime_evidence", RUNTIME_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arm():
    return {
        "run_nonce": "run-1",
        "branch": "restart/codex-control-v1",
        "head": "a" * 40,
        "manifest_sha256": "b" * 64,
        "guarded_hashes": {"AGENTS.md": "c" * 64},
        "repo_root": "/repo",
    }


def valid_events():
    return [
        {
            "type": "SessionStart",
            "run_nonce": "run-1",
            "head": "a" * 40,
            "cwd": "/repo",
            "source": "startup",
        },
        {"type": "ProbeResult", "role": "__parent__", "run_nonce": "run-1", "passed": True},
        {
            "type": "SubagentStart",
            "role": "integration_auditor",
            "agent_id": "agent-a",
            "run_nonce": "run-1",
        },
        {
            "type": "ProbeResult",
            "role": "integration_auditor",
            "agent_id": "agent-a",
            "run_nonce": "run-1",
            "passed": True,
        },
        {
            "type": "SubagentStop",
            "role": "integration_auditor",
            "agent_id": "agent-a",
            "run_nonce": "run-1",
        },
        {
            "type": "SubagentStart",
            "role": "semantic_reviewer",
            "agent_id": "agent-b",
            "run_nonce": "run-1",
        },
        {
            "type": "ProbeResult",
            "role": "semantic_reviewer",
            "agent_id": "agent-b",
            "run_nonce": "run-1",
            "passed": True,
        },
        {
            "type": "SubagentStop",
            "role": "semantic_reviewer",
            "agent_id": "agent-b",
            "run_nonce": "run-1",
        },
    ]


def derive(events):
    return load_runtime().derive_attestation(arm(), events)


def test_manifest_fixes_minimal_gate0_policy():
    data = json.loads(MANIFEST_PATH.read_text())
    assert data["runtime_policy"]["sandbox_mode"] == "read-only"
    assert data["runtime_policy"]["approval_policy"] == "on-request"
    assert data["immediate_roles"] == ["integration_auditor", "semantic_reviewer"]
    assert data["closure_actor"] == "ordinary_wsl"
    assert data["automatic_final_subagent_stop_closure"] is False
    assert {"semantic_index_completion", "prompt_cache_calibration", "r2a_rollback"} <= set(
        data["forbidden_gate0_dependencies"]
    )


def test_bootstrap_assigns_final_closure_to_ordinary_wsl():
    text = BOOTSTRAP.read_text()
    assert "**STOP** the live Gate 0 interaction" in text
    assert "ordinary WSL closure and admission" in text
    assert "automatic final-`SubagentStop` closure" in text


def test_valid_event_chain_can_be_derived():
    result = derive(valid_events())
    assert result["passed"] is True
    assert result["first_failure"] is None


def test_stale_nonce_fails():
    events = valid_events()
    events[0]["run_nonce"] = "old"
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "SESSION_START"


def test_missing_session_start_fails():
    result = derive(valid_events()[1:])
    assert result["passed"] is False and result["first_failure"] == "SESSION_START"


def test_missing_parent_probe_fails():
    events = [valid_events()[0], *valid_events()[2:]]
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "PARENT_PROBE"


def test_missing_first_subagent_start_fails_at_exact_invariant():
    result = derive(valid_events()[:2])
    assert (
        result["passed"] is False
        and result["first_failure"] == "SUBAGENT_START:integration_auditor"
    )


def test_wrong_first_role_fails():
    events = valid_events()
    events[2]["role"] = "semantic_reviewer"
    result = derive(events)
    assert (
        result["passed"] is False
        and result["first_failure"] == "SUBAGENT_START:integration_auditor"
    )


def test_duplicate_child_identity_fails():
    events = valid_events()
    events[5]["agent_id"] = "agent-a"
    events[6]["agent_id"] = "agent-a"
    events[7]["agent_id"] = "agent-a"
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "DISTINCT_CHILD_IDENTITY"


def test_child_probe_failure_fails():
    events = valid_events()
    events[3]["passed"] = False
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "PROBE:integration_auditor"


def test_missing_subagent_stop_fails():
    events = valid_events()
    del events[4]
    result = derive(events)
    assert (
        result["passed"] is False and result["first_failure"] == "SUBAGENT_STOP:integration_auditor"
    )


def test_unexpected_extra_role_event_fails():
    events = valid_events()
    events.append(
        {
            "type": "SubagentStart",
            "role": "implementation_worker",
            "agent_id": "extra",
            "run_nonce": "run-1",
        }
    )
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "UNEXPECTED_EVENT"


def test_duplicate_expected_role_event_fails():
    events = valid_events()
    events.insert(3, {**events[2], "agent_id": "duplicate-agent"})
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "PROBE:integration_auditor"


def test_changed_head_fails():
    events = valid_events()
    events[0]["head"] = "d" * 40
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "SESSION_START"


def test_model_status_json_cannot_create_pass():
    result = derive([{"type": "ModelStatus", "status": "GATE0_PASS", "run_nonce": "run-1"}])
    assert result["passed"] is False


def test_automatic_closure_is_disabled_in_production_contract():
    module = load_runtime()
    assert module.AUTOMATIC_FINAL_SUBAGENT_STOP_CLOSURE is False


def test_clean_arm_binds_head_manifest_and_guarded_hashes():
    module = load_runtime()
    record = module.make_arm_record(
        branch="restart/codex-control-v1",
        head="a" * 40,
        manifest_sha256="b" * 64,
        guarded_hashes={"AGENTS.md": "c" * 64},
        run_nonce="run-1",
        worktree_clean=True,
    )
    assert record["branch"] == "restart/codex-control-v1"
    assert record["head"] == "a" * 40
    assert record["manifest_sha256"] == "b" * 64
    assert record["guarded_hashes"] == {"AGENTS.md": "c" * 64}


def test_dirty_tree_cannot_arm():
    module = load_runtime()
    try:
        module.make_arm_record(
            branch="restart/codex-control-v1",
            head="a" * 40,
            manifest_sha256="b" * 64,
            guarded_hashes={"AGENTS.md": "c" * 64},
            run_nonce="run-1",
            worktree_clean=False,
        )
    except module.Gate0Error as exc:
        assert "dirty" in str(exc).lower()
    else:
        raise AssertionError("dirty tree was admitted")


def test_wrong_branch_fails_arm_binding():
    module = load_runtime()
    ok, failure = module.validate_arm_binding(
        arm(),
        current_branch="main",
        current_head="a" * 40,
        current_manifest_sha256="b" * 64,
        current_guarded_hashes={"AGENTS.md": "c" * 64},
        current_worktree_clean=True,
    )
    assert ok is False and failure == "BRANCH"


def test_changed_guarded_file_fails_arm_binding():
    module = load_runtime()
    ok, failure = module.validate_arm_binding(
        arm(),
        current_branch="restart/codex-control-v1",
        current_head="a" * 40,
        current_manifest_sha256="b" * 64,
        current_guarded_hashes={"AGENTS.md": "d" * 64},
        current_worktree_clean=True,
    )
    assert ok is False and failure == "GUARDED_HASHES"


def test_post_arm_dirty_worktree_invalidates_binding():
    module = load_runtime()
    ok, failure = module.validate_arm_binding(
        arm(),
        current_branch="restart/codex-control-v1",
        current_head="a" * 40,
        current_manifest_sha256="b" * 64,
        current_guarded_hashes={"AGENTS.md": "c" * 64},
        current_worktree_clean=False,
    )
    assert ok is False and failure == "WORKTREE_DIRTY"


def test_admission_record_binds_proven_commit_and_evidence_digest():
    module = load_runtime()
    record = module.build_admission_record(
        arm=arm(),
        derived={"passed": True, "evidence_sha256": "e" * 64},
        admission_id="GATE0-20260812-001",
        admitted_at_utc="2026-08-12T00:00:00Z",
    )
    assert record["proven_commit"] == "a" * 40
    assert record["evidence_sha256"] == "e" * 64
    assert record["manifest_sha256"] == "b" * 64
    assert record["guarded_hashes"] == {"AGENTS.md": "c" * 64}
    assert record["disposition"] == "GATE0_PASS"


def test_final_admission_requires_sealed_fresh_rederived_evidence():
    module = load_runtime()
    sealed_arm = {**arm(), "state": "SEALED"}
    derived = {"passed": True, "first_failure": None, "evidence_sha256": "e" * 64}
    module.validate_final_admission_evidence(
        sealed_arm, derived=derived, recomputed=dict(derived), binding_ok=True
    )
    try:
        module.validate_final_admission_evidence(
            {**sealed_arm, "state": "ARMED"},
            derived=derived,
            recomputed=dict(derived),
            binding_ok=True,
        )
    except module.Gate0Error as exc:
        assert "sealed" in str(exc).lower()
    else:
        raise AssertionError("unsealed Gate 0 evidence was admitted")
    try:
        module.validate_final_admission_evidence(
            sealed_arm,
            derived=derived,
            recomputed={**derived, "evidence_sha256": "f" * 64},
            binding_ok=True,
        )
    except module.Gate0Error as exc:
        assert "recomputed" in str(exc).lower()
    else:
        raise AssertionError("stale derived evidence was admitted")
    try:
        module.validate_final_admission_evidence(
            sealed_arm, derived=derived, recomputed=dict(derived), binding_ok=False
        )
    except module.Gate0Error as exc:
        assert "binding" in str(exc).lower()
    else:
        raise AssertionError("stale Git/control binding was admitted")


def test_runtime_validator_is_dedicated_gate0_surface():
    assert VALIDATOR_PATH.is_file(), "Unit 4 seam: tools/validate_gate0.py is not implemented yet"
    text = VALIDATOR_PATH.read_text().lower()
    for forbidden in ["prompt_cache", "orchestration_attempt", "r2a", "semantic_index.schema"]:
        assert forbidden not in text


def valid_probe_payload(*, role: str = "__parent__", nonce: str = "run-1") -> dict:
    return {
        "gate0_probe": True,
        "role": role,
        "nonce": nonce,
        "run_nonce": "run-1",
        "passed": True,
        "platform": {
            "system": "Linux",
            "machine": "x86_64",
            "wsl_distro": "Ubuntu-24.04",
            "kernel_release": "6.6.87.2-microsoft-standard-WSL2",
        },
        "repo_root": "/repo",
        "head": "a" * 40,
        "probes": {
            name: {"write_allowed": False}
            for name in ("repository", "git_metadata", "slash_tmp", "home")
        },
    }


def test_session_start_must_bind_exact_armed_root_and_startup_source():
    events = valid_events()
    events[0]["cwd"] = "/repo/subdir"
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "SESSION_START"
    events = valid_events()
    events[0]["source"] = "resume"
    result = derive(events)
    assert result["passed"] is False and result["first_failure"] == "SESSION_START"


def test_probe_payload_must_bind_role_nonce_run_head_root_platform_and_denials():
    module = load_runtime()
    probe = valid_probe_payload()
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=probe
    )
    assert ok is True and failure is None
    mutations = [
        ("role", "semantic_reviewer"),
        ("nonce", "wrong"),
        ("run_nonce", "wrong"),
        ("head", "d" * 40),
        ("repo_root", "/wrong"),
    ]
    for field, value in mutations:
        bad = json.loads(json.dumps(probe))
        bad[field] = value
        ok, failure = module.validate_probe_payload(
            arm(), role="__parent__", expected_nonce="run-1", probe=bad
        )
        assert ok is False and failure is not None
    bad = json.loads(json.dumps(probe))
    bad["platform"]["system"] = "Windows"
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=bad
    )
    assert ok is False and failure == "PLATFORM"
    bad = json.loads(json.dumps(probe))
    bad["probes"]["repository"]["write_allowed"] = True
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=bad
    )
    assert ok is False and failure == "WRITE_BOUNDARY"


def test_probe_pass_boolean_cannot_override_failed_mechanical_detail():
    module = load_runtime()
    probe = valid_probe_payload()
    probe["probes"]["git_metadata"]["write_allowed"] = True
    probe["passed"] = True
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=probe
    )
    assert ok is False and failure == "WRITE_BOUNDARY"


def test_hook_commands_resolve_from_git_root_not_session_subdirectory():
    hooks = json.loads((ROOT / ".codex/hooks.json").read_text())["hooks"]
    commands = {
        hook["command"] for groups in hooks.values() for group in groups for hook in group["hooks"]
    }
    assert commands == {'bash "$(git rev-parse --show-toplevel)/.codex/hooks/run_gate0_attest.sh"'}


def test_host_policy_requires_wsl2_and_native_linux_storage():
    module = load_runtime()
    module.validate_host_policy(
        system="Linux",
        machine="x86_64",
        wsl_distro="Ubuntu-24.04",
        kernel_release="6.6.87.2-microsoft-standard-WSL2",
        repo_root="/home/user/repo",
    )
    for kwargs in [
        {
            "system": "Linux",
            "machine": "x86_64",
            "wsl_distro": "",
            "kernel_release": "6.6.87.2-microsoft-standard-WSL2",
            "repo_root": "/home/user/repo",
        },
        {
            "system": "Linux",
            "machine": "x86_64",
            "wsl_distro": "Ubuntu-24.04",
            "kernel_release": "4.4.0-19041-Microsoft",
            "repo_root": "/home/user/repo",
        },
        {
            "system": "Linux",
            "machine": "x86_64",
            "wsl_distro": "Ubuntu-24.04",
            "kernel_release": "6.6.87.2-microsoft-standard-WSL2",
            "repo_root": "/mnt/c/repo",
        },
        {
            "system": "Windows",
            "machine": "AMD64",
            "wsl_distro": "",
            "kernel_release": "",
            "repo_root": "C:/repo",
        },
    ]:
        try:
            module.validate_host_policy(**kwargs)
        except module.Gate0Error:
            pass
        else:
            raise AssertionError(f"host policy unexpectedly admitted: {kwargs}")


def test_live_probe_requires_wsl_identity_not_generic_linux_only():
    module = load_runtime()
    probe = valid_probe_payload()
    probe["platform"]["wsl_distro"] = None
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=probe
    )
    assert ok is False and failure == "PLATFORM"
    probe = valid_probe_payload()
    probe["platform"]["kernel_release"] = "4.4.0-19041-Microsoft"
    ok, failure = module.validate_probe_payload(
        arm(), role="__parent__", expected_nonce="run-1", probe=probe
    )
    assert ok is False and failure == "PLATFORM"


def test_bootstrap_uses_canonical_host_preflight_entrypoint():
    text = BOOTSTRAP.read_text()
    assert "bash tools/bootstrap_preflight.sh" in text
