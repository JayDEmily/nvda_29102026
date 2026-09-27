# VI-12R U05 Stage 7 — Promotion and close-out evidence

## Status

**U05 ACCEPTED AND PROMOTED — STAGE 7 CLOSE-OUT.**

This record concerns promotion only. It does not add or alter U05 production semantics and it does
not authorise U06.

## Exact accepted identities

- accepted U05 replacement candidate:
  `2bdbedff62307ecfaf6186f9c12814fb662c11a7`;
- accepted candidate tree:
  `e15e743e006217a8a3a6313011caf82265a679cf`;
- independent Stage-6 Tester disposition commit:
  `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8`;
- independent Tester disposition:
  `PASS`;
- Stage-7 pre-promotion `main`:
  `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
- Stage-7 preserved-ancestry promotion integration identity:
  `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8`.

The promotion integration identity is the review commit because `main` was fast-forwarded directly
to the reviewed accepted lineage. No merge, squash, rebase or history rewrite was used.

## Promotion operation and ancestry verification

Before promotion, both of the following ancestry checks succeeded:

```text
git merge-base --is-ancestor main 9f35df4c1915de78847dfc4a23ce886dfa3b5fd8
git merge-base --is-ancestor 2bdbedff62307ecfaf6186f9c12814fb662c11a7 9f35df4c1915de78847dfc4a23ce886dfa3b5fd8
```

`main` was then checked out and fast-forwarded with:

```text
git merge --ff-only 9f35df4c1915de78847dfc4a23ce886dfa3b5fd8
```

Observed result immediately after the operation:

```text
old main: 4bf4b4feb08412f65216fc95d8615d2cc46eadaf
new main: 9f35df4c1915de78847dfc4a23ce886dfa3b5fd8
HEAD:     9f35df4c1915de78847dfc4a23ce886dfa3b5fd8
branch:   main
```

## Candidate immutability through review and promotion

The accepted candidate remained the production/proof implementation state under review. Before
promotion, the diff from the accepted candidate to the Tester disposition commit contained only:

```text
handoff/control/CURRENT_STATE.md
implementation/proof/VI12R_U05_STAGE6_TIMEZONE_RETURN_REPAIR_EVIDENCE.md
implementation/proof/VI13R_U05_STAGE6_INDEPENDENT_TESTER_DISPOSITION.md
```

The following scoped diff was empty:

```text
git diff --name-only \
  2bdbedff62307ecfaf6186f9c12814fb662c11a7..9f35df4c1915de78847dfc4a23ce886dfa3b5fd8 \
  -- src tests config pyproject.toml
```

Therefore no production, test, configuration or dependency bytes changed after the exact candidate
that received independent Tester `PASS`.

## Independent acceptance evidence

The independent Tester disposition is preserved at:

`implementation/proof/VI13R_U05_STAGE6_INDEPENDENT_TESTER_DISPOSITION.md`.

The Tester reported, against exact accepted candidate `2bdbedff...`:

- Stage-2–5 restart proof: 27/27 passed;
- configured real-PostgreSQL U05 durability family: 55/55 passed;
- accepted U01–U04 regression proof: 416/416 passed;
- architecture/bootstrap: 74/74 passed;
- mypy: success, 16 source files;
- Ruff: passed;
- independent fresh-owner timezone discriminator: PASS;
- independent public-object-graph persistence-bypass challenge: PASS;
- `git diff --check`: PASS;
- `git fsck --full`: exit 0, with six unreachable dangling blobs reported diagnostically only.

The Tester also independently verified the previous timezone defect closed under
`Australia/Melbourne` and `Asia/Kathmandu` PostgreSQL timezone representations/sessions through the
production owner seam.

## Stage-7 disposition

The exact accepted U05 lineage is now integrated into `main` with preserved ancestry. U05 is
accepted and promoted for the scope governed by the active U04-to-U05 ExecPlan.

This ExecPlan stops here. U06 has not begun and is not authorised by this plan. Any U06 work requires
the then-current explicit Programme Owner instruction and governing planning authority.
