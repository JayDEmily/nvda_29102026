# ADR-WBV2-002 — Thirty downstream working modules and local strategy-code duplication

**Status:** Programme-owner-approved **Workbook V2 architectural design direction** (14 October 2026). Not an accepted production architecture allocation and not an amendment of the active M01 ExecPlan or normative calculation catalogue.

## Decision

1. Maintain shared **M00 Raw Signal Truth** and the proposed **M01-1 strategy-independent Derived Raw Signal** foundation. Raw or M01-1 results are reusable by all downstream modules; neither their canonical identity nor their calculation code is duplicated merely to serve several consumers.
2. Promote the **30 proposed responsibility groups** in the completed Pass 05 review to **30 proposed downstream working modules**, without introducing an interstitial shared-strategy-calculation module. Allocate **working labels** in the original Pass 05 group order: `P01 -> M02`, `P02 -> M03`, ... `P30 -> M31`.
3. Preserve exactly **95/95 excluded canonical D-signals** with their original D-identifiers and the original Pass 05 group membership: each D-ID has precisely one **proposed** module label in the Workbook V2 register. These are classifications for V2 workbook review, **not** official architectural `M` registry allocations, transfers of canonical D ownership or accepted product implementation.
4. If **two or more downstream modules need the same strategy-dependent intermediate computation** (rather than a reusable M00 or M01-1 foundational result), each module shall **own an independent local implementation** and local tests of that computation. A change to one local computation must not automatically modify another module. This is deliberate duplication, rather than a reusable downstream strategy calculation layer.
5. Existing canonical D-to-D dependencies across the proposed module boundaries are **not silently removed or duplicated**. Private code duplication and canonical `Dxxx` output identity are different concepts. For a future implementation, the precise contracts, consumer context, duplicated intermediate arithmetic, persistence and code ownership must be designed and authorised separately before replacing any current upstream-D usage. The current accepted M01 graph and semantics remain intact.
6. A module's *working number* does not establish dependency order. The former Pass 05 proposed group and research-source mapping remain traceable so that any future architecture admission can be checked against original evidence.

## Workbook presentation

- Retain all existing sheets, including the seven original research tabs, the existing V2 `00_Guardrails & Method` and `M01-1 Derived Raw` tabs.
- Append six `M-001`–`M-006` constraints to the `00` worksheet (do not rewrite prior guardrails).
- Add `M02-M31 Module Register` containing all 30 working identities, exact D-memberships, responsibility and review boundaries.
- Add `M02-M31 Signal Allocation` containing a complete 95-row D-ID to proposed module crosswalk with original and normative provenance.
- Add one independent worksheet for each working module `M02` through `M31`, showing its canonical D-rows and explicit external D prerequisites. These worksheets are documentation, not separately executable code.
- Retain Pass 05 evidence and the 95-row exclusion audit unchanged. No new 01/02 worksheets are required by this pass.

## Unresolved technical boundary

The Pass 05 effective normative D-dependency data contain **107 direct D-to-D references crossing the 30 working module assignments**, representing **67 distinct directed module-pairs**. These are *unresolved prospective ownership/interfaces*, not implemented independent modules. Do not claim they were migrated merely because the workbook now uses new module labels.

## Authority boundary

The root `GUARDRAILS.md`, root `AGENTS.md`, accepted root `EXEC_PLAN.md`, normative `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, production M00/M01 implementation, architecture registry and tests are unchanged. Current production M01 still has the accepted D001–D209 calculation responsibility. No production module creation, Stage-2 implementation or acceptance is authorised by this V2 workbook decision.
