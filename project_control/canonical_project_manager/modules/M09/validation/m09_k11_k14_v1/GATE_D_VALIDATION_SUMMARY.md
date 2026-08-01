# M09 K11/K14 Gate D Validation Summary

## Disposition

`PASS:GATE_D_ACCEPTED:M09_K11_K14_CAPITAL_AUTHORITY`

## Accepted implementation

The canonical `nvda_desk.m09_capital_authority` package exposes frozen
`FinalRiskDecision`, `CapitalState`, `CapitalDeploymentDecision` and
`CapitalDeploymentReceipt` contracts plus one deterministic
`CapitalAuthorityService`.

K11 consumes exact revalidated M05 and M06 products, requires matching prepared
lineage, preserves branch evidence and fails closed on missing, contradictory,
unknown or blocked authority. K14 consumes the exact K11 result, one immutable
capital snapshot, one non-rejected M07 receipt and a closed M09 policy. It
computes fresh-capital percentage and notional only; it grants no placement,
broker, execution, position, lifecycle, durable-transaction or replay authority.

The retained C-036 final-risk path is a bounded compatibility adapter only. It
does not fabricate canonical M05/M06 lineage and does not expose confidence on
its categorical branch-join receipt.

## Independent high-consequence review

A detached C-PROOF review found and closed four numeric-domain omissions before
Gate D opened: zero available capital, negative reserved capital, percentages
above 100 and caution multipliers above 1.

A separate post-implementation boundary probe then found an upward-rounding
defect: `9.999%` could become `10.00%`, exceeding a hard/state cap. Normative law
and proof were amended before implementation acceptance. Percentage authority
now rounds down to the greatest policy-quantum multiple not exceeding the raw
bound; notional rounds down to cents; sub-quantum authority becomes `no_trade`;
and numerically equivalent decimal representations share one semantic identity.

## Environment and comparison point

- branch: `work/m09-k11-k14-capital-authority-v1`;
- source checkpoint: `330becaa99e862f40ae4066d35e21ae9788ddcae`;
- hardened proof baseline: `66f6bc4`;
- Python: `3.13.5`;
- pytest: `9.0.2`;
- successful raw output and JUnit comparison data retained outside Git under
  `/tmp` only;
- Ruff and Black: unavailable because the locked modules are not installed; no
  substitute was installed or used.

## Results

| Check | Result |
|---|---|
| Static compilation / diff check | PASS |
| Focused K11/K14 proof | PASS — 32 / 32 |
| Proof composition | 10 reference-law cases; seven named mutants; 15 production-facing cases |
| C-036 compatibility proof | PASS — 3 / 3 |
| Named proof block | PASS — 32 / 32 |
| Proof-block manifest | PASS — 61 / 61 |
| Proof-executor contract | PASS — 21 / 21 |
| Tier B admitted set | PASS — 49 / 49 |
| M09 vocabulary audit | PASS — zero unresolved candidates; 297 governed occurrences across 27 files |
| Affected exact comparison | baseline 49 passed / 32 failed; current 67 / 14; 18 resolved; zero new failing nodes |
| Non-vocabulary Tier A | baseline 1,437 passed / 268 failed; current 1,455 / 250; 18 resolved; zero new failing nodes |
| Vocabulary Tier A | baseline 100 passed / 3 failed; current 100 / 3; unchanged |
| Complete Tier A | baseline 1,537 passed / 271 failed; current 1,555 / 253; 18 resolved; zero new failing nodes |
| Deterministic boundary property probe | PASS — 400 generated clear/caution sizing cases |
| Forged-state probe | PASS — two recomputed state/notional contradictions rejected |

## Failure delta

The 18 resolved nodes are the 15 canonical M09 production-facing cases and the
three retained C-036 compatibility cases. No previously passing baseline node
fails in the candidate tree.

The remaining 253 complete Tier A failures reproduce at the hardened proof
baseline. They concern unopened or pre-existing boundaries including
caller-owned scenario/module identity, the unadmitted M04 bootstrap/capital
packet roles, M10/M11/M12 obligations and three unchanged vocabulary baseline
defects. They are not represented as accepted M09 behaviour.

All 17 vocabulary files were run in bounded groups because the combined
vocabulary-directory route has a known suite-order non-termination history.
The grouped runs cover the complete 103-node vocabulary set on both baseline and
current trees.

## Known integration limit

The current M06 evaluator truthfully returns `unknown` for concentration,
inventory and liquidity when those owner facts are unavailable. M09 proof uses a
contract-valid typed M06 assessment with complete owner evidence to prove the
K11/K14 seam. This accepts M09 owner-product consumption; it does **not** claim
that current M00 composition can yet produce an eligible end-to-end decision.
That composition remains for later integration work.

## Commands

```text
python -m compileall -q src/nvda_desk/m09_capital_authority src/nvda_desk/contracts/risk.py src/nvda_desk/domain/final_risk/terminal_join.py
PYTHONPATH=src:. python -m pytest -q tests/tier_a/m09_k11_k14/test_m09_k11_k14_contract.py
PYTHONPATH=src:. python -m pytest -q tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py -k final_risk
python scripts/run_proof_block.py --block m09_k11_k14_capital_authority_contract
python scripts/run_proof_block.py --check-all
PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py
PYTHONPATH=src python -m pytest -q tests/tier_b
PYTHONPATH=src python -m nvda_desk.vocabulary_synonym_audit --namespace m09 --check-clean
PYTHONPATH=src python -m pytest -q tests/tier_a/m09_k11_k14/test_m09_k11_k14_contract.py tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py tests/tier_a/capital_deployment
PYTHONPATH=src python -m pytest -q tests/tier_a --ignore=tests/tier_a/vocabulary
PYTHONPATH=src python -m pytest -q <all 17 vocabulary files in bounded groups>
```

## Next gate

Pause and publish the user-requested clean full-history M09 checkpoint. M10
execution-gateway authority is next and has not started.
