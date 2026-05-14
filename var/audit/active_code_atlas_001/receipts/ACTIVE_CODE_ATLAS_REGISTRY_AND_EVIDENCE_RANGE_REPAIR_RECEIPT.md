# ACTIVE_CODE_ATLAS_REGISTRY_AND_EVIDENCE_RANGE_REPAIR_RECEIPT

Status: `PASS` for the auditor-blocking registry and evidence-range repair only.

This receipt does not accept the all-surface primary active-code Atlas. The generated all-surface artefact remains `ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001`, a navigation scaffold only.

Required limitation statement:

```text
This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status.
```

## 1. Scope

Repair requested by external branch auditor:

1. Move `tests/tier_b/proof_model/test_checkpoint_receipt_contract.py` out of `tier_a_registry_reconciliation_inventory` and into `tier_b_registry_reconciliation_inventory` in `config/retained_test_registry.yaml`.
2. Keep Tier A declared/actual inventory count at `95`.
3. Update Tier B declared/actual inventory count from `11` to `12`.
4. Ensure no `tests/tier_b` paths remain under the Tier A inventory and no `tests/tier_a` paths exist under the Tier B inventory.
5. Repair out-of-bounds evidence ranges in surface-specific active-code Atlas records.
6. Add recurring validation so the same defects cannot recur silently.
7. Rerun relevant proof commands and update `ROADMAP_LEDGER.md` and receipts.

## 2. Registry repair

Changed:

```text
config/retained_test_registry.yaml
```

Observed repaired state:

```text
tier_a_test_count=95
tier_a_entries=95
tier_a_registered_retained_seed_tier_a=95
tier_b_paths_under_tier_a=0

tier_b_test_count=12
tier_b_entries=12
tier_b_registered_retained_tier_b=12
tier_b_covered_by_command_or_owns_after_amendment=12
tier_a_paths_under_tier_b=0
```

`tests/tier_b/proof_model/test_checkpoint_receipt_contract.py` is now recorded under `tier_b_registry_reconciliation_inventory` with `registry_status: registered_retained_tier_b`.

## 3. Evidence-range repair

Changed:

```text
var/audit/active_code_atlas_001/vocabulary_governance_surface/vocabulary_governance_active_code_atlas_records.json
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface/testing_proof_checkpoint_active_code_atlas_records.json
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface_transform_required/testing_proof_checkpoint_transform_required_records.json
```

Repaired evidence ranges:

```text
tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py: line_end 107 -> 95
tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py: line_end 97 -> 86
config/proof_blocks.yaml: line_end 9999 -> 383
var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_execution_queue.json: line_end 9999 -> 1273
config/retained_test_registry.yaml: old stale range 2982-2983 -> repaired Tier B inventory entry range 2759-2760
```

## 4. Validation hardening added

Added:

```text
var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py
```

Report:

```text
var/audit/active_code_atlas_001/reports/validate_surface_records_and_registry_output.json
```

The validation enforces:

- every evidence path exists;
- every evidence path is a file;
- every `line_start` / `line_end` is an integer range within actual file length;
- Tier A inventory entries must start with `tests/tier_a/`;
- Tier B inventory entries must start with `tests/tier_b/`;
- declared inventory totals match entry counts;
- declared registered-status counts match actual registry-status counts;
- duplicate registry inventory paths are rejected.

Observed validation result:

```text
validation_status=PASS
error_count=0
warning_count=0
surface_record_file_count=3
surface_record_count=16
evidence_entry_count=106
unique_evidence_path_count=38
tier_a_declared_total=95
tier_a_entry_count=95
tier_b_declared_total=12
tier_b_entry_count=12
```

## 5. Proof and command evidence rerun

Commands rerun:

```bash
python3 var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py
PYTHONPATH=src python3.13 -m pytest tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py -q
PYTHONPATH=src python3.13 -m pytest tests/tier_a/vocabulary/test_vocabulary_schema_contract.py tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_classification_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_payload_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py -q
PYTHONPATH=src python3.13 scripts/vocabulary_synonym_audit.py --check-clean
PYTHONPATH=src python3.13 -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py -q
PYTHONPATH=src python3.13 scripts/run_proof_block.py --block proof_executor_contract
PYTHONPATH=src python3.13 -m pytest tests/tier_b/proof_model/test_checkpoint_receipt_contract.py -q
PYTHONPATH=src python3.13 scripts/run_proof_block.py --block checkpoint_receipt_contract
PYTHONPATH=src python3.13 -m pytest tests/tier_b/proof_model -q
PYTHONPATH=src python3.13 scripts/run_proof_block.py --check-all
git diff --check
```

Observed outputs/statuses:

```text
validate_surface_records_and_registry_status=0
candidate_review_cli_pytest_status=0; 16 passed in 17.93s
vocabulary_governance_conformance_candidate_pytest_status=0; 114 passed in 39.43s
vocabulary_synonym_audit_clean_check_status=0; vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
proof_executor_contract_pytest_status=0; 20 passed in 33.12s
proof_executor_contract_proof_block_status=0; 20 passed in 33.08s
checkpoint_receipt_contract_pytest_status=0; 2 passed in 0.56s
checkpoint_receipt_contract_proof_block_status=0; 2 passed in 0.53s
proof_model_pytest_status=0; 22 passed in 32.88s
proof_blocks_check_all_status=0; proof_blocks_check_all=PASS count=19
git_diff_check_status=0
```

## 6. Receipts and reports updated

Updated:

```text
var/audit/active_code_atlas_001/vocabulary_governance_surface/vocabulary_governance_validation_report.json
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface/testing_proof_checkpoint_validation_report.json
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface_transform_required/testing_proof_checkpoint_transform_required_validation_report.json
var/audit/active_code_atlas_001/vocabulary_governance_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_001_VOCABULARY_GOVERNANCE_SURFACE_RECEIPT.md
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_002_TESTING_PROOF_CHECKPOINT_SURFACE_RECEIPT.md
var/audit/active_code_atlas_001/testing_proof_checkpoint_surface_transform_required/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_003_TESTING_PROOF_CHECKPOINT_SURFACE_TRANSFORM_REQUIRED_RECEIPT.md
ROADMAP_LEDGER.md
PLANS.md
```

## 7. Boundaries held

No source implementation file was changed.

No dependency file, VENV, original Atlas JSON, Bridge JSON, generated Atlas slice, vocabulary data file, runtime trading path, or refactor work was changed.

The structural inventory remains navigation only.

## 8. Next pointer

The next queue row remains:

```text
ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_004_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE
```

Queue basis: `ACATQ-0041` / `ACABC-0042`, blueprint surface `Persistence, ledgers, and receipts`, required action `extend_existing_test_family_before_code`, proof tier `Tier A`.
