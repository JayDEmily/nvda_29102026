# Independent M01 Stage-1 F1 inventory review — 2026-10-09

**Decision: `F1_INVENTORY_ACCEPTED`.** This is an inventory-evidence decision **only** under the active root `EXEC_PLAN.md` F1. It is **not** Stage-1 `PASS`, arithmetic repair, nor acceptance of graph correlation; Stage 2 is still unauthorised. Exact reviewed worker HEAD: `d27b275bbdc696fab561f20a9fd94dfd4a92de47`, tree `a6e46679d01a77d07ce749ab55ea8d7fd602527d`.

## Authority, inspection and independence

Read repository `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, scoped `tests/AGENTS.override.md`, `handoff/m01_completion/AUTHORITY_INDEX.md`, applicable exact accepted brief and CSV including §§5–9, 11–14, 17–18; reviewed `api.py`, `_stage1.py`, prior reviewer result at `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json`, F1 class map, implementation map, proof matrix, unresolved register, phase scripts and Git commits. The source of domain meaning is the exact accepted brief plus SHA-bound normative catalogue, not the F1 inventory annotations.

Reviewer-generated independent audit: `handoff/m01_completion/review/proof/f1_independent_audit_20261009.py` uses its own parsing, population reconciliation and iterative cross-stage closure (not the worker's scripts). The resulting `F1_INDEPENDENT_AUDIT_20261009.json` establishes 174 Stage-1 rows, 291 raw direct edges, 197 derived direct edges, one no-edge sentinel (D007), 144 closed, 25 direct and five transitively cross-stage rows, 21 represented classes, and exact zero set differences. Checks source catalogue and per-row/per-edge authoritative identity/field metadata, selected RC assignments for D015/D016/D120/D109/D170/D121/D122/D065, class-to-proof-matrix coverage and code-function presence. Separately executed the worker's `python -S handoff/m01_completion/foundation/f1_readback.py`, with zero differences, and verified all 15 manifest evidence-output hashes.

Verified three clean evidence-only Git checkpoints F1a `ba11e27eca136aed9de60bb96e59e2afadfed3d3`, F1b `c1b7dcd5afe0b95da259cc272b1d3e99b4ebe5b2`, F1c `d27b275bbdc696fab561f20a9fd94dfd4a92de47` descend from exact F1 handoff `11790d8c16334da7f61c468f86c69c21e50ff85c`. `git diff` shows only 14 newly added evidence files under `handoff/m01_completion/foundation/`; no worker production, tests, root guardrails/agents/plan, normative authority or package version was changed. `git fsck --no-reflogs --full` exit 0; 16 historical dangling objects do not indicate failed object connectivity. Worker candidate worktree clean.

## Why acceptance is bounded

- F1 demonstrates exhaustive **catalogue accounting** and an actionable **classification/gap inventory**, not semantic correctness of all joins.
- The 21 RC classes are review/planning groupings, not row-specific executable identity law. For each affected edge, F2–F4 must apply its exact accepted row rule, not assume all members of an RC class use the same join or cardinality. General class-level descriptive citations do not replace the row's `brief_rule_ref`, including D006/D008/D065 grouped under RC01.
- All 256 `UNKNOWN` cardinality entries and 437 `NOT_PER_EDGE_PROVED` flags remain visible. These do not constitute evidenced failure of 256 joins or 437 calculations. An indispensable unresolved relationship dimension at implementation time requires `BLOCKED`, not an invented matching rule.
- Eight edge records tagged `KNOWN_PUBLIC_FAILURE` belong to the two publicly failed calculation **rows** D016 and D120. They are *not* eight independently isolated broken edges.
- The independent prior public-seam failure remains **unrepaired**: D015 sign +1 is not correctly associated to raw trade data by D016/D120. D065 event identity is unassessed, D121/D122 grouped-public materialisation is unassessed, and D109/D170 proof must remain protected. No new runtime product tests or PostgreSQL checks were run for this F1 inventory review; these are later gates and must not be inferred from static checks.

## Next authority

`F1_INVENTORY_ACCEPTED` releases **F2 only**. The worker must use the accepted normative brief, retained F1 inventory and the bounded handoff at `handoff/m01_completion/repair/M01_F2_OBSERVATION_IDENTITY_WORKER_HANDOFF_20261009.md`. F2 requires proof-before-production Git commits and adversarial public-seam evidence. It cannot alter M00 meaning, accepted relationships, normative file versions or Stage-2 scope. F3 and F4 remain downstream stages under the current plan. Stage-1 remains `REPAIR / RECURRENT_CLASS`, not accepted.
