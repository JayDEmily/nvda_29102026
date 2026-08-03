# NVDA Canonical Feature Evolution Methodology — Version 2

**Status:** audited methodology for proposed adoption; it does not amend repository authority by itself
**Audit date:** 2026-08-03
**Repository baseline:** `74d2f2c3fa403538fd11e428a928c5de517dc165` (`work/m03-m05-semantic-continuity-repair-v1`)
**Supersedes:** `NVDA_CANONICAL_FEATURE_EVOLUTION_METHODOLOGY_DRAFT_20260803.md`
**Language:** Australian English

## 0. Decision and outcome

The first draft should **not** be adopted unchanged.

Its central decision is sound: retain the existing six-stage route and enrich it rather than create another gate stack. Version 2 preserves:

`definition → governing alignment → tests → implementation → validation → gated integration`

and the existing local promotion direction:

`C-NORM → C-PROOF → Gate D`

Version 2 corrects the parts that could otherwise authorise the wrong feature, the wrong owner, an unsafe compatibility period or an unproved completion claim. The material changes are:

1. establish current implementation truth and falsify the request premise **before** classifying the change;
2. separate an umbrella feature outcome from its owner-local semantic propositions;
3. use consequence tags rather than forcing one primary change class;
4. trace both direction and impact dimension, then reconcile the prospective trace against the actual diff;
5. keep old and new contract authority explicit during a versioned migration instead of declaring the new contract the sole meaning too early;
6. make cutover, data migration, crash behaviour, rollback and retirement first-class where triggered;
7. distinguish owner-local availability, composed shadow use, active bounded use, consumer migration and compatibility retirement;
8. block semantic progression when the requested target or numeric meaning is Unknown;
9. treat tests and vocabulary scans as bounded evidence, not semantic certificates; and
10. correct the four worked cases against the current repository.

This method introduces no fourth gate, new maturity tier or replacement status vocabulary. Its labels and tags are change-record aids only unless separately admitted through repository governance.

## 1. Governing position

### 1.1 Authority remains above the method

This method is subordinate to the repository authority hierarchy, the active bounded pack, the current ExecPlan and continuation route, the numbered normative corpus, the Gate C protocol and the accepted M00–M15 ownership allocation.

For the audited baseline, the controlling propositions include:

- one accepted owner and one public seam per behaviour;
- normative authority before truthful proof before implementation;
- current implementation truth proved directly rather than inferred from plans, paths, receipts or test colour;
- compatibility paths subordinate to canonical owners;
- M13 as transaction/storage mechanism rather than owner of domain meaning;
- M14 and M15 as governance planes rather than universal runtime dependencies;
- risk-triggered independent validation for irreversible or high-consequence changes; and
- serial canonical integration even when bounded delivery work is parallel.

If this method conflicts with current routed authority, the routed authority wins and the change record is blocked until the conflict is resolved.

### 1.2 Existing route, expanded obligations

The method adds evidence and decisions inside the existing route:

| Existing stage | Required evolution work |
|---|---|
| Definition | Authority intake; exact outcome; premise falsification; current-state classification; proposition decomposition; consequence tags; impact map; Unknowns and non-goals. |
| Governing alignment | Owner/seam and exclusions; contract/version law; identity/time/state; compatibility/cutover; persistence/replay; vocabulary only where triggered; `C-NORM`. |
| Tests | Minimum truthful public-seam proof; conforming case; material prohibited case; plausible false positive; migration/failure proof where triggered; `C-PROOF`. |
| Implementation | Smallest dependency-closed owner-local slices; explicit composition; bounded adapters; migrations and telemetry where authorised. |
| Validation | Targeted and affected proof; architecture, dependency, vocabulary, state and replay checks where affected; actual-diff impact reconciliation; accepted aggregate and shadow routes. |
| Gated integration | Serial integration; activation/cutover decision; exact claim boundary; consumer-migration and retirement follow-up; concise reproducible evidence. |

## 2. Audit of the first draft

| First-draft weakness | Why it matters | Version 2 correction |
|---|---|---|
| Classification preceded repository discovery. | It can turn an already-existing, compatibility-only or incorrectly owned capability into a false “new feature”. | Perform authority intake and current-state premise falsification first; classification remains provisional until evidence is complete. |
| One “concept owner” could be read as one owner for a cross-module outcome. | Persistence, packet carriage, domain meaning, replay interpretation and composition have different lawful owners. | Use one umbrella feature record plus one owner-local record for each semantic proposition. |
| One primary change class was required even though classes overlap. | A replacement can simultaneously change contract, policy, persistence, composition and retirement obligations. | Use non-exclusive consequence tags; no primary tag is required. |
| Four directions were not paired with impact dimensions. | A downstream trace alone can miss schema, serialisation, state, replay, operational and governance consequences. | Complete a direction-by-dimension impact matrix. |
| There was no mandatory post-change reconciliation. | The actual dependency cone often differs from the predicted cone. | Reconcile the map against changed paths, imports, public seams, proof nodes and runtime composition before integration. |
| A new canonical contract was described as sole meaning before consumer migration completed. | That creates a period in which old consumers depend on a contract that the record says is no longer authoritative. | Keep contract-version authority explicit until cutover; retire the old version only after named conditions pass. |
| Compatibility projection rules did not fully address information loss, domain coverage or reverse derivation. | A coarse projection may not be total or meaning-preserving, and old values cannot usually reconstruct new truth. | Require a versioned, deterministic, declared-domain projection; prohibit reverse derivation; use atomic cutover when projection is unsafe. |
| Migration, backfill, crash windows and rollback were not complete enough. | Storage and replacement changes can pass local tests while leaving mixed or unrecoverable state. | Add triggered data-migration, recovery, rollback and reconciliation obligations. |
| Test results were presented as stress-testing the method. | The 95 green tests exercise selected current repository seams; they do not prove any proposed feature or the completeness of the method. | Treat them as repository probes only and state exactly what they do not establish. |
| Missing M01 vocabulary namespace was labelled a repository gap. | Current vocabulary law permits global governed M01 terms; absence of a module namespace is not automatically defective. | Make M01 namespace work conditional on new M01-owned durable terms or a required module-scoped audit. |
| The coefficient trace prescribed a range before the target field and semantics were identified. | An arbitrary numeric range would invent policy and might enter capital-sensitive paths. | Block at Definition until target identity, meaning, owner, unit, direction, bounds and consumers are decided. |
| The M06 retention trace blurred domain, packet, persistence, replay and sequencing ownership. | It could move business meaning into M13 or make M12/M04/M00 implicit owners. | Decompose the retention outcome across M06, M04, M13, M12 and M00 with one exact hand-off rule. |
| The position trace began from “no database” rather than a complete existing-state classification. | M11 already supports typed state and optional restart-safe SQLite, while current position health remains a separate gap. | Preserve M11 state; define health as separate time-indexed evidence and decide its later lifecycle authority explicitly. |

## 3. Unit of change

### 3.1 Umbrella feature record

One user-visible outcome may span multiple modules. The umbrella record states the outcome, non-goals, end-to-end success condition, activation boundary and dependency-closed proposition list. It does **not** create a new semantic owner.

Examples:

- “Every accepted M06 packet is durably retained before M09 hand-off” is an umbrella outcome.
- “M06 owns the retention policy for its output evidence” is one possible owner-local proposition.
- “M04 validates the retained packet occurrence” is a separate proposition.
- “M13 supplies the typed durable evidence port” is a mechanism proposition.
- “M00 calls retention before M09” is a composition proposition.
- “M12 constructs replay material from exact retained evidence” is a replay proposition.

### 3.2 Owner-local semantic proposition

Each proposition must have:

1. one semantic owner;
2. one public seam or an explicit statement that no boundary is crossed;
3. one exact behaviour and one exact prohibited-authority boundary;
4. bounded inputs and outputs;
5. identity, lineage, time and state law where material;
6. a proof proposition and failure signal; and
7. a truthful completion claim limited to that proposition.

A proposition is not a file, class, commit, test directory or arbitrary task. One implementation slice may satisfy one proposition or a dependency-closed subset of one proposition, but it must not blend unrelated owners merely to produce a convenient patch.

### 3.3 Dependency-closed slicing

If a feature needs a prerequisite change, record it as a separate proposition with its own owner and proof. For example, exact Vega/Rho admission cannot be truthfully implemented as an M01-only field addition if M01/M03 scalar contracts and serialisation do not admit `Decimal`.

An owner-local Gate D pass means only that the bounded proposition is available at its accepted seam. It does not mean the umbrella feature is active end to end.

## 4. Definition begins with premise falsification

Premise falsification is part of Definition, not a new gate.

### 4.1 Authority intake

Record:

- baseline commit and working-tree state;
- active bounded pack and execution route;
- routed normative and control files read in full;
- relevant public contracts, composition paths and retained proof families;
- accepted comparable checkpoint and declared test environment; and
- authority conflicts or stale evidence.

Repository search is navigation evidence. A path match, no-match, import graph, test count, generated registry or vocabulary scan cannot replace contextual reading.

### 4.2 Exact requirement

Rewrite the request as observable outcomes and prohibited outcomes. Separate user intent from an example implementation.

For every important noun, identify whether it names:

- a domain fact;
- a carrier or packet occurrence;
- current state;
- append-only evidence;
- a policy/configuration value;
- an external effect;
- a review projection; or
- a compatibility shape.

If the requested field or behaviour cannot be identified, the record remains blocked. A nearby specimen may be used to test the method, but it must not be substituted as the requested target.

### 4.3 Current-state matrix

Before choosing a design, complete this table for each claimed capability:

| Required outcome | Normative owner/seam | Direct source evidence | Current proof evidence | Composition evidence | Current-state classification |
|---|---|---|---|---|---|
| Exact outcome | Exact authority locator | Contract/service/store path | Admitted proof and result | Caller/wiring path or absence | One classification below |

Allowed current-state classifications are explanatory only:

- absent;
- owner-local but not composed;
- composed in shadow/advisory mode;
- active only through compatibility;
- active at the canonical seam;
- present but incorrectly owned;
- present but semantically defective;
- present but non-durable;
- present with bounded durability; or
- Unknown because evidence is insufficient.

The record must preserve mixed truth. For example, M11 position state can be active and restart-safe when SQLite is injected while position-health assessment remains absent.

### 4.4 Decision-readiness blockers

Do not open `C-NORM` for implementation meaning while any material item is Unknown, including:

- the exact target contract or consumer;
- semantic meaning or decision effect;
- source authority and provenance;
- unit, sign, scale, range, quantum or rounding;
- missing/unknown/degraded behaviour;
- owner or public seam;
- current state versus evidence distinction;
- external-effect or persistence failure policy; or
- compatibility/cutover acceptability.

Discovery code, experimental spikes and evidence gathering may continue without authorising the feature contract.

## 5. Consequence tags

Apply every material tag. These tags drive obligations; they are not repository vocabulary admissions and no primary tag is required.

| Tag | Triggered consequence |
|---|---|
| `new_contract` | New public shape, identity, invariant or version. |
| `contract_replacement` | Old and new meanings need coexistence, cutover or atomic replacement. |
| `local_implementation` | Owner-internal behaviour changes without a public contract change. |
| `policy_numeric` | Policy, algorithm, coefficient, unit, bound, precision or rounding changes. |
| `source_adapter` | New source/provider/family, entitlement or acquisition semantics. |
| `composition_activation` | Existing owner products are newly called, ordered, shadowed or activated. |
| `state_persistence` | Current state, append-only evidence, repository, schema or durability changes. |
| `data_migration` | Existing records require backfill, transformation, verification or mixed-version handling. |
| `compatibility_migration` | Old callers, shapes or paths remain temporarily. |
| `ownership_correction` | Meaning or writes move to the accepted owner. |
| `external_side_effect` | Broker, network, publication or other irreversible effect is introduced or reordered. |
| `deprecation_removal` | Consumer, field, path, schema, projection or store will be retired. |
| `defect_correction` | Accepted meaning exists but current behaviour violates it. |

Tags may change after discovery or after the actual diff is known. Any newly triggered obligation reopens the relevant earlier stage.

## 6. Impact mapping

### 6.1 Direction-by-dimension matrix

For each cell, record `affected`, `not affected` with reason, or `Unknown`.

| Direction | Semantic authority and ownership | Contracts/data/serialisation | Runtime/composition/consumers | Identity/time/state | Persistence/replay/migration | Operations/external effects | Governance/proof/vocabulary |
|---|---|---|---|---|---|---|---|
| Upstream prerequisites | | | | | | | |
| Downstream consumers | | | | | | | |
| Lateral/shared mechanisms | | | | | | | |
| Temporal: old data, in-flight work, replay and retirement | | | | | | | |

The four directions answer **where** consequences propagate. The dimensions answer **what kind** of consequence exists.

### 6.2 Consumer census

Name consumers rather than writing “all callers”. Check, as applicable:

- public imports and direct calls;
- transitive composition and dependency injection;
- packet adapters and role validators;
- schemas, serialisers, fingerprints and canonicalisation;
- repositories, migrations, read models and retention jobs;
- configuration, registries and promotion surfaces;
- fixtures, factories and test harnesses;
- API/CLI adapters and exported review views;
- replay and historical reconstruction;
- vocabulary registry, namespace scan paths and generated projections; and
- operational monitors, alerts or external integrations.

Zero code-search results mean only that the searched spelling was absent in the searched paths. They do not prove zero semantic consumers.

### 6.3 Prospective and retrospective traces

Complete the matrix twice:

1. **Prospective trace:** before authoritative tests or implementation, to define scope and proof.
2. **Retrospective trace:** after implementation, using the actual diff, changed imports, public exports, generated artefacts, executed proof nodes and composition changes.

An unexplained new cell is a scope defect. An expected cell with no implementation or proof is an incompleteness defect. Integration remains blocked until the differences are resolved or explicitly returned to governing alignment.

## 7. Mandatory change record

The record may live in an existing concept/module/ExecPlan surface. It must contain the following fields without creating a duplicate tracker.

### 7.1 Control and outcome

- record ID and title;
- baseline commit and working-tree state;
- active route and authority locators;
- exact user outcome;
- prohibited outcomes and non-goals;
- umbrella activation condition;
- consequence tags; and
- risk class with reason.

### 7.2 Current implementation truth

- premise claims tested;
- current-state matrix;
- direct contract/source/composition/proof evidence;
- accepted comparable checkpoint;
- known defects, compatibility-only paths and bounded durability; and
- Unknowns and the evidence needed to close them.

### 7.3 Proposition ledger

For every owner-local proposition:

- proposition ID and normative locator;
- owner and public seam;
- exact inputs/outputs and prohibited authority;
- dependency-plane edges;
- identity, lineage, clock and version owners;
- state/evidence owner, writer, readers and mechanism;
- compatibility and retirement impact;
- proof proposition, false-positive challenge and failure signal;
- implementation slice; and
- proposition-level completion claim.

### 7.4 Impact and migration

- prospective direction-by-dimension matrix;
- named consumer census;
- invariant and must-not-change list;
- contract/version plan;
- data migration, backfill and mixed-version plan where triggered;
- cutover, rollback and recovery plan;
- observability and reconciliation plan; and
- retrospective impact reconciliation.

### 7.5 Evidence and closure

- `C-NORM` result;
- `C-PROOF` result and expected-red/existing-green reason;
- exact validation commands or stable command locators;
- environment, exit status, counts and failing-node delta;
- targeted, affected, aggregate and shadow results;
- architecture/dependency/vocabulary/state/replay checks triggered;
- pre/post Git state;
- umbrella activation state;
- remaining consumers or retirement work; and
- bounded final claim plus explicit non-claims.

## 8. Contract evolution law

### 8.1 Version authority

A changed meaning requires an explicit version decision. Do not silently reuse a version when any accepted consumer could interpret the same shape differently.

During migration:

- the old contract remains authoritative for the consumers and epochs that still lawfully use it;
- the new contract is authoritative for named new-version consumers after its owner-local acceptance;
- canonical composition names which version it selects;
- no adapter may make both versions competing owners of the same occurrence; and
- the old version is retired only after its named consumers, stored data and replay obligations are closed.

The phrase “new contract is the sole canonical meaning” is lawful only after cutover and retirement conditions are met, not merely after the new class exists.

### 8.2 Compatibility projection

A temporary old-shape projection from a new contract is permitted only when it is:

1. outward from the accepted owner;
2. deterministic and versioned;
3. total for a declared input domain, or explicitly rejecting outside it;
4. honest about information loss and boundary values;
5. incapable of changing source authority, identity or state;
6. proved against every retained old consumer; and
7. tied to named retirement conditions and an owner.

Never derive the richer new truth from the coarse old shape unless a separate owner-issued source makes that derivation authoritative. A `low|medium|high` value, for example, cannot reconstruct an original continuous coefficient.

New consumers must use the new canonical contract. Any exception must be named in the change record and reopens the compatibility plan; it cannot arise by convenience.

If no meaning-preserving projection exists, use an atomic consumer cutover, a separately authorised dual-read period or reject the replacement. Do not invent thresholds merely to keep an old API alive.

### 8.3 Cutover and retirement

Name exact conditions, such as:

- new contract accepted at the owner seam;
- all named consumers migrated and proved;
- stored records backfilled or explicitly quarantined;
- replay can interpret required historical versions;
- canonical composition no longer selects the old path;
- no new writes occur in the old schema/store;
- an observation period has no material divergence;
- rollback boundary has expired or been consciously closed; and
- compatibility code, tests, vocabulary and config are removed or reclassified.

“Deprecated” without a consumer list, last-write condition and removal test is not a retirement plan.

## 9. Numeric, identity and time law

### 9.1 Exact numeric definition

Every authority-bearing numeric addition or replacement must define:

- domain meaning and decision effect;
- unit and conversion basis;
- sign convention and monotonic direction;
- inclusive/exclusive minimum and maximum;
- precision, quantum and canonical serialisation;
- rounding mode and the boundary at which rounding occurs;
- missing, unknown, unavailable, degraded and non-applicable states;
- finite-value rules and overflow/underflow behaviour;
- policy/configuration version;
- equality/fingerprint behaviour; and
- whether calculations require `Decimal` end to end.

Do not choose `[-100,+100]`, `[0,1]`, percentages, basis points or category thresholds by convention alone. Those are semantic decisions.

When exact decimal meaning is required, every upstream binding, candidate union, model field, validator, derivation, fingerprint, packet serialiser, persistence codec, fixture and consumer must preserve it. Converting through `float` defeats an exact-numeric claim even if the final field is typed `Decimal`.

### 9.2 Identity

Define the identity of the domain fact, contract version, occurrence, packet, state snapshot, evidence record and transaction separately where they differ.

A scalar inside a uniquely identified observation need not receive a synthetic UUID. It needs a separate identity only when it is independently referenced, revised, superseded, retained or reconciled.

Packet ID alone is not sufficient where repository law identifies a packet occurrence by its source-and-ID pair. A storage key may encode that pair, but it must not replace either constituent identity.

### 9.3 Time

Name source observation/effective time, capture time, packet emission time, persistence time, decision time and replay time separately. Current wall-clock time must not stand in for a missing owner-issued temporal fact.

For mutable or repeated assessments, define:

- as-of/effective time;
- validity horizon and staleness behaviour;
- ordering and late-arrival law;
- supersession/correction law;
- timezone and precision; and
- historical query/replay semantics.

## 10. State, persistence and migration law

### 10.1 Distinguish current state from evidence

Current state answers “what is true now?” and may be versioned through controlled mutation. Evidence answers “what happened or was assessed at a stated time?” and is normally append-preserved.

Do not place rapidly changing market observations, health scores or historical assessments into a current-state record merely because that record already has a database. Different identity, update cadence, retention and replay semantics require separate records.

### 10.2 Mandatory persistence decisions

For every new or changed store, define:

1. semantic owner of each stored record;
2. authorised writer and primary readers;
3. whether the record is current state, append-only evidence, configuration or a derived read model;
4. exact public repository/store port and storage mechanism;
5. occurrence or entity identity and idempotency scope;
6. schema/version/canonical encoding and fingerprint;
7. transaction/consistency boundary and write ordering;
8. duplicate, conflict, retry and late-arrival behaviour;
9. failure propagation and the next owner that must not be called;
10. crash-window and partial-completion behaviour;
11. restart/readback and integrity verification;
12. retention, deletion, privacy and access rules where authorised;
13. backup/recovery, capacity and operational Unknowns; and
14. proof that the chosen implementation satisfies only the claimed durability boundary.

M13 may provide transaction and typed storage mechanics. The domain owner retains record meaning and policy. A SQLite adapter proves neither universal durability nor production recovery.

### 10.3 Write-order claims

Use distinct lifecycle facts:

- produced;
- contract-valid;
- accepted for a named boundary;
- durably stored;
- handed off;
- consumed;
- decision completed; and
- replayable.

A successful synchronous store before a call can establish “stored before hand-off”. It does not establish that the downstream owner consumed the record. A crash after storage but before the call creates a lawful stored-but-not-handed-off occurrence unless the requirement says otherwise.

If the requirement is exactly-once downstream processing rather than store-before-call, define a durable hand-off state machine, inbox/outbox or equivalent idempotent recovery protocol. Do not make that stronger claim from call order alone.

### 10.4 Data migration phases

Where existing data changes meaning or schema, record these triggered phases:

1. introduce the new schema/contract without changing authority;
2. write or derive new-version records under an explicit policy;
3. backfill with source lineage and deterministic transformation version;
4. verify counts, identities, fingerprints, invariants and rejected records;
5. shadow-read or compare where semantically lawful;
6. cut over named readers and writers;
7. stop old writes;
8. retain or quarantine old data for required replay; and
9. remove the old path only after retirement conditions pass.

Rollback is not the reverse of every migration. Define the last reversible point, data produced after cutover, compensation/reconciliation and which accepted evidence must never be deleted merely to restore old code.

### 10.5 External effects

When a store and an external effect must agree, a database call after the effect is not atomicity. Define request identity, idempotency, acknowledgement, reconciliation, retry, timeout, compensation and recovery. Use an outbox/inbox or equivalent governed design when required. Such changes trigger the repository’s high-consequence independent-validation rule.

## 11. Proof and validation law

### 11.1 `C-NORM`

`C-NORM` closes the bounded proposition, including owner, seam, inputs/outputs, exclusions, identity/time/state semantics, contract versions, compatibility/cutover and vocabulary admissions where triggered.

It remains blocked when the proposition depends on invented numeric semantics, an unidentified target field, an unresolved owner or an unproved premise.

### 11.2 `C-PROOF`

Use the smallest truthful public-seam proof. As applicable, include:

- one conforming case;
- the material missing or forbidden input/action;
- one plausible false-positive implementation;
- an exact boundary value or rounding case;
- version/compatibility projection cases;
- wrong owner/private-import/fabricated-authority rejection;
- duplicate/conflict/idempotency and restart cases;
- write failure preventing the next owner call;
- state isolation, order, replay and substitution; and
- information-loss or reverse-derivation rejection.

Expected red is useful only when it fails for the exact absent behaviour. A test that fails from an import error, bad fixture, wrong environment or unrelated validation does not open Gate D.

The false-positive challenge should be concrete: for example, mutate a coefficient without its policy version, persist after rather than before M09, accept a Decimal through a float conversion, or treat a process-memory store as restart-safe.

### 11.3 Gate D validation

After implementation, run and record:

1. targeted admitted proof;
2. affected admitted proof in the dependency cone;
3. unaffected sentinel proof for plausible spill paths;
4. architecture/dependency checks where contracts or imports changed;
5. vocabulary builder/audit only in the correct global or module scope where triggered;
6. state, migration, restart and replay proof where triggered;
7. current admitted aggregate route and relevant shadow suite once when available; and
8. the retrospective impact reconciliation.

Compare the failing-node set with the latest accepted comparable checkpoint. Reuse a current comparable baseline; rerun it only when its admitted set, environment, command or comparability changed or is Unknown.

### 11.4 Evidence claim boundary

The concise validation record must state what each command establishes and does not establish. A green targeted set does not prove:

- an unimplemented proposed feature;
- full consumer migration;
- durability outside the injected store;
- complete replay evidence;
- production recovery;
- live or paper operational readiness;
- profitability; or
- that the methodology itself is complete.

The first draft’s `95 passed in 1.30s` is useful evidence that selected existing seams were green in its declared environment. It does not validate Vega/Rho, a coefficient replacement, durable M06 retention or a new position-health assessment. It was not reproduced in this audit because the supplied repository declares Python 3.13.5 while the audit runtime exposes Python 3.12 without the locked test dependencies; the original result is retained as supplied evidence, not re-labelled as current execution.

### 11.5 Risk-triggered independent validation

Use the current Gate C triggers without adding another gate. Independent validation remains mandatory when a proposition owns:

- atomic state transition, rollback, idempotency or transaction participation;
- fresh-capital sizing or deployment authority;
- broker submission, acknowledgement or fill reconciliation;
- live position, inventory, exit or close mutation;
- durable storage migration, recovery or promotion authority; or
- another boundary recorded as equivalently irreversible or high-consequence.

Broad shared-contract or packet changes require an explicit Project Manager risk decision. They do not automatically create a new universal review tier.

## 12. Implementation and activation

### 12.1 Implementation rules

- Change the accepted owner first.
- Cross modules only through public exports or admitted evidence/transaction ports.
- Keep evaluators pure where current authority requires purity; place I/O in a separate owned service or adapter.
- Make clocks, identifiers, policy/configuration, repositories and ports explicit.
- Do not broaden a compatibility path with new meaning.
- Do not move unrelated files merely to make a feature patch look architecturally complete.
- Keep production changes, migrations, proof and composition within the smallest dependency-closed slice that remains semantically complete.

### 12.2 Activation descriptions

Record these as plain-language descriptions, not new formal workflow statuses:

1. **Owner-local available:** the new owner contract and behaviour pass at the public seam, but canonical composition does not use them.
2. **Composed in shadow:** canonical composition executes or compares the new path without granting it decision/state authority.
3. **Active in a bounded route:** named canonical callers use the new contract for a defined scope, version or epoch.
4. **Consumer migration complete:** every named canonical consumer has cut over and required historical data/replay remains interpretable.
5. **Compatibility retired:** old writes, callers, projections and selectable paths are removed or canonically quarantined, with proof.

The umbrella feature is complete only at the description named in its outcome. “Available” must not be reported as “active”, and “active” must not be reported as “retired”.

### 12.3 Activation controls

Where material, define:

- feature/config selection owner;
- default and fail-closed behaviour;
- scope, version, tenant/account/environment or epoch;
- shadow comparison and divergence limits;
- observability and alerts;
- rollback switch and last reversible point; and
- exact evidence required to widen activation.

## 13. End-to-end execution sequence

### Stage 1 — Definition

1. declare authority and baseline;
2. rewrite the request as exact outcomes and non-goals;
3. falsify the premise against authority, source, proof and composition;
4. classify current implementation truth;
5. block unidentified or semantically Unknown targets;
6. decompose the umbrella outcome into owner-local propositions;
7. apply consequence tags;
8. complete the prospective impact matrix and consumer census;
9. define activation and retirement scope; and
10. record risk class and independent-validation trigger.

**Exit:** the record is decision-ready, not merely descriptive.

### Stage 2 — Governing alignment

1. place each proposition at the accepted owner and public seam;
2. amend existing routed authority where mandatory meaning is absent;
3. close contract/version, numeric, identity, time, state and persistence law;
4. define compatibility, cutover, migration, rollback and failure propagation;
5. admit vocabulary only through the correct existing global/module route where triggered; and
6. record `C-NORM`.

**Exit:** normative meaning is complete enough that a false implementation can be written and rejected without guessing.

### Stage 3 — Tests

1. identify or write minimum truthful public-seam proof;
2. cover conforming, prohibited and plausible false-positive cases;
3. add migration, restart, replay, failure-injection and compatibility proof only where triggered;
4. demonstrate expected red for the exact absent behaviour or admit exact existing green proof; and
5. record `C-PROOF` and the Gate D boundary.

**Exit:** proof fails or passes for the proposition’s reason, not an incidental reason.

### Stage 4 — Implementation

1. implement dependency-closed owner-local slices;
2. keep public seams typed and mechanisms subordinate;
3. add compatibility projection or migration only as authorised;
4. wire composition explicitly;
5. add observability and recovery hooks where required; and
6. avoid activating beyond the recorded scope.

**Exit:** owner-local behaviour and required composition exist, but no integration claim is made yet.

### Stage 5 — Validation

1. run targeted and affected proof;
2. run applicable sentinel, architecture, dependency, vocabulary, state, migration and replay checks;
3. run current aggregate and relevant shadow routes once when available;
4. compare failing nodes with the accepted comparable checkpoint;
5. reconcile prospective impact against the actual diff and composition; and
6. state limitations and unavailable checks.

**Exit:** the exact bounded claim is reproducible and no unexplained impact remains.

### Stage 6 — Gated integration

1. integrate serially from the named canonical checkpoint;
2. decide owner-local availability, shadowing, activation or cutover as authorised;
3. update the existing module/concept record, validation log and live roadmap;
4. publish one completed semantic-slice checkpoint;
5. retain named consumer/retirement work if the umbrella outcome is not complete; and
6. state the final claim and non-claims.

**Exit:** the checkpoint claim matches actual activation and migration state.

## 14. Completion and return rules

### 14.1 Proposition complete

An owner-local proposition is complete only when:

- authority and public seam are closed;
- truthful proof protects the accepted and prohibited behaviour;
- implementation passes targeted and affected validation;
- the retrospective impact trace has no unexplained change;
- triggered migration/replay/compatibility obligations are satisfied for that slice; and
- the claim is bounded to actual composition and durability.

### 14.2 Umbrella feature complete

The feature is complete only when:

- every required proposition is complete;
- canonical composition uses the new route at the promised activation scope;
- required records are stored/read/replayed as promised;
- named consumers and historical versions are reconciled;
- retirement conditions are met if replacement/removal was part of the outcome; and
- failure, recovery and observability match the defined outcome.

### 14.3 Mandatory return to an earlier stage

Return when:

- the actual target differs from the request;
- current-state evidence invalidates the premise;
- a new owner, consumer or persistence domain appears;
- an Unknown becomes material;
- expected red fails for the wrong reason;
- the implementation requires a broader contract or compatibility path;
- actual impact exceeds the prospective map;
- a migration/restart/replay check fails; or
- the activation claim exceeds direct evidence.

Returning is correction, not a failed feature.

## 15. Worked trace A — Vega and Rho admission

### 15.1 Corrected current-state finding

No `vega` or `rho` field is present in the audited source, tests, docs or configuration under those exact names.

The current M01 `SourceSemanticBinding.value_type` admits only `float`, `int`, `str`, `bool`, `date` and `datetime` (`src/nvda_desk/m01_source_admission/contracts.py`). M03 `PreparedScalar` has the same effective scalar family and `PreparedRuntimePayloadV1` uses `float` for its numeric market fields (`src/nvda_desk/preparation/field_resolution.py`; `src/nvda_desk/contracts/prepared_data.py`). Therefore a requirement for exact decimal Greeks has a real cross-owner prerequisite; adding `Decimal` only at the final payload would not preserve exactness.

M01 not having a `m01` vocabulary namespace is **not** a current defect. The namespaced projection law permits existing globally governed terms, and the registry currently carries M01/M13 terms globally. A new M01 namespace becomes a prerequisite only if the accepted change introduces M01-owned durable vocabulary requiring bounded module scope or if a module-scoped audit is expressly required. Human-registry admission must precede projection changes.

### 15.2 Decision blockers

Before `C-NORM`, decide:

- exact source/provider and entitlement;
- contract-level versus aggregate Greek;
- valuation model and inputs;
- Vega convention: per one volatility point or per unit volatility;
- Rho convention and rate-bump basis;
- currency/unit, sign, as-of time and expiry/strike/right identity;
- precision, quantum, rounding and missing/degraded behaviour; and
- whether both facts are source-issued or deterministically derived by an accepted owner.

Until then the feature is **architecturally traceable but semantically blocked**.

### 15.3 Dependency-closed propositions

1. **Exact-numeric prerequisite:** extend the M01/M03 semantic candidate, validation, canonicalisation, fingerprint, serialisation and persistence boundary to preserve `Decimal`, with no float round-trip.
2. **M01 source admission:** add a versioned typed option-contract source family and bindings for owner-issued Vega/Rho facts.
3. **M03 prepared truth:** introduce a new prepared payload version or lawful typed extension; do not silently add changed meaning to the literal `prepared_runtime_v1`/`1.0.0` contract.
4. **Consumer adoption:** each M05/M06 or later use is a separate proposition with its own decision meaning and proof.
5. **Vocabulary:** add or extend an M01 namespace only if durable-term and bounded-scan requirements trigger it.

### 15.4 Proof focus

- exact Decimal round-trip through M01 → M03 → serialisation/fingerprint;
- exponent and trailing-zero canonicalisation;
- negative, zero, boundary and non-finite rejection;
- wrong unit/model/version rejection;
- absent/degraded source behaviour;
- no fabricated provider or current-time authority; and
- no change to M05/M06 decisions merely because fields became available.

Initial activation should be owner-local availability, then optional carriage. Decision use is a later proposition.

## 16. Worked trace B — replace `low|medium|high` with a continuous coefficient

### 16.1 Audit decision

This case is **blocked at Definition** because the exact requested field and intended consumer were not identified.

The strategic-ladder specimen is not a safe substitute for the unidentified target. It contains:

- `LadderConfidence = low | medium | high` on each rung; and
- a separate `StrikeZoneSignal.score: Decimal`.

It is located in `src/nvda_desk/contracts/strategic_ladder.py` and `src/nvda_desk/upstream/strategic_ladder.py`, outside the accepted M07 public package, and must not be assumed to be the requested M08 playbook field or a canonical coefficient owner.

The repository also contains a separate legacy `FinalRiskJoinReceipt.confidence_scalar: float`, explicitly labelled for pre-M09 compatibility (`src/nvda_desk/contracts/risk.py`). Canonical M09 law rejects confidence joins and prohibits sizing from serial confidence or execution ranks. M07 already has governed Decimal coefficient/bounds/version contracts. These meanings must not be merged.

### 16.2 Decisions required before design

- exact field, contract version and every named producer/consumer;
- whether the value means confidence, eligibility, rank, distance, strength, risk, modifier or another proposition;
- accepted owner: M07 only if it is genuinely coefficient/modifier authority;
- unit, direction, range, quantum, rounding and missing state;
- whether category boundaries carry accepted business meaning;
- whether the coefficient can affect candidate formation, risk, capital or lifecycle; and
- whether replacement is required or the numeric score already satisfies the real outcome.

No `[-100,+100]` or other range is recommended without these decisions.

### 16.3 Lawful replacement patterns

If the identified categorical field is genuinely replaced:

1. introduce an explicit new-version coefficient contract at its accepted owner;
2. retain old-version authority for named old consumers during migration;
3. allow `coefficient.v2 → category_projection.v1 → low|medium|high` only if threshold semantics are accepted and total for the declared domain;
4. never derive `coefficient.v2` from an old category;
5. make canonical composition select one version per scope/epoch;
6. prove that no confidence/coefficient enters M09 capital sizing unless separately authorised; and
7. retire categories only after consumer and replay conditions pass.

If category boundaries are arbitrary or meaning-changing, use atomic consumer cutover rather than a compatibility projection.

## 17. Worked trace C — retain every accepted M06 packet before M09

### 17.1 Corrected current-state finding

The current canonical M00 route evaluates M06, emits one M04 `parallel_risk_packet`, then immediately calls M09 (`src/nvda_desk/m00_application_shell/coordinator.py`). It does not durably retain that packet first.

The older `ParallelRiskObservationStore` is process-memory, write-only and tied to legacy bootstrap/lane packet schemas (`src/nvda_desk/persistence/parallel_risk_observations.py`). It is not the canonical K10-to-M09 path.

M13 already provides `EvidenceRepositoryPort` and `SqliteEvidenceRepository` for typed, idempotent evidence occurrences with exact reload and fingerprint verification (`src/nvda_desk/m13_state_kernel/ports.py`; `src/nvda_desk/m13_state_kernel/sqlite.py`). That mechanism does not supply retention policy or domain meaning. M12 owns replay-material and replay-assessment meaning, but no current durable-retention guarantee.

### 17.2 Required owner decomposition

The umbrella outcome should be decomposed at least as follows:

| Proposition | Owner responsibility |
|---|---|
| M06 retention policy | Define which M06 output occurrence must be retained, required evidence content and failure consequence; this is a new normative state/persistence proposition because current K10 is transient. |
| M04 packet acceptance | Validate exact role, source-and-ID occurrence, producer, lineage, execution context, typed payload and carriage fingerprint; M04 retains packet meaning. |
| M13 storage mechanics | Store and reload the exact typed occurrence idempotently; reject conflicting reuse; retain committed sequence and fingerprint; own no risk/packet/replay meaning. |
| M00 composition | Invoke the retention seam after valid M04 emission and before M09; do not call M09 on retention failure; carry the evidence-record reference into the run evidence if admitted. |
| M12 replay use | Convert exact retained owner evidence into ordered `ReplayMaterial` and classify replay without reinterpreting M04/M06 meaning. |

The `owner_module` value, occurrence-key encoding and exact retained wrapper are `C-NORM` decisions. They must preserve both M06 payload ownership and M04 packet-occurrence identity rather than collapsing them.

### 17.3 Proposed ordering proposition

The narrow default proposition is:

`M06 assessment → valid M04 parallel_risk_packet → successful durable evidence record → M09 hand-off`

Required behaviour:

- retention failure prevents the M09 call;
- exact retry returns the same evidence record without a duplicate row;
- conflicting content under the same occurrence fails closed;
- M09 receives the exact packet whose retained fingerprint was verified;
- restart reload reproduces the typed packet; and
- stored-but-not-handed-off is a visible possible crash outcome unless a stronger hand-off state machine is separately authorised.

This proves “stored before hand-off”, not exactly-once M09 consumption, production backup/recovery or universal replay completeness.

### 17.4 Proof and risk

- valid packet stored before an instrumented M09 call;
- invalid packet never stored or handed off;
- injected storage failure yields no M09 call;
- idempotent retry and conflicting occurrence;
- SQLite restart/readback, type validation and fingerprint integrity;
- same source-and-ID and execution context retained;
- M12 material order and exact content where included; and
- no revival of the legacy bootstrap packet or process-memory store as canonical authority.

This change triggers independent validation because it introduces durable evidence and recovery/failure-ordering behaviour.

## 18. Worked trace D — persistent position management and position health

### 18.1 Corrected current-state finding

The premise “there is no position database” is false for the bounded canonical alpha path.

M11 already owns typed `PositionState`, `PortfolioSnapshot`, `LifecycleDecision` and `CloseReceipt`; mutations use M13 transaction participation. `PortfolioLifecycleService` defaults to non-durable memory but can consume the M13 SQLite state port. In that injected configuration, current paper portfolio state and receipts survive restart within their admitted bounds (`src/nvda_desk/m11_portfolio_lifecycle/contracts.py`; `src/nvda_desk/m11_portfolio_lifecycle/service.py`; `src/nvda_desk/m13_state_kernel/sqlite.py`). This is not live-account truth or universal operational durability.

M11 also exposes `PortfolioRiskFactIssuer`, which creates point-in-time concentration and inventory owner facts from an exact snapshot plus explicit measurements. That is partial related behaviour, not a general historical position-health assessment.

### 18.2 Remaining gap

The repository lacks one general, time-indexed, policy-versioned `PositionHealthAssessment` that binds:

- exact portfolio snapshot and position identity/version/fingerprint;
- owner-issued market mark and source/effective/capture/freshness facts;
- component metrics and missing/degraded states;
- assessment policy/version and thresholds;
- as-of time, validity horizon and deterministic fingerprint;
- non-empty reasons and limitations; and
- explicit statement of whether it is review-only or may inform lifecycle decisions.

The exact components and decision effect remain Unknown and block authoritative implementation. Examples such as unrealised return, drawdown, distance from stop or thesis integrity must not be invented by the method.

### 18.3 Recommended separation

Keep `PositionState` as transactionally current holding truth. Add health as a separate immutable assessment occurrence because it changes at a different cadence and needs history/replay.

Possible dependency-closed propositions are:

1. source/mark owners expose exact typed measurements with time/freshness lineage;
2. M11 owns the assessment contract and deterministic evaluation if health is part of position lifecycle meaning;
3. M11 retains append-only assessment evidence through an M13 port while M13 owns only mechanics;
4. M12 consumes exact assessments for review/replay; and
5. a later M11 lifecycle-policy version may consume health only after a separate high-consequence proposition and proof.

Do not add fast-changing marks, scores or assessment history directly to `PositionState`. Do not let an assessment mutate quantity or close a position merely because it exists.

### 18.4 Proof and activation

- exact snapshot/position/mark/time binding;
- stale, future, missing and conflicting measurement behaviour;
- deterministic component and aggregate calculations with Decimal rules;
- append order, idempotency/conflict and restart reload;
- no mutation of current `PositionState` from assessment creation;
- review/replay over an ordered history; and
- separately proved lifecycle consumption, stale-snapshot rejection and atomic mutation if later activated.

Initial activation should be owner-local assessment plus review-only retained evidence. Lifecycle decision authority is a later independently validated proposition.

## 19. Vocabulary application

Vocabulary work is triggered by durable concept identity, not every code symbol.

For a new durable term:

1. amend the human registry first with definition, scope, owner, relationships, aliases, misleading uses, lifecycle and metadata;
2. select the existing global or module namespace by ownership and scan scope;
3. extend a namespace only when its accepted scope requires it;
4. regenerate the machine projection through the governed builder;
5. run the correct scoped audit plus global checks only when globally affected; and
6. interpret a zero-candidate audit as scanner evidence only.

For the four traces:

- M06 and M11 already have bounded namespaces;
- M01 currently does not, but that is not itself a failure;
- the coefficient target cannot select a namespace until its owner is known; and
- cross-module method labels in this document are not automatically durable repository vocabulary.

## 20. Embedded change-record template

Copy this template into the existing authorised concept/module control surface; do not create a duplicate tracker unless the active plan requires one.

```markdown
# Feature evolution record: <ID> — <title>

## A. Control
- Baseline commit:
- Pre-change Git state:
- Active pack / route:
- Authority files read in full:
- Accepted comparable checkpoint:
- Declared environment:

## B. Exact outcome
- User outcome:
- Observable success:
- Prohibited outcomes:
- Non-goals:
- Promised activation scope:
- Consequence tags:
- Risk class and independent-validation trigger:

## C. Premise falsification and current truth
| Premise / required capability | Authority | Source evidence | Proof | Composition | Current classification |
|---|---|---|---|---|---|
| | | | | | |

Unknowns and required decisions:

## D. Owner-local proposition ledger
| ID | Proposition / locator | Owner | Public seam | Inputs / outputs | Prohibited authority | Dependencies | Proof / false-positive challenge | Slice |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## E. Contract and semantic decisions
- Version and coexistence law:
- Numeric/unit/rounding/missingness law:
- Identity and lineage roles:
- Source/effective/capture/emission/persistence times:
- Invariants and must-not-change list:

## F. Prospective impact matrix
| Direction | Authority | Contract/data | Runtime/composition | Identity/time/state | Persistence/replay | Operations/effects | Governance/proof/vocabulary |
|---|---|---|---|---|---|---|---|
| Upstream | | | | | | | |
| Downstream | | | | | | | |
| Lateral/shared | | | | | | | |
| Temporal/history | | | | | | | |

Named consumer census:

## G. Compatibility, migration and activation
- Projection or atomic cutover:
- Named old consumers:
- Data backfill / mixed-version handling:
- Write/read cutover:
- Crash and retry behaviour:
- Rollback / last reversible point:
- Observability and reconciliation:
- Retirement conditions and owner:

## H. Proof plan
| Proposition | Conforming | Prohibited | False positive | Migration/failure/replay | Target command |
|---|---|---|---|---|---|
| | | | | | |

- C-NORM result:
- C-PROOF result:
- Expected-red or exact existing-green reason:

## I. Validation and actual-impact reconciliation
- Targeted result:
- Affected result:
- Sentinel result:
- Architecture/dependency result:
- Vocabulary result:
- State/migration/replay result:
- Aggregate/shadow result:
- Failing-node delta:
- Prospective versus actual matrix differences:
- Unavailable checks / limitations:
- Post-change Git state:

## J. Integration and claim
- Owner-local availability:
- Shadow use:
- Active bounded route:
- Consumer migration:
- Compatibility retirement:
- Exact completed claim:
- Explicit non-claims:
- Remaining work and owner:
- Checkpoint:
```

## 21. Adoption recommendation

Adopt Version 2 as an overlay inside the current six-stage route after Project Manager review. Do not create a separate gate or standalone status system.

The best first pilot remains Vega/Rho only after the source/model/unit/precision decisions are supplied. It is bounded and exercises premise falsification, an exact-numeric prerequisite, versioned M01/M03 contracts, conditional vocabulary scoping and deferred consumer activation without immediately changing durable workflow state.

Do **not** use the coefficient specimen as a pilot until the exact target is identified. Do **not** begin M06 retention as a “database addition” without first closing the new M06 retention-policy proposition, packet-occurrence identity, M00 ordering and crash/failure semantics. Do **not** rebuild M11 position storage; extend it only for the separate health proposition if its metrics and decision authority are accepted.

## 22. Final one-line rule

First prove what exists and what the request actually means; then evolve one owned proposition at a time, preserve explicit version and state authority through cutover, and claim only the activation and durability directly proved.
