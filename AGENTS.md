# AGENTS.md

Changes require explicit owner authorisation.

Read `GUARDRAILS.md` in full.

Read the accepted `EXEC_PLAN.md`.

Direct current user instructions outrank repository instructions.

## Execution workflow

Follow the gates, leaves, dependencies and acceptance criteria in `EXEC_PLAN.md`.

Upon completion of each leaf, commit locally and export a verified Git bundle.

Rerun or expand tests only when new changes, failures, or unresolved concerns justify doing so.

## Independent testing

Use independent testing arrangements specified in the `EXEC_PLAN.md`.

Before an authorised ChatGPT-to-GitHub cross-thread handover, read `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md`.

## Blockers

If a requirement is unresolved, a necessary capability is unavailable, or an owner decision is required, report `BLOCKED`.

Identify to the user the exact missing information or decision needed to proceed. Stop dependent work until the blocker is resolved.
