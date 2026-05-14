# Module 8 — supplementary brief for historical receipt report exactness reconciliation

## Purpose

This brief fixes the remaining closeout defect in the current Module 8 historical receipt-normalisation tranche.

The defect is **not** in runtime code, tests, packets, persistence, or the historical workbook values themselves.

The defect is that the tracked report claims certain workbook ranges as **exact** when those ranges do not match the actual workbook deltas.

This supplementary tranche is therefore **report-exactness reconciliation only**, with normal receipt closeout and proof rerun.

Do **not** reopen Module 8 implementation, Temporal tranche work, Tranche 4 work, or any runtime/design surface.

---

## Baseline

Start from the submitted Module 8 historical receipt-normalisation closeout repo exactly as handed back for audit.

Expected starting state after unzip:

1. artefact: `NVIDIA_V7_module_8_historical_receipt_normalisation_closeout_2026-04-22.zip`
2. branch: `work/module-8-historical-receipt-normalisation-20260422`
3. committed HEAD: `1fa546e2410b3365fcc073e497db0b2f72b8d4ab`
4. authoritative closeout tag present:
   `module-8-historical-receipt-normalisation-authoritative-closeout-20260422`
5. repo clean: yes

If the provided repo does not match that exact branch, HEAD, tag, and clean starting state, stop and report the blocker.

---

## Problem statement

The current report `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md` contains inexact workbook-range statements.

Observed defects to correct:

1. In `SL1`, the report states `Audit_Register!A87:J90`, but the actual workbook delta is `Audit_Register!A87:H90`.
2. In `SL1`, the report states `Validation_Log!A91:J94`, but the actual workbook delta is `Validation_Log!A91:E94`.
3. In `SL3`, the report states `Audit_Register!A87:J89`, but the actual workbook delta is `Audit_Register!A87:H89`.
4. In `SL4`, the report states `Audit_Register!A87:J90`, but the actual workbook delta is `Audit_Register!A87:H90`.
5. In `SL4`, the report lists `Tranche_Leaf_Receipts!F127` and `Tranche_Leaf_Receipts!J127` separately even though both are already contained within `Tranche_Leaf_Receipts!A125:J128`.

This means the report does **not** presently satisfy its own requirement to state exact workbook cells changed.

---

## Why this supplementary tranche exists

The current branch is materially close, but `docs/01_NORMATIVE_CORE.md` defines done as binary.

A tracked report that claims exact workbook ranges must be exact.

The next tranche must **not** start from a branch whose receipt surface still contains a known exactness defect.

This brief closes that defect cleanly, then stops.

---

## Mandatory read order before changing anything

Read these in full, in this order:

1. `AGENTS.md`
2. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
3. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
4. `var/audit/briefs/module_8_historical_receipt_normalisation_brief.md`
5. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
6. `var/audit/nvda_running_audit_log.xlsx`
7. this brief

Do not skim.

---

## Scope

### In scope

1. reconcile the report so every workbook-range statement is exact and non-overlapping
2. add one supplementary report that records:
   1. the baseline used
   2. the exact defect found
   3. the exact corrected workbook ranges
   4. the proof outputs
3. append the live running audit log with this supplementary tranche receipt
4. create one new clean authoritative supplementary closeout tag
5. rerun the proof floor
6. return a clean unmerged repo zip including `.git`

### Out of scope

1. changing runtime code
2. changing tests
3. changing packet/specimen/persistence surfaces
4. reopening Module 8 implementation scope
5. reopening Temporal tranche scope
6. attempting Tranche 4 work or closeout
7. rewriting normative docs
8. changing the historical workbook truth surfaces already landed in the prior tranche, except where a direct transcription defect is proven

Do not widen this into another implementation tranche.

---

## Files allowed to change

Only these files may change in this supplementary tranche unless a blocker proves another receipt surface is strictly required:

1. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
2. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_exactness_supplementary_report.md`
3. `var/audit/nvda_running_audit_log.xlsx`
4. one copy of this brief under `var/audit/briefs/`

If anything outside that set appears necessary, stop and report the blocker before proceeding.

---

## Exact report corrections required

### 1. SL1 declaration correction

In the `SL1` section of `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`, the exact workbook sheets and cells for the full tranche must be corrected to this exact set:

1. `Tranche_Leaf_Receipts!J101`
2. `Audit_Register!A87:H90`
3. `Validation_Log!A91:E94`
4. `Tranche_Leaf_Receipts!A125:J128`

Do not use `Audit_Register!A87:J90`.
Do not use `Validation_Log!A91:J94`.

### 2. SL3 workbook-delta correction

In the `SL3` section, the workbook cells changed in `SL3` must be stated exactly as:

1. `Tranche_Leaf_Receipts!J101`
2. `Audit_Register!A87:H89`
3. `Validation_Log!A91:E93`
4. `Tranche_Leaf_Receipts!A125:J127`

Do not use `Audit_Register!A87:J89`.

### 3. SL4 final-delta correction

In the `SL4` section, the final workbook cells changed in the tranche must be stated exactly as this **non-overlapping** set:

1. `Tranche_Leaf_Receipts!J101`
2. `Audit_Register!A87:H90`
3. `Validation_Log!A91:E94`
4. `Tranche_Leaf_Receipts!A125:J128`

Do **not** keep redundant sub-cells such as `Tranche_Leaf_Receipts!F127` or `Tranche_Leaf_Receipts!J127` as separate final entries, because they are already contained inside `Tranche_Leaf_Receipts!A125:J128`.

### 4. Supplementary report content

Create `var/audit/2026-04-22_module_8_historical_receipt_normalisation_exactness_supplementary_report.md`.

It must explicitly state:

1. the exact baseline branch and HEAD
2. the prior authoritative closeout tag present at baseline
3. the exact report defects found
4. the exact corrected ranges now used in `SL1`, `SL3`, and `SL4`
5. that no runtime, test, specimen, packet, or persistence files changed
6. the proof outputs
7. the new supplementary authoritative closeout ref name
8. that the branch remains unmerged

### 5. Running-audit-log receipt

Append new rows to `var/audit/nvda_running_audit_log.xlsx` for this supplementary tranche.

Those rows must record, at minimum:

1. baseline branch and HEAD
2. the exact defect class: report range exactness mismatch
3. the corrective objective: reconcile report ranges to actual workbook deltas
4. that the historical workbook values themselves were not reopened as substantive scope
5. the new supplementary authoritative closeout ref name

Do not overwrite prior history.

---

## Required leaf structure

Use this exact bounded sequence:

1. `SL1-read-and-declare-exactness-remediation-scope`
2. `SL2-reconcile-report-range-exactness`
3. `SL3-supplementary-report-and-audit-log-receipts`
4. `SL4-proof-and-clean-supplementary-closeout`

Only one leaf is active at a time.
Each closed leaf gets its own commit.

---

## Required Git actions

Perform these actions in this exact order:

1. create a new branch from the baseline closeout commit:
   `work/module-8-historical-receipt-normalisation-exactness-remediation-20260422`
2. complete `SL1`
3. complete `SL2`
4. complete `SL3`
5. complete `SL4`
6. create one annotated tag on the final clean supplementary closeout commit named:
   `module-8-historical-receipt-normalisation-exactness-authoritative-closeout-20260422`
7. verify the tag points to the final clean commit
8. verify the repo is clean
9. package the repo including `.git`

Do not continue working on the old branch.
Do not move to the next tranche from the old closeout tag.

---

## Proof requirements

After the final supplementary closeout commit, rerun exactly:

1. full shell proof  
   `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

2. compile proof  
   `python -m compileall src`

Record the exact outputs in the supplementary report.

This is a receipt-only supplementary tranche, but the proof floor must still be rerun so the branch remains promotable.

---

## Branch and packaging requirements

1. final branch must be `work/module-8-historical-receipt-normalisation-exactness-remediation-20260422`
2. leave the branch unmerged
3. final repo must be clean
4. final repo must include the annotated supplementary closeout tag:
   `module-8-historical-receipt-normalisation-exactness-authoritative-closeout-20260422`
5. zip the full repo including `.git`

Return:

1. updated repo zip
2. concise execution summary with:
   1. branch name
   2. starting HEAD
   3. final HEAD
   4. supplementary authoritative closeout ref name
   5. exact tag target commit
   6. whether repo is clean
   7. proof results
   8. exact files changed

---

## Definition of done

This supplementary brief is complete only if all of the following are true:

1. the report’s `SL1`, `SL3`, and `SL4` workbook-range statements are exact
2. the final workbook-range statements are non-overlapping
3. the supplementary report exists and states the exact defect and exact correction
4. the running audit log is appended for this supplementary tranche
5. no runtime, test, specimen, packet, or persistence files changed
6. proofs reran clean
7. repo is clean
8. branch remains unmerged
9. the supplementary authoritative closeout tag exists and points to the final clean commit
10. the old branch is no longer the branch proposed for next-tranche continuation

If any one of those is false, stop and report the blocker truthfully.
