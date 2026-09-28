# VI-17-L1 — Independent authority/lineage Tester disposition

## Disposition

**PASS**

## Exact reviewed state

- candidate commit: `c07d5277512f600669b05a88cc2c174af3e3b046`;
- candidate tree: `5a156a0170bb31ab2253822a9cf3172bd610f5fe`;
- Tester cycle: `TESTER_VI17_L1_1790601177`;
- accepted VI-16 candidate: `9248f3b1788f8e99e59a0482c4cc393c27942715`;
- VI-16 independent Tester PASS: `9f5f7e90b463365fb39c361f2e346d9e67c6d915`;
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- accepted wheel SHA-256: `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- accepted sdist SHA-256: `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`;
- received Tester handoff SHA-256: `698657aa09b038032eb6b74a223af918be7f9b38c78815b571ef292fcde6dac2`.

The review was performed against a detached worktree at the exact candidate, not the later routing tip.

## Fixed authority reconstruction

The Tester independently recomputed the current fixed authority identities:

- accepted BICP JSON: `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- accepted BICP Markdown: `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`;
- accepted IRB: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`;
- VI-04 authority closure: `4909bfb3561f4ad08d21d82005f2aa60ed9c18440067c91180f6ee65c85bc9ca`;
- fixed IWO JSON: `a673ff05bc58870fdfca49167482aabe4647889d7750fd1b49805c7064ef7eed`;
- fixed IWO Markdown: `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e`;
- VI-15 final distribution authority: `59ad4a66bedeacd89947fae974808d435fd94cf9eb1ef7e9bbeec7797780b4c2`.

The handoff and implementation copies of the fixed IWO are byte-identical. The implementation-authority binding still
binds the accepted IRB, `IA-AUTH-001`, create target `M / raw_signal_occurrence_truth`, and modify target `A00`.

The VI-06 review fact pattern remains truthful: `implementation/review/VI06_IWO_REVIEW_001.md` is `BLOCKED`, not PASS.
Later explicit Programme Owner direction in `implementation/authority/VI06_OWNER_DIRECTION.md` authorises proceeding
with the fixed IWO for this run while preserving that blocked review record.

## Later authority additions

The material post-root authority additions were independently identified in Git history and inspected in full. They are
separately attributable records rather than silent source/test inventions:

- Raw Signal catalogue carriage at `7eb85b097dd4e05705cc781fd102bddf0f6762ca`;
- U03 recurrence/root-cause direction at `2439688f254d0bb7fc856e5e770fa1e5ae293b4a`;
- U03 review-lineage/blocker correction at `65716819fd24cc7d5941cace83e5883d8e0e76f9`;
- U03 NativeValueV1 domain authority at `4c196dfad6c128c04815b167c1a6bbcd5c0145e0`;
- U03 static-envelope clarification at `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`;
- VI-15 final distribution authority at `466055a1cd5fe678a40049a00f0dc88158951d74`.

The carried signal-catalogue workbook independently hashes to
`519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`, matching its bound identity.

No post-root mutation was found to the fixed BICP, IRB, VI-04 authority, fixed IWO, VI-06 owner direction or
implementation-authority binding paths.

## Thin-transport provenance boundary

The local Git history has one root: `8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e` / tree
`2220077c621eb9fef5b9b2cd37377c6926ff148a`. Recorded external predecessor
`d095954c16a9818eadb60d6364148229f2dc4558` / tree `7fdb0e5308f3af187134bc3ebf633835748e9475`
is not present as a local Git object and is not represented as local ancestry.

This is not concealed. `METHOD_PINS.md`, `GATE_03_BINDING.md`, the VI-08 Worker handoff and the recovered VI-08
architecture-admission evidence explicitly identify the source package/bundle/commit/tree and state that omitted history
is an intentional thin-transport reduction. The accepted Gate-03 binding operates on the supplied implementation
workspace rather than pretending the unavailable predecessor object was reverified locally.

For VI-17-L1, this bridge is sufficient because the current authority bytes needed for the bounded implementation are
embedded at the thin root with fixed identities, and the entire accepted architecture/proof/implementation/package
lineage from that active root through the VI-17 candidate is locally reproducible. This PASS does **not** upgrade
`d095954...` into local ancestry or claim that its absent object was independently reverified.

## Architecture and proof lineage

Current architecture state independently validates as:

- one active runtime module `M00 / raw_signal_occurrence_truth`;
- A00 permitted dependency and declared owner edge exactly `A00 -> M00`;
- M00 package `nvda_desk.raw_signal_occurrence_truth` and public seam `.api`;
- one durable implementation allocation for M00;
- the direct Psycopg PostgreSQL adapter remains a non-owning mechanism;
- zero dependency/public-seam violations.

Current BICP proof identity contains exactly nineteen obligations: thirteen current product obligations and
`IA17-ARCH-001..006`. Product-proof control contains six physical families covering 13/13 current product obligations.
`IA22R01-PROD-009` is the current persistence obligation and predecessor `IA17-PROD-009` remains forbidden/non-current.
The architecture proof axis remains separately governed by `architecture_kernel`.

Independent structural checks passed on the exact candidate:

- architecture validation;
- dependency-direction/cycle validation;
- public-seam validation;
- implementation-authority binding validation;
- product-proof-control validation.

The implementation-authority validator reports the next unallocated candidate module as M01 because M00 is already
lawfully allocated; this does not alter the accepted M00 implementation target.

## Accepted implementation and closure ancestry

The Tester independently checked candidate -> review -> promoted-forward ancestry for U01-U06 and VI-14/VI-15/VI-16.
Every referenced accepted identity is present and is an ancestor of the exact VI-17-L1 candidate. No rewritten or
parallel accepted lineage was required to make the chain resolve.

A complete Git scan of substantive `src/**`, `tests/**`, `config/**` and `pyproject.toml` mutations after the thin root
found the expected architecture-admission/proof-authoring tranches, U01-U06 implementation/reviewer repairs and VI-15
metadata change. No unexplained post-root production/configuration mutation was found outside those governed tranches.

There is no substantive `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift from package candidate
`332c1f95da032f841e8779ef21fe3c1fceb698a2` to the exact VI-17-L1 candidate.

## Package trace

The supplied accepted artefacts independently hash to:

- `nvda_architecture_kernel-1.0.0-py3-none-any.whl` — 37,378 bytes —
  `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- `nvda_architecture_kernel-1.0.0.tar.gz` — 161,445 bytes —
  `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

Wheel metadata states `nvda-architecture-kernel==1.0.0`. All sixteen wheel runtime Python files were compared
byte-for-byte with the exact accepted package candidate and produced `16 compared / 0 mismatches`.

## Repository integrity and acceptance boundary

The exact candidate worktree is clean. `git diff --check` and `git fsck --full --no-dangling` passed. The frozen
candidate itself is an empty freeze commit over the Worker audit packet; later routing changes are confined to handoff
records and do not alter the reviewed candidate.

No material authority/lineage gap or unauthorised semantic mutation was established. Exact candidate
`c07d5277512f600669b05a88cc2c174af3e3b046` therefore satisfies VI-17-L1 and is accepted for subsequent
preserved-ancestry VI-17-L1 promotion/close-out only. VI-17-L2 must not begin in the Tester role.
