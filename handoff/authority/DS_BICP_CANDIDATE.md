# Derived Signal Calculation Truth — BICP candidate

Status: **CANDIDATE FOR DS-A02 INDEPENDENT REVIEW**. This packet is not architecture admission, implementation acceptance, a work order, a numeric object allocation, package authority, or authority to change production code.

## Exact accepted authority

- PCM accepted-brief archive: `8ea9bf69f6a651f19e84bd1401cb9f4e8c10f8e62603a3ff407f4418936e1731`.
- Accepted source commit/tree: `23968fdfcc489cdc2ea14aa9dd1e1aea3b3d72ce` / `81ff4871ddb14f8c5feec2bf1a543ce290fba0be`.
- Ingress brief byte object: `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, SHA-256 `603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c`.
- Normative companion catalogue: `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5`.
- Reference-only workbook: `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.
- External acceptance reference recorded by the ingress binding: `PCM-INSTANTIATION-APPROVAL@09c1ac507f6ac0d9931c286e5b66680f1045af31`. It resolves to the Programme Owner approval in `.pcm/control/instantiation.json` introduced by that commit and carried by the current accepted lineage.

The archive is the PCM accepted-brief package identity. The native Implementation Authority Ingress binds the exact Markdown member because the accepted brief itself defines that Markdown as the single ingress byte object and incorporates the CSV normatively by its exact digest.

## One bounded semantic responsibility

Create one runtime semantic owner for **Derived Signal Calculation Truth**: given lawfully exposed M00 Raw Signal facts, compatible predecessor Derived Signal facts, and exact immutable calculation/configuration/context versions, deterministically calculate and durably preserve canonical `D001`–`D209` occurrences with complete lineage under the accepted brief and catalogue.

This owner calculates facts only. It does not own provider ingestion, Raw Signal truth, M00 persistence, provider-specific extraction fallback, order/account mutation, provider/network effects, or downstream authority to act on calculated values.

## Minimal architecture projection intent

The exact projection intent is:

1. **create** category `M`, responsibility name `derived_signal_calculation_truth`;
2. **modify** existing `M00` only to add the brief-authorised read-only typed raw-value/history projection for this consumer.

No numeric identifier is present for the create target. Numeric candidate resolution remains a mechanical, non-durable architecture-kernel result until a later authorised architecture-admission task performs durable allocation.

The intended runtime dependency direction is from the new Derived Signal semantic owner to M00's declared public seam. M00 does not gain a dependency on the new owner. The M00 modification preserves M00 Raw Signal ownership: it exposes exact raw facts plus mapping/lineage metadata and performs no `Dxxx` calculation, aggregation, interpolation or semantic rescaling.

## Persistence and public-boundary constraints carried from accepted authority

- The Derived Signal owner must not directly read or write M00-owned PostgreSQL relations.
- The Derived Signal owner requires a separate PostgreSQL schema/write-role boundary from M00's writer; one PostgreSQL deployment remains permitted.
- M00's additive projection must refuse absent or ambiguous field mappings and retain source occurrence, mapping, native unit/value, temporal/receipt ordering and relevant subject/revision metadata.
- Cross-owner use is through declared typed public seams only; direct private-owner access is not admitted.
- Derived dependency evaluation remains the accepted version-consistent acyclic graph; missing required history/context/version/unit/temporal prerequisites produce no canonical occurrence.

## Proof and later-admission boundary

The 27 proof classes in accepted brief clause 18 remain required before implementation acceptance. This packet does not satisfy those proofs. It only prepares the exact authority binding and bounded projection intent required before architecture admission.

A later architecture-admission task must mechanically resolve and durably admit the numeric create identity, M00 extension boundary, owner dependency/public-seam declarations and work-order authority. This packet does not perform those mutations.

## Deliberately unresolved matters

The following remain unresolved exactly as required by the accepted brief and project authority: numeric architecture identifier; package/distribution name and version; Python public API spelling; PostgreSQL schema/role names and physical layout; calculation mechanism placement; occurrence-ID algorithm; concrete provider/native-field mappings; concrete production parameter/context instances; performance/SLA/RTO/RPO targets; and downstream action authority.

No unresolved item is converted into an implementation default by this candidate.

## Exact ingress binding artefact

The schema-valid native binding is `implementation/authority/DS_IMPLEMENTATION_AUTHORITY_BINDING.yaml`, SHA-256 `ae365e6ac6635ba9de2dc76136f47c18fc4f501c2f158ec4db9bf407ccde799e`. Its create target contains category and responsibility name only; its only numeric target is the existing-object modification `M00`.

Mechanical ingress evidence is recorded in `implementation/authority/DS_INGRESS_EVIDENCE.md`.
