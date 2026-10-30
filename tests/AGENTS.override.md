# Test-local AGENTS.override.md — R2 CHAT_MANUAL local worker

This file applies only beneath `tests/`. The owner approved R2 CHAT_MANUAL, with local Git bundle handover only. Read frozen root `GUARDRAILS.md`, approved root `AGENTS.md` and current local `EXEC_PLAN.md` in full. Product tests remain assigned to the independent manual Tester at L32; this setup does not execute them.

- Preserve every valid historical case, strict validator, proof, generation, claim and failed/repaired result. Never rewrite expected outputs or lower proof standards to make tests pass.
- The Worker may author or update only the allocated scope-specific tests and independent oracles before product implementation; mark implementation `IMPLEMENTED_UNTESTED`. Do not execute product tests, routine RED, speculative probes, broad regressions or unrelated cross-module E2E suites.
- In `CHAT_MANUAL`, the separate independent Tester chat is the sole strict executor at final leaf `L32`. It executes accepted new/invalidated module-local proofs in prerequisite order and records raw commands/results, exact candidate, reached refusal, durable readback and semantic disposition. Earlier documentary review is not test acceptance.
- Reuse uninvalidated previously accepted evidence; rerun or expand only when new changes, failures or unresolved concerns justify it, without exceeding accepted proof budgets or masking failed runs.
- Target CPython 3.13.5 only after accepted environment/dependency/SQLite compatibility and relevant proof requirements have been established. Existing CPython 3.12.14 / SQLite 3.53.1 evidence is historical, not equivalence evidence. If the test environment is unsuitable, report `BLOCKED` rather than claiming a pass.
- Preserve prior findings and repairs; independent review must assess recurrence classes and bypass helper composition that conceals critical negative sequences.

Frozen GUARDRAILS remains unchanged. The current setup provides no independent Tester execution and does not authorise product tests by the Worker.
