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


## Unit 6 — Tier C operational assurance

- Exact clean commit: `bb44560`.
- Installed-package isolation, cross-process SQLite restart, canonical M01→M02→M03→M00 paper continuity, hermetic provider substitution and broker fail-closed safety: 5 passed.
- Tier C remains current-nonblocking and excluded from `alpha_current`.
- Current alpha promotion remained 19/19 with 802 Tier A tests; Tier B 90/90; Black/Ruff passed.

## Unit 7 — vocabulary adjudication

- Unit-start current scan: 751 overlapping candidates across global plus 12 module namespaces.
- Global-first exact adjudication reduced the residual module set to 373 occurrences by resolving shared contexts once.
- 593 unique occurrence-scoped dispositions were added after reading each exact path/line/context; no generated semantic acceptance, broad suppression, mass rename or automatic alias admission was used.
- Disposition source classes: 293 implementation, 211 test, 50 normative and 39 configuration observations.
- Canonical additions/aliases: none.
- All 13 admitted namespaces (`global`, `m00`, `m02`–`m12` excluding unregistered `m01`/`m13`) rerun with zero candidates and `vocabulary_touched=False`.
- The clean audit exposed stale proof/schema assertions. PM-010 P1-035/P1-036, P1-066..P1-070 and P1-122/P1-123 explicitly quarantine Mutable Runtime Surface, Baseline-only Surface, five generated temporal-status labels, Candidate Audit and Stage-read State. Tests now assert their absence, and the unused `audit_surface` enum category was removed.
- Complete Tier A vocabulary suite: 103 passed.

## Unit 8 — aggregate closeout

- Exact pre-transition clean commit: `747d8d3a7cdf20c1e681d2f1af9ef5693a364e2e`.
- Offline non-editable install: PASS on CPython 3.13.5 with 38 compatible distributions.
- Installed-package smoke: PASS.
- Tier C: 5/5 passed and remained outside `alpha_current`.
- `alpha_current`: 19/19 blocks, 802 Tier A tests, zero skips.
- Tier B: 90/90 passed.
- Promotion receipt verification: PASS; evidence hash `d8e9f16279293eeb83f6c9d3cf01492e937803147b1ecb3738274996638c926e`.
- All 13 vocabulary namespaces: zero candidates, current touch stamps.
- Proof authority: 201 families / 203 test files / 73 blocks.
- Black, Ruff, compile, diff, clean-state and Git object-integrity checks: PASS.
- All eight material-debt rows are repository-resolved. External live commissioning remains unproven because the required entitlement, account approval, credentials, endpoint and authorised side-effect procedure were not supplied; no real order or network effect was attempted.
