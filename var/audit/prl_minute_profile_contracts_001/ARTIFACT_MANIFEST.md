# Artefact manifest — PRL minute profile contracts 001

Branch: `work/prl-minute-profile-contracts`

## Governance and planning artefacts

- `ROADMAP_LEDGER.md`
- `docs/planning/PRL_MINUTE_RISK_PROFILE_IMPLEMENTATION_PLAN.md`
- `var/audit/prl_minute_profile_contracts_001/FULL_READ_MANIFEST.md`
- `var/audit/prl_minute_profile_contracts_001/COMMAND_LOG.md`
- `var/audit/prl_minute_profile_contracts_001/vocabulary_search.txt`

## Implementation artefacts

- `src/nvda_desk/contracts/parallel_risk.py`
- `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py`

## Validation artefacts

- `var/audit/prl_minute_profile_contracts_001/pytest_parallel_risk_contracts.txt`
- `var/audit/prl_minute_profile_contracts_001/git_diff_check.txt`

## Diff / archive artefacts

- `var/audit/prl_minute_profile_contracts_001/prl-minute-profile-contracts.patch`
- `/mnt/data/prl-minute-profile-contracts-branch.tar.gz`

## Scope statement

This leaf implements contract-only schema models/enums and default-deny authority flags for PRL-MRP-001/002. It does not implement domain calculations, service integration, workbook editing, event proximity logic, missing-signal calculation, freshness scoring logic, risk-family aggregation, evaluator changes, or plain-English generation.
- `var/audit/prl_minute_profile_contracts_001/git_diff_check_closeout.txt`
