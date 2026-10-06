# Current Repository State

## Status

**CLEAN MAIN HANDOFF — PCM V5 NOT CARRIED FORWARD IN ACTIVE TREE**

This state supersedes the prior M00-era routing text in this file.

## Repository/product baseline

- Active branch: `main`.
- Distribution/package version: `1.0.0`.
- M00 Raw Signal Occurrence Truth remains the previously completed Raw Signal semantic owner.
- M01 `derived_signal_calculation_truth` is the admitted Derived Signal semantic owner.
- The independently reviewed M01 foundation tranche through DS-R01 is complete and preserved in ordinary Git history.
- PCM V5 execution material is **DO_NOT_CARRY_FORWARD** from this state: `.pcm/` is absent from the active tree.

## Exact preserved PCM/foundation boundary

The last pre-cleanup Programme Owner checkpoint is:

- commit `d0ed951148e33077975ecc5066c8431fed51c5b8`;
- tree `c51d848e5868611f62bd91d851517ed53326285d`;
- tag `checkpoint/ds-gate2-foundation-tranche-complete-20261006`;
- archive branch `archive/pcm-v5-derived-signal-gate2-20261006`.

The final DS-R01 independent foundation review PASS was preserved by reviewer-evidence commit:

- `bbf4b7b97db53c7b635af72842674a049eb285ea`;
- reviewed implementation source `14a6085b863afd083b7ccf2c8a8f02ad435d758e`;
- review result semantic SHA-256 `13de5887f33c5806581536adc05d052b7ac3398b76458ed39d9381b7b2f2ca91`.

All PCM control files, accepted review results and routing history remain recoverable from the archive branch and normal Git ancestry. They are not present in the active `main` tree and are not current routing authority.

## Important completeness boundary

The repository must **not** be described as a completed M01 Derived Signal implementation at this state.

Verified current M01 production source contains the admitted foundation/public API/persistence boundary only. The source itself records that no D-kernel was admitted in DS-I01, and the former Derived Signal plan scheduled the authoritative `D001`–`D209` kernel implementation, advanced kernels, whole-catalogue integration and later package/freeze work after DS-R01.

Therefore the truthful state is:

- M00: prior terminal bounded implementation preserved;
- M01 architecture identity and reviewed foundation: established;
- full M01 Derived Signal calculation implementation: **not complete**;
- future governance/methodology: **not selected**.

A future programme manager may establish new governance from this clean `main` baseline. It must inspect Git history and current source before deciding whether to continue M01 or commission another module; it must not infer completion of the remaining M01 calculation work from the foundation checkpoint.

## Version boundary

No version change is made by this cleanup. `pyproject.toml` and `src/nvda_desk/__init__.py` remain at `1.0.0`, matching the terminal M00 baseline's final authorised distribution version. Future version changes require separate authority.
