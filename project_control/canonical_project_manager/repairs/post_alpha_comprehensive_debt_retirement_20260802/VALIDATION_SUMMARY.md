# Comprehensive Material-Debt Retirement Validation Summary

## Unit 0 — control registration

- Branch: `work/post-alpha-comprehensive-debt-retirement-v1` from `d4bffb8f95141e95353182c3e4c6e6ddc8e15472`.
- Active pack: `POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1`.
- Canonical parent status remains `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`.
- `tests/tier_b/proof_model/test_proof_authority_contract.py`: 15 passed.
- `scripts/proof_authority.py --check`: PASS, 196 families / 198 tests / 68 blocks.
- Black, Ruff, `git diff --check`, and current full-read manifest validation: PASS.

## Unit 1 — promotion identifier migration

- Expected-red proof: five failures, all caused by absent `alpha_current` and stale defaults.
- Canonical key: `alpha_current`.
- Compatibility alias: `pre_m00_current`, membership-identical to `alpha_current`.
- Membership before later units: 15 blocks / 15 families / 17 paths.
- Focused proof authority, promotion gate and environment controls: 39 passed.
- `scripts/proof_authority.py --check`: PASS.
- Three retained `pre_m00_current` promotion receipts independently verify after migration.
- Black, Ruff and `git diff --check`: PASS.
