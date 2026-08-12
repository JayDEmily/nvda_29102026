# NVDA Raw Signal Clean Rebuild — Authority Manifest

This repository distinguishes **source normative authority** from **derived module authority**. The Raw Signal module documents must be derived from, and remain semantically subordinate to, the source authorities below.

## Source normative authority

| Artefact | Role | SHA-256 |
|---|---|---|
| `authority/source/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx` | Authorised signal/data workbook; complete workbook is source authority. | `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae` |
| `authority/source/NVDA_CROSS_MODULE_DATA_IDENTITY_GUIDANCE_20260804.tar.gz` | Preserved supplied cross-module identity archive. | `bac8f4271c34cc945bdc6b4a51d6a6eea9c60b35f273de158d3726c1cc530ebc` |
| `authority/source/NVDA_CROSS_MODULE_DATA_IDENTITY_AND_DMPV3_GOVERNANCE_20260804.md` | Cross-module data identity, ownership and DMPV3 governance authority. | `ec9b64534ad8d28a76375874c9097e5f61fe2699da4e1bc0a622aa84e5d268fb` |
| `docs/architecture/ARCHITECTURE_KERNEL_RESET_BRIEF.md` | Architecture-kernel source authority. | `5d722717509775df5a52f8a6e3a3ff3ddfe5e31650d56053d39d071b7abbd9df` |
| `docs/architecture/ARCHITECTURE_KERNEL.md` | Architecture-kernel source authority. | `74d632a0221968d7fada3ee436d8b8f69c979a83057e55826702856a16700491` |
| `docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md` | Architecture-kernel source authority. | `285b25bc847b8bb5b35322becace2665968fc5a280cefc40be818c0209d8bd6f` |
| `docs/architecture/DEPENDENCY_LAWS.md` | Architecture-kernel source authority. | `a7253fc48132af4b90b79ef50dde125f782053ebe7aebb1e94265a99559f1add` |
| `docs/architecture/PUBLIC_SEAM_LAW.md` | Architecture-kernel source authority. | `09b1f286b24803011819d010d51643a89a7b92bc9c439bb496078489d2443e2b` |
| `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` | Architecture-kernel source authority. | `2ce24aa5cdfc4a1fd41110e229c137f1cdacdf18cbc59b3a0e7a861207cdbf4f` |
| `docs/architecture/EXTENSION_AND_RETIREMENT_RULES.md` | Architecture-kernel source authority. | `ba033ae888f8f231e73aff4441a735ad72da251714530d53321896687927b6b1` |

## Workbook execution rendering

The files under `authority/rendered/workbook/` are deterministic, full-cell renderings produced from the authorised workbook to make complete semantic reading practical in Codex. They are **not summaries and not independent authority**. If a rendering and workbook differ, the workbook wins. Formatting-dependent or formula-dependent ambiguity must be checked against the `.xlsx` itself.

Every semantic worker and reviewer must read all rendered sheets in full before making its first Raw Signal semantic judgement in that thread, and must inspect the workbook directly whenever presentation, formula, merged-cell, or other workbook semantics may matter.

## Candidate derived material

`authority/candidate/` may contain prior Raw Signal normative text imported without its old Git history. Candidate material is **non-authoritative evidence**. It may accelerate comparison, but it must never be used to override, fill gaps in, or reinterpret source normative authority.

## Derived authority admission

Raw Signal module normative documents become active only after bounded source-backed semantic work and independent review under `PLANS.md`. Accepted module authority belongs under `docs/architecture/`; tests derive from accepted module authority; implementation derives from accepted tests and authority.
