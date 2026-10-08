# Current Repository State

## Status

**M01 COMPLETION CONTINUATION — F2 REVIEW REPAIR; F2a TEMPORAL SIGN WORKER RETURN ONLY**

The previous foundation-cleanup checkpoint was not the end of M01. Current Programme Owner instruction is to continue and finish M01 before commissioning a later module.

## Repository boundary

- Continuation branch: `work/m01-completion`.
- Branch base: clean `main` commit `8cd63f2723b936ea8f5a6cfb558b69a4750e6667`, tree `c1bd5cdcbbee31bbb3b18a43840f47e607f254e8`.
- Package/distribution version remains `1.0.0`.
- `.pcm/` is not active authority and must not be recreated.
- M00 remains the completed Raw Signal semantic owner.
- M01 architecture identity and foundation are established; M01 remains incomplete until the accepted D001–D209 calculation responsibility and integration are realised and independently accepted.

## Accepted starting evidence

The final independent foundation review PASS is preserved at:

`handoff/m01_completion/review/DS_R01_FOUNDATION_PASS.json`

Result semantic SHA-256:

`13de5887f33c5806581536adc05d052b7ac3398b76458ed39d9381b7b2f2ca91`

Exact accepted M01 authority is under `handoff/m01_completion/authority/` and indexed by `handoff/m01_completion/AUTHORITY_INDEX.md`.

## Current actor and next action

**Actor: WORKER — F2a contemporaneous quote/trade identity repair only, following independent F2 review of `dcd2067bbd30`; see `handoff/m01_completion/review/M01_F2_INDEPENDENT_REVIEW_20261009.md` and `handoff/m01_completion/repair/M01_F2A_TEMPORAL_SIGN_WORKER_HANDOFF_20261009.md`. F1 remains accepted, F2 is not accepted, and Stage 2 is not authorised.**

Programme Owner amended the Stage-1 acceptance boundary on 2026-10-08 to resolve the normative cross-stage dependency circularity: 174 Stage-1-kernel rows comprise 144 Stage-1-closed rows and 30 cross-stage rows whose end-to-end reachability is deferred until Stage 2. The amendment is recorded in root `EXEC_PLAN.md` and `handoff/m01_completion/STAGE1_ACCEPTANCE_BOUNDARY_AMENDMENT_20261008.md`.

The latest independent Stage-1 review of worker `514cf90` is `REPAIR` / `RECURRENT_CLASS`, recorded in `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_514cf90e4c49.json` and `handoff/m01_completion/repair/M01_STAGE1_SIGNED_TRADE_LINEAGE_REVIEW_HANDOFF_20261008.md`. Public-seam D015→D016 and D015→D120 proofs fail: exact trade sign +1 is lost through mistaken cross-namespace occurrence-ID joins, producing persisted zero instead of signed volume/notional. D121/D122 grouping remains independently unassessed. The prior D109/D170 selection repair was not invalidated by these proofs.

**Latest Programme Owner plan amendment (2026-10-08):** root `EXEC_PLAN.md` (plan-change commit `89f6c012342f1508222700a3acb1f301b6c6723b`) introduces F1→independent inventory review→F2→F3→F4→independent whole-Stage-1 review. The independent reviewer has now issued `F1_INVENTORY_ACCEPTED` for evidence-only candidate `d27b275bbdc696fab561f20a9fd94dfd4a92de47`, recorded at `handoff/m01_completion/review/M01_F1_INDEPENDENT_REVIEW_20261009.md`. **Execute F2 only** in the next worker pass under `handoff/m01_completion/repair/M01_F2_OBSERVATION_IDENTITY_WORKER_HANDOFF_20261009.md`, using proof-before-production commits. Earlier three-leaf proofs are preserved for F4 reconciliation; they are not declared accepted. See `handoff/m01_completion/foundation/STAGE1_F1_INVENTORY_ONLY_WORKER_HANDOFF_20261008.md`. **Stage-1 acceptance is blocked; do not start Stage 2.**

Financial Calendar, later-module work, PCM reinstatement and package-version changes remain out of scope.
