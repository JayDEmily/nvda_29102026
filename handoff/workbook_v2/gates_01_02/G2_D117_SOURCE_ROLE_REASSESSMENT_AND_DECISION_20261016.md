# Gate 2 — D117 source-role reassessment and bounded proposed decision

**Issue:** `G2I-011`, D117 Unusual option volume z-score.

**Date:** 16 October 2026 — Australia/Melbourne.

**Status:** `INVESTIGATED / MATERIAL ROLE CLARIFICATION STILL REQUIRED / DEPENDENCY CORRECTION PROPOSED, NOT ACCEPTED`.

**Authority:** Frozen root `EXEC_PLAN.md` G2.2–G2.6; accepted planning boundary A1–A7, recorded in `G2_PLANNING_BOUNDARY_OWNER_ACCEPTANCE_20261016.md`. The register shows D117 has no D predecessor and R041/R075 terminals; direct catalogue readback confirms those dependencies. Its investigation is independent of the blocked L2 book questions. It is performed after the L2 checkpoint, not by assuming its blocker resolved.

## 1. Required and observed meanings

The effective catalogue binds D117 to `R041;R075`, K04, P_BASELINE, `20-60 sessions`, one-minute cadence and each-contract/delta-bucket scope. Its binding note excludes the current observation from its historical baseline. Original workbook `Derived Signals!A121:O121` describes matching contract/delta/expiry-normalised activity.

The accepted brief §5 K04 defines:

`z = (x_current - mean(x_1…x_N)) / sample_sd(x_1…x_N)`

with the sample standard deviation using denominator `N-1`, `N >= 2`, non-zero dispersion, strictly prior baseline observations visible at the knowledge cutoff, and D117's parameter-selected historical window and matching time-of-day/contract bucket. Appendix A defines P_BASELINE as a prior historical sample length, matching rule and minimum sample. The generic mathematical minimum does not replace D117's named session horizon.

Original workbook `Raw Signals!A45:Y45` identifies R041 as volume, IBKR `tickSize`, tick 8. `Raw Signals!A79:Y79` identifies R075 as Average Option Volume, tick 87/generic 105, contracts/day. The provider's [official tick table](https://interactivebrokers.github.io/tws-api/tick_types.html), row 87, corroborates the average-volume field. This older page is deprecated; the current [official RTD generic-tick table](https://www.interactivebrokers.com/docs/excel/rtd/topic/generic-tick-types) corroborates generic 105 as average option volume but is not a TWS deployment certificate. Neither inspected entry establishes the required per-contract/time/delta/expiry historical sample or its sample standard deviation.

**Verified project constraint:** `D116_CALCULATION_DEFINITION_AUTHORISED_CORRECTION_20261011.md` expressly retains D117's R075 dependency while correcting D116 to open-interest inputs. R075 is not open interest. That owner's direction cannot be undone by a worker merely because a kernel does not use R075 numerically.

## 2. Source and test evidence actually inspected

`src/nvda_desk/derived_signal_calculation_truth/_stage1.py`, `_eval_k04`, maps D117 numerical observations to R041. It selects prior observations and computes sample mean/standard deviation from those selected values. This local kernel inspection establishes that R075 does not contribute to that branch's numerical mean or dispersion. It is not a full public call-path or production correctness verdict.

Full test source `tests/product/derived_signal/test_m01_f4_rc14_option_volume_z_public.py` constructs controlled exact-contract R041 history 8/12 and current 16, plus an R075 value 90. The expected z-score is `6/sqrt(8)`; R075 is expected in lineage. Another test expects refusal when that input is absent. The R075 occurrence is locally named `oi`, and the test name calls it required open interest. Those labels conflict with the raw workbook/provider meaning; they do not turn its numeric value into actual open interest. The test does not vary R075 to establish a distinct numerical or source-qualification role.

The fixture's two historical samples exercise a bounded K04 case; they do not establish a full 20–60-session D117 deployment. No tests were run here, and no test is altered or invalidated merely because the fixture is bounded.

Historical context inspected: the 10 October RC14 D117 progress entry; `F4_RC14_D117_RECON_20261010.json`; the 12 October source-preflight PF-03; the D116 owner correction in full; Git lineage of that correction and D117 test (`1ce93a9`, `9e80dbb`). PF-03 already distinguishes a suspected source-role gap from a proved normative defect. This pass narrows that existing question; it is not a new root issue or a new independent acceptance review. Historical passing-test labels are not adopted as source certification.

## 3. Separate conclusions

1. **K04 arithmetic is established:** standardising a current volume observation against a matched prior volume sample is exactly specified. A provider average alone cannot substitute for the prior sample and dispersion without changing the estimator.
2. **R075 native meaning is established within the inspected reference scope:** average option volume, not open interest. Exact actual provider matching/history remains unproved.
3. **R075's required D117 role remains UNKNOWN:** existing authority requires it, but the inspected normative clauses do not specify a numerical contribution or an exact nonnumerical qualifying predicate. Kernel nonuse is not permission to delete it, and requiring a synthetic value to be present does not supply its intended role.
4. **Classification remains UNKNOWN:** the accepted planning amendment does not let an unresolved input-role/selection question be treated as operational-only debt. This pass does not establish a model/policy disqualifier or assign D117 to a downstream group.

## 4. Recommended bounded owner decision — not yet effective

**Recommendation:** define D117's numerical measurement wholly from current and strictly prior matched R041 volume history, and remove R075 as a mandatory D117 dependency. This follows the existing K04 estimator rather than inventing a new purpose for a provider average. It is a proposed correction to the input contract, not a claim that previous owner intent has been disproved.

**Proposed revision:** `D117-RAW-VOLUME-HISTORY-20261016-01`.

Exact proposed clauses for acceptance:

1. Change D117's effective direct raw dependencies only from `R041;R075` to `R041`; retain no D predecessor. R041 denotes current and required historical volume occurrences, not only a single latest value.
2. Preserve K04's sample-mean/sample-standard-deviation z-score, current-observation exclusion, knowledge cutoff and invalid/missing-history refusal. Preserve P_BASELINE, the catalogue's `20-60 sessions` and its matching time-of-day/contract/delta/expiry requirements. No integer horizon, new bucket rule, selector or coefficient is chosen by this amendment. These still require exact, immutable, non-strategy source/selection specification before unqualified classification.
3. R075 retains its raw meaning and identity and remains available for separately authorised uses. It is not redefined, relabelled as open interest, or replaced with a fabricated raw sample.
4. Supersede **only for D117** the D116 correction's statement retaining its mandatory R075 dependency. Preserve the D116 correction, arithmetic, right-conditional open-interest dependencies and every unrelated D/R rule.
5. Record approval as a semantic overlay if accepted. Leave frozen catalogue/workbook/runtime bytes unchanged during Gate 2. Later authorised C–E work must synchronise the normative/runtime catalogue and its hash binding, adjust lawful materialisation/lineage and test expectations, and independently prove the revised input contract. Do not delete tests to obtain green or claim that the existing fixture certifies the new contract.
6. Acceptance of this proposed revision is not Gate 2 acceptance, D117 implementation acceptance, source admission or final M02 allocation. Reassess D117 after the remaining baseline-selection semantics are established; do not turn the dependency correction alone into an eligibility pass.

If the owner intends R075 to perform a separate calculation or qualification function, the required alternative input is an exact authority-backed equation/predicate and compatible source selection. Its present purpose is UNKNOWN; this document does not invent one. The proposed correction is recommended because the inspected accepted estimator already has a complete numerical role for volume history and none specified for the provider average.

## 5. Present disposition, receiving work and limits

Until the exact revision is accepted, `R041;R075` remains effective and D117 remains blocked on source-role and fixed baseline-selection semantics. Update only the new planning/operational assessment fields and evidence links for G2I-011/D117; keep previous authority and assessment values intact. No row is reclassified, no R edge removed, and no inference of provider or implementation completion follows.

After a proper semantic decision, later C–E receives actual source mapping, historical collection, public evaluation, lineage, persistence and independently executed proof. The next in-scope step for this issue is the bounded owner decision above plus completion of the exact non-strategy historical sample-selection contract; operational connectivity is not requested now.

This pass inspects the identified source/test clauses to investigate one semantic role. It does not open a full implementation census or claim complete D117 public-path/proof coverage. No application imports, application tests, broker calls, database, code edits or governing-file edits were performed. The cumulative population and existing issue identities are preserved.
