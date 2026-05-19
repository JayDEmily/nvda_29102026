# FWD-004 test-first receipt

Targeted row-proof test added: `tests/tier_a/packets/test_fwd004_reopened_row_packet_carriage_proof.py`.

Scope: the 59 reopened `unsupported_worker_claim` rows from `var/audit/non310_completion_claim_audit_20260519/FWD004_ROW_AUDIT.csv`.

The test is not a registry-presence check. It parametrises every reopened row and asserts native packet-carriage or review-packet-service behaviour through live source surfaces.

Proof run before ledger closeout:

```
env PYTHONPATH=src python3 -m pytest tests/tier_a/packets/test_fwd004_reopened_row_packet_carriage_proof.py
```

Observed result: `59 passed`, status file `0`, captured under `var/audit/fwd004_target_surface_repair_20260519/reports/test_first_reopened_rows.*`.
