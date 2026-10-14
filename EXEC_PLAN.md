# NVDA V2 — Active ExecPlan G01: Foundation Authority and Proof (2.1)

**Date:** 14 October 2026 (Australia/Melbourne)
**Status:** **ACCEPTED FOR G01 EXECUTION — programme owner, 14 October 2026.** G01-L1–L4 authorised sequentially, including bounded test reruns. This status does not assert any leaf has passed.
**Starting Git branch:** `work/v2-commissioning-brief-audit-handoff-20261014`
**Starting HEAD:** `c82daa03e0a870ff5b038ba41a4d560443dbecd3`
**Superseded plan:** original M01 209-signal root `EXEC_PLAN.md` from parent commit `c82daa03`; preserved in Git history. Explicit current owner instruction accepts this G01-only replacement. Original production responsibility remains unchanged.

## 1. One gate and one decision

**G01 proposition:** Define and independently establish the authoritative V2 shared-foundation boundary, including the precise calculations and input contracts eligible for that foundation. Test the current implementation against representative accepted meanings to detect and document calculation errors. **G01 does not implement, repair or accept the completed M01-1 software.**

The Programme Owner has accepted this **high-level architectural arrangement**:

- **M00 locked:** retain the admitted raw-record semantic owner, native record identities, values, timestamps, units, provenance, history and typed read-only public interface; no D-derived transformations added to M00.
- **M01:** retain the already registered architectural runtime identity. **M01-1** is its V2 descriptive-market/source-time calculation responsibility, **not** a second registered `M01-1` runtime object (the current `M` identifier grammar does not admit hyphens).
- **M01-1:** contain only precisely defined, reproducible and versioned strategy-independent measurements, with lawful M00 or qualifying foundational predecessor inputs, exact sampling/selection rules, refusal and lineage. Deterministic computation alone is insufficient for admission.
- **M02–M31:** future independent downstream peers; no downstream runtime, private implementation or private data dependencies between peers. Strategy-dependent intermediate chains are local to each peer. Their implementation is out of G01 scope.

**V2 decision precedence:** Owner's current direction and `GUARDRAILS.md` govern. For V2 design interpretation, the verbatim **ADR-WBV2-003** controls over prior **ADR-WBV2-001 and 002**; preserve and explicitly reconcile prior decisions and accepted original M01 mathematical authority, rather than silently discarding them. ADR-003 is an investigation commission, not by itself a production-admission certificate.

## 2. G01 leaves — in dependency order

### G01-L1 — Exact baseline and authority lock

**Proposition:** A single, fully identified source baseline supports the proposed foundation definition.

1. Resolve Git branch/HEAD/tree, clean/dirty state, archive hashes and effective normative catalogue revisions. Read in full `GUARDRAILS.md`, root `AGENTS.md`, applicable nested instructions, root `EXEC_PLAN.md`, ADR-WBV2-003/001/002, `handoff/m01_completion/AUTHORITY_INDEX.md`, the accepted calculation brief and all effective amendments.
2. Confirm effective D001–D209 identity, source-field and mathematical authority against the reference original workbook, Workbook V2 Pass08 and architecture ownership, taxonomy, public-seam and dependency laws.
3. Record that the current production M01 remit remains the original 209-D graph until a **separately accepted** ownership/ExecPlan transition. Do not substitute an audit's claim for governing files.

**Evidence:** exact Git/hash/authority index and documented conflicts; first unresolved required authority causes `BLOCKED` for its dependent work.

### G01-L2 — Define and reconcile foundation eligibility

**Proposition:** Each canonical D001–D209 identity has exactly one explicitly evidenced V2 target and every proposed foundational row has a strategy-independent meaning through its **complete** dependency closure.

1. Reconcile all 209 original identities with the currently proposed **114 M01-1 / 95 downstream** working allocation. These counts are starting hypotheses, **not** acceptance or completion percentages. Preserve the old stage/owner, original D identity, effective equation, units, raw/derived/context dependencies, fixed measurement conventions, versions and source contract.
2. Examine all 114 proposed foundation rows and their full typed/context/configuration and recursive D/R chains, including the **65 measurement-convention flags**. Reject or qualify anything whose meaning depends on candidate, portfolio, policy, order intent, discretionary weight or strategy-configured interpretation. Multiple inputs or descriptive regression do not alone disqualify a measurement.
3. Resolve semantic eligibility and version ownership **before** altering allocation. For every disputed row retain **current production owner**, **workbook-proposed owner**, **recommended disposition** and the exact owner decision required. Keep D001–D209 singular: no invented canonical identities.
4. Establish the intended `M01`/`M01-1` ownership statement, fixed measurement-definition/version rule, approved parameter-selection boundary, lawful M00 seam, output identity, lineage, persistence/recalculation constraints and explicit exclusions. Preserve prior durable M01 results as historical facts; do not silently relabel them.
5. Record where unfinished old M01 Stage-1/Stage-2 obligations fall: eligible foundation, downstream, authority/source blocked, or **DO_NOT_CARRY_FORWARD** from a future active tree with Git history retained. Do not carry old stage order into V2 as architecture.

**Evidence:** one 209-row canonical crosswalk; reviewed foundation-definition schedule; exception/decision register; architecture-responsibility text suitable for an exact authority-approval vote. No unapproved change to `modules.yaml`, the catalogue or workbook.

### G01-L3 — Independent numerical challenge and test rerun

**Proposition:** The test evidence distinguishes a correct accepted calculation from a fixture that accidentally validates incorrect source meanings. **Do not equate a green existing suite with proof of the V2 foundation.**

1. Before executing, read existing test sources and historical reviewer repairs. Specify the expected values independently from accepted definitions, using correct original `Rxxx` identities. Separate already-tested behaviour, missing proof, observed failure, suspected defect and unresolved source-contract authority.
2. **Rerun the existing relevant public-path tests** against the fixed Git candidate and reproducible environment, retaining commands, outputs and all failures; then separately run authority-derived adversarial tests. Existing test locations include:
   - `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py` (**D025**);
   - `tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py` (**D099/D100**);
   - `tests/product/derived_signal/test_m01_f4_macro_vintage_public.py` (**D009**).
3. **D025 discriminating witness:** original `R039=High=120`, `R040=Low=80`, `R037=Last=90`; accepted `(Last−Low)/(High−Low) = 0.25`. Current `_stage1.py` reads R039 as low and R040 as high; the historical symmetric midpoint fixture is inadequate to reveal that inversion. Prove both numerical output and lawful field identities through the public path.
4. **D099/D100 source-meaning witness:** native **R015 is option right C/P**, not numeric strike. Use actual C/P values and explicit versioned strike/contract metadata; prove correct IV/delta matching, required source identities and absence refusal. Do not change R015's meaning to satisfy an existing fixture.
5. **D009 vintage-meaning witness:** examine accepted `initial` / `latest_known_at_cutoff` / `revised` distinction and exact provider-time/cutoff semantics. Prove the missing category if its normative selection is sufficiently defined; otherwise mark the exact semantic question `BLOCKED`, not guessed.
6. Treat **D096 absent + D097/D098/D107/D108 dependencies**, **D117/R075**, **D123 official OI periods**, **D138 L2 snapshot/event semantics** and every further detected discrepancy as *distinct* implementation, authority, source-contract or coverage obligations. G01 establishes and records their definitions/status; it **does not build D096, invent mappings or repair kernels**.
7. Where applicable, rerun focused regression and the repository's architecture/public-seam/dependency checks needed to prove **this gate's** no-change and isolation propositions; record environment limitations (especially PostgreSQL) and `UNRUN` separately. Author new discriminating proof before any later production-behaviour repair; preserve red witnesses without weakening their expected result. Do not launch the entire obsolete 209-signal implementation programme.

**Evidence:** per-proposition witness/expected/actual/outcome matrix, exact test selection, commands, environment, raw outputs and failure classification. A test may intentionally remain **RED** in G01; report the proved discrepancy and stop the relevant repair path pending separate authority.

### G01-L4 — Independent authority review and freeze

**Proposition:** The exact proposed foundational responsibility and each admitted descriptive calculation definition are supported by primary evidence; all uncovered defects and incomplete proofs are explicit.

1. Freeze a clean, recoverable, evidence-only candidate with Git HEAD/tree, 209-row crosswalk, definition/version schedule, test log manifest, remaining discrepancies, and precise old-M01 disposition; do not edit frozen `GUARDRAILS.md` or production source/config/schema/tests to hide a failure.
2. Send the candidate to an **independent reviewer**. The reviewer checks semantic classification, numerical witness independence, exact raw meanings, scope of historical tests, unaddressed rows, contradictions and correct no-change boundary.
3. Present the bounded ownership/measurement authority for explicit Programme Owner approval. Only after acceptance may a **separate** V2 implementation/transition ExecPlan replace root `EXEC_PLAN.md` through the governed Git process.

**G01 success:** **FOUNDATION_AUTHORITY_ACCEPTED** only if the precise foundation scope and eligible calculation meanings are owner-approved, the required evidence and independent review agree, and all material errors/unknowns have explicit dispositions. This is **not** `M01-1_IMPLEMENTED`, `M01-1_TESTS_PASS` or permission to proceed to production repairs. Otherwise return **REPAIR / BLOCKED / PARTIAL** with the first unmet invariant and exact recovery checkpoint.

## 3. Explicit limits and next gate

G01 permits semantic inspection, read-only inventories and — **under the explicit programme-owner acceptance dated 14 October 2026** — bounded relevant proof/test execution. It does **not** authorise production repairs, changing M00, implementing D096, allocating M02–M31, running a broker, changing stored results, or deploying trading activity. The original-M01 ExecPlan is superseded only as execution schedule by this owner-accepted G01 plan; its original production responsibilities and accepted mathematical authority are not changed.

**Next gate after G01 acceptance, requiring its own separately approved plan:** govern the original-M01-to-V2 ownership/ExecPlan transition, then perform proof-before-production correction and separation work one accepted semantic unit at a time, with independent review. No known defective calculation can be declared fixed merely because G01 recorded or reproduced it.

## 4. Baseline evidence/state at G01 plan drafting (historical)

- **Verified by repository inspection, not test execution in this drafting task:** branch HEAD `c82daa03e0a870ff5b038ba41a4d560443dbecd3`; `M00` active, `M01` bootstrap with original D001–D209 remit; original active M01 plan; ADR-WBV2-003/001/002; `_stage1.py` D025, D099/D100 and D009 source branches; corresponding test sources.
- **Reported/partially established, requiring independent challenge:** the 114/95 allocation, 65 convention flags, D096 graph gap, D117/D123/D138 contract limits, and scope of historical test acceptance. Refer to `handoff/workbook_v2/reviews/v2_investigation_20261014/` as evidence to re-examine, not governing law.
- **Not performed while authoring this proposed plan:** any test suite, production code change, root ExecPlan replacement, new authority admission or semantic acceptance.

## 5. Activation and execution evidence

Programme Owner explicitly accepted this G01 plan for commit and sequential execution of G01-L1 through G01-L4 on 14 October 2026. G01 replaces the old M01 execution schedule only; it does not change production code, normative calculations or M00 authority. The accepted proposal is preserved byte-for-byte at `handoff/workbook_v2/g01/G01_ACCEPTED_PLAN_PROPOSAL_VERBATIM_20261014.md`. Each leaf will record its actual result and first unmet invariant in a separate evidence file. External independent review and further owner approval remain required before `FOUNDATION_AUTHORITY_ACCEPTED` may be claimed.

## 6. Executed G01 leaf ledger — 14 October 2026

The four leaves were visited sequentially; the distinction between evidence production and acceptance remains binding.

| Leaf | Observed work | Semantic disposition |
|---|---|---|
| G01-L1 | Exact baseline, archives, accepted amendments, 209 identity/acyclicity checks; evidence commit `7f0feb17` | Identity/authority baseline VERIFIED; does not prove eligible meanings |
| G01-L2 | Effective-catalogue 209-row full dependency crosswalk, V2 114/95 proposal, 65 frozen-convention flags, exact exception list; evidence commit `76df624c` | Population accounting VERIFIED; 114-row *semantic freeze / owner admission NOT COMPLETE* |
| G01-L3 | Existing focused 37 PASSED; three new authority-derived public-path tests FAILED (D025 0.75 instead of 0.25; D099/D100 native C/P refusal); architecture/dependency/public-seam scripts PASSED after `PYTHONPATH=src`; red proofs committed first | Bounded test investigation executed; material defects CONFIRMED and left unrepaired |
| G01-L4 | Review candidate and questions prepared for separate independent reviewer | Review NOT PERFORMED; owner acceptance NOT GRANTED; G01 PARTIAL/BLOCKED |

The current active plan is **not** a production-authority transition. The original 209-row mathematical remit and registered M01 state are unchanged. **Do not enter a later implementation gate or repair the red calculations under this G01.** First unmet acceptance condition is the exact independent semantic review and unadmitted definition/version decisions. This is a recoverable `PARTIAL/BLOCKED` checkpoint; do not label G01 `PASS`.
