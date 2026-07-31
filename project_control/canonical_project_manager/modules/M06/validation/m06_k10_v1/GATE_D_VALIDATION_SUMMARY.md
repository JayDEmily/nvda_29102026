# M06 K10 Gate D Validation Summary

## Disposition

`PASS:GATE_D_ACCEPTED:M06_K10_PARALLEL_RISK_AUTHORITY`

## Accepted implementation

The canonical `nvda_desk.m06_parallel_risk` public seam contains frozen
`ParallelRiskInput`, `ParallelRiskObservation` and `ParallelRiskAssessment`
contracts plus one deterministic, side-effect-free `ParallelRiskEvaluator`. The
input projects exact revalidated M03 prepared authority, optional admitted M04
packet lineage and explicit M07-owned VIX threshold references. The assessment
preserves six admitted environmental-risk families, explicit unknown/degraded
evidence, block-dominant deterministic aggregation and closed K11/capital/
execution/lifecycle authority. The retained lane-service compatibility surface
now keeps policy-decision state instance-local rather than module-global.

## Environment and comparison point

- branch: `work/gate-c-evidence-economy-m03-continuation-v1`;
- C-PROOF baseline: `af51af9203eb3d586aa398ab2f3eac11dc9af54c`;
- Python: `3.13.5`;
- pytest: `9.0.2`;
- successful raw output retained outside the tracked tree under `/tmp` only;
- Ruff and Black: unavailable because the locked modules are not installed; no
  substitute was installed or used.

## Results

| Check | Result |
|---|---|
| Static compilation | PASS |
| Focused K10 proof | PASS — 30 / 30 |
| Former expected-red public seam | PASS — 7 / 7 |
| Added Gate D integrity cases | PASS — 10 added cases |
| Retained compatibility-state repair | PASS — two module-global state failures resolved |
| Affected exact comparison | baseline 99 passed / 34 failed; current 117 / 26; zero new failing nodes, eight resolved, ten added passing cases |
| Tier A comparison | baseline 1,489 passed / 265 failed; current 1,508 / 256; zero new failing nodes, nine resolved, ten added passing cases |
| M06 vocabulary audit | PASS — zero unresolved candidates; 145 governed occurrences |
| Named proof block | PASS — 30 / 30 |
| Proof-block manifest | PASS — named block and 60 / 60 total manifests |
| Proof-executor contract | PASS — 21 / 21 |
| Tier B admitted set | PASS — 49 / 49 in two explicit partitions |
| Vocabulary namespace parity | PASS — 4 / 4 |

## Affected-route classification

The affected comparison resolves exactly the seven admitted M06 production-facing
failures and the C-020/C-035 module-global state defect. The full Tier A
comparison also resolves the second retained gateway-service test exercising the
same instance-local state repair, for nine resolved nodes in total. The remaining
256 Tier A failures reproduce at the C-PROOF baseline and concern unopened or
pre-existing boundaries, including the unadmitted legacy bootstrap packet role,
caller-owned scenario identity, orchestration composition, observation-store
packet identity and three unchanged vocabulary baseline defects. They are not
represented as accepted M06 behaviour.

The all-vocabulary-directory command did not terminate after partial progress.
Every vocabulary test file was therefore run independently in both baseline and
current trees. Together with the non-vocabulary partition, this executed the
complete admitted Tier A set: 1,754 tests at baseline and 1,764 currently.

## Commands

```text
python -m compileall -q <M06 source and proof files>
PYTHONPATH=src:. python -m pytest -q tests/tier_a/m06_k10/test_m06_k10_contract.py
PYTHONPATH=src:. python scripts/run_proof_block.py --block m06_k10_parallel_risk_contract
PYTHONPATH=src:. python scripts/run_proof_block.py --check-all
PYTHONPATH=src:. python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py
PYTHONPATH=src:. python -m pytest -q tests/tier_b --ignore=tests/tier_b/proof_model/test_proof_executor_contract.py
PYTHONPATH=src:. python -m pytest -q tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
PYTHONPATH=src python -m nvda_desk.vocabulary_synonym_audit --namespace m06 --check-clean
PYTHONPATH=src:. python -m pytest -q --tb=no <affected M06/compatibility test set>
PYTHONPATH=src:. python -m pytest -q --tb=no tests/tier_a --ignore=tests/tier_a/vocabulary
PYTHONPATH=src:. python -m pytest -q --tb=no tests/tier_a/vocabulary
```

## Next gate

Pause at the user-requested M06 checkpoint. On resumption, the next lawful unit
is M09 K11/capital authority; M10 execution and M11 lifecycle mutation remain
closed.
