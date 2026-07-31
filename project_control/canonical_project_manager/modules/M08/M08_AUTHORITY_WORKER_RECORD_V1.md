# M08 Authority Worker Record V1

## Assignment

- Worker: `Lane 4AW`
- Unit: `M08-PROOF-MLC-A-V1`
- Owner module: `M08 playbook_catalogue`
- Contract boundary: `K13 PlaybookCatalogue`
- Source commit: `ee67c752d14073a959fda478f31f4466b6952cae`
- Worker branch: `work/lane-4a-m08-mlc-a-v1`
- Result label: `PROPOSED_M08_AUTHORITY_V1_AWAITING_LANE_4AT`

## Question

Is current numbered authority sufficient to govern a replaceable, versioned M08 playbook catalogue and eligibility decision boundary—including candidate-family origin and stand-down—without granting capital, execution or lifecycle authority?

## Worker result

`BLOCKED_MISSING_NORMATIVE_AUTHORITY:Which numbered proposition defines the immutable catalogue, playbook-definition, candidate-family and eligibility-decision identities and versions; the exact mandatory eligibility inputs; deterministic filtering, ordering, tie-break and lead-selection rules; posture-block and valid-empty-set stand-down outputs; and the lawful boundary for carrying playbook-specific lifecycle intent downstream without granting M08 capital, broker-execution or portfolio-lifecycle authority?`

Current numbered authority is sufficient to allocate M08/K13 ownership, require replaceability, bound the catalogue seam and prohibit capital, broker and exit/close authority. It is not sufficient to author authoritative M08 proof because the decision and identity semantics named in the return question are not defined by a current numbered proposition. The C-033/C-034 and D-033/D-034 records identify the same required behaviours, but they are downstream historical proof/control evidence and cannot create the missing normative meaning.

## Current numbered authority established

| Topic | Current authority | Finding |
|---|---|---|
| Runtime position | `docs/01_NORMATIVE_CORE.md:35-69` | Posture and risk permission precedes playbook eligibility; the six-stage serial spine forms the candidate and does not own capital deployment. |
| Replaceable boundary | `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md:23-39` | A variable capability requires one owner, explicit input/output contract, external selection/configuration, no fixed implementation count, no hidden shared state and substitution proof. |
| Playbook expansion | `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md:41-58` | The library owns playbook definitions and selection metadata; the serial eligibility stage consumes an explicit registry/equivalent contract; adding/replacing a playbook is bounded; fixed-count assumptions and hidden capital, broker, exit/close, persistence or coefficient authority are prohibited. |
| Expression/lifecycle boundary | `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md:60-75` | Candidate lifecycle intent and bounded handoff belong to the later serial expression stage; broker submission, placement readiness, fills, inventory and exit/close execution remain downstream. |
| Required absence | `docs/03.1_DOMAIN_MODEL_WORKING.md:41-55`; `docs/05.1_GUARDRAILS_WORKING.md:21-31` | Owner-issued identifiers must retain one meaning; missing required identity/authority/input must fail closed or stand down without fabricated substitutes. |
| Modularity | `docs/05.1_GUARDRAILS_WORKING.md:46-58` | Fixed playbook counts, central unrelated dispatch and ripple changes across unrelated stages are prohibited. |
| Ownership-record minimum | `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:32-49` | Alignment requires owner, writer, readers, contracts, identifiers, state, replay, absence behaviour, forbidden mixing and extension boundary. |
| Generic replay facts | `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:66-80`; `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:159-181` | A material decision must preserve material playbook/version inputs, output identity, semantic result and time distinct from emission time; exact per-boundary mandatory fields remain to be fixed. |
| M08 ownership supplement | `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:193-204` | Playbook-library authority owns definition, registry, eligibility-constraint and selection-metadata meaning; state is configuration/metadata receipt only; serial eligibility and review/proof are readers; capital, source ingress, coefficient, broker, live execution and exit/close authority are prohibited. |
| Surface 5.10 | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:288-303` | Surface 5.10 owns definitions, eligibility constraints, selection rules and metadata; inputs are definitions, eligibility context, governed signals and calendar/event constraints; outputs are candidates, eligibility and metadata receipts through explicit registry/eligibility carriers. |
| Replaceable playbooks | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:68-85` | Playbooks must vary behind a contract/registry; orchestration consumes the contract; a new playbook must not rewrite unrelated owners; the consumer contract changes only by lawful versioning. |
| M08 target owner | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:152-173` | M08 owns versioned playbook definitions, catalogue and eligibility semantics; it must not own runtime capital or execution decisions. |
| Dependency boundary | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:175-195` | M08 has no runtime/contract prerequisite; M05 consumes M08. |

## M08/K13 accepted architecture mapping

| Artefact | Exact locator | Accepted mapping |
|---|---|---|
| Architecture report | `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md:100-143` | Surface 5.10 maps to M08; M08 owns playbook definitions, replaceable registry and eligibility semantics; replaceability/composition remain unproved. |
| Workbook surface | `Atlas_Architecture_Traceability.xlsx`, `Surface Map!A11:O11` | 5.10, M08, B08, C-033/C-034, D-033/D-034; accepted M08 ownership and no M07 runtime dependency. |
| Workbook module | `Atlas_Architecture_Traceability.xlsx`, `Target Modules!A10:Q10` | M08 `playbook_catalogue`; state owner `versioned playbook catalogue`; interfaces `PlaybookDefinition`, `PlaybookCatalogue`, `EligibilityDecision`; no runtime dependency; accepted target ownership. |
| Workbook contract | `Atlas_Architecture_Traceability.xlsx`, `Contracts!A14:E14` | K13 `PlaybookCatalogue`, owned by M08, governs replaceable definitions and eligibility, linked to C-033/C-034. |
| Workbook ownership edge | `Atlas_Architecture_Traceability.xlsx`, `Dependency Edges!A91:E91` | M08 owns K13. |
| Machine projection | `Atlas_Architecture_Machine_Readable.json`, `modules[module_id=M08]` | Same M08 ownership, interfaces, extension point, empty runtime dependency set and accepted target ownership. |
| Machine projection | `Atlas_Architecture_Machine_Readable.json`, `contracts[contract_id=K13]` | Same K13 owner and governed meaning. |

These accepted architecture records allocate ownership and target structure. Under the active plan and numbered authority, they do not independently admit behavioural selection or stand-down semantics.

## Bounded transformation assessment

### Structurally governed target

```text
versioned catalogue + governed playbook definitions
+ eligibility context + governed signal families + calendar/event constraints
→ M08 catalogue lookup, eligibility filtering and selection-metadata construction
→ playbook candidates + EligibilityDecision + metadata receipt
→ M05 serial candidate formation
```

This structure is supported by surface 5.10 and the M08/K13 allocation. The explicit registry/carrier seam and substitution boundary are governed.

### Missing decision authority

The current numbered corpus does not state:

1. which owner originates `catalogue_id`, `catalogue_version`, `playbook_definition_id`, `playbook_definition_version`, `candidate_family_id` and `eligibility_decision_id`;
2. the scope, uniqueness, stability, immutability and lawful absence rules for those identities;
3. whether a catalogue version is an immutable ordered snapshot, how replacement/removal changes it, and how a decision binds to the exact snapshot;
4. the exact mandatory eligibility input contract, including whether posture permission is an explicit mandatory M08 input rather than merely an earlier serial result;
5. the deterministic predicate, ordering, precedence and tie-break law for eligible candidates and lead selection;
6. whether `posture blocked`, `no eligible candidates`, `invalid catalogue`, `disabled definition` and `missing mandatory context` are distinct decision states and which exact output each emits;
7. the required decision reasons, candidate ordering, semantic fingerprint, as-of/effective time and receipt fields;
8. whether M08 is transient, configuration-backed or stateful beyond its configuration/metadata receipt, and the replacement/supersession rule for catalogue state;
9. which playbook-specific lifecycle facts may be carried to the expression stage without allowing M08 to decide exit/close, portfolio state or broker action.

Generic identifier, replay, fail-closed and replacement laws constrain any later contract but do not decide these M08-specific meanings.

## Identity, lineage, state, time and side effects

| Dimension | Current numbered authority | MLC-A result |
|---|---|---|
| Catalogue/playbook identity | M08 owns versioned definitions/catalogue; generic owner-issued identifier law applies. | Missing exact M08 identities, scopes and version-transition semantics. |
| Candidate identity/origin | Surface 5.10 emits playbook candidates; the serial spine forms the candidate. | Missing candidate-family owner/origin and identity semantics. |
| Decision identity | Generic replay law requires bounded output identity. | Missing `EligibilityDecision` identity and required fields. |
| Lineage | Generic replay law requires material playbook versions and consumed identities. | Missing exact catalogue-to-candidate-to-decision lineage contract. |
| State | Configuration/metadata receipt only; checked-in example registry is not live authority. | No M08 state/supersession model beyond that limit. |
| Time | Generic replay law separates effective/source time from emission time. | Missing M08 decision as-of/freshness semantics. |
| Side effects | Metadata receipt is selection evidence only. | No capital, broker, inventory or lifecycle mutation is authorised. |

## Substitution and stand-down challenge

- **Substitution:** sufficient at the structural level. A playbook can be added, removed or replaced behind the registry/contract without fixed-count orchestration or unrelated-module change.
- **Unknown/disabled definitions:** surfaced by historical C-033/C-034 design evidence, but no current numbered proposition gives the exact eligibility result or error taxonomy.
- **Posture block:** the numbered runtime order places posture before eligibility and generic law requires stand-down on missing/blocked required authority. It does not state that posture permission is a mandatory M08 input or define the M08 posture-block decision.
- **Empty eligible set:** no current numbered proposition defines a valid empty-set result, its reason, or whether it emits an M08 stand-down decision rather than only an empty candidate collection.
- **Deterministic lead:** no current numbered proposition defines order, priority, tie-break, stability or whether M08 or the later expression stage owns lead selection.
- **Lifecycle extension:** the later expression stage owns lifecycle intent, while exit/close belongs downstream. The contract for carrying playbook-specific lifecycle facts across that boundary is not defined.

## C/D evidence reconciliation

| Record | Current evidence | MLC-A use |
|---|---|---|
| C-033 | Requires candidate-family origin, registry version, composed selection and stand-down for posture block/empty set. | Confirms the missing proof question; does not supply normative meaning. |
| D-033 | Closed because annotation inspection did not prove actual consumption, propagation, filtering or absence of unrelated authority. | Remains a valid false-positive warning; no test observation or mutation performed. |
| C-034 | Requires deterministic lead selection, candidate identity, no broker/capital authority and lifecycle extension through contracts. | Confirms the missing identity/selection/lifecycle question; does not supply normative meaning. |
| D-034 | Historical proof authority recorded as ready but dependency-held behind D-033. | Cannot override current module-local MLC-A or create missing numbered authority. |

The historical 5.10 retained-test records were read only after current authority. Their registry, eligibility, duplicate, metadata and hidden-authority assertions remain evidence of earlier intent; under `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`, they cannot be reverse-promoted into normative authority.

## Contradictions and missing meaning

### Resolved status supersession

Core 5.10 records implementation truth as `reserved`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` explicitly supersedes it to `thin_seam`. This is a controlled supersession, not an unresolved contradiction.

### No ownership contradiction found

The numbered corpus, accepted M08/K13 allocation and prohibited-authority rules agree that:

- M08 owns catalogue/definition/eligibility meaning;
- M05 consumes M08 for serial candidate formation;
- M08 does not depend on M07 at runtime;
- M08 does not own capital, broker execution or portfolio lifecycle.

### Locked projection locator defect

`Atlas_Architecture_Traceability.xlsx` `Surface Map!G11` and the matching `Atlas_Architecture_Machine_Readable.json` surface-5.10 record cite `docs/02_BRIEFING_AND_BEHAVIOURAL_ARCHITECTURE_CORE.md`. That path does not exist in the source checkpoint. The routed current file is `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`. The workbook/JSON are locked in this assignment, so the defect is recorded and not repaired. It does not supply the missing M08 decision meaning.

### Blocking missing meaning

The nine items under “Missing decision authority” prevent truthful test-authority admission. Historical tests, current registry/code behaviour and Atlas trace records cannot lawfully fill them.

## Return boundary

Return to the existing routed numbered normative surface for one bounded M08 proposition package answering the exact worker-result question. Do not route tests, write proof, mutate catalogue/configuration or implement M08 before that authority is admitted and independently accepted.

`PROPOSED_M08_AUTHORITY_V1_AWAITING_LANE_4AT`


## 2026-07-31 fast-track C-NORM closure

### Disposition

`PASS:C-NORM:M08_K13_PLAYBOOK_CATALOGUE_AUTHORITY`

The historical blocker above is resolved by numbered authority rather than by code, example configuration or retained tests:

- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` section 7.8 defines `PlaybookDefinition`, `PlaybookCatalogue` and `EligibilityDecision`; immutable catalogue/definition/family identity and versions; mandatory posture/context facts; exact rejection and stand-down states; deterministic filtering, ordering, tie-break and eligibility-lead law; decision fingerprinting; lifecycle carriage; and state/replay/side-effect closure.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` section 10.17 admits those exact contract concepts under machine namespace `m08` while preserving M05 serial-stage and final candidate-expression ownership.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` section 11.10.3.2 fixes the exact K13 public-interface boundary and prohibits transitional registry/library/output surfaces from remaining competing canonical identities.
- `docs/vocabulary/vocabulary_registry.md` and the generated projection admit `m08.playbook_definition`, `m08.playbook_catalogue` and `m08.eligibility_decision`.

### Closure against the original blocker

| Former missing dimension | Closed authority |
|---|---|
| Catalogue, definition and family identity/version | sections 7.8.1–7.8.2 |
| Mandatory posture/context and required facts | section 7.8.3 |
| Invalid authority versus posture/empty stand-down | section 7.8.4 |
| Filtering, priority, tie-break and eligibility lead | section 7.8.5 |
| Decision identity, reasons, lineage and fingerprint | section 7.8.6 |
| Catalogue replacement/state/replay law | sections 7.8.2 and 7.8.7 |
| Bounded lifecycle carriage without foreign authority | sections 7.8.1, 7.8.6 and 7.8.7 |

### Evidence

- generated vocabulary projection parity: PASS — 153 entries and namespaces `global`, `m04`, `m07`, `m08`;
- M08 scoped vocabulary audit: PASS — zero unresolved candidates across 20 files;
- one shifted contextual repository-path occurrence was individually re-adjudicated; no global suppression was added;
- static normative assertions and `git diff --check`: PASS;
- M08 production/runtime configuration changes: none;
- existing vocabulary parity proof: 3 passed / 1 expected red because the previous assertion hard-codes only `global`, `m04` and `m07`.

Exact outputs and the full-read manifest are under `raw_validation/fast_track_k13_v1/`. The next gate is `C-PROOF`; M08 Gate D remains closed.


## 2026-07-31 fast-track C-PROOF acceptance

### Disposition

`PASS:C-PROOF:GATE_D_OPEN:M08_K13_PLAYBOOK_CATALOGUE_AUTHORITY`

The accepted section 7.8 proposition is now protected by one bounded Tier A
public-seam family:

- `tests/support/m08_k13_contract_harness.py` supplies a deterministic reference
  resolver and five explicit false-positive mutants;
- `tests/tier_a/m08_k13/test_m08_k13_contract.py` proves missing authority versus
  lawful stand-down, posture block, no-family/no-eligible distinctions,
  authority priority, identity/version tie-break, required-fact rejection,
  deterministic lineage, lifecycle carriage and foreign-authority closure;
- seven production-facing cases define the target public seam and remain exact
  expected red because `nvda_desk.m08_playbook_catalogue` does not yet exist.

### Proof result

| Check | Result |
|---|---|
| Reference and mutant proof | PASS — 11 / 11 |
| Named false-positive mutants | PASS — 5 / 5 killed |
| Production-facing seam | EXPECTED RED — 11 passed / 7 failed; all seven fail at the absent canonical package |
| Vocabulary namespace parity | PASS — 4 / 4 |
| Proof-block manifest | PASS — 56 / 56 |
| Proof-executor contract | PASS — 21 / 21 |
| M08 scoped vocabulary audit | PASS — zero unresolved candidates across 22 files |
| Production/config mutation | none |

The proof uses no skip, xfail, weakened assertion, fake production fixture or
implementation substitution. The namespace-parity assertion was updated only
to the already-admitted `global`, `m04`, `m07`, `m08` projection and the exact
three M08 identities. Two proof-scope vocabulary candidates were resolved by
exact occurrence disposition; no new alias or global suppression was added.

### Gate D boundary

Opened:

- one explicit package API for `PlaybookDefinition`, `PlaybookCatalogue` and
  `EligibilityDecision`;
- owner-local deterministic catalogue validation and eligibility resolution;
- direct transitional adapters only where required to preserve compatibility.

Closed:

- M05 candidate-expression/final-candidate authority;
- caller/container ordering, hidden live state, wall-clock inference and runtime
  self-tuning;
- capital, broker/order, inventory/position, exit/close, coefficient, source,
  replay or transaction authority;
- unrelated module, configuration or test changes.

Exact evidence is retained under
`raw_validation/fast_track_k13_c_proof_v1/`.
