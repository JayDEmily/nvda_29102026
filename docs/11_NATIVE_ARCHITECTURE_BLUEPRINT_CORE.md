# 11 Native Architecture Blueprint Core

Status: accepted normative architecture authority  
Acceptance receipt: `var/audit/ledgers/native_blueprint/acceptance_receipt.json`  
Document class: primary code-structure architecture document under the `docs/01_NORMATIVE_CORE.md` authority hierarchy  
Scope: native codebase structure, sequential architecture surfaces, ownership, seams, persistence, tests, reservations, and migration traceability  
Purpose: prevent messy code from being created, preserved, normalised, or migrated into the native repo

---

## 0. Core law

The native NVDA codebase must be structured as a clean target-state codebase.

All production code, tests, contracts, repositories, adapters, schemas, services, configuration surfaces, and migration work must conform to the target architecture defined by this document.

Current-state mess does not define future structure. Legacy convenience does not define target ownership. Migration pressure does not justify blurred package placement, hidden coupling, mixed responsibilities, or unclear seams.

A code change is not architecturally valid unless the affected capability can be assigned to:

1. a target package or subpackage;
2. a target module or component form;
3. an owning authority;
4. a lawful seam and carrier, where a boundary is crossed;
5. a persistence owner, where state is stored or read;
6. a test family, where behaviour or structure requires proof;
7. a traceability path, where migration or current-state carry-forward is involved;
8. an honest structural status: `Locked`, `Provisional`, or `Reserved`;
9. an honest implementation-truth status: `implemented`, `thin_seam`, `placeholder`, `reserved`, `future_only`, `legacy_only`, or `rejected`.

---

## 1. What this document is

This document is the target architecture benchmark for the native deterministic NVDA repo.

It governs package, module, component, seam, persistence, test, reservation, migration-allocation, traceability, and sequential runtime/control-surface structure.

It defines what good code structure means before implementation, migration planning, or refactor execution occurs.

It is first-class native code-structure authority within the `docs/01_NORMATIVE_CORE.md` authority hierarchy. It does not outrank the normative hierarchy that governs it.

It does not need source-provenance language inside the normative body.

---

## 2. What this document is not

This document is not a migration sequence.

This document is not a file-by-file refactor plan.

This document is not a work ledger.

This document is not an implementation task list.

This document is not permission to collapse target architecture into current-state compromises.

This document does not make messy code acceptable because equivalent behaviour already exists somewhere in the repo.

---

## 3. Status models

This document uses two separate status models. They must not be conflated.

### 3.1 Structural status

Every target architecture item uses one of three structural status values.

| Status | Meaning | Rule |
|---|---|---|
| `Locked` | The benchmark shape is fixed now. | Code must conform to it. |
| `Provisional` | The likely target shape is known, but final details are not fixed. | Code may proceed only within the stated bounded shape. |
| `Reserved` | The target role is known, but the final allocation is unresolved. | Code must not guess or hard-code the unresolved allocation. |

A structural status value is not a progress label.

`Reserved` is not a defect. Hidden ambiguity is a defect.

### 3.2 Implementation-truth status

Every sequential architecture surface must carry exactly one implementation-truth status.

| Status | Meaning | Rule |
|---|---|---|
| `implemented` | Native code and proof surfaces currently satisfy the surface. | The claim must cite native code and proof evidence. |
| `thin_seam` | A lawful native seam exists, but behaviour is incomplete. | The surface must not be described as mature implemented behaviour. |
| `placeholder` | A named native shell exists with little or no behaviour. | The surface must not be treated as behaviourally complete. |
| `reserved` | Architecture reserves the surface, and native implementation is not present. | Later admissibility work is required before implementation. |
| `future_only` | Planned future surface with no current native implementation. | It must not be used as current runtime truth. |
| `legacy_only` | Found only in legacy or Atlas evidence. | It must not become native architecture without later admissibility work. |
| `rejected` | Not part of native architecture. | The reason for rejection must be stated. |

A surface marked `implemented` must cite native code and proof evidence.

A surface marked `thin_seam`, `placeholder`, `reserved`, or `future_only` must not be described as completed runtime behaviour.

Durable architecture terms used by this document must be governed by `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` before freeze. A target term that is not governed, admitted, aliased, or explicitly quarantined by the vocabulary process is not accepted normative language.

---

## 4. Primary control surfaces

The native architecture is controlled through the following surfaces.

| Control surface | Governs | Required decision before code is accepted |
|---|---|---|
| Sequential Native Architecture Surfaces | Top-to-bottom runtime/control architecture from source ingress to review and proof. | Which architecture surface owns the capability. |
| Target Structure | Target package and subpackage families. | Where the code belongs. |
| Component Skeleton | Module-level component shape. | What component form the code takes. |
| Ownership Matrix | Capability ownership and forbidden placement. | Who owns the capability. |
| Seam Contracts | Boundary crossings and carrier rules. | How data crosses a boundary. |
| Bridge and Shell Policy | Transitional, advisory, optional, and shell surfaces. | Whether partial surfaces are lawful and how they are labelled. |
| Persistence Architecture | State ownership, writers, readers, repositories, and stores. | Who may write and who may read durable state. |
| Test Architecture | Required architecture test families. | What must prove the structure or behaviour. |
| Reservations | Bounded unresolved allocations. | What must stay open rather than guessed. |
| Module Allocation Appendix | Migration-facing module allocation detail. | How current or donor material maps into target structure without overriding it. |
| Traceability Appendix | Current-state and donor traceability. | Why carried-forward material exists and where it must land. |

No other control surface may silently override these surfaces.

---

## 5. Sequential Native Architecture Surface law

The native architecture must be described top-to-bottom from source ingress to review and proof.

The blueprint must not start at the serial desk-cognition spine.

The following eighteen architecture surfaces are the required order for native architecture discussion, review, migration allocation, and Bridge satisfaction mapping.

The term `architecture surface` is the normative term in this document. The informal architecture metaphor must not be used as normative language.

### 5.1 External source interfaces and API ingress

| Required field | Normative value |
|---|---|
| Purpose | Lawful outer boundary for external market, options, broker, calendar, and reference inputs before native preparation. |
| Target owner | ingress and adapter authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | external payloads; broker/API responses; checked-in reference artefacts; operator source bundles. |
| Lawful outputs | typed native ingress carriers; adapter outputs; source validation results. |
| Prohibited decisions | domain decisions; trading decisions; persistence authority; hidden mutation of downstream state. |
| Downstream consumers | raw capture; calendar/reference architecture; prepared ingress. |
| Vocabulary terms used | external source interface; API ingress; adapter; typed carrier. |
| Proof interface | adapter tests; carrier validation tests; source-shape proof; boundary rejection proof. |
| Seam boundaries | external data crosses only through explicit adapters and typed carriers. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.2 Raw capture and source temporal law

| Required field | Normative value |
|---|---|
| Purpose | Raw capture, source timestamp treatment, source session context, and preservation of source-time truth before runtime interpretation. |
| Target owner | raw capture and source-temporal authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | typed ingress carriers; source timestamps; capture metadata; session/source metadata. |
| Lawful outputs | raw capture records; source-time-normalised carriers; capture receipts. |
| Prohibited decisions | runtime regime decisions; candidate formation; capital decisions; retrospective timestamp rewriting. |
| Downstream consumers | raw signal families; financial/event calendar architecture; prepared ingress. |
| Vocabulary terms used | raw capture; source temporal law; capture receipt; source timestamp. |
| Proof interface | capture fixture tests; timestamp invariant tests; replay determinism tests. |
| Seam boundaries | raw capture may feed preparation and audit ledgers but must not bypass preparation into cognition or downstream authority. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.3 Raw signal families

| Required field | Normative value |
|---|---|
| Purpose | Native grouping of raw and minimally-derived signal families before runtime preparation. |
| Target owner | raw signal family authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | raw market data; raw options chain data; raw volatility references; raw calendar/event context; source-normalised capture outputs. |
| Lawful outputs | typed raw signal family carriers and eligibility for preparation. |
| Prohibited decisions | runtime scoring; play selection; posture/risk decisions; downstream deployment decisions. |
| Downstream consumers | prepared ingress; temporal/context preparation; calendar/event context. |
| Vocabulary terms used | raw signal family; market snapshot; options surface; volatility reference. |
| Proof interface | signal schema tests; fixture round-trip tests; source-family boundary tests. |
| Seam boundaries | raw signal families stay upstream of cognition. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.4 Financial and event calendar architecture

| Required field | Normative value |
|---|---|
| Purpose | Checked calendar truth, event reference material, event projection, and calendar-derived runtime authority. |
| Target owner | financial calendar authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | checked-in calendar/reference sources; event records; market-session metadata; source-time references. |
| Lawful outputs | calendar authority packets; event-context projections; session/event context for preparation. |
| Prohibited decisions | candidate formation; trading instruction; capital sizing; hidden online calendar mutation. |
| Downstream consumers | prepared ingress; temporal context; serial desk-cognition spine; Parallel Risk Lane. |
| Vocabulary terms used | Financial Calendar Crosswalk; event calendar; calendar authority; event projection. |
| Proof interface | calendar import tests; projection tests; checked-reference parity tests; event-window tests. |
| Seam boundaries | calendar authority enters runtime through governed projection carriers. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.5 Prepared ingress and runtime context preparation

| Required field | Normative value |
|---|---|
| Purpose | Conversion of raw/captured/reference material into runtime-ready typed inputs. |
| Target owner | runtime preparation authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | raw signal family carriers; calendar authority packets; source-temporal material; configuration authority. |
| Lawful outputs | prepared runtime substrate; stage input carriers; context packets. |
| Prohibited decisions | serial stage decisions; risk decisions; capital decisions; direct persistence writes unless explicitly assigned. |
| Downstream consumers | DMPV3 packet carriage; serial desk-cognition spine; parallel risk lane. |
| Vocabulary terms used | runtime preparation; prepared substrate; context preparation; stage input carrier. |
| Proof interface | preparation tests; contract tests; replay fixture tests; rejection tests for incomplete inputs. |
| Seam boundaries | preparation is the lawful seam between upstream evidence and runtime cognition. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.6 DMPV3 packet carriage

| Required field | Normative value |
|---|---|
| Purpose | True inter-module packet carriage at deliberate runtime boundaries. |
| Target owner | DMPV3 packet authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | serial runtime outputs; admitted packet payloads; bounded parallel-risk inputs; runtime receipts. |
| Lawful outputs | DMPV3 envelopes; DeskModulePacketV3 carriers; packet receipts. |
| Prohibited decisions | raw ingress carriage; every internal serial step; business logic; persistence truth by implication. |
| Downstream consumers | parallel risk lane; downstream capital deployment authority; persistence/receipts; review/replay. |
| Vocabulary terms used | DMPV3; packet carriage; envelope; DeskModulePacketV3. |
| Proof interface | packet schema tests; boundary fixture tests; replay equivalence tests; no-DMP-upstream checks. |
| Seam boundaries | DMPV3 begins at deliberate inter-module packet boundaries. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.7 Serial desk-cognition spine

| Required field | Normative value |
|---|---|
| Purpose | Ordered candidate formation through the serial runtime stages. |
| Target owner | serial desk-cognition authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | prepared runtime substrate; temporal context; Market Regime Context; options/flow context; posture inputs; eligibility inputs; execution-stage inputs. |
| Lawful outputs | serial candidate outputs; stage packets; execution candidate material. |
| Prohibited decisions | parallel risk independence; capital deployment authority; live position management; persistence writes unless explicitly assigned. |
| Downstream consumers | DMPV3 packet carriage; parallel risk lane; downstream pre-deployment gate; capital deployment authority; review. |
| Vocabulary terms used | serial desk-cognition spine; temporal stage; regime stage; options/flow stage; posture; eligibility; execution. |
| Proof interface | stage-order tests; stage contract tests; deterministic replay tests; no-capital-leakage tests. |
| Seam boundaries | serial cognition emits bounded outputs and must not decide capital deployment. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.8 Parallel risk lane

| Required field | Normative value |
|---|---|
| Purpose | Independent risk assessment outside the serial desk-cognition spine. |
| Target owner | parallel risk authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | admitted bounded serial packets; risk context; market/caution context; configuration authority. |
| Lawful outputs | parallel risk packet; independent risk envelope; caution/block signals. |
| Prohibited decisions | serial candidate formation; capital deployment sizing; mutation of serial stage internals; hidden upstream reads. |
| Downstream consumers | downstream capital deployment authority; review/replay; persistence/receipts. |
| Vocabulary terms used | parallel risk lane; independent risk; risk envelope; risk packet. |
| Proof interface | risk-lane contract tests; independence tests; packet-in/out tests; hidden-read rejection tests. |
| Seam boundaries | parallel risk consumes only lawful bounded packets and emits its own product. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.9 Dynamic coefficient and modifier authority

| Required field | Normative value |
|---|---|
| Purpose | Bounded coefficient, threshold, modifier, and state-conditioned adjustment authority. |
| Target owner | coefficient and modifier authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | governed coefficient config; state context; admitted runtime context; vocabulary-lawful coefficient families. |
| Lawful outputs | bounded coefficients; modifier packets; applied-threshold decisions. |
| Prohibited decisions | unbounded runtime mutation; hidden strategy changes; capital deployment decisions; source-data ingestion. |
| Downstream consumers | serial spine stages; parallel risk lane; playbook eligibility; review/proof. |
| Vocabulary terms used | dynamic coefficient; modifier authority; coefficient authority; bounded coefficient. |
| Proof interface | config schema tests; bounds tests; state-conditioned modifier tests; replay determinism tests. |
| Seam boundaries | modifier surfaces influence authorised runtime surfaces only through governed coefficient/config carriers. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.10 Playbook library architecture

| Required field | Normative value |
|---|---|
| Purpose | Target home for governed playbook definitions, eligibility constraints, play selection rules, and proofable playbook metadata. |
| Target owner | playbook library authority. |
| Structural status | `Provisional`. |
| Implementation-truth status | `reserved`. |
| Lawful inputs | vocabulary-lawful playbook definitions; eligibility context; governed signal families; calendar/event constraints. |
| Lawful outputs | playbook candidates; Playbook Eligibility; playbook metadata receipts. |
| Prohibited decisions | capital deployment; raw source ingestion; uncontrolled strategy mutation; hidden coefficient ownership. |
| Downstream consumers | serial desk-cognition spine; eligibility; execution candidate formation; review/proof. |
| Vocabulary terms used | playbook library; playbook eligibility; play selection; setup family. |
| Proof interface | future playbook registry tests; eligibility tests; no-hidden-playbook tests. |
| Seam boundaries | playbook material crosses into runtime through explicit registry/eligibility carriers. |
| Evidence basis | reserved because final target allocation requires later admissibility and implementation evidence. |

### 5.11 Downstream capital deployment authority

| Required field | Normative value |
|---|---|
| Purpose | Downstream decision that determines whether and how much capital may be deployed after serial and parallel products exist. |
| Target owner | capital deployment authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `placeholder`. |
| Lawful inputs | serial candidate material; downstream pre-deployment result; parallel risk packet; capital state; bounded deployment policy; final join/risk product. |
| Lawful outputs | deploy/stand-down decision; authorised deployable percentage; authorised notional; capital-deployment receipt. |
| Prohibited decisions | candidate formation; serial execution-stage decisions; parallel risk generation; opening placement mechanics. |
| Downstream consumers | opening architecture and placement readiness; persistence/receipts; review. |
| Vocabulary terms used | capital deployment authority; authorised deployable percentage; capital state; stand-down. |
| Proof interface | capital precondition tests; cap/bounds tests; no-spine-capital tests; downstream receipt tests. |
| Seam boundaries | posture permission may reach capital deployment authority only through serial candidate material or downstream pre-deployment result; capital deployment authority consumes it as deployment precondition material and must not recompute posture permission or form the candidate. |
| Evidence basis | placeholder because downstream authority must not be treated as mature behaviour without proof. |

### 5.12 Opening architecture and placement readiness

| Required field | Normative value |
|---|---|
| Purpose | Downstream opening authorisation, placement readiness, and handoff structure after deployment authority. |
| Target owner | downstream opening authority. |
| Structural status | `Provisional`. |
| Implementation-truth status | `placeholder`. |
| Lawful inputs | capital deployment decision; candidate execution material; account/broker readiness context; placement constraints. |
| Lawful outputs | opening snapshot; placement readiness result; placement handoff material. |
| Prohibited decisions | capital sizing; serial candidate formation; parallel risk evaluation; broker adapter implementation detail beyond handoff contract. |
| Downstream consumers | execution bridge; persistence/receipts; live inventory. |
| Vocabulary terms used | opening architecture; placement readiness; placement handoff; downstream opening. |
| Proof interface | opening contract tests; placement readiness tests; handoff invariant tests. |
| Seam boundaries | opening and placement surfaces receive downstream authority outputs. |
| Evidence basis | placeholder because current downstream opening behaviour is expected to be thin until later implementation leaves. |

### 5.13 Live position and inventory architecture

| Required field | Normative value |
|---|---|
| Purpose | Live position, inventory, exposure, and capital-state read/write structure after entry. |
| Target owner | live inventory and position authorities. |
| Structural status | `Provisional`. |
| Implementation-truth status | `placeholder`. |
| Lawful inputs | execution receipts; fill/state updates; capital state; position repository state; risk limits. |
| Lawful outputs | live inventory snapshot; position state; exposure state; capital/inventory receipts. |
| Prohibited decisions | new candidate formation; raw signal preparation; direct broker placement decisions; ungoverned capital mutation. |
| Downstream consumers | exit and close architecture; review/replay; persistence/ledgers. |
| Vocabulary terms used | live inventory; position repository; exposure; inventory snapshot. |
| Proof interface | repository tests; fill-feedback tests; position-state invariant tests; capital-state consistency tests. |
| Seam boundaries | live inventory consumes execution/state receipts through lawful persistence seams. |
| Evidence basis | placeholder because current live inventory behaviour is expected to be thinner than target behaviour. |

### 5.14 Exit and close architecture

| Required field | Normative value |
|---|---|
| Purpose | Target home for exit strategy, close execution, trimming, profit-taking, trailing stop, and position wind-down behaviour. |
| Target owner | exit and close authority. |
| Structural status | `Provisional`. |
| Implementation-truth status | `reserved`. |
| Lawful inputs | live position state; risk context; playbook/exit policy; market state; broker/execution constraints. |
| Lawful outputs | exit decision; close execution handoff; exit receipt; position closure state. |
| Prohibited decisions | initial candidate formation; capital deployment sizing; raw source ingestion; hidden live-inventory mutation. |
| Downstream consumers | execution bridge; live inventory; persistence/receipts; review. |
| Vocabulary terms used | exit strategy; close execution; trailing stop; take profit; position wind-down. |
| Proof interface | future exit-policy tests; close handoff tests; position-closure replay tests. |
| Seam boundaries | exit decisions are downstream of live position/inventory state. |
| Evidence basis | reserved because exact native implementation allocation requires later admissibility work. |

### 5.15 Review and explanation layer

| Required field | Normative value |
|---|---|
| Purpose | Post-runtime explanation, trace review, replay comparison, and human-readable review surfaces. |
| Target owner | review and explanation authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | runtime receipts; packets; decisions; proof outputs; ledger entries; replay artefacts. |
| Lawful outputs | review records; explanation packets; replay comparison outputs; audit summaries. |
| Prohibited decisions | online self-learning; live trading decisions; mutation of production state; hidden strategy changes. |
| Downstream consumers | persistence/ledgers; research/replay; implementation proof workflow. |
| Vocabulary terms used | review explanation; replay; trace review; audit receipt. |
| Proof interface | review packet tests; replay comparison tests; explanation determinism tests. |
| Seam boundaries | review consumes completed runtime evidence and must not alter live decisions. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.16 Persistence, ledgers, and receipts

| Required field | Normative value |
|---|---|
| Purpose | Durable truth, audit ledgers, receipts, repositories, and replayable state records. |
| Target owner | persistence and ledger authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | authorised writer outputs; runtime receipts; proof receipts; state transitions; ledger records. |
| Lawful outputs | durable state; audit ledgers; receipt files; repository read models. |
| Prohibited decisions | candidate formation; risk decisions; hidden runtime orchestration; duplicate truth without reconciliation. |
| Downstream consumers | review/replay; live inventory; capital state; testing/proof. |
| Vocabulary terms used | persistence; ledger; receipt; repository; audit record. |
| Proof interface | JSON validation tests; duplicate-ID tests; repository tests; replayability tests. |
| Seam boundaries | only authoritative writers may write durable truth. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.17 Testing, proof, and checkpoint surfaces

| Required field | Normative value |
|---|---|
| Purpose | Proof families, test tiers, checkpoint declarations, promotion gates, and evidence required for architectural claims. |
| Target owner | testing and proof authorities. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | architecture claims; code changes; ledger outputs; proof requirements; checkpoint declarations. |
| Lawful outputs | Tier A/B/C proof results; checkpoint receipts; validation reports; promotion decisions. |
| Prohibited decisions | production decision logic; architecture authority by green tests alone; hidden acceptance of wrong package ownership. |
| Downstream consumers | all architecture surfaces; process/tranche law; review/replay. |
| Vocabulary terms used | Tier A proof; Tier B proof; Tier C proof; checkpoint; promotion; retained test. |
| Proof interface | retained-test registry checks; proof-block tests; checkpoint tests; validation command capture. |
| Seam boundaries | testing proves claims at the correct boundary. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

### 5.18 Vocabulary governance interface

| Required field | Normative value |
|---|---|
| Purpose | Durable term admission, aliases, quarantines, synonym collision handling, and canonical vocabulary regeneration. |
| Target owner | vocabulary governance authority. |
| Structural status | `Locked`. |
| Implementation-truth status | `thin_seam`. |
| Lawful inputs | candidate durable terms; aliases; disallowed phrases; synonym candidates; architecture-surface language. |
| Lawful outputs | admitted terms; alias records; quarantined terms; canonical vocabulary JSON; vocabulary proof receipts. |
| Prohibited decisions | runtime trading decisions; architecture decisions without authority; user vernacular leakage into normative docs. |
| Downstream consumers | all normative/control documents; planning briefs; tests/proof surfaces. |
| Vocabulary terms used | vocabulary governance; durable term; alias; quarantine; canonical vocabulary. |
| Proof interface | vocabulary builder parity tests; synonym audit tests; disallowed-phrase checks; canonical JSON validation. |
| Seam boundaries | durable language enters normative surfaces only through governed vocabulary admission. |
| Evidence basis | The `thin_seam` status remains until native code and proof evidence justify a lawful `implemented` status in the acceptance ledger. |

---

## 6. Target Structure law

Target Structure governs package and subpackage placement.

Each target package or subpackage must have:

1. one bounded responsibility;
2. allowed contents;
3. forbidden contents;
4. preferred component forms;
5. an honest structural status.

Code must be placed by target responsibility, not by historical file location, local convenience, or similarity of names.

A package must not become a dumping ground for unrelated services, schemas, adapters, repositories, orchestration, tests, and configuration.

A subpackage must not own behaviour that belongs to another layer simply because the dependency is nearby.

If a capability does not have a lawful package home, the capability is `Reserved` until the target home is resolved.

---

## 7. Component Skeleton law

Component Skeleton governs the internal shape of modules.

Every module must have a coherent primary responsibility.

A component must use the correct form for its job:

| Component form | Owns | Must not own |
|---|---|---|
| Adapter | External boundary translation. | Core domain decisions. |
| Contract | Data shape crossing a boundary. | Runtime behaviour. |
| Schema or model | Validated data structure. | Service orchestration. |
| Service | Runtime operation or domain action. | Persistence authority unless explicitly assigned. |
| Repository or store | Durable state read/write boundary. | Candidate formation or strategy logic. |
| Orchestrator | Ordered coordination. | Hidden business rules outside authorised stages. |
| Configuration authority | Governed parameters and allowed values. | Ad hoc runtime mutation. |
| Test surface | Proof of structure or behaviour. | Production decision logic. |

A module must not mix component forms unless the target architecture explicitly allows that mixture.

Helper functions do not define ownership. Ownership is defined by bounded responsibility and target component form.

---

## 8. Ownership Matrix law

Ownership Matrix governs capability ownership.

Every major capability or concept must have:

1. a target owner;
2. a target module or area;
3. a preferred form;
4. an input carrier, where applicable;
5. an output carrier, where applicable;
6. forbidden placement;
7. an honest status.

A capability must not be implemented in two places with competing authority.

A capability must not be placed in an adapter, schema, repository, or test merely because that location is convenient.

A capability must not be carried forward from legacy code until its target owner is known or explicitly reserved.

Where ownership is unresolved, the correct action is `Reserved`, not implicit implementation.

---

## 9. Seam Contract law

Seam Contracts govern boundaries between architecture surfaces.

A seam must define:

1. upstream owner;
2. downstream owner;
3. carrier type;
4. required invariants;
5. persistence side effects;
6. allowed variants;
7. forbidden variants;
8. carrier family;
9. seam category;
10. traceability reference, where migration is involved.

A boundary crossing must use an explicit carrier or contract.

Data must not cross architecture boundaries through hidden imports, shared mutable objects, implicit globals, undocumented dictionaries, or test-only shortcuts.

A seam must not become an owner of the decisions it transports.

A carrier must not become business logic.

A downstream surface must not read upstream internals if the seam defines a lawful carrier.

---

## 10. Bridge and Shell Policy law

Bridge and Shell Policy governs transitional, advisory, optional, and shell surfaces.

A partial surface is lawful only when it is explicitly labelled and bounded.

A bridge or shell must define:

1. target home;
2. allowed behaviour;
3. required label;
4. forbidden behaviour;
5. target resolution path;
6. honest status.

A shell must not masquerade as completed behaviour.

A bridge must not become permanent architecture by inertia.

An advisory surface must not make binding runtime decisions unless the target architecture assigns that authority.

A transitional surface must have a resolution path or a reservation.

---

## 11. Persistence Architecture law

Persistence Architecture governs durable state.

Every persistence domain must define:

1. authoritative writer;
2. primary readers;
3. persistence class;
4. bootstrap or fallback rule;
5. forbidden mixing;
6. target repository or store module;
7. traceability reference, where migration is involved.

Only the authoritative writer may write durable truth for a persistence domain.

Readers must consume through lawful repository, store, contract, or query surfaces.

Persistence must not be mixed with candidate formation, orchestration, adapter translation, schema validation, or tests unless explicitly assigned.

State must not be duplicated into competing durable stores without a governed reconciliation rule.

A bootstrap or fallback path must not silently become normal runtime authority.

---

## 12. Test Architecture law

Test Architecture governs proof families, not individual test-case trivia.

Every benchmark family must map to a required test family.

A test family must define:

1. primary scope;
2. target subsystem;
3. failure signal;
4. notes or constraints;
5. honest status.

Tests must prove the architecture claim they are attached to.

A green test does not make code architecturally valid if the code is in the wrong package, wrong module form, wrong ownership boundary, wrong seam, or wrong persistence domain.

A test must not encode a messy current-state compromise as future architecture truth.

Where code structure is governed, tests must verify the boundary that matters, not merely execute the path.

---

## 13. Reservations and Provisional Allocations law

Reservations govern bounded open questions.

A reservation must define:

1. the open allocation point;
2. why it is not locked yet;
3. bounded options;
4. evidence required to resolve it;
5. current benchmark constraint;
6. owner to decide later;
7. likely target home, where known;
8. traceability reference, where migration is involved.

Unresolved architecture must be visible.

A reserved item must not be implemented as though it were locked.

A provisional item must not expand beyond its bounded options.

A developer must not create a new target home to avoid resolving a reservation.

---

## 14. Module Allocation Appendix law

Module allocation is migration-facing detail.

It assists current-state and donor material in finding target homes.

It must not override Target Structure, Component Skeleton, Ownership Matrix, Seam Contracts, Persistence Architecture, Test Architecture, or Reservations.

A module allocation entry must define:

1. target package;
2. target subpackage;
3. target module;
4. bounded responsibility;
5. preferred form;
6. primary inputs;
7. primary outputs;
8. forbidden co-location;
9. observed current basis, where relevant.

A current file must not be moved or rewritten directly into the native repo unless its target allocation is lawful.

Observed current basis explains what exists. It does not authorise preserving messy structure.

---

## 15. Traceability Appendix law

Traceability is migration evidence.

It explains why current-state or donor material was carried forward.

It must not pollute canonical target architecture.

A traceability entry must define:

1. traceability reference;
2. target surface;
3. donor or current-state source;
4. observed current basis;
5. reason carried forward.

Traceability must not become implementation authority.

A traceability reference is valid only when it leads to a lawful target package, component form, owner, seam, persistence owner, and test family.

---

## 16. Anti-mess law

The following patterns are prohibited:

1. mixed-responsibility modules;
2. business logic inside adapters;
3. orchestration hidden inside schemas or contracts;
4. persistence writes from non-authoritative surfaces;
5. shared mutable state across architecture boundaries;
6. implicit carriers where a seam requires a contract;
7. duplicate owners for the same capability;
8. test fixtures that become runtime authority;
9. migration code that bypasses target ownership;
10. reserved decisions implemented as if locked;
11. provisional decisions expanded beyond their bounded shape;
12. bridge or shell surfaces presented as completed behaviour;
13. code placement based on legacy file location rather than target architecture;
14. current-state compromise treated as native design.

A patch containing any prohibited pattern fails architecture review.

---

## 17. Acceptance rule for code changes

A code change is architecturally acceptable only when the reviewer can answer the following questions without guessing.

| Question | Required answer |
|---|---|
| Where does this belong? | Target package, subpackage, and module. |
| What form is it? | Adapter, contract, schema, service, repository, orchestrator, configuration authority, or test surface. |
| Who owns it? | One target owner. |
| What may it consume? | Lawful inputs or carriers. |
| What may it emit? | Lawful outputs or carriers. |
| What boundary does it cross? | Explicit seam contract, or no boundary crossing. |
| Does it persist state? | Authoritative writer and primary readers, or no persistence. |
| What proves it? | Required test family and failure signal. |
| Is anything unresolved? | `Reserved` or `Provisional` with bounded options. |
| Is any current-state mess being preserved? | No. |

If any answer is missing, the change is incomplete.

If any answer depends on undocumented inference, the change is incomplete.

If any answer contradicts a locked target structure, the change is rejected.

---

## 18. Acceptance rule for this document

This document is sufficient when each in-scope major capability can be assigned to:

1. target package or subpackage;
2. target module;
3. component form;
4. seam owner;
5. persistence owner;
6. test family;
7. traceability path;
8. `Locked`, `Provisional`, or `Reserved` status.

This document fails if it becomes a migration plan, a receipt ledger, a trading-flow essay, or a justification of current-state mess.

---

## 19. One-line rule

Write and refactor code into the clean target architecture; do not create, preserve, normalise, or migrate messy code.
