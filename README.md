# NVDA Repository

Before substantive work, read `GUARDRAILS.md`, `AGENTS.md`, and the complete current `EXEC_PLAN.md` in full.
Then read `handoff/control/CURRENT_STATE.md`; it names the current actor and the active cycle under `handoff/review_cycles/`.
The active cycle prefix (`WORKER_` or `TESTER_`) identifies who acts next; read that cycle's `REQUEST.md` before acting.
Record the result/evidence in the same active cycle, then create the opposite-role cycle for the next authorised action; completed cycles are immutable.
If `CURRENT_STATE.md`, the active-cycle prefix, or the cycle request disagree about role or candidate identity, stop as `BLOCKED` rather than guessing.
