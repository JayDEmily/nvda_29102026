# NVDA V2 — Understanding, reuse assessment and implementation planning brief

Date: 14 October 2026 — Australia/Melbourne  
Version: 1  
Status: Standalone commissioning brief for investigation and implementation planning; future production execution remains subject to the specific authority described below.

## 1. Read this first: the objective

The programme owner has changed the intended organisation of the NVDA system. Workbook V2 is the first expression of that change. Your task is to understand it, establish what the unfinished original M01 engineering actually delivers, and produce a practical, evidence-grounded route from that existing work to the V2 design.

There are two distinct questions to answer:

1. Against the original M01 brief, what has actually been implemented, what has been demonstrated, and what remains unfinished?
2. Against the V2 design, what existing work can serve M01-1 and the downstream modules, what changes are necessary, and how will the resulting capabilities be implemented and accepted?

Do not let the original implementation schedule determine the new responsibility boundaries. Equally, do not treat the new workbook as proof that those boundaries have already been implemented or admitted into production.

The intended result is a stable shared foundation and independently changeable downstream modules. Preserve useful engineering, original signal identities, accepted mathematics and historical evidence. Do not assume that preserving engineering means retaining its existing ownership or dependency structure.

## 2. Why the spreadsheet was reset

The old label “derived signals” did not distinguish sufficiently between descriptive market measurements, model-dependent calculations, portfolio economics and policy or strategy calculations. Deterministic computability alone does not establish that a calculation is strategy-independent.

The owner therefore reset the workbook to make responsibility boundaries explicit before continuing development. This is an architectural change of direction, not merely a presentation change or a request to rename M01.

The V2 intent is:

| Responsibility | Intended meaning | Required independence |
|---|---|---|
| M00 | Preserve authorised raw observations and records, native values, identities, units, timestamps, provenance and history. Raw records are not exclusively market quotes; they also include other authorised record types. | Preserve its accepted ownership and typed public access. Do not move derived mathematical transformations into M00 for convenience. |
| M01-1 | Reusable, precisely defined, strategy-independent descriptive market/source-time calculations, including qualifying statistical measurements. | Its inputs and calculation meaning must not depend on downstream strategy, candidate, portfolio or order-intent choices. Results must be reproducible, versioned and traceable. |
| M02–M31 | The proposed downstream responsibility groups, with their own relevant calculations, assumptions and configuration. They are not all necessarily complete trading strategies. | Independently executable, configurable, replaceable and testable peers. No runtime or private-data dependency on another M02–M31 peer. |

Fixed non-strategy measurement conventions are permitted in M01-1. A five-day measurement and a ten-day measurement can have separately defined meanings. A strategy must not silently redefine an existing foundational result by changing its sampling rule, coefficient or interpretation. Complexity, multiple inputs, regression or use of a versioned parameter object does not alone decide eligibility; examine the actual meaning and full input chain.

### 2.1 The downstream self-sufficiency rule

All downstream peers may consume lawful shared M00 and M01-1 outputs. They must not obtain strategy-dependent intermediate results by calling another downstream peer, importing its private implementation or reading its private data.

Where two peers need equivalent strategy-dependent intermediate arithmetic, each contains and tests its own implementation, including the intermediate chain necessary to reach lawful foundational inputs. A change in one local implementation must not implicitly change another peer.

This deliberate duplication does not create a second canonical Dxxx signal. Private intermediates need local identities, configuration/version handling and lineage. Preserve the single canonical identity and proposed owner of each original D signal unless the owner explicitly approves a change.

Example of the design rule, not a claim about any particular existing module: if module A needs an intermediate calculation historically associated with module B, A must contain the required strategy-dependent intermediate chain itself. It must not wait for B to execute. Qualifying M01-1 results remain shared rather than copied into A and B.

Working module numbers are identities, not an execution sequence. Historical D-to-D edges in the original M01 graph do not authorise runtime edges between V2 peers.

## 3. Immediate scope and authority boundary

The immediate assignment is understanding, source-based assessment and concrete implementation planning. Proceed through that work without requiring permission for routine reading or recoverable analysis steps.

During this assignment:

- Do not run unit, integration, database, performance, lint or type-check suites. Do not run application code to demonstrate behaviour. Read existing test source and historical results as evidence only.
- Read-only document/workbook parsing, source inspection, Git inspection and identity/hash checks are allowed. Static inventories may assist reading but must not replace semantic analysis.
- Do not alter production code, tests, schemas, runtime configuration, workbook allocations, accepted calculation definitions, module ownership or governing repository files.
- Produce the assessment and proposed implementation plan as separate deliverables. Do not install the proposed plan as the active EXEC_PLAN.md merely because it has been written.
- Planning must include eventual testing and independent acceptance. The present prohibition on execution is not permission to omit those obligations from implementation.
- Do not implement M01-1, resume the old M01 repair programme or implement downstream modules merely because an implementation roadmap appears in this brief.

The owner's current request authorises preparation of this brief. When supplied as the next worker's assignment, its immediate scope is the investigation and planning above. Future production changes require applicable explicit programme authority. Before seeking that authority, finish the available investigation and present exact proposed changes, affected boundaries, unresolved decisions and acceptance conditions. If existing explicit authority already covers a proposed action, identify it rather than asking again.

Current explicit user directions take precedence. Read GUARDRAILS.md in full, applicable AGENTS.md/AGENTS.override.md and the active governing plan before substantive work, and follow their applicable requirements. Do not use this brief to silently resolve an authority conflict. Stop dependent work at a genuine missing or contradictory required authority and state the exact gap.

## 4. Source package and evidence hierarchy

This brief is standalone in its explanation of intent and method. It is not a substitute for the repository and source evidence. Give the next worker this brief and the two packages below. If unavailable, locate the exact packages through available files; do not pretend that this brief supplies their contents.

### 4.1 Primary repository package

- Filename: `NVDA_WORKBOOK_V2_PASS08_SELF_SUFFICIENCY_CLARIFIED_FULL_GIT_20261014.tar(2).gz`
- SHA-256 of supplied archive bytes: `0b5a459e6620d617c539bd8aa3f4830fcc176c9ecd7440484adc983d85b29429`
- Library identity: `libfile_731274619d288191bc9bc1788675f988`
- Archive repository root: `repository/`
- The archived `.git/HEAD` and loose branch reference identify branch `work/workbook-v2-pass01-guardrails-method-20261014` at `514040e0d32cf2efd0629c08cdf056b4c8b3f766`.

Those reference bytes were inspected when preparing this brief. They do not establish a clean worktree, full repository integrity or programme acceptance. Resolve and inspect the actual Git state on worker entry. Do not assume a newer filename, later timestamp or different archive is equivalent. If another baseline is supplied, reconcile the difference before relying on old findings.

### 4.2 Supporting prior audit package

- Filename: `NVDA_M01_M011_SEMANTIC_AUDIT_20261014.tar(1).gz`
- SHA-256: `488e9462f9189b97ab4609bda9d2164e15c09ae980b8eb6296b7b8b089523afc`
- Library identity: `libfile_4aa1f1a9881c819180fcfb0a9e4c632b`
- Report: `M01_TO_M01_1_SEMANTIC_REUSE_AUDIT.md`
- Crosswalk: `M01_M011_209_SIGNAL_SEMANTIC_AUDIT.csv`

Treat this audit as a navigation aid and set of claims to examine. It is not governing authority, an independent acceptance certificate or proof of each row's correctness.

### 4.3 Required reading inside the repository

Read the following in full, then follow the evidence they identify:

1. `GUARDRAILS.md`, root `AGENTS.md`, applicable nested instructions and `EXEC_PLAN.md`.
2. `handoff/m01_completion/AUTHORITY_INDEX.md`.
3. `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` and the effective `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` in that directory.
4. Applicable accepted clarifications and corrections in that authority directory. Read the complete index: early catalogue hashes there are historical and later authorised amendments change the effective authority.
5. The original workbook in that directory: `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`.
6. `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS08.xlsx`, including the original source sheets, `00_Guardrails & Method`, `M01-1 Derived Raw`, both M02–M31 registers and individual module sheets relevant to their allocations.
7. `handoff/workbook_v2/decisions/ADR_WBV2_001_MODULE_RESPONSIBILITY_CLASSIFICATION.md`.
8. `handoff/workbook_v2/decisions/ADR_WBV2_002_DOWNSTREAM_MODULES_LOCAL_DUPLICATION.md`.
9. `handoff/workbook_v2/pass08_independence_clarification/PASS08_CLARIFICATION.md`.
10. Under `handoff/workbook_v2/reviews/m01_1_boundary_20261014/`, the full `M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv`; under `handoff/workbook_v2/pass06_modules/`, the module register, signal allocations and historical cross-group reference inventory.

Relevant architecture laws include the actual files under `docs/architecture/` concerning ownership, public seams, dependencies, extension/retirement, implementation authority and test/promotion. Read those needed for the concrete migration proposals before recommending structural changes.

Starting implementation locations are `src/nvda_desk/derived_signal_calculation_truth/api.py`, `_stage1.py`, `_catalogue.py`, `_postgres.py`, `_financial_policy.py` and its runtime catalogue. Follow actual call paths, M00 projections, persistence definitions and relevant test source from there. These filenames are navigation, not a presumption of correct behaviour.

Use older project archives only where an identified authority or historical question requires them. Do not indiscriminately combine historical trees or make an older archive the active baseline.

## 5. Required reasoning method

Work from meaning to implementation, then to evidence:

1. What is the calculation intended to represent?
2. What exact accepted definition, equation, convention and input contract establish that meaning?
3. Does that meaning qualify for the proposed V2 responsibility, including its complete dependency chain?
4. What does the actual implementation do through the public path?
5. What existing evidence establishes each part of that behaviour, and what does it leave unproved?
6. What exact reuse, repair, separation, new implementation or authority decision is necessary?

Read the complete relevant functions and their callers/helpers. A dispatcher entry, symbol name, catalogue row or search hit is a starting point. Trace selection, correlation, history, units, versions, context, calculation, result construction and persistence far enough to establish the claim.

Separate VERIFIED, INFERRED, UNKNOWN, BLOCKED and PROPOSED where material. Distinguish a missing implementation from an implementation defect, missing evidence, unresolved source contract, unresolved authority and unaccepted architecture. These require different remedies.

Do not make a numerical completion percentage from path counts. Do not assume an old test remains applicable after ownership or meaning changes; explain the proposition it establishes. Conversely, retain valuable existing evidence where its scope and provenance justify reuse.

## 6. Investigation work packages

These are an ordered investigation sequence, not newly admitted production gates. Complete each available step and carry the findings forward. Do not repeatedly ask whether to continue when the next step is already in scope.

### A. Establish the baseline and articulate the change

Record the actual archive/Git identities, working-tree condition, governing documents and effective authority amendments. Read the V2 decisions alongside the original brief.

Explain in plain language why the old M01 responsibility differs from M01-1; why old Stage 1 is not synonymous with M01-1; and why downstream self-sufficiency requires more than moving functions between folders.

Output: a short intent and authority statement, an evidence index and an explicit distinction between current production responsibility and approved V2 design direction. Do not stop at this restatement; continue into the assessment.

### B. Reconcile the complete original population with V2

Account for every original D001–D209 identity exactly once in the canonical crosswalk. Compare original workbook concepts, effective normative definitions and V2 proposed allocations. Preserve differences rather than silently merging them.

Read all relevant source fields, including blanks, notes and qualification flags. Determine full dependency closure, including external typed context and versioned configuration; direct R/D lists alone may not expose strategy dependence.

Do not reclassify signals because a category looks inconvenient. Where exact evidence challenges a V2 allocation, document the issue and bounded proposed decision while keeping the present allocation separately visible.

Output: a complete identity and responsibility crosswalk with no unexplained omissions or duplicate canonical owners. Population reconciliation is not semantic completion.

### C. Establish actual original-M01 implementation progress

For each original calculation, identify its accepted requirement, actual production path or absence, dependency availability and existing evidence. Read the relevant historical repairs and reviewer findings before calling a defect current or resolved.

State separately: own-kernel availability, public graph reachability, source-contract readiness, persistence support, historical test evidence and independent acceptance. Where no implementation exists, record the search/call-path evidence supporting absence.

Output: an account of what remains against the original brief, including old Stage-1/Stage-2 relationships, without recommending completion of obsolete scope merely to satisfy historical scheduling.

### D. Assess M01-1 readiness and reusable engineering

For every proposed M01-1 calculation, establish whether its meaning and full input chain satisfy the V2 rules. Assess measurement conventions individually, including permissible values, selection/sampling, version changes and who may select them.

Inspect both numerical functions and supporting infrastructure: admitted M00 ingress, graph evaluation, history/identity selection, configuration, lineage, public API, persistence and refusal behaviour. Determine what can be retained and what must change to establish a separate responsibility.

Use the following reuse dispositions with supporting evidence:

- `REUSE_AS_IS_CANDIDATE`: source review supports semantic fit without changing that component; integration and acceptance evidence may still be needed.
- `REUSE_WITH_SEPARATION`: existing mathematics fits, but ownership, dependencies, interface or persistence requires adaptation.
- `REPAIR_REQUIRED`: a specific discrepancy is established; cite required and actual behaviour separately.
- `NEW_IMPLEMENTATION_REQUIRED`: the necessary capability is absent, with supporting evidence.
- `AUTHORITY_OR_SOURCE_CONTRACT_BLOCKED`: exact meaning or lawful input supply is unresolved.
- `DOWNSTREAM_PRESERVE`: engineering belongs outside M01-1; preserve it for the appropriate later responsibility.
- `UNASSESSED`: evidence has not yet been inspected; never count as completion.

A row may need more than one work item. Do not force a source-contract gap and a numerical defect into one vague disposition.

Output: a defensible M01-1 readiness assessment, including dependencies that cross the old scheduling boundary and all evidenced remaining obligations.

### E. Plan downstream self-sufficiency

For each proposed M02–M31 module, identify its purpose, canonical outputs, lawful foundational inputs, local strategy-dependent calculations and required recursive intermediate chain.

Distinguish the canonical allocation register from the module-private computation graph. Trace historical cross-group D references recursively until each required path reaches lawful M00/M01-1 ingress or an explicit unresolved prerequisite. Merely enumerating direct cross-group references is insufficient.

Identify existing code that could supply each local chain, and what remains missing or incompatible. Specify local identity, configuration/version and lineage treatment without inventing accepted new mathematical definitions. Resolve whether code extraction would leave hidden peer imports, private-data access or runtime calls.

Output: a per-module self-sufficiency design and implementation backlog. This is planning for all downstream groups; it does not authorise building them during the assessment.

## 7. Prior-audit leads requiring independent examination

The earlier audit reported the following. They are not findings established by this commissioning brief:

| Reported claim | Required examination |
|---|---|
| 114 M01-1 candidates and 95 downstream identities; 113/1 existing/absent own-kernel paths for the former and 61/34 for the latter | Reconcile exact rows, definitions and actual paths. Do not treat path presence as correctness or percent complete. |
| D096 absent, affecting D097, D098, D107 and D108 | Inspect the exact accepted D096 rule and current dispatcher/dependency paths. If confirmed, scope the required capability without importing unrelated advanced kernels. |
| D009 cannot produce the required revised-vintage result | Establish the exact classification semantics, complete branch behaviour and applicable historical decisions before proposing a correction. |
| D117 has an unresolved R075 role | Trace accepted dependency meaning, numerical/prerequisite use, source contract and history. Do not delete a dependency to make the implementation easier. |
| D123 controlled calculation exists but real official-period mapping is unresolved | Separate numerical support from provider-backed period/revision identity. Do not substitute receipt order for a required official reporting identity. |
| D138 complete snapshots versus incremental book events remain unresolved | Establish what the admitted input actually represents and whether reconstruction is required. Do not infer a production defect solely from a test fixture. |
| 65 candidate rows carry measurement-convention freeze flags | Inspect the flagged definitions and existing profiles. A flag is neither proof of a defect nor permission to choose a convention. |
| 107 historical cross-group references, across 67 ordered group pairs | Reconcile the inventory and recursive local closure. These are not proposed runtime peer interfaces. |

Reassess all relevant rows, not just these named leads. Record when a prior claim is confirmed, qualified or rejected and cite the evidence causing that conclusion. Do not invent further defects to fill a checklist.

## 8. Required implementation roadmap

The investigation must culminate in a concrete proposed route to implementation, not just a list of problems. Derive exact files, contracts, work units and sequencing from the inspected repository. Do not invent a new package layout or replacement subsystem before checking the existing architecture.

These phases describe dependencies and acceptance scope, not permission to postpone proof until after coding. In future authorised execution, preserve the applicable proof-before-production discipline: establish and commit authority-derived tests/proofs for each implementation or repair unit before its production-behaviour change, then execute the relevant evidence and review sequence. Phase 4 consolidates module acceptance; it is not the first time testing occurs. The present assignment only plans this sequence.

### Phase 1 — Make the intended production boundary explicit

Prepare the exact proposed authority transition: M01-1 population, measurement definitions, canonical ownership, treatment of the old M01 responsibility, downstream allocation and the replacement/amendment of the active ExecPlan where needed.

Distinguish preserved mathematical authority from changed software ownership and changed execution scope. Explain what happens to unfinished old M01 obligations: retained within M01-1, transferred to downstream planning, still unresolved, or excluded from the new active target with history preserved. Do not silently abandon them.

Identify the exact decisions requiring owner approval. Preserve GUARDRAILS.md and Git history; do not create a second competing active plan. Present proposed changes before requesting approval.

### Phase 2 — Establish the M01-1 implementation boundary

Plan the smallest repository-conformant separation of eligible calculations and reusable infrastructure. Specify public contracts, admitted M00 access, configuration ownership, durable result identities, lineage, persistence isolation and dependency restrictions.

Determine whether existing interfaces or stored results need compatibility handling, migration, recalculation or version separation. Do not silently relabel old results as new-owner outputs. Plan preservation of history and recovery to the last accepted checkpoint without destructive history rewriting.

Existing infrastructure is a reuse candidate, not automatically a reusable whole. Identify which parts are foundational and which currently embed policy or broad M01 assumptions.

### Phase 3 — Close M01-1 mathematical and source-contract gaps

Sequence missing mathematics, confirmed repairs and source-contract decisions by actual dependency. Distinguish problems solvable from accepted authority from decisions requiring new authority or external source evidence.

For each work unit specify: exact proposition, inputs, accepted definition, relevant files, dependency prerequisites, intended change, proof obligations, refusal behaviour, reviewer boundary and recoverable checkpoint. Do not choose financial equations, predictive assumptions or provider bindings merely to unblock code.

If D096 absence is confirmed, plan its bounded accepted measurement and dependent integration specifically. Its historical Stage-2 placement is not a reason to omit it from M01-1, nor permission to implement all old Stage 2.

### Phase 4 — Demonstrate and accept the independent foundation

Plan tests derived from accepted meanings, with expected values established independently of the implementation under examination. Cover the calculation-specific positive, boundary and invalid-input cases, temporal/history/selection rules, version compatibility, lineage, retry/recalculation, persistence and public reachability required by authority.

Distinguish independently executable calculation tests from integration tests that exercise legitimate foundational dependencies. Independence does not prohibit legitimate predecessor calculations; it prohibits unrelated or downstream prerequisites.

Reuse valid historical tests and results with their exact scope recorded. Require fresh execution where the changed proposition needs it, once testing and implementation are authorised. Distinguish controlled-input proof, native-source contract evidence and observed live-source behaviour. Do not imply live integration from synthetic fixtures or claim that live execution is universally required without an applicable acceptance obligation.

The proposed completion condition is that every admitted M01-1 calculation has its accepted implementation and applicable evidence, the module boundary and durable public behaviour are established, and independent review accepts the exact candidate. Counts, compilation and aggregate suite success alone do not establish this.

### Phase 5 — Implement downstream peers as separately bounded work

Use the section 6.E self-sufficiency maps to propose an evidence-based implementation order. Module numbers and historical D edges do not determine that order. The order may reflect shared-foundation readiness and the owner's priorities, but must not introduce peer runtime dependencies.

For each authorised peer: establish its exact contract, reuse and adapt suitable existing work, implement required private intermediate chains, preserve canonical identities, and provide its own configuration and evidence. Demonstrate that it can execute and be tested without another peer running or supplying private state. Show that local strategy changes do not change another peer's implementation implicitly.

Do not introduce a shared downstream strategy layer to avoid duplication. Do not convert historical cross-group D references into API contracts between peers.

### Phase 6 — Integration, transition and release boundary

Plan any system composition, registry changes, data transition and acceptance required by the inspected architecture. Verify shared foundational consumption and peer isolation as separate propositions.

Do not infer a trading orchestrator, order-routing policy, capital allocator or live-deployment mandate from the module list. If such functionality is required to realise a broader operational outcome but absent from accepted scope, identify the specific additional brief needed. This document authorises no live trading or external order/account mutation.

## 9. Required deliverables from the next worker

Produce a coherent package with these contents; combine files where it improves usability rather than proliferating receipts:

1. **Understanding and assessment report:** the intent, original-versus-V2 comparison, actual progress, separately evidenced findings, reusable assets, remaining work and precise limits of evidence. Answer the two questions in section 1 directly.
2. **209-row traceability register:** preserve every D identity and original/V2 relationship; link detailed evidence rather than repeating long prose in cells.
3. **M01-1 completion backlog:** the exact admitted/proposed population distinction, semantic/source/architecture/evidence gaps, dependencies and required decisions.
4. **Downstream self-sufficiency map:** each proposed peer's canonical outputs, foundational ingress, recursively required local intermediates, reuse candidates and missing work.
5. **Proposed implementation and acceptance plan:** repository-specific phases/work units, exact authority changes, affected files/contracts, proof and independent-review boundaries, compatibility/recovery treatment and the next executable unit after approval.
6. **Decision and unresolved register:** only material decisions or gaps, each with evidence, consequence, recommended resolution where supported, and the exact approval or missing fact required.

The traceability register must separate at least: D identity/name; original authority and amendments; old implementation stage; V2 proposed owner; direct and transitive dependencies; typed contexts; equation/conventions and units; source contract; implementation location and actual behaviour; own-kernel availability; public reachability; persistence/lineage; test-source coverage proposition; historical execution evidence; independent acceptance; reuse disposition; outstanding work; evidence references; epistemic status.

Use separate linked records for multiple findings on one signal. Mark genuinely non-applicable fields N/A and unestablished fields UNKNOWN. Missing inspection is UNASSESSED, not a favourable conclusion.

## 10. Working discipline and stop conditions

Take the time needed to read and understand. Do not optimise for a quick tally. Maintain a concise progress record so a successor can resume at the exact inspected boundary without rereading everything or trusting a summary as authority.

Progress updates should state what has been established, what remains uncertain and what the next reading will resolve. Do not narrate every search command.

Stop dependent work if a required governing file is absent/unreadable, a material authority conflict cannot be resolved, or a mandatory integrity check fails. Preserve the failed check and exact source identity. Do not silently substitute a weaker check. Otherwise, investigate ordinary uncertainties within scope before asking the owner.

At an unresolved decision, ask one specific question tied to concrete alternatives and consequences. Do not ask broad questions that the repository can answer. Do not fabricate provider mappings, new mathematical definitions, missing history or test acceptance to keep moving.

Do not run tests during this assignment. Do not claim exhaustive semantic correctness from a static inventory. Do not equate “source inspected”, “implementation present”, “historical tests passed”, “independently accepted” and “ready under V2”. Prove each claim separately.

## 11. Completion criteria for this investigation and planning assignment

This assignment is ready to return when:

- The intended architecture is explained correctly, including downstream local duplication and no peer runtime dependencies.
- Every original D identity is accounted for and the required in-scope inspection is performed. If a genuine blocker prevents this, return a clearly labelled partial/blocked handoff with unassessed rows visible; do not call the investigation complete.
- Original-M01 progress and V2 readiness are assessed separately against their respective requirements.
- Reuse conclusions are supported by source and semantic evidence, rather than dispatcher counts.
- M01-1 gaps and downstream recursive self-sufficiency needs are explicit.
- The proposed implementation plan is concrete enough for a worker to execute after the identified authority decisions, with exact scope, dependency order and acceptance propositions.
- Genuine blockers and outstanding evidence remain visible; no full readiness claim is made if they prevent it.
- The owner receives a recoverable handoff containing the reports, registers, proposed plan, exact baseline and precise next step. Preserve source repositories and history; do not destroy or silently supersede existing work.

The first worker response should briefly confirm this objective and the read-only/no-tests boundary, then begin the authorised investigation. Do not spend the entire turn merely restating this brief.

## 12. Evidence and limits of this brief

This brief was prepared from the owner's instructions, the supplied repository's GUARDRAILS.md, AGENTS.md and EXEC_PLAN.md, the authority index, V2 workbook design rules, ADR-WBV2-001, ADR-WBV2-002, Pass08 clarification and the supplied prior audit report. The archive hashes and archived branch reference were read directly.

It does not certify the previous audit's calculation counts, defect diagnoses, actual production behaviour, test results or acceptance claims. Those remain subjects of the worker's primary-evidence assessment. No project tests or production changes were performed in preparing this brief.

TS: 14-10-26 20:07
