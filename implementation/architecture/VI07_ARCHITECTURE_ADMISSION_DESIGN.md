# VI-07 — Exact architecture admission design

## Status

**CANDIDATE DERIVED FROM CURRENT AUTHORITY — 2026-09-19.**

This leaf designs the smallest truthful architecture mutation needed before product implementation. It does not yet contain Raw Signal product decision logic.

## Revalidated ingress

The exact implementation-authority binding was re-run against the exact accepted IRB bytes after the Programme Owner execution-routing direction.

Observed current projection:

```text
create:raw_signal_occurrence_truth->M00
modify:A00
```

Current architecture state before mutation:

- active runtime modules: `0`;
- current module registry: empty;
- current module retired IDs: empty;
- durable implementation allocations: empty;
- A00 permitted architecture dependencies: empty;
- declared owner edges: empty.

Therefore the resolver-selected current identity remains `M00`. This result is a current mechanical resolution, not historical identity revival.

## Exact mutation design

### 1. Durable implementation allocation

Append exactly one implementation allocation:

```yaml
- object_id: M00
  name: raw_signal_occurrence_truth
  implemented_on: "2026-09-19"
```

Semantic effect: consume `M00` as the current post-reset implementation identity for the accepted Raw Signal Occurrence Truth owner.

### 2. Active M00 registry entry

Register `M00` as `active` with:

- name: `raw_signal_occurrence_truth`;
- package: `nvda_desk.raw_signal_occurrence_truth`;
- public seam: `nvda_desk.raw_signal_occurrence_truth.api`;
- permitted architecture-owner dependencies: none;
- semantic responsibility: the bounded Raw Signal Occurrence Truth meanings admitted by the accepted BICP/IRB, including semantic persistence/transaction-outcome truth;
- exclusions: P01/DMPV3, K01, replay, provider/network integration, live external effects/accounts, downstream consumers, validation/quarantine, D001+, exact counts/membership/finality/SLA/performance/retention/recovery semantics and other preserved Remaining Unknowns;
- state ownership: capture-scope policy versions, scheduled capture occurrences, raw observation occurrences, receipt-evidence relation meaning, receipt-presence assessment meaning and their semantic persistence state;
- time ownership: configured schedule-slot truth, receipt-time meaning, source-temporal-kind preservation and assessment system-knowledge time; no invented provider event time;
- side effects: owner-authorised persistence through its semantic persistence port only;
- component forms: `contract`, `schema`, `service`, `repository`, `adapter`;
- state writer boundary: M00-owned command/service boundary through the M00 persistence port;
- lawful readers: M00 referential-read facet exposed to A00;
- persistence mechanism: direct Psycopg 3.3.4 PostgreSQL adapter as a non-owning technical mechanism;
- prohibited state writers: A00, PostgreSQL/SQL schema/driver/adapter as semantic owners, P01, K01 and downstream consumers;
- replay obligations: original durable facts remain referentially retrievable by domain identity; no authoritative replay/re-identification capability is activated.

### 3. Package/public-seam skeleton

Create only:

- `src/nvda_desk/raw_signal_occurrence_truth/__init__.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/api.py`.

These files establish truthful package/seam existence only. They must contain no product decision logic in VI-08.

### 4. A00 dependency authority

Modify A00 so `permitted_dependencies` contains exactly `M00` in addition to no other new owner.

### 5. Runtime owner edge

Add exactly one declared owner edge:

```yaml
- source: A00
  target: M00
```

No reverse `M00 -> A00` edge is permitted. No P01/K01/G/S runtime edge is added.

### 6. Surfaces left unchanged

No architecture `S` object is required for this bounded owner admission. `surfaces.yaml` remains unchanged.

### 7. Proof/control state

The existing architecture-kernel blocking proof set remains separate from later product proof. VI-08 must run the existing architecture validation/test/promotion surface against the admitted state. Product proof is introduced separately after architecture admission.

## Allowed VI-08 changed paths

Only the following architecture-admission paths are authorised by this design:

```text
config/architecture/modules.yaml
config/architecture/application_shells.yaml
config/architecture/dependency_rules.yaml
config/architecture/implementation_allocations.yaml
src/nvda_desk/raw_signal_occurrence_truth/__init__.py
src/nvda_desk/raw_signal_occurrence_truth/api.py
implementation/architecture/VI08_ARCHITECTURE_ADMISSION_EVIDENCE.md
```

A change outside this set requires a separately recorded reason tied to an actually failing current invariant.

## Acceptance evidence required for VI-08

- exact implementation-authority ingress still resolves `M00` and `A00` immediately before mutation;
- schema/registry validation passes;
- active package/public seam exists;
- dependency/public-seam analysis reports zero violations;
- A00 may depend on M00 and no reverse/private import exists;
- implementation allocation contains exactly the new M00 consumption;
- existing architecture blocking tests pass on the committed candidate state;
- no product behaviour is present in the package skeleton.
