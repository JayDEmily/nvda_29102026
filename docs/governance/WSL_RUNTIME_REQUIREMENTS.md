# WSL runtime requirements for NVDA Gate 0

This document separates programme requirements from Codex product facts. Product facts must be rechecked against current official OpenAI documentation before a live run.

## Programme requirements

- The operational repository used for Gate 0 must be the exact accepted clean repository in native WSL2/Linux storage under `/home/...`, not the forensic R2 tree.
- The Codex **agent** must run in WSL2. Integrated-terminal selection is independent and is not evidence of agent runtime.
- Gate 0 uses `read-only` sandbox mode with `on-request` approvals.
- The human approves only the exact nonce-bound mechanical probe command supplied by the admitted Gate 0 flow. If running the probe requires widening the filesystem boundary being measured, the invariant fails.
- Project trust and exact current non-managed hook trust must be established before the fresh run.
- Ordinary WSL performs static admission/arm and, after live success, derives, strictly validates, seals, and admits the run.

## Current OpenAI product facts checked 12 August 2026

Official Codex documentation states that Windows Desktop can switch the agent from Windows-native to WSL and requires an app restart for that agent-mode change; the integrated terminal is configured independently. It also documents `sandbox_mode = "read-only"`, `approval_policy = "on-request"`, project-scoped custom agents, and hook lifecycle events including `SessionStart`, `SubagentStart`, `PreToolUse`, `PostToolUse`, and `SubagentStop`. Non-managed command hooks require trust against their current definition, and project-local hooks require a trusted project layer.

Official references:
- https://developers.openai.com/codex/app/windows
- https://developers.openai.com/codex/agent-approvals-security
- https://developers.openai.com/codex/agent-configuration/subagents
- https://developers.openai.com/codex/hooks
- https://developers.openai.com/codex/config-reference

## Live Unknowns

Static configuration does not prove that the installed Desktop build will spawn the required child, preserve the intended approved read-only command boundary, or append the protected journal. Those remain empirical Gate 0 obligations.
