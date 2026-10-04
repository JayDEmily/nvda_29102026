# Requirements

## REQ-001 — Exact accepted authority binding

**Statement:** All project work shall remain bound to the accepted brief repository at source commit `23968fdfcc489cdc2ea14aa9dd1e1aea3b3d72ce` / tree `81ff4871ddb14f8c5feec2bf1a543ce290fba0be`, as recorded by `.pcm/control/instantiation.json`, with the brief Markdown, SHA-256-bound companion CSV, and reference workbook interpreted exactly as the accepted brief defines their authority roles. The normative CSV digest is `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5`; a mismatch is fail-closed.

## REQ-002 — Bounded semantic ownership and architecture admission

**Statement:** Establish exactly one runtime semantic owner for Derived Signal Calculation Truth through the repository's normal implementation-authority ingress and architecture-admission process. A create projection shall identify category/responsibility only; the numeric architecture identifier must be resolved mechanically from current post-reset allocation state and must not be selected by the PM, brief or implementation convenience. Existing M00 meaning remains owned by M00.

## REQ-003 — M00 public projection and isolation

**Statement:** Extend M00 only by the brief-authorised additive read-only typed raw-value/history projection. Every projected value must bind the requested `Rxxx` to one exact native field through an immutable `RawSignalProjectionMapping`, preserve native value/units, source occurrence identity, temporal/receipt ordering and relevant subject/revision metadata, support stable bounded enumeration, and never aggregate or calculate `Dxxx`. The calculation owner must not directly read or write M00-owned PostgreSQL relations and must not implement provider-specific parsing as fallback behaviour.

## REQ-004 — Explicit versioned calculation inputs and selection law

**Statement:** All non-signal inputs required by the brief, including parameter profiles, mappings, unit conventions, input-selection policy and the admitted typed contexts, must be immutable/versioned and retained in lineage. Subject/contract/universe/time matching, knowledge cutoff, history sufficiency, synchronous-skew limits and unit conversion must be explicit; magnitude heuristics, look-ahead, fabricated timestamps, hidden defaults and silent nearest-neighbour/interpolation behaviour are prohibited unless the accepted kernel explicitly authorises them.

## REQ-005 — Durable derived occurrence truth and persistence boundary

**Statement:** Persist typed derived occurrences with canonical `Dxxx`, opaque occurrence identity, calculation-definition and context/parameter versions, subject/universe, time/window/cutoff, typed result/units/shape, exact raw projection lineage, predecessor-D lineage and applicable convention/supersession metadata. Persistence must use a calculation-owner schema and write role separate from M00's writer with no calculation-owner database privilege over M00-owned tables; PostgreSQL remains a mechanism rather than semantic owner.

## REQ-006 — Catalogue, kernel and mathematical fidelity

**Statement:** Realise exactly the 209 authoritative catalogue rows `D001`–`D209`, each bound to exactly one catalogue kernel, dependency set, parameter profile and typed-context conjunction. Implement the mathematics and row-specific clarifications of accepted brief clauses 3–8 and kernels `K01_TIME` through `K17_ORDER_FLOW_IMBALANCE` without implementation-selected estimator, sign, scaling, annualisation, extraction, tie-break or result-interpretation changes.

## REQ-007 — Version-consistent acyclic dependency evaluation

**Statement:** Derived dependencies shall be evaluated only through the accepted acyclic D graph in topological order. Reuse of stored predecessors requires exact compatible lineage/version/context/time state; incompatible or absent predecessors yield no requesting occurrence. Runtime recursion may not add, remove or bypass dependency edges. Deterministic retries shall be idempotent and material changes shall create append-only successor occurrences rather than rewrite historical derived truth.

## REQ-008 — Typed public seam and external-effect exclusion

**Statement:** Expose one typed calculation/read seam that can materialise a named `Dxxx` for exact versions/context/time, retrieve by occurrence ID, retrieve bounded history, expose exact lineage/versions and distinguish absence from persisted values. Calculated action-like values remain facts only; this project must not perform or authorise orders, cancellations, account mutation, provider/network effects or other external actions.

## REQ-009 — Proof and independent review

**Statement:** Before implementation acceptance, establish all 27 proof classes required by accepted brief clause 18, including catalogue/dependency integrity, raw-field projection ambiguity refusal, unit adversaries, subject/time refusal, representative direct/history/derived/regression/surface/score/evaluation calculations, no-look-ahead, deterministic/idempotent/append-only behaviour, M00 seam isolation, L2/candidate/live-position/attribution semantics, PostgreSQL schema/role isolation, structured result persistence, external-effect exclusion and normal architecture admission. Whole-system acceptance requires independent review of the exact candidate and current evidence.

## REQ-010 — Test-first production change discipline

**Statement:** Any task changing executable production behaviour must depend on an accepted governing test/proof task under PCM `test_first_policy=required`. Production work may not begin by collapsing test/proof and implementation responsibility or by weakening tests to obtain green.

## REQ-011 — Package identity and terminal freeze

**Statement:** Package/distribution name and version remain unresolved by the accepted brief and require an explicit later Programme Owner decision before final package metadata is represented as authoritative. Final closure must bind exact Git/package/proof/review identities, preserve a clean append-only lineage and durable recovery artefact, and make no claim beyond Derived Signal Calculation Truth.

## REQ-012 — Fail-closed unknowns and authority changes

**Statement:** Any missing required mapping, context, parameter, history, authority, architecture capability or evidence that is necessary to continue must remain `UNKNOWN` or `BLOCKED`; it may not become a default. Any change to accepted calculation semantics, ownership, dependency meaning, write scope, actor class, review law or external-effect boundary requires Programme Owner governance rather than autonomous repair.
