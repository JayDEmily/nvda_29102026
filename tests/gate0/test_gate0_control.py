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
    }


def valid_events():
    return [
        {"type": "SessionStart", "run_nonce": "run-1", "head": "a" * 40},
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
    )
    assert ok is False and failure == "GUARDED_HASHES"


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


def test_runtime_validator_is_dedicated_gate0_surface():
    assert VALIDATOR_PATH.is_file(), "Unit 4 seam: tools/validate_gate0.py is not implemented yet"
    text = VALIDATOR_PATH.read_text().lower()
    for forbidden in ["prompt_cache", "orchestration_attempt", "r2a", "semantic_index.schema"]:
        assert forbidden not in text
