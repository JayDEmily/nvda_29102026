# NVDA Raw Signal Clean Rebuild — Authority Manifest

This repository separates **Raw Signal source normative authority**, **accepted architecture authority**, **historical lineage**, and **derived module authority**. Raw Signal module documents must remain semantically subordinate to the Raw Signal source authorities and structurally subordinate to the accepted architecture authorities below.

## Raw Signal source normative authority

| Artefact | Role | SHA-256 |
|---|---|---|
| `authority/source/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx` | Authorised signal/data workbook; complete workbook is source authority. | `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae` |
| `authority/source/NVDA_CROSS_MODULE_DATA_IDENTITY_GUIDANCE_20260804.tar.gz` | Preserved supplied cross-module identity archive. | `bac8f4271c34cc945bdc6b4a51d6a6eea9c60b35f273de158d3726c1cc530ebc` |
| `authority/source/NVDA_CROSS_MODULE_DATA_IDENTITY_AND_DMPV3_GOVERNANCE_20260804.md` | Cross-module data identity, ownership and DMPV3 governance authority. | `ec9b64534ad8d28a76375874c9097e5f61fe2699da4e1bc0a622aa84e5d268fb` |

## Current direct user authority

The following decisions are current direct user authority for Raw Signal and are not inferred from the source workbook:

- **Persistence technology:** Raw Signal persistence must use PostgreSQL as the backing-store technology. Physical schema, indexing, partitioning, connection pooling, and transaction design remain engineering decisions unless separately authorised.
- **Scheduled capture-set cadence:** the live system must maintain a distinct scheduled 30-second capture-set clock. Every scheduled slot must be durably representable, including a slot in which zero live observations are received. Absence must be represented explicitly; do not fabricate raw observations or an event timestamp. This system cadence is distinct from provider-native cadence.

## Accepted architecture authority

| Artefact | Role | SHA-256 |
|---|---|---|
| `docs/architecture/ARCHITECTURE_KERNEL.md` | Architecture-kernel authority. | `4801a631b6ff4632dfb170209103aa251fcac94f553c93dff7bf319ebb174431` |
| `docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md` | Architecture-kernel authority. | `285b25bc847b8bb5b35322becace2665968fc5a280cefc40be818c0209d8bd6f` |
| `docs/architecture/DEPENDENCY_LAWS.md` | Architecture-kernel authority. | `a7253fc48132af4b90b79ef50dde125f782053ebe7aebb1e94265a99559f1add` |
| `docs/architecture/PUBLIC_SEAM_LAW.md` | Architecture-kernel authority. | `09b1f286b24803011819d010d51643a89a7b92bc9c439bb496078489d2443e2b` |
| `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` | Architecture-kernel authority. | `2ce24aa5cdfc4a1fd41110e229c137f1cdacdf18cbc59b3a0e7a861207cdbf4f` |
| `docs/architecture/EXTENSION_AND_RETIREMENT_RULES.md` | Architecture-kernel authority. | `ba033ae888f8f231e73aff4441a735ad72da251714530d53321896687927b6b1` |

## Workbook execution rendering

The files under `authority/rendered/workbook/` are deterministic, full-cell renderings produced from the authorised workbook to make complete semantic reading practical in Codex. They are **not summaries and not independent authority**. If a rendering and workbook differ, the workbook wins. Formatting-dependent or formula-dependent ambiguity must be checked against the `.xlsx` itself.

Every semantic worker and reviewer must read all rendered sheets in full before making its first Raw Signal semantic judgement in that thread, and must inspect the workbook directly whenever presentation, formula, merged-cell, or other workbook semantics may matter.

## Derived authority admission

Raw Signal module normative documents become active only after bounded source-backed semantic work and fresh independent review under the active ExecPlan. Accepted module authority belongs under `docs/architecture/`; tests derive from accepted module authority; implementation derives from accepted tests and authority.
