# FWD-001 Boundary Receipt

Date: 2026-05-14
Branch: `worker/fwd-001-vocabulary-governance-blocker-resolution`

## Outcome

The reproduced synonym-candidate blocker is resolved in the current checkout.

```text
python scripts/vocabulary_synonym_audit.py --check-clean
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
EXIT:0
```

Before repair, the substantive baseline audit produced `unresolved_candidates=17`. After repair, the exact audit command produces `candidates=0`.

## Candidate decision summary

- Reproduced candidates: 17.
- Candidate entries adjudicated: 17.
- Decision: `REJECTED_WITH_EVIDENCE` for all 17.
- New aliases admitted: 0.
- New canonical terms admitted: 0.
- Remaining candidate blocker: none observed in the current audit report.

Adjudication artefact: `FWD001_VOCABULARY_SYNONYM_CANDIDATE_ADJUDICATION.md`.

## Current proof evidence

| Command | Result | Evidence file |
|---|---|---|
| `python scripts/vocabulary_synonym_audit.py --check-clean` | `EXIT:0`, `candidates=0` | `reports/exact_vocabulary_synonym_audit_clean_check.stdout` |
| `PYTHONPATH=src python -m pytest tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py -q` | `47 passed`, `EXIT:0` | `reports/targeted_synonym_candidate_audit_pytest.stdout` |
| `PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_synonym_audit_clean_check` | `EXIT:0` | `reports/vocabulary_synonym_audit_clean_check.stdout` |
| `PYTHONPATH=src python scripts/run_proof_block.py --block vocabulary_governance_conformance_candidate` | `117 passed`, `EXIT:0` | `reports/vocabulary_governance_conformance_candidate.stdout` |
| `python scripts/run_proof_block.py --check-all` | `proof_blocks_check_all=PASS count=46`, `EXIT:0` | `reports/proof_block_check_all.stdout` |
| `PYTHONPATH=src python -m pytest -q tests/tier_a` | `590 passed`, `EXIT:0` | `reports/tier_a_pytest_q.stdout` |
| `PYTHONPATH=src python -m pytest -q tests/tier_b` | `48 passed`, `EXIT:0` | `reports/tier_b_pytest_q.stdout` |
| `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` | `638 passed`, `EXIT:0` | `reports/tier_a_tier_b_pytest_q.stdout` |
| `git diff --check` | `EXIT:0` | `reports/git_diff_check.stdout` |

## Known true

- The exact vocabulary synonym audit command now runs without `PYTHONPATH` and reports zero candidates.
- The FWD-001 candidate suppression is exact-path and exact-fragment bounded.
- The same phrases still escalate outside the adjudicated paths.
- Tier A, Tier B, and combined Tier A/Tier B passed after the final pytest path-order repair.

## Ruled out

- No vocabulary alias admission was needed for the 17 reproduced candidates.
- No canonical vocabulary term addition was needed for the 17 reproduced candidates.
- The remaining blocker was not semantic after the wrapper/import and proof-runner path issues were corrected.

## Next gate

FWD-001 can move to `bounded_closed_current` for this worker package. The next planned row is `FWD-002`.

## Caveat

The read-status manifest distinguishes full reads from sectional current-evidence reads. It does not claim every large planning/control file was fully re-read in this worker pass.
