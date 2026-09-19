# VI-05 — Implementation Work Order Candidate 001

## Status

**CANDIDATE FOR VI-06 INDEPENDENT CHALLENGE.**

This work order does not itself claim implementation, proof, architecture admission or promotion. It is the bounded engineering decomposition of the exact accepted Raw Signal Occurrence Truth BICP after VI-04 authority closure.

No physical product tests or product/runtime implementation are authored by VI-05.

## 1. Exact authority binding

The work order is bound to:

- IRB SHA-256 `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`, 20,559 bytes;
- implementation-authorisation reference `IA-AUTH-001`;
- accepted BICP `BICP-CANDIDATE-005` JSON SHA-256 `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- METHOD-006 baseline `7c76b1dc87a9773e92841cae47e34b3b50190614` / tree `3cf7d5e78a490611076a6317f3b709b692cdf553`;
- BUILD-001 baseline `17263909abae9ca8cabb2440db282d12ff492ad6` / tree `26c421f7cbc75d61ea3e538d79091f4e01136585`;
- accepted VI-04 authority record SHA-256 `4909bfb3561f4ad08d21d82005f2aa60ed9c18440067c91180f6ee65c85bc9ca`;
- accepted VI-04 predecessor commit `d08fb6c466cbe3bfce356ade647df247d00e7dad` / tree `be645c678ddff01f2074d67a75f48d9099f1bd18`.

The accepted meaning is not reopened by this work order.

## 2. Bounded target

Implement one current post-reset category-`M` semantic owner for **Raw Signal Occurrence Truth** and modify existing `A00` only enough to construct and call it.

The owner identity remains resolver-selected until VI-07. The IA-time candidate `M00` is informative only until re-resolution.

Current VI-04 authority fixes:

- owner package: `nvda_desk.raw_signal_occurrence_truth`;
- M public seam: `nvda_desk.raw_signal_occurrence_truth.api`;
- PostgreSQL Python driver: `psycopg[binary]==3.3.4`;
- PostgreSQL `17.9` as the recorded proof environment only, not a production-version requirement;
- bounded delegation for the smallest correctness-only PostgreSQL relation layout, SQL types and dependent direct repository/adapter form required by BC-011.

Still not authorised:

- P01/DMPV3;
- K01 selection/activation;
- authoritative replay/re-execution;
- provider/API/network integration;
- live external effects/accounts;
- downstream business consumers;
- retention/deletion policy;
- RTO/RPO/recovery/throughput/SLA claims;
- PostgreSQL partitioning or pooling;
- independently designed performance indexes;
- final distribution naming/version metadata before VI-15 authority closure.

## 3. Semantic owner and ownership boundary

The M owner alone owns:

1. immutable capture-scope policy-version meaning;
2. owed 30-second scheduled capture occurrence meaning;
3. actual raw-observation occurrence meaning;
4. receipt-evidence relation meaning;
5. append-only receipt-presence assessment meaning;
6. semantic transaction-success/durability and referential-read meaning.

`A00` owns construction, source/scheduler translation and top-level lifecycle only. PostgreSQL, Psycopg, SQL schema, repository/store, adapters, tests and configuration mechanisms remain non-owning.

The authorised runtime architecture is only:

```text
A00 -> M-owner public seam
```

There is no reverse M -> A00 dependency and no runtime P/K/G/S edge for this unit.

## 4. Public contract target

The M public seam must expose typed representations of the exact five `.v1` payload contracts:

- `nvda.raw_signal.CaptureScopePolicy.v1`;
- `nvda.raw_signal.ScheduledCaptureOccurrence.v1`;
- `nvda.raw_signal.RawObservationOccurrence.v1`;
- `nvda.raw_signal.CaptureReceiptEvidenceRelation.v1`;
- `nvda.raw_signal.CaptureReceiptPresenceAssessment.v1`.

The seam must provide typed command and referential-read facets for A00. Exact private class/helper/module names remain implementation freedom. The later accepted proof may fix additional test-facing private construction symbols only where necessary to exercise a boundary; those symbols do not become semantic authority.

The command capability must be sufficient to perform, without adding stronger meaning:

- register an immutable capture-scope policy version;
- realise or idempotently recover one owed scheduled capture occurrence for a lawful slot;
- admit/retry one raw observation occurrence;
- derive receipt-presence relation truth when separately admitted eligibility authority establishes eligibility;
- append a receipt-presence assessment under the exact three-state/supersession law;
- reconcile explicitly requested owed schedule slots after restart without promising a catch-up horizon.

The read capability must retrieve original policy/capture/observation/assessment facts by their domain identities with required lineage/schedule context. Receipt-evidence relation may be materialised or derived on demand; this work order does not require a persistence table for it.

### Eligibility boundary

Concrete provider eligibility/mapping remains BC-016 Unknown and is not implemented in this tranche. Relation derivation must therefore consume a controlled, separately admitted/configured eligibility decision or resolver input and preserve its policy-lineage reference. The M owner decides only what the established eligibility fact means for Raw Signal receipt evidence. A00/provider fixtures must not silently define new Raw Signal semantics.

### Opaque identity boundary

Production opaque-ID generation/collision/cross-process recovery remains BC-016 Unknown. Tests and bounded implementation may use supplied/injected opaque IDs or an injected technical ID source. The semantic owner remains responsible for identity-layer separation, retry equality/conflict rules and no cross-layer substitution; this tranche makes no production ID-generator fitness claim.

## 5. PostgreSQL implementation boundary

BC-011 requires real PostgreSQL-backed logical durability. Under VI-04, the implementation worker may choose the smallest correctness-only physical design satisfying the accepted behavior.

The minimum logical persistence responsibilities are distinct append-oriented representations for:

1. capture-scope policy versions;
2. scheduled capture occurrences;
3. raw-observation occurrences;
4. receipt-presence assessments.

Receipt-evidence relation is not required to be stored.

### Physical-design law

The worker may choose table names, columns and direct repository/adapter decomposition only under these constraints:

- opaque/domain/provider/delivery identities must not be collapsed into one universal identifier;
- physical SQL types must preserve the exact typed payload meaning and lawful absence distinctions;
- UTC instants must preserve at least the required microsecond precision;
- `source_timestamp_raw` and provider timezone/native material must not be normalised into invented event time;
- native record data must round-trip without the owner or SQL layer rewriting provider logical names/values under the admitted mapping;
- same occurrence identity + identical content is idempotent; same identity + conflicting content fails closed;
- the stable scheduled-slot retry key admits at most one capture occurrence;
- assessment rows are append-only and supersession must not overwrite the predecessor;
- every occurrence or assessment durability claim is bounded to its own committed transaction;
- no transaction API or schema shape may imply cross-kind atomicity;
- referential readback must reconstruct the exact owner fact and lineage required by BC-011;
- restart reconciliation must operate from committed durable state, not process memory;
- no partitioning or pooling;
- no performance/SLA indexes; database-intrinsic correctness constraints are permitted only where required to enforce an admitted invariant;
- Psycopg 3.3.4 is the Python driver;
- PostgreSQL 17.9 is the recorded proof environment but not a production-version claim.

The selected physical design must be recorded in the implementing unit's evidence before production code is accepted, including the semantic reason for each correctness constraint. The SQL design remains mechanism, not product meaning.

## 6. Risk/coupling-derived realisation units

The units below are ordered by semantic and proof dependency, not by preferred file topology. Each implementation unit receives its accepted proof before production implementation.

### IWO-U01 — Typed contracts, identity layers and owner boundary

**Purpose:** establish the exact public data-contract vocabulary and identity/absence/version invariants used by every later unit.

**Includes:**

- five exact canonical concepts and five `.v1` payload-contract identities;
- separately typed policy/capture/observation/assessment/provider/delivery/concept/schema identities;
- structural absence versus provider-native null distinction;
- allowed temporal discriminants and three assessment outcomes;
- M ownership/write-boundary declarations and A00-only consumer boundary;
- public command/read seam shape sufficient for later units;
- compatibility invariants for `.v1`.

**Must not include:** schedule generation, provider mapping, persistence implementation, packet carriage, replay or downstream consumers.

**Primary proof obligations:** `IA17-PROD-001`, `IA17-PROD-011`, `IA17-PROD-012`; supporting `IA17-ARCH-003`, `IA17-ARCH-005`.

### IWO-U02 — Capture policy and owed-slot truth

**Purpose:** implement immutable policy versions and exact 30-second owed-slot semantics independently of scheduler wake/receipt/provider-event time.

**Includes:**

- activation/deactivation alignment;
- at most one active policy version at an instant in this slice;
- exact `[start,end)` 30-second slots at nominal `:00`/`:30` boundaries;
- no owed slot before activation or at/after deactivation;
- stable `(scope_policy_ref, slot_start_utc)` retry reference distinct from opaque capture occurrence ID.

**Primary proof obligations:** `IA17-PROD-002`; identity portion of `IA17-PROD-008`.

### IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth

**Purpose:** implement one actually received provider logical record as one RawObservation occurrence while preserving native/delivery/receipt/time/provenance truth.

**Includes:**

- provider logical-record and delivery boundaries;
- separable records -> separate observations sharing delivery ref;
- independent no-scope observation validity;
- required receipt UTC and local sequence/scope;
- optional genuine nanosecond receipt evidence only;
- exact `true_instant|date_only|receipt_only` law;
- no inferred provider timezone/event UTC;
- same-occurrence retry versus newly received retransmission identity law;
- no equal-value/provider-ID deduplication.

**Primary proof obligations:** `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005`, observation/identity portions of `IA17-PROD-008`.

### IWO-U04 — Receipt evidence and append-only assessment state

**Purpose:** implement the relation and assessment semantics without membership/count/finality invention.

**Includes:**

- relation only for established eligible active policy plus receipt time inside `[start,end)`;
- `relation_role=evidences_receipt_presence_only`;
- lawful no-relation state for no-scope observation;
- assessment outcomes exactly `unknown_not_established|zero_received|one_or_more_received`;
- as-of system-knowledge time distinct from event/finality/SLA time;
- append-only immediate-predecessor supersession;
- later eligible evidence may supersede zero with one-or-more without overwriting;
- no final assessment concept.

**Primary proof obligations:** `IA17-PROD-006`, `IA17-PROD-007`; state/identity portions of `IA17-PROD-008`.

### IWO-U05 — PostgreSQL durability, idempotency, failure, restart and referential readback

**Purpose:** bind U01-U04 owner facts to real PostgreSQL while preserving semantic ownership and exact transaction claims.

**Includes:**

- direct Psycopg 3.3.4 technical adapter behind the M-owned persistence port;
- smallest correctness-only physical design authorised by VI-04;
- each occurrence or assessment committed in its own transaction;
- durable-success signal only after commit;
- failed write remains unachieved durability and fabricates no semantic fallback;
- retry identical-content success / conflicting-content rejection against durable state;
- restart reconciliation of explicitly requested owed slots from durable policy/capture state;
- missing owed slot -> durable capture plus `unknown_not_established`, with no inferred zero;
- original facts retrievable by domain identity with lineage/schedule context;
- no cross-kind atomicity, bounded-recovery, RTO/RPO, replay-equivalence or retention claim.

**Primary proof obligations:** `IA22R01-PROD-009`, `IA17-PROD-010`; persistence-bearing portions of `IA17-PROD-007`, `IA17-PROD-008`; supporting `IA17-ARCH-003`.

### IWO-U06 — A00 construction and governed sequential composition

**Purpose:** prove and implement the only authorised cross-owner runtime composition.

**Includes:**

- A00 constructs/injects the non-owning PostgreSQL adapter and other technical/configuration inputs;
- A00 constructs the admitted M owner;
- A00 calls only the M typed public command/read boundary;
- declared owner edge exactly `A00 -> M`;
- no `M -> A00`, private-state/table/repository bypass, P01/K01 or downstream consumer;
- startup/shutdown/top-level lifecycle remains A00-owned;
- sequential/end-to-end path exercises admitted behavior without expanding it.

**Primary proof obligations:** `IA17-PROD-013`; `IA17-ARCH-004`, `IA17-ARCH-005`, `IA17-ARCH-006`.

## 7. Architecture obligations before product implementation

Before VI-12R production implementation begins, VI-07/VI-08 must establish the exact current architecture claim and VI-09/VI-10/VI-11 must establish accepted product proof.

Architecture admission must:

- re-run exact implementation-authority ingress and re-resolve the create ID from then-current state;
- consume the resolver-selected M identity durably, never caller-select `M00` by historical resemblance;
- register the M as a truthful active runtime module using package `nvda_desk.raw_signal_occurrence_truth` and public seam `nvda_desk.raw_signal_occurrence_truth.api`;
- record exact bounded responsibility/exclusions/state/time/side-effect ownership;
- bind the M-owned persistence port and non-owning PostgreSQL mechanism;
- modify A00 permitted dependency to the selected M identity;
- declare only `A00 -> M` in the runtime owner graph;
- create only the minimum package/public-seam skeleton required for truthful active registration, with no product decision logic;
- create the implementation-allocation record;
- leave P01/K01/surfaces/inactive capabilities unchanged;
- activate only the architecture proof obligations actually implied by this claim.

`IA17-ARCH-001` through `IA17-ARCH-006` remain separate from product proof.

## 8. Product proof requirements before code

VI-09 must create a separate N15/N19 product-proof control surface. VI-10 then authors physical proof before any VI-12R production implementation.

Every activated family must state:

- exact proposition(s) and proof obligation(s);
- exact implementation identity/version/boundary under test;
- proof level;
- fixtures/inputs/dependency substitutions;
- positive cases;
- prohibited false-positive cases;
- missing-authority cases;
- lawful optional-absence cases;
- failure signal;
- exact command/environment/versions;
- limitations/adjacent non-claims.

The proof must include the complete BC-014/BC-015 adversarial surface and the 19 accepted obligations. The accepted BICP uses `IA22R01-PROD-009` for the repaired persistence/restart obligation; predecessor `IA17-PROD-009` is lineage only. Real BC-011 durability/restart proof must use the authorised real PostgreSQL path; in-memory/mock/same-process substitutes do not prove those claims.

No product proposition is inserted into the kernel `architecture_kernel` proof registry. Product and architecture aggregates remain separately attributable.

## 9. Reviewer isolation and branch discipline

- VI-06 reviewer receives exact BICP/IRB, VI-04 authority and this IWO only; no physical proof or candidate product implementation.
- VI-11 reviewer receives exact authority and physical proof but no production candidate.
- VI-13R reviewer receives exact authority + accepted proof + final unit candidate/diff/results.
- Failed candidates remain in Git history; repair creates a successor candidate/commit.
- One implementation unit per VI-12R branch, in U01 -> U02 -> U03 -> U04 -> U05 -> U06 order unless fresh evidence proves a different dependency order is required.
- A unit may consume accepted predecessor public/internal contracts but may not reopen predecessor meaning for convenience.

## 10. Allowed mutation jurisdictions

### VI-07/VI-08 architecture admission

Allowed only as derived by VI-07, expected to include:

- `config/architecture/**` exact affected registries;
- `src/nvda_desk/raw_signal_occurrence_truth/__init__.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- minimal A00 composition/package changes required to make the registry truthful;
- architecture proof/config changes required by then-current kernel law;
- accepted implementation-authority binding/lineage records.

No product behavior is smuggled into this architecture leaf.

### VI-09 through VI-11 proof preparation

Allowed:

- separate product-proof registries/manifests/runner/config under a clearly product-proof-owned path;
- physical product test files/fixtures under their admitted proof families;
- proof-environment helpers that do not implement production semantics.

### VI-12R implementation

Allowed:

- `src/nvda_desk/raw_signal_occurrence_truth/**` under the owner boundary;
- bounded `src/nvda_desk/composition/**` changes for A00-owned construction/translation/lifecycle only;
- required package dependency declaration for Psycopg 3.3.4;
- correctness-only SQL/adapter artefacts owned as technical mechanism under the M persistence port;
- unit-specific evidence/lineage records.

Do not mutate standing normative authority or frozen repository guardrails.

## 11. Remaining Unknowns carried through this IWO

The following remain unresolved and must not be selected by implementation convenience:

- concrete provider eligibility/scope/mapping contents;
- provider revision/retransmission equivalence;
- clock accuracy/drift/leap/smear/wake latency;
- finality/watermarks/exact counts/member queries;
- provider duplicate equivalence/exactly-once;
- pre-commit raw loss/bounded recovery;
- availability/latency/throughput/RTO/RPO;
- production opaque-ID generation/collision/cross-process recovery;
- PostgreSQL partitioning;
- PostgreSQL pooling;
- performance/SLA index policy;
- retention/deletion/deterministic recomputation/P01;
- real provider adapters/networking;
- validation/quarantine;
- D001+;
- downstream consumers/behavior;
- historical-M re-establishment detail;
- provider/collector-specific ingestion-sequence scope/overflow;
- final distribution naming/version metadata until VI-15.

## 12. Stop conditions

Stop the dependent unit if any of the following occurs:

- exact IRB/BICP/VI-04 authority identity cannot be rebound;
- current candidate M identity differs in a way that invalidates this work order's architecture/proof projection;
- architecture admission cannot truthfully represent active package/public seam state without product logic leakage;
- proof cannot discriminate one of the accepted semantic distinctions;
- a physical PostgreSQL choice would exceed VI-04's correctness-only delegation;
- a Remaining Unknown above becomes required;
- test/proof requires weakening, replacing or bypassing accepted authority;
- implementation would require P01/K01/replay/external effects/downstream semantics;
- real PostgreSQL proof cannot run with the authorised mechanism;
- independent review reports an unresolved material finding;
- product or architecture aggregate is incomplete/red/skipped without authority.

## 13. Completion boundary

This IWO is complete only when all accepted VI leaves through VI-18 are discharged. It authorises no work beyond the exact Raw Signal Occurrence Truth BICP.

VI-18 PASS is not production commissioning, broader NVDA completion, provider integration or downstream trading capability.
