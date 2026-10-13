# M01 F4 — D175 policy and D189/D192 reconciliation

Date: 13-10-2026. **PROPOSAL ONLY — OWNER APPROVAL REQUIRED.**
Investigation base: `ff4cbd16d67250755fa1dfd5f2bb91cbd159f75c` / tree `0e3ca1a4c52597e5c6ab2f6aed183bfc83ce16b3`.
Latest authority: Programme-Owner Direction, D175 Policy Resolution, 13-10-2026. Investigation and consolidated recommendation only; no new-mathematics implementation, accepted-catalogue mutation or Stage 2.

## 1. Decision recommended

Approve **REFERENCE_CALIBRATED_ENVELOPE_V1**: retain the previously proposed Greek monetary envelope; calculate explicit capital, concentration and liquidity envelope ceilings; translate separately configured CVaR/stress ceilings into the same envelope coordinate using the exact current candidate measurements. Preserve both the native loss measurements/ceilings and the translated limits.

This creates an exact current-state breach test without calling measured CVaR or measured stress loss a permissible limit. It does **not** assert that an arbitrary new hedge has proportional CVaR/stress loss. D189 remains an indicative, envelope-capped target adjustment, not a revalued/executable hedge certificate. Every changed position/candidate requires fresh scenario measurements and a new D175 occurrence before the next decision. That validity boundary is part of the proposed definition, not an optional warning.

The proposal is bounded to one explicitly managed NVDA sleeve and one named account/currency. It is not an account-wide diversified risk model. It supplies no production risk appetite, shock size, confidence level or fraction by default. The numerical values later in this document are proof examples only.

## 2. Evidence and authority trace

Read current root GUARDRAILS/AGENTS/EXEC_PLAN, authority index, relevant accepted brief sections K02/K08/K10–K14 and §§6–17, catalogue rows, API context/selection/history carriers, Stage-1 D175/D176/D189/D192 and D168 source, and relevant tests. Prior complete brief and workbook inspection is retained in the base checkpoint with its exact hashes. Current effective catalogue is still `d651436df1fcd1395f8f1147dfd80db1ed178da4834447a947c3c9c32fd82aa7`.

`D175_AUTHORITY_TRACE.json` independently enumerates the exact catalogue predecessor closure: **95 D identities including D175**, and **81 distinct raw identities**. This is a static graph census, not 95-row semantic revalidation. Every closure row, kernel, parameter profile and declared context is preserved in that record. No transitive predecessor is thereby authorised as a new direct edge.

Direct trace:

| Input | Established meaning | Role, not to be confused with a limit |
| --- | --- | --- |
| R205 | Net liquidation value, account currency | Capital fact N |
| R206 | Available funds, account currency | Account capacity fact A |
| R209 | Excess liquidity, account currency | Account capacity fact E |
| R208 | Maintenance margin requirement, account currency | Requirement M, not spendable funds or permitted loss |
| D162 | Weighted VaR/CVaR from D160 weights and D174 P&L; percentages use positive Candidate.risk_capital_currency | Tail-risk measurement, with confidence/measurement lineage |
| D174 | Candidate×scenario **gross** full-revaluation P&L, using D160/D168 and exact option convention | Scenario outcomes; D168 Greek diagnostics retained; not itself a scalar stress limit |
| CandidateStructureContext | Exact candidate legs/quantities/premium assumptions and positive risk capital | Scope and percent denominator; no account/currency or active-limit policy fields |
| P_RULE | Immutable thresholds, bands and policy coefficients | Can hold explicit policy numbers; cannot hold a precomputed D175 answer |

Accepted brief: D175 at line 287 defines only the minimum of every active common-currency limit. D162 at line 335 defines weighted worst-tail measurement, not allowable CVaR. D174 at line 323 defines full gross revaluation, not an allowed stress-loss threshold. K02 and §§6/9 supply explicit unit conversion and versioning, not a financial budget policy. No inspected accepted rule fixes activation, policy fractions, concentration scope or mapping of these measurements into permitted limits.

The independent concentrations D124 (market OI), D128 (dealer gamma) and D143 (venue depth) are not D175 dependencies and are not the managed sleeve's capital-concentration policy. They must not be silently imported.

### Source and tests

At base `_stage1.py:3356–3370`, D175 takes abs of all supplied R205/R206/R209/R208 values and recognised D162/D174 scalar fields and returns their minimum. It does not consume its candidate context or a policy profile, and does not require complete direct inputs in this pure kernel. The public graph does require its declared predecessors/contexts and refuses unavailable Stage-2 kernels (`api.py:2228–2236`). Public absence does not make the pure-kernel arithmetic correct.

The current controlled D175 witness supplies D162=80 and D174=70 as scalars, account values 100/50/90/60, no candidate context or policy, and expects 50 (`test_m01_f4_cross_stage_rule_algebra_own_kernel.py:66–72`). It demonstrates the shortcut and lineage plumbing, not accepted CVaR/matrix/policy semantics. D176 tests consume a scalar D175 plus configured per-unit risk; D189/D192 tests do not establish monetary conversion. No test has been changed in this investigation. The ten-test inherited file reran successfully on Python 3.12.14/pytest 9.0.3: diagnostic evidence, **not** the required 3.13.5 acceptance run.

### History, including newly available material

The D175 shortcut appears at `d881165a63843328b0b7fc2e8eee60b2bd1c4911`; the inspected `b6a300e3df569f887100debaca3fe643f48d0866` diff reformats it without introducing limit formulas. Current authority entered the continuation at `d5c39c2c563831529b532f8de2eee24df2a4cebd`. Relevant pickaxe searches and diffs did not recover another accepted D175 policy.

The previously unavailable admission archive now arrived. Its **278 active text members** were scanned for D175/active-limit-carrier literals, with no matches. Archive SHA and scan boundary are retained in D175_AUTHORITY_TRACE.json. This does not claim a complete audit of its binary archives or Git objects. Prior D193, D104, D116 and D134/D135 repair precedents are retained in the base resolution record; none supplies D175 risk appetite.

Retrieved project continuity did not supply an explicit prior owner-approved D175 formula. Prior assistant statements were treated as continuity, not governing evidence.

## 3. One consistent risk coordinate

Retain the earlier **GREEK_SHOCK_ENVELOPE_V1** definition, with all shocks fixed by an exact immutable version:

```text
G(x) = S*|delta| + (S²/2)*|gamma| + V*|vega| + T*|theta|
```

S>0 is an absolute underlying-price shock in currency C per share, V>0 a volatility-point shock, T>0 days. D168/D181–D184 already include quantity and multiplier. The four terms are currency C. Explicit canonical vega and theta scaling is mandatory; no extra multiplier or inferred factor 100.

D175 obtains reference x from **D174's retained D168 diagnostics**, through its declared D174 edge. It must not recursively fetch D168 or D181–D184 as an undeclared direct input. D189 independently forms x from its four live exposure predecessors and requires exact equality with the reference exposure/scoping evidence in D175 before using that budget. The D174 diagnostics are a unit/reference carrier, not a substitute for its nonlinear scenario P&L.

Set `G0=G(x_reference)`. Measurements:

```text
C_signed = D162.CVaR_currency
C = max(0, C_signed)
W = max(0, max_s(-D174.PnL_s))
```

The selected stress set is the exact full D174 scenario set, including zero-weight scenarios; stress is worst admitted shock, not weighted CVaR. No new random scenarios, losses, fee deductions or option models are introduced. D162 retains its signed value; flooring to zero applies only to this proposed non-negative loss-budget usage. D174 remains gross, with no silent D164 subtraction. A later net-of-liquidation-cost risk policy would be a different definition.

## 4. Exact limit policy proposed

Require finite same-currency account facts N,A,E,M with N>0 and M>=0. Define K=Candidate.risk_capital_currency with `0<K<=N`. The context supplies the explicitly allocated sleeve capital, not a silently inferred account allocation.

Five fractions `f_capital,f_tail,f_stress,f_concentration,f_liquidity` are each explicit immutable Decimal in [0,1]. All five activation flags are explicit booleans; this V1 requires capital, concentration and liquidity active, while tail/stress may be explicitly inactive. Missing flag/coefficient is invalid; zero is a valid active restrictive threshold, not an instruction to disable a limit.

Native permissible thresholds and capacity:

```text
capital_envelope_ceiling      = f_capital*K
native_CVaR_ceiling           = f_tail*K
native_stress_ceiling         = f_stress*K
concentration_envelope_ceiling= f_concentration*N
capacity                     = max(0,min(A,E,N-M))
liquidity_envelope_ceiling    = f_liquidity*capacity
```

These are **new proposed policy mappings**, not recovered finance law. Maintenance margin is used once as a requirement in the proposed N-M absorption-capacity guard; it is never itself an allowed-loss limit. Negative A/E or M>N give known zero capacity, not positive capacity via abs. Combining the three reported capacities conservatively by minimum is an explicit definition; it is not asserted to reproduce broker margin mechanics.

Concentration here means the aggregate **net Greek-envelope risk of the one complete managed NVDA sleeve divided by account NLV**, not OI HHI, gross premium notional or diversified account concentration. Position-set completeness and one-sleeve allocation are mandatory. An arbitrary candidate leg subset cannot be labelled the full live sleeve. Hypothetical mode may enumerate the proposed full sleeve; live mode must match its exact LivePositionContext. Other account exposures are not claimed to be modelled by this V1.

Translate native loss thresholds into the reference envelope coordinate:

```text
tail_envelope_ceiling   = G0 * native_CVaR_ceiling / C     when active and C>0
stress_envelope_ceiling = G0 * native_stress_ceiling / W   when active and W>0
```

For active C=0 or W=0 the corresponding constraint is **non-binding on this reference**, explicitly recorded as such, not emitted as 0 or Infinity. Inactive limits are separately recorded `inactive_by_policy`; this is not the same state as active/non-binding. At least the three mandatory envelope ceilings are finite, so the minimum always has a finite candidate.

```text
B = min(all finite active envelope ceilings)
D175.maximum_currency = B
D175.maximum_percent_risk_capital = 100*B/K
```

If G0=0 and C>0 or W>0, **refuse**: non-zero nonlinear loss cannot be represented in this zero Greek coordinate. If G0=C=W=0, tail/stress are explicitly non-binding, B comes from the finite envelope ceilings and current usage is zero. No fabricated epsilon or zero-budget false breach is introduced.

For G0>0, exact algebra establishes:

```text
G0 > B  iff at least one active constraint is exceeded:
G0 > capital_envelope_ceiling, G0 > concentration_envelope_ceiling,
G0 > liquidity_envelope_ceiling, C > native_CVaR_ceiling,
or W > native_stress_ceiling.
```

Equality is not breach. Crucially, the CVaR/stress **measurement stays on the left of its native threshold comparison**; it is not itself a permissible budget. If a measured loss becomes smaller with fixed G0/threshold, the translated permissible envelope increases, rather than becoming more restrictive as the inherited min(measurements) shortcut can do.

Translation is an exact reference-state calibration, not an assertion that CVaR/W are functions of aggregate Greeks. Its meaning is valid only for the frozen reference occurrence, candidate legs, model, scenario grid, confidence, currency and time. It can also represent a fixed-composition quantity ray when proportional full-P&L scaling is explicitly proved; no such general proof is claimed here. A new hedge composition must be revalued; do not use old coefficients to certify its tail/stress losses.

**Exact numerical carrier:** construct monetary terms/ratios from the exact finite Decimal input values as rationals. Rank limits, resolve ties and compare breach using those exact rationals. Retain each canonical rational as `(numerator: int, denominator: positive int)` in lowest terms, including `maximum_currency_exact` and `maximum_percent_risk_capital_exact`. A finite Decimal convenience field may be rounded downward to 28 fractional places but is not the canonical comparison value. D176/D189/D192 must not compare a rounded display amount when the exact ratio is available; otherwise an exact boundary could be falsely reported as a breach. No epsilon tolerance is proposed. The previously proposed conservative rounding of the *adjustment fraction* remains an additional safety step after exact admissibility, not an excuse to weaken exact monetary comparisons.

## 5. Reconcile D189 and D192 without hidden new edges

Preserve each independent band-midpoint adjustment h_j and the previously proposed **joint** clipping:

```text
lambda_cap = 1 if G(h)=0 else min(1,B/G(h))
lambda = largest z in [0,lambda_cap] with G(x+z*h)<=G(x)
permitted_adjustment = lambda*h
```

Use the earlier exact-rational breakpoint solution and explicitly proposed conservative 28-fractional-place persistence rule. Readback must recheck inequalities. Zero active budget permits only the zero adjustment. In-band exposures remain zero adjustment. No component gets the entire budget independently.

**Validity restriction:** this clips indicative Greek exposure against the same calibrated envelope B. It is not proof of post-hedge CVaR, stress, broker margin, full thesis preservation or executable instruments. Carry `post_adjustment_native_loss_status=requires_revaluation` in D189. Recalculate native measurements and D175 for every changed actual/candidate position before a new D192 decision; no stale reference-budget reuse. Do not weaken the accepted full-revaluation meanings of D174/D188.

D192 consumes the computed D189 carrier and its already-declared D175 predecessor. Verify that D189.reference_risk_currency=G0, its d175_occurrence_id is the selected D175, and all scope/currency/reference/convention identities and cutoffs agree. Then `breach=(G0>B)`; combine this actual comparison with a non-zero **permitted** adjustment for the mandatory-hedge branch. A configuration flag merely enables the rule; it cannot establish breach. Preserve all other accepted precedence and domain-specific comparisons.

The calibrated limit is not generally valid for another vector with the same envelope. This proposal intentionally does not claim universal permissible-loss certification for arbitrary structures. If that stronger meaning is required, aggregate Greek clipping is insufficient and additional leg-level hypothetical revaluation semantics would be needed. Recommend the bounded indicative/reference-state contract above for M01 calculation truth, with no downstream authority to act.

## 6. Exact proposed normative and typed changes — not applied

### A. Insert after the accepted D175 rule (new revision D175-REFERENCE-20261013-01)

> D175 uses REFERENCE_CALIBRATED_ENVELOPE_V1 as defined in sections 3–5 of this approved clarification. Its typed result preserves the maximum currency envelope, maximum percent of explicitly assigned risk capital, every native permissible threshold and measured usage, every translated active envelope ceiling or explicit inactive/non-binding status, binding-limit identities, account/currency/sleeve/reference identities and exact convention/model/scenario/time lineage. It is not the minimum of raw account amounts or measured losses. It is valid only for its frozen reference scope. Missing or incompatible mandatory inputs fail closed. No new Dxxx/Rxxx edge is implied by retention of diagnostics or source lineage.

### B. Row-context changes only

| Catalogue field | Current | Proposed exact replacement |
| --- | --- | --- |
| D175.typed_contexts | `CandidateStructureContext` | `CandidateStructureContext;RiskScopeContext` |
| D189.typed_contexts | empty | `LivePositionContext;RiskScopeContext` |

All raw/derived edges, D identities, kernels and parameter profiles remain unchanged. D192 uses the scope evidence in its declared D189/D175 predecessors; no extra row context or edge is needed. After approval only, synchronise the two CSV copies, loader digest, authority index and mechanically affected census. Do not pre-amend any of them in this proposal pass.

### C. Admit immutable RiskScopeContextV1 (reference-only, no calculated answers)

```text
context_id: str; version: positive int
account_identity: str; account_subject_identity: str; currency_code: str
sleeve_identity: str; underlying_identity: str (=NVDA in V1)
scope_mode: candidate_sleeve | live_sleeve
candidate_structure_ref: VersionRefV1
live_position_ref: VersionRefV1, required in live_sleeve mode
position_membership_source_refs: tuple[str,...]
membership_definition_ref: VersionRefV1
risk_definition_parameter_ref: VersionRefV1
```

Membership refs and the explicit completeness definition must establish the entire managed sleeve and its signed quantities, not merely assert completeness with a Boolean. In hypothetical mode the candidate enumerates the complete proposed sleeve; in live mode exact source refs and quantities must agree with LivePositionContext. This is not permission to place a precomputed current risk, CVaR, stress loss or D175 result in context.

The public `_raw_values` path currently requires one request subject absent basket mode (`api.py:1227–1233`). Account facts and NVDA candidate facts are different domains. Proposed **D175-only** selector: its four direct account R inputs must match RiskScope.account_subject_identity and account_identity/currency; its derived candidate inputs must match the exact scoped candidate/sleeve. Do not relabel an account record as NVDA or invent a multi-subject basket. Preserve original M00 subjects and lineages. This is a narrow heterogeneous-subject contract clarification, not permission to relax subject matching elsewhere.

### D. Retained predecessor carrier requirements

D174 keeps its authoritative candidate×scenario gross P&L matrix and additionally names its already-required D168 Greek diagnostics, their component units and exact occurrence ID. D162 must expose its candidate/ref, signed currency CVaR, confidence, D174 occurrence ID and scenario/model/option-convention identities. A differing D162 scenario/matrix is not compatible merely because its numeric CVaR is equal.

Pass actual predecessor/context/version identities into kernel metadata or a typed reference carrier. The current `_occurrence_kernel_value` lacks complete parameter/context/predecessor refs; persistence alone does not validate this correspondence. No hidden runtime dereference to undeclared signals.

Proposed D175 result adds `reference_greeks`, `reference_envelope_currency`, `native_measurements`, `native_thresholds`, `active_limit_records`, `binding_limits`, `risk_capital_currency`, `maximum_currency`, `maximum_percent_risk_capital`, scope/ref/version/time evidence. Recursive named tuples are representable by existing DerivedResultV1; exact field validation and persisted replay still need proof.

The exact rational fields specified in §4 are canonical; any Decimal `maximum_currency` or percent convenience is labelled by its rounding convention. Integer numerator/denominator pairs fit DerivedResultV1 without introducing a competing risk definition. All downstream consumers must reconstruct/validate the exact amount, with no denominator-zero or non-normalised carrier acceptance.

Literal P_RULE additions: `limit_policy_definition=REFERENCE_CALIBRATED_ENVELOPE_V1`; `capital_active`, `tail_active`, `stress_active`, `concentration_active`, `liquidity_active`; `capital_fraction`, `tail_fraction`, `stress_fraction`, `concentration_fraction`, `liquidity_fraction`; and the already proposed risk-definition/shock keys. D176 must explicitly read the structured monetary ceiling and reject unlike per-unit risk domains; a scalar shortcut must not silently survive this carrier amendment. D189/D192 use the same exact risk-definition version. No arbitrary production values are assigned.

## 7. Numerical positive, boundary and refusal cases

All example amounts use one named example currency; they are not account observations or recommended risk settings. Cases are retained in NUMERICAL_CASES.json and independently checked with rational arithmetic.

Take N=10000,K=10000,A=3000,E=2500,M=1000; fractions capital=.10, tail=.03, stress=.06, concentration=.20, liquidity=.50. Let S=1,V=1,T=1 and x=(1000,0,0,0), so G0=1000. D162.CVaR=200 and D174 gross P&L=(-400,100), so C=200,W=400.

| Case | Exact result |
| --- | --- |
| All five active | Ceilings capital=1000, tail=1500, stress=1500, concentration=2000, liquidity=1250; B=1000, percent=10; equality is no breach |
| Tail fraction .01 | Native tail ceiling=100; translated tail=500; B=500 and current breach true |
| Stress fraction .02 | Native stress ceiling=200; translated stress=500; B=500 and current breach true |
| Concentration fraction .04 | Concentration=400; B=400, breach true |
| A=400 | Liquidity=200; B=200, breach true |
| A=-10 or M=12000 | Known liquidity capacity=0; B=0, breach true for G0>0; no abs resurrection |
| CVaR=0, W=0 | Active tail/stress non-binding; B=1000, not 0 |
| Tail explicitly inactive, native CVaR ceiling=100 | Tail excluded by policy, not mistaken for a missing input; other ceilings give B=1000; D162 remains a required fact |
| Missing D162 or D174 even with tail/stress inactive | Refuse, preserving declared dependency law |
| G0=0 with W=400 | Refuse: positive nonlinear loss in zero envelope coordinate |
| G0=C=W=0 | Valid zero usage, finite B=1000, no breach |
| K>N, N<=0, M<0, non-finite value, missing flag, fraction outside [0,1] | Refuse malformed/incompatible policy or capacity basis |
| Wrong account/currency/candidate/reference/model/confidence/position set; stale/future/ambiguous observation | Refuse; no inferred conversion, scope or nearest match |

Clipping witness for tail-breach case: delta band [0,0], other bands containing zero gives h=(-1000,0,0,0), G(h)=1000, B=500, lambda=.5, adjustment=(-500,0,0,0), residual envelope=500. D192 selects hedge when its hedge rule is active and no mandatory exit overrides it. Residual equality does not certify a new structure's native losses; that state still requires revaluation. For B=1000, the same non-zero adjustment proposal alone cannot trigger risk-breach hedge because current G0=B.

Discriminating future proofs must separately establish each active limit, activation/non-binding distinction, loss sign, common currency, source/account join, exact scenario identity, full sleeve scope, zero-coordinate refusal, policy-version changes, D176 carrier compatibility, D189 joint clipping and D192 breach/precedence. Matrix/refusing/public/persistence proof must follow approval before production changes.

## 8. Approval requested and preserved boundary

Approve the exact reference-calibrated policy equations, activation/zero rules, managed-sleeve concentration meaning, capacity guard and validity restriction; the D175/D189 row-context additions, RiskScopeContext and D175-only account/candidate subject selection; and the retained predecessor/result contracts including necessary D176 consumer synchronisation. These replace the unresolved D175 section of the earlier proposal; they do not alter D178 economics or authorise Stage 2.

No production code, tests, accepted catalogue or root governance has been edited. This is an evidence-only descendant of the preserved checkpoint. New policy implementation remains blocked on explicit Programme-Owner acceptance of this exact recommendation. Stage-1 acceptance remains an independent review result, not an inference from this proposal or its arithmetic checks.
