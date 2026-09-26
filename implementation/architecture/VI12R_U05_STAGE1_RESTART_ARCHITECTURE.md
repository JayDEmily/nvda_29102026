# VI-12R U05 Stage 1 — Restart Architecture and Durable Contract

## Status

**WORKER STAGE-1 DESIGN — U05 PRODUCTION IMPLEMENTATION NOT STARTED**

This record executes Stage 1 of the active root `EXEC_PLAN.md` only. It derives the durable
reconstruction/query contract required to carry the accepted U01-U04 Raw Signal Occurrence Truth
semantics across complete loss of process-local owner state.

It does not implement PostgreSQL, Psycopg, SQL DDL, U05 production behaviour, or U05 proof repair.
Stage 2 remains prohibited until this design state is committed and handed off cleanly.

## 1. Bound starting state

The semantic source baseline is the accepted U04 production candidate:

- candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- production tree: `3c7a42eb215d708a0f8d8db37727133ecc234275`;
- independent Reviewer-032 PASS: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`;
- accepted units: U01, U02, U03 and U04.

The active U05 work branch was created from the accepted recovery line after the successor ExecPlan
was committed on `main` at `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`.

Direct Git comparison establishes that the accepted U04 production path and U01-U04 physical proof
bytes are unchanged between `dc3b448...` and the Stage-1 starting `HEAD`. The `api.py` blob at both
points is `b8aa18ee89ecc3d93d25420a8d09ea69075128e2`.

The active tree contains no tracked U05 `_postgres.py` and no carried-forward CP0-CP8/checkpoint
implementation state. Historical U05 branches remain Git evidence only.

## 2. Authority used for this design

This design is derived from, and does not extend, the following current authority:

- root `GUARDRAILS.md` and `AGENTS.md`;
- active root `EXEC_PLAN.md`;
- accepted `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`, especially BC-003 through
  BC-013 and BC-016;
- accepted `handoff/authority/VI04_AUTHORITY_CLOSURE.md`;
- `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`, especially IWO-U01 through
  IWO-U05;
- accepted proof obligations `IA17-PROD-002` through `IA17-PROD-010`, repaired
  `IA22R01-PROD-009`, and supporting `IA17-ARCH-003`;
- accepted U04 implementation and Reviewer-031/032 disposition evidence.

The VI-04 authority permits the smallest correctness-only PostgreSQL relation/type/constraint and
repository/adapter form needed for BC-011, with direct `psycopg[binary]==3.3.4`. It does not transfer
Raw Signal semantic ownership to PostgreSQL or permit partitioning, pooling, performance indexes,
SLA/recovery claims, P01/K01, provider integration or other preserved Unknowns.

## 3. Architectural conclusion

U05 must use **durable query-on-demand semantics**, not caller-managed reconstruction and not an
eager process-local cache as correctness authority.

A completely fresh owner starts with no U01-U04 semantic cache. Each public command obtains, inside
its own authorised transaction where mutation is involved, the durable facts or technical query
results needed for the M00 owner itself to make the accepted semantic decision. Public referential
reads also query durable state directly.

Process-local caching may not be required for U05 correctness. If a later implementation introduces
any cache for convenience, durable state remains the authority for every restart-sensitive decision,
and the cache cannot be required to make the command correct.

This directly avoids the abandoned design failure where append/read-by-identity persistence retained
records but a fresh owner lacked the durable set/relationship state needed to enforce accepted
semantics.

## 4. Restart/reconstruction inventory

The table below is the Stage-1 inventory required by ExecPlan 5.1. `Current state` names the accepted
U04 process-local state presently used by `api.py`; it is descriptive evidence, not new authority.

| Restart-sensitive invariant | Current U04 process-local state | Durable requirement after empty-process restart | Owner decision / public discriminator | Failure if unavailable |
| --- | --- | --- | --- | --- |
| Same policy identity/version is idempotent only for identical content | `policies_by_identity` | Read policy by `(scope_policy_id, scope_policy_version)` | `register_capture_scope_policy`; same value returns original, changed content rejects | Fresh owner could overwrite/re-admit conflicting policy |
| At most one active policy interval exists at an instant | all values of `policies_by_identity` | Enumerate durable policies sufficient for owner-side interval-overlap evaluation | Register a later/non-overlapping version and challenge an overlapping version after restart | Fresh owner could admit overlapping schedule universes |
| Effective policy reference resolves to exact policy lineage | `policies_by_ref` | Read policy by stored `scope_policy_ref` | Capture realisation, relation derivation, assessment derivation | Fresh owner could treat an unregistered/mismatched policy ref as valid or lose eligibility lineage |
| Stable owed-slot retry `(scope_policy_ref, slot_start_utc)` maps to at most one capture | `captures_by_slot` | Read capture by stable slot key | Repeat capture realisation after restart with same and different capture IDs | Fresh owner could create a second capture for one owed slot |
| Capture occurrence identity cannot move to another slot | `captures_by_identity` | Read capture by `capture_occurrence_id` | Reuse same capture ID against another slot after restart | Identity could be rebound to different schedule truth |
| Capture readback preserves schedule/policy context | `captures_by_identity` | Read durable capture by domain identity | `get_scheduled_capture_occurrence` from fresh owner | Referential readback fails or loses schedule context |
| Observation same-ID retry requires exact NativeValueV1/content equality | `observations_by_identity` | Read full durable observation by `observation_occurrence_id`, including exact native type representation | Retry exact observation and conflicting representation after restart | Fresh owner could accept changed content or fail lawful retry |
| Ingestion sequence does not decrease within one local scope | `ingestion_high_water_by_scope` | Obtain durable maximum admitted sequence for the exact `ingestion_sequence_scope` in the admission transaction | Admit lower/equal/higher sequence in fresh process after prior durable observation | Restart resets high-water and permits a decrease |
| Ingestion high-water remains scope-local | `ingestion_high_water_by_scope` | Scope-qualified durable max/query only | Interleave independent scopes after restart | One scope can incorrectly constrain another or global order is invented |
| Observation remains referentially readable with native/provenance/temporal fidelity | `observations_by_identity` | Read the complete durable observation by domain identity and reconstruct exact v1 carrier types | `get_raw_observation_occurrence` in fresh owner | Readback loses native type/value, absence/null or provenance/time distinctions |
| Receipt relation uses exact durable observation, capture and effective policy facts | observation/capture/policy maps plus optional `relations_by_key` | Read observation, capture and policy by durable identities; no durable relation cache is required | Derive relation in a fresh owner with the admitted eligibility authority | Relation can depend on lost cache or wrong effective policy |
| Optional relation materialisation must not control assessment truth | U04 assessment scans `observations_by_identity`; relation cache is not its evidence source | Query durable in-slot observations independent of relation materialisation | Append assessment after restart without first deriving relation | Restart reintroduces the U04 R031 false-negative class |
| Assessment uses capture-local eligible committed observation evidence | `observations_by_identity` + capture/policy state | Query durable observations whose receipt time is in the exact capture `[start,end)` window, then apply admitted eligibility authority in M00 | Fresh-owner zero/one assessment path | Fresh owner can fabricate zero or miss eligible durable evidence |
| Missing eligibility authority fails closed where in-slot evidence requires adjudication | `eligibility_resolver` construction input | Resolver remains an admitted construction dependency; durable observation/policy facts must be available to call it | Fresh owner with in-slot evidence and absent resolver | Missing authority could be masked as `zero_received` |
| Same assessment ID retry returns original outcome even if later evidence now exists | `assessments_by_identity` | Read assessment by `assessment_occurrence_id` before any new outcome derivation | Retry earlier zero after later observation is durable | Restart could recompute same ID to a different outcome |
| Assessment identity reuse with changed command content rejects | `assessments_by_identity` | Full assessment read by ID | Same ID with changed capture/as-of/supersession after restart | Conflicting identity reuse could be accepted |
| Assessment history is append-only and supersedes only immediate predecessor | `assessment_order_by_capture` + `assessments_by_identity` | Ordered durable assessment history for exact capture | Append first, lawful successor and non-immediate successor from fresh owners | Restart loses predecessor/current-chain truth or permits branching/overwrite |
| Assessment list/readback preserves history | same assessment maps/order | Read assessment by ID and list ordered chain by capture | Fresh `get_...assessment` and `list_...assessments` | Original assessment state cannot be replay-read referentially |
| Explicit restart reconciliation finds an already-realised owed slot | `captures_by_slot` | Slot-key capture query against durable state | Fresh `reconcile_owed_slots` with pre-existing durable capture | Reconciliation duplicates capture or loses stable slot identity |
| Explicit restart reconciliation creates a missing owed slot as capture + `unknown_not_established`, never zero | no U04 implementation; U05 placeholder only | Durable policy/slot query, capture write, assessment-history query, and assessment write | Reconcile declared slot from a fresh owner | Absence may be misclassified as zero or remain process-only |
| Interrupted reconciliation after capture commit is resumable | no U04 implementation; BC-011 requires own transactions/no cross-kind atomicity | Durable capture must be discoverable on retry; absence of assessment must be separately discoverable | Fault after capture commit, fresh retry, then read both facts | Partial success becomes unrecoverable or is hidden by false atomicity |
| Original policy/capture/observation/assessment facts remain referentially readable | four U04 state families | Direct durable reads by domain identity with policy/schedule/lineage fields intact | Destroy owner; construct fresh owner; read originals | U05 would prove storage but not BC-011/IA17-PROD-010 referential readback |

### 4.1 State that does not require semantic cache reconstruction

The following accepted U01-U04 behaviour is stateless once the durable records are reconstructed
correctly and therefore does not justify a persistent semantic cache:

- exact typed identity wrappers and constructor validation;
- canonical concept/contract constants;
- half-minute boundary validation and interval arithmetic;
- NativeValueV1 snapshot/validation and exact comparator logic;
- temporal-kind discriminant validation;
- relation role and other fixed v1 constants.

Those rules still apply to values reconstructed from PostgreSQL; PostgreSQL does not replace them.

## 5. Minimum M00 persistence contract

The U05 port must be derived from the inventory above. The abandoned identity-only append/get protocol
is insufficient because it cannot answer set/relationship questions needed by a fresh owner.

The minimum logical contract is a transaction factory yielding a **record/query transaction** with
only technical data operations. Exact Python names remain an implementation detail for Stage 2, but
the capability set is fixed here.

### 5.1 Transaction lifecycle capability

The port provides an internal transaction context used only by M00 implementation code:

- enter transaction;
- perform authorised record reads/queries and at most the semantic fact write owned by that command;
- commit on successful context exit;
- return control to the public command only after commit acknowledgement;
- rollback/abort on exception;
- never convert a failed transaction into an empty/unknown/zero semantic result.

Read-only public reads may use a read transaction but cannot mutate durable state.

### 5.2 Policy record/query capability

Required technical operations:

- get policy by `(scope_policy_id, scope_policy_version)`;
- get policy by exact stored `scope_policy_ref`;
- enumerate policies needed for owner-side active-interval overlap checking;
- append one already-validated `CaptureScopePolicyV1` record.

The adapter does not decide whether policies overlap. M00 evaluates `_intervals_overlap` against the
returned records. Database uniqueness/locking may prevent races but does not create the semantic rule.

### 5.3 Capture record/query capability

Required technical operations:

- get capture by `capture_occurrence_id`;
- get capture by stable `(scope_policy_ref, slot_start_utc)` key;
- append one already-decided `ScheduledCaptureOccurrenceV1` record.

The adapter does not decide whether a slot is owed. M00 resolves the effective policy and applies
activation/deactivation and exact-slot law before creating the record.

### 5.4 Observation record/query capability

Required technical operations:

- get observation by `observation_occurrence_id`;
- obtain the maximum admitted `ingestion_sequence` for one exact `ingestion_sequence_scope`;
- enumerate observations with `received_ts_utc` inside one exact capture receipt window;
- append one already-validated `RawObservationOccurrenceV1` record.

The maximum query is a technical projection over already-durable observations. M00 decides whether a
new sequence is lawful. Receipt-window enumeration is only a candidate evidence query; M00 applies
eligibility authority and decides assessment truth.

### 5.5 Assessment record/query capability

Required technical operations:

- get assessment by `assessment_occurrence_id`;
- list all assessments for one `capture_occurrence_id`;
- append one already-decided `CaptureReceiptPresenceAssessmentV1` record.

The adapter does not decide zero/one/unknown or supersession meaning. M00 first resolves any existing
same-ID record, then obtains capture/policy/evidence/predecessor state, reconstructs the capture-local chain in M00, and constructs the semantic
assessment.

### 5.6 Receipt-relation persistence

No PostgreSQL receipt-relation table is required for U05 correctness.

BC-007 makes relation materialisation optional. BC-011 and IWO-U05 require durable logical
representations/readback for policy, capture, assessment and raw observation facts; they do not make
optional relation materialisation a prerequisite for restart correctness or referential readback.
A relation can therefore be re-derived by M00 from durable observation/capture/policy facts plus the
admitted eligibility authority.

Persisting relation materialisation merely to recreate a process-local cache would reintroduce the
R031 class and is not part of the minimum U05 design.

## 6. Minimum PostgreSQL physical design

VI-04 delegates the smallest correctness-only physical relation/type/constraint design. Stage 1
selects four semantic-fact tables and no performance-only structures.

Names below are design names; Stage 2 may choose equivalent implementation-local identifiers without
changing the contract.

### 6.1 `rsot_capture_scope_policy_v1`

Stores:

- `scope_policy_id` — `text`;
- `scope_policy_version` — integral PostgreSQL numeric representation;
- `scope_policy_ref` — `text`, stored explicitly because the opaque policy ID is not safely parseable
  from the ref string;
- `activation_ts_utc` — `timestamptz`;
- `deactivation_ts_utc` — nullable `timestamptz`;
- `eligibility_policy_ref` — `text`.

Correctness constraints:

- primary key `(scope_policy_id, scope_policy_version)`;
- unique `scope_policy_ref`;
- no performance index beyond structures intrinsic to correctness constraints.

M00 continues to validate exact concept/contract/units, version positivity, slot alignment,
deactivation ordering and interval non-overlap. Registration transactions must serialize the overlap
read/check/write race sufficiently that two concurrent registrations cannot both evade the accepted
non-overlap rule.

### 6.2 `rsot_scheduled_capture_occurrence_v1`

Stores:

- `capture_occurrence_id` — `text`, primary key;
- `scope_policy_ref` — `text`, foreign key to policy;
- `slot_start_utc` — `timestamptz`;
- `slot_end_utc` — `timestamptz`.

Correctness constraints:

- unique `(scope_policy_ref, slot_start_utc)` stable owed-slot key;
- referential constraint to the stored policy ref.

M00 continues to decide policy activity and exact 30-second schedule truth. The unique stable-slot
constraint closes concurrent duplicate physical creation; it does not decide that the slot is owed.

### 6.3 `rsot_raw_observation_occurrence_v1`

Stores the complete observation fact:

- `observation_occurrence_id` — `text`, primary key;
- delivery/provider identities — `text`;
- exact native record — versioned `bytea` codec described in section 7;
- `received_ts_utc` — `timestamptz`;
- `received_epoch_ns` — nullable integral PostgreSQL numeric representation;
- `ingestion_sequence` — integral PostgreSQL numeric representation;
- `ingestion_sequence_scope` — `text`;
- `source_temporal_kind` — `text`;
- `raw_signal_catalogue_ids` — nullable ordered `text[]`;
- all accepted optional source/provenance/timezone/session/revision headers — nullable `text`.

There is no separate semantic high-water table. The durable high-water is the maximum sequence among
committed observations in the exact scope. The observation admission transaction must serialize its
scope-qualified high-water check and insert strongly enough to prevent a concurrent lower sequence
from being accepted after a higher durable sequence. A correctness-only database lock is permitted;
no throughput/performance claim follows.

### 6.4 `rsot_capture_receipt_presence_assessment_v1`

Stores:

- `assessment_occurrence_id` — `text`, primary key;
- `capture_occurrence_ref` — `text`, foreign key to capture;
- `outcome` — constrained text over the three accepted values;
- `evidence_as_of_ts_utc` — `timestamptz`;
- `supersedes_assessment_ref` — nullable self-reference.

Correctness constraints must preserve one append-only capture-local chain in the presence of physical
write races. At minimum the database representation must prevent one assessment identity from being
reused and one predecessor from gaining multiple successors. M00 still decides whether the caller's
supersession reference is exactly the immediate current predecessor. The assessment command must
serialize the capture-local predecessor read/check/write sufficiently to prevent two concurrent
commands from both becoming the current successor.

No UPDATE/DELETE semantic operation is part of the U05 persistence port.

### 6.5 Excluded physical structures

Stage 1 deliberately does not introduce:

- a receipt-relation table;
- a semantic cache table;
- a replay/run table;
- a provider mapping table;
- partitioning;
- pooling;
- performance/SLA indexes;
- retention/deletion machinery;
- cross-kind transaction wrappers.

## 7. Exact value reconstruction

Fresh-owner correctness requires reconstructed values to satisfy the same exact U01-U04 type/content
law as in-memory values.

### 7.1 Identity and ordinary fields

Opaque identity values are stored as text and reconstructed through their exact typed identity
constructors. PostgreSQL text does not become identity authority.

UTC datetimes are stored as `timestamptz` and reconstructed as UTC-aware Python `datetime` values.
The adapter/session must not substitute local timezone meaning.

Structural optional field absence may use SQL `NULL` only as a storage representation of absence.
This does not collapse provider-native null: a provider-native `None` inside `native_record` is encoded
as a typed native value in the native codec and remains distinct from an absent semantic header.

### 7.2 NativeValueV1 codec

`json/jsonb` alone is insufficient because it can collapse distinctions that U03 explicitly preserves,
including `int` versus `float`/`Decimal`, list versus tuple, bytes and exact IEEE-754 float content.

The minimum design therefore stores `native_record` in `bytea` using a versioned, deterministic,
non-semantic codec with explicit type tags for:

- `None`;
- `bool`;
- arbitrary Python `int` representation;
- `float` as its exact 64-bit IEEE-754 bytes;
- `Decimal` as exact sign/digits/exponent tuple content;
- UTF-8 `str`;
- raw `bytes`;
- list;
- tuple;
- mapping with exact string keys and recursively encoded NativeValueV1 values.

The codec performs no value normalisation, timezone inference, provider mapping or semantic decision.
Decode reconstructs the finite accepted NativeValueV1 carrier before the public dataclass validation
runs. A codec version prefix permits technical evolution without silently changing v1 value meaning.

## 8. Command transaction model

Each semantic mutation below returns success only after the transaction containing that fact has
committed. A transaction exception propagates as failure and no semantic empty/unknown/zero fallback
is fabricated.

### 8.1 Register policy

Within one policy transaction M00:

1. reads same identity/version;
2. if present, compares full accepted content and returns the original only after no write is needed;
3. otherwise enumerates durable policies and applies owner-side overlap law;
4. validates ref uniqueness;
5. appends the policy;
6. exits the transaction and returns only after commit acknowledgement.

The transaction must serialize the overlap read/check/write race. PostgreSQL may enforce physical
uniqueness/race exclusion, but an adapter exception is not itself the semantic diagnosis; M00 rebinds
the durable record facts before returning an identity/overlap conflict.

### 8.2 Realise capture

Within one capture transaction M00:

1. resolves durable effective policy by exact ref;
2. applies activation/deactivation and exact slot law;
3. reads the stable slot key;
4. returns the existing capture for an identical slot retry, or rejects a different capture ID;
5. separately rejects an existing capture ID bound elsewhere;
6. appends a new capture if lawful;
7. returns only after commit acknowledgement.

### 8.3 Admit observation

Within one observation transaction M00:

1. reads same observation ID;
2. if present, applies the accepted exact NativeValueV1/full-record comparator and returns the original
   only for identical content;
3. otherwise obtains durable scope-local high-water;
4. rejects a lower sequence and permits an equal/higher sequence according to accepted U03 law;
5. appends the full observation;
6. returns only after commit acknowledgement.

The high-water check and append are one correctness unit and must be serialized accordingly.

### 8.4 Derive receipt relation

The relation command uses a read transaction to obtain the durable observation, capture and exact
effective policy. M00 applies slot locality and the admitted eligibility resolver and constructs the
relation if eligible.

No preparatory read/hydration by the caller is required. No relation persistence is required. A fresh
owner can derive the same governed proposition from the durable facts plus the same admitted
eligibility authority.

### 8.5 Append assessment

Within one assessment transaction M00:

1. reads same assessment ID first;
2. if present, validates the caller-supplied capture/as-of/supersession identity inputs and returns that
   original record without recomputing outcome from later evidence;
3. resolves durable capture and effective policy;
4. queries durable observations in the exact capture receipt window;
5. where in-slot evidence exists, invokes the admitted eligibility resolver; missing required
   eligibility authority fails closed;
6. derives `zero_received` or `one_or_more_received` in M00 from eligible committed evidence;
7. obtains all durable assessments for the capture, reconstructs the single-predecessor chain in M00, and validates first/immediate-predecessor law;
8. appends the already-decided assessment;
9. returns only after commit acknowledgement.

The evidence query and assessment append occur in the same assessment transaction. Receipt time is
used only for capture-window locality; it is not compared with or substituted for the supplied
`evidence_as_of_ts_utc`.

### 8.6 Referential reads

Public policy/capture/observation/assessment reads query PostgreSQL directly through the internal
technical port and reconstruct exact public v1 records. Assessment list read obtains the durable capture-local assessment set and M00 reconstructs the accepted single-predecessor chain order before returning it.

Read methods cannot write or perform semantic outcome decisions.

## 9. Restart reconciliation model

`reconcile_owed_slots` is an explicit M00 command over caller-declared slot/capture/assessment
identities. It does not generate the schedule universe and does not scan time ranges on its own.

For each requested slot, M00 performs two independently committed semantic-fact steps because BC-011
forbids a cross-kind atomicity claim.

### 9.1 Capture step

In the capture's own transaction:

1. resolve the durable policy and validate the requested slot under accepted U02 law;
2. query durable capture by stable `(scope_policy_ref, slot_start_utc)`;
3. if present, require the caller's capture ID to match and reuse it;
4. if absent, require the caller's capture ID not to be bound elsewhere, append the capture and commit;
5. only after that commit may the capture be treated as durably achieved.

### 9.2 Initial-unknown assessment step

In a separate assessment transaction:

1. read the caller-supplied assessment ID; an existing identical reconciliation-created assessment is
   an idempotent retry;
2. list durable assessments for the reconciled capture;
3. if a current assessment already exists, reconciliation does not infer or append a new zero/unknown
   merely because the process restarted;
4. if no assessment exists, M00 creates the authorised initial `unknown_not_established` assessment
   with no predecessor and commits it;
5. the required `evidence_as_of_ts_utc` is a UTC system-knowledge time sampled for that assessment
   transaction; it must not be substituted with slot time, observation receipt time or provider time;
6. return only after the assessment transaction commits.

The exact technical clock injection/sampling form is a Stage-2 implementation detail constrained by
item 5. No clock-accuracy, drift, wake-latency, SLA or finality claim is created.

### 9.3 Interrupted reconciliation

If the capture transaction commits and the assessment transaction fails, the public reconciliation
call fails. The committed capture remains a truthful durable fact; the failed assessment does not
exist.

A fresh retry finds that capture through the stable slot query, finds no assessment, and appends the
same caller-declared initial unknown assessment. This is the required recovery path and does not
claim cross-kind atomicity or bounded recovery time.

## 10. Public capability boundary

The declared public seam remains the M00 owner `commands` and `reads` facets returned by
`create_owner`. The concrete PostgreSQL adapter, connection and record transaction are construction
mechanisms and are not returned by either facet.

The Stage-2 construction must satisfy all of the following:

- the concrete PostgreSQL class is not exported through the M00 public `__all__`;
- owner public facets expose only semantic command/read methods;
- no public/data attribute on the returned owner/facets references the concrete adapter, connection,
  cursor, transaction object or a raw mutation repository;
- no command/read method returns such an object;
- a caller cannot obtain an append/SQL capability by following the ordinary returned owner object
  graph;
- technical port methods accept/return records/query data only and expose no eligibility, relation,
  assessment-outcome, supersession or schedule-truth decision method.

The constructor may receive the technical persistence dependency because A00 is authorised to
construct/inject it. Possessing a constructor dependency does not make it part of the returned owner
public object graph.

This boundary is stronger than relying on an underscore name. Stage 2 must challenge the realised
object graph as soon as the adapter is wired, before later semantic slices are added.

## 11. Fresh-owner construction rule

A U05 restart proof is valid only when the second owner is newly constructed with:

- empty process-local semantic state;
- the authorised PostgreSQL persistence dependency pointing at the already-committed database;
- the admitted eligibility authority where the scenario requires it;
- no test/caller reads performed merely to populate owner state before the command under test.

The owner itself may issue the durable queries required by the command. Those queries are part of the
production semantic path and are not caller-managed hydration.

## 12. Proof implications for later stages

The current pre-implementation U05 physical proof contains an older record-only storage protocol
(`append/get/list` by identity). That proof remains lower-layer evidence and is not architecture
authority. Stage 2/3/4 proof repair will need to discriminate the transaction/query contract above,
including at minimum:

- fresh-owner policy overlap after restart;
- fresh-owner stable slot retry/conflict;
- interrupted reconciliation after capture commit;
- durable observation high-water after restart;
- assessment from durable observations without relation materialisation;
- stable same-assessment-ID retry after later evidence;
- durable immediate-predecessor enforcement;
- public object-graph absence of raw persistence mutation capability.

Proof changes may strengthen discrimination but may not weaken the accepted U01-U04 or U05
propositions to match implementation convenience.

## 13. Remaining Unknowns and blocker assessment

No Stage-1 semantic authority blocker was established.

The following remain deliberately unresolved exactly as current authority requires and are not needed
to begin Stage 2:

- concrete provider eligibility/scope/mapping contents — the resolver remains an admitted external
  authority dependency keyed by durable policy lineage;
- provider duplicate/revision equivalence;
- exact clock accuracy/drift/leap/smear/wake characteristics — the reconciliation assessment needs
  only a UTC system-knowledge sample and makes no accuracy/SLA claim;
- provider-specific ingestion-scope/overflow details — U05 preserves only the already-typed local
  scope and no-global-order law;
- partitioning, pooling, performance indexing, throughput/SLA, retention/deletion and bounded
  recovery;
- opaque-ID generation/collision/cross-process allocation — reconciliation continues to receive
  caller-declared identities through the accepted public seam;
- replay/P01/K01/provider/network/downstream semantics.

If Stage 2 discovers that one of these values is actually required for correctness, it must stop at
that exact dependency rather than choose a default.

## 14. Stage-1 exit proposition

This design explains, invariant by invariant, how a fresh owner can enforce every identified
restart-sensitive U01-U04 decision from durable records/queries without caller-managed hydration:

- policy identity, overlap and effective-policy lookup;
- capture identity and stable owed-slot lookup;
- observation identity, exact content and scope-local high-water;
- eligible durable evidence access independent of optional relation materialisation;
- assessment same-ID stability, append-only history and immediate predecessor;
- interrupted explicit owed-slot reconciliation;
- referential readback of original policy/capture/observation/assessment facts.

The next lawful engineering stage is Stage 2 only after this Stage-1 design/evidence state is committed
cleanly. Stage 1 itself adds no PostgreSQL production implementation.
