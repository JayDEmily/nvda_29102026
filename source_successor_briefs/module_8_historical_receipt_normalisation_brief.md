# Module 8 — supplementary historical receipt-normalisation brief
## Remove hand-back-summary placeholder dependency, then stop

## Purpose

This brief exists because the attempted **Tranche 4 repo-wide audit** correctly found a **historical tracked-receipt blocker** in the older accepted Module 8 closeout surfaces.

This brief is for the **same execution thread** that attempted Tranche 4.

The required action is:

1. **disregard the blocked Tranche 4 attempt**
2. return to the latest accepted baseline
3. perform one **narrow historical Module 8 receipt-normalisation tranche**
4. close that tranche out cleanly
5. stop and await further instructions

Do **not** continue Tranche 4 from the blocked state.
Do **not** try to patch Tranche 4 in place.

---

## Mandatory instruction about the blocked Tranche 4 attempt

The prior Tranche 4 attempt is **not** to be continued.

Treat it as:

1. a valid failed audit attempt
2. a useful blocker discovery
3. **not** the branch/repo state to continue from

That means:

1. do **not** keep the blocked Tranche 4 branch as the move-forward baseline
2. do **not** create `temporal-standard-tranche-4-authoritative-closeout-20260422`
3. do **not** create a Tranche 4 success report
4. do **not** update the workbook as if Tranche 4 passed
5. do **not** package a Tranche 4 success repo

The blocked Tranche 4 attempt should be disregarded for execution purposes except as blocker evidence.

---

## Correct baseline to use

Use the **accepted Tranche 3 supplementary preparation/raw-bundle closeout repo** as the remediation baseline.

Required baseline artefact:

- `NVIDIA_V7_temporal_standard_tranche_3_supplementary_preparation_raw_bundle_closeout_2026-04-22.zip`

Required starting state after unzip:

1. branch: `work/temporal-standard-tranche-3-supplementary-preparation-raw-bundle-remediation-20260422`
2. committed HEAD: `b976398b018c3a54b72fb998d9aad7a2df1d0386`
3. repo clean: yes
4. authoritative closeout tag present:
   `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-preparation-raw-bundle`

Create the new remediation branch from that exact state.

Required new branch name:

- `work/module-8-historical-receipt-normalisation-20260422`

If the provided repo is not actually on:
1. branch `work/temporal-standard-tranche-3-supplementary-preparation-raw-bundle-remediation-20260422`
2. clean HEAD `b976398b018c3a54b72fb998d9aad7a2df1d0386`
3. with tag `temporal-standard-tranche-3-authoritative-closeout-20260422-supplementary-preparation-raw-bundle`

stop immediately and report the blocker before doing any other work.

---

## Why this supplementary tranche exists

The blocked Tranche 4 audit found that older accepted Module 8 tracked receipts still rely on forbidden placeholder wording.

### Blocker evidence already identified

1. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md:46`
   still uses hand-back-summary placeholder wording for the Module 8 RL5/final closeout identity

2. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md:283`
   still states the exact final closeout hash is reported in the hand-back summary

3. `var/audit/nvda_running_audit_log.xlsx`
   sheet `Tranche_Leaf_Receipts`, cell `J101`
   still mirrors that same placeholder dependency

That wording conflicts with the later authoritative-closeout discipline now used by the project.

This tranche exists to remove that historical receipt defect cleanly.

---

## Mandatory execution posture

1. Work on the new historical-normalisation branch only.
2. Do **not** merge to `main`.
3. Do **not** continue the blocked Tranche 4 branch.
4. Do **not** change runtime code, persistence code, packet builders, harness code, specimen artefacts, or tests in this tranche.
5. Do **not** widen Module 8 Stage B/C, Module 9, Module 10, or Module 11.
6. Do **not** reopen any accepted implementation scope.
7. Read all required governing files and receipt files **in full** before changing anything.
8. If output truncates, continue reading in chunks until the required source is fully read.
9. One active leaf at a time.
10. Return a clean committed work branch zip including `.git`.

This historical-normalisation tranche succeeds only if it stays narrow.

---

## Blocker discipline — mandatory

If a blocker is encountered, the executor must:

1. stop immediately
2. make no further changes
3. not improvise
4. not keep going “just to see”
5. not partially execute later leaves
6. not create substitute assumptions
7. return the exact blocker with evidence

The executor is not allowed to wing it, keep going anyway, or work around it silently.

---

## Anti-shortcut / anti-path-to-green discipline — mandatory

The executor must not optimise for:

1. the smallest apparent wording tweak
2. the fastest route to green
3. avoiding receipt updates
4. keeping old placeholder wording alive for convenience

Instead, optimise for:

1. exact brief conformance
2. full required reading
3. truthful receipt normalisation
4. one authoritative closeout mechanism only

Green proofs do not excuse skipped required receipt work.

---

## Scope

### In scope

This supplementary tranche is limited to **historical Module 8 receipt normalisation only**.

At minimum this includes:

1. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
2. `var/audit/nvda_running_audit_log.xlsx`

And, if directly coupled and truthfully required:

3. one brief copy under `var/audit/briefs/`
4. one updated receipt note in the running audit workbook

### Out of scope

1. runtime code
2. persistence code
3. packet builders
4. harnesses
5. specimen artefacts
6. tests
7. Tranche 4 execution
8. normative-document rewrites
9. backward-compatibility layers of any kind

If anything outside this narrow historical receipt scope appears necessary, stop and report the blocker.
Do **not** expand the tranche.

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
3. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
4. `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md`
5. `var/audit/2026-04-22_temporal_standard_tranche_4_repo_wide_audit_report.md` if present, otherwise use the blocker note supplied by the user as the Tranche 4 failed-audit evidence
6. `var/audit/nvda_running_audit_log.xlsx`

Do not start changing anything until the full read is complete.

---

## Required normalisation rule

The historical Module 8 tracked receipts must no longer rely on hand-back-summary placeholder wording.

That means:

1. do **not** keep wording like:
   1. `exact hash reported in the hand-back summary`
   2. `recorded in the hand-back summary`
   3. equivalent placeholder/self-reference wording

2. replace that pattern with **one authoritative closeout ref name** recorded directly in the tracked receipts

3. preserve a truthful historical note that this is a later receipt-normalisation tranche, not a claim that the original old closeout used the newer tag model

---

## Required closeout model for this historical normalisation

Use one explicit historical authoritative closeout ref for Module 8:

- `module-8-historical-receipt-normalisation-authoritative-closeout-20260422`

This tranche must:

1. create one final bounded receipt-normalisation commit
2. create one annotated tag with that exact name
3. point that tag to the final clean historical-normalisation commit
4. update the historical Module 8 report to record that exact authoritative closeout ref name
5. update the workbook to record that same exact authoritative closeout ref name in the Module 8 receipt cell(s)

Do **not** preserve the hand-back-summary placeholder wording anywhere in the active tracked Module 8 receipt surfaces after this tranche closes.

---

## Required implementation rules

### A. Historical report correction

Update `var/audit/2026-04-21_module_8_parallel_risk_lane_truth_pass_report.md` so it explicitly states:

1. the old hand-back-summary placeholder dependency has been superseded by this historical receipt-normalisation tranche
2. the authoritative closeout ref for historical tracked-receipt purposes is:
   `module-8-historical-receipt-normalisation-authoritative-closeout-20260422`
3. the tag points to the final clean receipt-normalisation commit

### B. Workbook correction

Update `var/audit/nvda_running_audit_log.xlsx` so the Module 8 receipt cells no longer rely on hand-back-summary placeholder wording.

At minimum correct:

1. the `Tranche_Leaf_Receipts` Module 8 RL5/final-closeout cell previously identified as `J101`

Also correct any other directly coupled Module 8 receipt cell if it still mirrors the same placeholder pattern.

### C. No implementation drift

Do **not**:
1. change runtime/code/test logic
2. re-open Module 8 implementation
3. re-open Tranche 3 implementation
4. attempt Tranche 4 closeout here

This is historical receipt normalisation only.

---

## Mandatory L1 declarations before editing

In **L1**, before any edit leaf starts, record in the supplementary report:

1. exact files to change
2. exact workbook cells/sheets to change
3. explicit statement that:
   1. the blocked Tranche 4 attempt is disregarded and not continued
   2. this tranche starts from accepted baseline `b976398b018c3a54b72fb998d9aad7a2df1d0386`
   3. old Module 8 hand-back-summary placeholder wording will be removed from tracked receipts
   4. no runtime/test/specimen changes are allowed

If any of those cannot be stated exactly, stop and report the blocker before doing further work.

---

## Required leaf structure

Use this exact bounded sequence unless a blocker prevents it:

1. `SL1-read-scope-and-historical-receipt-declarations`
2. `SL2-module-8-report-receipt-normalisation`
3. `SL3-workbook-receipt-normalisation`
4. `SL4-report-workbook-proof-and-clean-closeout`

One active leaf at a time.
Do not batch everything into one opaque commit.

---

## Proof requirements

After the final historical-normalisation closeout commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record exact outputs in the updated report.

This tranche must not change tests, but it must still prove the repo remains clean and intact after the receipt-only change.

---

## Receipt requirements

Maintain and return:

1. one new report:
   `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
2. updated `var/audit/nvda_running_audit_log.xlsx`
3. one brief copy under `var/audit/briefs/`

The new report must explicitly state:

1. the blocked Tranche 4 attempt was disregarded for execution purposes and not continued
2. this historical receipt-normalisation tranche began from accepted baseline `b976398b018c3a54b72fb998d9aad7a2df1d0386`
3. the old Module 8 hand-back-summary placeholder dependency was removed
4. the authoritative closeout ref used is:
   `module-8-historical-receipt-normalisation-authoritative-closeout-20260422`
5. exact workbook cells changed
6. proof outputs

The report must not rely on hand-back-summary placeholders.

---

## Authoritative closeout mechanism — mandatory

Use this exact pattern:

1. make one final bounded historical-normalisation closeout commit on the existing historical-normalisation branch
2. create one annotated Git tag named:

`module-8-historical-receipt-normalisation-authoritative-closeout-20260422`

3. the tag must point to the final clean historical-normalisation closeout commit
4. tracked receipts must record that exact authoritative closeout ref name
5. do not use hand-back-summary placeholder wording

---

## Branch and packaging requirements

1. leave the branch as `work/module-8-historical-receipt-normalisation-20260422`
2. leave the branch unmerged
3. final repo must be clean
4. include the annotated historical-normalisation closeout tag
5. zip the full repo including `.git`

Return:

1. updated repo zip
2. concise execution summary with:
   1. branch name
   2. starting HEAD
   3. final HEAD
   4. historical-normalisation authoritative closeout ref name
   5. exact tag target commit
   6. whether repo is clean
   7. proof results
   8. exact files changed
   9. exact workbook cells changed

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. the blocked Tranche 4 attempt was disregarded and not continued
2. the work started from accepted baseline `b976398b018c3a54b72fb998d9aad7a2df1d0386`
3. the historical Module 8 report no longer relies on hand-back-summary placeholder wording
4. the workbook Module 8 receipt cells no longer rely on hand-back-summary placeholder wording
5. no runtime/test/specimen changes were made
6. the new historical-normalisation report is complete
7. workbook is updated
8. proofs rerun clean
9. repo is clean
10. branch remains unmerged
11. historical-normalisation authoritative closeout tag exists and points to the final clean commit

If any one of those is false, stop and report the blocker truthfully.
