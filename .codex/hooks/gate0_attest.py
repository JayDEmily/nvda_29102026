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


def deny_pretool(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def stop_posttool(reason: str) -> dict[str, Any]:
    return {"continue": False, "stopReason": reason, "systemMessage": reason}


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


def spawn_agent_role(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    role = tool_input.get("agent_type")
    return role if isinstance(role, str) and role else None


def record_and_deny(root: Path, *, stage: str, reason: str) -> dict[str, Any]:
    rt.record_failure(root, stage=stage, reason=reason)
    return deny_pretool(reason)


def record_and_stop(root: Path, *, stage: str, reason: str) -> dict[str, Any]:
    rt.record_failure(root, stage=stage, reason=reason)
    return stop_posttool(reason)


def main() -> int:
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")
    root = rt.repo_root()
    arm = rt.load_active_arm(root)

    # Gate-0 policy must not leak into normal post-Gate-0 semantic execution.
    if arm is None:
        output({})
        return 0

    binding_ok, binding_failure = rt.current_binding(root, arm)

    if event == "SessionStart":
        if not binding_ok:
            reason = f"NVDA Gate 0 arm binding invalid: {binding_failure}"
            rt.record_failure(root, stage=f"BINDING:{binding_failure}", reason=reason)
            output({"continue": False, "stopReason": reason, "systemMessage": reason})
            return 0
        if rt.load_failure(root) is not None:
            failure = rt.load_failure(root) or {}
            reason = f"NVDA Gate 0 already failed at {failure.get('stage')}"
            output({"continue": False, "stopReason": reason, "systemMessage": reason})
            return 0
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

    if event == "PreToolUse":
        if not binding_ok:
            reason = f"NVDA Gate 0 arm binding invalid: {binding_failure}"
            output(record_and_deny(root, stage=f"BINDING:{binding_failure}", reason=reason))
            return 0
        failure = rt.load_failure(root)
        if failure is not None:
            output(
                deny_pretool(
                    "NVDA Gate 0 already failed at "
                    f"{failure.get('stage')}; all later local tools are denied."
                )
            )
            return 0

        tool_name = payload.get("tool_name")
        tool_input = payload.get("tool_input")
        if tool_name == "Bash":
            command = tool_input.get("command") if isinstance(tool_input, dict) else None
            role = rt.command_role(root, arm, command) if isinstance(command, str) else None
            if role is None:
                output(
                    record_and_deny(
                        root,
                        stage="UNEXPECTED_LOCAL_TOOL:Bash",
                        reason=(
                            "Gate 0 permits only the exact nonce-bound mechanical probe command."
                        ),
                    )
                )
                return 0
            rt.append_event(
                root,
                {
                    "type": "PreToolUse",
                    "role": role,
                    "run_nonce": arm["run_nonce"],
                    "tool_use_id": payload.get("tool_use_id"),
                    "tool_name": "Bash",
                },
            )
            output(
                hook_context(
                    "PreToolUse",
                    "Exact NVDA Gate 0 probe command matched the protected arm.",
                )
            )
            return 0

        if tool_name == "wait_agent":
            if not rt.wait_agent_allowed(rt.load_events(root), run_nonce=arm["run_nonce"]):
                output(
                    record_and_deny(
                        root,
                        stage="WAIT_OUTSIDE_ACTIVE_CHILD",
                        reason=(
                            "Gate 0 wait_agent is allowed only while the one authorised "
                            "Gate 0 child is still in progress."
                        ),
                    )
                )
                return 0
            rt.append_event(
                root,
                {
                    "type": "PreToolUse",
                    "role": "__orchestration__",
                    "run_nonce": arm["run_nonce"],
                    "tool_use_id": payload.get("tool_use_id"),
                    "tool_name": "wait_agent",
                },
            )
            output(hook_context("PreToolUse", "Gate 0 wait_agent orchestration call allowed."))
            return 0

        if tool_name == "spawn_agent":
            try:
                expected_role = rt.expected_next_spawn_role(
                    rt.load_events(root), run_nonce=arm["run_nonce"]
                )
            except rt.Gate0Error as exc:
                output(
                    record_and_deny(
                        root,
                        stage="SPAWN_SEQUENCE",
                        reason=f"Gate 0 spawn request is not at a lawful boundary: {exc}",
                    )
                )
                return 0
            actual_role = spawn_agent_role(tool_input)
            if expected_role is None or actual_role != expected_role:
                output(
                    record_and_deny(
                        root,
                        stage=f"SPAWN_REQUEST:{expected_role or 'NONE'}",
                        reason=(
                            "Gate 0 permits only the next exact custom-role spawn; "
                            f"expected {expected_role!r}, got {actual_role!r}."
                        ),
                    )
                )
                return 0
            rt.append_event(
                root,
                {
                    "type": "SpawnRequest",
                    "role": actual_role,
                    "run_nonce": arm["run_nonce"],
                    "tool_use_id": payload.get("tool_use_id"),
                },
            )
            output(
                hook_context(
                    "PreToolUse",
                    "Authenticated Gate 0 spawn request for "
                    f"{actual_role} matched the expected sequence.",
                )
            )
            return 0

        output(
            record_and_deny(
                root,
                stage=f"UNEXPECTED_LOCAL_TOOL:{tool_name}",
                reason=(
                    "Armed Gate 0 denies every hook-observable local tool except the exact "
                    "mechanical probe and the next authorised spawn_agent call."
                ),
            )
        )
        return 0

    if event == "PostToolUse":
        if not binding_ok:
            reason = f"NVDA Gate 0 arm binding invalid after tool execution: {binding_failure}"
            output(record_and_stop(root, stage=f"BINDING:{binding_failure}", reason=reason))
            return 0
        failure = rt.load_failure(root)
        if failure is not None:
            output(
                stop_posttool(
                    f"NVDA Gate 0 already failed at {failure.get('stage')}; stop live execution."
                )
            )
            return 0

        tool_name = payload.get("tool_name")
        tool_input = payload.get("tool_input")
        if tool_name in {"spawn_agent", "wait_agent"}:
            # SubagentStart/Stop are the authoritative lifecycle proof. Spawn/wait are
            # bounded orchestration tools and never perform semantic work themselves.
            # pre-authorised and recorded in PreToolUse; no model-side closure occurs here.
            output({})
            return 0
        if tool_name != "Bash":
            output(
                record_and_stop(
                    root,
                    stage=f"UNEXPECTED_POST_TOOL:{tool_name}",
                    reason="Unexpected local tool completed during armed Gate 0.",
                )
            )
            return 0

        command = tool_input.get("command") if isinstance(tool_input, dict) else None
        role = rt.command_role(root, arm, command) if isinstance(command, str) else None
        if role is None:
            output(
                record_and_stop(
                    root,
                    stage="UNEXPECTED_POST_TOOL:Bash",
                    reason="Unexpected Bash result during armed NVDA Gate 0.",
                )
            )
            return 0
        probe = find_probe(payload.get("tool_response"))
        nonces = json.loads((rt.state_dir(root) / "agent_nonces.json").read_text()).get("roles", {})
        agent_id = nonces.get(role, {}).get("agent_id") if role != "__parent__" else None
        expected_nonce = (
            arm["run_nonce"] if role == "__parent__" else nonces.get(role, {}).get("nonce")
        )
        passed = False
        probe_failure = "MACHINE_READABLE_OUTPUT"
        if probe and isinstance(expected_nonce, str):
            passed, probe_failure = rt.validate_probe_payload(
                arm, role=role, expected_nonce=expected_nonce, probe=probe
            )
        rt.append_event(
            root,
            {
                "type": "PostToolUse",
                "role": role,
                "run_nonce": arm["run_nonce"],
                "tool_use_id": payload.get("tool_use_id"),
                "tool_name": "Bash",
            },
        )
        rt.append_event(
            root,
            {
                "type": "ProbeResult",
                "role": role,
                "agent_id": agent_id,
                "run_nonce": arm["run_nonce"],
                "passed": passed,
                "failure": probe_failure,
            },
        )
        if not passed:
            reason = f"NVDA Gate 0 mechanical probe failed for {role}: {probe_failure}."
            output(record_and_stop(root, stage=f"PROBE:{role}", reason=reason))
        else:
            output(hook_context("PostToolUse", f"NVDA Gate 0 mechanical probe PASS for {role}."))
        return 0

    if event == "SubagentStart":
        if not binding_ok:
            reason = f"NVDA Gate 0 arm binding invalid at SubagentStart: {binding_failure}"
            rt.record_failure(root, stage=f"BINDING:{binding_failure}", reason=reason)
            output(
                {
                    "systemMessage": reason,
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStart",
                        "additionalContext": "Gate 0 is failed. Use no tools and stop immediately.",
                    },
                }
            )
            return 0
        failure = rt.load_failure(root)
        if failure is not None:
            output(
                {
                    "systemMessage": f"NVDA Gate 0 already failed at {failure.get('stage')}.",
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStart",
                        "additionalContext": "Gate 0 is failed. Use no tools and stop immediately.",
                    },
                }
            )
            return 0

        role = payload.get("agent_type")
        expected_role = rt.expected_next_start_role(
            rt.load_events(root), run_nonce=arm["run_nonce"]
        )
        if role != expected_role:
            reason = f"Unexpected Gate 0 SubagentStart: expected {expected_role!r}, got {role!r}."
            rt.record_failure(
                root, stage=f"SUBAGENT_START:{expected_role or 'NONE'}", reason=reason
            )
            output(
                {
                    "systemMessage": reason,
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStart",
                        "additionalContext": "Gate 0 is failed. Use no tools and stop immediately.",
                    },
                }
            )
            return 0

        data_path = rt.state_dir(root) / "agent_nonces.json"
        data = json.loads(data_path.read_text())
        if role in data.get("roles", {}):
            reason = f"Duplicate Gate 0 subagent start for {role}"
            rt.record_failure(root, stage=f"SUBAGENT_START:{role}", reason=reason)
            output(
                {
                    "systemMessage": reason,
                    "hookSpecificOutput": {
                        "hookEventName": "SubagentStart",
                        "additionalContext": "Gate 0 is failed. Use no tools and stop immediately.",
                    },
                }
            )
            return 0
        nonce = secrets.token_hex(16)
        data.setdefault("roles", {})[role] = {
            "nonce": nonce,
            "agent_id": payload.get("agent_id"),
        }
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
        if not binding_ok:
            reason = f"NVDA Gate 0 arm binding invalid at SubagentStop: {binding_failure}"
            rt.record_failure(root, stage=f"BINDING:{binding_failure}", reason=reason)
            output({"continue": False, "stopReason": reason, "systemMessage": reason})
            return 0
        failure = rt.load_failure(root)
        if failure is not None:
            reason = f"NVDA Gate 0 failed at {failure.get('stage')}; stop live execution."
            output({"continue": False, "stopReason": reason, "systemMessage": reason})
            return 0
        events = rt.meaningful_events(rt.load_events(root))
        if len(events) < 2 or not (
            events[-2].get("type") == "ProbeResult"
            and events[-2].get("role") == role
            and events[-2].get("agent_id") == payload.get("agent_id")
            and events[-2].get("passed") is True
            and events[-1].get("type") == "SubagentStop"
        ):
            reason = f"SubagentStop for {role} was not preceded by its authenticated passing probe."
            rt.record_failure(root, stage=f"SUBAGENT_STOP:{role}", reason=reason)
            output({"continue": False, "stopReason": reason, "systemMessage": reason})
            return 0
        output({"continue": True})
        return 0

    output({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
