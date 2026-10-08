# ExecPlan — Complete M01 Derived Signal Calculation Truth

## Status

**ACCEPTED BY PROGRAMME OWNER — 2026-10-07.**

This plan supersedes the completed M00 closure plan as active planning authority for the current branch. It is intentionally lightweight. PCM V5 is retired for this continuation and is not part of the active tree or routing model.

## 1. Purpose and fixed starting boundary

Complete the already-admitted **M01 `derived_signal_calculation_truth`** responsibility from the independently accepted foundation state, without reopening M00 or introducing a later module.

Starting product boundary:

- branch base: `main` commit `8cd63f2723b936ea8f5a6cfb558b69a4750e6667` / tree `c1bd5cdcbbee31bbb3b18a43840f47e607f254e8`;
- M00 Raw Signal Occurrence Truth: preserved prior completed owner;
- M01 architecture identity/public seam/persistence foundation: established;
- final foundation independent-review PASS: result semantic SHA-256 `13de5887f33c5806581536adc05d052b7ac3398b76458ed39d9381b7b2f2ca91`;
- package/distribution version: retain `1.0.0`.

The exact accepted M01 brief, normative catalogue and reference workbook are indexed at `handoff/m01_completion/AUTHORITY_INDEX.md` and stored under `handoff/m01_completion/authority/`.

## 2. Non-negotiable boundaries

- Finish **M01 only**. Financial Calendar and later modules are out of scope.
- Preserve M00 semantic ownership and public behaviour except for a defect that is demonstrably required to satisfy already-accepted M01 authority; such a defect must be separately evidenced before change.
- No direct M01 access to M00-owned PostgreSQL relations; use the admitted typed M00 public projection only.
- No provider-specific fallback, provider/network effects, order/account mutation or downstream authority to act on calculated values.
- No invented defaults. Missing mapping, context, units, history, version compatibility, temporal prerequisites or predecessor truth remains absence/fail-closed exactly as the accepted brief requires.
- Preserve exact D001–D209 catalogue identity/dependencies and K01–K17 mathematics. Implementation convenience does not choose estimator, sign, scaling, annualisation, tie-break, interpolation, extraction or result meaning.
- Version remains `1.0.0`; changing package/distribution identity or version is out of scope unless the Programme Owner separately authorises it.
- Do not recreate `.pcm/`.

## 3. Execution discipline

For each stage below:

1. inspect the exact accepted brief/catalogue and current implementation before changing behaviour;
2. write the executable proof/tests for that stage **before** production implementation and commit the proof boundary separately;
3. implement only the behaviour established by accepted authority and that proof boundary;
4. run the relevant focused proof plus the necessary regression/architecture checks;
5. freeze one exact candidate and return it to an independent reviewer;
6. on reviewer PASS, continue to the next stage; on REPAIR, repair only the proved defect/class and return for fresh review.

The Worker may perform proof-authoring and implementation sequentially on this branch, but the Git history must preserve their order: the proof/test commit precedes the production-behaviour commit. Independent review remains a separate actor/thread.

## 4. Stage 1 — foundational deterministic kernels and graph mechanics

### Proposition

Every authoritative catalogue row bound to `K01_TIME` through `K08_RULE_BUCKET_POLICY`, plus `K16_STRUCTURED_ASSEMBLY` and `K17_ORDER_FLOW_IMBALANCE`, is calculated under the exact accepted mathematics and version-consistent dependency/history rules with no hidden defaults.

### Required proof/implementation scope

Cover the accepted catalogue bindings and representative/adversarial behaviour for:

- temporal distinctions and expiry/session calculations;
- algebra/scaling and deterministic transforms;
- anchored returns/rates of change;
- baseline/z-score/rank/percentile laws;
- realised-risk/history sufficiency;
- coherent regression/dependence;
- weighted score/latent-factor extraction and transforms;
- rule ordering, grouping, constrained selection and tie-break law;
- canonical structured assembly, including D155 where applicable;
- order-flow imbalance, including D145;
- version-consistent predecessor reuse, topological evaluation and history sufficiency;
- fail-closed absence, no-look-ahead and idempotent/append-only occurrence behaviour insofar as exercised by this group.

### Stage 1 execution leaves — Programme Owner amendment 2026-10-08

The Worker completes the following three internal leaves in order. These leaves are engineering closure targets inside **one Stage-1 acceptance unit**; they are not independent-review gates. No independent-review stop occurs between Leaf 1, Leaf 2 and Leaf 3. The Worker records a distinct Git checkpoint at the end of each leaf and continues directly to the next leaf unless a governing invariant is `BLOCKED`.

#### Leaf 1 — selection identity and lineage closure

**Proposition:** Stage-1 selection identity remains exact and reconstructable across the entire requesting calculation, including direct raw inputs and predecessor-D graph edges.

This leaf will:

- derive every mandatory Stage-1 selection dimension from accepted row semantics rather than caller policy convenience;
- enforce canonical subject identity for single-instrument calculations;
- enforce material option contract, underlying, expiry, strike, option-right, delta-bucket and selected-option/L2 identities wherever the accepted row semantics require them;
- enforce exact versioned basket/member identity for cross-sectional calculations wherever the accepted row semantics require it;
- preserve the selected identity required to validate predecessor-D reuse in durable occurrence/lineage state;
- prove raw-to-raw, raw-to-predecessor and predecessor-to-predecessor mismatch refusal, including the accepted D131/D087 selected-contract case;
- fail closed when a required selection identity is absent, ambiguous, incompatible or omitted from a caller-supplied policy.

**Leaf completion:** the Worker commits the complete authority-derived proof before the production repair, runs the focused and necessary regression checks, records the Leaf-1 checkpoint, and continues directly to Leaf 2.

#### Leaf 2 — temporal, history and graph-consistency closure

**Proposition:** Every Stage-1 calculation and predecessor reuse decision obeys the accepted temporal, history, version and graph-consistency law with no look-ahead or hidden substitution.

This leaf will:

- enforce knowledge-cutoff eligibility and the accepted event/receipt temporal distinctions;
- enforce required freshness and synchronous-skew constraints;
- enforce exact history sufficiency and refuse insufficient history;
- enforce calculation-definition, parameter, context, unit and selection-version compatibility for predecessor reuse;
- preserve topological evaluation and refuse incompatible, absent or stale predecessor truth;
- enforce no-look-ahead and prohibit fabricated timestamps, silent nearest-neighbour substitution or interpolation unless the accepted row/kernel explicitly authorises it;
- prove deterministic retry/idempotency and append-only successor behaviour where Stage-1 recalculation exercises those obligations;
- prove fail-closed absence across representative direct, history-dependent and predecessor-dependent Stage-1 paths.

**Leaf completion:** the Worker commits the complete authority-derived proof before any production repair required by this leaf, runs the focused and necessary regression checks, records the Leaf-2 checkpoint, and continues directly to Leaf 3.

#### Leaf 3 — Stage-1 kernel and catalogue closure

**Proposition:** Every authoritative Stage-1 catalogue row is bound, implemented, reachable and semantically faithful to its accepted kernel mathematics under the now-closed selection and graph laws.

This leaf will:

- census the complete Stage-1 population bound to `K01_TIME` through `K08_RULE_BUCKET_POLICY`, `K16_STRUCTURED_ASSEMBLY` and `K17_ORDER_FLOW_IMBALANCE`;
- prove that every authoritative Stage-1 row is implemented exactly once with the accepted dependency set, parameter profile and typed-context conjunction;
- run representative and adversarial mathematical proof across every Stage-1 kernel family, including temporal calculations, algebra/scaling, anchored returns, rank/baseline law, realised-risk history, regression/dependence, scoring/transforms, rule ordering/tie-breaks, D155 structured assembly and D145 order-flow imbalance;
- run the full Stage-1 regression plus the necessary architecture, dependency, public-seam, type and lint checks;
- verify that no Stage-2 kernel (`K09` through `K15`) or later-module behaviour has been introduced;
- freeze one exact Stage-1 candidate with clean Git state and complete proof identities for independent review.

**Leaf completion and Stage-1 review boundary:** after Leaf 3, the Worker stops and returns the one exact frozen Stage-1 candidate to the independent Reviewer. Stage 2 remains unauthorised until that independent Stage-1 review returns `PASS`.

## 5. Stage 2 — advanced model, scenario, risk, attribution and evaluation kernels

### Proposition

Every authoritative catalogue row bound to `K09_SURFACE_DENSITY` through `K15_EVALUATION` is calculated using the fixed accepted model/convention/context laws and remains calculation truth rather than an external action.

### Required proof/implementation scope

Cover the accepted surface/density, conditional-distribution/scenario, exposure/stress, execution-aware value, expected-risk utility, path-attribution and evaluation semantics, including required option/P&L/evaluation conventions, candidate/live-position contexts, no-look-ahead and cost double-counting exclusion.

### Review boundary

Stop after one exact Stage-2 candidate and obtain independent review before Stage 3.

## 6. Stage 3 — whole-catalogue integration and M01 completion

### Proposition

All 209 canonical Derived Signal identities operate as one acyclic, version-consistent, fail-closed M01 calculation graph through the admitted M00 seam and M01 persistence/public boundaries, with exact lineage and no external-effect authority.

### Required proof/implementation scope

- complete D001–D209 catalogue census and dependency acyclicity;
- recursive predecessor-D lineage and exact raw lineage;
- representative named calculations across every kernel family;
- history/context/unit/temporal/version refusal cases;
- deterministic retry, idempotency and append-only recalculation;
- M00 isolation and PostgreSQL role/schema isolation;
- structured result persistence and bounded retrieval;
- candidate/live-position/attribution/evaluation semantics where the brief requires them;
- external-effect exclusion;
- all proof classes required by accepted brief clause 18 that remain applicable to full M01 acceptance.

Make only bounded integration repairs required to realise already-accepted semantics. Do not introduce new D identities, dependency edges, kernel meanings, context meanings or external behaviour.

### Terminal review boundary

Freeze one exact integrated M01 candidate and obtain independent whole-M01 review. M01 may be described as complete/active/composable only if that review establishes the accepted brief in full and the architecture lifecycle change is supported by evidence. Until then it remains incomplete.

## 7. Terminal condition

This plan is complete only when:

- the accepted D001–D209 responsibility is implemented in full;
- the applicable clause-18 proof surface passes against one exact integrated candidate;
- independent review accepts that exact candidate;
- M00/M01 ownership, public-seam and persistence isolation remain intact;
- repository state is clean and recoverable;
- no claim is made for Financial Calendar or any later module.

Then stop and return to the Programme Owner before commissioning another module.
