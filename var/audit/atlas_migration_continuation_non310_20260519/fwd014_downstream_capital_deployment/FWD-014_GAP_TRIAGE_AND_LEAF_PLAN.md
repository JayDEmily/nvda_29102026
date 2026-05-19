# FWD-014 — Downstream capital deployment authority gap triage and leaf plan

Selected records: 2. Ledger rows: 2. Status counts: `{'implemented_in_tests_and_code': 2}`.

No `test_only`, `code_only`, `evidence_only_not_implemented`, `deferred_by_authority`, or `rejected_out_of_scope` rows were emitted. No source/test/config/fixture/vocabulary/Atlas/generated-slice mutation is proposed.

Proof to run: manifest validation, targeted pytest `['tests/tier_a/capital_deployment', 'tests/tier_b/capital_deployment/test_capital_deployment_transform_boundary_surface.py']`, `python3 scripts/run_proof_block.py --check-all`, `git diff --check`.
