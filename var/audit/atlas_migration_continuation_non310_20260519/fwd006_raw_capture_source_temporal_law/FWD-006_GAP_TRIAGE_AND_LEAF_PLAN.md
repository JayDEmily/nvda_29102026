# FWD-006 — Raw capture and source temporal law gap triage and leaf plan

Selected records: 108. Ledger rows: 108. Status counts: `{'duplicate_or_subsumed': 108}`.

No `test_only`, `code_only`, `evidence_only_not_implemented`, `deferred_by_authority`, or `rejected_out_of_scope` rows were emitted. No source/test/config/fixture/vocabulary/Atlas/generated-slice mutation is proposed.

Proof to run: manifest validation, targeted pytest `['tests/tier_a/ingress/test_raw_bundle_loader_surface.py', 'tests/tier_a/temporal']`, `python3 scripts/run_proof_block.py --check-all`, `git diff --check`.
