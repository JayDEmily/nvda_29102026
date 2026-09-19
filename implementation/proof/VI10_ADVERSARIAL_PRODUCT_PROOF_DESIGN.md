# VI-10 — Adversarial Physical Product-Proof Design

## Status

PM design for `G03-L06 / VI-10`. This document authorises physical product proof only. It does not authorise production implementation, product-proof PASS, VI-11 acceptance, or any capability outside the accepted BICP/IWO.

## Exact authority binding

- BICP: `BICP-CANDIDATE-005`, JSON SHA-256 `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`.
- IRB: SHA-256 `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`.
- METHOD-006 baseline: `7c76b1dc87a9773e92841cae47e34b3b50190614` / tree `3cf7d5e78a490611076a6317f3b709b692cdf553`.
- Accepted IWO: `VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001`.
- Current architecture target: `M00`, package `nvda_desk.raw_signal_occurrence_truth`, public seam `nvda_desk.raw_signal_occurrence_truth.api`.
- Product proof obligations: exactly 13 current obligations, including repaired `IA22R01-PROD-009`; predecessor `IA17-PROD-009` is forbidden lineage only.
- Product tier treatment: `NOT_CLASSIFIED`.
- Architecture proof remains the separate `architecture_kernel` axis.

## Pre-authoring read completed by PM

Before this design was fixed, the PM reread current `GUARDRAILS.md`, root `AGENTS.md`, accepted `EXEC_PLAN.md`, the applicable current architecture law, the six BICP-routed METHOD-006 authorities, `tests/AGENTS.override.md`, the complete current admitted architecture/bootstrap proof surface, and the preserved pre-reset testing-method corpus at `d24f962...`.

The preserved corpus was inspected source-wide: 217 Python test/support files and 1,135 test functions, including explicit mutant/falsification, rejection, parametrised, identity/time substitution, absence and restart families. That historical corpus is method evidence only; its tier identities, product meanings and green states are not reactivated.

## Proof design rule

The six families below must jointly cover all 13 current product obligations and the complete BC-014/BC-015 adversarial surface. Each family must include, where applicable:

- lawful positive cases;
- prohibited / false-positive cases;
- missing-mandatory-authority cases;
- lawful optional-absence cases;
- identity/lineage/status extension cases where they bear on the obligation;
- failure signals that are observable at the exact claimed boundary.

A test must not pass merely because implementation is absent. Missing required implementation must fail explicitly. Blocking tests must not skip because a dependency, PostgreSQL DSN, symbol or production path is missing.

## Test-facing implementation-shape choices

The accepted IWO leaves concrete Python implementation shape free while allowing later accepted proof to fix additional test-facing construction symbols where necessary. VI-10 therefore fixes the following minimal proof-facing shape so physical tests can be written before production code:

1. The five exact `.v1` payload contracts are Python-visible through `nvda_desk.raw_signal_occurrence_truth.api` as:
   - `CaptureScopePolicyV1`
   - `ScheduledCaptureOccurrenceV1`
   - `RawObservationOccurrenceV1`
   - `CaptureReceiptEvidenceRelationV1`
   - `CaptureReceiptPresenceAssessmentV1`
2. The proof harness obtains a subject only through private construction symbol `api._build_test_owner(...)`. This symbol is test-facing construction glue, not semantic authority; VI-13 must reject an implementation that hides domain logic in this factory instead of the owner.
3. The returned subject exposes separate `commands` and `reads` facets. The command facet operations used by proof are:
   - `register_capture_scope_policy`
   - `realise_scheduled_capture_occurrence`
   - `admit_raw_observation_occurrence`
   - `derive_capture_receipt_evidence_relation`
   - `append_capture_receipt_presence_assessment`
   - `reconcile_owed_slots`
4. The read facet operations used by proof are:
   - `get_capture_scope_policy`
   - `get_scheduled_capture_occurrence`
   - `get_raw_observation_occurrence`
   - `get_receipt_presence_assessment`
   - `list_receipt_presence_assessments`
5. U06 may use one A00-private proof construction symbol `nvda_desk.composition._build_test_application(...)` solely to construct the real A00 -> M00 composition path. It must not implement Raw Signal semantics.

These names are concrete proof-harness choices needed to exercise the public boundary. They do not broaden the accepted meaning, activate a downstream consumer, or authorise a second semantic owner.

## Family map

### PPF-RSOT-U01 — Typed contracts, owner boundary and compatibility

Path: `tests/product/raw_signal/test_u01_contract_owner_boundary.py`

Obligations: `IA17-PROD-001`, `IA17-PROD-011`, `IA17-PROD-012`.

Must prove at least:

- exact five v1 contract identities and separately represented concept/schema/domain identities;
- command/read facet separation and M00 ownership while A00/storage/adapters/tests remain non-owning;
- no P01/DMPV3/K01/downstream-consumer activation;
- structural headers reject untyped null/extra semantic authority;
- compatible optional addition cannot change existing v1 interpretation;
- breaking requiredness/discriminant/time/null/identity/provenance change is not silently accepted as v1;
- missing named consumer/boundary authority cannot be fabricated;
- lawful absence of downstream consumer/carrier remains lawful.

### PPF-RSOT-U02 — Capture policy and owed-slot truth

Path: `tests/product/raw_signal/test_u02_capture_schedule.py`

Obligations: `IA17-PROD-002`, scheduling/identity portion of `IA17-PROD-008`.

Must prove at least:

- exact `:00` and `:30` 30-second `[start,end)` slots;
- no slot before activation or at/after deactivation;
- absent deactivation does not imply perpetual-service meaning;
- scheduler wake/receipt/provider-event time cannot become schedule truth;
- stable `(scope_policy_ref, slot_start_utc)` retry reference yields one capture occurrence while opaque occurrence identity remains distinct;
- same occurrence ID with conflicting content fails closed;
- missing/contradictory policy/version/activation authority fails closed.

### PPF-RSOT-U03 — Raw observation, native fidelity and temporal-kind law

Path: `tests/product/raw_signal/test_u03_observation_native_temporal.py`

Obligations: `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005`, observation/identity portion of `IA17-PROD-008`.

Must prove at least:

- one separable provider record -> one observation; two separable records in one delivery -> two observations sharing delivery ref;
- no coalescing separate records and no repository-created field splitting;
- no-scope observation remains valid and unrelated to capture;
- native field names/values/provider-calculated values and applicable units/provenance round-trip unchanged;
- exact `true_instant`, `date_only`, `receipt_only` distinctions;
- date is never converted to midnight UTC; receipt time never fills missing provider time/timezone; raw `event_ts_utc` is absent;
- optional metadata stays absent when not applicable; provider-supplied null inside native record remains native data;
- microsecond receipt time and genuine optional `received_epoch_ns` remain distinct;
- same-occurrence retry is idempotent only for identical content; newly received retransmission gets a new observation identity even when native identifiers/values match;
- identity substitution across provider/delivery/observation/schema/concept layers fails closed.

### PPF-RSOT-U04 — Receipt evidence and append-only assessment state

Path: `tests/product/raw_signal/test_u04_receipt_assessment.py`

Obligations: `IA17-PROD-006`, `IA17-PROD-007`, state/identity portion of `IA17-PROD-008`.

Must prove at least:

- relation exists only under separately established eligibility, active policy and receipt time inside `[start,end)`;
- relation role is exactly `evidences_receipt_presence_only`;
- relation cannot imply contains/member/count/validity/completeness/finality/ownership;
- lawful no-relation state for no-scope observation;
- all three assessment outcomes are represented exactly;
- first assessment may omit supersession; later assessment names immediate predecessor only;
- later eligible evidence appends `one_or_more_received` superseding zero without overwriting zero;
- unknown is not zero; zero is not outage/finality/provider-event absence; one-or-more is not an exact count;
- broken/cyclic/non-immediate supersession or same-ID conflicting assessment fails closed.

### PPF-RSOT-U05 — Real PostgreSQL durability, failure, restart and referential readback

Path: `tests/product/raw_signal/test_u05_postgresql_durability.py`

Obligations: `IA22R01-PROD-009`, `IA17-PROD-010`, persistence-bearing portions of `IA17-PROD-007` and `IA17-PROD-008`.

Environment is mandatory real PostgreSQL 17.9 with Psycopg 3.3.4. `NVDA_TEST_POSTGRES_DSN` must identify the real server. Missing DSN, wrong driver version, non-PostgreSQL backend or wrong proof server version is a proof failure, not a skip.

Must prove at least:

- independent connection verifies PostgreSQL 17.9 proof environment;
- durable-success signal occurs only after own transaction commit;
- fresh owner/process-equivalent construction over same DSN reads committed original policy/capture/observation/assessment facts by domain identity with lineage/schedule context;
- identical-content retry is idempotent against durable state and conflicting same-ID reuse fails closed;
- assessment persistence is append-only;
- failed transaction/write produces no semantic empty/unknown/zero fallback and no durable fact;
- restart reconciliation of explicitly requested owed slots uses durable schedule/capture state;
- missing owed slot after restart creates durable capture plus initial `unknown_not_established`, never inferred `zero_received`;
- no same-process memory is accepted as durability evidence;
- no cross-kind atomicity, replay equivalence, retention, bounded recovery, RTO/RPO or SLA claim is made.

### PPF-RSOT-U06 — A00 -> M00 governed sequential composition

Path: `tests/product/raw_signal/test_u06_a00_composition.py`

Obligation: `IA17-PROD-013` with supporting public-governance coverage from `IA17-PROD-011`.

Must prove at least:

- real A00 composition constructs/injects technical inputs and M00 owner;
- A00 calls only M00 typed command/read facets;
- runtime direction is A00 -> M00 and never M00 -> A00;
- A00 does not decide Raw Signal outcomes;
- no private-state/table/repository bypass;
- no P01/K01/downstream consumer appears;
- one sequential path exercises admitted policy -> slot -> observation -> relation/assessment -> referential read without expanding meaning;
- missing lawful M00 allocation/seam/dependency/proof authority cannot be silently bypassed.

## Registry and aggregate changes

VI-10 must update only the separate product-proof control:

- admit exactly the six families above in `config/product_proof/families.yaml`;
- set `config/product_proof/aggregates.yaml` to `READY_FOR_PROOF` only when those six families cover exactly all 13 current product obligations;
- preserve `tier_treatment: NOT_CLASSIFIED` for every product family;
- do not mutate `config/proof/**` or the `architecture_kernel` aggregate.

## Expected pre-implementation disposition

After VI-10 authoring:

- `python tools/validate_product_proof.py` must PASS structurally;
- the six physical product tests must exist and be admitted exactly;
- the product aggregate runner must execute those exact paths and be RED before implementation for attributable missing product implementation / required proof environment, not because the proof registry is incomplete;
- architecture validation/aggregate, mypy and Ruff must remain green;
- no `src/nvda_desk/raw_signal_occurrence_truth/**` production behaviour may be added.

A red pre-implementation product aggregate is expected evidence, not VI-10 failure, provided the failures are attributable to absent production implementation or deliberately absent mandatory real proof environment and not to malformed tests/control.

## Stop conditions

Stop if:

- any test requires meaning not present in the exact authority;
- a Remaining Unknown must be defaulted to make a test concrete;
- a mock/in-memory backend would be used to stand in for required PostgreSQL durability/restart proof;
- production code would have to be written to make the proof authorable;
- a family cannot discriminate a listed prohibited false positive from the lawful case;
- product proof would need Tier A/B/C classification or architecture-registry contamination;
- a test would silently skip a mandatory boundary;
- any architecture or current control regression appears.
