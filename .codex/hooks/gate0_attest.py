from __future__ import annotations

import json
import secrets
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import gate0_runtime_evidence as rt  # noqa: E402


def output(value: dict[str, Any]) -> None:
    print(json.dumps(value, sort_keys=True))


def hook_context(event: str, text: str) -> dict[str, Any]:
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def find_probe(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        if value.get("gate0_probe") is True:
            return value
        for child in value.values():
            found = find_probe(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_probe(child)
            if found:
                return found
    elif isinstance(value, str):
        text = value.strip()
        try:
            parsed = json.loads(text)
        except Exception:
            for line in reversed(text.splitlines()):
                try:
                    parsed = json.loads(line)
                    found = find_probe(parsed)
                    if found:
                        return found
                except Exception:
                    continue
        else:
            return find_probe(parsed)
    return None


def main() -> int:
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")
    root = rt.repo_root()
    arm = rt.load_arm(root)
    ok, failure = rt.current_binding(root, arm)
    if not ok:
        output({"continue": False, "stopReason": f"NVDA Gate 0 arm binding invalid: {failure}"})
        return 0

    if event == "SessionStart":
        rt.append_event(
            root,
            {
                "type": "SessionStart",
                "run_nonce": arm["run_nonce"],
                "head": arm["head"],
                "session_id": payload.get("session_id"),
                "cwd": payload.get("cwd"),
                "permission_mode": payload.get("permission_mode"),
                "source": payload.get("source"),
            },
        )
        cmd = rt.expected_probe_commands(root, arm)["__parent__"]
        context = (
            "NVDA Gate 0 is armed. Execute only this exact mechanical probe command, "
            f"then report its JSON result: {cmd}"
        )
        output(hook_context("SessionStart", context))
        return 0

    if event == "SubagentStart":
        role = payload.get("agent_type")
        if role not in rt.EXPECTED_ROLES:
            rt.append_event(
                root,
                {
                    "type": "SubagentStart",
                    "role": role,
                    "agent_id": payload.get("agent_id"),
                    "run_nonce": arm["run_nonce"],
                    "unexpected": True,
                },
            )
            output({"systemMessage": f"Unexpected Gate 0 subagent type: {role}"})
            return 0
        data_path = rt.state_dir(root) / "agent_nonces.json"
        data = json.loads(data_path.read_text())
        if role in data.get("roles", {}):
            rt.append_event(
                root,
                {
                    "type": "SubagentStart",
                    "role": role,
                    "agent_id": payload.get("agent_id"),
                    "run_nonce": arm["run_nonce"],
                    "duplicate": True,
                },
            )
            output({"systemMessage": f"Duplicate Gate 0 subagent start for {role}"})
            return 0
        nonce = secrets.token_hex(16)
        data.setdefault("roles", {})[role] = {"nonce": nonce, "agent_id": payload.get("agent_id")}
        data_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        rt.append_event(
            root,
            {
                "type": "SubagentStart",
                "role": role,
                "agent_id": payload.get("agent_id"),
                "run_nonce": arm["run_nonce"],
                "role_nonce": nonce,
            },
        )
        cmd = rt.expected_probe_commands(root, arm)[role]
        context = (
            "Authenticated NVDA gate capability probe. Do no semantic pre-read/work. "
            f"Execute only this exact command, report its JSON result, then stop: {cmd}"
        )
        output(hook_context("SubagentStart", context))
        return 0

    if event == "PreToolUse":
        command = (payload.get("tool_input") or {}).get("command")
        role = rt.command_role(root, arm, command) if isinstance(command, str) else None
        if role is None:
            output(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "Gate 0 permits only the exact nonce-bound mechanical probe command."
                        ),
                    }
                }
            )
            return 0
        rt.append_event(
            root,
            {
                "type": "PreToolUse",
                "role": role,
                "run_nonce": arm["run_nonce"],
                "tool_use_id": payload.get("tool_use_id"),
            },
        )
        output(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        "Exact NVDA Gate 0 probe command matched the protected arm."
                    ),
                }
            }
        )
        return 0

    if event == "PostToolUse":
        command = (payload.get("tool_input") or {}).get("command")
        role = rt.command_role(root, arm, command) if isinstance(command, str) else None
        if role is None:
            output({"systemMessage": "Unexpected Bash result during armed NVDA Gate 0."})
            return 0
        probe = find_probe(payload.get("tool_response"))
        nonces = json.loads((rt.state_dir(root) / "agent_nonces.json").read_text()).get("roles", {})
        agent_id = nonces.get(role, {}).get("agent_id") if role != "__parent__" else None
        expected_nonce = (
            arm["run_nonce"] if role == "__parent__" else nonces.get(role, {}).get("nonce")
        )
        ok = False
        failure = "MACHINE_READABLE_OUTPUT"
        if probe and isinstance(expected_nonce, str):
            ok, failure = rt.validate_probe_payload(
                arm, role=role, expected_nonce=expected_nonce, probe=probe
            )
        rt.append_event(
            root,
            {
                "type": "PostToolUse",
                "role": role,
                "run_nonce": arm["run_nonce"],
                "tool_use_id": payload.get("tool_use_id"),
            },
        )
        rt.append_event(
            root,
            {
                "type": "ProbeResult",
                "role": role,
                "agent_id": agent_id,
                "run_nonce": arm["run_nonce"],
                "passed": ok,
                "failure": failure,
            },
        )
        if not ok:
            output(
                {
                    "decision": "block",
                    "reason": f"NVDA Gate 0 mechanical probe failed for {role}: {failure}.",
                }
            )
        else:
            output(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": f"NVDA Gate 0 mechanical probe PASS for {role}.",
                    }
                }
            )
        return 0

    if event == "SubagentStop":
        role = payload.get("agent_type")
        rt.append_event(
            root,
            {
                "type": "SubagentStop",
                "role": role,
                "agent_id": payload.get("agent_id"),
                "run_nonce": arm["run_nonce"],
            },
        )
        output({"continue": True})
        return 0

    output({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
