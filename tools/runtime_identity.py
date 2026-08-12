from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


class RuntimeIdentityError(RuntimeError):
    pass


def canonical_sha(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip()).resolve()


def state_dir(root: Path) -> Path:
    git_dir_text = subprocess.check_output(
        ["git", "rev-parse", "--git-dir"], cwd=root, text=True
    ).strip()
    git_dir = Path(git_dir_text)
    if not git_dir.is_absolute():
        git_dir = root / git_dir
    return git_dir.resolve() / "nvda_runtime_identity"


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)


def append_lifecycle_event(root: Path, event: dict[str, Any]) -> None:
    _append_jsonl(state_dir(root) / "events.jsonl", event)


def load_lifecycle_events(root: Path) -> list[dict[str, Any]]:
    path = state_dir(root) / "events.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def make_runtime_receipt(
    *,
    start: dict[str, Any],
    stop: dict[str, Any],
) -> dict[str, Any]:
    if start.get("event") != "SubagentStart" or stop.get("event") != "SubagentStop":
        raise RuntimeIdentityError("runtime receipt requires start and stop lifecycle events")
    for field in ("session_id", "turn_id", "agent_id", "agent_type"):
        if not start.get(field) or start.get(field) != stop.get(field):
            raise RuntimeIdentityError(f"runtime lifecycle mismatch: {field}")
    transcript = stop.get("agent_transcript_path")
    if not isinstance(transcript, str) or not transcript:
        raise RuntimeIdentityError("runtime receipt requires a subagent transcript identity")
    body = {
        "schema_version": "1.0.0",
        "source": "CODEX_SUBAGENT_LIFECYCLE_HOOK_V1",
        "session_id": start["session_id"],
        "turn_id": start["turn_id"],
        "agent_id": start["agent_id"],
        "agent_type": start["agent_type"],
        "agent_transcript_path": transcript,
        "start_event_sha256": canonical_sha(start),
        "stop_event_sha256": canonical_sha(stop),
        "disposition": "COMPLETED",
    }
    body["receipt_id"] = f"RID-{canonical_sha(body)[:24]}"
    return body


def append_stop_and_receipt(root: Path, stop: dict[str, Any]) -> dict[str, Any]:
    events = load_lifecycle_events(root)
    matching = [
        item
        for item in events
        if item.get("event") == "SubagentStart"
        and item.get("agent_id") == stop.get("agent_id")
        and item.get("session_id") == stop.get("session_id")
    ]
    if not matching:
        raise RuntimeIdentityError("SubagentStop has no matching protected SubagentStart")
    start = matching[-1]
    append_lifecycle_event(root, stop)
    receipt = make_runtime_receipt(start=start, stop=stop)
    existing = load_runtime_receipts(root)
    prior = existing.get(receipt["receipt_id"])
    if prior is not None and prior != receipt:
        raise RuntimeIdentityError("runtime receipt ID collision")
    if prior is None:
        _append_jsonl(state_dir(root) / "receipts.jsonl", receipt)
    return receipt


def load_runtime_receipts(root: Path) -> dict[str, dict[str, Any]]:
    path = state_dir(root) / "receipts.jsonl"
    if not path.exists():
        return {}
    result: dict[str, dict[str, Any]] = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        receipt_id = record.get("receipt_id")
        if not isinstance(receipt_id, str) or not receipt_id:
            raise RuntimeIdentityError("runtime receipt is missing receipt_id")
        if receipt_id in result and result[receipt_id] != record:
            raise RuntimeIdentityError("duplicate runtime receipt ID has conflicting bytes")
        result[receipt_id] = record
    return result


def validate_runtime_ref(
    ref: dict[str, Any],
    *,
    receipts: dict[str, dict[str, Any]],
    expected_agent_id: str,
    expected_role: str,
    expected_thread_identity: str,
) -> dict[str, Any]:
    receipt_id = ref.get("receipt_id")
    digest = ref.get("sha256")
    receipt = receipts.get(receipt_id)
    if receipt is None:
        raise RuntimeIdentityError("runtime receipt reference is absent")
    if canonical_sha(receipt) != digest:
        raise RuntimeIdentityError("runtime receipt reference hash mismatch")
    if receipt.get("source") != "CODEX_SUBAGENT_LIFECYCLE_HOOK_V1":
        raise RuntimeIdentityError("runtime receipt has untrusted source")
    if receipt.get("disposition") != "COMPLETED":
        raise RuntimeIdentityError("runtime receipt is not completed")
    if receipt.get("agent_id") != expected_agent_id:
        raise RuntimeIdentityError("runtime receipt agent identity mismatch")
    if receipt.get("agent_type") != expected_role:
        raise RuntimeIdentityError("runtime receipt role mismatch")
    if receipt.get("agent_transcript_path") != expected_thread_identity:
        raise RuntimeIdentityError("runtime receipt thread identity mismatch")
    return receipt
