# NVIDIA_2026 Normative Authority and Top-Down Alignment ExecPlan

## Status
active

## Objective
Establish one internally coherent, evidence-backed alpha architecture baseline; freeze that baseline through the repository's numbered core/addendum model; then align tests and implementation from raw inputs to final outputs one semantic boundary at a time.

The work is not production-hardening. The repository is an alpha system with placeholders, incomplete end-to-end composition, no paper-data execution history, and no established production retention, recovery, capacity, deployment or availability requirements. Those production matters must remain `Unknown`, `reserved`, or explicitly out of scope unless the user later supplies authority.

## Governing user intent
The user is the system architect. The code is implemented by GPT workers. The required project posture is:

1. external authoritative best practice informs architectural decisions;
2. adopted project-specific meaning is recorded in normative documents;
3. normative documents govern tests;
4. tests govern code;
5. modularity and future change must be designed at known volatility boundaries;
6. semantic judgement must be performed by the LLM through full contextual reading, not delegated to automated comparison, summaries, search, scripts, embeddings, ASTs, inventories or counts.

## Authority
Apply this order for this programme:

1. current user instructions and explicit approvals;
2. `AGENTS.md`;
3. this ExecPlan;
4. active repository normative documents and their explicit routing rules;
5. tests;
6. source, configuration, schemas, fixtures and migrations;
7. ledgers, receipts, historical plans and reports;
8. `PROJECT_EXECUTION_METHOD.md` where higher authority is silent.

External vendor and standards material is evidence, not a floating runtime authority. A best-practice proposition becomes project authority only after its source, rationale, project-specific interpretation and scope are recorded in the normative corpus.

## Branch and baseline
- Baseline branch: `work/NVIDIA_2026_gate1_normative_repair_final_20260529`
- Baseline commit: `e9e9eba`
- Working branch: `work/NVIDIA_2026_normative_authority_top_down_alignment_20260717`
- Source audit bundle: `/mnt/data/NVDA_ARCHITECTURE_MODULARITY_REVIEW_OUTPUT_20260717`

No merge to another branch is authorised.

## Scope
### In scope
- semantic reconciliation of the active normative corpus;
- authoritative-source cross-checks where a normative proposition needs external grounding;
- numbered addenda or controlled amendments that resolve contradiction, ambiguity, overclaim, missing ownership, missing extensibility boundaries or inaccurate status;
- a frozen normative baseline manifest with versions, hashes, authority relationships and explicit supersession;
- top-down semantic audit from raw inputs through final outputs;
- alpha-stage identity, lineage, state ownership, replay requirements and replaceable contracts;
- tests derived from frozen normative requirements;
- code/config/schema/fixture changes required to satisfy those tests;
- evidence, validation and semantically bounded commits.

### Out of scope unless separately authorised
- production retention periods;
- RTO/RPO, high availability, disaster recovery or production SLOs;
- production deployment topology, scaling or capacity targets;
- live brokerage or production credentials;
- real-money execution;
- paper-trading claims unsupported by actual paper data;
- rewriting project intent to match current tests or code;
- automated semantic acceptance.

## Non-negotiable semantic-reading rule
Every normative document in the active corpus must be read in full, in routed order, as prose and as a connected architecture. Each semantic acceptance decision must be made by the LLM after reading the proposition in its surrounding context and comparing it with all materially related propositions.

Automation may only assist deterministic mechanics such as file inventory, hashing, line numbering, formatting, cross-reference extraction, diffing and validation. Automation must not decide or certify:

- semantic equivalence;
- contradiction or absence;
- project intent;
- authority;
- architectural adequacy;
- modularity;
- future-proofing;
- final acceptance.

Search, grep, ASTs, scripts, tables, summaries, embeddings and generated registries are navigation aids only. They cannot substitute for reading. No document or semantic unit may be marked reviewed unless it was read in full.

## Architectural interpretation rules
1. This is an alpha system. Current placeholders must be labelled honestly rather than inflated into production claims.
2. Future-proofing means stable, explicit substitution boundaries at known volatility points. It does not mean speculative abstraction everywhere.
3. A common envelope must not collapse strongly typed payloads into ungoverned generic dictionaries.
4. Authoritative identifiers may only be originated by their named owner and must not be fabricated downstream.
5. Missing authority fails closed where continuing would manufacture lineage, policy or decision authority.
6. Structural status and implementation-truth status must be reported separately using the exact status models in `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`. Active behaviour cannot remain implementation-labelled `reserved` or `future_only`; it must use `implemented`, `thin_seam`, or `placeholder` as the evidence warrants.
7. In-memory state is acceptable in alpha when declared as such and isolated behind a replaceable contract. It must not be called durable or replay-complete.
8. External best-practice disagreement must be resolved through explicit project rationale, not vendor-name voting.

## Numbered normative-document model
The existing core/addendum pattern is preserved:

- `N` is the stable core document;
- `N.1`, `N.2`, and later documents are controlled expansions, corrections or supersession records;
- addenda must identify exact propositions extended, clarified or replaced;
- an addendum must state which earlier text remains authoritative;
- contradictions may not be left as two apparently active claims;
- historical text is preserved unless a direct amendment is necessary for routing or truthfulness.

## Acceptance units

### Gate A0 — Control and corpus establishment
**Pass:** branch, plan, full-read manifest, active normative inventory and routing order are established without semantic claims based on automation.

**Required reads:** `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, `ROADMAP_LEDGER_V2.md`, `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`, and any route-specific override that becomes applicable.

**Allowed changes:** task-local plan, manifest, progress ledger and evidence directory only.

**Validation:** Git state, branch, file existence, `git diff --check`.

### Gate A1 — Normative corpus semantic reconciliation
Work one routed normative document pair or independently bounded normative surface at a time.

For each unit:
1. read the core document in full;
2. read its working/addendum document in full where present;
3. read all materially related normative propositions in other documents;
4. identify the precise governed surface and intended system meaning;
5. classify each material proposition as `coherent`, `ambiguous`, `contradictory`, `overclaimed`, `underspecified`, `reserved`, `provisional alpha`, or `superseded`;
6. consult current authoritative sources only where external grounding is necessary;
7. record the source, date, proposition, project-specific adaptation and rejected alternatives;
8. draft the smallest lawful addendum or amendment;
9. reread the changed normative unit in full;
10. validate cross-document coherence before acceptance and commit.

**Pass:** all active normative propositions are internally coherent, routed, status-truthful and explicitly connected to their addenda and adopted external rationale.

**Fail:** unresolved contradiction, silent supersession, unclear owner, production overclaim, fabricated specificity, or automated semantic acceptance.

### Gate A2 — Normative freeze
Create a baseline manifest recording:
- every active normative document and addendum;
- hash and effective status;
- authority and routing relationships;
- superseded propositions;
- reserved and provisional-alpha surfaces;
- unresolved Unknowns;
- adopted external-source crosswalk.

**Pass:** a reader can determine exactly which normative proposition governs each architecture surface without consulting tests or code.

### Gate B — Top-down semantic reconstruction and conformance mapping
Gate B is semantic cartography, not repair. It reconstructs what the alpha system is intended to do and what it currently does, including incomplete paths, honest placeholders, correct graceful failures, hidden fallbacks, uncomposed components, contradictions, dead ends and Unknowns. Tests, source, configuration, schemas, fixtures and migrations remain read-only throughout Gate B.

Proceed sequentially, one semantic boundary at a time:

1. raw input definitions and source identity;
2. input envelopes, schemas and validation;
3. canonicalisation and normalisation;
4. identifier and lineage propagation;
5. intermediate state ownership;
6. persistence boundaries;
7. deterministic transformations and algorithms;
8. strategy/playbook selection and execution;
9. risk and policy decisions;
10. execution or simulated-execution boundaries;
11. exit and close behaviour;
12. outputs, receipts, reporting and replay.

For every boundary, first write a plain-English behaviour statement that a systems architect can understand without reading code. Each statement must establish:

- the human trading or operational purpose;
- actual inputs and their meaning;
- the interpretation, transformation or decision performed;
- actual outputs and downstream use;
- time, ordering and state dependence;
- identity and lineage behaviour;
- the observed current alpha status.

The current alpha status must use one of these exact classifications:

- `operates_consistently_with_intent`;
- `partially_implements_intent`;
- `honest_placeholder`;
- `correctly_fails_closed`;
- `locally_implemented_not_composed`;
- `behaves_differently_from_intent`;
- `unreachable`;
- `Unknown`.

For every boundary, reconstruct four distinct views:

1. **Normative view:** exact frozen propositions describing what must happen.
2. **Observed implementation view:** manual semantic trace from entry to output, including branches, fallbacks, state changes and termination.
3. **Test view:** what current tests actually prove, assume, omit or misrepresent. Tests must be classified as `normatively_aligned`, `partially_aligned`, `implementation_locked`, `insufficient`, `misleading`, or `absent`.
4. **Conformance view:** exact delta between normative requirement, current test claim and observed code behaviour.

A failing test is evidence, not meaning. A passing test is bounded proof, not conformance certification. Syntax errors, incomplete wiring or graceful failure do not prevent semantic reconstruction. The worker must read and trace the code as connected meaning; execution, search, ASTs, scripts and test runs may assist navigation or deterministic validation but may not decide or certify behaviour.

Incomplete behaviour is not automatically a defect. Gate B must distinguish at minimum:

- aligned thin seam;
- honest placeholder;
- correct graceful failure;
- uncomposed component;
- missing implementation;
- incorrect implementation;
- architectural coupling defect;
- hidden fallback;
- dead or unreachable path;
- Unknown.

Gate B must produce two complementary maps:

- **Longitudinal flow map:** information and decisions from source artefact through ingress, preparation, cognition, risk, execution, exit/close and review/replay.
- **Transverse ownership map:** meaning, owner, writers, readers, state, extension seam and replacement impact for cross-cutting capabilities such as temporal context, financial calendar, dynamic coefficients, cognitive stack, Parallel Risk Lane, vocabulary, DMPV3, lineage, persistence and review.

DMPV3 must be mapped only from the precise boundary where packet carriage begins. Pre-DMPV3 raw and canonical inputs must not be redescribed as DMPV3 merely for architectural neatness.

Required Gate B artefacts:

- `PLAIN_ENGLISH_BEHAVIOUR_ATLAS.md`;
- `END_TO_END_FLOW_MAP.tsv`;
- `TRANSVERSE_OWNERSHIP_MAP.tsv`;
- `NORMATIVE_TEST_CODE_CONFORMANCE.tsv`;
- `UNKNOWN_AND_PLACEHOLDER_REGISTER.tsv`;
- `GATE_C_TEST_REQUIREMENTS.tsv`;
- updated `TOP_DOWN_ALIGNMENT_REGISTER.tsv`, `FULL_READ_MANIFEST.tsv`, `PROGRESS_LEDGER.md` and `VALIDATION_LOG.md`.

**Pass:** every material sequential path and transverse capability is understood and described semantically from input to output; all incomplete, contradictory, graceful-failure, fallback, dead-end and Unknown behaviour is explicitly classified; every observed behaviour is mapped to frozen normative propositions and current test evidence; and no material behaviour remains unlabelled. Code correctness is not required for Gate B to pass.

**Fail:** any material path is inferred from filenames, tests or automation instead of semantic reading; a failure is repaired before the complete boundary is understood; a passing test is treated as meaning or architecture proof; an incomplete alpha seam is automatically labelled defective; or source/tests are mutated during reconstruction.

### Gate C — Normative test authority and executable contract

Gate C is divided into two acceptance stages. Gate D may not open until both stages pass.

#### Gate C1 — Normative test design and executable baseline

Gate C1 converts Gate B's 48 semantic behaviour units into executable contracts derived from the frozen normative baseline. Trading/domain production source and runtime configuration remain unchanged. Test/proof tooling and development-only dependency metadata may change only where required to make the proof system isolated, collectible and truthful. A red test may be an accepted Gate C1 result when it truthfully exposes an implementation gap.

For each Gate B requirement, Gate C1 must:
1. disposition the requirement as ready, blocked by missing normative authority, or explicitly deferred;
2. identify the exact frozen normative proposition and Gate B semantic unit;
3. semantically disposition existing relevant tests;
4. design positive, negative, false-positive, graceful-failure, identity/lineage, substitution, state-isolation and replay cases where required;
5. write executable tests for every ready requirement without changing production code;
6. preserve blockers rather than inventing product meaning;
7. run the tests against untouched implementation and record truthful red/green evidence;
8. route every normative implementation failure into one candidate Gate D unit.

The Gate C1 artefacts are the existing Gate C authority, design, matrix, fixture, isolation, prerequisite, red/green and backlog files recorded below.

**Gate C1 pass:** all 48 requirements have explicit disposition; ready requirements have executable normative proof; blockers name exact missing authority; production implementation remains frozen; proof isolation is demonstrated; and every implementation failure has a bounded candidate work unit. Gate C1 does not require all tests to pass.

#### Gate C2 — Proof-tier authority and proof-envelope closure

Gate C2 freezes the proof authority that later implementation must consume. It is test-governance work, not code implementation. It must:

1. explicitly classify the five Gate C normative files by tier using registry, proof-block or active-pack authority rather than folder placement;
2. map each admitted file to exact normative propositions and both positive and false-positive obligations;
3. construct one proof envelope for each candidate Gate D unit containing the governing proposition, Gate B meaning, positive Tier A proof, negative Tier A proof, existing Tier A dependants, Tier B shadow evidence, Tier C evidence, test limitations, fixture/isolation obligations, targeted command, aggregate route, test-fallout authority and dependencies;
4. mark each unit `proof_authority_ready` or `closed`, with the exact conflict, missing proof or upstream dependency and required return gate;
5. prohibit Gate D from opening a closed unit or deciding, rewriting, weakening, skipping, broadening or reclassifying test authority.

Gate C2 may pass with closed units. Passing means every unit has a truthful proof-authority decision, not that every unit is ready for implementation.

Required Gate C2 artefacts:
- `GATE_C_TIER_A_ADMISSION_RECEIPT.md`;
- `GATE_C_TIER_A_PROMOTION_MANIFEST.tsv`;
- `GATE_C2_PROOF_ENVELOPE_REGISTER.tsv`;
- `GATE_C2_DEPENDENCY_MAP.tsv`;
- individual envelope records under `gate_c2_proof_envelopes/`;
- `GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv`;
- `GATE_C2_CLOSEOUT.md`;
- validation evidence under `gate_c2_evidence/`.

**Gate C2 pass:** all 24 candidate units have frozen proof envelopes and explicit open/closed decisions; the five-file tier admission is exact; positive and false-positive proof is recorded; existing Tier A conflicts are not concealed; incomplete Gate C1 proof is returned rather than guessed; production source, runtime configuration, test assertions and fixtures remain unchanged; and Gate D remains closed for every unresolved unit.

### Controlled normative completion before Gate D

Direct user authority on 2026-07-20 closes Gate D and reopens normative authority for the ten Gate C requirements that were truthfully blocked by missing meaning. The earlier Gate C1/C2 results remain retained evidence and a valid checkpoint, but every prior `gate_d_open_decision=yes` is suspended until the expanded normative baseline and proof authority are re-frozen.

This controlled return consists of six ordered stages:

1. **Plan amendment:** record this closure, package boundaries, mutable surfaces and stopping point before substantive mutation.
2. **Normative completion:** resolve one semantic decision package at a time through numbered normative addenda or a lawful core revision.
3. **Expanded normative freeze:** update proposition, baseline, routing, Unknown and coherence evidence for every accepted package.
4. **Gate C1 reopening:** derive positive and false-positive executable proof for all ten formerly blocked requirements without changing production source or runtime configuration.
5. **Gate C2 reopening:** re-admit the complete Gate C proof surface, re-evaluate every existing and new proof envelope, dependencies, conflicts and implementation-unit boundary, then freeze the revised proof authority.
6. **Gate D readiness review:** report whether any implementation unit may open, create a clean durable checkpoint, and stop before implementation.

The nine semantic decision packages and linked requirements are:

| Package | Governed decision | Requirements |
|---|---|---|
| `N-01` | typed options contract | `C-004` |
| `N-02` | financial-calendar layer model and ownership | `C-005`, `C-018` |
| `N-03` | prepared-data common envelope | `C-008` |
| `N-04` | canonical merge conflict and source precedence | `C-011` |
| `N-05` | common metadata and stage-specific carriers | `C-013` |
| `N-06` | cross-state transaction boundary | `C-024` |
| `N-07` | signal-informed intraday phase model | `C-026` |
| `N-08` | serial and parallel risk join | `C-036` |
| `N-09` | authoritative replay envelope | `C-046` |

For each package, the worker must read the connected normative documents, Gate B unit and neighbours, existing tests, and bounded source surfaces in full; state the unresolved proposition; adopt one project-specific decision; record alternatives ruled out, longitudinal and transverse effects, source lineage and remaining Unknowns; reread every changed normative surface in full; perform connected-document coherence validation; commit the semantic unit; verify the tree; and create a full repository-plus-`.git` checkpoint with checksum.

The numbered addendum allocation is owner-aligned and may be populated incrementally one accepted package at a time:

- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md` — `N-01`, `N-02`;
- `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` — `N-03`, `N-04`, `N-05`;
- `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` — `N-06`, `N-08`, `N-09`;
- `docs/02.2_SIGNAL_INFORMED_INTRADAY_PHASE_WORKING.md` — `N-07`.

These documents extend their named core/working companions only for the exact propositions recorded in their supersession and relationship sections. They do not create a competing authority stack. If full reading proves a package must move or split, amend this plan before the affected normative mutation.

Gate D remains closed throughout these stages. Production source, runtime configuration, schemas, fixtures and migrations remain prohibited. Gate C test surfaces become mutable only after the expanded normative freeze is committed and the tests subtree override has been reread.

**Normative-completion pass:** all nine packages have explicit dispositions, their connected documents are coherent, the expanded baseline is frozen, and no linked requirement remains blocked merely because a decision was omitted.

**Gate C reopening pass:** all 48 requirements have an authoritative executable disposition, Tier authority and aggregate promotion are explicit, every candidate implementation unit has a re-evaluated frozen proof envelope, and unresolved dependencies fail closed.

**Required stopping point:** a clean, committed, downloadable Gate D readiness checkpoint. No implementation may begin in the semantic unit that decides readiness.

### Gate D — Normative implementation alignment

Gate D is currently closed. It may reopen only by the Gate D readiness decision produced after controlled normative completion and Gate C1/C2 re-freezing. When lawfully reopened, it consumes the then-current frozen normative propositions and Gate C2 proof envelopes. It has no authority to decide or edit proof meaning. For each unit marked `gate_d_open_decision=yes`, Gate D must:

1. reread the exact normative proposition, Gate B semantic statement, Gate C1 tests and Gate C2 proof envelope;
2. confirm all envelope prerequisites are satisfied;
3. write a pre-code implementation decision stating current behaviour, required behaviour, semantic owner, permitted files and forbidden authority expansion;
4. make the smallest semantically complete architectural change, not merely the smallest textual patch;
5. reread the changed input-to-output flow semantically;
6. run targeted positive and false-positive Tier A proof, existing Tier A dependants, Tier B shadow checks and the aggregate promotion route;
7. preserve blocked requirements, alpha status and unrelated boundaries;
8. record evidence and commit one semantic unit.

Gate D must not alter normative documents, admitted Gate C tests, their assertions or fixtures. If an envelope proves contradictory or incomplete, return the unit to Gate C2; if normative meaning is missing, return it to numbered normative authority.

**Gate D pass:** every lawful open unit is implemented and semantically verified or explicitly returned; all admitted positive and false-positive proof passes without weakening; affected Tier A proof remains reconciled; blocked units remain untouched; and post-change behaviour is recorded truthfully.

## Progress and evidence files
Maintain within this directory:
- `FULL_READ_MANIFEST.tsv`;
- `PROGRESS_LEDGER.md`;
- `NORMATIVE_PROPOSITION_REGISTER.tsv`;
- `EXTERNAL_SOURCE_DECISIONS.md`;
- `NORMATIVE_BASELINE_MANIFEST.tsv`;
- `TOP_DOWN_ALIGNMENT_REGISTER.tsv`;
- `PLAIN_ENGLISH_BEHAVIOUR_ATLAS.md`;
- `END_TO_END_FLOW_MAP.tsv`;
- `TRANSVERSE_OWNERSHIP_MAP.tsv`;
- `NORMATIVE_TEST_CODE_CONFORMANCE.tsv`;
- `UNKNOWN_AND_PLACEHOLDER_REGISTER.tsv`;
- `GATE_C_TEST_REQUIREMENTS.tsv`;
- `GATE_C_TEST_AUTHORITY_REGISTER.tsv`;
- `EXISTING_TEST_DISPOSITION.tsv`;
- `gate_c_test_design/`;
- `IDENTIFIER_LINEAGE_PROOF_MATRIX.tsv`;
- `MODULARITY_SUBSTITUTION_MATRIX.tsv`;
- `STATE_PERSISTENCE_TEST_MATRIX.tsv`;
- `DETERMINISM_REPLAY_TEST_MATRIX.tsv`;
- `AUTHORITATIVE_FIXTURE_REGISTER.tsv`;
- `TEST_ISOLATION_REGISTER.tsv`;
- `NORMATIVE_PREREQUISITE_REGISTER.tsv`;
- `RED_GREEN_EVIDENCE.tsv`;
- `GATE_D_IMPLEMENTATION_BACKLOG.tsv`;
- `GATE_C_TIER_A_ADMISSION_RECEIPT.md`;
- `GATE_C_TIER_A_PROMOTION_MANIFEST.tsv`;
- `GATE_C2_PROOF_ENVELOPE_REGISTER.tsv`;
- `GATE_C2_DEPENDENCY_MAP.tsv`;
- `gate_c2_proof_envelopes/`;
- `GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv`;
- `GATE_C2_CLOSEOUT.md`;
- `NORMATIVE_COMPLETION_DECISION_REGISTER.tsv`;
- `normative_completion_decisions/`;
- `NORMATIVE_COMPLETION_COHERENCE_REVIEW.md`;
- `GATE_D_READINESS_REPORT.md`;
- `CHECKPOINT_REGISTER.tsv`;
- `VALIDATION_LOG.md`.

These are evidence and execution aids. They do not become semantic authority merely by existing.

## Commit discipline
- Commit the plan/control establishment separately.
- Commit each accepted normative semantic unit separately where feasible.
- Do not combine normative, test and code changes for unrelated boundaries.
- A normative unit may include its explicit addendum and directly required routing/index updates.
- Preserve exact validation evidence in the progress and validation logs.

## Stop conditions
Stop only for:
- missing authority that cannot be inferred lawfully;
- an architectural choice requiring the user's decision after the evidence and one recommended path are prepared;
- unavailable required source material or official documentation;
- destructive/external action requiring approval;
- unsafe repository/tool state;
- exhaustion of the authorised programme with all acceptance gates passed.

Ordinary contradiction, failing tests, missing dependencies, placeholders and implementation gaps are work, not stop conditions.

## Progress
- 2026-07-17: user authorised creation and uninterrupted execution of this ExecPlan.
- 2026-07-17: branch established from baseline `e9e9eba`.
- 2026-07-17: task pack relocated to `project_control/` and expressly routed through `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` before normative content mutation.
- 2026-07-17: Gate A1 completed through full semantic reconciliation of routed normative units `01/01.1` through `11/11.1`, including vocabulary authority and the eighteen-surface blueprint.
- 2026-07-17: Gate A2 completed through one controlled normative baseline manifest containing exact document hashes, routing, supersessions, alpha reservations, explicit Unknowns, external-source decisions and direct governing-proposition lookup for all eighteen architecture surfaces.

- 2026-07-17: Gate B amended by direct user authority from alignment/repair wording to read-only semantic reconstruction and conformance mapping, with plain-English behaviour statements, longitudinal and transverse maps, and explicit separation of normative, test, code and conformance views.
- 2026-07-17: Gate B completed as read-only semantic reconstruction: 48 behaviour units across B01-B12, 12 transverse ownership cards, 16 explicit Unknown/placeholder records and 48 proposed Gate C test requirements. Source, tests, configuration, schemas, fixtures, migrations and scripts remained unchanged.
- 2026-07-18: Gate C amended by direct user authority into a normative test-authority programme with explicit evidence deliverables, accepted red-test semantics, production-code freeze and blocked-authority handling.
- 2026-07-18: Gate C1 completed: 48 requirements dispositioned; 38 ready requirements admitted; 10 blocked by exact missing normative authority; 30 new normative tests recorded 11 green and 19 expected red; 1,154 existing tests passed; 24 bounded candidate Gate D units created.
- 2026-07-19: Gate C2 reconstructed from the durable Gate C checkpoint: five-file Tier A admission restored; 24 proof envelopes frozen; 13 units marked proof-authority ready and 11 units closed by test conflict, incomplete Gate C1 proof or upstream proof dependency.
- 2026-07-20: direct user authority closed Gate D, suspended all earlier Gate D-open decisions, and inserted controlled normative completion for `N-01` through `N-09`, followed by expanded Gate A2 freeze and Gate C1/C2 reopening.
- 2026-07-20: `N-01` through `N-09` were accepted as nine separately committed semantic units; the ten missing-meaning blockers were resolved without production/test mutation.
- 2026-07-20: the expanded normative baseline was re-frozen; Gate C1 is the next active acceptance stage and Gate D remains closed.

## Decisions
- The programme is alpha architecture alignment, not production hardening.
- Semantic judgement remains human-like LLM work performed after full reading; automation is restricted to mechanics.
- The existing numbered core/addendum model is preserved.
- Normative coherence precedes test and code alignment.
- Gate B is semantic cartography only. It may classify defects and Gate C requirements but may not modify tests, source, configuration, schemas, fixtures or migrations.
- The initial Gate C1/C2 records are retained checkpoints, not current Gate D opening authority.
- All earlier `gate_d_open_decision=yes` values are suspended until the expanded baseline and proof authority are re-frozen.
- Normative completion uses four owner-aligned numbered addenda and nine separately committed semantic decision records.

## Roadblocks
None recorded at plan creation.

## Validation
Gates A0, initial A1/A2, B, and initial C1/C2 passed as retained checkpoints. Normative completion N-01 through N-09 and the expanded Gate A2 freeze have passed. Reopened Gate C1 is active. Exact evidence, commands and mechanical results are recorded in `VALIDATION_LOG.md`; semantic acceptance and proof-authority decisions are recorded in `PROGRESS_LEDGER.md`, the Gate B semantic artefacts, the normative-completion records and the Gate C1/C2 authority records. Gate D is closed and has not started.

## Artefacts
This ExecPlan and its task-local evidence files.

## Unknowns
- The complete external-source lineage for every pre-existing normative proposition is not established; no N-01 through N-09 decision required external evidence.
- Exact implementation field names, schemas, enum values and assembly surfaces under N-01 through N-09 remain Gate D work and are not normative Unknowns.
- N-07 numeric thresholds, dwell/grace windows and confidence calibration remain versioned configuration work; they were intentionally not invented.
- Production retention, historical executable packaging, storage, RTO/RPO, availability, deployment, capacity and live/paper operating requirements remain intentionally Unknown.
- Vocabulary semantic/machine parity and proof-system aggregate closure remain open under their existing authorities.

## Closeout
Normative completion N-01 through N-09 and the expanded normative freeze are complete. Reopened Gate C1 is active; all prior Gate D-open decisions remain suspended. Gate D is closed and has not started. The authorised stopping point remains the re-frozen Gate C2 and Gate D readiness checkpoint before any implementation.

- 2026-07-20: reopened Gate C1 established executable authority for all ten formerly blocked requirements: 23 new Tier A contract tests recorded 23 expected reds against untouched production code; nine package-aligned Gate D candidates were created but remain held pending Gate C2.
