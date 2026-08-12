from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/runtime_identity.py"


def load_module():
    spec = importlib.util.spec_from_file_location("runtime_identity", MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    return repo


def start_event() -> dict:
    return {
        "event": "SubagentStart",
        "session_id": "session-1",
        "turn_id": "turn-1",
        "agent_id": "agent-1",
        "agent_type": "semantic_worker",
        "permission_mode": "default",
        "cwd": "/repo",
    }


def stop_event() -> dict:
    return {
        "event": "SubagentStop",
        "session_id": "session-1",
        "turn_id": "turn-1",
        "agent_id": "agent-1",
        "agent_type": "semantic_worker",
        "permission_mode": "default",
        "cwd": "/repo",
        "agent_transcript_path": "/runtime/agent-1.jsonl",
    }


def test_protected_lifecycle_pair_produces_hash_bound_runtime_receipt(tmp_path):
    module = load_module()
    repo = init_repo(tmp_path)
    module.append_lifecycle_event(repo, start_event())
    receipt = module.append_stop_and_receipt(repo, stop_event())
    receipts = module.load_runtime_receipts(repo)
    ref = {"receipt_id": receipt["receipt_id"], "sha256": module.canonical_sha(receipt)}
    resolved = module.validate_runtime_ref(
        ref,
        receipts=receipts,
        expected_agent_id="agent-1",
        expected_role="semantic_worker",
        expected_thread_identity="/runtime/agent-1.jsonl",
    )
    assert resolved == receipt
    assert (module.state_dir(repo) / "receipts.jsonl").is_file()


def test_stop_without_protected_start_cannot_create_runtime_receipt(tmp_path):
    module = load_module()
    repo = init_repo(tmp_path)
    with pytest.raises(module.RuntimeIdentityError, match="no matching"):
        module.append_stop_and_receipt(repo, stop_event())


def test_runtime_receipt_reference_cannot_be_self_declared(tmp_path):
    module = load_module()
    repo = init_repo(tmp_path)
    module.append_lifecycle_event(repo, start_event())
    receipt = module.append_stop_and_receipt(repo, stop_event())
    receipts = module.load_runtime_receipts(repo)
    forged = {"receipt_id": receipt["receipt_id"], "sha256": "0" * 64}
    with pytest.raises(module.RuntimeIdentityError, match="hash"):
        module.validate_runtime_ref(
            forged,
            receipts=receipts,
            expected_agent_id="agent-1",
            expected_role="semantic_worker",
            expected_thread_identity="/runtime/agent-1.jsonl",
        )


def test_runtime_receipt_file_is_outside_tracked_worktree(tmp_path):
    module = load_module()
    repo = init_repo(tmp_path)
    module.append_lifecycle_event(repo, start_event())
    module.append_stop_and_receipt(repo, stop_event())
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=repo, text=True
    )
    assert status == ""
    lines = (module.state_dir(repo) / "receipts.jsonl").read_text().splitlines()
    assert json.loads(lines[0])["source"] == "CODEX_SUBAGENT_LIFECYCLE_HOOK_V1"
