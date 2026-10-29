# M01 F4 — D178 / D189 / D192 consolidated authority resolution

Date: 13-10-2026. Status: **EVIDENCE AND PROPOSAL; NOT AUTHORISED NEW MATHEMATICS**.
Base: `f491c623d37403884fd4bf05cc47275296e320d1`.
The Programme Owner authorises joint investigation and existing-semantic repairs. New conversions, risk definitions and catalogue amendments require explicit approval. Stage 2 remains unauthorised; this is not a Stage-1 review candidate.

## 1. Recommendation and actual boundary

Resolve D178 with an explicit execution-reference and currency contract. Resolve D189 and D192 together with one versioned monetary-risk definition and a computed D189 risk-evidence carrier. Reuse the existing parameter, recursive-result, context-reference and dependency mechanisms. Do not add a D192→D181–D184 edge merely to recover information already calculable by D189.

There is sufficient authority for the price inequality, four independent band adjustments, action precedence, quantity/multiplier algebra and failure rules. There is insufficient inspected authority for the complete edge-to-price conversion, the monetary-risk functional, its clipping interpretation, or the policy converting D175 inputs into active limits. The proposals below are exact decisions for approval, not recovered project law. No production, tests, normative catalogue or governing file is changed in this checkpoint.

The existing mandatory-predecessor guards are already implemented at `1b64bd44b43cf75555ae2fb20738b701eed04de7`. Repeating that repair would not resolve the three semantic blockers. An isolated side-field patch would likewise leave an emitting D178 branch with unauthorised economics. Dependent production work stops here under GUARDRAILS failure law while the authorised consolidated investigation is preserved.

## 2. Evidence inspected and verified

Read root GUARDRAILS, AGENTS and EXEC_PLAN in full; test-local AGENTS supplement; README, Makefile, pyproject; accepted brief including K02, K08, K11–K14 and §§6–17; authority index and current catalogue; relevant API contracts, public context resolution, predecessor conversion/reuse and graph materialisation; relevant Stage-1 dispatch branches and three inherited focused test files. Read reference workbook rows listed in WORKBOOK_REFERENCE_ROWS.json, including native R016 and R205/R206/R208/R209 meanings. The workbook is supporting evidence only.

The supplied full-Git repository initially had the requested HEAD and empty `git status --short`. `git fsck --full --no-reflogs` returned success with dangling objects reported; those are retained, not pruned. `AUTHORITY_READBACK.json` verifies:

| Object | SHA-256 |
| --- | --- |
| Accepted brief | `603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c` |
| Effective catalogue, both byte-identical copies | `d651436df1fcd1395f8f1147dfd80db1ed178da4834447a947c3c9c32fd82aa7` |
| Reference workbook | `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae` |

209 catalogue rows were read. Original catalogue digests in the brief are historical, superseded by the explicit D134/D135 and D116 exceptions in AUTHORITY_INDEX. The brief's inherited draft-status header is not itself admission evidence; the current accepted root plan and authority index establish its governing role.

### Current source findings, separately established

| Row | Primary source at base | Verified finding |
| --- | --- | --- |
| D178 | `_stage1.py:3377–3391`; brief:289,327–328 | Only checks D133/D177 presence; computes from configured allowance and configured side. Does not read their values or typed order side/size/urgency. |
| D189 | `_stage1.py:3417–3441`; brief:291 | Reads four exposures but outputs only bands enumerated by caller; does not validate a complete four-band schema or apply D175 monetary clipping. |
| D192 | `_stage1.py:3442–3467`; brief:292 | Hedge flag plus non-zero vector causes hedge without a comparable current-risk value. `bool(D187)` is not an explicit score threshold. Missing hold currency can fall through to hold. |
| D175 prerequisite | `_stage1.py:3356–3370`; brief:287,334–335 | Takes absolute values of four raw account facts and recognised CVaR/stress fields, then their minimum. No active-limit policy mapping is demonstrated. A D174 candidate×scenario matrix is not the `stress_loss` field it recognises. |

`OMISSIONS_DIAGNOSTIC_PY312.json` records actual runs: D178 returns 5.5 for both `(D133=4,D177=2)` and `(400,-200)`; typed sell still returns the configured-buy value 5.5; D189 returns the same four adjustments with D175=0 and D175=100000; D192 emits hedge without any current-risk value. These are bounded diagnostic reproductions, not proof that any proposed risk model is accepted.

19 inherited focused tests passed on Python **3.12.14**, pytest **9.0.3**. The project requires **3.13.5**; the supplied bootstrap checks that version but does not supply its interpreter. No pinned-runtime acceptance, full regression, PostgreSQL, lint/type or whole-Stage-1 verification is claimed. The initial workbook read used an incorrect relative path and failed; its corrected read succeeded and is the basis of workbook findings.

Two admission-handover attachments failed to materialise, including the re-upload. They were not read. The current checkpoint contains the governing files needed for this bounded investigation; no conclusion is based on the unavailable attachments. Earlier project-source archives were not comprehensively audited.

## 3. Relevant historical precedents

History was inspected by file lineage and pickaxe searches, then relevant diffs and records, rather than commit titles alone.

| Precedent | Inspected Git evidence | Applicable lesson and limit |
| --- | --- | --- |
| D193 cost repair | Proof `02af6520289d83974e95d1278e9c2cc7886bc640`; repair `2f2d0b70f8539f3efe4e4e775add608c0dc9a2f6` | Use the declared signed arrival-benchmark predecessor, actual executed quantity and multiplier; no replacement quote benchmark. Establishes cost algebra, not D177 utility inversion. |
| D104 clarification | Authority `01202775523ceea4ac0e1c38b71437a1cfba4ebf` and exact normative record | Explicit owner equation precedes repair; no extra scaling inferred from labels. Does not authorise another row's mathematics. |
| D116 dependency correction | `9e80dbb4fc4441b5c5865bf7dc7021a80200dab4` and its normative correction | Correct a genuine source/dependency contradiction only under a narrow owner exception. Reference field meanings matter. |
| D134/D135 correction | `72f20394357be2b1b83cede07ab1296f516c1584`, authority-index exception and positional-book diff | Owner-approved catalogue synchronisation, not an undeclared runtime input. |
| Current three-row refusal repair | `1b64bd44b43cf75555ae2fb20738b701eed04de7`; proposal `44875e9b98cace7a3337230fe9997bd355f7a6f1` | Missing mandatory predecessors refuse. Presence is not correct mathematical use. |

The original runtime introduction `d881165a63843328b0b7fc2e8eee60b2bd1c4911` and formatting/validation successor `b6a300e3df569f887100debaca3fe643f48d0866` retain the simplified three-row calculations. Inspected source/authority history did not supply an accepted four-Greek monetary mapping. This bounded search does not establish absence from every external historical attachment.

## 4. D178 — exact proposed execution-reference contract

### Existing authority

D133 preserves expected fill price `F`, signed slippage per premium unit `c`, bps and expected slippage currency, for exact side, size and multiplier (brief:327). D177 recomputes the D165 utility at the pre-order cutoff and **does not subtract D164 again** (brief:328,336). D165 already deducts D164. OrderIntentContextV1 contains `side`, `intended_size`, `urgency` (api:460–469), but no multiplier or currency. CandidateStructureContextV1 has no currency-code field; UnitConventionVersion is explicit affine conversion, not permission to invent an exchange rate.

No K12 implementation of D133/D177 exists in the current Stage-1 dispatch. Scalar fixtures D133=4 and D177=2 therefore do not establish the future structured cost/utility contract. D164 currently scalarises D133: that is another Stage-1 contract integration prerequisite once normative D133 structure is supplied, not evidence that D133 should remain scalar.

### Proposed clarification `EXECUTION_EDGE_CURRENCY_V1` — approval required

For one selected leg, `q = OrderIntent.intended_size > 0`, `m > 0` is the exact D133-retained contract multiplier, and `s=+1` for typed buy, `s=-1` for typed sell. Let `M=(bid+ask)/2`, `c=s(F-M)`, `Q=q*m`. All premium prices and E/r below must use the same named currency C. Require D133 to retain q, m, side, selected contract, decision-midpoint reference, order-intent ref, cutoff and currency/convention refs. Verify `expected_slippage_currency=Q*c` and `slippage_bps=10000*c/M` when M>0.

Do not add an undeclared R016 lookup. The multiplier is retained predecessor evidence required by D133's existing rule. A concrete Stage-2 D133 producer must later establish its lawful source.

Use `E` = D177's **untransformed, risk-adjusted, net currency utility** at the D133 executable reference, and reserve `r` in that same declared domain. A transformed score alone is insufficient. Require D177 to retain the currency-domain value and utility-definition/convention identity. An arbitrary monotone score cannot silently be treated as money. Version 1 refuses unlike currencies; an FX-capable successor requires an exact lawful dated rate/source contract, not a numerical guess.

At the same frozen candidate/state/risk terms, change only execution-cost price, so for proposed limit p:

```text
d(p) = s*(p-M)
E_at_limit(p) = E - Q*(d(p)-c)
edge_bound = c + (E-r)/Q
a = min(c, edge_bound, urgency_cap[OrderIntent.urgency])
buy_target  = min(ask, M+a)
sell_target = max(bid, M-a)
```

Require finite values, `0<=bid<=ask`, positive M/q/m, named non-negative urgency cap, `c>=0` and `a>=0`; otherwise refuse in this proposed V1. Require an explicit urgency entry; no implicit urgency default or configuration-side override. Output at the permitted boundary is the proposed deterministic choice within the accepted inequality. Retain `E_at_limit>=r` as a discriminating proof condition.

The important difference is reference price. `min(c,(E-r)/Q)` would reserve an entire midpoint-to-limit cost from an E already net of c. The proposed equation reserves only the **change** from the already-costed execution reference. Example: q=2,m=100,M=5,F=5.5,c=.5,E=20,r=30 gives edge_bound=.45 and buy target 5.45; retained edge is exactly 30. With E=40,r=30 the D133 cap .5 binds, retaining 40. This price-reference interpretation is not explicit in current authority and needs approval.

Multi-leg headroom must not be spent independently by every leg. Proposed V1 allocation: immutable non-negative leg weights w_l sum to 1, `H_l=w_l*(E-r)`, and `edge_bound_l=c_l+H_l/(q_l*m_l)`. All order legs and allocation version are fixed together; a changed or missing leg/allocation refuses. The joint execution-price change satisfies `sum Q_l*(d_l-c_l)<=E-r`. This is a proposed allocation contract, not existing authority. A single leg has w=1. Do not multiply by Candidate.quantity a second time without its declared quantity convention; D168 source currently uses leg_quantities directly.

Price ticks, nonlinear utility/price-dependent risk revaluation and favourable-negative-c cases are not silently approximated. They need an explicitly approved extension if required; this V1 limitation must be accepted, not mistaken for complete support of every possible contract.

## 5. D189 / D192 — one proposed exact risk convention

### What can be reused

D181–D184 already aggregate quantity×multiplier×Greek; do not multiply them again. Units are share-equivalent, delta change per underlying currency price, currency per volatility point and currency per day. K14 supplies delta×price-change, half gamma×squared-price-change, vega×IV-change and theta×elapsed-days monetary terms. K14 is a dimensional precedent; it does **not** authorise a new prospective risk functional. D174/D188 require full nonlinear leg revaluation; no Greek metric is presented as a substitute for either.

### Proposed `GREEK_SHOCK_ENVELOPE_V1` — genuinely new policy, approval required

Select one named currency C and immutable strictly positive shocks `S` (underlying-price units C/share), `V` (volatility **points**) and `T` (days). Fixed coefficients in P_RULE can represent these without a precomputed answer or new signal dependency. For exposure x=(delta,gamma,vega,theta):

```text
R(x) = S*abs(delta) + (S*S/2)*abs(gamma)
       + V*abs(vega) + T*abs(theta)
```

This is the exact definition of a gross Greek shock-envelope metric. It is not asserted to equal CVaR, margin, contractual loss or nonlinear scenario loss. It prevents opposite signed Greek components cancelling in the scalar risk measure. No magnitude-based scaling, implied spot shock, hidden horizon or stochastic draw is used. The owner must explicitly accept this metric as the D189/D192 comparison basis; common currency alone does not establish equivalence of different risk measures.

For four mandatory, distinct, inclusive bands `[lo_j,hi_j]`, require `lo_j<=hi_j`. Define independently:

```text
h_j = 0                         if lo_j<=x_j<=hi_j
h_j = (lo_j+hi_j)/2 - x_j        otherwise
B = D175.maximum_currency       with matching scope and risk-basis authority
lambda_cap = 1                  if R(h)=0
lambda_cap = min(1,B/R(h))       otherwise, B>=0
lambda = largest z in [0,lambda_cap] such that R(x+z*h)<=R(x)
permitted_adjustment = lambda*h
```

The feasible interval contains z=0. Determine lambda from the finite piecewise-linear absolute-value function, using breakpoints `-x_j/h_j` in the interval and exact segment intersections; no iterative approximate optimiser or component priority. Rational ratios/intersections require exact rational arithmetic for decisions. If the persisted Decimal carrier needs rounding, the approved contract must state its precision and round lambda downward, then recompute all inequalities; never round through a limit. Proposal: 28 fractional decimal places, ROUND_FLOOR, with exact-rational admissibility followed by conservative readback.

Interpretation requiring express approval: D175 caps the **joint monetary envelope of the adjustment**, `R(lambda*h)<=B`; residual risk is calculated and must not increase. This allows a partial corrective hedge while residual risk is still above B. It does not assert that clipping alone returns the entire position within the monetary limit. An interpretation requiring `R(x+lambda*h)<=B` instead is materially different and must not be silently substituted.

Proof example: S=1,V=1,T=1, x=(15,0,0,0), delta band [0,10], other bands including zero, B=4. Unclipped h=(-10,0,0,0), lambda=.4, permitted h=(-4,0,0,0), current risk=15, adjustment risk=4, residual risk=11. Four components share the same lambda; inside-band components remain exactly zero. B=0 permits a zero vector without disguising a current breach. Missing or incompatible convention/limit is absence, not a zero vector.

### Typed carrier and lawful information path

`DerivedResultV1` already supports recursive named tuples (api:705,132–149). Proposed versioned D189 structured result:

```text
adjustment: named four-vector
unclipped_adjustment: named four-vector
current_exposure: named four-vector
current_risk_currency, adjustment_risk_currency, residual_risk_currency: Decimal
clipping_fraction: Decimal
risk_definition_id/version, currency, scope_identity: named scalars
d175_occurrence_id, risk_limit_currency: named scalars
as_of_utc, knowledge_cutoff_utc, position_context_id/version: named scalars
```

D189 computes these values from its declared D181–D184/D175 predecessors; callers do not supply current risk as configuration. D192 reads the computed carrier through its **already-declared D189 dependency**, validates the exact D175 occurrence, definition/version, currency, scope, position and time basis, and compares `current_risk_currency > B`. Equality is not a breach in the proposed V1. It must not test non-zero values across the whole structured record: only the four `adjustment` components count as a permitted hedge.

API `_occurrence_kernel_value` currently retains units, result_shape, raw lineage and source cutoff, but not all parameter/context references. Persisted occurrence refs alone therefore need either an additive metadata pass-through or the explicit result evidence above for cross-row risk-version validation. Mere tuple representability does not prove public reuse compatibility.

Proposed literal P_RULE keys are `risk_definition_id`, `risk_definition_version`, `risk_currency`, `risk_price_shock`, `risk_volatility_points_shock`, `risk_horizon_days` and `target_bands` with all four names. These are fixed model/configuration inputs; no `current_risk` or `risk_breached` parameter is admitted. Distinct scoped child parameters must retain the same exact risk convention.

For current-position identity use the admitted immutable LivePositionContext and its source occurrence refs. Proposed narrow catalogue clarification: require LivePositionContext on D189; D192 can consume its exact computed scope through D189 and need not acquire a new signal edge. Require D175's existing CandidateStructureContext to denote the same risk scope/legs; a hypothetical candidate limit is not automatically a live-portfolio limit. A scope-binding rule and validation of the live Greek source set against LivePositionContext refs are necessary, not optional labels. This row-context clarification needs owner approval before catalogue synchronisation.

## 6. D175 prerequisite must be resolved explicitly

Accepted D175 is `B=min(active capital,CVaR,stress,concentration,liquidity limits)` in common currency. Reference R205 is net liquidation, R206 available funds, R208 maintenance margin requirement, R209 excess liquidity. These are facts; they are not all maximum allowed-loss limits. D162 contains measured candidate CVaR, and D174 is a scenario P&L matrix. Current source applies abs/min to them without demonstrating their policy roles.

Do not invent `B=abs(MaintMarginReq)` or use measured CVaR as its own allowed CVaR. The present investigation establishes a **required upstream policy/contract gap**, not a complete D175 financial audit or authority to repair D175 outside scope. Exact missing owner decision: identify each active limit, its mathematical mapping from lawful declared facts plus versioned coefficients, treatment of negative/unavailable capacity, the concentration input/limit basis, and whether the proposed Greek envelope is admitted against that monetary ceiling. No such mappings are approved by this report.

Proposed D175 carrier clarification retains `maximum_currency`, named `active_limits_currency`, currency, scope and risk-definition refs. If percent is emitted, preserve its declared positive capital denominator and `maximum_percent=100*maximum_currency/capital`; reverse conversion is `currency=percent*capital/100`. This algebra is established by K02/K13 unit law, but selection of a particular D175 denominator and policy is still owner authority. Do not assume account NLV and candidate risk capital are interchangeable.

The entire approval packet must include this D175 mapping or a bounded authorisation to resolve it. Approving only the Greek functional does not supply missing active-limit semantics. Stage-1 own-kernel proof can use an exact controlled D175 monetary-limit carrier after approval; it must not claim the actual D175 producer is consequently correct.

## 7. D192 precedence and failure contract

Preserve the accepted order: mandatory exit; breach plus permitted non-zero hedge; D190 utility gain above its declared-domain minimum; D191 currency above D188 expected currency P&L plus currency margin; hold. Use strict comparisons as stated, with explicit versioned thresholds/tie order. D187 is a K07 score: the invalidation rule must name its threshold/domain, not Python truthiness. Policy flags can activate rules but cannot establish facts such as breach.

Require all declared predecessors and the risk carrier even when a higher-priority branch appears to be applicable; missing facts remain no occurrence under §§13,17. Require D190 threshold domain compatibility and D188 currency component; missing currency is not hold. Proof must independently distinguish branch order, score threshold, monetary breach, non-zero permitted adjustment, modification domain and economic-exit comparison.

## 8. Discriminating proof and implementation sequence after authority

1. Record exact approved clarification(s), their versions and narrowly approved catalogue/context changes. Preserve original source and RED history.
2. D178 proof commit before production: typed buy/sell despite a conflicting config side; size/multiplier scaling; D133 signed/bps/currency consistency; independently binding cost/edge/urgency bounds; already-net cost reference; exact multi-leg allocation with no duplicate budget; missing/future/wrong-contract/foreign-currency/nonlinear-score refusals; below-reserve/negative-cap cases; deterministic replay and lineage.
3. D189 proof commit before production: four independent bands and inclusive boundaries; theta-only adjustment; reject missing/duplicate/reversed bands; joint rather than per-coordinate budget; B=0; all-in-band zero; risk-increasing midpoint clipping; exact fractional intersection and conservative persistence; currency/definition/scope/time mismatch; actual lineage/source-set matching.
4. D192 proof commit before production: identical non-zero hedge with risk below/equal/above B; actual breach with zero permitted adjustment; all precedence collisions; missing or tampered D189 risk evidence; different D175 occurrence; score/utility/currency mismatches; no boolean substitute; structured persistence and append-only/retry behaviour.
5. Reconcile D164/D175 contract prerequisites under expressly approved scope, then remaining 30-row own-kernel/public-refusal evidence and full 174/144/30 acceptance obligations. Controlled Stage-2 predecessors do not prove public Stage-2 execution. Run required pinned-runtime regression, architecture/dependency/public-seam, lint/type and PostgreSQL checks, recording every non-run. Freeze one clean full-Git candidate for independent review only when those obligations are met.

## 9. Exact approval boundary

Approve or revise the execution-reference/currency and multi-leg allocation contract in §4; the new risk functional, joint-adjustment clipping interpretation, partial-hedge behaviour and numerical persistence convention in §5; the computed carrier and narrow D189 LivePositionContext/scope clarification; and supply or authorise the missing D175 active-limit mapping in §6. These are programme/domain authority decisions expressly reserved by the current direction, not tool-permission requests.

This checkpoint preserves investigation, reproducible observations and a concrete proposal. It makes **no repair-complete, Stage-1 acceptance or Stage-2 authorisation claim**.
