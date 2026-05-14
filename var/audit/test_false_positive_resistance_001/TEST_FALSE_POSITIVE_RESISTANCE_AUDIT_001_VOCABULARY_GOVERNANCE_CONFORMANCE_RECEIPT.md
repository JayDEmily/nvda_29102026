# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Vocabulary governance conformance receipt

Status: `VOCABULARY_GOVERNANCE_CONFORMANCE_CANDIDATE_HARDENED_LOCAL_PASS`

## Scope

Selected proof-block family: `vocabulary_governance_conformance_candidate`.

Primary architecture row: `5.17 Testing, proof, and checkpoint surfaces`.
Supporting architecture row: `5.18 Vocabulary governance interface`.

## Authority / oracle basis read

- `AGENTS.md` — 272 lines.
- `PLANS.md` — 538 lines.
- `ROADMAP_LEDGER.md` — 329 lines.
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` — 50 lines.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` — 33 lines.
- `docs/vocabulary/README.md` — 23 lines.
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` — 213 lines.
- `docs/08_TESTING_AND_PROMOTION_CORE.md` — 202 lines.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` sections `5.18` and `12`.
- `config/proof_blocks.yaml` vocabulary proof-block entries.

## Independent invariants applied

- Vocabulary is an admission system, not a free-form glossary.
- Candidate actions are exactly `enrich_existing`, `add_new`, `alias_only`, or `quarantine`.
- A new durable term must not enter live surfaces without lawful admission metadata.
- Candidate payload helpers and CLI review surfaces must not admit terms, suppress candidates, mutate canonical vocabulary data, or bypass the builder/generator workflow.
- Invalid or quarantined candidate payloads must block clean-check status.
- Candidate alias collisions with multiple governed entries must not be admitted by document mutation helpers.

## Tests amended / created

- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py:222-245` adds a known-bad case for blank `stage_owner` and blank `maps_to_contract` metadata during `add_new` planning.
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py:248-278` adds a known-bad multi-owner alias candidate that must be rejected before mutation.
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py:160-172` adds a known-bad candidate payload whose alias field is not a list and must remain `INVALID`.
- `tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py:400-430` adds the CLI clean-check analogue proving the same invalid alias payload returns blocked status.

## Proof commands

All commands used `PYTHONPATH=src:.` because no VENV was authorised for this task.

| Command / probe | Status | Log |
|---|---:|---|
| `python -m pytest ... vocabulary proof-block files ... -q` | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_full_selected_pytest.log` |
| `python scripts/vocabulary_candidate_review.py --candidates tests/fixtures/vocabulary_candidate_review/clean_candidates.json --summary-only --check-clean` | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_candidate_review_clean_check.log` |
| `python scripts/vocabulary_synonym_audit.py --check-clean` | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_synonym_audit_clean_check.log` |
| Determinism repeat 1, selected amended files | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_repeat_run_1.log` |
| Determinism repeat 2, selected amended files | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_repeat_run_2.log` |
| Determinism repeat 3, selected amended files | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_repeat_run_3.log` |

Selected full proof result: `113 passed in 26.48s`.

## Mutation / fault-injection probes

| Probe | Expected result | Observed status | Log |
|---|---|---:|---|
| Disable alias-list type guard in `VocabularyCandidate.from_dict` | amended invalid-alias tests fail | `1` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_mutation_bad_alias_guard.log` |
| Disable blank metadata rejection in `VocabularyEntry.validate` | amended blank-metadata test fails | `1` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_mutation_blank_metadata_guard.log` |
| Disable quarantine admission guard in `VocabularyDocument.with_candidate_admission` | quarantine admission tests fail | `1` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_mutation_quarantine_admission_guard.log` |
| Post-revert selected amended files | pass | `0` | `var/audit/test_false_positive_resistance_001/logs/vocabulary_post_revert_selected.log` |

## Non-actions

- No VENV created.
- `black` not run.
- `ruff` not run.
- No runtime trading behaviour changed.
- No canonical vocabulary data modified.
- No source implementation change retained after mutation probes.

## Limits

This receipt does not prove full Tier A reliability. It proves one selected Tier A vocabulary proof-block family has been locally hardened with additional false-positive resistance cases, selected mutation probes, and determinism repeats.
