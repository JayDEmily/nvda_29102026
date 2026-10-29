# VI-17-L2 — Promotion and close-out evidence

## Status

**VI-17-L2 ACCEPTED AND PROMOTED — CLOSE-OUT.**

This record concerns preserved-ancestry promotion only. It does not alter implementation, proof-control, authority, dependency, package or accepted distribution semantics and does not itself perform VI-18.

## Exact accepted identities

- accepted VI-17-L2 candidate: `57712201296c6da811e4e6838d0f3fb302239df4`;
- accepted candidate tree: `1b017b6c01176fc61963a63bcf12d843aac8d0db`;
- independent Tester PASS commit: `90fdc6fc5f2fe13e81202dd50f1f9d4c9dfa4634`;
- pre-promotion `main`: `4daaa4050da594e8feb893bb60f171c6828687af`;
- preserved-ancestry promotion integration identity: `90fdc6fc5f2fe13e81202dd50f1f9d4c9dfa4634`;
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
- supplied wheel and sdist hashes exactly match the accepted identities and package `SHA256SUMS` returns `OK` for both;
- `git diff --check` across candidate to Tester PASS succeeds;
- `git fsck --full --no-dangling` succeeds.

The accepted provenance limitation is preserved: the exact binary/archive digest of the PyYAML `6.0.3` overlay used by the prior accepted proof environment remains `UNKNOWN`. This close-out does not claim a fully self-contained offline proof environment or generally reproducible build.

## Promotion operation

Promotion was performed on `main` by ordinary fast-forward to `90fdc6fc5f2fe13e81202dd50f1f9d4c9dfa4634`.

The later routing-only handoff commit `e7694cbcb36c394fc57d85e92bc005160c676c07` was not used as the promotion integration target. Its promotion request is preserved in the completed promotion cycle.

## Disposition

VI-17-L2 is accepted and promoted under the active VI-14 through VI-18 ExecPlan. The next dependent leaf is VI-18-L1 — final freeze and durable recovery artefact. This close-out does not claim VI-18 acceptance.
