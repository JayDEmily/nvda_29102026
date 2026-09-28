# VI-12R U06 Stage 6 — Promotion and close-out evidence

## Status

**U06 ACCEPTED AND PROMOTED — STAGE 6 CLOSE-OUT.**

This record concerns promotion only. It does not add or alter U06 production semantics and it does
not authorise U07, VI-14, or any later implementation/closure unit.

## Exact accepted identities

- accepted U06 frozen candidate:
  `8462630277b04d431ad393e2b73039cacb5d6247`;
- accepted candidate tree:
  `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`;
- Stage-4 evidence/handoff commit supplied to the Tester:
  `5224b928117cf12e1213e44cac4afdc09435e628`;
- independent Stage-5 Tester disposition commit:
  `562767529235cedff77d3e740a259fab9d88716e`;
- independent Tester disposition:
  `PASS`;
- Stage-6 pre-promotion `main`:
  `c3ae566ff8367d83dc783289d9b553faa9a51325`;
- Stage-6 preserved-ancestry promotion integration identity:
  `562767529235cedff77d3e740a259fab9d88716e`.

The promotion integration identity is the independent review commit because `main` was
fast-forwarded directly to the reviewed accepted U06 lineage. No merge, squash, rebase or history
rewrite was used.

## Promotion operation and ancestry verification

Before promotion, the following conditions were verified:

```text
git merge-base --is-ancestor \
  c3ae566ff8367d83dc783289d9b553faa9a51325 \
  562767529235cedff77d3e740a259fab9d88716e

git merge-base --is-ancestor \
  8462630277b04d431ad393e2b73039cacb5d6247 \
  562767529235cedff77d3e740a259fab9d88716e
```

Both succeeded.

`main` was then checked out and fast-forwarded with:

```text
git merge --ff-only 562767529235cedff77d3e740a259fab9d88716e
```

Observed result immediately after the operation:

```text
old main: c3ae566ff8367d83dc783289d9b553faa9a51325
new main: 562767529235cedff77d3e740a259fab9d88716e
HEAD:     562767529235cedff77d3e740a259fab9d88716e
branch:   main
```

## Candidate immutability through review and promotion

The exact accepted candidate remained the production/proof implementation state under review.
Before promotion, the scoped diff from candidate to independent review was empty:

```text
git diff --name-only \
  8462630277b04d431ad393e2b73039cacb5d6247..562767529235cedff77d3e740a259fab9d88716e \
  -- src tests config pyproject.toml
```

The only paths added or changed after the frozen candidate and before independent acceptance were
Stage-4 handoff/evidence and Stage-5 Tester evidence. Therefore no production, test, configuration
or dependency bytes changed after the exact candidate that received independent Tester `PASS`.

## Independent acceptance evidence

The independent Tester disposition is preserved at:

`implementation/proof/VI13R_U06_STAGE5_INDEPENDENT_TESTER_DISPOSITION.md`.

Against exact candidate `8462630277b04d431ad393e2b73039cacb5d6247`, the Tester reported:

- product-proof control: `PASS`, 13/13 obligations across six admitted physical product families;
- admitted product proof: 479/479 passed;
- supplemental U05 restart proof: 27/27 passed;
- U06 construction/delegation/real-PostgreSQL closure set: 15/15 passed;
- architecture/bootstrap: 74/74 passed;
- structural architecture, dependency-direction/cycle and public-seam validation: `PASS`;
- mypy: success across 16 source files;
- Ruff: passed;
- candidate `git diff --check`: passed;
- candidate `git fsck --full`: exit 0, with dangling historical blobs reported diagnostically only.

The Tester also performed a fixture-independent production-path challenge through the declared A00
public production seam with PostgreSQL-backed M00 and found no material U06 defect.

## Stage-6 disposition

The exact independently accepted U06 lineage is integrated into `main` with preserved ancestry.
U06 is accepted and promoted for the scope governed by the active U06 ExecPlan.

This ExecPlan stops here. No U07 begins under it. VI-14 aggregate/interaction closure, VI-15
packaging, VI-16 whole-BICP review, VI-17 provenance audit and VI-18 final bounded-implementation
freeze remain outside this plan and require then-current governing authority plus explicit Programme
Owner routing.
