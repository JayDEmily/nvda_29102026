# Stage 1 worker handoff — 2026-10-08

Plans have changed only in execution shape, not in accepted M01 semantics.

The latest independent Stage-1 review remains `REPAIR` / `RECURRENT_CLASS` at reviewer-evidence commit `a47a581a3cec27a0ccf67c9bccad4f147d2d6076`. The current defect class is selection identity compatibility across direct raw inputs and predecessor-D graph edges.

Programme Owner instruction now requires the Worker to complete the remaining Stage-1 work as three internal leaves defined formally in root `EXEC_PLAN.md`:

1. **Leaf 1 — selection identity and lineage closure**
2. **Leaf 2 — temporal, history and graph-consistency closure**
3. **Leaf 3 — Stage-1 kernel and catalogue closure**

Complete all three leaves in order. Preserve proof-before-production Git ordering within each leaf and create a distinct Git checkpoint after each leaf. **Do not return to the Reviewer after Leaf 1 or Leaf 2.** Return only after Leaf 3 with one exact frozen Stage-1 candidate, unless a governing invariant becomes `BLOCKED`.

Stage 2 remains unauthorised until that final Stage-1 candidate receives independent `PASS`.

Read `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, `handoff/control/CURRENT_STATE.md`, the latest Stage-1 review result, and the accepted M01 authority before continuing.
