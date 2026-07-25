# PM-001 Vocabulary Current-Truth Receipt

`unit_result: pass`

## Control

- Branch: `work/NVIDIA_2026_pm001_pm010_restart_20260721`
- HEAD inspected: `21c1e5eccfbb818bdd422afd42117f23b1f74f26`
- Unit: PM-001 evidence-only current-truth census
- Mutation scope: `project_control/canonical_project_manager/units/PM-001/` only
- Semantic decisions made: none
- Gate D: closed

## Exact census

The deterministic inventory normalisation was: Unicode-preserving `casefold()`, ordered ASCII token runs `[a-z0-9]+`, joined with one ASCII space.

| Measure | Observed |
|---|---:|
| Human `###` headings | 46 |
| Generated canonical entries | 87 |
| Exact normalised concept matches | 26 |
| Human-only normalised labels | 20 |
| Generated-only normalised labels | 61 |
| Two-sided register rows | 133 |

Arithmetic reconciles: `26 + 20 = 46` on the human side; `26 + 61 = 87` on the generated side. The main register deliberately retains two rows for each exact match—one human row and one generated row—so no side is hidden.

Disposition row counts: `{'human_only_pending_semantic_adjudication': 20, 'exact_normalised_match': 52, 'generated_only_pending_semantic_adjudication': 61}`. Every row has `semantic_status=not_decided_in_PM-001`.

## Explicit normative admissions

Sections 10.7 and 10.8 contain 27 explicit admission rows: 16 historical bounded-pack admissions and 11 current-programme admissions.

Exact-normalised inventory location counts: `{'neither': 18, 'both': 5, 'human_only': 4}`. These are presence observations only; PM-001 did not alter, ratify, reject, alias, or project any admission.

## Builder and generated projection

- In-memory `build_canonical_payload()` equals committed `data/vocabulary/canonical_vocabulary.json`: `true`.
- Builder entries: 87; committed entries: 87.
- Builder seed locations found: 87/87.
- `governed_source_hashes()` returned 10 existing governed paths. Those paths and hashes are recorded below; coverage is implementation evidence, not semantic completeness.

```text
docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md	2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8
docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md	67db5a62f3082d57dac6764255f4d22682cf097186519ebbd4f333ed79b1bca3
docs/vocabulary/README.md	e76cc9c284641d194283f0a3194d0b81d2a603fd5f5c01b042f3b0fbe0e74439
docs/vocabulary/CONSOLIDATION_WORKFLOW.md	0cce16eb35b95f03684c035da751f4344b10e8ca6f1e671b1cf697e2f9a56f56
docs/vocabulary/vocabulary_registry.md	c1bdface589b6765ca9fdee0a83c4c0682923f129c7e87e94583f69b7bfc826c
scripts/build_canonical_vocabulary.py	e241a7c444dfb0e00464b1c3ec6924758dddcf66cce8c03c0407bfe126d1899e
src/nvda_desk/schemas/vocabulary.py	ba60ed76720f1e6538ce9defd5a31c204d328830f297f558e9b7ce9957b2565d
src/nvda_desk/vocabulary_builder.py	5bd0b7d7b84cd58bcd102936950768798868c430bf9fc02a40778f5592111e10
src/nvda_desk/vocabulary_synonym_audit.py	19895d084a192eeedf7f56b671ce8c6415a08d9b6fab6ade5ac841872dfea3f2
data/vocabulary/canonical_vocabulary.json	235299146440aea2be3bb59c002d2c84c9fda33653e83990110895012ea4cd14
```

## Touch stamp, synonym audit and adjudication appendix

- Tracked touch-stamp fingerprint: `4d2ba332cf6e4c009c1b14ac76b3d506b8704fe692a3457cfd098c0e653b3700`.
- Tracked synonym report fingerprint: `4d2ba332cf6e4c009c1b14ac76b3d506b8704fe692a3457cfd098c0e653b3700`.
- Tracked report state: `vocabulary_touched=false`, candidates=0, classifications=0.
- In-memory current report fingerprint: `6f9bccf5e9664ab834171368ed06b2206679263ea5208eb039a54e456f7fa338`.
- In-memory current report state: `vocabulary_touched=true`, candidate occurrences=9, classifications=9.
- Therefore the tracked stamp/report are stale against current source bytes. PM-001 records this mismatch and does not write governed audit or stamp paths.
- Current candidate occurrence phrases: `['or coefficient authority', 'ecursor runtime context', 'compile playbook eligibility', 'ecursor runtime context', 'or coefficient authority', 'source temporal standard requires', 'market context', 'compile playbook eligibility', 'source temporal standard requires']`.
- Adjudication appendix: reported prior transient count=152; exact original set reconstructed=false; reconstructable records=88; reconstruction status=`not_fully_reconstructable`.
- Reconstructable decision counts: `{'already_governed': 2, 'admitted_alias': 38, 'admitted_exact': 20, 'disallowed_non_term_phrase': 28}`. In particular, 28 disallowed phrase records remain visible evidence; no record was suppressed or semantically revisited.

## Test evidence

- Live `tests/tier_a/vocabulary/test_*.py` files: 17; each appears exactly once in `VOCABULARY_TEST_EVIDENCE_REGISTER.tsv`.
- Files with an explicit retained-seed Tier A family row: 13/17.
- File(s) without an explicit retained-seed family row: `['tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py', 'tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py', 'tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py', 'tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py']`.
- Strongest honest proof classes are recorded per file and are limited to current contract, presence, parity, validation, CLI, non-mutation, workflow, audit and guardrail assertions. None is semantic authority.
- Bounded execution command: `PYTHONPATH=src python -m pytest tests/tier_a/vocabulary -q`.
- Result: `101 passed in 16.24s`; exit code 0; the command produced no worktree-status change.
- Classification: `current_assertions_executed_green` only. Existing tests are not treated as the authority hierarchy’s semantic source and are not a PM-001 pass condition.

## Atlas evidence

- Atlas slice metadata record count: 10.
- Atlas rows emitted: 10/10, each satisfaction-record ID and Atlas-record ID unique.
- Native satisfaction dispositions: `{'partially_satisfied': 3, 'missing': 3, 'already_satisfied': 1, 'transform_required': 3}`.
- Every row is marked `atlas_candidate_evidence_only_not_semantic_authority` and `not_decided_in_PM-001`.
- Donor enums, helpers, fields, categories, serialisation choices and test proposals were not promoted into requirements.

## Limitations and later gates

1. PM-001 identifies exact normalised two-way gaps but does not decide synonymy, equivalence, alias law, novelty, ownership, scope or admission.
2. The stale 42/87 and 16/61 narrative is superseded only as census evidence by the observed 46/87 and 26/20/61 arithmetic; normative repair belongs to PM-002.
3. Human-only and generated-only terms require the supplied PM-002–PM-009 semantic briefs in serial order.
4. Tracked audit/stamp regeneration is not authorised in PM-001.
5. The 152-candidate historical transient set is not fully reconstructable from committed evidence; only the 88-record appendix is directly inspectable.

## Files created

- `PM-001_FULL_READ_MANIFEST.tsv`
- `VOCABULARY_CURRENT_TRUTH_REGISTER.tsv`
- `VOCABULARY_NORMATIVE_ADMISSION_REGISTER.tsv`
- `VOCABULARY_TEST_EVIDENCE_REGISTER.tsv`
- `VOCABULARY_ATLAS_EVIDENCE_REGISTER.tsv`
- `VOCABULARY_CURRENT_TRUTH_RECEIPT.md`
- `VALIDATION_OUTPUT.txt`

The final validation transcript is in `VALIDATION_OUTPUT.txt`.
