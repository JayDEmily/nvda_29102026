# M01 continuation — worker start here

Plans changed after the DS-R01 foundation review.

**Continue M01 `derived_signal_calculation_truth`; do not start Financial Calendar or any later module.**

The M01 foundation has already passed independent review. The calculation kernels and full D001–D209 integration are still outstanding. PCM V5 is retired for this continuation and `.pcm/` must not be recreated.

Read, in order:

1. `GUARDRAILS.md`
2. `AGENTS.md`
3. `EXEC_PLAN.md`
4. `handoff/control/CURRENT_STATE.md`
5. `handoff/m01_completion/AUTHORITY_INDEX.md`
6. the exact accepted authority under `handoff/m01_completion/authority/`

The current Stage-1 reviewer result is `REPAIR` and is preserved under `handoff/m01_completion/review/`. Programme Owner instruction dated 2026-10-08 divides the remaining Stage-1 work into **three internal Worker leaves** in `EXEC_PLAN.md`. Complete Leaf 1, Leaf 2 and Leaf 3 in order without returning to the Reviewer between leaves. Each leaf will preserve proof-before-production Git ordering and a distinct checkpoint. Return only after Leaf 3 with one exact frozen Stage-1 candidate, unless a governing invariant becomes `BLOCKED`. Stage 2 remains unauthorised until that candidate receives independent `PASS`.
