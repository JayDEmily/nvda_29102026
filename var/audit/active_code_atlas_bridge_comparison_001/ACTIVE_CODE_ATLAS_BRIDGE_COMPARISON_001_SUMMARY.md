# ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001 summary

Status: `static_comparison_generated_no_refactor_opened`

## Inputs

- Atlas intent corpus: `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json` records=1716
- Atlas Bridge ledger: `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json` records=1716
- Structural inventory scaffold: `var/audit/active_code_atlas_001/active_code_atlas.json` records=4075

## Result counts

- comparison records: 48
- bridge records accounted for: 1716
- Atlas records joined: 1716
- test-first queue records: 46
- record-level join records: 1716

## Group status counts

| Status | Count |
|---|---:|
| `already_satisfied` | 2 |
| `partially_satisfied` | 28 |
| `transform_required` | 18 |

## Record-level join status counts

| Join status | Count |
|---|---:|
| `active_symbol_and_surface_test_evidence_present` | 35 |
| `active_symbol_present_different_surface_or_owner` | 54 |
| `same_surface_evidence_only` | 1627 |

## Test-first action counts

| Action | Count |
|---|---:|
| `confirm_existing_proof_only_no_refactor` | 2 |
| `extend_existing_test_family_before_code` | 17 |
| `write_new_test_family_before_code` | 29 |

## Guardrail

This output is static comparison only. It does not execute pytest/proof blocks and does not authorise source refactor, feature import, test implementation, dependency changes, vocabulary mutation, original Atlas/Bridge mutation, or generated slice rebuild.

## Files emitted

- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison_summary.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_queue.json`


## External audit correction

The current artefact is classified as `ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001` / static structural inventory scaffold only. It is useful navigation evidence, not the completed primary active-code Atlas.

Required limitation:

```text
This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status.
```

Selected contributing files must still be read in full surface-by-surface before records can be accepted as primary active-code Atlas records.
