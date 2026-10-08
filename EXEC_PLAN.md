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
6. on reviewer PASS, continue to the next stage; on REPAIR, follow the active reviewer-return repair/checkpoint sequence, repair only the proved defect/class, and return for fresh review.

For the current Stage-1 `RECURRENT_CLASS` review return, the later **Stage-1 reviewer-return foundation checkpoint** section controls worker re-entry and adds a mandatory independent F1 inventory acceptance before further production repair.

The Worker may perform proof-authoring and implementation sequentially on this branch, but the Git history must preserve their order: the proof/test commit precedes the production-behaviour commit. Independent review remains a separate actor/thread.

## 4. Stage 1 — foundational deterministic kernels and graph mechanics

### Proposition

Every authoritative catalogue row bound to `K01_TIME` through `K08_RULE_BUCKET_POLICY`, plus `K16_STRUCTURED_ASSEMBLY` and `K17_ORDER_FLOW_IMBALANCE`, has its Stage-1 kernel logic bound and implemented under the exact accepted mathematics and version-consistent dependency/history rules with no hidden defaults. Rows whose complete dependency closure is available within Stage 1 are also publicly reachable end to end at this stage; rows whose normative dependency closure requires Stage-2 predecessors remain fail-closed at the public graph boundary until those predecessors exist.

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


### Stage-1 cross-stage dependency boundary — Programme Owner amendment 2026-10-08

The accepted catalogue contains 174 rows whose own kernel belongs to Stage 1. Dependency analysis of the normative `derived_dependencies` graph establishes:

- **144 Stage-1 rows** have a complete predecessor closure entirely within Stage 1 and therefore must be publicly reachable end to end for Stage-1 acceptance;
- **25 Stage-1 rows** have at least one direct Stage-2 predecessor: `D097`, `D098`, `D107`, `D108`, `D128`, `D155`, `D158`, `D159`, `D163`, `D164`, `D166`, `D167`, `D172`, `D173`, `D175`, `D176`, `D178`, `D187`, `D190`, `D191`, `D192`, `D199`, `D200`, `D207`, `D208`;
- **5 additional Stage-1 rows** reach Stage 2 transitively through another Stage-1 predecessor: `D156`, `D157`, `D171`, `D186`, `D189`;
- therefore **30 Stage-1 rows** cannot yet have complete public end-to-end graph materialisation without implementing Stage-2 authority prematurely.

For Stage-1 acceptance, all 174 Stage-1 rows will have exact catalogue binding and Stage-1 kernel implementation/proof. The 144 Stage-1-closed rows will additionally be publicly reachable end to end. For the 30 cross-stage rows, Stage 1 will prove the row's own kernel semantics, binding, dependency declaration and fail-closed behaviour using exact predecessor values where required, but public end-to-end reachability through the real graph is deferred until the normative Stage-2 predecessors exist. Stage 2 will prove those cross-stage connections when it implements `K09` through `K15`; Stage 3 will prove the complete 209-row graph end to end.

This amendment changes only the execution/acceptance boundary. It does not alter any accepted `Dxxx` identity, dependency edge, kernel binding, mathematics or final M01 acceptance requirement.

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

**Proposition:** Every authoritative Stage-1 catalogue row is bound, implemented and semantically faithful to its accepted kernel mathematics under the now-closed selection and graph laws; every Stage-1-closed row is publicly reachable end to end, while every cross-stage row remains correctly fail-closed until its normative Stage-2 predecessors exist.

This leaf will:

- census the complete Stage-1 population bound to `K01_TIME` through `K08_RULE_BUCKET_POLICY`, `K16_STRUCTURED_ASSEMBLY` and `K17_ORDER_FLOW_IMBALANCE`;
- prove that every authoritative Stage-1 row is implemented exactly once with the accepted dependency set, parameter profile and typed-context conjunction;
- prove end-to-end public reachability for all 144 Stage-1-closed rows and prove kernel semantics plus fail-closed public behaviour for all 30 cross-stage rows without introducing Stage-2 implementation;
- run representative and adversarial mathematical proof across every Stage-1 kernel family, including temporal calculations, algebra/scaling, anchored returns, rank/baseline law, realised-risk history, regression/dependence, scoring/transforms, rule ordering/tie-breaks, D155 structured assembly and D145 order-flow imbalance;
- run the full Stage-1 regression plus the necessary architecture, dependency, public-seam, type and lint checks;
- verify that no Stage-2 kernel (`K09` through `K15`) or later-module behaviour has been introduced;
- freeze one exact Stage-1 candidate with clean Git state and complete proof identities for independent review.

**Leaf completion and Stage-1 review boundary:** after Leaf 3, the Worker stops and returns the one exact frozen Stage-1 candidate to the independent Reviewer. Stage 2 remains unauthorised until that independent Stage-1 review returns `PASS`.

### Stage-1 reviewer-return foundation checkpoint — Programme Owner amendment 2026-10-08

**Authority and activation.** The Programme Owner authorised this amendment on 2026-10-08 after the independent Stage-1 `REPAIR / RECURRENT_CLASS` review of Worker `514cf90e4c49a3dc72d318796549a6da9dc38cc7` (reviewer disposition commit `2b5b086099561c2e28aa86bf20dfa222c5d4b3ec`). **This checkpoint is active now; Stage 2 remains unauthorised.** The reviewer result and public-seam reproducer at `handoff/m01_completion/review/` are evidence, not a new mathematics, identity or dependency authority.

**Reason for this re-entry.** The previous three Stage-1 internal leaves and their checkpoints remain historical implementation/proof evidence, but no Stage-1 `PASS` has been established. Their broad selection/lineage obligation did not prevent a derived D015 occurrence ID from being joined as though it were an M00 raw-observation ID when D016/D120 applied signed-trade information. The accepted brief already requires exact per-trade signed arithmetic, source lineage, compatible predecessor reuse and fail-closed missing prerequisites (§5 K08; §§7–9, 12–14, 17–18). The intervention below changes the *order and independent proof boundary* for the rejected Stage-1 repair; it does not change these normative obligations.

**Precedence and workload limit.** For this return only, the F1–F4 sequence below supersedes the prior instruction to proceed directly through Leaf 1 → Leaf 2 → Leaf 3 without interim reviewer engagement. The three original leaf propositions and full Stage-1 acceptance conditions remain binding; previously authored work is reused where evidenced, not blindly repeated or declared accepted. Work **F1 only** before its independent reviewer checkpoint. Do not advance F2/F3/F4, edit production, or turn uncertain relationship meaning into implementation policy while F1 is unaccepted. F2 and F3 are separate bounded engineering leaves with separate proof-before-production checkpoints; independent review next occurs at F4 unless a required invariant fails earlier.

#### F1 — authority-derived relationship census and implementation map (evidence only)

**Proposition:** Every normative Stage-1 input relationship is accounted for and classified by the exact accepted meaning needed to associate inputs with the requesting calculation; gaps between this meaning and the current public calculation path are visible before coding.

The Worker will produce a reviewer-readable versioned inventory under `handoff/m01_completion/foundation/` and commit it. The inventory will:

- mechanically enumerate **all 174** accepted Stage-1-kernel rows from the exact digest-indexed normative CSV and, for each row, every declared direct `Rxxx` and predecessor `Dxxx` dependency; separately account for direct and transitive Stage-2 predecessors without pretending their graph is currently executable;
- reconcile the census to independently generated row/edge counts and expose an explicit set-difference (`missing`, `extra`, `unclassified`) rather than treating a sampled set as exhaustive; cite the precise authoritative catalogue row and applicable brief rule for each material classification;
- classify the *required relationship*, not just the identifier field: per-observation, per-subject/contract, same-window/history, versioned basket/member, candidate/context, bucket/group aggregation or other authority-established type; distinguish **one-to-one**, **one-to-many**, **many-to-one** and **many-to-many** where derivable, and mark genuinely unspecified cardinality `UNKNOWN`, not guessed;
- record relevant join/selection identity dimensions, source vs derived occurrence-ID namespace, direct/ultimate raw lineage, predecessor-D lineage, parameter/context/model/version identity, time basis, grouping and fail-closed/absence requirements **only where supported** by the brief/catalogue; mark non-applicable fields `N/A` and unsupported assertions `UNKNOWN` with their source gap;
- for every distinct currently implemented selection, value-carrier, reuse, aggregation or correlation mechanism, identify the relevant production entry point and supporting tests; distinguish *current source behaviour* from *required authority* and identify unproved or mismatching implementations;
- include the recurring D015→D016/D120 witness, the D109/D170 contract-predecessor repair and the not-yet-independently-proved D120/D091→D121 and D120/D085→D122 grouping paths, without treating other similar joins as verified failures merely because they look alike;
- assign a stable relationship-class identifier to each classification and map each classified normative edge/row use to one class, with representative positive, negative and public-seam proof obligations per class; do **not** treat a source-code census alone as a proof of correct meaning;
- explicitly list unresolved normative ambiguity, implementation absence and coverage gaps, with a bounded proposed disposition. A material gap that cannot be resolved from accepted authority is `BLOCKED`, not licence to invent a selection or correlation law.

**Bounded execution:** F1a enumerates the authority graph and completeness census; F1b maps authority-defined relationship classes to actual source/public-seam carriers; F1c reconciles gaps and writes the proof matrix. Each is a separate Git evidence checkpoint. This is an ordering by dependency (inventory → map → proof), not three new independent acceptance gates. Use scripts as needed to census the catalogue, but do not create a second normative catalogue or redefine a D/R edge. No production changes; no new Stage-1 PASS claim.

**F1 acceptance and stop:** The Worker freezes an exact clean Git **evidence-only F1 candidate** (inventory, classifications, discrepancy register, commands/results, referenced sources and handoff) and stops for independent reviewer assessment. The reviewer verifies exhaustiveness against the accepted CSV, authority-grounding of relationship classes, coverage of the known failed witness and declared gaps, and that no production/normative/governance change occurred beyond this Programme Owner amendment. Dispositions: `F1_INVENTORY_ACCEPTED` (authorises F2 only), `F1_REPAIR` (return bounded inventory defect), or `BLOCKED` (unresolved required authority). **F1_INVENTORY_ACCEPTED is not Stage-1 acceptance.** The worker may not proceed beyond F1 without that separate evidence checkpoint.

#### F2 — observation-level identity and signed-flow closure

**Proposition:** When an accepted calculation applies a derived per-observation fact to raw inputs, the association is explicit, exact and reconstructable through admitted source/predecessor lineage, without equating different occurrence-ID namespaces or fabricating zero on missing correlation.

After `F1_INVENTORY_ACCEPTED`, the Worker will author and separately commit authority-derived public-seam proofs **before** any production repair. First prove D015→D016 and D015→D120 with known buy/sell signs, multiple distinct observations, same/different contracts, missing or ambiguous sign, mismatch refusal, correct quantities/notional, persisted R/D lineage, retry and recalculation. Extend proof to **every affected relationship class** identified in F1, not necessarily every edge by hand-written fixture; map coverage back to the census and record any unproved instance. Repair only the established correlation mechanisms; preserve M00-owned semantics, opaque ID namespaces, parameter/context versioning and existing admitted behaviour. Run focused regression and commit the F2 checkpoint. If the required model/contract was not resolved at F1, return `BLOCKED` instead of coding a substitute.

##### F2 reviewer-return batching amendment — Programme Owner instruction 2026-10-09

**Purpose and precedence.** The independent review of Worker F2 checkpoint `dcd2067bbd306e1cf1aeb5fc9665dce25a4c8684` returned `REPAIR / RECURRENT_CLASS` at reviewer commit `5e210f096b6220182a3a1d575020364fd92909c4`. The reviewer found a new public-seam D015 contemporaneous-quote defect and separately identified the D064/D065 event-score identity prerequisite. The initial reviewer handoff ordered an independent stop after **F2a only**. At Programme Owner direction this routing is superseded: perform **F2a and F2b as sequential, separately committed internal engineering checkpoints**, with **one consolidated independent F2 review** after both. This paragraph controls the review cadence of this F2 return over the earlier statement that the next ordinary independent review is at F4, and over the historical F2a-only handoff. It does **not** change normative semantics, expand Stage-1 scope, or accept F2/F3/Stage 1.

**F2a — point-in-time trade/quote correlation.** First establish and commit failing authority-derived public-seam proofs for the retained later-quote adversarial witness and related per-trade temporal/lineage cases. Only then repair the established trade-to-contemporaneous-quote selection and signed-flow correlation mechanism. Prove stable earlier-trade signs under later **quote-only** updates, lawful event/receipt/cutoff eligibility, multiple opposing trades, contract/version and ambiguity refusal, exact D015→D016/D120 arithmetic, original reviewer numeric witness, persisted direct-D and ultimate-R lineage, retry and recalculation. Create an exact **F2a Git checkpoint** with focused results and remaining work; **do not stop solely to request an intermediate reviewer round-trip**. This remains a substantive proof-first semantic unit, not licence for opportunistic F3 work.

**F2b — D064/D065 prerequisite and remaining observation-class reconciliation.** Next investigate the independently identified D064 raw R289 / K07 `P_SCORE` feature problem and D065 R284-event-to-D064-derived correlation against the exact accepted brief, catalogue, typed M00 projection, F1 census and implementation; also reconcile D017 co-reference and other genuinely applicable F2 per-observation classes. Do **not** assume that a raw-only D064 is impossible or that raw/derived occurrence IDs are interchangeable. First establish that existing authority and the admitted interface specify a lawful scoring input and event association. If they do, commit discriminating public-seam proofs **before** any minimal production repair, including positive, competing-event, missing/ambiguous, version/cutoff and lineage cases. If a mandatory law or representable interface is absent or contradictory, **stop `BLOCKED` immediately**, preserve the completed F2a checkpoint and return one exact authority question; do not invent an extractor, weaken the obligation, silently defer a required F2 prerequisite, or proceed to F3. Record an F2b Git checkpoint only for actually established closure.

**Consolidated F2 review boundary.** After both F2a and F2b pass their authorised proofs, reconcile the F1 class-to-edge ledger and outstanding F2 entries; run focused and necessary regression, architecture/type/lint and relevant database/public-seam checks with explicit non-runs. Freeze **one** clean full-Git F2 candidate and stop for **one** independent F2 review. Individual F2a/F2b commits are internal proof and implementation checkpoints, **not** separate review gates or permission to advance scope. The reviewer may accept F2 as a bounded engineering unit or return a class-wide REPAIR/BLOCKED disposition; it cannot declare Stage 1 accepted. **F3 is authorised only following this consolidated F2 acceptance.** Existing F3, F4 and Stage-1 final independent-acceptance obligations remain unchanged. A genuine unmet invariant always invokes the root stop law and overrides the batching preference.

#### F3 — contract-specific predecessor and grouped-aggregation closure

**Proposition:** Parent and grouped Stage-1 rows select all and only compatible exact predecessor instances; bucket, expiry, call/put, contract and temporal grouping do not collapse per-contract identities or silently reuse mismatched predecessors.

The Worker will preserve and re-prove the earlier D109/D170 contract-specific predecessor behaviour and author independent public-seam proofs for the **previously unassessed** D120/D091→D121 and D120/D085→D122 grouped paths with multiple distinct contracts/buckets, conflicting or absent members, correct signed totals, absence refusal and reconstructable lineage. Apply the same authority-derived proof method to other F1-classified contract/group mechanisms. Commit proofs before any bounded production repair and record an F3 checkpoint. Do not implement Stage-2 predecessor kernels merely to satisfy a deferred dependency.

#### F4 — class reconciliation, full Stage-1 revalidation and single review candidate

**Proposition:** The F1 complete census has no unaccounted Stage-1 relationship class or implementation discrepancy; every applicable class is supported by discriminating production/public-seam positive and adversarial evidence, and the existing Stage-1 acceptance requirements are independently reviewable against one exact candidate.

The Worker will:

- reconcile all F1 classified relationships and discrepancy entries to F2/F3 proofs or documented still-`BLOCKED` authority; no open material gap can be silently labelled accepted;
- use the F1 class-to-edge map to show mechanism coverage across the **entire authoritative Stage-1 population**, including previously reviewed graph, raw/derived, history, version, temporal, subject, contract, grouped, basket and context relations; distinguish exhaustive static/accounting checks from representative adversarial runtime evidence;
- preserve the reviewer’s deliberately failing D016/D120 reproducer as regression proof and prove it now passes without changing the expected canonical result or masking the public seam; preserve D109/D170 and prior regression witnesses;
- rerun relevant existing tests plus necessary architecture, type, lint, PostgreSQL boundary/durability and runtime/public-seam checks in a declared reproducible environment; report unavailable or unexecuted checks explicitly, not as `PASS`;
- enforce the unchanged Stage-1 acceptance population: **174** exact Stage-1 kernel implementations/proofs, **144** Stage-1-closed rows publicly reachable end to end, and **30** cross-stage rows with own-kernel proof and lawful public fail-closed behaviour until Stage 2; preserve all mathematics, accepted edges, units, context conjunctions and prior Leaf 1–3 obligations;
- freeze one exact Stage-1 candidate (Git HEAD and tree, clean status, evidence identities, commands/logs and unresolved register) and stop for independent review. Stage-1 `PASS` is available only from this independent review on its full acceptance proposition, not from F1 or individual successful tests.

**Scope/authority lock for F1–F4:** No edits to `GUARDRAILS.md`, `AGENTS.md`, accepted brief, normative CSV, source-ownership boundaries or package version `1.0.0`. No unrelated architectural redesign, M00 table access, later-module implementation, fabricated defaults, weaker acceptance criteria or blanket reimplementation. Any discovered authority conflict/semantic under-specification is returned `BLOCKED` with the exact contradictory/missing source, not worked around. This amendment is a finite, evidence-first repair sequence, not a new normative definition of relationships.

## 5. Stage 2 — advanced model, scenario, risk, attribution and evaluation kernels

### Proposition

Every authoritative catalogue row bound to `K09_SURFACE_DENSITY` through `K15_EVALUATION` is calculated using the fixed accepted model/convention/context laws and remains calculation truth rather than an external action.

### Required proof/implementation scope

Cover the accepted surface/density, conditional-distribution/scenario, exposure/stress, execution-aware value, expected-risk utility, path-attribution and evaluation semantics, including required option/P&L/evaluation conventions, candidate/live-position contexts, no-look-ahead and cost double-counting exclusion. Implement the normative Stage-2 predecessors required by the 30 cross-stage Stage-1 rows and prove those previously deferred cross-stage graph connections become lawfully reachable without changing their Stage-1 kernel semantics.

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
