# Worker Brief PM-001 — Vocabulary Current-Truth Census

## Dispatch state

`prepared_not_dispatched`

This brief is a complete standalone instruction for one bounded evidence unit. It does not authorise the worker to select or begin a follow-on unit.

## Role

You are the PM-001 evidence worker. You share the repository and live files with the Project Manager. Preserve every unrelated change. Do not change root control files, semantic vocabulary authority, tests, generated vocabulary, or implementation.

## Exact outcome

Create a reproducible current-truth register that accounts for every human vocabulary heading and every generated canonical vocabulary entry, records the two-way discrepancy without making semantic admission decisions, and reconciles the counts with the builder, audit evidence, and the retained ten-record Atlas vocabulary slice.

This unit answers only: “What vocabulary material exists now, where did it come from, and where do the human and generated concept sets differ?”

It does not answer: “Which generated-only terms should be admitted?” or “Which human-only terms should be projected?” Those are later semantic units.

## Baseline and control

| Field | Required value |
|---|---|
| Working branch | `work/NVIDIA_2026_canonical_project_manager_20260720` |
| Baseline commit | `f7bd3f46862fe9b33340f3f13951518795724fe7` |
| Active plan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Programme gate | P1 vocabulary semantic authority |
| Unit | PM-001 current-truth census only |
| Mutation class | Project-control evidence only |
| Gate D | Closed |

Before work, confirm the branch and inspect `git status --short --branch`. If the worktree contains changes outside `project_control/canonical_project_manager/**`, do not overwrite or normalise them. Stop and report any overlap with your allowed output paths.

## Governing propositions

- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`: vocabulary is an admission system; one term/one meaning; durable terms require governance.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`: human semantic authority precedes builder and generated JSON; automated reconciliation cannot decide meaning; the recorded 42/87 inventory must be reverified.
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`: candidate and scanner processes are feeders/evidence only.
- `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`: do not fabricate authority or hide unresolved mismatch.
- `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`: presence/parity proof cannot claim semantic completeness.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` section 5.18 and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`: vocabulary governance remains a `thin_seam` alpha surface.

If these propositions are insufficient or contradictory for the census, stop and return the precise conflict. Do not repair them in this unit.

## Required read order

Read each file semantically in full. Search, scripts, counts, parsers, and prior manifests may assist after reading; they are not substitutes.

1. `AGENTS.md`
2. `PLANS.md`
3. `ROADMAP_LEDGER.md`
4. `ROADMAP_LEDGER_V2.md`
5. `project_control/canonical_project_manager/EXEC_PLAN.md`
6. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
7. `docs/05_GUARDRAILS_CORE.md`
8. `docs/05.1_GUARDRAILS_WORKING.md`
9. `docs/08_TESTING_AND_PROMOTION_CORE.md`
10. `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
11. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
12. `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
13. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` section 5.18 and all general status/modularity rules that govern it
14. `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
15. `docs/vocabulary/README.md`
16. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
17. `docs/vocabulary/vocabulary_registry.md`
18. `tests/AGENTS.override.md`
19. every `tests/tier_a/vocabulary/test_*.py` file
20. `src/nvda_desk/schemas/vocabulary.py`
21. `src/nvda_desk/vocabulary_builder.py`
22. `src/nvda_desk/vocabulary_synonym_audit.py`
23. `scripts/build_canonical_vocabulary.py`
24. `scripts/vocabulary_synonym_audit.py`
25. `scripts/vocabulary_candidate_review.py`
26. `data/vocabulary/canonical_vocabulary.json`
27. `data/vocabulary/vocabulary_touch_stamp.json`
28. `var/vocabulary/synonym_candidates.json` if present; record absence otherwise
29. `var/audit/active_code_atlas_001/vocabulary_candidate_adjudication_evidence_hardening_before_fwd016_20260515/VOCABULARY_CANDIDATE_ADJUDICATION_APPENDIX.json`
30. `var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json`
31. `config/retained_test_registry.yaml` only for the explicit vocabulary-family admission rows and live Tier A reconciliation inventory
32. `config/proof_blocks.yaml` only for vocabulary proof-block definitions and commands

Create `project_control/canonical_project_manager/units/PM-001/PM-001_FULL_READ_MANIFEST.tsv` before any other output. For every required path record path, reason, `read_full`/`read_required_section` status, current SHA-256, and whether it may be changed. `read_required_section` is permitted only for the row-5.18 blueprint material and the expressly bounded vocabulary rows/blocks in `config/retained_test_registry.yaml` and `config/proof_blocks.yaml`; all other listed files must be `read_full`.

## Inputs to reconcile

### Human semantic side

For every `###` entry in `docs/vocabulary/vocabulary_registry.md`, record:

- exact heading;
- normalised comparison label;
- definition;
- scope;
- current normative admission evidence, including any relevant admissions recorded in `docs/10.1`;
- exact source path and line interval;
- whether an exact normalised generated label exists.

### Generated/projection side

For every entry in `data/vocabulary/canonical_vocabulary.json`, record:

- `canonical_slug`;
- `canonical_label`;
- normalised comparison label;
- category and stage owner;
- contract mapping;
- aliases;
- disallowed phrases;
- notes and candidate-descriptor fields;
- builder seed location/symbol or `builder_source_not_located`;
- whether an exact normalised human heading exists.

### Evidence side

Reconcile without semantic promotion:

- builder output equals or differs from committed JSON;
- source-hash coverage declared by the builder;
- touch-stamp state;
- synonym-candidate report state;
- adjudication appendix rows, including quarantined/disallowed evidence;
- vocabulary test files, their current registry/proof-block authority, and their strongest honest proof class;
- all ten Atlas vocabulary records, with ID, intended behaviour, current satisfaction disposition, and candidate-only status.

Atlas rows remain candidate evidence. Do not turn any donor enum, field, helper, category, alias, or serialisation choice into a requirement.

## Comparison method

Use an explicit deterministic comparison normalisation solely for inventory:

1. Unicode-preserving case-fold;
2. take ordered ASCII alphanumeric token runs `[a-z0-9]+`;
3. join tokens with one space.

This normalisation may identify exact inventory matches only. It cannot establish synonymy, equivalent meaning, alias law, ownership, novelty, or admission.

The Project Manager's pre-brief recount observed these verification targets:

- 46 human headings;
- 87 generated entries;
- 26 normalised exact matches;
- 20 human-only normalised labels;
- 61 generated-only normalised labels.

Independently verify them. If your result differs, do not force the target. Record the actual result, the exact algorithm/bytes, and the discrepancy.

## Required outputs

Create only:

1. `project_control/canonical_project_manager/units/PM-001/PM-001_FULL_READ_MANIFEST.tsv`
2. `project_control/canonical_project_manager/units/PM-001/VOCABULARY_CURRENT_TRUTH_REGISTER.tsv`
3. `project_control/canonical_project_manager/units/PM-001/VOCABULARY_TEST_EVIDENCE_REGISTER.tsv`
4. `project_control/canonical_project_manager/units/PM-001/VOCABULARY_ATLAS_EVIDENCE_REGISTER.tsv`
5. `project_control/canonical_project_manager/units/PM-001/VOCABULARY_CURRENT_TRUTH_RECEIPT.md`
6. `project_control/canonical_project_manager/units/PM-001/VALIDATION_OUTPUT.txt` only if a command requires captured output; otherwise record commands/results in the receipt.

The main current-truth register must have one row per distinct side/entry, not one merged row that hides two-way gaps. Include at least:

`record_id, side, exact_label, normalised_label, canonical_slug, category_or_scope, owner, source_path, source_locator, opposite_side_exact_match, inventory_disposition, semantic_status, notes`

Use these inventory dispositions only:

- `exact_normalised_match`;
- `human_only_pending_semantic_adjudication`;
- `generated_only_pending_semantic_adjudication`.

Every row's `semantic_status` is `not_decided_in_PM-001`.

## Allowed changes

Only new files under:

`project_control/canonical_project_manager/units/PM-001/`

## Forbidden changes

Do not change:

- `AGENTS.md`, `PLANS.md`, either roadmap ledger, or either ExecPlan;
- any numbered normative document;
- any file under `docs/vocabulary/`;
- any test or test fixture;
- `config/retained_test_registry.yaml` or `config/proof_blocks.yaml`;
- `src/**` or `scripts/**`;
- `data/vocabulary/**` or `var/vocabulary/**`;
- Atlas inputs, slices, mappings, ledgers, or Git history;
- dependency files, Makefile, packaging, or CI.

Do not run a command that writes to canonical vocabulary, audit, touch-stamp, generated, or Atlas paths. Use temporary paths under `/tmp` for any safe comparison output.

## Validation

Run and record:

1. `git status --short --branch` before work;
2. independent counts and two-way set comparison;
3. builder-versus-committed-JSON comparison in memory or `/tmp` without writing governed paths;
4. schema/TSV shape and unique-row checks for all new registers;
5. proof that the ten Atlas rows are accounted for exactly once;
6. proof that every live vocabulary test file is accounted for exactly once;
7. `git diff --check`;
8. `git diff --name-only` and an allowed-path assertion;
9. final `git status --short --branch`.

Pytest is not required to pass this evidence-only unit. If the locked environment is available, you may run the existing vocabulary tests read-only and report the result. If it cannot initialise, report the exact environmental blocker; do not alter dependencies and do not call the tests passed.

## Pass conditions

PM-001 passes only if:

- all required reads are recorded truthfully;
- every human heading and generated entry is represented exactly once on its own side;
- matches and both gap directions reconcile arithmetically;
- builder, JSON, touch stamp, audit, aliases, disallowed phrases, quarantined evidence, tests, and ten Atlas rows are explicitly accounted for;
- no row is semantically admitted, rejected, aliased, or suppressed;
- all changed files are under the one allowed output directory;
- validation results and limitations are reproducible.

## Fail and return conditions

Stop and return to the Project Manager without broadening scope if:

- a required file is absent or unreadable;
- current authority conflicts on the human source of semantic meaning;
- the builder cannot be compared without writing governed paths;
- an overlap or unrelated worktree change affects the allowed output directory;
- a durable term requires a semantic decision to complete the census;
- Atlas evidence conflicts with current normative authority;
- a validation failure requires changing any forbidden path.

## Return format

Return:

1. exact files created;
2. observed counts and arithmetic;
3. builder/JSON comparison result;
4. audit/touch-stamp/quarantine state;
5. test-evidence count and strongest honest classifications;
6. Atlas 10/10 accounting result;
7. commands and results, including environmental blockers;
8. `git diff --stat` and final status;
9. unresolved questions for later semantic adjudication.

Do not commit, package, update the roadmap, prepare the next worker brief, or claim P1 complete. The Project Manager owns review, acceptance, checkpointing, and follow-on selection.
