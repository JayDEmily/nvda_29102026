# NVDA V2 — contract-correct controlled-input validation candidate

**Date:** 14 October 2026 (Australia/Melbourne)
**Status:** G01 proof/evidence work only; NOT independently reviewed or accepted as normative law, implementation authority, production repair, or a new active ExecPlan.
**Parent:** `08ec7686338d4bb01bb114269963db001dc94451` (`G01 PARTIAL/BLOCKED`).

## Owner instruction and scope

The owner confirms that mathematical/module validation **does not require live IBKR data**. Controlled synthetic values are valid when they preserve accepted raw-signal meanings, typed selection identity, units, timestamps, versioned selection, and lineage. Live provider-ingress readiness is a distinct proposition and must never be inferred from controlled inputs. The owner directs creating a work branch for this standard and requests tested promotion to `main` **only when applicable acceptance conditions are satisfied**.

This document captures the bounded validation approach; it does not install authority that G01 has not accepted. Current `EXEC_PLAN.md` expressly prohibits production repairs under G01; source/registry/schema changes and `main` promotion are not performed in this candidate.

## Candidate validation contract for future module work

1. **Canonical R identity first.** Every controlled input is declared as `(Rxxx, native value, native units, subject/contract identity, timestamps, provenance, projection mapping/version)`. The corresponding accepted raw-field specification determines its value type and meaning, not a convenience test fixture or a calculation implementation. Reject meaning substitutions even when the arithmetic would produce an expected number.
2. **Lawful M00 boundary.** Supply controlled M00 observations via admitted typed projection/public path, preserving raw occurrences and selection lineage. Do not place a derived or precomputed D result into an R field. Do not modify M00 merely to satisfy a downstream calculation.
3. **Independent numerical oracle.** Determine expected positive, asymmetric, boundary and refusal results from accepted calculation authority independently of production logic. Include cases capable of detecting field transpositions and implausible joins; symmetric/midpoint-only cases are insufficient for D025.
4. **Time and contract correlation.** Validate same-contract/same-expiry and required cross-field pairing, legal staleness and knowledge-cutoff conditions, absent or incompatible metadata, duplicate/conflicting observations, disallowed future input, and refusal without invented defaults.
5. **Exact version and lineage.** Each result must cite the accepted calculation definition, parameter profiles, raw input occurrence identities, mappings and unit conversions; retry/recalculation and persistence are separately proven where applicable. Downstream strategies must not alter foundational measurement definitions.
6. **Three distinct evidence labels.** `CONTROLLED_INPUT_CALCULATION_PROOF`, `NATIVE_SOURCE_CONTRACT_EVIDENCE`, and `LIVE_PROVIDER_INGRESS_EVIDENCE`. A passing controlled proof supports only the first. Provider connection or live data is **not** a prerequisite for calculation correctness.
7. **Independent acceptance.** Commit authority-derived proofs before implementation-behaviour changes; retain red results and their exact expected values; execute focused public-path and regression checks, then obtain independent semantic review before promotion. Green tests alone are not acceptance.

## Concrete current witnesses and unresolved dependencies

| Case | Canonical input contract | Independent proposition | Current checkpoint |
|---|---|---|---|
| D025 | `R037=Last`, `R039=High`, `R040=Low` | `Last=90, High=120, Low=80` gives `(90−80)/(120−80)=0.25`, not 0.75 | Red G01 public-path witness, no production repair |
| D099 | `R111=model IV`, `R112=model delta`, `R015=option right (C/P)`; same expiry/contract | 25Δ put IV 0.40 and call IV 0.30 gives +10 vol points | Red G01 public-path witness, with contract identity and strike as metadata |
| D100 | Same lawful raw meanings, target 10Δ | 10Δ put IV 0.50 and call IV 0.20 gives +30 vol points | Red G01 public-path witness |
| D120 | `R015=option right (C/P)`, `R016=contract multiplier`; trade R120/R121 and D015 | Distinguish right categorical truth from multiplier numeric truth; refuse or resolve missing required data without numerical reinterpretation | **Authority/source-contract BLOCKED**: accepted D120 catalogue currently lists R015 but not R016, while its equation uses a multiplier and its implementation parses R015 as numeric. New direct dependency or lawful identity metadata must be explicitly approved before a positive result is required. |

### Existing tests known to use inconsistent R values

- `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py` supplies numeric strike values under R015.
- `tests/product/derived_signal/test_m01_f3_grouped_public.py` supplies numeric multiplier 100 under R015.
- The previously committed G01 public-path witnesses use lawful C/P under R015 for D099/D100; they must **not** be rewritten to turn RED green.

## Boundaries and first outstanding invariants

- G01-L4 independent semantic review and owner approval of the M01-1 foundation definitions remain outstanding. This document does not substitute for them.
- The currently active root `EXEC_PLAN.md` permits proof/evidence work but expressly excludes production repairs; a separately accepted implementation-ready brief and ExecPlan transition are required for those changes under `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md`.
- The packaged local Git repository has **no `main` ref**, and its configured `origin` points to a non-existent local path. A separately discovered GitHub `main` must not be assumed equivalent to this unpromoted G01 lineage without ancestry/integrity verification. No `main` creation, overwrite or force-update is authorised by this evidence.

**Next lawful action after owner resolves missing prerequisites:** authority approval of the affected source contracts and exact repair scope, then proof-first bounded production correction, fresh independent review, and guarded promotion only to the verified accepted `main` target.
