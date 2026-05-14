# GLOBAL_ADMISSION_RECONCILIATION_001 report

Date: 2026-05-09
Status: `LOCAL_CLEAN_ADMITTED_BASE_CANDIDATE`

## Objective

Stop opening roadmap rows and reconcile whether the live latest sandbox repo can be treated as a clean admitted base after the recent roadmap branch work.

## Live-state basis

The live repo state, not the uploaded audit package list, was treated as authoritative after inspection. The branch inspected was `work/roadmap-ledger-tranche-control-20260509`.

## Authority/read intake

Full read/intake ledger: `var/audit/global_admission_reconciliation_001/READ_LEDGER.tsv`.

The intake covered:

- `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`;
- process/tranche law docs;
- runtime ownership docs;
- testing/promotion docs;
- vocabulary governance docs;
- architecture blueprint and current-state architecture map;
- active planning briefs;
- latest roadmap receipts under `var/audit/roadmap_*` and planning receipts;
- proof-block config, retained-test registry, Makefile;
- vocabulary audit implementation and Tier A vocabulary synonym tests.

`EXEC_PLAN.md` was not present in the repo root during this pass.

## Baseline reconciliation finding

The live repo was not globally clean at the start of this gate. The existing failure was the vocabulary synonym escalation gate, with generated candidates written to `var/vocabulary/synonym_candidates.json`.

Baseline evidence:

- `logs/baseline_vocabulary_synonym_pytest.status` = `1`.
- `logs/baseline_vocabulary_synonym_pytest.stdout` records the Tier A vocabulary synonym candidate audit failure.
- The dirty candidate artefact contained unresolved roadmap-control terms from proof blocks, retained-test registry entries, working docs, and planning docs.

## Repair decision

No allowed aliases were added to `data/vocabulary/canonical_vocabulary.json`.

The repair did three things instead:

1. Reworded working governance prose where it was using near-synonyms instead of canonical or row-specific wording.
2. Added path+candidate+slug-bounded identifier suppression for exact roadmap-control identifiers generated from proof-block IDs, file paths, route slugs, branch labels, and test-family IDs.
3. Added Tier A tests proving those suppressions are path bounded and do not hide the same phrases in arbitrary prose.

Additional proof-quality repair:

- `scripts/vocabulary_synonym_audit.py` now exits with `raise SystemExit(main())`, so `--check-clean` failures propagate to shell/Make/proof-block callers.

Decision ledger: `VOCABULARY_SYNONYM_REPAIR_DECISION_LEDGER.tsv`.

## Final proof result

Final proof summary is in `PROOF_SUMMARY.tsv`.

Key terminal proof states:

| Proof | Final status | Evidence |
|---|---:|---|
| Vocabulary synonym Tier A test file | `0` | `logs/vocab_synonym_pytest_after_black.*`; `44 passed` |
| Vocabulary synonym clean-check | `0` | `logs/vocab_check_clean_after_black.*`; `candidates=0 vocabulary_touched=False` |
| Full pytest | `0` | `logs/full_pytest_after_black.*`; `400 passed in 19.80s` |
| Proof-block manifest check-all | `0` | `logs/proof_blocks_check_all_after_black.*`; `PASS count=14` |
| All 14 named proof blocks | `0` | `logs/proof_blocks/*.status`; all status files contain `0` |
| All roadmap Makefile gates | `0` | `logs/make_*.status`; all roadmap Make gates contain `0` |
| YAML parse of proof-block and retained-test registry | `0` | `logs/yaml_parse_registry_proofblocks.*` |
| Ruff touched Python | `0` | `logs/ruff_touched_after_black.*` |
| Black check touched Python | `0` | `logs/black_check_touched_after_black.*` |
| Git diff whitespace check | `0` | `logs/git_diff_check_after_black.*` |
| Cache cleanup | `0` | `logs/make_clean_caches_after_full.*`; `cache_artifacts_after_cleanup.txt` has `0` rows |

## Admission conclusion

The repo can be treated as a **local clean admitted-base candidate** for the sandbox branch after this reconciliation.

That conclusion is bounded:

- It means the live sandbox repo is internally clean under the proofs above.
- It does not mean the external/GitHub repo has accepted or merged these changes.
- It does not open any new roadmap row.
- It does not admit runtime trading behaviour, concrete broker placement, dependency changes, external API clients, original Atlas/Bridge JSON mutation, or generated Atlas slice mutation.

## Next state

`ROADMAP_LEDGER.md` now points to `USER_ACCEPTANCE_OR_EXTERNAL_MERGE_DECISION_REQUIRED` after `GLOBAL_ADMISSION_RECONCILIATION_001`. No implementation row is open.
