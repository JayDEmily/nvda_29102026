# Worker 009 — VI-10R3 Proof Repair Handoff

## Mission

Repair only the eleven proof-adequacy findings from VI-11R2 Tester Iteration 005. Do not enter VI-12R and do not write production code.

## Mandatory read order

1. `GUARDRAILS.md` in full.
2. root `AGENTS.md` in full.
3. accepted root `EXEC_PLAN.md` in full.
4. exact routed METHOD-006 normatives (`N04`, vocabulary governance, `N06`, `N18`, `N15`, `N19`).
5. exact accepted IRB/BICP/IWO authority.
6. `tests/AGENTS.override.md`.
7. current admitted architecture/bootstrap proof corpus and preserved Tier A/B/C method evidence.
8. exact Tester Iteration 005 response/evidence.
9. `implementation/proof/VI10R3_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.

## Bound findings

`T005-F001` through `T005-F011`, exactly as recorded in `implementation/proof/VI11R2_TESTER_ITERATION_005_DISPOSITION.md`.

## Hard boundaries

- proof repair only;
- no `src/nvda_desk/**` production behaviour;
- no architecture-proof weakening or contamination;
- no product-obligation deletion or tier reclassification;
- no physical PostgreSQL schema invention;
- preserve all failed predecessor states in ordinary Git history;
- first failed required invariant stops dependent work;
- successor requires fresh independent VI-11R3 review before VI-12R.
