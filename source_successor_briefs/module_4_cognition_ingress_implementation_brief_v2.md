# Module 4 implementation brief — Cognition ingress (tightened replacement)

## Status

This is a **non-normative execution brief** for one bounded implementation tranche.
It **supersedes** the earlier Module 4 brief.
Use this brief instead of the prior Module 4 brief.

This brief is written for a stateless executor working on the uploaded repo zip in isolation.

## Objective

Advance **Module 4 — Cognition input translator** only.

In human terms, this module owns the step that turns the **prepared runtime substrate** into the **typed stage-input bundle** needed by the serial spine.

In repo terms, this is the cognition-ingress-owned **prepared substrate -> cognition ingress bundle** seam and the cognition-ingress-owned mapper/coordinator home.

## Required executor outcome

1. First complete the outstanding Module 3 supplementary brief on the existing Module 3 work branch.
2. Then create a new Module 4 work branch from the **corrected Module 3 branch tip**.
3. Execute only the Module 4 tranche on that new branch.
4. Do **not** merge to `main`.
5. Do **not** close the tranche beyond the branch-local state.
6. When finished, leave the new branch intact, zip the full repo including `.git`, and stop.
7. Await further instructions from the user.

## Baseline and branching rule

1. Repo root: `work_api_dto`
2. Required prerequisite branch already present and corrected first:
   - `work/module-3-preparation-truth-pass-20260421`
3. New work branch to create for this tranche:
   - `work/module-4-cognition-ingress-truth-pass-20260421`

### Mandatory branching sequence

1. First complete the Module 3 supplementary brief on:
   - `work/module-3-preparation-truth-pass-20260421`
2. Confirm the Module 3 branch remains unmerged.
3. Record the exact corrected Module 3 HEAD commit hash.
4. Create the Module 4 branch **from that corrected Module 3 HEAD**, not from `main`.
5. If the uploaded repo does not contain the corrected Module 3 branch state, stop and say so.

## Mandatory read order before changing anything

Read these fully, in order, before coding:

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/02_vocabulary_dictionary_system_audit.md`
5. `migration_prebuild/03_nvda_test_ordering_review_2026-04-18.md`
6. `migration_prebuild/04_rebuild_execution_order.md`
7. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
8. `migration_prebuild/06_tier_family_normalisation.md`
9. `migration_prebuild/07_wave1_truth_pass_and_completeness_2026-04-19.md`
10. `migration_prebuild/08_repository_runtime_hardening_2026-04-19.md`
11. `migration_prebuild/09_upstream_serial_domain_hardening_2026-04-19.md`
12. `migration_prebuild/10_adapter_registry_hardening_2026-04-19.md`
13. `migration_prebuild/11_completeness_matrix_all_workbook_paths_present_2026-04-19.md`
14. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
15. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
16. `docs/01_NORMATIVE_CORE.md`
17. `docs/03_DOMAIN_MODEL_CORE.md`
18. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
19. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
20. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
21. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
22. `data/vocabulary/canonical_vocabulary.json`
23. `src/nvda_desk/schemas/vocabulary.py`
24. `tests/AGENTS.override.md`
25. `var/audit/nvda_running_audit_log.xlsx`

Do not skip the workbook.
Do not skip the core normative docs.
Do not skip the vocabulary surfaces.

## Vocabulary admission gate — mandatory before code changes

This gate is mandatory and comes **before** changing code, contracts, tests, manifests, receipts, or docs.

1. Build the candidate term list for this tranche from:
   1. workbook-owned terms for cognition ingress
   2. seam names
   3. model names
   4. contract names
   5. test names
   6. any new helper/class/function names proposed in implementation
2. Reconcile each candidate term against:
   1. `data/vocabulary/canonical_vocabulary.json`
   2. `src/nvda_desk/schemas/vocabulary.py`
   3. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
   4. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
3. For each term, classify it exactly one way:
   1. already admitted canonical term
   2. lawful alias of an admitted term
   3. new term requiring admission in this same bounded gate
   4. blocked/quarantined term that must not enter live repo surfaces
4. **Do not** use a term in live code or tests merely because it appears in the workbook.
5. If a term is missing but required for this tranche, admit it lawfully in the same bounded gate **before** using it elsewhere.
6. If lawful admission is not possible within this tranche boundary, stop and record the missing term as a blocker.

### Explicit vocabulary rule for `StageInputBundle`

1. `StageInputBundle` must **not** be casually adopted just because the workbook uses it.
2. The executor must first determine whether it is:
   1. already admitted canonically
   2. a lawful alias of an admitted canonical carrier
   3. a new term that must be admitted in this tranche
4. If admission is required, perform the lawful vocabulary update first and then use the term.
5. If admission is not in scope, stop and record the blocker.

## Test-family and invariant gate — mandatory before implementation

This gate is mandatory and comes **after** the vocabulary gate and **before** code changes.

1. Identify the real invariants for the Module 4 seam:
   1. each stage input explicit
   2. absent fields represented lawfully
   3. deterministic mapping
   4. no direct serial-runtime reach into preparation internals
2. Identify the governing test families already covering this area.
3. Decide truthfully for each affected or missing proof surface whether the right action is:
   1. preserve
   2. re-author
   3. add
   4. defer with explicit reason
   5. archive/block with explicit reason
4. Do **not** pre-decide “no new tests needed” before this invariant check is complete.
5. Record the test-family decision in the branch-local report/receipts.

## Module 4 benchmark owner map

These workbook-owned surfaces are the benchmark for this tranche.

### Target structure

- `Target_Structure` row for **Cognition Ingress**:
  - target package: `nvda_desk.cognition.ingress`
  - responsibility: `Prepared-substrate to stage-input translation for the serial pipeline.`
  - owned content: `temporal/regime/options mappers, input bundle coordinator.`
  - forbidden content: `raw source decode, persistence writes, review logic.`
  - preferred form: `functions + thin translator service`

### Ownership matrix

- `Ownership_Matrix` rows for cognition ingress:
  1. **Regime translation from prepared substrate**
     - owner package: `nvda_desk.cognition.ingress`
     - path: `cognition/ingress/regime_mapper.py`
     - owner form: `functions`
     - input: `prepared snapshot + optional regime overlay`
     - output: `typed regime input`
     - note: `Final owner depends on regime-source audit.`
  2. **Temporal translation from prepared substrate**
     - owner package: `nvda_desk.cognition.ingress`
     - path: `cognition/ingress/temporal_mapper.py`
     - owner form: `functions`
     - input: `prepared snapshot`
     - output: `typed temporal input`
     - note: `Pure deterministic mapping.`
  3. **Options-flow translation from prepared substrate**
     - owner package: `nvda_desk.cognition.ingress`
     - path: `cognition/ingress/options_mapper.py`
     - owner form: `functions`
     - input: `prepared snapshot`
     - output: `typed options input`
     - note: `Pure deterministic mapping.`
  4. **Cognition ingress translation coordinator**
     - owner package: `nvda_desk.cognition.ingress`
     - path: `cognition/ingress/translator.py`
     - owner form: `service class`
     - input: `prepared snapshot`
     - output: `typed stage input bundle`
     - note: `Coordinator only; calculations remain in functions.`

### Seam contracts

- `Seam_Contracts` row for **Prepared substrate -> cognition ingress bundle**:
  - source owner: `cognition ingress`
  - consumer: `serial cognition runtime`
  - invariants:
    1. each stage input explicit
    2. absent fields represented lawfully
    3. mapping deterministic
  - allowed persistence: `None`
  - allowed pattern: `Separate mappers per stage`
  - anti-pattern: `Direct serial runtime access to preparation internals`
  - named carrier: `StageInputBundle`

- `Seam_Contracts` provisional row touching this area:
  - seam: `Prepared substrate -> regime input`
  - owner: `preparation or cognition ingress`
  - invariant: `Cross-asset regime completeness requirements explicit; partial regime represented explicitly.`
  - anti-pattern: `Supportive fixture silently replacing native path in production shape.`
  - reservation id: `TR-SM-001`

### Component skeleton

- `Component_Skeleton` rows for cognition ingress:
  1. `cognition/ingress/temporal_mapper.py`
     - function family: `build_temporal_input`
     - model family: `TemporalContextInput`
     - preferred form: `functions`
  2. `cognition/ingress/regime_mapper.py`
     - function family: `build_regime_input`
     - model family: `MarketRegimeContextInput`
     - preferred form: `functions`
     - note: `Owner fixed; completeness unresolved.`
  3. `cognition/ingress/options_mapper.py`
     - function family: `build_options_flow_input`
     - model family: `OptionsFlowContextInput`
     - preferred form: `functions`
  4. `cognition/ingress/translator.py`
     - class family: `CognitionIngressTranslator`
     - function family: `convert_snapshot`
     - model family: `StageInputBundle`
     - preferred form: `service class`
     - note: `Coordinator only.`

### Reservations touching this area

- `Reservations` row `TR-RS-001` keeps **final ownership of regime ingress completeness** unresolved.
- Do **not** use this tranche to settle the full regime-source audit.
- You may only make regime incompleteness explicit and typed so supportive fixtures cannot masquerade as the native path.

## Current observed native state to correct

At the baseline for this tranche, Module 4 is present but too thin.

1. `src/nvda_desk/cognition/ingress/translator.py` accepts `Mapping[str, Any] | PreparedRuntimeDataset`, normalises to one snapshot, and returns a plain `dict[str, Any]` rather than an admitted typed carrier.
2. `temporal_mapper.py` falls back to wall-clock time when `observed_at` is absent.
3. `regime_mapper.py` defaults missing numeric fields to zero certainty.
4. `options_mapper.py` defaults missing numeric fields to zero certainty.

These defaults fabricate certainty rather than representing absence lawfully.

## What “fully transferred” means for Module 4 in this brief

For this tranche, “fully transferred” means **truthfully advancing the native cognition-ingress module to its workbook-owned shape and seam responsibilities**.
It does **not** mean solving the whole serial runtime.

A satisfactory result for this brief must include all of the following:

1. The cognition-ingress module exposes the workbook-owned mapper family:
   1. `build_temporal_input`
   2. `build_regime_input`
   3. `build_options_flow_input`
2. The cognition-ingress module exposes the workbook-owned coordinator family:
   1. `CognitionIngressTranslator`
   2. `convert_snapshot`
3. The coordinator emits a lawful admitted typed carrier rather than an untyped dict blob.
4. Mapper behaviour is deterministic.
5. Absent prepared fields are represented lawfully rather than replaced with wall-clock or zero-value certainty.
6. Regime incompleteness remains explicit and typed.
7. Serial runtime consumes cognition-ingress outputs through the admitted bundle surface, not by reaching into preparation internals.
8. No raw ingress decode, persistence logic, review logic, or serial-stage reasoning is pulled into cognition ingress.
9. All terms introduced or used by this tranche are lawfully admitted or explicitly blocked.
10. The test-family decision is explicit and evidenced.

## Stop boundary

This tranche is invalid if it drifts into later-module implementation work beyond the minimum required to keep the cognition-ingress seam lawful.

### In scope

1. `src/nvda_desk/cognition/ingress/**`
2. minimal contract or schema additions strictly required to admit the lawful stage-input carrier and lawful stage-input models
3. minimal serial-runtime signature changes strictly required to consume the admitted ingress carrier
4. bounded Tier A and Tier B proof aligned to the cognition-ingress seam and nearby serial-runtime consumer boundary
5. vocabulary admission updates strictly required for this tranche
6. required audit/receipt updates for this branch-local tranche

### Out of scope

1. raw bundle decode redesign
2. preparation redesign beyond minimal seam adaptation
3. serial-stage reasoning deepening
4. DMPV3 expansion
5. parallel-risk hardening
6. final-risk changes
7. capital deployment changes
8. downstream operations policy
9. review policy
10. broad API changes
11. persistence redesign
12. settling the full regime-completeness reservation beyond explicit truthful absence handling
13. any merge to `main`

## Required execution pattern

1. Read all mandatory governing sources in order.
2. Run the vocabulary admission gate and either:
   1. admit required terms lawfully, or
   2. stop with a blocker.
3. Run the invariant/test-family gate and decide the truthful proof action.
4. Only then implement the bounded Module 4 changes.
5. Keep the work leaf-led and branch-local.
6. Do not batch vague changes; keep commits leaf-scoped and inspectable.

## Required branch-local proof

Run and preserve artefacts for:

1. targeted Module 4 proof first
2. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
3. `python -m compileall src`

If any proof step fails, stop and report the exact blocker.
Do not claim completion without the proof artefacts.

## Required receipts and artefacts

Before stopping, update or create branch-local artefacts that truthfully show:

1. parent Module 3 corrected HEAD commit hash
2. new Module 4 branch name
3. leaf commit hashes for this tranche
4. vocabulary admission decision for each candidate term
5. test-family decision and proof scope
6. exact proof outputs
7. exact unresolved blockers, if any

Also update the live running audit workbook with:

1. the Module 4 tranche row/state
2. leaf closures
3. exact closing commit hashes

## Final stop instruction

When the Module 4 tranche is complete:

1. leave the branch unmerged
2. do not merge to `main`
3. zip the **entire repo including `.git`**
4. return the zip plus concise execution notes
5. stop and await further instructions

