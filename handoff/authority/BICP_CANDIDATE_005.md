# BICP Candidate 005 — Raw Signal Occurrence Truth

Status: **CANDIDATE**. This packet is not an implementation-status claim and authorises no code, work order, physical tests or durable architecture allocation.

## Exact task authority

- IRB: `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342` (20,559 bytes).
- Upstream semantic acceptance: M10 V004 `1b54afea782a5ddfb03463e23995e6eb83f76f5fb34939304f7c078a9dda34d6`, exact W006 handoff `8f74441102855ddbef814ec63609117dabf1441c76ef8ba951c3916c0ac1efa5`, independent T006 `APPROVE`/zero findings `d65cda7cf7bbdb4ee7e22b20f4feb85a126ca2faa6463525c0e0f8f3f9f3ea78`.
- Current implementation-admission authority: `IA-AUTH-001`.
- Current METHOD-006 standing baseline: `7c76b1dc87a9773e92841cae47e34b3b50190614` / tree `3cf7d5e78a490611076a6317f3b709b692cdf553`.
- Current BUILD-001 checkpoint: `17263909abae9ca8cabb2440db282d12ff492ad6` / tree `26c421f7cbc75d61ea3e538d79091f4e01136585`.

## Bounded normative context

Primary route: `R-N04`. Triggered cross-cutting routes only: `R-VG`, `R-N06`, `R-N18`, `R-N15`, `R-N19`. Prepared-data, calendar-runtime ownership, packet/DMPV3, modifiers, authoritative replay, live external effects and external accounts remain inactive. Semantic persistence is required, but physical persistence realisation remains unresolved.

## One bounded implementation unit

**Responsibility:** Raw Signal Occurrence Truth.

- semantic owner create target: `IA11-TARGET-001`, current non-durable candidate `M00`;
- supporting existing shell target: `IA11-TARGET-002`, `A00`;
- runtime direction: `A00 -> M00`;
- public boundary: M00 owns/provides both typed command and referential-read facets; A00 is the sole authorised consumer/caller; command inputs flow A00 -> M00 without changing seam ownership;
- M00 owns semantic state/time/persistence meaning; A00 owns construction/translation/top-level lifecycle only;
- M00 owns its semantic persistence port; A00 may construct/inject a non-owning PostgreSQL adapter;
- P01/DMPV3 inactive; K01 not selected; no downstream business consumer admitted.

## Proof surface

The packet carries 19 proof obligations only: 13 product obligations and 6 architecture obligations. Each exact BC-015 named proposition `M16-RSOT-001`…`012` is represented as a task-specific `IRB_PROPOSITION` authority with its exact BC-015 locator and is bound directly to its corresponding product proof obligation in machine lineage. The persistence/failure successor obligation `IA22R01-PROD-009` explicitly requires the BC-011/BC-015 restart case: reconcile durable captures after restart and create a missing owed slot as `unknown_not_established`, never inferred zero. Product Tier A/B/C remains `NOT_CLASSIFIED`; architecture Tier A treatment applies only where a later implementation/allocation claim activates the corresponding current kernel proposition.

## Implementation freedom boundary

Private module/class/function/helper naming and internal decomposition inside M00, internal algorithms that preserve identical observable semantics, optional materialisation of the BC-007 receipt relation, private exception plumbing and non-semantic A00 wiring details remain implementation choices within their stated authority boundaries.

**Final package naming/version metadata is not implementation freedom.** It remains an explicit `BC-016` Remaining Unknown. If implementation requires that package name or version metadata, the later worker must stop at the exact repository-defined blocker and seek authority rather than choosing a default.

The same stop rule continues to apply to every other BC-016 Remaining Unknown, including physical PostgreSQL layout/types/indexes/partitions/pooling/driver.

## Explicit exclusions

This candidate contains no Implementation Work Order, physical product test, product code, durable registry allocation, P01/DMPV3 activation, K01 selection, authoritative replay, external-effect/account authority, or downstream business semantics.

## Machine packet

The complete exact authority catalogue, route receipt, architecture projection, successor proof obligations, corrected implementation-freedom classification and exact-class lineage graph are in `BICP_CANDIDATE_005.json`. Exact packet byte identities are externalised in `BICP_CANDIDATE_005.sha256`.

Candidates 001 through 004 and their review/repair evidence remain preserved unchanged. Candidate 005 repairs only accepted finding `IA23R04-F001`: `IF-FREE-001` no longer classifies package naming as implementation-free, and `IF-SRC-012` explicitly preserves final package naming/version metadata as a BC-016 stop-and-seek-authority Remaining Unknown. All Candidate 004 architecture, route, proof and other implementation-freedom meaning is preserved.
