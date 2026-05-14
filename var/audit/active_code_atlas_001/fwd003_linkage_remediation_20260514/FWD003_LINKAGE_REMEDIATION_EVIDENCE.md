# FWD-003 linkage remediation evidence

## Gate

FWD-003 / 5.16 Persistence, ledgers, and receipts.

## Prior blocker

`FWD003_DIRECT_ATLAS_BRIDGE_LINKAGE_GAP_AFTER_CURRENT_THREE_WAY_COMPARISON`

Prior closure-gate report recorded 38 direct active-code Atlas links across 97 selected native persistence records, leaving 59 records without explicit one-to-one active-record linkage.

## Remediation rule

The previous blocker is resolved only where a native Atlas ID has either:

1. direct active-code Atlas linkage through `linked_atlas_record_ids`; or
2. grouped satisfaction through its selected Bridge comparison record (`ACABC-*`) and test-first queue record (`ACATQ-*`), where active-code records explicitly link to both records.

This pass does not invent one-to-one links for records that the active-code Atlas does not directly link. It records the lawful grouped overlay separately.

## Result

| Measure | Count |
|---|---:|
| Selected native persistence Atlas IDs | 97 |
| Direct active-code linked IDs from prior gate | 38 |
| Previously unlinked IDs | 59 |
| Resolved by grouped-satisfaction overlay | 59 |
| Resolved by direct + grouped evidence | 38 |
| Current covered IDs | 97 |
| Current unresolved IDs | 0 |

## Group evidence

| Native status | Comparison | Queue | Native records | Previously unlinked now group-resolved | Active-code records |
|---|---|---|---:|---:|---|
| `transform_required` | `ACABC-0040` | `ACATQ-0039` | 23 | 8 | `ACATP-006-0001` |
| `missing` | `ACABC-0041` | `ACATQ-0040` | 18 | 0 | `ACATP-005-0001, ACATP-005-0002` |
| `partially_satisfied` | `ACABC-0042` | `ACATQ-0041` | 56 | 51 | `ACATP-004-0001, ACATP-004-0002, ACATP-004-0003, ACATP-004-0004, ACATP-004-0005, ACATP-004-0006` |

## Remaining unresolved IDs

None.

## Evidence files

- Machine-readable report: `var/audit/active_code_atlas_001/fwd003_linkage_remediation_20260514/FWD003_LINKAGE_REMEDIATION_REPORT.json`
- Per-Atlas resolution table: `var/audit/active_code_atlas_001/fwd003_linkage_remediation_20260514/FWD003_LINKAGE_REMEDIATION_PER_ATLAS_RECORD.tsv`
- Prior selected input: `var/audit/active_code_atlas_001/fwd003_closure_gate_20260514/FWD003_SELECTED_ATLAS_BRIDGE_ACTIVE_RECORDS.json`
- Prior comparison report: `var/audit/active_code_atlas_001/fwd003_closure_gate_20260514/FWD003_THREE_WAY_COMPARISON_REPORT.json`
- Prior closure evidence: `var/audit/active_code_atlas_001/fwd003_closure_gate_20260514/FWD003_CLOSURE_GATE_EVIDENCE.md`

## Scope control

No source, test, config, fixture, dependency, original Atlas/Bridge JSON, generated slice, or frozen control-file mutation is recorded by this remediation file.

## Final proof/status capture

- Proof summary: `var/audit/active_code_atlas_001/fwd003_linkage_remediation_20260514/FWD003_LINKAGE_REMEDIATION_PROOF_SUMMARY.json`
- Captured status `0`: manifest validation, `git diff --check`, `proof_blocks --check-all`, and all three FWD-003 targeted proof blocks.
- Monolithic Tier A/B pytest attempts are retained in `reports/`; no closure claim relies on uncaptured monolithic exit codes.
