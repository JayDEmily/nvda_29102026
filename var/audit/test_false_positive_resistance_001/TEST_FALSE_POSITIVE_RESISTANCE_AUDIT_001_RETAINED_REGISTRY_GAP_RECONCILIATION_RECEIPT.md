# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_RETAINED_REGISTRY_GAP_RECONCILIATION_RECEIPT

Date: 2026-05-10

## Scope

Resolve the retained-registry truth gap left by Tier A proof-block coverage reconciliation.

This receipt is limited to test authority/proof-surface reconciliation. It does not claim runtime correctness, full false-positive resistance for every test, or full-suite reliability.

## Controlling authority read

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

## Files read for the three retained-registry gaps

- `tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py` — 106 lines
- `tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py` — 71 lines
- `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py` — 95 lines
- `src/nvda_desk/contracts/upstream_signal.py` — 79 lines
- `src/nvda_desk/upstream/raw_signal_ingress.py` — 79 lines
- `src/nvda_desk/upstream/raw_signal_coverage.py` — 41 lines
- `src/nvda_desk/contracts/dataset_packets.py` — 41 lines
- `src/nvda_desk/schemas/vocabulary.py` — 718 lines
- `scripts/build_canonical_vocabulary.py` — 28 lines
- `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py` — 86 lines

## Changes made

- Added `tests/tier_a/upstream_signal/` to the retained-test native Tier A tree.
- Reconciled `upstream_non_interference_and_sanity_traces` from deferred/no-native-test status to explicit retained Tier A native test status.
- Reconciled `upstream_signal_coverage_map_and_scope_lock` from deferred/no-native-test status to explicit retained Tier A native test status.
- Added explicit retained Tier A registry entry for `vocabulary_document_json_helpers`.
- Rebuilt `tier_a_registry_reconciliation_inventory` to reflect 95 physical Tier A pytest files.
- Did not change runtime source, canonical vocabulary data, dependencies, VENV, `black`, or `ruff`.

## Post-state evidence

### Registry/proof-block coverage

Artefact: `var/audit/test_false_positive_resistance_001/retained_registry_gap_reconciliation/tier_a_registry_reconciliation_summary_final.json`

Observed summary:

```json
{
  "covered_by_command_or_owns_count": 95,
  "covered_by_proof_block_command_count": 95,
  "covered_by_proof_block_owns_count": 84,
  "in_retained_registry_count": 95,
  "not_in_proof_block_command": [],
  "not_in_proof_block_command_or_owns": [],
  "not_in_retained_registry": [],
  "proof_block_count": 17,
  "tier_a_pytest_file_count": 95
}
```

### Targeted retained-registry gap pytest

Command:

```bash
PYTHONPATH=src python -m pytest \
  tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py \
  tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py \
  tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py
```

Result: `12 passed`, status `0`.

Log: `var/audit/test_false_positive_resistance_001/retained_registry_gap_reconciliation/registry_gap_targeted_pytest.log`

### Proof blocks rerun

- `support_spine_prepared_packet_review_surface`: `33 passed`, status `0`.
- `vocabulary_governance_conformance_candidate`: `113 passed`, status `0`.
- `tier_a_remaining_coverage_inventory`: `50 passed`, status `0`.
- `proof_blocks --check-all`: `proof_blocks_check_all=PASS count=17`, status `0`.

Logs and status files are stored under:

`var/audit/test_false_positive_resistance_001/retained_registry_gap_reconciliation/`

### Vocabulary clean check

Command:

```bash
PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean
```

Result: `vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False`, status `0`.

### Segmented pytest baseline

One-shot full pytest was attempted but timed out in the sandbox before completion; it is not claimed as passed.

Segmented evidence:

- `tests/tier_a`: `383 passed`, status `0`.
- `tests/tier_b/proof_model/test_proof_executor_contract.py`: `19 passed`, status `0`.
- `tests/tier_b/options_flow_support`: `2 passed`, status `0`.
- `tests/tier_b/review_lineage`: `9 passed`, status `0`.
- `tests/tier_b/review_replay`: `3 passed`, status `0`.
- `tests/tier_b/serial_boundaries`: `7 passed`, status `0`.
- `tests/tier_b/upstream_support`: `2 passed`, status `0`.
- `tests/tier_c`: no tests collected; pytest exit code `5`, expected for an empty Tier C directory, not a failing test assertion.

Segmented total excluding empty Tier C: `425 passed`.

Summary artefact: `var/audit/test_false_positive_resistance_001/retained_registry_gap_reconciliation/segmented_full_pytest_summary.json`

## Known true

- The prior retained-registry gap of two upstream-signal Tier A files and one vocabulary JSON-helper Tier A file is resolved.
- All 95 physical Tier A pytest files are now present in proof-block command coverage.
- All 95 physical Tier A pytest files are now recorded in the retained registry surface.
- `proof_blocks --check-all` passes with 17 proof blocks.
- Tier A segmented pytest passes with `383 passed`.
- Tier B segmented pytest passes with `42 passed` across its six active sub-surfaces.
- Vocabulary synonym clean check passes with zero candidates.

## Ruled out

- No runtime trading behaviour was changed.
- No canonical vocabulary data was changed.
- No VENV was created.
- `black` and `ruff` were not run.
- A one-shot full pytest pass is not claimed.
- Full false-positive resistance for every test is not claimed.

## Next gate

Proceed to `TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_TIER_A_REMAINING_ASSERTION_STRENGTH_AUDIT`, selecting the next Tier A proof-block family whose assertions have not yet been independently audited against the new false-positive-resistance method.
