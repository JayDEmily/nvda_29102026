# ADR-WBV2-002 — Thirty downstream working modules and local strategy-code duplication

**Status:** Programme-owner-approved **Workbook V2 architectural design direction** (14 October 2026). Not an accepted production architecture allocation and not an amendment of the active M01 ExecPlan or normative calculation catalogue.

## Decision

1. Maintain shared **M00 Raw Signal Truth** and the proposed **M01-1 strategy-independent Derived Raw Signal** foundation. Raw or M01-1 results are reusable by all downstream modules; neither their canonical identity nor their calculation code is duplicated merely to serve several consumers.
2. Promote the **30 proposed responsibility groups** in the completed Pass 05 review to **30 proposed downstream working modules**, without introducing an interstitial shared-strategy-calculation module. Allocate **working labels** in the original Pass 05 group order: `P01 -> M02`, `P02 -> M03`, ... `P30 -> M31`.
3. Preserve exactly **95/95 excluded canonical D-signals** with their original D-identifiers and the original Pass 05 group membership: each D-ID has precisely one **proposed** module label in the Workbook V2 register. These are classifications for V2 workbook review, **not** official architectural `M` registry allocations, transfers of canonical D ownership or accepted product implementation.
4. **M02–M31 are independently executable peers.** No M02–M31 module may call, import from, read another peer's privately owned computed output, or require another M02–M31 module to run. Each may consume lawful shared M00 raw facts and proposed M01-1 strategy-independent derived-raw results. The base kernel permits declared acyclic M-to-M dependencies in general; this **V2-specific rule is stricter** and does not amend the generic architecture law.
5. If two or more M02–M31 modules require the same **strategy-dependent intermediate calculation**, each shall implement and test that arithmetic independently inside its own module, including any intermediate chain needed to reach M00/M01-1 inputs. A change to one local implementation must not implicitly alter another module. No shared downstream strategy-calculation layer is introduced.
6. **A local copy of code is not a second canonical `Dxxx` signal.** Each original D001–D209 identity remains singular and assigned once in the design crosswalk. Module-private intermediate results must receive local names, their own configuration/version/lineage and fail-closed proof obligations; they do not represent new canonical D-signal occurrences. Exact calculation mathematics must not be silently altered by local duplication.
7. The 107 D-to-D references crossing proposed M02–M31 groups are **historical/normative calculation-lineage references from the currently accepted single M01 graph**, not authorised M02–M31 runtime edges or directions of module coupling. For each proposed downstream module, a later implementation must establish **self-sufficiency**: all strategy-dependent intermediate arithmetic satisfied internally, lawful M00/M01-1 ingress only, no peer calls, and independent tests. Merely listing historical references does not establish that independent implementation exists. The original normative M01 graph is unchanged until separately authorised.
8. A working module number is an identity label, not an execution order or permitted dependency. The Pass 05 group/research mapping remains traceable.

## Workbook presentation

- Retain all existing sheets, including the seven original research tabs, the existing V2 `00_Guardrails & Method` and `M01-1 Derived Raw` tabs.
- Append six `M-001`–`M-006` constraints to the `00` worksheet (do not rewrite prior guardrails).
- Add `M02-M31 Module Register` containing all 30 working identities, exact D-memberships, responsibility and review boundaries.
- Add `M02-M31 Signal Allocation` containing a complete 95-row D-ID to proposed module crosswalk with original and normative provenance.
- Add one worksheet for each working module `M02` through `M31`, showing its assigned canonical D-rows and **historical cross-group D-lineage annotations**. Those annotations are **not** intended runtime dependencies on other proposed modules. These worksheets are documentation, not executable code.
- Retain Pass 05 evidence and the 95-row exclusion audit unchanged. No new 01/02 worksheets are required by this pass.

## Unresolved technical boundary

The Pass 05 effective normative catalogue contains **107 direct D-to-D references crossing proposed group boundaries**, corresponding to **67 distinct ordered group-pairs**. These remain **audit references to the accepted M01 calculation graph**, not module-to-module runtime contracts. They identify 107 *direct occurrences needing examination* when later proving module-local calculation closure; recursive dependency closure, contract/semantic compatibility, private implementation and independent proof are not yet established. No production change has occurred.

## Authority boundary

The root `GUARDRAILS.md`, root `AGENTS.md`, accepted root `EXEC_PLAN.md`, normative `NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, production M00/M01 implementation, architecture registry and tests are unchanged. Current production M01 still has the accepted D001–D209 calculation responsibility. No production module creation, Stage-2 implementation or acceptance is authorised by this V2 workbook decision.
