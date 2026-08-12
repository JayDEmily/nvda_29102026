from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import runtime_identity as identity  # noqa: E402


def output(value: dict) -> None:
    print(json.dumps(value, sort_keys=True))


def lifecycle_record(payload: dict, event: str) -> dict:
    record = {
        "event": event,
        "session_id": payload.get("session_id"),
        "turn_id": payload.get("turn_id"),
        "agent_id": payload.get("agent_id"),
        "agent_type": payload.get("agent_type"),
        "permission_mode": payload.get("permission_mode"),
        "cwd": payload.get("cwd"),
    }
    if event == "SubagentStop":
        record["agent_transcript_path"] = payload.get("agent_transcript_path")
    return record


def main() -> int:
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")
    if event not in {"SubagentStart", "SubagentStop"}:
        output({})
        return 0
    root = identity.repo_root()
    record = lifecycle_record(payload, event)
    try:
        if event == "SubagentStart":
            identity.append_lifecycle_event(root, record)
            output({})
        else:
            receipt = identity.append_stop_and_receipt(root, record)
            output(
                {
                    "systemMessage": (
                        "NVDA authenticated runtime identity receipt: "
                        f"{receipt['receipt_id']} sha256={identity.canonical_sha(receipt)}"
                    )
                }
            )
        return 0
    except (identity.RuntimeIdentityError, OSError, ValueError) as exc:
        output({"continue": False, "stopReason": f"NVDA runtime identity failure: {exc}"})
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
