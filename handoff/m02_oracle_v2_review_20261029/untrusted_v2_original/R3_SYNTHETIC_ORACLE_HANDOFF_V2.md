# M02 R3 — synthetic V2 independent oracle design handover

**Status:** AUTHOR-PRODUCED DOCUMENTARY/SYNTHETIC DESIGN; NOT AN ACCEPTED PRODUCT POLICY OR PRODUCT PROOF. This addendum follows the owner's instruction to continue useful work using tentative synthetic settings. It does not close the returned independent G4 gate.

## Concrete work completed

| Group | Frozen authority | Synthetic example and independently calculable expected result | Representative refusal |
|---|---|---|---|
| D079–D081 | K06 single joint OLS-with-intercept | 64 full-rank aligned rows give α=0.0002, βmarket=1.50, βtech=0.40, βsemi=0.70, one fit ID | Collinear factor rows: no fit |
| D078 dependent | K06 same-fit residual | Held-out D075=0.0208 gives predicted=0.0208 and residual=0 | Any coefficient from different fit: refuse |
| D091 | K08 absolute signed option delta bucket | 0.10 maps to 10–25% bin, 0.25 maps to 25–50% bin; exactly 1.00 maps to final bin | Missing or out-of-range delta |
| D142 | K08 first *joint* recovery | t=1 shock, t=3 depth-only recovery is not enough; first combined recovery at t=7, so elapsed=6s | Spread never recovers or generation resets |
| D144 | K02 structured SMART-minus-direct | Four side/rank pairs, same synthetic STK, skew=0.100s; first bid price gap +0.01 USD, depth gap +2 shares | 0.251s skew or absent direct row |

**Important correction:** D142 elapsed time is from the **shock** (t=1) to recovery (t=7) = **6 seconds**, not from baseline (t=0), and the early depth-only state must not trigger recovery. Both books for D144 are distinct sources; equal direct-venue/SMART equality is not assumed. Native receipt time is never claimed to be event time.

Files are actual CSV/JSON scenario artefacts and expected-value oracles, not synthetic M00 native callback recordings or precomputed D occurrences injected into producers. The exact rational validation was performed independently of product imports/runners. `R3_SYNTHETIC_ORACLE_READBACK_V2.json` carries file hashes and results.

## Next implementation frontier (not commissioned)

- **Potential synthetic-only test design:** D079–D081 common-fit family, D091 delta bucket, D142 joint recovery, D144 matched-book difference, and D078 downstream residual example. If future coding is commissioned, author exactly the module-public-seam success/refusal cases permitted by the then-applicable proof law; these CSV rows are *data examples*, not automatically new physical cases.
- **Production/source blockers remain:** no accepted real K06 historical sample/fit, R112 option variant, complete real joint L2 state, SMART/direct simultaneous source coverage, selected-option trade sign, exchange-calendar/expiry and other eight source holds. D145 source-event time remains paused. None of the 28 held identities is promoted by this V2 dataset.
- **Required separate authority:** programme approval of concrete production-neutral settings and actual-source profiles; any source/code/claim changes require their own implementation commission and independent proofs. Owner has approved *synthetic placeholders*, not unconditional production values.
- **Independent tester:** verify the fixture/expected arithmetic, K06/K08/K02 semantics, scope statements, unchanged historical 98/11 evidence, Git restoration, and that G4 is *still pending*. Do not rerun existing product tests for this documentary-only addendum.
