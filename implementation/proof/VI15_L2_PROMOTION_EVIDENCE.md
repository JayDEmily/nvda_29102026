# VI-15-L2 — Promotion and close-out evidence

## Status

**VI-15-L2 ACCEPTED AND PROMOTED — CLOSE-OUT.**

This record concerns preserved-ancestry promotion only. It does not alter production, proof,
configuration, dependency or package semantics and does not itself perform VI-16.

## Exact accepted identities

- accepted VI-15-L2 candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- accepted candidate tree: `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`;
- independent Tester PASS commit: `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`;
- pre-promotion `main`: `3b1671dc0c15e5ab9023bd20362c432b1fd7a05a`;
- preserved-ancestry promotion integration identity: `eed5c5f6fa9eeda02886ed8fda0d6205177823e5`;
- wheel: `nvda_architecture_kernel-1.0.0-py3-none-any.whl`, SHA-256
  `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist: `nvda_architecture_kernel-1.0.0.tar.gz`, SHA-256
  `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

`main` was fast-forwarded directly to the independently reviewed Tester lineage. No squash, rebase,
merge synthesis or history rewrite was used.

## Pre-promotion verification

Before promotion, the Worker established:

- pre-promotion `main` is an ancestor of the accepted candidate;
- the accepted candidate is an ancestor of the Tester PASS commit;
- no post-candidate `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift exists;
- the Tester disposition is `PASS` for the exact candidate;
- supplied wheel and sdist hashes exactly match the accepted identities;
- `git fsck --full` exits successfully, with only pre-existing dangling blobs reported.

## Promotion operation

Promotion was performed on `main` by ordinary fast-forward to
`eed5c5f6fa9eeda02886ed8fda0d6205177823e5`.

The later routing-only handoff commit `a52bbfc3f0cbdeb908bfe28e0a2a46a6e51a03a3` was not used as the
promotion integration target. Its promotion request is preserved in the completed promotion cycle.

## Disposition

VI-15-L2 is accepted and promoted under the active VI-14 through VI-18 ExecPlan. The next dependent
leaf is VI-16-L1 — fresh whole-BICP semantic review. This close-out does not claim VI-16 semantic
acceptance.
