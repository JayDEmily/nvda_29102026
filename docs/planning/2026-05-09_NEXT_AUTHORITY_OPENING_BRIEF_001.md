# NEXT_AUTHORITY_OPENING_BRIEF_001

Date: 2026-05-09
Type: authority decision brief

## Recommended next opening

Open **I1 — `roadmap_live_position_and_inventory_architecture` / row `5.13 Live position and inventory architecture`**.

## Why this is the recommended next path

This is the cleanest next authority seam because it strengthens durable state truth before capital deployment, risk weighting, opening placement, and exit/close behaviour.

Blueprint row `5.13` defines the target as live position, inventory, exposure, and capital-state read/write structure after entry. It allows execution receipts, fill/state updates, capital state, position repository state, and risk limits as inputs; it emits live inventory snapshots, position state, exposure state, and capital/inventory receipts. It explicitly prohibits new candidate formation, raw signal preparation, direct broker placement decisions, and ungoverned capital mutation.

## Exact authority phrase to use if opening it

```text
Open row 5.13 live position and inventory architecture for bounded read/write state and repository invariant hardening. Do not open broker placement, new candidate formation, raw signal preparation, or ungoverned capital mutation.
```

## First implementation gate if opened

Gate: authority intake and baseline invariant proof for live position/inventory state.

Pass condition:

1. `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, blueprint row `5.13`, runtime ownership docs, and the I1 read-set files are read before mutation.
2. Existing inventory/repository tests are run and logged before mutation.
3. The branch declares touched/read-only/prohibited files before changing source/tests.
4. No broker adapter, order placement, candidate formation, raw-source preparation, or ungoverned capital mutation boundary is opened.

## Likely touched files if opened

- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `src/nvda_desk/domain/downstream/live_inventory.py`
- `src/nvda_desk/downstream/live_inventory.py`
- `src/nvda_desk/repositories/position_repository.py`
- `src/nvda_desk/repositories/capital_state_repository.py`
- `src/nvda_desk/contracts/downstream.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/persistence/test_position_repository_surface.py`
- `tests/tier_a/persistence/test_capital_state_repository_surface.py`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- `Makefile`
- `ROADMAP_LEDGER.md`
- `var/audit/roadmap_live_inventory_5_13/*`

## Explicitly prohibited if opened

- broker placement or order execution;
- new candidate formation;
- raw signal preparation;
- ungoverned capital mutation;
- dependency changes;
- original Atlas/Bridge JSON mutation;
- generated Atlas slice mutation;
- historical receipt mutation.

## Proof target if opened

The likely named proof block should be:

```text
live_position_inventory_architecture_surface
```

Minimum proof family:

- repository tests;
- fill-feedback tests;
- position-state invariant tests;
- capital-state consistency tests;
- no broker-placement authority test;
- proof-block check-all receipt;
- full or broad targeted suite if the branch touches shared contracts/repositories.

## Stop condition

Without the exact authority phrase or equivalent explicit user instruction, implementation must not start.
