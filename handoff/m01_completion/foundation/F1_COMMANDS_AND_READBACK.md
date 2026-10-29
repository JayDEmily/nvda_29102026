# F1c — commands, evidence and independent readback

**Authorised unit:** F1 authority relationship census and implementation mapping, evidence only. Starting reviewer handoff `NVDA_DERIVED_SIGNAL_M01_STAGE1_FOUNDATIONAL_CENSUS_F1_HANDOFF_FULL_GIT_20261008.tar(1).gz`, extracted Git base `11790d8c16334da7f61c468f86c69c21e50ff85c` (tree `ce07302e2128653473be9a65962ee3756c75af5b`).

## Exact source authorities

- `GUARDRAILS.md` (fully read); `AGENTS.md` and active `EXEC_PLAN.md` F1–F4 Programme Owner amendment; scoped `tests/AGENTS.override.md` for consulted tests.
- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5`.
- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, SHA-256 `603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c`.
- Independent reviewer `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json`, associated `review/proof/test_stage1_signed_flow_public.py`, `review/proof/stage1_signed_flow_public_fail_20261008.log`, plus historical source/selection repair lineage.
- `src/nvda_desk/derived_signal_calculation_truth/api.py` and `_stage1.py`, associated M01 tests: `tests/product/derived_signal/test_m01_stage1_semantics.py`, `test_m01_stage1_leaf2_temporal_graph.py`, `test_m01_stage1_leaf3_catalogue_kernels.py`, `test_m01_stage1_predecessor_scope.py`, `test_m01_stage1_selection_lineage.py`, `test_ds_t01_m00_projection.py`.

## Deterministic replay (working directory = extracted repository root)

```sh
python -S handoff/m01_completion/foundation/f1_census.py
python -S handoff/m01_completion/foundation/f1_classify.py
python -S handoff/m01_completion/foundation/f1_readback.py
git status --porcelain
git fsck --no-reflogs
git diff 11790d8c16334da7f61c468f86c69c21e50ff85c..HEAD --name-only
```

**Observed first three script exit codes:** 0 / 0 / 0. The source digest gate passed. The independent readback does **not** import F1a/F1b modules and separately parses the authority CSV and checks the complete edge set and an iterative Stage-2 closure. Results:

| Exact population/check | Observed |
|---|---:|
| Stage-1 catalogue rows | 174 |
| Raw direct edges | 291 |
| Derived direct edges | 197 |
| Direct dependency edges total | 488 |
| Zero-dependency sentinel for D007 (not an edge) | 1 |
| Edge-use census records including sentinel | 489 |
| Relationship classes RC01–RC21 | 21 |
| Stage-1 closed | 144 |
| Stage-1 with direct Stage-2 dependency | 25 |
| Stage-1 with transitive-only Stage-2 ancestry | 5 |
| Direct Stage-2 dependency edges | 40 |
| Missing/extra rows, edges, classifications | 0/0 |
| Unclassified edge uses / mismatched row fields / closure mismatches | 0/0/0 |
| Duplicate classifications / edges | False/False |

`F1_SET_DIFFERENCE.json` is the machine-readable outcome with explicit empty `missing`, `extra`, `classification_missing`, `classification_extra`, `unclassified_edge_ids` and mismatch arrays. `F1_CLASSIFIED_EDGE_MAP.csv` carries per-edge source row, brief rule, identity/correlation/time basis, class, cardinality, version and lineage responsibilities, current code mechanism and proof status. Its unknowns are explicit: 256 cardinalities `UNKNOWN`; 437 records `NOT_PER_EDGE_PROVED`. These are **not** class-level semantic acceptance.

## Outputs and stable class mapping

- F1a: `F1_AUTHORITY_ROW_CENSUS.csv`, `F1_AUTHORITY_RELATIONSHIP_CENSUS.csv`, `F1_COUNTS.json`, `f1_census.py`.
- F1b: `F1_CLASSIFIED_EDGE_MAP.csv`, `F1_RELATIONSHIP_CLASSES.md`, `F1_IMPLEMENTATION_GAP_MAP.md`, `f1_classify.py`.
- F1c: `F1_SET_DIFFERENCE.json`, `F1_PROOF_MATRIX.md`, `F1_UNRESOLVED_REGISTER.md`, `f1_readback.py`, this document and `F1_REVIEW_HANDOFF.md`.
- All are **evidence** under `handoff/m01_completion/foundation/`. None supersede the accepted CSV or create an input/selection policy.
- Each of F1a, F1b and F1c is a separate committed evidence checkpoint. Inspect `git log --oneline -4` for exact commit IDs; the archive's top-level freeze manifest records final HEAD and tree independently.

## Explicit limits

1. **No production changes were made**: code, package version, tests, normative sources and root governance remain those of the reviewer handoff. Verify with `git diff <base>..HEAD --name-status` and scoped `git diff --quiet`.
2. **No new pytest execution is claimed for F1**. The reviewer failure and older regression/test results were inspected as historical test evidence. F1 is an authority and source mapping task, not a new arithmetic proof; failure remains outstanding.
3. **No public join-class success is inferred from census exhaustiveness.** The reviewer-witnessed D015→D016/D120 defect and D121/D122 grouping proof gap remain.
4. The Stage-2 dependent rows are included in the normative census, not represented as executable through Stage-1 public graph closure.
5. F2 is blocked by the F1 independent review checkpoint, not by an environment problem. Accepted next disposition is `F1_INVENTORY_ACCEPTED`, `F1_REPAIR` or `BLOCKED`.
