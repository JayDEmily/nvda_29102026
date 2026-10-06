# Derived Signal Calculation Truth — Foundation Tranche / PCM Retirement Checkpoint

## Status

**PROGRAMME-OWNER CHECKPOINT — FOUNDATION TRANCHE CLOSED; PCM V5 RETIRED AND NOT CARRIED FORWARD ON ACTIVE `main`**

This record supersedes the earlier form of this checkpoint that left `.pcm/` visible in the active tree.

## Programme Owner instruction

On 2026-10-06 the Programme Owner directed that the PCM methodology used for this tranche be retired from the active repository state. The intended repository pattern is the same structural pattern visible at the terminal M00 boundary: product/source/history remain, while temporary project-execution machinery does not remain in the active `main` tree.

Accordingly:

- `.pcm/**` is classified **DO_NOT_CARRY_FORWARD**;
- `.pcm/` is absent from the active `main` tree after this checkpoint;
- the exact pre-cleanup state remains recoverable in normal Git history and at branch `archive/pcm-v5-derived-signal-gate2-20261006`;
- Git history is not rewritten or pruned;
- the PCM controller is not a post-retirement repository requirement.

## Exact pre-cleanup boundary

The state immediately before active-tree cleanup was:

- commit `d0ed951148e33077975ecc5066c8431fed51c5b8`;
- tree `c51d848e5868611f62bd91d851517ed53326285d`;
- tag `checkpoint/ds-gate2-foundation-tranche-complete-20261006`.

The final independent DS-R01 PASS entering that checkpoint was preserved at:

- reviewer-evidence commit `bbf4b7b97db53c7b635af72842674a049eb285ea`;
- reviewed source `14a6085b863afd083b7ccf2c8a8f02ad435d758e`;
- reviewed source tree `d0efb6ec890a2f1d9429e31fec4db84955012da7`;
- review packet semantic SHA-256 `98f474171f642541136a139f4a047882af3c92b1b61be809016cd17db491ed58`;
- review result semantic SHA-256 `13de5887f33c5806581536adc05d052b7ac3398b76458ed39d9381b7b2f2ca91`;
- disposition `PASS`.

The former PCM review-result file remains recoverable from the archive branch/history; it is intentionally not present as an active `.pcm/` path after cleanup.

## Closed work

The completed and independently reviewed tranche comprises:

1. accepted-authority ingress and independent review (`DS-A01` / `DS-A02`);
2. architecture admission of M01 and independent review (`DS-A03` / `DS-A04`);
3. foundation proof/test work and bounded proof refinements;
4. M01 foundation implementation and bounded repair iterations; and
5. final independent DS-R01 `PASS`.

## Completeness/non-claim boundary

This checkpoint closes **that foundation tranche only**.

It does **not** assert that the entire M01 Derived Signal Calculation Truth module is implemented. Current source explicitly retains the DS-I01 boundary that no D-kernel is admitted there. The former plan's later D001–D209 kernel, advanced-kernel, whole-catalogue integration and package/freeze work was not executed before PCM retirement.

Therefore:

- M00 remains the completed Raw Signal semantic owner from the prior terminal baseline;
- M01 is durably assigned as `derived_signal_calculation_truth` and its reviewed foundation exists;
- the full authoritative M01 calculation behaviour remains future work unless a future Programme Owner explicitly changes scope;
- no provider/network effects, order/account mutation or downstream action authority is created by this checkpoint.

## Version

The repository remains at distribution version `1.0.0`. No version bump is authorised or required by this governance cleanup.

## Next-work boundary

No project methodology is active after this cleanup checkpoint. A future programme manager must establish new governance from the clean `main` baseline and must re-establish the intended next semantic unit from current repository evidence before changing product state.
