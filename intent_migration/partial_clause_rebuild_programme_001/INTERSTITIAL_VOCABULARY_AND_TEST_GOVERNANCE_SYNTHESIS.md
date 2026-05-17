# Interstitial vocabulary and test-governance synthesis

Status: `planning_read_synthesis_no_mutation`

## Vocabulary operating interpretation

The vocabulary system is an admission layer, not a free-form glossary. A durable term must either reuse an existing governed term, enrich an existing term, become an explicit alias, be added through the governed generator-backed path, or be quarantined.

The admission classifications are: `enrich_existing`, `add_new`, `alias_only`, `quarantine`.

The rebuild programme must therefore treat every clause title, test name, proof-block id, fixture name, receipt label, and public contract-facing assertion as vocabulary-sensitive.

## Test-tier operating interpretation

Tier placement by directory is insufficient. Tier authority comes from live doctrine, retained-test registry, proof blocks, or active bounded-pack receipts.

Proof block tier counts from `config/proof_blocks.yaml`:

{
  "Tier A": 42,
  "Tier B": 4
}

Retained-test registry summary:

- Tier A families listed in native tree: 30
- retained seed Tier A entries: 117
- Tier B disposition entries: 41

## Vocabulary test family inventory

- `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py`
- `tests/tier_a/vocabulary/test_financial_calendar_vocabulary_terms.py`
- `tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_plan_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_admission_review_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_classification_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_payload_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_candidate_schema_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`
- `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py`
- `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py`
- `tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py`
- `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py`
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`
- `tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py`

## Planning consequence

Before any owner-service implementation leaf writes tests or code, it must classify durable terms and decide whether the existing vocabulary proof blocks are sufficient or whether a bounded vocabulary/admission leaf is required first.
