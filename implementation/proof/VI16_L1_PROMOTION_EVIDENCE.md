# VI-16-L1 — Promotion and close-out evidence

## Status

**VI-16-L1 ACCEPTED AND PROMOTED — CLOSE-OUT.**

This record concerns preserved-ancestry promotion only. It does not alter production, proof,
configuration, dependency or package semantics and does not itself perform VI-17.

## Exact accepted identities

- accepted VI-16-L1 candidate: `9248f3b1788f8e99e59a0482c4cc393c27942715`;
- accepted candidate tree: `5560c97ad83a05190603c323eb4fbfa0c21d983d`;
- independent Tester PASS commit: `9f5f7e90b463365fb39c361f2e346d9e67c6d915`;
- pre-promotion `main`: `5a7a027886cb6f854c19dc323b23b8a0b193edd7`;
- preserved-ancestry promotion integration identity: `9f5f7e90b463365fb39c361f2e346d9e67c6d915`;
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
- `git fsck --full` exits successfully, with only eight pre-existing dangling blobs reported.

## Promotion operation

Promotion was performed on `main` by ordinary fast-forward to
`9f5f7e90b463365fb39c361f2e346d9e67c6d915`.

The later routing-only handoff commit `cd0f456bf2b333bf6ce62d5860e7773a7c3245b7` was not used as the
promotion integration target. Its promotion request is preserved in the completed promotion cycle.

## Disposition

VI-16-L1 is accepted and promoted under the active VI-14 through VI-18 ExecPlan. The next dependent
leaf is VI-17-L1 — authority and lineage reconstruction. This close-out does not claim VI-17 acceptance.
