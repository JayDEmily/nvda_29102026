# M10 K15 Gate D Validation Summary

## Disposition

`PASS:GATE_D_ACCEPTED:M10_K15_EXECUTION_GATEWAY`

## Accepted boundary

M10 consumes one exact positive M09 capital-deployment receipt and explicit paper-only limit facts, forms a downward-rounded NVDA buy intent, submits it through a provider-substitutable offline paper port, and atomically records one acknowledgement plus one exact full-fill event using M13 non-durable transaction/idempotency mechanics. The terminal execution receipt binds the exact intent, events, port and transaction facts.

M10 does not establish live broker connectivity, network submission, market-price discovery, position/inventory mutation, M11 lifecycle authority, durable commit or production trading readiness.

## Commands and results

| Surface | Result |
|---|---:|
| `PYTHONPATH=src pytest -q tests/tier_a/m10_k15/test_m10_k15_contract.py` | 28 passed |
| M10 legacy compatibility surfaces | 5 passed |
| `python scripts/run_proof_block.py --check-all` | 62/62 manifests valid |
| proof-executor contract | 21 passed |
| `PYTHONPATH=src pytest -q tests/tier_b` | 49 passed |
| vocabulary canonical-builder parity | 4 passed |
| M10 vocabulary audit | zero unresolved; 16 files; 111 governed occurrences |
| complete Tier A baseline | 1,568 passed / 264 failed |
| complete Tier A current | 1,583 passed / 253 failed |
| failure-node delta | 11 resolved; zero new |
| static compilation / diff check | passed |
| Ruff / Black | unavailable; locked modules not installed |

The complete Tier A comparison used the non-vocabulary tree plus the vocabulary partition because the aggregate vocabulary route has a known suite-order non-termination history. Baseline and current vocabulary totals were both 100 passed / three unchanged failures. The remaining 253 Tier A failures are outside the admitted M10 write set and reproduce at hardened proof baseline `236a8aeaf88303b4cc5e783d069c73cc129bb4b8`.
