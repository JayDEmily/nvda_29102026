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
Gate C converts Gate B's 48 semantic behaviour units into an executable contract derived from the frozen normative baseline. Trading/domain production source and runtime configuration remain unchanged. Test/proof tooling and development-only dependency metadata may change only where required to make the proof system isolated, collectible and truthful. A red test may be an accepted Gate C result when it truthfully exposes an implementation gap; Gate D owns implementation repair.

For each Gate B requirement:
1. classify it as `ready_for_test_design`, `blocked_missing_normative_authority`, or `deferred_by_explicit_authority`;
2. identify the exact frozen normative proposition and Gate B semantic unit;
3. semantically read every existing relevant test and classify it as `preserve_unchanged`, `enrich`, `split`, `replace_implementation_locked`, `retire_misleading`, or `retain_non_authoritative_regression`;
4. design positive, negative, false-positive-resistance, graceful-failure, identity/lineage, substitution, state-isolation and replay cases where the proposition requires them;
5. write executable tests for every ready requirement without changing production code;
6. preserve blocked requirements as explicit authority prerequisites rather than inventing product meaning;
7. run the admitted Gate C tests against the untouched implementation and record truthful red/green/error/blocked evidence;
8. route each normative failure into one bounded Gate D implementation unit.

Required Gate C artefacts:
- `GATE_C_TEST_AUTHORITY_REGISTER.tsv`;
- `EXISTING_TEST_DISPOSITION.tsv`;
- twelve boundary design packs under `gate_c_test_design/`;
- `IDENTIFIER_LINEAGE_PROOF_MATRIX.tsv`;
- `MODULARITY_SUBSTITUTION_MATRIX.tsv`;
- `STATE_PERSISTENCE_TEST_MATRIX.tsv`;
- `DETERMINISM_REPLAY_TEST_MATRIX.tsv`;
- `AUTHORITATIVE_FIXTURE_REGISTER.tsv`;
- `TEST_ISOLATION_REGISTER.tsv`;
- `NORMATIVE_PREREQUISITE_REGISTER.tsv`;
- `RED_GREEN_EVIDENCE.tsv`;
- `GATE_D_IMPLEMENTATION_BACKLOG.tsv`;
- updated `FULL_READ_MANIFEST.tsv`, `PROGRESS_LEDGER.md`, `VALIDATION_LOG.md`, and executable tests for all ready requirements.

Test design rules:
- tests express the normative proposition, not current implementation convenience;
- a model-validation pass, registry row, same-process memory read, manifest entry or proof-block status is never sufficient by itself;
- fixtures must identify the semantic case, provenance, schema/policy version and whether they are authoritative, synthetic-valid or deliberately invalid;
- governed tracked artefacts are read-only during test execution; generated output uses isolated temporary locations;
- current in-memory adapters may be tested for interface semantics but must not be represented as durable;
- production retention, RTO/RPO, scaling and deployment requirements remain out of scope;
- the financial-calendar layer model, signal-informed intraday phase policy and any other missing product meaning remain blocked until admitted through numbered normative authority.

**Pass:** all 48 requirements have explicit disposition; every ready requirement has accepted executable normative tests; every blocked requirement names the exact missing authority; trading/domain production code and runtime configuration remain unchanged; any proof-tooling or development-dependency change is bounded and evidenced; test isolation protects governed artefacts; the red/green baseline is recorded honestly; and every failing normative test is routed into a bounded Gate D unit. Gate C does not require all tests to pass.

**Fail:** tests are derived from filenames, current implementation or automation instead of frozen meaning; blocked product meaning is invented; assertions are weakened to obtain green; governed artefacts are mutated; production code is changed; or a red normative result is concealed or treated as Gate C failure solely because implementation is incomplete.

### Gate D — Code alignment
For each Gate C unit:
1. make the smallest implementation change satisfying the normative contract;
2. preserve dependency inversion and explicit ownership;
3. avoid speculative production machinery;
4. maintain alpha status labels where implementation remains provisional;
5. run targeted tests and applicable admitted proof blocks;
6. record exact evidence and commit the semantic unit.

**Pass:** target-surface behaviour satisfies the governing tests and normative proposition without weakened validation or unrelated changes.

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
- 2026-07-18: Gate C completed: 48 requirements dispositioned; 38 ready requirements admitted; 10 blocked by exact missing normative authority; 30 new normative tests recorded 11 green and 19 expected red; 1,154 existing tests passed; 24 bounded Gate D work units created.

## Decisions
- The programme is alpha architecture alignment, not production hardening.
- Semantic judgement remains human-like LLM work performed after full reading; automation is restricted to mechanics.
- The existing numbered core/addendum model is preserved.
- Normative coherence precedes test and code alignment.
- Gate B is semantic cartography only. It may classify defects and Gate C requirements but may not modify tests, source, configuration, schemas, fixtures or migrations.

## Roadblocks
None recorded at plan creation.

## Validation
Gates A0, A1, A2, B and C passed. Exact evidence, commands and mechanical results are recorded in `VALIDATION_LOG.md`; semantic acceptance and boundary decisions are recorded in `PROGRESS_LEDGER.md`, the Gate B semantic artefacts and the Gate C authority/evidence registers. Gate D has not started.

## Artefacts
This ExecPlan and its task-local evidence files.

## Unknowns
- The complete external-source lineage for every existing normative proposition is not yet established.
- The authoritative financial-calendar business-layer model and precedence are not yet specified.
- The signal-informed intraday phase policy requires a numbered normative addendum before its Gate C tests can be admitted.
- Production operational requirements are intentionally not established at this stage.

## Closeout
Gate C complete. Gate D is the next lawful gate and has not started.
