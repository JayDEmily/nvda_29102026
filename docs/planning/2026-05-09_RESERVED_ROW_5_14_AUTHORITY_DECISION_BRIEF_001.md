# RESERVED_ROW_5_14_AUTHORITY_DECISION_BRIEF_001

Date: 2026-05-09
Type: reserved-row authority decision brief

## Recommended next opening

Prepare, but do not yet implement, **row `5.14 Exit and close architecture`**.

## Why this row is next

Blueprint row `5.14` is downstream of live position/inventory state, playbook policy, risk context, market state, and broker/execution constraints. Row `5.10` now has bounded playbook registry and metadata-receipt proof, so the next unresolved reserved row is exit/close. The opening must still be bounded because row `5.14` remains reserved in the blueprint.

## Exact authority phrase to open row 5.14

```text
Open row 5.14 exit and close architecture for bounded exit-policy contracts, close-handoff metadata, exit receipts, and position-closure replay proof. Do not open broker order execution, live order placement, capital deployment sizing, initial candidate formation, source-ingress authority, hidden live-inventory mutation, dependency changes, Atlas/Bridge JSON mutation, generated Atlas slice mutation, or historical receipt mutation.
```

## First gate if opened

Gate: authority intake and baseline exit/close-surface proof.

Pass condition:

1. Read `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, blueprint row `5.14`, process/tranche law, testing/promotion law, vocabulary governance, runtime ownership docs, proof blocks, retained-test registry, Makefile, and current downstream/opening/live-inventory/playbook source/tests before mutation.
2. Declare touched/read-only/prohibited files before source or test changes.
3. Run baseline downstream/opening/live-inventory/playbook/proof-block checks before mutation.
4. Keep broker order execution, live placement, capital deployment sizing, initial candidate formation, source-ingress authority, dependency changes, Atlas/Bridge JSON, generated Atlas slices, and historical receipts closed.

## Candidate read set if opened

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- `Makefile`
- `ROADMAP_LEDGER.md`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/downstream/opening.py`
- `src/nvda_desk/downstream/live_inventory.py`
- `src/nvda_desk/contracts/playbook.py`
- `src/nvda_desk/contracts/capital.py`
- `tests/tier_a/downstream_runtime/`
- `tests/tier_a/playbook/`
- `tests/tier_a/capital_deployment/`

## Expected proof family if opened

- exit-policy contract tests;
- close-handoff metadata tests;
- exit receipt tests;
- position-closure replay tests;
- no broker execution tests;
- no capital sizing tests;
- no initial candidate formation tests;
- no hidden live-inventory mutation tests;
- vocabulary synonym audit clean-check;
- proof-block manifest check-all;
- targeted proof block for row `5.14` if admitted.

## Stop condition

Do not implement row `5.14` without the exact authority phrase above or equivalent explicit user instruction.
