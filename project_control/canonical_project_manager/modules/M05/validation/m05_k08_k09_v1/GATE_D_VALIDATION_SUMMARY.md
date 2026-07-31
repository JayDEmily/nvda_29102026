# M05 K08/K09 Gate D Validation Summary

## Disposition

`PASS:GATE_D_ACCEPTED:M05_K08_K09_SERIAL_COGNITION_AUTHORITY`

## Accepted implementation

The canonical `nvda_desk.m05_serial_cognition` public seam contains frozen
`StageContext`, `StageInput`, `StageOutput` and `SerialCandidate` contracts plus
a deterministic `SerialRunner`. The candidate binds one prepared context,
owner-issued bounded carrier facts, exact input/output/dependency lineage, the
six governed serial stages, M07 modifier and M08 eligibility authority, and
formed or explicit terminal results without importing M06 parallel-risk,
capital, broker, position, lifecycle-mutation, transaction or replay authority.

## Environment and comparison point

- branch: `work/gate-c-evidence-economy-m03-continuation-v1`;
- C-PROOF baseline: `a5404645a4fa2e04f6bd5cdb80a86ecdeeec22d4`;
- Python: `3.13.5`;
- pytest: `9.0.2`;
- successful raw output retained outside the tracked tree under `/tmp` only;
- Ruff and Black: unavailable because the locked modules are not installed; no
  substitute was installed or used.

## Results

| Check | Result |
|---|---|
| Static compilation | PASS |
| Focused K08/K09 proof | PASS — 32 / 32 |
| Former expected-red public seam | PASS — 7 / 7 |
| Added Gate D integrity cases | PASS — 12 added cases |
| Affected exact comparison | baseline 36 passed / 146 failed; current 55 / 139; zero new failing nodes, seven resolved, 12 added passing cases |
| Tier A comparison | baseline 1,457 passed / 265 failed; current 1,476 / 258; zero new failing nodes, seven resolved, 12 added passing cases |
| M05 vocabulary audit | PASS — zero unresolved candidates; 81 governed occurrences |
| Named proof block | PASS — 32 / 32 |
| Proof-block manifest | PASS — named block and 59 / 59 total manifests |
| Proof-executor contract | PASS — 21 / 21 |
| Tier B admitted set | PASS — 49 / 49 in two partitions; combined command did not terminate after partial progress |
| Vocabulary namespace parity | PASS — 4 / 4 |

## Aggregate-route note

The complete admitted Tier A set was run in two explicit partitions: all Tier A
tests excluding `tests/tier_a/vocabulary`, then the vocabulary directory. The
baseline collected 1,722 tests and the current tree collected 1,734 tests. The
seven resolved nodes are exactly the admitted M05 production-facing failures;
no new failing nodes exist. The remaining 258 Tier A failures are unchanged
outside this M05 slice.

The combined Tier B route completed 13 tests and then did not terminate within
the bounded run. The same 49-test admitted set was therefore executed as the
21-test proof-executor contract plus the remaining 28 Tier B tests. Both
partitions passed. This is recorded as a suite-order/non-termination warning,
not represented as a successful combined command.

## Commands

```text
python -m compileall -q <M05 source and proof files>
PYTHONPATH=src:. python -m pytest -q tests/tier_a/m05_k08_k09/test_m05_k08_k09_contract.py
python scripts/run_proof_block.py --block m05_k08_k09_serial_cognition_contract
python scripts/run_proof_block.py --check-all
PYTHONPATH=src:. python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py
PYTHONPATH=src:. python -m pytest -q tests/tier_b --ignore=tests/tier_b/proof_model/test_proof_executor_contract.py
PYTHONPATH=src:. python -m pytest -q tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
PYTHONPATH=src python -m nvda_desk.vocabulary_synonym_audit --namespace m05 --check-clean
PYTHONPATH=src:. python -m pytest -q --tb=no <affected M05/compatibility test set>
PYTHONPATH=src:. python -m pytest -q --tb=no tests/tier_a --ignore=tests/tier_a/vocabulary
PYTHONPATH=src:. python -m pytest -q --tb=no tests/tier_a/vocabulary
```

## Next gate

Pause at the user-requested M05 checkpoint. On resumption, the next lawful unit
is M06 parallel-risk `C-NORM`; M09 capital and downstream execution/lifecycle
authority remain closed.
