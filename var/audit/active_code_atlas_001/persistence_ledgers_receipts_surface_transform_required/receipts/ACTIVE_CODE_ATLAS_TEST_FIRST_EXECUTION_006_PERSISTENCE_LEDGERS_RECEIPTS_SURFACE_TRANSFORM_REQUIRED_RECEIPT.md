# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_006_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE_TRANSFORM_REQUIRED_RECEIPT

## Scope

Target: `ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_006_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE_TRANSFORM_REQUIRED`

Queue row: `ACATQ-0039`

Comparison row: `ACABC-0040`

Architecture row: `5.16 Persistence, ledgers, and receipts`

Required action: `write_new_test_family_before_code`

Proof tier: `Tier A`

## Authority read for this pass

The pass continued from the live `PLANS.md` / `ROADMAP_LEDGER.md` pointer after commit `adb43f4` and stayed inside the current 5.16 surface. The governing 5.16 law remained:

- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`: duplicate durable truth identifiers must be rejected; append-only/readback copy boundaries remain mandatory.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`: row 5.16 owns persistence, ledgers, receipts, repository read models, audit records, and replayable durable boundaries.

## New test-first blocker

Added: `tests/tier_a/persistence/test_module_registry_repository_surface.py`

The new blocker requires:

- empty `module_id` rejection;
- duplicate `module_id` rejection;
- copy-safe readback;
- no promotion-service writer surface on the repository.

## Pre-repair failure

```bash
PYTHONPATH=src python -m pytest -q tests/tier_a/persistence/test_module_registry_repository_surface.py
```

Observed result before source repair: `1 failed, 2 passed`.

Failure reason: `ModuleRegistryRepository.write_record("", ...)` did not raise `ValueError` and the original implementation also silently overwrote duplicate `module_id` records.

## Bounded source repair

Changed only: `src/nvda_desk/repositories/module_registry.py`

Repair:

- normalise `module_id` with `str(module_id).strip()`;
- reject empty `module_id`;
- reject duplicate `module_id` before writing;
- retain deep-copy write/read behaviour.

No other `src/` files were changed.

## Registry/proof admission

- Added proof block: `module_registry_repository_surface`.
- Added retained Tier A family: `module_registry_repository_surface`.
- Updated Tier A registry inventory count from `96` to `97`.
- Updated the wider `persistence_ledgers_receipts_surface` proof block ownership to include the module registry repository and test.

## Post-repair validation commands

```bash
PYTHONPATH=src python -m pytest tests/tier_a/persistence/test_module_registry_repository_surface.py -q
```

Observed result: `3 passed in 0.42s`.

```bash
PYTHONPATH=src python scripts/run_proof_block.py --block module_registry_repository_surface
```

Observed result: `3 passed in 0.45s`; `proof_block_id=module_registry_repository_surface`.

```bash
PYTHONPATH=src python scripts/run_proof_block.py --block persistence_ledgers_receipts_surface
```

Observed result: `34 passed in 1.17s`; `proof_block_id=persistence_ledgers_receipts_surface`.

```bash
PYTHONPATH=src python scripts/run_proof_block.py --check-all
```

Observed result: `proof_blocks_check_all=PASS count=21`.

```bash
PYTHONPATH=src python var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py
```

Observed result: `validation_status=PASS`, `error_count=0`, `warning_count=0`; Tier A declared/entry count `97`; Tier B declared/entry count `12`.

## Boundary statement

This pass does not admit donor `PromotionService`, imported-module schemas, broad module schema APIs, downstream placement policy, or any runtime trading behaviour. It only hardens the active module-registry persistence seam against duplicate durable truth.

## Scope exhaustion note

The next queue row after this pass is `ACATQ-0017` / `ACABC-0017`, `DMPV3 packet carriage`. That leaves the current bounded 5.16 persistence/ledgers/receipts surface requested by the user.

```bash
git diff --check
```

Observed result: exit `0`, no output.
