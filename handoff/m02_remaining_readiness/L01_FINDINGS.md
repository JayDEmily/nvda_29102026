# L01 — documentary source and prerequisite reassessment

Status: AUTHOR_COMPLETED; INDEPENDENT_REVIEW_PENDING (owner-directed final handover).
No product implementation or product/static/runtime tests were authorised or performed.

## Individually sourced findings

### D062 — Time to next scheduled event

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No declared public R284 scheduled-event temporal projection + revision/relevance/knowledge selector compatible with the admitted controlled D001 temporal occurrence.

**Observed distinction:** D001 is NOW independently accepted for a fixed NVDA true-instant controlled profile; it is not a calendar/event producer. Require exact scheduled UTC, event identity, revision, relevance, cutoff, no-event and typed lineage.

**Proposed next action:** Specify and admit R284 temporal/native provenance and exact event selection, then bounded matching D001 profile and two-case future proof.

**Decision/receiver:** M00 source/calendar custodian + M02 temporal owner. Approve R284 carrier and relevance/revision contract; do not claim native event schedule from D001.

**Evidence inspected:** `src/nvda_desk/market_measurement_truth/_temporal.py` (SHA256 3cd505cab724e90b…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` (SHA256 282f7d73c5e2fdf3…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D085 — Calendar days to expiry

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No admitted option-contract expiry-date R013 + receipt R001 source/identity and US option calendar contract matching a lawful D004 option trading-date occurrence.

**Observed distinction:** D004 NOW has a controlled NVDA/Australia-Melbourne overnight-session result using R023/R024 and actual D003. This does NOT establish US option session/holiday/early-close or the option contract.

**Proposed next action:** Design option-key/date-only mapping and actual exchange calendar with per-expiry D004 source, then exact whole-day difference/refusal.

**Decision/receiver:** M00 option source + exchange-calendar owner; M02 temporal owner. Accept option R013 type, expiry convention and exchange calendar/session/zone before a new profile.

**Evidence inspected:** `src/nvda_desk/market_measurement_truth/_temporal_date.py` (SHA256 fea27e3502251e97…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D086 — Time to expiry in years

**Readiness:** `HELD_FOR_SOURCE`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No specified actual option expiry instant and native R013 contract/date-to-instant convention with a compatible D001 true-instant producer.

**Observed distinction:** D001 is accepted for fixed NVDA true-instant sample, not an option contract maturity clock. ACT/365F and nonterminating 1/365 require exact rational or accepted precision policy.

**Proposed next action:** Supply option expiry instant/zone/day-count and lawful typed D001 matching contract; bind deterministic ACT/365F carrier/refusal.

**Decision/receiver:** M00 option source + M02 temporal/numeric owner. Approve expiry timestamp interpretation and numeric representation; not just a calendar date.

**Evidence inspected:** `src/nvda_desk/market_measurement_truth/_temporal.py` (SHA256 3cd505cab724e90b…); `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…).

### D091 — Delta bucket

**Readiness:** `HELD_FOR_DEFINITION_OR_POLICY`. **Owner:** retained conditional M02 foundation scope.

**First unmet invariant:** No owner-accepted ordered, complete/nonoverlapping absolute-delta interval/label/boundary/out-of-coverage policy.

**Observed distinction:** R112 model delta/right/contract/source variant and numeric scale must be bound; 10D/25D/50D examples are not accepted policy. Neutral classification remains M02.

**Proposed next action:** Propose versioned interval table and refusal examples with actual R112 option contract lineage; commission controlled proof separately.

**Decision/receiver:** M02 classification owner + programme owner. Accept exact interval boundaries/labels/inclusivity, absence, scale and model variant.

**Evidence inspected:** `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md` (SHA256 2d95d7c5e425ed1d…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA256 67bacbcf77afa766…); `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` (SHA256 603b850802a41878…).

## Propagation into later leaves

D085 blocks D096 and D122; D086 blocks D102 and D111; D091 blocks D109 and D121. D001/D004 have accepted *controlled* producers, correcting the older historical absence premise, but there is no automatic option/calendar/domain admission.

## Inspection and scope limit

Read documentary authority / original hold text and relevant public controlled producer/source snippets; consulted historical evidence references in the L00 inventory. Only current documentary source/readiness conclusions were drawn. No test, runtime execution, M00 changes, proof admission, acceptance claim or downstream owner activation. Findings are ready for independent reviewer, not independently accepted.
