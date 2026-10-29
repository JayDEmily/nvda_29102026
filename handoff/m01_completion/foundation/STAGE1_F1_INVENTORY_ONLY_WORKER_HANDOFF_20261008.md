# Stage-1 F1 evidence-only Worker handoff — 2026-10-08

## Authority and exact continuation

Programme Owner authorised the Stage-1 foundational identity-and-lineage re-entry on 2026-10-08 after the independent recurrent-class reviewer return. Root `EXEC_PLAN.md` is the **only active plan**. The review return is preserved at `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json`; the worker-facing signed-flow defect evidence remains in `handoff/m01_completion/repair/M01_STAGE1_SIGNED_TRADE_LINEAGE_REVIEW_HANDOFF_20261008.md` and `handoff/m01_completion/review/proof/`.

- Accepted review-return predecessor: `2b5b086099561c2e28aa86bf20dfa222c5d4b3ec`.
- Active ExecPlan amendment commit: `89f6c012342f1508222700a3acb1f301b6c6723b` (tree `f21a7fd29a6ec5d7d40ab8fbc628ab6890226a37`).
- Work from the exact full-Git handoff supplied with this note; preserve branch ancestry, all proof files and the accepted normative bytes.
- Before acting, read `GUARDRAILS.md`, `AGENTS.md`, current `EXEC_PLAN.md`, `handoff/control/CURRENT_STATE.md`, `handoff/m01_completion/AUTHORITY_INDEX.md`, and the relevant accepted brief and CSV. Historical repair handoffs are evidence, not a licence to skip the new F1 boundary.

## Only authorised task this pass: F1

Deliver a fully enumerated, authority-derived Stage-1 raw/derived relationship map and a separately inspectable implementation-gap assessment. Do **not** repair D016/D120, D121/D122 or other production calculations during F1. Do not claim an existing test green proves semantic correctness.

1. **F1a — authoritative census.** Parse the accepted catalogue for all 174 Stage-1-kernel rows. Enumerate every raw `Rxxx` and derived `Dxxx` dependency per row (including rows with no edges); show exact counts by source, row, edge type and Stage-1 vs cross-stage. Emit a reproducible comparison proving no missing/extra normative relationships.
2. **F1b — identity/lineage classification and source map.** For every normative edge, record the authority-grounded selection/correlation law (subject, contract, observation, time, grouping, model/version/parameter/context, predecessor/ultimate raw lineage, cardinality where determined). Map each relevant implementation mechanism to concrete file/function and distinguish observed behaviour, authority requirement and inference. Explicitly flag derived-occurrence versus M00-observation namespace, and the D015/D016/D120, D109/D170 and D121/D122 cases.
3. **F1c — proof matrix and gaps.** Assign stable relationship-class IDs to the complete census; identify positive and adversarial public-seam proof obligations for each distinct class; show which existing tests genuinely cover each and which do not. List every `UNKNOWN`, unresolved material authority discrepancy, missing implementation mapping, and uncovered class as a separate item; never invent a correlation law to fill a blank.

Use repo-native formats (CSV or Markdown) that permit the reviewer to recompute every total from the **accepted** catalogue. Recommended outputs under this `foundation/` directory: `F1_AUTHORITY_RELATIONSHIP_CENSUS.csv`, `F1_RELATIONSHIP_CLASSES.md`, `F1_IMPLEMENTATION_GAP_MAP.md`, `F1_PROOF_MATRIX.md`, `F1_UNRESOLVED_REGISTER.md`, `F1_COMMANDS_AND_READBACK.md`. These are evidence documents; no document becomes normative input.

Commit evidence-only checkpoints after F1a, F1b and F1c. Stop dependent work at the first unresolved required authority invariant and return `BLOCKED` with its exact source. If the entire census and proof matrix are supported, freeze one clean, exact **F1-only** Git candidate and provide its HEAD, tree, commands, readback and full-Git archive for independent `F1_INVENTORY_ACCEPTED`/`F1_REPAIR` review. A successful F1 review **does not** imply Stage-1 PASS and authorises F2 only. **Do not work on F2/F3/F4, Stage 2, or any later module in this pass.**

## Non-mutation constraints

No production code, tests that change acceptance, `GUARDRAILS.md`, `AGENTS.md`, root `EXEC_PLAN.md`, normative authority, M00 ownership, package/distribution version or `.pcm/` change in the Worker F1 pass. Small census scripts or evidence-only tests may be committed with their output if needed to establish completeness. No overwrite of prior reviewer failures or disposition artefacts.

## Why the inventory matters

The independent public-seam witness D011=5 and D015=+1 but D016=0 (instead of 2), and D120 signed volume/notional=(0,0) (instead of (2,1200)). Prior 194 green regression tests did not discriminate that failure. The worker must establish the general identity-mapping obligations first so the next repair is bounded by **all** known affected relationship classes, rather than by a single latest witness.
