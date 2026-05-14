# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_001_VOCABULARY_GOVERNANCE_SURFACE_RECEIPT

Status: `PASS` for the first vocabulary-governance surface pass only.

This receipt does not accept the all-surface primary active-code Atlas. The previously generated all-surface artefact remains `ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001`, a navigation scaffold only.

Required limitation statement:

```text
This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status.
```

Surface limitation:

```text
This vocabulary-governance surface slice is read-adjudicated for the cited files only. It does not convert the full structural inventory into an accepted all-surface primary active-code Atlas.
```

## 1. Scope

Surface: `5.18 Vocabulary governance interface` / `Vocabulary governance interface`.

Queue records addressed from the proposed queue:

- `ACATQ-0046` / `ACABC-0047`
- `ACATQ-0045` / `ACABC-0046`
- `ACATQ-0044` / `ACABC-0045`

The generated structural inventory and comparison were used only as navigation. The surface records in this pass were confirmed or rewritten from read evidence.

## 2. Read intake completed for this surface

Normative/control files read for this surface included:

- `AGENTS.md`
- `tests/AGENTS.override.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `docs/reference/vocabulary_dictionary_system_audit.md`
- `data/vocabulary/README.md`
- `data/vocabulary/feeder/README.md`

Selected active source files read for this surface included:

- `src/nvda_desk/schemas/vocabulary.py`
- `src/nvda_desk/vocabulary_builder.py`
- `src/nvda_desk/vocabulary_synonym_audit.py`
- `src/scripts/build_canonical_vocabulary.py`
- `src/scripts/vocabulary_synonym_audit.py`
- `scripts/vocabulary_synonym_audit.py`
- `scripts/vocabulary_candidate_review.py`

Selected active test files read for this surface included:

- `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_classification_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_payload_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`
- `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py`
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`
- `tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py`

Relevant proof/registry surfaces inspected for this surface:

- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`

## 3. Surface records written

Surface record file:

```text
var/audit/active_code_atlas_001/vocabulary_governance_surface/vocabulary_governance_active_code_atlas_records.json
```

Validation file:

```text
var/audit/active_code_atlas_001/vocabulary_governance_surface/vocabulary_governance_validation_report.json
```

Counts:

- surface records: `10`
- linked Atlas records: `10`
- linked Bridge records: `10`
- validation status: `PASS`

## 4. Test-first change

Added one Tier A test before any source change:

```text
tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py::test_candidate_review_cli_does_not_mutate_canonical_vocabulary_file
```

Purpose: prove that the candidate-review CLI writes output and receipt artefacts without mutating the canonical vocabulary input file when run with `--check-clean`.

No source repair was required because the added test passed against existing source.

## 5. Validation evidence

Commands run:

```bash
PYTHONPATH=src python3.13 -m pytest tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py -q
PYTHONPATH=src python3.13 -m pytest tests/tier_a/vocabulary/test_vocabulary_schema_contract.py tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_classification_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_payload_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py -q
PYTHONPATH=src python3.13 scripts/vocabulary_synonym_audit.py --check-clean
git diff --check
python3 -m json.tool var/audit/active_code_atlas_001/vocabulary_governance_surface/vocabulary_governance_active_code_atlas_records.json
```

Observed statuses:

```text
candidate_review_cli_pytest_status=0
vocabulary_governance_conformance_candidate_pytest_status=0
vocabulary_synonym_audit_clean_check_status=0
git_diff_check_status=0
surface_records_json_parse_status=0
surface_validation_json_parse_status=0
```

Observed outputs:

```text
16 passed in 11.49s
114 passed in 23.29s
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
```

Raw reports:

- `var/audit/active_code_atlas_001/vocabulary_governance_surface/reports/candidate_review_cli_pytest.stdout`
- `var/audit/active_code_atlas_001/vocabulary_governance_surface/reports/vocabulary_governance_conformance_candidate_pytest.stdout`
- `var/audit/active_code_atlas_001/vocabulary_governance_surface/reports/vocabulary_synonym_audit_clean_check.stdout`
- `var/audit/active_code_atlas_001/vocabulary_governance_surface/reports/vocabulary_surface_validation_status.txt`

## 6. Boundaries held

No source implementation file was changed.

No dependency file, VENV, original Atlas JSON, Bridge JSON, generated Atlas slice, vocabulary data file, runtime trading path, or refactor work was changed.

The structural inventory remains navigation only.

## 7. Next pointer

After this pass, the next queue row is:

```text
ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_002_TESTING_PROOF_CHECKPOINT_SURFACE
```

Queue basis: `ACATQ-0043` / `ACABC-0044`, blueprint surface `Testing, proof, and checkpoint surfaces`, required action `extend_existing_test_family_before_code`, proof tier `Tier B`.

## 8. Auditor repair follow-up — evidence-range validation

Auditor-blocking evidence range defects in this surface were repaired.

Repaired:

```text
tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py: line_end 107 -> 95
tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py: line_end 97 -> 86
```

Added/ran recurring validation:

```text
var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py
validation_status=PASS
error_count=0
warning_count=0
```

Relevant proof rerun:

```text
candidate_review_cli_pytest_status=0; 16 passed in 17.93s
vocabulary_governance_conformance_candidate_pytest_status=0; 114 passed in 39.43s
vocabulary_synonym_audit_clean_check_status=0; vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
git_diff_check_status=0
```

The all-surface primary active-code Atlas remains not accepted; this surface remains read-adjudicated only for the cited files.
