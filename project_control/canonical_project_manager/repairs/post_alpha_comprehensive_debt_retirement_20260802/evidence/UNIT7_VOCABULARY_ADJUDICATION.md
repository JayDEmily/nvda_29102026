# Unit 7 — Vocabulary Adjudication Evidence

## Outcome

PASS at working-tree validation. The current vocabulary debt was resolved through exact occurrence-scoped human adjudication, not candidate-count suppression or automated semantic acceptance.

## Authority read

- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`
- `src/nvda_desk/schemas/vocabulary.py`
- `src/nvda_desk/vocabulary_builder.py`
- `src/nvda_desk/vocabulary_synonym_audit.py`
- `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv`
- `project_control/canonical_project_manager/units/PM-010/P1_CANDIDATE_SEMANTIC_DISPOSITION_REGISTER.tsv`
- every current candidate path, line, column and source context emitted by the namespaced audit.

## Candidate reconciliation

The first current scan reported 751 overlapping namespace candidates:

| namespace | initial candidates | final candidates |
|---|---:|---:|
| global | 235 | 0 |
| m02 | 3 | 0 |
| m03 | 11 | 0 |
| m04 | 36 | 0 |
| m07 | 2 | 0 |
| m08 | 18 | 0 |
| m05 | 35 | 0 |
| m06 | 73 | 0 |
| m09 | 96 | 0 |
| m10 | 25 | 0 |
| m11 | 72 | 0 |
| m12 | 4 | 0 |
| m00 | 141 | 0 |

Global-first adjudication resolved shared exact occurrences before module reruns. The residual module set was 373; 593 unique rows were added overall because module-owned occurrences not in the global scan still required exact decisions.

The added rows comprise 293 implementation observations, 211 read-only test observations, 50 normative observations and 39 configuration observations. Each row records stable occurrence identity, exact source context hash, file hash, semantic disposition, rationale and `suppress_same_occurrence_only`.

No canonical label, alias or category was admitted from scanner similarity. Typical dispositions were typed lineage/member identifiers, imported owner concepts, implementation/test-control identifiers, validation reason codes, versioned protocol identifiers, quarantined legacy compatibility terms and deliberate false-positive fixtures.

## Stale proof/schema defects exposed

The complete vocabulary proof initially failed three assertions that contradicted accepted PM-010 authority:

- P1-035/P1-036 quarantine `mutable_runtime_surface` and `baseline_only_surface`;
- P1-066..P1-070 quarantine the generated temporal conformance/status labels;
- P1-122/P1-123 quarantine `candidate_audit` and `stage_read_state`; and
- `VocabularyCategory.AUDIT_SURFACE` had no canonical entry and existed only as stale schema breadth.

The tests were corrected to prove quarantine/absence, and the unused schema category was removed. No quarantined concept was promoted merely to satisfy a test.

## Validation

- all 13 admitted namespaces: `candidates=0`, `vocabulary_touched=False`;
- touch stamp updated for all 13 namespaces;
- `pytest -q tests/tier_a/vocabulary`: 103 passed;
- Black/Ruff on the three changed Python files: passed.

The exact clean-commit aggregate rerun is deferred to Unit 8.
