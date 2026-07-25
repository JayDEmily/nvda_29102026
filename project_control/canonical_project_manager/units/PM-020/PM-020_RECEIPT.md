# PM-020 validation and packaging receipt

## Verified

- Physical discovery reproduces `166 Tier A / 13 Tier B / 179 total` files.
- All 179 test SHA-256 values match PM-011.
- The ledger is `179 YES / 0 NO`; all 179 receipt paths exist and are one-to-one with test paths.
- The ledger records `777` assertion groups and `777` relationships.
- All final file dispositions use the allowed file-level enumeration.
- Complete Tier B shadow validation passed: `49 passed in 10.52s`.
- Proof-block structural validation passed: `proof_blocks_check_all=PASS count=51`.
- `git diff --check` passed.
- `git fsck --full` exited zero; dangling blobs were reported as retained unreachable objects, not integrity failures.
- The 42 Gate C failures match the frozen sequence-160 expected-red node set exactly.
- No skip, xfail or collection-error summary appeared in complete Tier A output.
- Sequence-160 comparison found no source, test, normative, configuration, fixture, script or proof-block mutation.
- Active retained-test and proof-block configuration remains byte-identical to sequence 160.

## Failed

- PM-019 integration validation failed.
- `99` assertion-group relations are unresolved or outside the allowed enum.
- `123` assertion-group proof strengths are unresolved or outside the allowed enum.
- `214` admitted assertion groups lack an exact group-level authority locator projection.
- Complete Tier A remains red: `61 failed, 1097 passed in 16.93s`.
- Nineteen failures are outside the 42 frozen Gate C expected-red nodes.

## Unknown

- No environment route was Unknown in this run.
- Semantic acceptance remains Unknown and is reserved to the Project Manager.

## Blocked

- Mechanical update of `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` is blocked by the failed PM-019 agreement gate. Updating them would falsely promote unresolved relationships.
- P3 repair remains closed in this worker run; failed tests and blocked proof relationships were not repaired, skipped, weakened or suppressed.

## Git state

- Branch: `work/NVIDIA_2026_pm001_pm010_restart_20260721`.
- HEAD: `21c1e5eccfbb818bdd422afd42117f23b1f74f26`.
- The complete dirty working tree and `.git` are preserved in the returned archive.
- Detailed evidence: `GIT_STATE.txt`, `TRACKED_DIFF.patch`, `TRACKED_DIFF_STAT.txt`, `TRACKED_CHANGED_PATHS.txt`, `UNTRACKED_PATHS.txt`.

## Validation executed

- PM-011 physical census and hash continuity.
- Ledger, receipt, count and enumeration checks.
- PM-019 deterministic projection and validator.
- Targeted sequences 161-179.
- Complete `tests/tier_a` and `tests/tier_b` without suppression.
- `scripts/run_proof_block.py --check-all`.
- Git diff and object-integrity checks.
- Sequence-160 protected-surface comparison.
- Final archive safe-path and fresh-extraction validation, recorded in the package sidecar and staging log.

## Artefacts returned

- Complete repository with `.git`.
- All 179 semantic receipts and absolute ledger.
- PM-019 candidate, group traceability, proof and dependency registers.
- PM-019 and PM-020 raw validation output.
- Current count set, Git evidence, repository manifest, open defects, archive checksum and extraction verification.

## Next Project Manager gate

Reopen only the failed PM-019 relationships one file at a time under the serial-write rule; repair the enum and exact-locator defects from full rereads; rerun PM-019; then decide whether active registry/proof projections may lawfully change. Do not begin P3 from this candidate without explicit authority.

`P2 candidate returned for independent Project Manager audit`.
