# Temporal standard program — tranche 3 execution brief v1
## Code and persistence remediation

## Purpose

This brief executes **Tranche 3 — code and persistence remediation** of the temporal-standard program.

This brief is self-contained on purpose.
It does **not** depend on any external planning note or master brief file being present inside the repo.

This tranche has one job:

1. bring the exact deferred runtime, contract, persistence, harness, and coupled proof surfaces from Tranche 2 into conformance with the admitted temporal standard

This is the tranche that converts the active rebuilt repo from:
1. admitted temporal law plus audit inventory
to
2. actual code/persistence/harness/test conformance

This tranche is **not** for:
1. new normative-document rewriting
2. Module 8 Stage B market translation
3. Module 8 Stage C candidate semantics
4. Module 9 final risk join
5. Module 10 capital deployment
6. Module 11 downstream operations

---

## Baseline to use

Use this accepted repo zip as the required starting baseline:

- `NVIDIA_V7_temporal_standard_tranche_2_conformance_audit_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/temporal-standard-tranche-2-conformance-audit-proof-remediation-20260422`
2. committed HEAD: `1d487abd4cd5b5cbc5a5ec98d20ce24a5ce1cdc2`
3. repo clean: yes
4. authoritative closeout tag present:
   `temporal-standard-tranche-2-authoritative-closeout-20260422`

Create the new tranche branch from that exact state.

Required new branch name:

- `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`

If the provided repo is not actually on:
1. branch `work/temporal-standard-tranche-2-conformance-audit-proof-remediation-20260422`
2. clean HEAD `1d487abd4cd5b5cbc5a5ec98d20ce24a5ce1cdc2`
3. with tag `temporal-standard-tranche-2-authoritative-closeout-20260422`

stop immediately and report the blocker before doing any other work.

---

## Program context this tranche must obey

This tranche is **step 4** in the temporal-standard program order:

1. admit the temporal law
2. audit the repo against it
3. fix proof/test/governor surfaces where truthful now
4. fix code and persistence surfaces
5. run final repo-wide conformance audit
6. close out cleanly

Tranche 2 already classified **22 deferred surfaces** as requiring code/persistence remediation.
This tranche must remediate those exact deferred surfaces.

This tranche is not allowed to:
1. shrink that deferred set for convenience
2. remediate only the easiest subset
3. invent replacement scope
4. widen adjacent unfinished modules to make the story feel complete

The blueprint/workbook remains the **anti-drift ownership benchmark**, not the primary temporal-law authority.

---

## Mandatory execution posture

1. Work on the new tranche branch only.
2. Do **not** merge to `main`.
3. Do **not** rewrite normative documents in this tranche.
4. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
5. Read all required governing files and all required deferred source/test files **in full** before changing anything.
6. If output truncates, continue reading in chunks until the required source is fully read.
7. Return a **clean committed work branch** zip including `.git`.
8. Use the authoritative closeout-tag pattern at the end of the tranche.
9. One active leaf at a time.

This tranche is successful only if it remediates the deferred temporal-conformance surfaces without drifting into unfinished runtime work.

---

## Blocker discipline — mandatory

If a blocker is encountered, the executor must:

1. **stop immediately**
2. **make no further changes**
3. **not improvise**
4. **not keep reading onward “just to see”**
5. **not partially execute later leaves**
6. **not create substitute assumptions or substitute baselines**
7. **return the exact blocker with evidence**

A blocker includes, at minimum:

1. wrong baseline repo identity
2. missing required files named by the brief
3. missing required tags/branches
4. inability to state L1 declarations exactly
5. vocabulary admission not possible in scope
6. inability to remediate a deferred surface without widening prohibited modules
7. proof-floor impossibility caused by the provided baseline
8. any instruction conflict between the brief and the actual repo contents

The executor is **not** allowed to “wing it”, “keep going anyway”, or “work around it silently”.

---

## Anti-shortcut / anti-path-to-green discipline — mandatory

The executor must not optimise for:

1. the smallest apparent remediation set
2. the fastest route to green proofs
3. the smallest vocabulary delta
4. the fewest affected surfaces
5. the least reading work
6. the shortest route to a superficially plausible answer

Instead, the executor must optimise for:

1. exact brief conformance
2. exact hierarchy order
3. full required reading
4. sequential completion of required work
5. truthful receipts
6. explicit preservation of scope boundaries

The **22 deferred surfaces** named below are mandatory.
The executor is not allowed to reduce that set because a smaller set would be easier or more efficient.

Green proofs do **not** excuse skipped required work.

---

## Outcome target

At the end of this tranche, the repo must truthfully support:

1. the admitted source temporal standard across the exact deferred runtime/contract/persistence/harness surfaces from Tranche 2
2. the DMPV3 temporal mapping rule across the exact deferred packet-related surfaces from Tranche 2
3. the workbook temporal provenance rule across the exact deferred specimen/harness surfaces from Tranche 2
4. updated coupled proof surfaces so they assert the remediated temporal grammar truthfully
5. one clean authoritative closeout for this tranche

And the tranche must **not**:

1. widen unfinished runtime-module behaviour
2. fake conformance by weakening tests
3. leave any of the 22 deferred surfaces silently untouched
4. invent provider-specific logic beyond the admitted provider-agnostic temporal grammar

---

## Mandatory read order before changing anything

Read these in full, in this order.

### Control surfaces

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/04_rebuild_execution_order.md`
5. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
6. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
7. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`

### Core normative docs

8. `docs/01_NORMATIVE_CORE.md`
9. `docs/03_DOMAIN_MODEL_CORE.md`
10. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
11. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
12. `docs/05.1_GUARDRAILS_WORKING.md`
13. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
14. `docs/09_DMPV3_PROTOCOL_CORE.md`
15. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
16. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
17. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
18. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

### Accepted module reports and active audit surfaces

19. `var/audit/2026-04-21_module_3_preparation_truth_pass_report.md`
20. `var/audit/2026-04-21_module_4_cognition_ingress_truth_pass_report.md`
21. `var/audit/2026-04-21_module_7_dmpv3_packet_carriage_truth_pass_report.md`
22. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
23. `var/audit/2026-04-22_module_6_serial_spine_truth_pass_report.md`
24. `var/audit/2026-04-22_temporal_standard_tranche_1_normative_admission_report.md`
25. `var/audit/2026-04-22_temporal_standard_tranche_2_conformance_audit_report.md`
26. `var/audit/temporal_conformance_inventory.json`
27. `var/audit/nvda_running_audit_log.xlsx`

### Exact deferred source surfaces to remediate in full

1. `src/nvda_desk/preparation/runtime_preparer.py`
2. `src/nvda_desk/cognition/ingress/temporal_mapper.py`
3. `src/nvda_desk/cognition/ingress/translator.py`
4. `src/nvda_desk/contracts/stage_inputs.py`
5. `src/nvda_desk/contracts/parallel_risk.py`
6. `src/nvda_desk/services/parallel_risk_lane_service.py`
7. `src/nvda_desk/risk/parallel/evaluate.py`
8. `src/nvda_desk/domain/parallel_risk/environment_assessment.py`
9. `src/nvda_desk/persistence/parallel_risk_observations.py`
10. `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`
11. `src/nvda_desk/runtime/orchestrator.py`
12. `src/nvda_desk/domain/temporal/event_windows.py`
13. `src/nvda_desk/domain/temporal/session_clock.py`
14. `src/nvda_desk/contracts/temporal.py`

### Exact coupled proof surfaces to remediate in full

15. `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py`
16. `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py`
17. `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`
18. `tests/tier_a/runtime/test_runtime_orchestrator_surface.py`
19. `tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py`
20. `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_emission_surface.py`
21. `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`
22. `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`

Do not start changing anything until the full read is complete.

---

## Vocabulary gate

Before changing code or proof surfaces:

1. check whether any new durable term is actually required for the remediation
2. likely terms to check include:
   1. source_time_raw
   2. source_time_kind
   3. source_timezone_raw
   4. source_time_utc
   5. source_date
   6. captured_at_utc
   7. persisted_at_utc
   8. source_provider
   9. source_channel
   10. time_granularity
3. if a term is already governed, use it lawfully
4. if a term is not governed and is required as a durable term, admit it lawfully in the same tranche before using it in governed surfaces
5. if lawful admission is not possible in scope, stop and report the blocker

Do **not** silently invent remediation terminology.

---

## Mandatory L1 declarations before any remediation coding

In **L1**, before any implementation leaf starts, record in the tranche report:

1. the exact 22 deferred surfaces listed above
2. the exact target temporal fields/concepts to be remediated on each source surface
3. the exact coupled proof files to be updated
4. the exact workbook sheet names and row numbers being used only as anti-drift ownership references, if any are cited in the report
5. explicit statement that this tranche is:
   1. code/persistence/harness remediation for the exact deferred set only
   2. no unfinished-module widening
   3. no normative rewriting

If any of those L1 items cannot be stated exactly, stop and report the blocker before doing further work.

---

## Scope

### In scope

1. remediation of the exact 14 deferred source surfaces listed above
2. remediation of the exact 8 coupled proof surfaces listed above
3. lawful vocabulary admission if required for the remediation
4. update the tranche report and live audit workbook
5. create the authoritative closeout tag for this tranche

### Out of scope

1. any source or proof surface not listed in the deferred set unless it is an unavoidable minimal glue change and is receipted explicitly
2. Module 8 Stage B implementation
3. Module 8 Stage C implementation
4. Module 9 final risk join implementation
5. Module 10 capital deployment implementation
6. Module 11 downstream operations implementation
7. normative-document rewrites
8. provider-specific implementation logic beyond the admitted provider-agnostic temporal standard

If a change outside the deferred set is truly unavoidable, it must be:
1. minimal
2. receipted explicitly
3. justified as unavoidable glue
4. not a backdoor expansion of unfinished modules

---

## Required remediation rule

The deferred source surfaces must be brought onto the admitted temporal grammar.

That means, where applicable:

1. replace local temporal grammar fields such as:
   1. `observed_at`
   2. `next_event_at`
   3. `starts_at`
   4. `ends_at`
   5. `recorded_at`
   6. overloaded packet `emitted_at` usage
2. separate:
   1. source observation time
   2. packet emission time
   3. repo-process capture time
   4. repo-process persistence time
3. preserve workbook mixed-date provenance truthfully
4. remove fake single-timestamp semantics where the admitted rules prohibit them
5. keep the serial spine stateless
6. keep the parallel-risk observation store write-only
7. keep packet `time` as packet emission time, not source observation time
8. keep provider raw time and granularity truthfully where relevant

Do not partially modernise a temporal surface.
Make each deferred surface either:
1. conformant in this tranche, or
2. blocked with evidence and immediate stop

No silent leftovers.

---

## Required anti-drift implementation rules

1. Do **not** invent timestamp precision.
2. Do **not** apply fake UTC normalisation.
3. Do **not** collapse mixed-date workbook provenance into one false observation timestamp.
4. Do **not** create module-local temporal grammars that diverge from the admitted architecture-level standard.
5. Do **not** overload packet emission time with source observation time.
6. Do **not** introduce hidden state into the serial spine.
7. Do **not** make the workbook direct runtime authority.
8. Do **not** make the parallel-risk observation store readable by live runtime in this tranche.

---

## Required leaf structure

Use this exact bounded leaf sequence unless a blocker prevents it:

1. `L1-read-vocabulary-scope-and-remediation-declarations`
2. `L2-contract-and-preparation-temporal-remediation`
3. `L3-parallel-risk-and-persistence-temporal-remediation`
4. `L4-serial-runtime-and-stage-packet-temporal-remediation`
5. `L5-coupled-proof-remediation`
6. `L6-report-workbook-proof-and-clean-closeout`

One active leaf at a time.  
Do not batch everything into one opaque commit.

---

## Receipt requirements

Maintain and return:

1. `var/audit/briefs/` copy of this brief
2. `var/audit/2026-04-22_temporal_standard_tranche_3_code_persistence_remediation_report.md`
3. updates to `var/audit/nvda_running_audit_log.xlsx`

The report must include:

1. branch name
2. baseline commit
3. leaf chronology
4. exact closing commit for each leaf
5. vocabulary decisions
6. exact source surfaces remediated
7. exact proof surfaces remediated
8. exact unavoidable glue changes outside the deferred set, if any
9. explicit statement that unfinished modules remained out of scope
10. exact authoritative closeout ref name
11. proof outputs
12. final authoritative packaged HEAD or authoritative closeout ref pattern, consistent with the closeout rule below

The report must not rely on “hand-back summary” placeholders.

---

## Proof requirements

After the final receipt-reconciliation commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record exact outputs in the report.

The remediation is only accepted if the repo-wide proof floor still passes after the deferred surfaces are brought into conformance.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded receipt/closeout commit on the tranche branch
2. create one annotated Git tag named:

`temporal-standard-tranche-3-authoritative-closeout-20260422`

3. the tag must point to the final clean closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do **not** use:
   1. “recorded in hand-back summary”
   2. “exact hash reported in hand-back summary”
   3. self-reference placeholder wording

This closeout mechanism is mandatory.

---

## Branch and packaging requirements

1. Leave the branch as `work/temporal-standard-tranche-3-code-persistence-remediation-20260422`
2. Leave the branch unmerged
3. The final repo must be **clean**
4. The final repo must include the annotated tag:
   `temporal-standard-tranche-3-authoritative-closeout-20260422`
5. Zip the **full repo including `.git`**
6. Return:
   1. the updated repo zip
   2. a concise execution summary with:
      1. branch name
      2. baseline commit
      3. final HEAD
      4. authoritative closeout ref name
      5. exact tag target commit
      6. whether the repo is clean
      7. proof results
      8. exact source surfaces remediated
      9. exact proof surfaces remediated
      10. exact unavoidable glue changes outside the deferred set, if any

---

## Definition of done

Tranche 3 is complete only if all of the following are true:

1. it started from the exact accepted Tranche 2 baseline
2. all 14 deferred source surfaces were remediated truthfully
3. all 8 coupled proof surfaces were remediated truthfully
4. no deferred surface was silently skipped
5. any unavoidable glue change outside the deferred set is minimal and receipted explicitly
6. the admitted source temporal standard is now reflected in the remediated active surfaces
7. the DMPV3 temporal mapping rule is now reflected in the remediated active surfaces
8. the workbook temporal provenance rule is now reflected in the remediated specimen/harness surfaces
9. the parallel-risk observation store remains write-only
10. the serial spine remains stateless
11. unfinished modules remained out of scope
12. report is complete
13. workbook is complete
14. report and workbook agree
15. the authoritative closeout tag exists and points to the final clean commit
16. proofs rerun clean
17. repo is clean
18. branch is unmerged

If any one of those is false, stop and report the blocker truthfully.
