# Worker 007 — VI-10R2 Proof Repair Handoff

## Mission

Repair only the eleven proof-adequacy findings from VI-11R Tester Iteration 004. Do not enter VI-12R and do not write production code.

## Mandatory read order

1. `GUARDRAILS.md` in full.
2. root `AGENTS.md` in full.
3. accepted root `EXEC_PLAN.md` in full.
4. exact routed METHOD-006 normatives (`N04`, vocabulary governance, `N06`, `N18`, `N15`, `N19`).
5. exact accepted IRB/BICP/IWO authority.
6. `tests/AGENTS.override.md`.
7. current admitted architecture/bootstrap proof corpus and preserved Tier A/B/C method evidence.
8. exact Tester Iteration 004 response/evidence.
9. `implementation/proof/VI10R2_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.

## Bound findings

`T004-F001` through `T004-F011`, exactly as recorded in `implementation/proof/VI11R_TESTER_ITERATION_004_DISPOSITION.md`.

## Hard boundaries

- proof repair only;
- no `src/nvda_desk/**` production behaviour;
- no architecture-proof weakening or contamination;
- no product-obligation deletion or tier reclassification;
- no physical PostgreSQL schema invention;
- preserve all failed predecessor states in ordinary Git history;
- first failed required invariant stops dependent work;
- successor candidate requires fresh independent VI-11R review before VI-12R.
