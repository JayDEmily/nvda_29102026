# Vocabulary Suppression Removal Receipt

Date: 2026-05-14

Scope: PM/user-authorised FWD-001 / 5.18 remediation. FWD-006 was not opened.

## Result

`src/nvda_desk/vocabulary_synonym_audit.py` no longer contains source-code vocabulary synonym suppression tables or path/surface-bound suppression predicates. The only remaining `score = 0` assignments are generic parsing/tokenisation filters for protocol-field identifier fragments and Python function declaration identifier fragments.

## Mechanisms found and removed

| Category | Count | Result |
|---|---:|---|
| Hard-coded FWD-001 governance candidate table + predicate + branch | 1 | Removed from source. |
| Path/surface-specific suppression predicates and branches | 18 | Removed from source. |
| Total source-code suppression mechanisms removed | 19 | Removed from source. |
| Generic parsing filters inspected | 2 | Retained as non-path-bound tokenisation filters. |

## Governed vocabulary decisions

| Decision class | Count |
|---|---:|
| Candidate phrases adjudicated after source suppression removal | 37 |
| Converted to governed allowed aliases | 9 |
| Converted to governed disallowed phrases / rejection evidence | 28 |
| Left unresolved | 0 |
| Blocked awaiting PM/source authority | 0 |

Decision evidence: `var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/VOCABULARY_SUPPRESSION_REMOVAL_DECISIONS.md`.

## Files intentionally changed

- `src/nvda_desk/vocabulary_synonym_audit.py`
- `src/nvda_desk/vocabulary_builder.py`
- `data/vocabulary/canonical_vocabulary.json`
- `data/vocabulary/vocabulary_touch_stamp.json`
- `var/vocabulary/synonym_candidates.json`
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`
- `ROADMAP_LEDGER.md`
- `var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/**`

## Ledger amendment

`ROADMAP_LEDGER.md` was amended to record this as an exceptional FWD-001 / 5.18 remediation boundary. Prior FWD-001 evidence that depended on exact path/raw-phrase source-code synonym suppression is superseded by this removal-and-governance evidence. FWD-001 remains bounded closed only on the superseding evidence recorded here.

## Validation summary

| Command / proof surface | Captured result |
|---|---:|
| `git diff --check` | 0 |
| `PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean` | 0; `candidates=0`, `vocabulary_touched=False` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` | 0; `17 passed` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a/vocabulary` | 0; `95 passed` |
| `python scripts/run_proof_block.py --check-all` | 0; `proof_blocks_check_all=PASS count=46` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a` | 0; `560 passed` |
| Tier B batched proof | PASS; `49` total passed receipts |

## Tier B note

The monolithic Tier B command did not produce a shell exit-code receipt within the tool boundary. It was therefore not used as proof. Tier B proof is based on captured file-level receipts for 12 non-`proof_executor_contract` Tier B files plus captured node-level receipts for the 21 `proof_executor_contract` tests. Total captured Tier B proof count is 49 passed tests, matching the Tier B suite count.

## Source-code suppression search

Final source search found no `FWD001_GOVERNANCE`, `_is_fwd001`, `selected_fragments`, `GOVERNANCE_CANDIDATE`, `_is_sequence`, or `_is_roadmap` suppression symbols in `src/nvda_desk/vocabulary_synonym_audit.py`. The remaining `score = 0` lines are the two retained generic parsing filters.

Report: `var/audit/active_code_atlas_001/vocabulary_suppression_removal_20260514/reports/final_source_suppression_forbidden_search.stdout`.

## Remaining blockers

None for this remediation gate.
