# AKR-6 architecture projection attempt

Status: NON-NORMATIVE REHEARSAL EVIDENCE — CORRECTED PROJECTION IN PROGRESS.

## Bound input

External brief SHA-256:

`938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`

The brief remains external, exact and unchanged. This record is a kernel-side architecture projection record only; it does not restate or amend the brief.

## Correction of the prior attempt

The earlier AKR-6 projection attempt made two invalid moves:

1. it treated the literal `G02` references in the unchanged external brief as automatically requiring a current `G02` create/modify target;
2. it represented the already-authorised `DO_NOT_CARRY_FORWARD` disposition of the inherited vocabulary-governance mechanism as lifecycle retirement by adding `G02` to current `retired_ids`.

Current explicit human/programme authority establishes that the inherited vocabulary-governance mechanism and its `G02` structural allocation are not carried into the target kernel. `DO_NOT_CARRY_FORWARD` is not lifecycle retirement. The current tree therefore does not register `G02` as a current governance object or as a retired current-state identity. Git history preserves the former state.

The exact external brief is not changed by this correction. Its literal `G02` text remains part of its accepted byte identity.

## Projection facts established from the exact brief

The brief explicitly:

- assigns Raw Signal Occurrence Truth semantic ownership to `M16`;
- names `A00` as the sole initial caller/consumer and composition owner;
- states that `P01` and `K01` remain non-active and are not contract consumers;
- contains literal `G02` catalogue/schema/governance references.

Under current explicit architecture authority, the inherited `G02` structural allocation is `DO_NOT_CARRY_FORWARD` and is not a current architecture-object target. This is a kernel-side projection disposition; it does not remove or alter the `G02` text in the brief and it does not invent a replacement governance owner.

Accordingly the bounded current target projection is:

```text
create:M16
modify:A00
```

`P01` and `K01` are not targets because the brief explicitly leaves them non-active/non-consumers. `G02` is not a target under the current explicit carry-forward disposition.

## Current architecture state

Current registry state establishes:

- `M16` is not currently registered;
- `A00` is currently registered;
- `P01` and `K01` remain registered non-active placeholders;
- `G02` is absent from the current governance-plane registry;
- `G02` is not represented in current `retired_ids`;
- production `modules` and `surfaces` remain empty.

## Mechanical target-state challenge

The repository-native implementation-authority validator was run against the exact brief bytes and the bounded target projection above and returned:

```text
PASS: implementation authority brief_sha256=938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
targets: create:M16, modify:A00
```

This establishes only exact-byte and current target-state validity. It does not establish semantic completeness or any downstream implementation/proof proposition.

## Next boundary

AKR-6 proceeds to derive the candidate `M16`/`A00` architecture declarations required by the exact brief and challenge them against ownership, dependency and public-seam law. No brief-derived production object is admitted by this rehearsal record.
