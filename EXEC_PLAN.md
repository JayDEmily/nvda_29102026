# ExecPlan — U06 A00 Construction and Governed Sequential Composition

## Status

**ACTIVE — PROGRAMME OWNER APPROVED FOR U06 EXECUTION ON 2026-09-27.**

This document is the narrow successor to the completed U04→U05 ExecPlan.

The Programme Owner explicitly accepted this plan on 2026-09-27 and authorised its installation as the root `EXEC_PLAN.md`. It does the following:

1. supersedes the completed U05 ExecPlan as the single active planning authority;
2. preserves the completed U05 ExecPlan in ordinary Git history as historical execution evidence;
3. authorises **IWO-U06 only**;
4. stops after accepted U06 promotion.

It does not authorise a hypothetical U07, VI-14 closure work, final packaging, provider/network integration, downstream behaviour, or any other later tranche.

---

## 1. Fixed starting boundary

The fixed starting repository state for this plan is the promoted U05 `main` lineage:

- `main` / current repository HEAD at plan drafting: `90156998e3f70fc6c0afa54c73b577ccec4e47b6`;
- tree: `e186da49135c67f19ae78e201c9af6e14a064de2`;
- accepted U05 production candidate: `2bdbedff62307ecfaf6186f9c12814fb662c11a7`;
- accepted U05 candidate tree: `e15e743e006217a8a3a6313011caf82265a679cf`;
- fresh independent U05 Tester `PASS` preserved at `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8`;
- U01 through U05 are the accepted active Raw Signal Occurrence Truth implementation lineage.

U01–U05 meaning is not reopened by this plan.

The completed U05 ExecPlan, its Stage 1–7 execution records, failed candidate `249fb5f…`, accepted replacement candidate `2bdbedf…`, Tester evidence and promotion evidence remain historical/current evidence according to their existing status. They are not execution stages of U06.

---

## 2. Governing authority

This plan operationalises already-authorised work only. It does not create new Raw Signal semantics.

Authority remains, in order:

1. current explicit Programme Owner instruction;
2. `GUARDRAILS.md`;
3. applicable `AGENTS.md` / `AGENTS.override.md`;
4. this ExecPlan;
5. accepted task/normative/architecture authority;
6. accepted proof obligations and proof artefacts;
7. implementation/source/configuration;
8. historical evidence.

The already-authorised engineering obligation is:

> **IWO-U06 — A00 construction and governed sequential composition**

from `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`.

Its accepted purpose is:

> prove and implement the only authorised cross-owner runtime composition.

Its primary proof obligations are:

- `IA17-PROD-013` — governed sequential end-to-end A00 → typed M00 composition;
- `IA17-ARCH-004` — declared runtime edge is A00 → M00 through the public boundary and the active M graph remains acyclic;
- `IA17-ARCH-005` — typed command/read facets remain restricted to the declared A00/M00 public boundary;
- `IA17-ARCH-006` — composition selects only lawfully admitted active objects/forms/boundaries and does not escalate product status.

The accepted U06 product-proof family already exists at:

`tests/product/raw_signal/test_u06_a00_composition.py`

with product-proof registration in:

`config/product_proof/families.yaml`

Those tests are evidence derived from authority. They do not supersede the IWO/BICP or create new meaning.

---

## 3. Current implementation observation

At the fixed starting boundary:

- architecture already declares the runtime owner edge exactly `A00 -> M00`;
- A00 is already permitted to depend on `M00`;
- M00 is an active admitted Raw Signal Occurrence Truth owner;
- the U05 PostgreSQL mechanism and durable M00 public seam are accepted;
- `src/nvda_desk/composition/__init__.py` contains the existing composition-plan scaffold but does **not** yet provide the U06 production `create_application` path required by the accepted U06 proof;
- the existing U06 physical proof therefore describes the implementation target rather than an already-completed U06 implementation.

U06 is consequently a bounded composition/integration unit. It is not authority to redesign M00 or add another semantic owner.

---

## 4. U06 terminal proposition

U06 is acceptable only when one exact committed candidate establishes the following complete proposition:

> A00 lawfully constructs the admitted Raw Signal Occurrence Truth runtime composition, including the non-owning PostgreSQL technical mechanism and the admitted M00 owner; A00 owns only construction, source/scheduler translation and top-level lifecycle; all Raw Signal semantic commands and reads pass through the typed M00 public seam; the declared runtime owner edge remains exactly A00 → M00; and a governed sequential path can carry authorised inputs and exact M00-returned identities through policy registration, capture realisation, observation admission, receipt-evidence derivation, assessment append and referential readback without A00 calculating Raw Signal outcomes, bypassing M00 private state/persistence, reversing the dependency, or activating P01, K01 or downstream consumers.

The terminal proposition must be established through both boundary-focused proof and a real production composition path. A spy-only delegation test does not by itself establish that the default A00 production construction path composes the accepted PostgreSQL/M00 implementation correctly.

---

## 5. Explicit non-goals

U06 does **not** authorise or claim:

- new Raw Signal semantic meaning beyond accepted U01–U05;
- changes to M00 persistence semantics for convenience;
- a second semantic owner;
- M00 → A00 dependency;
- direct A00 access to M00 private state, SQL tables, repository/store internals or the PostgreSQL adapter as a semantic mutation surface;
- P01/DMPV3 activation;
- K01 selection or activation;
- provider/API/network integration;
- authoritative replay or re-execution;
- live external effects/accounts;
- downstream business consumers;
- packet-carrier semantics;
- finality, exact counts, membership, outage semantics or provider-event absence claims;
- retention/deletion policy;
- RTO/RPO, throughput, latency or SLA claims;
- PostgreSQL partitioning or pooling;
- new performance index policy;
- final distribution naming/version metadata;
- U07 or any later implementation unit;
- VI-14/VI-15/VI-16/VI-17/VI-18 closure work.

Remaining Unknowns carried by the accepted IWO remain unknown unless separately authorised. Implementation convenience may not resolve them.

---

## 6. Execution model

U06 will be executed as **six natural stages**.

The stages are intentionally larger than individual methods/tests but smaller than the complete U06 unit. Each implementation stage has one coherent architectural proposition and ends at a clean Git resumability boundary.

A stage commit is not acceptance. U06 receives semantic acceptance only after the exact frozen candidate passes fresh independent Tester review and is promoted with preserved ancestry.

During Stages 1–4:

- ordinary work occurs on one U06 work lineage;
- `main` remains the accepted U05 baseline;
- meaningful intermediate states are committed;
- evidence must name the exact state it describes;
- do not allow multiple substantial stages to accumulate as one dirty overlay;
- stop after each stage boundary before beginning the next stage unless the Programme Owner has explicitly authorised continued autonomous execution.

### Stage 1 — A00 production construction and lifecycle boundary

**Purpose:** implement the minimum truthful A00 production construction boundary before adding the sequential use case.

This stage begins by tracing the accepted U06 construction obligations against the realised U05 production surfaces. The Worker must establish, rather than assume:

- the current public M00 construction seam;
- the accepted technical PostgreSQL construction seam;
- which configuration/technical values A00 must receive to construct the production composition;
- which resources, if any, actually require A00-owned startup/shutdown handling;
- the smallest public A00 application object required for later governed composition.

Then implement the bounded production construction path, expected to include the accepted `create_application` symbol required by the physical proof.

The construction must satisfy all of the following:

- A00 constructs/injects the non-owning PostgreSQL technical dependency required by accepted U05;
- A00 constructs the admitted M00 owner through M00's public construction seam;
- A00 may expose bounded dependency injection needed for proof, but the production default path must construct the real admitted dependencies;
- dependency injection must not create a caller-accessible semantic bypass around M00;
- A00 does not import M00 private implementation modules as a semantic API;
- A00 does not decide policy, capture, observation, relation or assessment meaning;
- A00 owns only construction and whatever top-level lifecycle the admitted mechanisms actually require;
- no artificial pooling, recovery, scheduler, network or shutdown semantics are invented merely to make the application object look complete.

Architecture proof must continue to establish:

- declared owner edge exactly `A00 -> M00`;
- no `M00 -> A00` edge;
- A00 composition imports M00 only through the declared public seam, except for any separately admitted non-semantic technical constructor whose use is already authorised and cannot lawfully be reached through that seam;
- no P01/K01/downstream runtime edge appears.

**Required proof at this stage:** focused A00 construction/architecture proof plus applicable existing architecture/static checks. Do not require the full sequential business path to be green yet if that behaviour has not been implemented.

**Stage exit:** one clean committed tree contains a truthful production A00 construction/lifecycle boundary, with no Raw Signal semantic decisions in A00 and no unadmitted dependency edge. Commit the exact implementation/proof state before Stage 2.

### Stage 2 — Governed typed delegation and semantic dataflow

**Purpose:** implement the actual A00 → M00 sequential orchestration while preserving M00 semantic ownership.

Implement the governed sequence through M00's typed public command/read facets only:

1. register the capture-scope policy;
2. realise the scheduled capture occurrence;
3. admit the raw observation occurrence;
4. derive the receipt-evidence relation;
5. append the receipt-presence assessment;
6. perform the required referential readback.

This is orchestration, not semantic reimplementation.

The stage must prove exact dataflow, not merely method order:

- authoritative A00 input values are passed to the correct M00 command positions;
- capture realisation is consistent with the exact policy identity/version accepted by policy registration;
- a caller-supplied policy reference inconsistent with the registered policy fails before capture realisation;
- the exact capture identity returned by M00 flows into later relation/assessment commands where required;
- the exact observation identity returned by M00 flows into relation derivation and referential readback where required;
- the effective policy reference used by later operations comes from the authoritative M00 result/path required by the accepted proof;
- the exact evidence-as-of timestamp and supersession input flow into assessment append;
- A00 returns/propagates the exact semantic objects returned by M00 rather than recreating them;
- A00 never chooses `zero_received`, `one_or_more_received`, `unknown_not_established`, eligibility, supersession meaning or any other M00-owned outcome.

Proof may use an opaque spy owner/factory to discriminate delegation and object/argument identity, because that is the accepted U06 proof technique. The spy may observe calls only; it must not become an alternate Raw Signal semantic implementation.

**Required proof at this stage:** the accepted U06 delegation/dataflow family must pass for the implemented path, together with applicable architecture/static checks and predecessor regression needed to show the change did not disturb accepted U01–U05 behaviour.

**Stage exit:** one clean committed tree proves exact typed A00→M00 sequential delegation and dataflow without semantic duplication or private bypass. Commit before Stage 3.

### Stage 3 — Real production PostgreSQL/M00 sequential composition

**Purpose:** prove that the production A00 construction path and the accepted M00/PostgreSQL implementation actually compose end-to-end, rather than relying solely on spy substitution.

Using the authorised real PostgreSQL proof environment and the production A00 factory:

- construct the application through the default production path;
- establish only the technical configuration required by the accepted implementation;
- execute one representative governed sequential Raw Signal path using accepted v1 facts;
- verify policy registration, capture, observation, relation, assessment and referential readback all pass through the realised M00 owner;
- verify durable facts can be read back through the public owner/application path as required by the sequential composition proposition;
- verify the result preserves the accepted U05 transaction/durability behaviour without A00 acquiring transaction semantics;
- verify application teardown/lifecycle does not fabricate semantic success or mutate M00 facts;
- verify no external provider/network/downstream capability is needed or silently activated.

The stage must specifically discriminate these false positives:

- the injected spy path works but the production default factory does not;
- A00 builds an in-memory/non-durable substitute instead of the accepted PostgreSQL-backed M00 path;
- A00 reaches PostgreSQL or repository mutation directly instead of using M00 commands;
- correct call order hides incorrect identity/reference propagation;
- composition success depends on an unadmitted P01/K01/downstream object;
- production construction widens the public capability graph to expose direct persistence mutation.

Do not reopen U05 durability design. If real composition exposes an actual U05 regression, stop at that first unmet invariant and route the defect according to repository failure law; do not patch around it inside A00.

**Required proof at this stage:** real PostgreSQL production-composition discriminator(s), the accepted U06 proof family, applicable U01–U05 regressions, and architecture/static proof relevant to the modified surface.

**Stage exit:** one clean committed tree establishes that the actual production A00 factory composes the accepted PostgreSQL-backed M00 owner and executes the authorised sequential path through public boundaries only. Commit before Stage 4.

### Stage 4 — Whole-U06 adversarial closure and candidate freeze

**Purpose:** determine whether Stages 1–3 form one coherent U06 implementation and freeze one exact Worker candidate for independent review.

This stage adds no new product capability. It closes the complete U06 proposition.

Challenge the realised implementation against the accepted authority:

- `IA17-PROD-013` sequential end-to-end proposition;
- `IA17-ARCH-004` exact runtime dependency direction and acyclicity;
- `IA17-ARCH-005` typed public seam / no private bypass;
- `IA17-ARCH-006` lawful composition of admitted active objects only;
- the U06 portions of BC-014/BC-015 adversarial proof already embodied in the accepted physical proof;
- predecessor U01–U05 conservation.

Perform a mandatory source-level logic trace through:

`A00 construction -> technical persistence construction -> M00 owner construction -> commands/reads -> sequential orchestration -> returned application result -> lifecycle/teardown`

For every step, identify who owns the decision and where each material input/result came from.

The trace must independently challenge at least:

- whether A00 contains any Raw Signal outcome/eligibility/supersession logic;
- whether A00 can bypass M00 into private state/table/repository/adapter mutation;
- whether M00 acquires a reverse dependency on A00;
- whether application construction can select an unadmitted owner/mechanism;
- whether exact registered-policy/capture/observation/effective-policy identities propagate correctly;
- whether the production default path differs materially from the path proved with dependency substitution;
- whether lifecycle handling adds semantic side effects beyond authority;
- whether the public object graph exposes a new persistence mutation capability under the already-accepted bounded public-seam proof law;
- whether P01/K01/packet/downstream capability has entered the runtime path.

Run the complete proof axes required for the U06 claim independently. Green product proof must not substitute for architecture proof or vice versa.

If all required propositions are established, freeze one exact clean commit/tree as the **U06 Worker candidate**. No evidence/handoff edit after candidate freeze may modify candidate production/test/config/dependency bytes.

**Stage exit:** complete Worker evidence establishes the U06 terminal proposition for one exact immutable candidate; predecessor regressions and required architecture/static/product axes are green; code trace finds no unresolved authority or ownership defect; worktree and evidence agree exactly.

### Stage 5 — Fresh independent Tester review

**Purpose:** independently challenge the exact frozen U06 candidate.

The fresh Tester receives:

- current governing authority;
- exact U06 IWO/BICP obligations;
- exact accepted U01–U05 predecessor lineage needed for context;
- exact U06 candidate commit/tree/diff;
- Worker evidence;
- accepted U06 physical proof;
- relevant historical U06 proof-review findings as risk evidence, not as current authority.

The Tester must inspect realised source paths as well as execute proof.

At minimum independently challenge:

- production A00 construction uses the admitted M00/PostgreSQL path;
- exact owner edge is A00 → M00 only;
- A00 calls only the typed M00 command/read seam for Raw Signal meaning;
- no A00 semantic calculation or private persistence bypass exists;
- material policy/capture/observation/assessment identities and timestamps propagate correctly;
- the real production path, not only a spy fixture, satisfies the sequential proposition;
- no P01/K01/downstream/unadmitted runtime capability appears;
- applicable predecessor, architecture, static and real-PostgreSQL proof remains green.

Tester disposition is exactly one of:

- `PASS`;
- `FAIL / RETURN_TO_WORKER`;
- `BLOCKED`.

A failure returns only the bounded U06 defect/class to the Worker. Repair creates a new exact candidate followed by fresh independent re-review. A failed candidate is never silently amended in place or promoted.

**Stage exit:** fresh independent Tester `PASS` on one exact candidate, or stop on the first material failure/blocker.

### Stage 6 — Promotion and U06 close-out

Only after fresh Tester `PASS`:

- preserve the Tester disposition in ordinary Git history;
- integrate the accepted U06 work lineage into `main` with preserved ancestry;
- record exact candidate, review and promotion identities;
- update current-state/handoff authority to describe the promoted repository truth;
- verify no production/test/config/dependency bytes changed after the independently accepted candidate except where separately reviewed and explicitly re-tested;
- verify the final worktree is clean and Git integrity/readback checks pass;
- stop.

This plan ends at accepted/promoted U06.

No U07 begins under this plan. VI-14 aggregate/interaction closure, VI-15 packaging, VI-16 whole-BICP review, VI-17 provenance audit and VI-18 final bounded-implementation freeze remain outside this plan and require the then-current governing authority.

---

## 7. Git and resumability discipline

During U06:

- `main` remains the accepted U05 baseline until U06 receives independent Tester acceptance;
- ordinary implementation occurs on one U06 work lineage;
- each substantial Stage 1–4 boundary receives a normal Git commit;
- stage commits are resumability/history points, not semantic acceptance;
- do not squash/rebase/history-rewrite the U06 lineage for tidiness;
- do not accumulate multiple stages as one large dirty worktree;
- handoffs name exact commit/tree and whether the worktree is clean;
- candidate freeze is one exact immutable commit/tree;
- Tester evidence and promotion records are separate from the candidate where possible;
- failed candidates and repair lineages remain recoverable in Git history.

If a governance correction is genuinely required mid-unit, make it explicit and separate. Do not continuously redesign the workflow underneath active dirty implementation.

---

## 8. Mutation discipline

Expected lawful U06 implementation jurisdiction is bounded by the accepted IWO and realised need, principally:

- `src/nvda_desk/composition/**` for A00-owned construction, translation, sequential orchestration and lifecycle;
- U06-specific product proof under `tests/product/raw_signal/**` where the accepted proof requires implementation-coupled repair/extension;
- product-proof descriptions/config only where needed to remain truthful to the realised proof;
- architecture proof/config only if required to preserve the already-authorised A00→M00 claim truthfully;
- U06 evidence/handoff records.

M00 production source under `src/nvda_desk/raw_signal_occurrence_truth/**` is **not presumed mutable merely because U06 consumes it**. A change there requires a demonstrated U06 dependency defect that cannot lawfully be resolved at the A00 composition boundary and must not reopen accepted U01–U05 meaning.

Do not mutate:

- `GUARDRAILS.md`;
- accepted BICP/IWO/normative meaning;
- accepted proof obligations merely to make implementation green;
- P01/K01/downstream surfaces;
- unrelated architecture/kernel state.

Make the smallest change that establishes the authorised U06 proposition.

---

## 9. Evidence discipline

For each Stage 1–4 work boundary, evidence must distinguish:

- **VERIFIED** — actually established by identified source/command/test/trace;
- **UNPROVED** — required axis not yet established;
- **BLOCKED** — required axis cannot currently be established for a stated reason;
- **NOT IN SCOPE** — proposition not required by the current stage.

Each material evidence record must include:

- exact commit/tree;
- changed paths;
- proposition under test;
- proof environment where material;
- commands/checks actually run;
- observed result counts where applicable;
- known limitations/non-claims;
- next lawful action.

Do not call U06 complete because the pre-existing U06 spy proof is green. The production construction path, real composition path, architecture boundary and independent review are separate propositions.

---

## 10. Mandatory stop conditions

Stop dependent U06 execution at the first occurrence of any of the following:

- the exact accepted U05 baseline or U06 authority cannot be established;
- the realised M identity/public seam differs materially from the accepted U06 projection;
- A00 composition requires a new Raw Signal semantic decision;
- A00 requires direct private-state/table/repository mutation to make the sequence work;
- M00 would need to depend on A00;
- a P01/K01/downstream/provider/network capability becomes required;
- a Remaining Unknown must be resolved to proceed;
- the production A00 path cannot lawfully construct the accepted PostgreSQL-backed M00 owner;
- real PostgreSQL proof required for the asserted composition proposition cannot run and the proposition cannot lawfully be narrowed;
- predecessor U01–U05 accepted semantics regress;
- product proof or architecture proof is materially red/incomplete for a required U06 proposition;
- source logic trace finds A00-owned Raw Signal semantic behaviour or capability bypass;
- evidence/handoff state disagrees with the actual source/Git state;
- fresh independent Tester reports an unresolved material finding.

Preserve the last exact proved commit and first unmet invariant. Do not continue into later stages merely to accumulate progress.

---

## 11. Definition of U06 done

U06 is done only when all of the following are true for one exact independently reviewed candidate:

1. U01–U05 accepted semantics remain conserved;
2. production `create_application` or equivalent accepted A00 construction path exists and truthfully constructs the admitted runtime composition;
3. A00 constructs/injects the accepted non-owning PostgreSQL technical mechanism and admitted M00 owner without becoming a semantic owner;
4. runtime owner edge remains exactly `A00 -> M00` and active owner dependencies remain lawful/acyclic;
5. M00 has no reverse A00 dependency;
6. Raw Signal commands/reads cross only the declared typed M00 public boundary;
7. A00 does not bypass M00 through private state/table/repository/persistence mutation;
8. sequential policy → capture → observation → relation → assessment → referential-read composition is exercised through the production path;
9. material identities, policy references, timestamps and supersession inputs propagate from exact authorised inputs or preceding M00 results as required;
10. caller policy-reference disagreement with registered policy fails closed before capture progression;
11. A00 returns/propagates M00-owned semantic results rather than recreating outcomes;
12. A00 contains no Raw Signal eligibility/outcome/supersession decision logic;
13. the production default composition path is proved in addition to any spy/dependency-substitution path;
14. required real PostgreSQL composition evidence passes;
15. no P01, K01, packet carrier, provider/network capability or downstream consumer is activated;
16. applicable U06 product proof and architecture/static proof pass independently;
17. a source-level logic trace finds no unresolved ownership, dependency or bypass defect;
18. candidate/evidence/handoff state is exact, clean and Git-resumable;
19. a fresh independent Tester returns `PASS` on that exact candidate;
20. accepted promotion preserves ancestry and records exact final identities.

Anything less is an intermediate U06 work state, not U06 acceptance.

---

## 12. Plan retirement and next boundary

Upon explicit acceptance of this draft as the new root `EXEC_PLAN.md`:

- the current completed U04→U05 ExecPlan becomes superseded historical planning evidence;
- it is retained in Git history and is not destructively removed;
- the new plan becomes the single active planning authority for U06 execution;
- current-state/handoff records should be updated to identify U06 Stage 1 as the next authorised Worker action only when execution is actually routed.

After Stage 6 promotion, this U06 ExecPlan is complete and must stop.

There is no authorised U07 in the accepted IWO. Any later tranche requires a new explicitly accepted governing plan derived from the then-current authority.
