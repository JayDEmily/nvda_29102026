# Module 8 historical receipt normalisation exactness supplementary report — 2026-04-22

## Purpose

This supplementary tranche exists to reconcile report exactness defects in `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md` and then stop.

The defect is confined to tracked report statements that claimed workbook ranges as exact when those ranges did not match the workbook deltas actually present in `var/audit/nvda_running_audit_log.xlsx`.

No runtime, test, specimen, packet, persistence, or historical workbook-value implementation scope is reopened by this supplementary tranche.

## Baseline

- Baseline artefact: `NVIDIA_V7_module_8_historical_receipt_normalisation_closeout_2026-04-22.zip`
- Baseline branch: `work/module-8-historical-receipt-normalisation-20260422`
- Baseline HEAD: `1fa546e2410b3365fcc073e497db0b2f72b8d4ab`
- Prior authoritative closeout tag present at baseline: `module-8-historical-receipt-normalisation-authoritative-closeout-20260422`
- Active remediation branch: `work/module-8-historical-receipt-normalisation-exactness-remediation-20260422`

## Required read set completed before edits

1. `AGENTS.md`
2. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
3. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
4. `var/audit/briefs/module_8_historical_receipt_normalisation_brief.md`
5. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
6. `var/audit/nvda_running_audit_log.xlsx`
7. `var/audit/briefs/module_8_historical_receipt_normalisation_supplementary_exactness_brief_2026-04-22.md`

## SL1 read-and-declare-exactness-remediation-scope

Exact files allowed to change in this supplementary tranche:

1. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
2. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_exactness_supplementary_report.md`
3. `var/audit/nvda_running_audit_log.xlsx`
4. `var/audit/briefs/module_8_historical_receipt_normalisation_supplementary_exactness_brief_2026-04-22.md`

Exact report defects identified at baseline:

1. `SL1` states `Audit_Register!A87:J90`, but the workbook delta present is `Audit_Register!A87:H90`.
2. `SL1` states `Validation_Log!A91:J94`, but the workbook delta present is `Validation_Log!A91:E94`.
3. `SL3` states `Audit_Register!A87:J89`, but the workbook delta present is `Audit_Register!A87:H89`.
4. `SL4` states `Audit_Register!A87:J90`, but the workbook delta present is `Audit_Register!A87:H90`.
5. `SL4` separately lists `Tranche_Leaf_Receipts!F127` and `Tranche_Leaf_Receipts!J127`, but both are already contained within `Tranche_Leaf_Receipts!A125:J128`.

Corrected exact ranges that this supplementary tranche will reconcile into the tracked report:

1. `SL1`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H90`, `Validation_Log!A91:E94`, `Tranche_Leaf_Receipts!A125:J128`
2. `SL3`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H89`, `Validation_Log!A91:E93`, `Tranche_Leaf_Receipts!A125:J127`
3. `SL4`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H90`, `Validation_Log!A91:E94`, `Tranche_Leaf_Receipts!A125:J128`

Mandatory declarations:

1. This supplementary tranche is report-exactness reconciliation only.
2. No runtime, test, specimen, packet, or persistence files are permitted to change.
3. Historical workbook values already landed in the prior tranche are not reopened as substantive scope.
4. The branch remains unmerged throughout this supplementary tranche.

## Open execution leaves

1. `SL1-read-and-declare-exactness-remediation-scope`
2. `SL2-reconcile-report-range-exactness`
3. `SL3-supplementary-report-and-audit-log-receipts`
4. `SL4-proof-and-clean-supplementary-closeout`

## Blockers

None at `SL1`. Baseline branch, HEAD, authoritative closeout tag, and clean repo state matched exactly before work began.

## SL2 reconcile-report-range-exactness

Updated `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md` so every tracked workbook-range statement now matches the workbook delta actually present in `var/audit/nvda_running_audit_log.xlsx`.

Corrected tracked report ranges now in force:

1. `SL1`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H90`, `Validation_Log!A91:E94`, `Tranche_Leaf_Receipts!A125:J128`
2. `SL3`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H89`, `Validation_Log!A91:E93`, `Tranche_Leaf_Receipts!A125:J127`
3. `SL4`: `Tranche_Leaf_Receipts!J101`, `Audit_Register!A87:H90`, `Validation_Log!A91:E94`, `Tranche_Leaf_Receipts!A125:J128`

Removed inexact or redundant report claims:

1. `Audit_Register!A87:J90`
2. `Validation_Log!A91:J94`
3. `Audit_Register!A87:J89`
4. separate final `Tranche_Leaf_Receipts!F127`
5. separate final `Tranche_Leaf_Receipts!J127`

No runtime, test, specimen, packet, or persistence file changed in `SL2`.

## SL3 supplementary-report-and-audit-log-receipts

Appended supplementary tranche receipt rows to `var/audit/nvda_running_audit_log.xlsx` without reopening the historical workbook values themselves as substantive scope.

Receipt staging recorded:

1. baseline branch and HEAD: `work/module-8-historical-receipt-normalisation-20260422` at `1fa546e2410b3365fcc073e497db0b2f72b8d4ab`
2. defect class: report range exactness mismatch
3. corrective objective: reconcile tracked report ranges to the actual workbook deltas and remove overlap
4. explicit note that the historical workbook values already landed in the prior tranche were not reopened as substantive scope
5. closed-leaf receipt rows for `SL1` and `SL2` on branch `work/module-8-historical-receipt-normalisation-exactness-remediation-20260422`

`SL4` proof outputs and final supplementary authoritative closeout reference will be recorded after the final clean closeout commit and annotated tag exist.

## SL4 proof-and-clean-supplementary-closeout

No runtime, test, specimen, packet, or persistence file changed in this supplementary tranche.

Proof outputs:

1. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 3.13s
```

2. `python -m compileall src`

```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/adapters'...
Listing 'src/nvda_desk/adapters/egress'...
Listing 'src/nvda_desk/adapters/ingress'...
Listing 'src/nvda_desk/analysis'...
Listing 'src/nvda_desk/analysis/replay'...
Listing 'src/nvda_desk/api'...
Listing 'src/nvda_desk/api/http'...
Listing 'src/nvda_desk/calendar'...
Listing 'src/nvda_desk/calendar/operational'...
Listing 'src/nvda_desk/calendar/reference'...
Listing 'src/nvda_desk/capital'...
Listing 'src/nvda_desk/cognition'...
Listing 'src/nvda_desk/cognition/ingress'...
Listing 'src/nvda_desk/cognition/modifiers'...
Listing 'src/nvda_desk/cognition/serial'...
Listing 'src/nvda_desk/config'...
Listing 'src/nvda_desk/contracts'...
Listing 'src/nvda_desk/domain'...
Listing 'src/nvda_desk/domain/capital'...
Listing 'src/nvda_desk/domain/downstream'...
Listing 'src/nvda_desk/domain/eligibility'...
Listing 'src/nvda_desk/domain/execution'...
Listing 'src/nvda_desk/domain/final_risk'...
Listing 'src/nvda_desk/domain/options_flow'...
Listing 'src/nvda_desk/domain/parallel_risk'...
Listing 'src/nvda_desk/domain/posture'...
Listing 'src/nvda_desk/domain/regime'...
Listing 'src/nvda_desk/domain/temporal'...
Listing 'src/nvda_desk/downstream'...
Listing 'src/nvda_desk/entry'...
Listing 'src/nvda_desk/ingress'...
Listing 'src/nvda_desk/packets'...
Listing 'src/nvda_desk/persistence'...
Listing 'src/nvda_desk/persistence/migrations'...
Listing 'src/nvda_desk/preparation'...
Listing 'src/nvda_desk/reference'...
Listing 'src/nvda_desk/repositories'...
Listing 'src/nvda_desk/risk'...
Listing 'src/nvda_desk/risk/join'...
Listing 'src/nvda_desk/risk/parallel'...
Listing 'src/nvda_desk/runtime'...
Listing 'src/nvda_desk/schemas'...
Listing 'src/nvda_desk/services'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

Supplementary authoritative closeout ref to create on the final clean commit:

- `module-8-historical-receipt-normalisation-exactness-authoritative-closeout-20260422`

Files changed in this supplementary tranche:

1. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_report.md`
2. `var/audit/2026-04-22_module_8_historical_receipt_normalisation_exactness_supplementary_report.md`
3. `var/audit/nvda_running_audit_log.xlsx`
4. `var/audit/briefs/module_8_historical_receipt_normalisation_supplementary_exactness_brief_2026-04-22.md`

Results:

1. The tracked report now uses the exact corrected ranges required by this supplementary brief.
2. The supplementary report records the baseline, defect class, corrected ranges, and proof outputs.
3. The running audit workbook was appended for this supplementary tranche without reopening the prior historical workbook values as substantive scope.
4. The branch remains unmerged.

