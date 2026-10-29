# M01 F4 — bounded consolidation of unresolved typed/numerical authority

Date: 12-10-2026. **PROPOSAL ONLY — NOT ACCEPTED NORMATIVE AUTHORITY.**

## Jurisdiction and evidence

The Programme Owner's latest acceptance of the recommendation to obtain consolidated clarification is authority to investigate and prepare one coherent request. It is **not** an authoritative assignment of previously undefined conversions, value types, parameter names, or risk predicates. This document records the precise outstanding decisions; it does not amend the accepted brief, catalogue, M00 ownership, or ExecPlan.

Primary authority: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 `K08_RULE_BUCKET_POLICY`, especially D175, D178, D186, D189, D192; corresponding rows in `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`; admitted contracts `src/nvda_desk/derived_signal_calculation_truth/api.py` (`CalculationParameterSetV1`, `EntryStateContextV1`, `OrderIntentContextV1`, `CandidateStructureContextV1`); current `_stage1.py` and RC07 source preflight PF-08–PF-11.

### C1 — D186 immutable similarity profile and stored-entry resolution

**Already accepted:** the anchor is the exact D155 occurrence identified by `EntryStateContextV1.d155_occurrence_id`; per-feature `w_j>=0`, sum weights 1, `s_j>0`; similarity is `exp(-0.5 * Σ w_j ((current_j-entry_j)/s_j)^2)` with raw/standardised deltas. Entry and current histories must be temporally/version compatible and lineage-identifiable.

**Verified typed mismatch:** the RC07 RED fixture's nested named tuples are rejected by `CalculationParameterSetV1`. Current D186 implementation also dereferences `entry.entry_state_vector`, which is not a field of `EntryStateContextV1`. See `D186_PARAMETER_SHAPE_PROBE.log` and the inherited `test_m01_f4_cross_stage_d186_entry_anchor.py`.

**Recommended precise clarification:** admit one explicitly versioned, collision-free flat feature-parameter naming convention in existing immutable `P_RULE` entries (for example, `similarity_weight:<exact feature id>` and `similarity_scale:<exact feature id>`), *if approved*; require a one-to-one feature-set mapping and exact anchor D155 occurrence retrieval from the supplied `D155` history, not inline entry-state attributes. Proof shall refuse absent/duplicate feature ids, unresolvable entry references, mismatched feature identity, invalid weights/scales, competing versions, and unavailable/future entry states. **Selection of literal keys and feature identity grammar remains a programme-owner/accepted-contract decision**, even though the typed API accepts flat scalar names.

### C2 — D178 cost and edge-reserve conversion

**Already accepted:** buy price `<= min(best_ask, midpoint + allowed_cost_per_unit)`; sell price `>= max(best_bid, midpoint - allowed_cost_per_unit)`; allowed cost bounded by fresh D133 and the minimum edge reserve from D177; exact typed side/size/urgency. D178 output is option premium; D133's declared output is `currency/bps` and D177's is `utility / currency`.

**Mandatory clarification:** specify the exact source keys/types and units of D133 and D177 used in D178's cap, the precise conversion of each to per-contract option-premium cost, the role of contract multiplier, quantity and FX (if needed), how the edge reserve is imposed, and how missing/ambiguous/unconvertible inputs fail closed. The existing scalar `allowed_execution_cost_per_unit` alone is insufficient evidence of predecessor-bounded cost; avoid inventing a conversion or assuming utility is currency.

### C3 — D189 D175 risk-bound clipping

**Already accepted:** D189 adjusts D181–D184 delta/gamma/vega/theta exposures outside versioned target bands towards clipped midpoints, retaining zero adjustments inside bands; D175 supplies the active monetary risk limit. D181–D184 output units are respectively share-equivalent, delta change/price, currency/vol point, and currency/day; D175 is currency/percent.

**Mandatory clarification:** supply a deterministic, versioned model that maps a proposed 4-dimensional Greek adjustment into the **same currency-risk basis** as D175 (including horizon/scenario/conversion conventions), and define how the admissible adjustment vector is clipped, component/joint ordering and ties, how percent-based limits become currency where applicable, and refusal when metadata is absent. Do not equate raw Greek magnitudes with currency risk.

### C4 — D192 D175 risk-breach predicate and precedence

**Already accepted:** fixed order exit for invalidation, then hedge **only upon D175 risk breach** with a non-zero permissible D189 adjustment, then modify based on D190 utility threshold, then exit if D191 currency value exceeds D188 expected-currency PnL plus margin, else hold.

**Mandatory clarification:** define the exact accepted value(s), units and typed versioned source through which D192 determines `current_position_risk > D175_permissible_risk` (or other explicitly defined breach condition) **without adding undeclared dependencies**. Specify where risk usage/breach state is represented, when it is contemporaneous with D175 and D189, and refusal if it cannot be established. A `mandatory_hedge_on_risk` configuration boolean plus a non-zero D189 vector does **not** itself establish breach.

## What is safely repaired without these decisions

New RED tests at `fae7079` showed four direct own-kernel missing-predecessor emissions: D178 without D133 or D177, D189 without D175, and D192 without D175. The accepted catalogue already makes those predecessors mandatory, so `1b64bd4` adds only six fail-closed guard lines. The fixed rows still have **incomplete substantive own-kernel semantics**; the correction cannot be counted as complete own-kernel proof or Stage-1 acceptance.

## Acceptance accounting, pending decisions

- 144 Stage-1-closed **rows**: RC07 relationship ledger reports **zero outstanding closed-stage dependency edges**; this memo claims no additional edge or row-level acceptance.
- 30 cross-stage rows: **all remain NOT_READY** for complete Stage-1 row-level own-kernel and public-refusal acceptance, despite bounded RC07 and RC08 tests.
- D186 remains deliberately RED and out of broader-green regression totals.
- Real-provider Stage-2 integration is not being implemented or inferred.
- No correction to the accepted maths, catalogue rows, guardrails, agents or execution plan is authorised by this proposal.
