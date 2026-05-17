# FWD-007/008/010/013 implementation receipt

## Scope

| Forward leaf | Owner surface | Clause rows | Native implementation summary |
|---|---|---:|---|
| FWD-007 | Raw signal families | 56 | Trace-only market substrate contracts and strategic-ladder observation validation without execution authority. |
| FWD-008 | Financial and event calendar architecture | 11 | Runtime event proximity query snapshot over the operational calendar repository, context-only. |
| FWD-010 | Dynamic coefficient and modifier authority | 12 | Bounded coefficient calibration proposal, audit packet, and replay fixture pack without live coefficient mutation. |
| FWD-013 | Parallel risk lane | 8 | Candidate semantic enrichment, fragility dimensions, and risk-policy observation records without capital sizing or arbitration authority. |
| **Total** |  | **87** |  |

## Changed implementation surfaces

- `src/nvda_desk/contracts/market_substrate.py`
- `src/nvda_desk/upstream/market_substrate.py`
- `src/nvda_desk/contracts/strategic_ladder.py`
- `src/nvda_desk/upstream/strategic_ladder.py`
- `src/nvda_desk/calendar/operational/events.py`
- `src/nvda_desk/contracts/modifiers.py`
- `src/nvda_desk/config/coefficient_authority.py`
- `src/nvda_desk/contracts/parallel_risk.py`
- `src/nvda_desk/domain/parallel_risk/candidate_audit.py`
- `src/nvda_desk/risk/parallel/evaluate.py`
- `src/nvda_desk/services/parallel_risk_lane_service.py`
- `src/nvda_desk/api/deps.py`
- `src/nvda_desk/api/app.py`
- `config/proof_blocks.yaml`

## Changed test surfaces

- `tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py`
- `tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py`
- `tests/tier_a/config/test_fwd010_coefficient_calibration_contract.py`
- `tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py`

## Evidence

- Clause closeout: `FWD_007_008_010_013_CLAUSE_CLOSEOUT_87.csv`
- Read/touch manifest: `FWD_007_008_010_013_READ_AND_TOUCH_MANIFEST.csv`
- Test-first receipt: `FWD_007_008_010_013_TEST_FIRST_FAILURE_RECEIPT.md`
- Proof summary: `FWD_007_008_010_013_PROOF_SUMMARY.md`
- Proof outputs: `proof/`

## Boundary notes

- No broker execution authority was added.
- No capital sizing authority was added to calendar or parallel-risk candidate surfaces.
- No live coefficient mutation authority was added.
- API additions expose bounded native mechanisms only; they do not introduce a broad donor-era endpoint catalogue.

## Next gate

Next owner-service leaf: `FWD-015 — Opening architecture and placement readiness`.

FWD-015 is not opened or implemented by this receipt.
