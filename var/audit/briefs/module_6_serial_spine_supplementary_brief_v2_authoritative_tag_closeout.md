# Module 6 — supplementary brief v2 for receipt reconciliation and authoritative closeout

## Purpose

This brief fixes the briefing defect in the prior Module 6 supplementary closeout brief.

The prior brief still treated final closeout identity as if it should be written directly into tracked receipt files as an exact self-referential final HEAD hash. That creates the same ambiguity loop again and again.

This brief uses a better closeout pattern:

1. complete the missing tracked receipt content
2. create one final clean receipt-reconciliation commit on the Module 6 work branch
3. create one immutable authoritative closeout Git tag pointing to that final clean commit
4. make the tracked receipts record the **authoritative closeout ref name**, not a hand-back-summary placeholder
5. package the clean repo including `.git`, so the authoritative ref and the exact commit hash are both preserved without self-reference ambiguity

This is a **closeout-only** brief.

Do **not** reopen Module 6 runtime design, packet logic, adjacent-module scope, or normative docs.

---

## Baseline

Start from the submitted Module 6 repo exactly as handed back for audit.

Expected starting state after unzip:

1. branch: `work/module-6-serial-spine-truth-pass-20260422`
2. committed HEAD: `ef68e41b49dff50b0d2028c3fdc27731c962b177`
3. repo clean: yes

If the provided repo does not match that exact branch and clean starting HEAD, stop and report the blocker.

---

## Why the previous brief was inadequate

The prior supplementary brief still left too much ambiguity around authoritative closeout identity.

Specifically, it did not prescribe one concrete closeout mechanism that avoids the self-reference loop.

That allowed the executor to continue using patterns like:

1. “recorded in hand-back summary”
2. “exact hash reported in hand-back summary”
3. other placeholder closeout wording in tracked receipts

That is not acceptable.

This brief fixes that by prescribing one explicit authoritative closeout mechanism.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded receipt-reconciliation commit on the existing Module 6 work branch
2. after that commit, create one annotated Git tag named:

`module-6-serial-spine-authoritative-closeout-20260422`

3. the tag must point to the final clean receipt-reconciliation commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do **not** use:
   1. “recorded in hand-back summary”
   2. “exact hash reported in hand-back summary”
   3. “SELF_REFERENCE_LIMITATION...” placeholders
   4. any equivalent placeholder language

This pattern is mandatory because:

1. the tracked receipts can now name one immutable authoritative closeout identity
2. the exact commit hash is preserved in Git through the tag target
3. the packaged repo can remain clean
4. no self-referential tracked-file loop is required

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
3. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
4. `tests/AGENTS.override.md`
5. `var/audit/briefs/module_6_serial_spine_implementation_brief_v3.md`
6. `var/audit/2026-04-22_module_6_serial_spine_truth_pass_report.md`
7. `var/audit/nvda_running_audit_log.xlsx`

Do not skim.

---

## Scope

### In scope

1. reconcile the Module 6 tracked receipt surfaces
2. insert the missing required L1 declarations into the tracked report
3. replace placeholder closeout wording with the authoritative closeout ref pattern
4. create the authoritative annotated Git tag
5. rerun the proof floor
6. return a clean unmerged work branch zip including `.git`

### Out of scope

1. changing Module 6 runtime logic
2. changing Module 7 or Module 8 behaviour
3. widening final risk / capital / downstream
4. adding new design scope
5. normative-document rewriting

Do not turn this into another implementation tranche.

---

## Required tracked receipt fixes

### 1. Report completeness

Update `var/audit/2026-04-22_module_6_serial_spine_truth_pass_report.md` so it explicitly contains all of the following:

1. the exact targeted test files named in L1
2. the exact stage packet emitters classified as:
   1. mandatory in this tranche
   2. conditional in this tranche
   3. reserved for later
3. the exact authoritative closeout ref name:
   `module-6-serial-spine-authoritative-closeout-20260422`
4. explicit wording that the annotated tag is the authoritative closeout identity for the packaged repo

The report must not rely on hand-back-summary language.

### 2. Workbook completeness

Update `var/audit/nvda_running_audit_log.xlsx` so the Module 6 rows mirror the report truthfully.

At minimum:

1. the Module 6 L5 row must record the authoritative closeout ref name
2. no workbook cell for Module 6 closeout may rely on:
   1. “exact hash reported in hand-back summary”
   2. placeholder self-reference language
3. the workbook notes/remarks must align with the report wording

### 3. Closeout identity wording

Use direct wording such as:

1. `authoritative_closeout_ref = module-6-serial-spine-authoritative-closeout-20260422`
2. `tag points to final clean packaged branch head`

Do not use vague language.

---

## Required Git actions

Perform these actions in this exact order:

1. update report
2. update workbook
3. commit those receipt reconciliations on the existing Module 6 branch
4. create the annotated tag:
   `module-6-serial-spine-authoritative-closeout-20260422`
5. verify the tag points to the final clean commit
6. verify repo is clean
7. rerun proofs
8. package repo including `.git`

Do not create extra speculative receipt-only commits after the tag unless a concrete blocker remains.

---

## Proof requirements

After the receipt reconciliation commit and authoritative tag creation, rerun exactly:

1. targeted Module 6 proof  
   `PYTHONPATH=src pytest -q tests/tier_a/runtime/test_runtime_orchestrator_surface.py tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py tests/tier_a/vocabulary/test_vocabulary_schema_contract.py tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py tests/tier_b/review_lineage/test_review_replay_dmp_v3_lineage.py`

2. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

3. compile proof  
   `python -m compileall src`

Record the exact outputs in the updated report.

---

## Branch and packaging requirements

1. Leave the branch as `work/module-6-serial-spine-truth-pass-20260422`
2. Leave the branch unmerged
3. The final repo must be **clean**
4. The final repo must include the annotated tag:
   `module-6-serial-spine-authoritative-closeout-20260422`
5. Zip the **full repo including `.git`**
6. Return:
   1. the updated repo zip
   2. a concise execution summary with:
      1. branch name
      2. starting HEAD
      3. final HEAD
      4. authoritative closeout ref name
      5. exact tag target commit
      6. whether the repo is clean
      7. proof results

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. report is complete
2. workbook is complete
3. report and workbook agree
4. one authoritative closeout ref name is recorded in the tracked receipts
5. the annotated tag exists and points to the final clean commit
6. no tracked receipt relies on hand-back-summary placeholder language
7. proofs rerun clean
8. repo is clean
9. branch is unmerged

If any one of those is false, stop and report the blocker truthfully.
