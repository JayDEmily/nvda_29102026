# VI-17-L1 — Promotion and close-out evidence

## Status

**VI-17-L1 ACCEPTED AND PROMOTED — CLOSE-OUT.**

This record concerns preserved-ancestry promotion only. It does not alter implementation, proof-control, authority, dependency, package or accepted distribution semantics and does not itself perform VI-17-L2.

## Exact accepted identities

- accepted VI-17-L1 candidate: `c07d5277512f600669b05a88cc2c174af3e3b046`;
- accepted candidate tree: `5a156a0170bb31ab2253822a9cf3172bd610f5fe`;
- independent Tester PASS commit: `5397a90dd2e245e17bd5e0eb526861396dae3082`;
- pre-promotion `main`: `d45b965919b8cc27f9417860fc597b5d010aff4e`;
- preserved-ancestry promotion integration identity: `5397a90dd2e245e17bd5e0eb526861396dae3082`;
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- wheel: `nvda_architecture_kernel-1.0.0-py3-none-any.whl`, SHA-256 `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist: `nvda_architecture_kernel-1.0.0.tar.gz`, SHA-256 `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

`main` was fast-forwarded directly to the independently reviewed Tester lineage. No squash, rebase, merge synthesis or history rewrite was used.

## Pre-promotion verification

Before promotion, the Worker established:

- pre-promotion `main` is an ancestor of the accepted candidate;
- the accepted candidate is an ancestor of the Tester PASS commit;
- the accepted candidate tree is exact;
- the Tester disposition is `PASS` for that exact candidate;
- no post-candidate `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift exists;
- supplied wheel and sdist hashes exactly match the accepted identities;
- `git fsck --full` exits successfully, with eight pre-existing dangling blobs reported.

## Promotion operation

Promotion was performed on `main` by ordinary fast-forward to `5397a90dd2e245e17bd5e0eb526861396dae3082`.

The later routing-only handoff commit `0477558a4d87e0d363e3618879c44252697ec50e` was not used as the promotion integration target. Its promotion request is preserved in the completed promotion cycle.

## Disposition

VI-17-L1 is accepted and promoted under the active VI-14 through VI-18 ExecPlan. The next dependent leaf is VI-17-L2 — provenance, environment and repository-integrity audit. This close-out does not claim VI-17-L2 acceptance.
