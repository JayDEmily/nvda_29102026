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

## Unit 2 — canonical raw-source-to-M03 workflow

- Expected-red state: 7 failures, all caused by absent upstream contracts/routes.
- Affected M01/M02/M03/M00/entry proof: 118 passed.
- Promotion-control proof: 37 passed.
- Current promotion membership: 16 blocks / 16 families / 18 paths.
- Authority reconciliation: 197 families / 199 physical tests / 69 blocks.
- M01 source, capture, content and repository artefact identities remain distinct.
- M01 non-admission and M02 withheld/rejected outcomes are terminal before M03.
- M03 carries M02 projection references; existing no-projection fingerprints remain stable.
- CLI and ASGI contain translation only.

## Unit 3 — M06 owner-fact completeness

- Exact M11 concentration/inventory and M01/provider liquidity owner facts were added.
- Current facts yield typed observations; absent/stale facts remain explicit unknown.
- Affected proof passed before commit `e7926a6`.

## Unit 4 — durable state and restart recovery

- SQLite state/receipt and typed evidence ports preserve atomicity, idempotency and restart truth.
- M11 and M12 bounded paper/replay surfaces restore from durable evidence.
- Unit proof: 10 passed; affected proof: 237 passed.
- Commit: `24cc97a`.

## Unit 5 — live provider and broker boundary

- Expected-red: eight missing-surface failures, followed by two guardrail failures for byte canonicalisation and blocker ordering.
- Unit proof: 10 passed.
- Affected M10/M00/entry and control proof: 138 passed.
- Authority reconciliation: 200 families / 202 physical tests / 72 blocks.
- Current promotion membership: 19 blocks / 19 families / 21 paths.
- Black, Ruff and diff validation: PASS.
- No real endpoint, credential, order, fill or live-account claim was used.
