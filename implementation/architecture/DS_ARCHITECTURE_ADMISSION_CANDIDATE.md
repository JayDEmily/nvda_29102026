# Derived Signal Calculation Truth — DS-A03 architecture admission candidate

## Status

**CANDIDATE FOR DS-A04 INDEPENDENT REVIEW.**

This record describes the durable architecture mutation and bounded work-order authority prepared by DS-A03. It is not DS-A04 review acceptance, production implementation, executable M01 activation, final package/distribution authority, or authority to change accepted calculation semantics.

## Accepted predecessor authority

The admission proceeds from the exact DS-A01 candidate bytes independently reviewed in DS-A02. The admitted DS-A02 result records:

- review packet SHA-256 `11685c4c6dd0f59f67fc9cf336980cd0c6f71d58af8587f97f86b4bd930e6098`;
- result SHA-256 `aaed1aa84021df158670da17c5bd6f7c390e5a277eb7a519abe67b383ff4c8c2`;
- reviewer actor instance `73bd570bd89988b33c0bcecb2b5a1fa7`;
- verdict/route `pass` / `PASS`;
- reviewed BICP candidate SHA-256 `e3a0be75da103d69d29ab3dee97429d343033b6c29e72c039e77e799e4869634`;
- reviewed ingress-evidence SHA-256 `10437c475d54322e4edb802a81b01b65ecd7b36acf67b6b62221adadbfb7d6db`.

That review accepted one bounded category-`M` Derived Signal Calculation Truth owner, a `create` projection without a caller-selected numeric identifier, `modify:M00`, and dependency direction from the new owner to M00 through M00's public seam. It did not itself mutate durable architecture state.

## Mechanical numeric allocation

Immediately before DS-A03 architecture mutation, the native implementation-authority validator resolved the existing create intent mechanically as:

```text
create:derived_signal_calculation_truth->M01, modify:M00
```

At that point M00 was the only consumed post-reset `M` identity and `M01` was neither registered nor retired nor durably allocated. DS-A03 therefore durably consumes `M01` for `derived_signal_calculation_truth` in `config/architecture/implementation_allocations.yaml` and registers that exact identity in `config/architecture/modules.yaml`.

After this durable allocation, a fresh generic create rehearsal correctly advances to `M02`; that later resolver result is evidence that M01 has been consumed, not a reinterpretation of the admitted M01 identity.

## Durable architecture projection

### M01 semantic owner and lifecycle

`M01` is registered as `derived_signal_calculation_truth` with status `bootstrap`.

The registry records the accepted bounded responsibility: deterministically calculate and durably preserve canonical `D001`–`D209` Derived Signal occurrences from lawfully projected M00 Raw Signal facts, compatible predecessor Derived Signal facts and exact immutable calculation/configuration/context versions, with complete lineage.

`bootstrap` is deliberate. DS-A03 is authorised to admit architecture state and a work order, not to create production source. M01 therefore remains non-composable until later governed implementation/proof establishes an executable owner and lawfully changes lifecycle state.

### Dependency direction and public boundaries

The declared runtime owner edge is exactly:

```text
M01 -> M00
```

M01's only permitted architecture-owner dependency is M00. No reverse `M00 -> M01` edge is added and A00 is not made dependent on M01 by this task.

The future M01 Python owner/public-boundary declarations are:

```text
package:     nvda_desk.derived_signal_calculation_truth
public seam: nvda_desk.derived_signal_calculation_truth.api
```

These declarations identify the one future cross-owner import boundary required by architecture law. No source package is created and no executable capability is claimed by DS-A03.

### M00 modification boundary

M00 retains Raw Signal semantic ownership and its existing writer boundary. Its architecture record gains only the accepted additive read-only typed raw-value/history reader boundary for M01. The boundary must preserve exact `Rxxx` field mapping/version, native value/units, source occurrence identity, temporal/receipt ordering and relevant subject/revision metadata and must perform no `Dxxx` calculation, aggregation, interpolation or semantic rescaling.

### M01 persistence boundary

M01 owns Derived Signal occurrence/lineage persistence only. Its writer boundary is a calculation-owner PostgreSQL schema/write role separate from M00, with no M01 database-role privilege over M00-owned relations. Shared PostgreSQL deployment remains permitted as a mechanism without transferring semantic ownership.

### External-effect exclusion

M01 has no order/account/provider/network effect authority. Action-like Derived Signal values remain persisted facts only. No downstream authority to act on them is admitted.

## Bounded implementation work order

`implementation/work_order/DS_IMPLEMENTATION_WORK_ORDER.md` records the downstream boundary. It follows the already-finalised PCM task graph: foundation proof `DS-T01` precedes foundation implementation `DS-I01`; subsequent proof/implementation groups remain separately gated; independent-review leaves remain independent.

The work order does not authorise immediate coding from DS-A03 and does not convert unresolved implementation choices into defaults.

## Deliberately unresolved/deferred matters

DS-A03 does not select final distribution name/version, concrete PostgreSQL schema/role names, physical database layout, occurrence-ID algorithm, provider/native-field mappings, production parameter/context instances, performance/SLA/RTO/RPO targets or downstream action authority.

The internal Python package/public-seam spelling above is resolved only as the architecture boundary required by this admission. Final distribution identity/version remains deferred to `DS-PO01` exactly as the finalised project plan requires.

## Proof/review boundary

Architecture/bootstrap proof fixtures that encoded the historical one-module/one-allocation state are updated only where the lawful M01 admission made those expectations stale. No test is removed, skipped, de-admitted or weakened.

`implementation/architecture/DS_ARCHITECTURE_ADMISSION_EVIDENCE.md` records the exact baseline, mutation and observed validation results.

DS-A04 must independently challenge identifier allocation, bounded ownership, dependency direction, public-seam/source trace and absence of unapproved architecture expansion before this admission is relied upon as independently reviewed architecture state.
