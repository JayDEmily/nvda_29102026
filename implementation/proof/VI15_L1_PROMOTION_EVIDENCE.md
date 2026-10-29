# VI-15-L1 — Promotion and close-out evidence

## Status

**VI-15-L1 ACCEPTED AND PROMOTED — CLOSE-OUT.**

This record concerns preserved-ancestry promotion only. It does not add or alter production,
proof, configuration, dependency or package semantics and does not itself perform VI-15-L2.

## Exact accepted identities

- authorised final distribution: `nvda-architecture-kernel==1.0.0`;
- accepted VI-15-L1 candidate: `466055a1cd5fe678a40049a00f0dc88158951d74`;
- accepted candidate tree: `350568be5d5f790d71121fbac383349b9284d649`;
- independent Tester PASS commit: `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355`;
- pre-promotion `main`: `1e4e649115f4eac87d58bfa6ad6c1bbc9912b767`;
- preserved-ancestry promotion integration identity: `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355`.

`main` was fast-forwarded directly to the independently reviewed lineage. No squash, rebase, merge
synthesis or history rewrite was used.

## Pre-promotion verification

The following were established before promotion:

- pre-promotion `main` is an ancestor of the accepted candidate;
- accepted candidate is an ancestor of the Tester PASS commit;
- candidate tree exactly matches the Tester-reviewed tree;
- the post-candidate handoff diff contains no `src/**`, `tests/**`, `config/**` or `pyproject.toml`
  drift;
- Tester disposition is `PASS` for the exact candidate;
- `git fsck --full` exits `0`, with dangling blobs only.

`git diff --check` over the broader handoff lineage reports four trailing-space lines in the immutable
Tester disposition. Direct inspection establishes those as Markdown hard-line-break spaces on the
header fields. They are not candidate drift, and the completed Tester evidence was preserved
unchanged as required by the handoff model.

## Promotion operation

Promotion was performed on `main` by ordinary fast-forward to
`226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355`.

The later routing-only handoff commit `e0c3d7a9da4f1dda2c8ceeef5f88a51f9c958715` was not used as the
promotion integration target. Its active promotion request is preserved in the completed promotion
cycle record rather than being treated as accepted candidate semantics.

## Disposition

VI-15-L1 is accepted and promoted under the active VI-14 through VI-18 ExecPlan. The next dependent
leaf is VI-15-L2 — complete aggregate promotion and truthful package/install proof. No VI-15-L2
package/build/install proposition is claimed by this close-out.
