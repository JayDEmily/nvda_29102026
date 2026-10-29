# L03 — documentary source and prerequisite reassessment

Status: AUTHOR_COMPLETED; INDEPENDENT_REVIEW_PENDING (owner-directed final handover).
No product implementation or product/static/runtime tests were authorised or performed.

## Individually sourced findings

### D120 — Signed option order flow

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No demonstrated native selected-option trade-sign source with option trade R120/R121 matched to quote R126/R127, right R015 and multiplier R016 under one lawful D015 option-domain contract.

**Observed distinction:** Existing D015 accepted NVDA shares quote-first profile; D087/D137 option quote assembly (L14) is NOT option trade classification or trade tape. Need option trade/quote time matching and sign rule.

**Proposed next action:** Commission a separately versioned D015 option source/measurement profile or explicit matching owner; then D120 typed window signed flow.

**Decision/receiver:** M00 options trade + M02 direction/flow owners. Approve option trade/quote matching, direction, contract/right/multiplier and window rules.

**Evidence inspected:** `src/nvda_desk/market_measurement_truth/_trade_direction.py` (SHA256 031c8643cab2b00e…); `handoff/downstream_reconciliation/FINAL_REPORT.md` (SHA256 8be0a591460cd29d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D121 — Signed flow by delta bucket

**Readiness:** `HELD_FOR_PREDECESSOR`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No actual compatible D120 signed option-flow occurrence and D091 admitted absolute-delta bucket.

**Observed distinction:** Must retain contract/right/expiry/delta version and separate per-member premium/notional lineages and bucket windows.

**Proposed next action:** After D120/D091, propose per-delta bucket grouping with immutable labels, actual historical contributions and refusal.

**Decision/receiver:** M02 option-flow owner. Accept bucket/window and notional aggregation contract after prerequisites.

**Evidence inspected:** `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D122 — Signed flow by expiry

**Readiness:** `HELD_FOR_PREDECESSOR`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No actual D120 signed option-flow occurrence and compatible D085 option-expiry/calendar occurrence.

**Observed distinction:** Expiry/DTE bucket needs exact domain/session boundary and premium/contract aggregation; D085 not native option-ready.

**Proposed next action:** After D120/D085, admit option expiry/DTE grouping, exact cutoff and per-contract flow provenance.

**Decision/receiver:** M02 option-flow/calendar owner. Accept expiry bucket boundaries, units and maturity convention after prerequisites.

**Evidence inspected:** `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D141 — Queue replenishment/reloading proxy

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No demonstrated matched execution versus cancellation/depletion source law and lawful complete ordered stock/option book+trade coverage.

**Observed distinction:** L14 native book/control handling does not identify executions from anonymous size changes. **K08 already fixes** same-subject/side/price replenishment, earliest qualifying one-to-one restoration for each depletion, capped credited size and the weighted positive-denominator ratio. Source attribution, clock and numeric Δt_max remain open; not the matching or score formula.

**Proposed next action:** Establish lawful execution-versus-cancellation attribution or separately authorised observable proxy and reset-safe ordered source. Future acceptance must select the first qualifying same-subject/side/price restoration within versioned Δt_max, match each depletion once, cap credited replenishment at the depleted size and compute Σ credited_replenished_size / Σ depleted_size across eligible matched events with denominator > 0 (K08 D141); refuse otherwise.

**Decision/receiver:** M00 trade/book source and M02 microstructure owner. Resolve source/proxy attribution, clock and Δt_max; **do not seek new authority for already-fixed K08 earliest matching, cap or score definition**.

**Evidence inspected:** `handoff/downstream_reconciliation/FINAL_REPORT.md` (SHA256 8be0a591460cd29d…); `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` (SHA256 1f540470a2096c90…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D142 — Liquidity resilience

**Readiness:** `HELD_FOR_DEFINITION_OR_POLICY`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No owner-accepted shock onset, severity, joint spread/depth threshold, window and first recovery conditions.

**Observed distinction:** L14 book reconstruction/control does not prove continuous real history, recovery after gaps, or trading venue feed. Source completeness also held.

**Proposed next action:** Version shock/recovery thresholds and observation clock/reset policy; require complete eligible book/quote source before proposing first recovery measure.

**Decision/receiver:** M02 microstructure policy + M00 book/quote source. Approve shock/recovery definition, thresholds, window, missing/gap/reset treatment.

**Evidence inspected:** `handoff/downstream_reconciliation/FINAL_REPORT.md` (SHA256 8be0a591460cd29d…); `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` (SHA256 1f540470a2096c90…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D144 — SMART versus direct depth divergence

**Readiness:** `HELD_FOR_DEFINITION_OR_POLICY`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No accepted SMART/direct matched level, time-skew, price/side/venue identity and unmatched-row policy.

**Observed distinction:** L14 D143 direct position/MPID concentration is NOT an admitted simultaneous SMART/direct comparison; no actual live venues or completeness certified.

**Proposed next action:** Define versioned join/matching/scaling and refusal policy on two reconstructed books with exact identity; prove only when compatible source exists.

**Decision/receiver:** M02 microstructure matcher + M00 market-depth source. Approve price/level/time/venue match, skew and unsupported/missing-book policy.

**Evidence inspected:** `handoff/downstream_reconciliation/FINAL_REPORT.md` (SHA256 8be0a591460cd29d…); `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` (SHA256 1f540470a2096c90…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` (SHA256 603b850802a41878…).

### D145 — Order-flow imbalance (OFI)

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** Paused event-clock K17 requires actual source-event timestamps, but accepted native depth specimens are receipt-only with null provider event time.

**Observed distinction:** The effective owner-approved dependency overlay `D145-L2-CONTRACT-20261016-01` requires co-referenced `R185;R187;R188;R189;R190` (position, operation, side, price, size), replacing only the old catalogue dependency declaration `R187;R188;R189;R190`; the historical catalogue bytes stay unchanged. L13 preserves +(3+1)=+4 source-event example and separate 317 resets. L14 does not grant a clock substitution or D145 implementation.

**Proposed next action:** Keep the K17 event-time profile paused. Any proposed resumption must trace native ordered book mutation and warm-up via `R185;R187;R188;R189;R190` under `D145-L2-CONTRACT-20261016-01`, plus lawful true-instant event time; an alternative receipt-clock profile requires separate owner-approved identity/definition/proof and cannot silently replace event time.

**Decision/receiver:** M00 depth-source custodian + M02 OFI owner + programme owner. Explicit source-event provenance or new owner-approved receipt-clock definition/identity/test allocation; no silent clock swap.

**Evidence inspected:** `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` (SHA256 1f540470a2096c90…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/downstream_reconciliation/FINAL_REPORT.md` (SHA256 8be0a591460cd29d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

**Direct governing source references:** D141 matching/score: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` K08 D141 (line 283). D145 raw roles: `handoff/m01_completion/authority/D138_D145_L2_OWNER_APPROVED_DEPENDENCY_AMENDMENT_20261016.md` §§1–3 (lines 7–27), original `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` §2.2.

## Source versus policy boundary

Option trades (D120) require actual selected-option sign/trade matching; L14 option quotes are not trades. D141 needs executable-vs-cancel interpretation, D142 shock/recovery threshold law and coverage, D144 matched SMART/direct policy. D145 remains on the exact event-time hold; separately versioned receipt-clock interpretation is only a potential owner decision.

## Inspection and scope limit

Read documentary authority / original hold text and relevant public controlled producer/source snippets; consulted historical evidence references in the L00 inventory. Only current documentary source/readiness conclusions were drawn. No test, runtime execution, M00 changes, proof admission, acceptance claim or downstream owner activation. Findings are ready for independent reviewer, not independently accepted.
