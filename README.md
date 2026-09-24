# NVDA Repository

Before substantive work, read `GUARDRAILS.md`, `AGENTS.md`, and the complete current `EXEC_PLAN.md` in full.
Then read `handoff/control/CURRENT_STATE.md`; it names the current actor and, when execution is authorised, the active cycle under `handoff/review_cycles/`.
If the current state is explicitly `BLOCKED` awaiting Programme Owner / human authority, do not invent a Worker or Tester action and do not create a successor cycle; report the exact blocker.
Otherwise the active cycle prefix (`WORKER_` or `TESTER_`) identifies who acts next; read that cycle's `REQUEST.md` before acting.
Record the result/evidence in the same active cycle, then create the opposite-role cycle for the next authorised action; completed cycles are immutable.
If `CURRENT_STATE.md`, the active-cycle prefix, or the cycle request disagree about role or candidate identity, stop as `BLOCKED` rather than guessing.
