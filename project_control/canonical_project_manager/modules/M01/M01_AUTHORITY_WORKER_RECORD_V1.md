# M01 Authority Worker Record V1

## Status

`ACCEPTED:MVP_FAST_TRACK_M01_C_PROOF_AND_GATE_D`

## Source checkpoint

| Field | Value |
|---|---|
| Repository | `JayDEmily/Nvda11` |
| Source branch | `review/m13-implementation-v2` |
| Source commit | `2cf3c4dbbeb0ce53d63d49143b524b620ab15838` |
| Worker branch | `work/m01-source-admission-mlc-a-v1` |
| Unit | `M01-PROOF-MLC-A-V1` |
| Leaf type | `MLC-A — Authority sufficiency` |

The worker branch was created from the authenticated remote Phase A checkpoint after the branch was confirmed absent locally and remotely. This record does not self-accept its disposition.

## Exact bounded question

Is current normative authority sufficient to define the bounded M01 `source_admission` contract for source identity, offline admission, raw capture, source time and raw-signal-family registration, while explicitly excluding M00 transport/composition, M02 calendar semantics, M03 preparation, M04 packet carriage, M13 transaction semantics and downstream cognition/risk/capital/execution ownership?

## Full-read statement

The required control, routed normative, accepted architecture, workbook, machine projection, dependency graph, validation and current C/D/normative-completion sources were read in full at the source checkpoint. The exact paths and Git-object SHA-256 hashes are retained in `raw_validation/mlc_a_v1/full_read_manifest.tsv`.

Implementation source and existing tests were not inspected to derive authority. Workbook columns that mention code and tests are preserved mechanically for historical traceability only.

## Proposed disposition

`AUTHORITY_SUFFICIENT`

Current normative authority is sufficient to define the bounded M01 source-admission contract. The authority is sufficient because it specifies the owner, accepted inputs, mandatory identity and lineage distinctions, offline admission mode, source and capture temporal meanings, immutable evidence requirement, typed-family extension boundary, fail-closed behaviour, prohibited fabrication and downstream ownership ceiling.

The conclusion is bounded. It does not resolve production retention, restart durability, authoritative replay packaging, exact storage technology, M13 participation mechanics, M02 calendar interpretation, M03 field resolution, M04 packet roles or any downstream decision policy.

## Accepted M01 ownership

M01 owns:

- source identity;
- provider/source authority and offline admission;
- raw-capture identity and immutable raw evidence;
- source-observed time and repository capture time;
- raw-signal-family registration and the typed extension boundary.

The bounded public contract may therefore accept an already obtained external payload, checked-in reference artefact, recorded response or operator bundle through one explicit source adapter/reader and typed family contract; validate its declared family, source, identity, temporal truth and limitations; create a distinct repository-owned capture identity for the immutable captured representation; and emit an admitted typed source/capture carrier or explicit non-admission result.

## Prohibited ownership

M01 does not own:

- M00 transport translation, dependency composition or run lifecycle;
- M02 financial/event calendar semantic layers, coalescence, supersession or projection;
- M03 prepared-data enrichment, canonical field resolution or stage projection;
- M04 DMPV3 packet identity, packet emission time or carriage;
- M13 transaction, idempotency, atomic-receipt or storage-port semantics;
- serial cognition or Parallel Risk;
- capital, placement, execution, position, exit, close or replay decisions.

Those exclusions are contract ceilings, not missing M01 behaviour.

## Contract shape

### Input

One already obtained external payload, recorded response, checked-in artefact or operator bundle enters through an explicit source adapter or reader under one declared input-family/source contract and schema version.

### Admission decision

M01 establishes:

1. which source family and contract apply;
2. which upstream provider and acquisition channel supplied the material;
3. which owner-issued source identifiers are present or lawfully absent;
4. whether mandatory temporal, identity, lineage, fingerprint and validation facts are present and internally coherent;
5. whether the family is registered and supported;
6. whether the material is admitted, explicitly degraded where the family contract permits that exact limitation, or withheld.

No content is admitted by payload-shape guessing, nearest-schema coercion, provider default, empty mapping or fabricated identity/time.

### Output

The admitted output is a typed, versioned source/capture carrier eligible for its lawful downstream owner: M02 for admitted calendar/reference source material and M03 for other admitted source/raw-signal material. M01 preserves the source contract and evidence but performs neither M02 calendar semantics nor M03 preparation.

The carrier contains:

- input-family and source-contract identity;
- provider and acquisition channel;
- source-issued identity where the source supplies one;
- distinct repository-owned capture identity;
- immutable captured evidence or a governed immutable reference plus fingerprint;
- validation outcome and explicit limitations;
- source temporal facts at original precision;
- repository capture time;
- typed payload variant routed only to its lawful downstream owner;
- no candidate, risk, capital, placement, execution, inventory, close or review authority.

An unsupported or invalid family remains outside all governed downstream processing and returns a typed rejection/non-admission or withheld result.

## Identity, lineage, time, state and side effects

### Identity

Source-issued identity and repository-owned capture identity are different owner facts. Packet, trace, run, scenario, timestamp, filename, hash, array position, random value and local sequence do not substitute for either required role.

### Lineage and fingerprint

The carrier preserves immutable lineage or fingerprint material sufficient to identify the original captured evidence. A hash proves equality only; it does not prove retrieval or durable replay. Prepared and packet identities remain downstream and distinct.

### Source time and capture time

M01 preserves source temporal truth using the admitted source-time meanings and original precision. Source observation time/date is distinct from `captured_at_utc`, `persisted_at_utc` and packet emission time. Date-only truth is not upgraded to an instant; local time requires consistent timezone/offset handling.

### State

M01 semantically owns raw artefacts and capture receipts. The current authority does not establish production durability, retention duration, restart readback or complete replay. Any alpha retention claim must remain honestly non-durable unless separately proved. Transaction participation, if later opened, uses M13 without transferring M01 record ownership.

### Side effects

The external carrier-validation boundary does not open credentials, construct live network/broker clients, make domain/trading decisions or write unrelated persistence state. The bounded raw-capture operation may create its owned capture identity and immutable capture record/receipt. Exact atomic commit mechanics remain M13-owned and outside this leaf.

## Failure and withholding law

M01 must fail closed or explicitly withhold admission when a mandatory family, contract, identity, version, temporal, fingerprint, typed-payload or validation fact is missing, invalid or contradictory.

A source-contract-permitted optional absence may remain explicit and degraded only when the contract states the consequence. A warning or default does not convert missing mandatory authority into valid source truth.

Unknown or unsupported families remain unadmitted until a lawful typed contract, owner and controlled registration/configuration entry exist.

## Raw-signal-family registration

A new provider or signal family enters through:

1. one explicit external adapter or source reader;
2. one typed, versioned family carrier/payload contract;
3. one controlled registration or configuration entry;
4. source-specific validation and mapping;
5. later contract, rejection, lineage and substitution proof.

Registration is not a dynamic plugin framework or untyped service locator. Adding or replacing one conforming family must not require unrelated preparation, cognition, risk, capital, inventory, close or other adapter logic to absorb provider-specific fields.

## Authority matrix

The locator-backed proposition matrix is retained in `raw_validation/mlc_a_v1/authority_locator_matrix.tsv`. It covers input, decision, output, source identity, capture identity, lineage/fingerprint, time, mutability, side effects, failure, prohibited fabrication and downstream boundaries for each proposed obligation.

No authority claim in this record relies only on architecture allocation. The accepted architecture assigns M01 ownership; the numbered doctrine supplies the behaviour and prohibition.

## Atlas traceability

Mechanical extraction from `Atlas_Architecture_Traceability.xlsx` produced:

- 69 exact M01-linked cohort rows;
- 562 exact M01-linked record rows;
- 174 M01-linked reference-rebase rows;
- 24 non-current reference rows: 9 directory-level and 15 unresolved;
- exact agreement with the M01 machine-projection counts.

The exact subsets and reconciliation output are retained under `raw_validation/mlc_a_v1/`.

Atlas is candidate and architecture-trace evidence only. No Atlas row was mechanically admitted. Ten cohorts consulted for boundary challenge were manually classified in `atlas_manual_classification.tsv`. No individual Atlas record proposition was used to establish normative sufficiency; all 562 record rows remain record-level traceability only.

The architecture report's changed `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` reference was reread in its current form. Directory-level references were not narrowed into test authority because MLC-R is not open. Unresolved code/test references were not used, because implementation and tests are lower-precedence and forbidden as authority in this leaf.

## C-xxx, D-xxx and normative-completion mapping

Direct and boundary-adjacent traceability is retained in `c_d_mapping.tsv`.

- Direct bounded M01 obligations: `C-001/D-001`, `C-002/D-002`, `C-003/D-003`, `C-007/D-007`.
- Typed-options M01/M03 boundary obligation: `C-004/D-049`. M01 owns the typed options source evidence, source/capture identity, source temporal truth, schema/version and validation state; M03 owns preparation and derivation into cognition-stage inputs. The historical proof or implementation status is not reopened in MLC-A.
- M01 lineage/temporal contributions with downstream ownership explicitly excluded: `C-015/D-015`, `C-025/D-025`.
- Surface 5.1 rows owned by M00 or other modules and therefore outside bounded M01: `C-021/D-021`, `C-048/D-048`.
- Accepted normative-completion support: `N-01` for the typed options source contract and the distinctions preserved by `docs/03.2`. It is supporting current authority, not a new mutation gate.

Historical `D-xxx` scheduling and prior Gate C statuses are traceability only. They do not reopen tests or implementation and are not used as current execution authority.

## Sufficiency and contradiction assessment

### Explicitly governed

- source/provider identity and acquisition channel;
- distinct source-issued and repository-owned capture identity;
- typed, versioned source-family contracts;
- offline/recorded/check-in/operator-bundle admission;
- immutable captured evidence or governed immutable reference plus fingerprint;
- source observation time/date and repository capture time;
- preservation of original precision and timezone truth;
- explicit validation/limitations;
- fail-closed missing mandatory authority;
- controlled family registration and provider substitution;
- separation from preparation, packet carriage and downstream decisions.

### Architecture allocation only

- target public-interface names such as `SourceArtifactEnvelope`, `CaptureReceipt`, `RawSignalBatch` and `SourceAdapter`;
- target path placement;
- M13 participation as an allocation fact.

Those names and paths may guide later MLC-P/implementation work but are not required to reach this authority-sufficiency disposition.

### Missing definitions that do not block this bounded leaf

- exact non-temporal common field names beyond the admitted semantic facts;
- per-family mandatory/optional/not-applicable tables for every future provider;
- concrete capture-store technology and retention duration;
- restart recovery and authoritative replay packaging;
- exact M13 command/receipt integration;
- role-specific M04 lineage subsets;
- exact later proof cases and implementation placement.

These are later contract, proof, implementation or operations questions. The bounded source-admission meaning can be specified without inventing them.

### Contradictions

No active numbered normative contradiction was found for the bounded question.

Atlas candidate rows contain mixed, stale, split and rejected intent, but they do not contradict current authority because they are not promoted. Stale Atlas paths and lower-precedence code/test references are explicitly excluded.

### Boundary collisions

- M00 transports and composes; it cannot own source truth.
- M02 interprets calendar semantics; M01 routes admitted calendar/reference source material to M02 without deciding calendar truth.
- M03 prepares/enriches other admitted source/raw-signal material; M01 routes that material to M03 without resolving prepared fields.
- M04 carries deliberate packets; packet identity/time do not replace source/capture identity/time.
- M13 supplies transaction mechanics; M01 retains semantic ownership of raw artefacts/capture receipts.

No unresolved collision blocks the bounded contract.

## What this leaf does not establish

This leaf does not:

- accept or reject any test;
- define MLC-R routing;
- create a proof specification;
- write expected-red proof;
- inspect or accept implementation;
- prove durability, restart recovery or authoritative replay;
- select storage or deployment technology;
- authorise live providers, credentials, paper trading or live trading;
- open M01 production or test mutation;
- accept M01 independently.

## Next lawful gate

If and only if an independent Project Manager accepts this proposal, the next lawful gate is:

`M01-PROOF-MLC-R-V1`

No MLC-R, MLC-O, MLC-D, MLC-P, MLC-T, MLC-V or implementation work was performed.

## Mutation statement

No source, test, configuration, vocabulary, normative document or canonical programme-control file was modified in Phase B. The only changed paths are this worker record and worker-owned evidence under `project_control/canonical_project_manager/modules/M01/raw_validation/mlc_a_v1/`.


## 2026-07-31 fast-track closure

The historical MLC-A proposal above remains the accepted authority record. Under
the current MVP ExecPlan, the former later MLC leaf sequence was superseded by
`C-NORM → C-PROOF → module-local Gate D`.

### Accepted bounded implementation

M01 now provides one offline, contract-driven source-admission seam that:

- resolves only explicitly registered family, contract and schema versions;
- enforces declared provider and acquisition-channel substitution law;
- preserves owner-issued source identity separately from repository capture
  identity and payload fingerprint;
- preserves source temporal truth at declared precision and requires UTC for
  source instants;
- requires a typed payload whose serialised material equals the captured input;
- records explicit limitations and an honestly `volatile_alpha` capture receipt;
- rejects unsupported families, shape guessing, fabricated identity/time,
  recursive credential or decision authority, and other downstream ownership.

The compatibility changes are limited to recursive external-source validation,
rejection of untyped raw-bundle fallback shapes and carriage of optional source
observation time on the raw upstream signal contract.

### Acceptance evidence

| Check | Result |
|---|---|
| Focused M01 public-seam proof | PASS — 18 / 18 |
| Reference and false-positive mutant subset | PASS — 9 / 9 |
| Proof-block manifest | PASS — 54 / 54 |
| Proof-executor contract | PASS — 21 / 21 |
| Direct repaired compatibility cases | PASS — 4 / 4 |
| Routed M01 shadow | 169 passed / 34 failed versus 165 / 38 at the M01 baseline |
| Full Tier A shadow | 1,334 passed / 267 failed versus 1,312 / 271 at the M01 baseline; zero new failing nodes, four resolved |
| Tier B | PASS — 49 / 49 |
| Tier C | no tests collected |
| Architecture, compile and diff checks | PASS |
| Global vocabulary shadow | unchanged at 50 pre-existing candidates; no M01 semantic candidate added |
| Pinned Ruff | UNAVAILABLE — configured mirror returned HTTP 404 for locked `pytokens==0.4.1`; no unpinned substitute used |

Exact commands, outputs, comparisons and hashes are retained under
`raw_validation/fast_track_v1/`.

### Scope ceiling

This acceptance does not establish live provider connectivity, credentials,
production durability, restart recovery, authoritative replay, every future
provider family, M02 calendar interpretation, M03 preparation, M04 packet
carriage or any cognition, risk, capital, execution or lifecycle authority.

### Next active slice

`M07:K12 C-NORM` — coefficient/modifier identity and version, precedence and
conflict law, bounds, application ordering and application-receipt meaning.
