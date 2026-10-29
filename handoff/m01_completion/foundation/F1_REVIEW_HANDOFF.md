# M01 Stage 1 — F1 evidence-only candidate for independent reviewer

**Requested disposition:** assess the exact archived F1 candidate against root `EXEC_PLAN.md` F1. The only acceptable outcomes are `F1_INVENTORY_ACCEPTED`, `F1_REPAIR` or `BLOCKED`. The candidate does **not** claim a Stage-1 PASS or repair the rejected signed flow.

## What the reviewer rejected

The supplied reviewer result `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json` is `REPAIR / RECURRENT_CLASS`. For a single buy-side trade (price 6, size 2, multiplier 100), public D015 yielded `+1` while D016 yielded `0` instead of `2`, and D120 yielded `(0, 0)` instead of `(2, 1200)`. Raw M00 source observation identity and hashed derived D015 occurrence identity are distinct namespaces. `_stage1.py` performs an ID-equality join that is not authorised by this lineage. The defect remains **VERIFIED AND UNREPAIRED**.

## F1 result, and exact limits

- Exhaustive CSV population: **174** Stage-1 rows, **291** raw and **197** derived direct edges (488 total). D007 has no edges and is represented by a distinct **non-edge** sentinel.
- Closure: **144** Stage-1 closed, **25** direct Stage-2 ancestors, **5** transitive-only; 40 Stage-2 direct edges.
- **21 stable RC classes** from row-specific accepted brief semantics. Every one of the 488 edges has exactly one class and row/brief reference, identity/time/version/lineage notes, code owner and proof status.
- Independent set difference is empty for missing, extra and unclassified edges and rows, as well as duplicates, row-field mismatches and Stage-2 boundary mismatches. See `F1_SET_DIFFERENCE.json`; script `f1_readback.py` does not import census/classification scripts.
- **Important:** 256 cardinality entries remain `UNKNOWN`; 437 evidence entries remain `NOT_PER_EDGE_PROVED`. A static census cannot prove these semantics. `F1_UNRESOLVED_REGISTER.md` separates known defect, existing D109/D170 repair, unassessed D121/D122, suspected cross-ID joins and insufficient public coverage with F2/F3/F4 dispositions.
- `F1_PROOF_MATRIX.md` prescribes adversarial and public-seam proof requirements for each RC class and retains the signed-flow witness separately from kernel-only passing examples.
- The three F1 phases are separately committed. Only new evidence files under `handoff/m01_completion/foundation/` were added. No tests were rewritten, no authority changed, no Stage-2 code added.

## Reviewer action

1. Recompute row/edge counts and selected classifications against the **accepted** normative CSV/brief, not the worker's generated CSV alone. Compare `F1_AUTHORITY_*`, `F1_CLASSIFIED_EDGE_MAP.csv`, `F1_RELATIONSHIP_CLASSES.md`, `F1_PROOF_MATRIX.md`.
2. Inspect `F1_IMPLEMENTATION_GAP_MAP.md` and `F1_UNRESOLVED_REGISTER.md` against `api.py` and `_stage1.py` and the preserved signed-flow public witness. Distinguish observed source behaviour from accepted meaning; do not promote suspicious joins to proven failures.
3. Run `python -S handoff/m01_completion/foundation/f1_readback.py` and inspect `F1_SET_DIFFERENCE.json`. Verify clean Git, ancestry, unchanged production, normative/test/governance files and the archive freeze manifest.
4. Return a bounded disposition. `F1_INVENTORY_ACCEPTED` authorises **F2 only**; F3/F4, production repair and Stage-1 acceptance remain separate.

**Candidate identity:** use `F1_FREEZE_MANIFEST.json` at the archive root for exact committed Git HEAD, tree and digest. Do not use a prior worker candidate.
