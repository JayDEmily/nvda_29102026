# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 — Tier A coverage reconciliation receipt

## Scope

Reconcile the physical Tier A pytest tree against `config/proof_blocks.yaml` command/ownership coverage after the selected proof-block rollup passed.

## Inputs read

- `AGENTS.md` — full file read earlier in this pass
- `PLANS.md` — full file read earlier in this pass
- `ROADMAP_LEDGER.md` — full file read earlier in this pass
- `tests/README.md` and `tests/tier_a/README.md` — full files read
- `config/proof_blocks.yaml` — full file read
- `config/retained_test_registry.yaml` — full file read into the reconciliation pass
- 27 physical Tier A pytest files not covered by any proof-block command/owns path before this reconciliation — full files read
- 2 upstream signal Tier A pytest files missing from retained registry but already covered by an existing proof-block command — full files read

## Pre-reconciliation inventory

```text
tier_a_pytest_file_count=95
covered_by_proof_block_command_count=68
covered_by_proof_block_owns_count=57
covered_by_command_or_owns_count=68
in_retained_registry_count=92
not_in_proof_block_command_or_owns_count=27
not_in_retained_registry_count=3
```

Pre-reconciliation inventory artefacts:

- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_summary.json`
- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_rows.json`
- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_rows.tsv`

## Change made

Added one explicit proof-block inventory surface to `config/proof_blocks.yaml`:

```text
proof_block_id=tier_a_remaining_coverage_inventory
tier=Tier A
lifecycle=admitted_for_test_false_positive_resistance_tier_a_coverage_reconciliation
```

This block covers the 27 physical Tier A pytest files that were not previously run or owned by any proof block.

## Proof commands

```text
PYTHONPATH=src python -m pytest <27 previously-uncovered Tier A files>
status=0
50 passed in 0.80s
```

```text
PYTHONPATH=src python scripts/run_proof_block.py --check-all
status=0
proof_blocks_check_all=PASS count=17
```

```text
PYTHONPATH=src python scripts/run_proof_block.py --block tier_a_remaining_coverage_inventory
status=0
50 passed in 0.79s
```

```text
PYTHONPATH=src python scripts/vocabulary_synonym_audit.py --check-clean
status=0
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
```

```text
PYTHONPATH=src python scripts/run_proof_block.py --block proof_executor_contract
status=0
19 passed in 18.01s
```

## Post-reconciliation inventory

```text
tier_a_pytest_file_count=95
proof_block_count=17
covered_by_proof_block_command_count=95
covered_by_command_or_owns_count=95
in_retained_registry_count=92
not_in_proof_block_command_or_owns_count=0
not_in_retained_registry_count=3
```

Post-reconciliation inventory artefacts:

- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_summary_after_remaining_inventory.json`
- `var/audit/test_false_positive_resistance_001/tier_a_coverage_reconciliation/tier_a_proof_block_coverage_rows_after_remaining_inventory.json`

## Remaining gap

The following physical Tier A tests remain absent from `config/retained_test_registry.yaml`:

- `tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py`
- `tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py`
- `tests/tier_a/vocabulary/test_vocabulary_document_json_helpers.py`

This receipt does not silently admit them into the retained registry. It records that current proof-block command coverage now reaches them, and routes the retained-registry truth gap to the next gate.

## Claim boundary

Known true:

- All 95 physical Tier A pytest files are now covered by at least one `config/proof_blocks.yaml` command path.
- The new inventory proof block passes locally.
- Manifest validation passes with 17 proof blocks.
- Vocabulary synonym clean-check remains clean after the manifest update.

Ruled out:

- This is not a false-positive-resistance trust claim for all 95 files.
- This is not a full-suite reliability claim.
- This does not resolve retained-registry truth for the three missing paths.
- This does not change runtime source, dependencies, VENV, `black`, or `ruff`.

Next gate:

`TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_RETAINED_REGISTRY_GAP_RECONCILIATION`

Purpose: resolve the three retained-registry gaps by reading the governing source/docstring surfaces and either admitting them truthfully into the registry or routing them to quarantine/removal if authority does not support them.
