# M01–M03 Semantic Continuity Repair ExecPlan

**Status:** `ACCEPTED:M01_M02_M03_SEMANTIC_CONTINUITY`
**Created:** 2026-08-03
**Owner:** User-authorised worker
**Canonical parent:** `project_control/canonical_project_manager/CONTINUATION.md` section 11
**Baseline commit:** `fb8793f97cfb820584ec567aa2f4ec2073a59815`
**Worker branch:** `work/m01-m03-semantic-continuity-repair-v1`
**Control-pack ID:** `M01-M03-SEMANTIC-CONTINUITY-REPAIR-V1`
**Live pointer:** `ROADMAP_LEDGER_V2.md`

## 1. Trigger and authority

The guidance-deviation audit proved that M03 could issue a valid prepared identity
for a caller-supplied value that contradicted the admitted M01 source value. The
user authorised repair of M01, M02 and M03 and requested a downloadable
checkpoint. Existing guidance already requires exact source-to-prepared
continuity; this plan implements that law without changing its meaning.

## 2. Objective

Make the canonical M01 → M02 → M03 chain evidentiary, not merely internally
self-consistent:

1. M01 family contracts declare exact payload-field-to-semantic-field bindings,
   including value type, unit and requirement, and admitted owner products carry
   those bindings unchanged.
2. M02 selected fields preserve their exact value type and unit from the selected
   candidates.
3. M03 consumes exact M01 source artefacts and M02 projections, constructs its
   own lineage references and candidate records, resolves direct fields under
   explicit M03 policies, executes admitted deterministic derivations, and
   constructs the prepared payload itself.
4. M00 delegates exact owner products and does not inspect payload meaning,
   invent semantic fields, or author M03 payload values.

## 3. In scope

- M01 source-family semantic binding contracts, validation and emitted products.
- M02 selected-field type/unit preservation and projection fingerprint effects.
- M03 strict owner-evidence preparation builder, derivation rules and public API.
- M00 upstream `PreparationSpec` and delegation required to select the repaired
  canonical seam.
- Existing affected tests and support fixtures, with proposition-preservation
  records for every changed assertion-bearing node.
- Admission/proof/vocabulary/control reconciliation and full-history checkpoint.

## 4. Out of scope

- M03 → M05 serial cognition continuity, which remains a separately verified
  defect from the audit.
- M04–M15 owner behaviour except compatibility adaptation required to consume a
  lawful M03 envelope.
- Live data, network, broker, durable operation or profitability claims.
- Broad refactoring, compatibility aliasing, test retirement, skips or xfails.

## 5. Acceptance units

### Unit 0 — Register and align
Pass when branch/baseline are exact, full-read manifest exists, this pack is the
single live slice, and readiness is explicitly suspended by the new evidence.

### Unit 1 — C-NORM
Pass when `C_NORM.md` defines exact M01 bindings, M02 typed selected facts, M03
owner-evidence resolution/derivation, M00 delegation and fail-closed conditions.

### Unit 2 — C-PROOF expected red
Pass when existing propositions remain binding and new public-seam tests prove:
- M01 emits exact semantic bindings;
- M02 preserves selected value type/unit;
- M03 rejects `190 → 999` substitution before envelope issuance;
- M03 rejects fabricated or mismatched owner evidence;
- M00 cannot supply or reinterpret a prepared payload.
The tests must fail only at the missing production boundary.

### Unit 3 — M01 and M02 owner implementation
Pass when exact owner products satisfy their focused tests and no downstream
module is used to infer missing source meaning.

### Unit 4 — M03 and M00 composition implementation
Pass when M03 constructs the payload and receipts from exact owner products,
M00 delegates without semantic inspection, and the adversarial substitutions
fail closed before prepared identity issuance.

### Unit 5 — Acceptance and checkpoint
Pass on one clean commit when affected cones, physical Tier A/B/C, proof
controls, vocabulary, formatting/lint/compile, signed promotion and Git checks
pass; controls accurately state the remaining M03→M05 defect; and a verified
full-history archive is published.

## 6. Prohibited shortcuts

No retired, re-authored, weakened, skipped, xfailed, broadened or redirected
failing test merely to make the repair green. Every changed test must preserve
its original proposition and record old node, authority, replacement assertion
and red-to-green evidence. No caller-authored semantic payload, fabricated
lineage reference, permissive mapping fallback, compatibility second owner or
receipt accepted without exact owner-evidence reconciliation.

## 7. Progress

- 2026-08-03: user authorised the bounded M01–M03 repair after the novel audit.
- 2026-08-03: branch created from exact continuation-ready checkpoint.
- 2026-08-03: Unit 0 registered the bounded pack and suspended readiness in the live roadmap.
- 2026-08-03: Unit 1 C-NORM aligned exact M01 bindings, M02 selected type/unit, M03 owner-evidence construction and M00 delegation.
- 2026-08-03: Unit 2/3 owner proof began expected-red at three exact missing surfaces and is now green: 56 focused M01/M02 tests pass; existing propositions were preserved through fixture-only binding additions.
- 2026-08-03: Unit 4 began with four exact expected-red failures at the caller-authored payload/owner-evidence seam. M03 now constructs direct and derived values from exact M01/M02 products; M00 carries only policies/rules. Five new adversarial continuity nodes and every original M03/M00/Tier C proposition pass in a 147-test affected cone.
- 2026-08-03: Proposition-preservation audit records 32 new/changed nodes or helpers, with zero deleted test nodes and zero skip/xfail mechanisms.
- 2026-08-03: Unit 5 acceptance is green: physical Tier A 1,999/1,999; Tier B 93/93; Tier C 5/5; proof authority 201 families, 203 paths and 73 blocks; 13/13 vocabulary namespaces clean. M01/M02→M03 continuity is accepted. M03→M05 remains open and continuation readiness remains suspended.
