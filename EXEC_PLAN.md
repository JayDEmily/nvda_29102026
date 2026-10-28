# M00 downstream contract reconciliation — ExecPlan

Date: 28 October 2026, Australia/Melbourne. Plan ID `M00-DOWNSTREAM-RECONCILIATION-PLAN-1`.

**Status: OWNER ACCEPTED AND EXECUTION COMMISSIONED — 28 October 2026.**

Current owner commission: “Okay, that's approved. Complete the plan.” This accepts the plan and commissions L00–L14 continuously under its independent review/checkpoint protocol. Earlier planning-only/no-test restrictions describe the completed drafting pass; they do not prohibit the explicitly planned scoped future proof. D145 implementation and unrelated holds remain excluded. This commission permits routine contract/profile choices needed to make the approved leaves concrete; it does not authorise silent mathematical changes or a fabricated source clock.

**Goal:** Reconcile the identified downstream source contracts, owning code and module-scoped tests with the completed M00 native-shaped synthetic output, while preserving prior controlled evidence and every unrelated hold.

**Architecture:** M00 owns immutable raw observations, projections and control discoverability. M02 owns neutral calculation input selection, book reconstruction, quote assembly, derived results and their durable lineage. Each module is proved within its own span against an explicit public input contract. There is no proposed M00→M01→M02 end-to-end test suite, automatic M01 activation or application composition.

**Tech stack:** Retain the accepted CPython 3.12.14 environment and pinned dependencies: pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11, PyYAML 6.0.3; accepted prior SQLite evidence records 3.53.1. Execution must record its actual environment rather than infer it from this plan. Do not substitute Python 3.13 or install PostgreSQL.

**Specification and authority:** Current owner request to write this plan, the preceding static impact review, frozen `GUARDRAILS.md`, applicable agent instructions, architecture ownership/dependency law, the preserved M00 Brief2 and existing accepted calculation authority. The static review identifies reconciliation work; it does not supply new mathematical definitions, numeric policies or implementation authority. Exact changes to source profiles, temporal bases, public carriers and acceptance cases must be resolved in G1 before their implementation.

For future execution, follow the repository's established one-leaf / independent-review / strict-proof / cumulative-download method. Generic skill defaults do not override the owner's no-test instruction for this planning pass or the existing bounded per-signal method. Read the relevant execution skill only after execution is commissioned.

## 1. Starting state, preserved plans and commission boundary

Starting accepted M00 checkpoint: `9b400183f275c3147b568d21b995b4aebd2af3c3` (L06). Previous signal anchor: D143 `17d7553cf3ad92700f849f696134de67b64b0dfa`.

The completed M00 root plan is preserved byte-identically at `handoff/planning/m00_downstream_reconciliation_20261028/COMPLETED_M00_BRIEF2_EXEC_PLAN.md` and in the starting commit. Its completion and evidence are retained. The earlier next-twenty plan remains PAUSED at `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md`; D145 is its outstanding scheduled signal. Neither plan automatically resumes.

Root `EXEC_PLAN.md` is the single proposed successor planning entry point. Its execution role begins only after explicit owner acceptance and commissioning. The completed plan's active scheduling role is `DO_NOT_CARRY_FORWARD`; its bytes, source, fixtures, evidence and full Git history are retained. Earlier AGENTS/test-map execution wording describes prior commissions and does not authorise new implementation in this planning pass.

This pass may write and inspect documentary planning material and save it for download. It must not run tests, product replay, exporters, static analysers or runtime probes; change production/tests/proof admissions or immutable generations; install runtimes; or execute any future leaf. Documentary self-review and file/Git inspection are allowed. No future leaf is marked complete by preparing this plan.

D145 remains paused throughout this reconciliation plan. L13 produces an explicit source/time disposition and a bounded successor proposal, not a D145 implementation. Any implementation or changed mathematical/time policy needs its own accepted authority. All other holds, including D120–D122 and D141/D142/D144, remain in force.

## 2. Evidence basis and scope of the identified impact

The prior static pass compared D143 to L06 and inspected the relevant public contracts, consumer code, fixtures, paused plan and review records. The implementation delta in `src/` is confined to M00's `_native_codec.py` and `api.py`: additive UTC-datetime encoding and observation-history enumeration. M01/M02 production files and existing signal product tests were unchanged by Brief2. New M00 proof and shared proof-control support were also added.

The following are source-relative compatibility findings, not observed new runtime regressions. Existing synthetic profiles remain evidence only for their exact accepted inputs and scope. Neither numerical agreement nor an old PASS establishes compatibility with a differently scoped native-shaped source.

| ID | Identified difference | Owning reconciliation and leaves |
| --- | --- | --- |
| I01 | Native depth preserves side 0 ASK / 1 BID; existing controlled SMART consumers and fixtures use 0 bid / 1 ask. | M02 versioned source interpretation; L01–L10. D136 inherits predecessor meaning. |
| I02 | Native-shaped depth is receipt-only with absent source timestamp/timezone; current book readers request event filtering and require true-instant lineage. | M02 selection/time carriers and codecs; L01/L02 and L04–L11. D145 disposition L13. |
| I03 | Errors 316/317, gap, reconnect and restart are separate controls; current consumers model reset through operation 317 and expose projection-only input protocols. | M02 control input/lifecycle contract using M00 public history; L01/L02 and L04–L11. |
| I04 | Direct positions span each subscribed book side across MPIDs; D143 partitions position lists by venue/side and restarts position zero per venue. | M02 subscribed-book reconstruction then qualified grouping; L11. |
| I05 | Options Level I is asynchronous and receipt-only; D087 uses an exact timestamped snapshot profile and D137 requires a single co-referenced occurrence. | M02 separately versioned assembly/selection; L03/L12. Retain lawful atomic stock path. |
| I06 | D145's paused profile requires native event-time windows, absent from the verified depth source. | Documentary disposition before resumption; L13. No fabricated source time. |
| I07 | SQLite datetime persistence now supports collector receipt carriers; retained PostgreSQL codec is separate and lacks that extension. | Reuse accepted M00 SQLite evidence; L00/L09/L10 and L14 record backend limits. PostgreSQL runtime/correction is excluded. |
| I08 | Shared proof loading now validates the fixed M00 Brief2 extension alongside authorised claims. | G01 build/proof dependency accounting in L00/L01; no cross-module semantic tests or speculative runner rewrite. |

Primary source navigation:

- `handoff/planning/m00_brief2_20261027/BRIEF_2_M00_RECONCILED_V3_20261027_1622_AEDT.md`, SHA256 `0d5ee211c1285b31834062ab2d871670ed2f318cbb955e7df95f80067d562007`.
- `handoff/m00_brief2/FINAL_REPORT.md`, `evidence/L06/FINAL_REVIEW.md`, `outputs/L05_verified/` and its replay/schema/oracle/acceptance files.
- `handoff/m00_brief2/authority/CONTROL_HISTORY_CONTRACT_V1.md`; inspect its implementation and independent approval rather than treating its preserved proposal header as current acceptance.
- `src/nvda_desk/raw_signal_occurrence_truth/api.py`, `_native_codec.py`, `_sqlite.py`, `_postgres.py`.
- `src/nvda_desk/market_measurement_truth/api.py`, `_selection.py`, `_book_depth.py`, `_smart_depth.py`, `_smart_ask.py`, `_smart_imbalance.py`, `_book_slope.py`, `_book_insert_rate.py`, `_book_delete_rate.py`, `_direct_venue.py`, `_option_scalars.py`, `_microprice.py`, `_evaluation.py`, `_record_store.py`.
- `tests/product/market_measurement_d087/`, `market_measurement_d131/`, `market_measurement_d134/`, `market_measurement_d135/`, `market_measurement_d136/`, `market_measurement_d137/`, `market_measurement_d138/`, `market_measurement_d139/`, `market_measurement_d140/`, `market_measurement_d143/`; read each owning claim/authority/generation alongside its test.
- `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, its catalogue and the exact D138/D145 owner-approved overlay dated 16 October 2026; current per-signal construction briefs/bindings remain applicable.
- `config/architecture/modules.yaml`, `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`, `DEPENDENCY_LAWS.md`, `IMPLEMENTATION_AUTHORITY_INGRESS.md`; `tools/product_proof_claims.py` and applicable `config/product_proof/` entries.

Navigation is not a claim that all listed source files have been read in full in this planning pass. L00 must record fresh full/partial inspection boundaries. No exhaustive D001–D209 reacceptance is proposed.

## 3. Global constraints and review focus

1. Preserve M00 native facts, existing public v1 payload semantics, immutable fixture families A/B/C, actual outputs, proof generations, previous failures and complete history. A5's midpoint-100 market is isolated from coherent C1's 1.20/1.40 market.
2. M00 performs no book reconstruction, quote assembly, derived calculation or consumer completeness certification. M02 consumes only lawful M00 public types/seams. M01 stays in its existing bootstrap/non-composable status; do not migrate its historical implementation into the active path.
3. Native operations are 0 insert / 1 update / 2 delete. Error 316/317 is never an R187/R194 depth operation in a native-compatible profile. A legacy synthetic reset carrier cannot quietly represent provider-native error semantics.
4. Preserve per-callback identity, Decimal lexical scale, exact integer/Decimal distinctions, source timestamp absence, receipt UTC, request, source, subject/right, generation, exchange, MPID and mapping versions. Do not fill absent fields or infer causal order from an occurrence-ID tie-break.
5. Native enum values may be interpreted by an explicit owner-local mapping while original projected values stay unchanged. Do not globally flip legacy records or reuse an old identity/version for changed semantics.
6. Each owning module's tests cover its own span. Consume the frozen M00 public-output contract as input evidence; do not rerun M00 production end-to-end for every M02 leaf or invent a chain-wide gate. Existing lawful public predecessor materialisation remains permitted where a signal's own contract requires it.
7. Preserve valid existing tests. Classify each assertion as unchanged, materially invalidated, legacy-profile-only or requiring a new versioned profile. Never weaken assertions or discard evidence to obtain green.
8. Carry forward the established exactly-two physical cases per D profile (one success, one reached refusal; six hard ceiling per identity). Preserve existing valid profiles/cases. If retained old cases plus a necessary new profile exceed this allowance, resolve exact allocation with owner authority in L01 before test authorship; no hidden loops, duplicate cases or self-authorised cap increase.
9. Future product execution: one independent final semantic reviewer as sole strict executor per leaf; no routine RED, duplicate GREEN, broad suite or unaffected regression. A failed check repeats only after documented material repair; a successful check repeats only for precise material invalidation. Retain original output and immutable generations.
10. Reuse accepted M00 37-case, original SQLite compatibility and reproducibility evidence only where its source/proposition remains unchanged. This is prior evidence, not a new run. Source edits require a scoped invalidation assessment before proceeding.
11. Scoped static checks and strict product gates occur only after execution commissioning. Retain the pinned environment; no PostgreSQL server, live IBKR calls, production entitlement claims, catalogue-wide rewrite, A00 composition or unrelated module work.
12. Stop dependent work at the first missing authority or failed invariant. A documentary blocker disposition is not an implemented capability or a completed mandatory runtime leaf.

Review focus allocated to future proof: side inversion and asymmetric expected results (L05–L10); receipt-only exclusion under event filtering (L02–L11); hidden reset/restart and incomplete re-warm-up (L02–L11); subscribed-book position shifts across MPIDs (L11); asynchronous quote identity/skew/age and missing constituents (L03/L12). Ambiguous receipt/sequence ties and generation boundaries belong in the accepted source contract and must not be hidden by convenient fixtures.

## 4. Gates, leaves and dependency order

Retain the established G0–G5 gate structure. Leaves are independently reviewable semantic obligations; their count follows the affected owners/profiles. Leaf numbering here is local to this plan and does not replace M00 Brief2's completed L00–L06.

| Gate | Acceptance boundary | Leaves |
| --- | --- | --- |
| G0 | Starting evidence, ownership and precise impact/invalidation inventory fixed | L00 |
| G1 | Exact source profiles, public interfaces, oracle and proof allocation authorised before code | L01 |
| G2 | Receipt/control input, durable lineage and compatible option quote selection reconciled | L02–L03 |
| G3 | Affected SMART and direct-book calculations reconciled within M02 | L04–L11 |
| G4 | Microprice quote domains reconciled and D145 timing conflict explicitly disposed | L12–L13 |
| G5 | All required evidence reconciled; cumulative delivery and resumption boundary recorded | L14 |

Execution dependencies: L00 → L01 → L02 → L03. L04 requires L03's actual compatible D087; L05 → L06 → L07 covers bid/ask predecessors and imbalance. L08 requires actual compatible D011. L09 → L10 covers insertion/deletion source reuse. L11 requires L01/L02. L12 uses L03's approved quote assembly contract without adding D087 as a mathematical predecessor. L13 requires the resolved temporal/control contract. L14 requires all mandatory implementation leaves and the explicit L13 disposition.

Default sequential traversal after commissioning: L00 through L14 in numerical order. Work one leaf at a time. Any justified order adjustment must preserve these dependencies and be recorded before advancement; publication of the preceding accepted leaf's checkpoint remains mandatory.

Every leaf below ends with the checkpoint protocol in §6. A code/test-independent documentary leaf may close through documentary evidence only; it does not require a token runtime test.

### G0 / L00 — freeze the impact boundary and evidence reuse

**Files:** create `handoff/downstream_reconciliation/L00/BASELINE_AND_IMPACT.md`; read the primary paths in §2. No product change in this leaf.

- [x] Read governing files and relevant source/authority in full where conclusions depend on them; record exact starting commit and full/partial coverage.
- [x] Re-derive I01–I08 from source, including the purpose and authority of each legacy synthetic convention. Distinguish an old limited proof from an invalid claim of native compatibility.
- [x] Enumerate affected callers, public protocols, codecs, owning tests/claims, predecessors and direct dependants. Record D136's D134/D135 dependence and D131's D087 dependence. Trace further dependants only where an affected output contract actually propagates; no blanket invalidation.
- [x] Classify unchanged evidence and precisely invalidated propositions. Record that the datetime fix already exists and that PostgreSQL's separate codec is a deferred backend issue, not an instruction to repair it here.
- [x] Account for shared proof-loader M00-extension validation as a governance/build prerequisite. Preserve valid admissions; propose G01 changes only if an actual control defect is identified.
- [x] Obtain independent documentary acceptance, commit and publish cumulative checkpoint.

**Acceptance:** exact affected/unaffected/unknown inventory and reusable evidence ledger exist; no tests are run merely to establish the inventory.

### G1 / L01 — approve consumer source contracts and proof allocation

**Files:** create `handoff/downstream_reconciliation/authority/CONSUMER_SOURCE_CONTRACT_V1.md`, `PROFILE_AND_PROOF_ALLOCATION.md`, independently authored `fixtures/` and `expected/` under this handoff; proposed bindings/claim deltas remain documentary until authorised.

- [ ] Specify exact per-profile provider/variant, subject/right, request/exchange, generation, mapping IDs/versions, units, side interpretation, receipt window, cutoff, completeness and identity eligibility. Treat M00's immutable A/B/C examples as separate source scenarios.
- [ ] Specify an additive M02 raw/control reader contract using the existing public `list_projected_raw_history(...)` and `list_raw_observation_history(...)`. Copy exact signatures/types from M00 at the execution anchor; no imagined selector API or private database enumeration.
- [ ] Specify ordered merging of projected mutations and separately discovered controls, G1 outgoing/G2 incoming restart discovery, invalidation policy for error/reset/gap/reconnect, explicit re-warm-up criteria, and refusal for unresolved causal ties. Control policy belongs to M02 and must identify its accepted authority.
- [ ] Specify typed receipt/event basis in lineage and owner-local durable decoding. Preserve absent provider time and legacy carrier compatibility; do not weaken the original Decimal-only selector globally.
- [ ] Specify direct positions per subscribed book side, source exchange distinct from MPID, and the exact grouping/depth scope for concentration. Specify asynchronous quote membership, selection time, skew/age bounds and lineage. The brief's 250 ms / 1000 ms examples are synthetic candidates, not approved production policy.
- [ ] Publish independent numerical oracles and two-case allocations per affected D/profile. Resolve the six-case ceiling and legacy retention explicitly before implementation; retain the original top-one D135 incompatibility refusal for D136 unless an exact replacement is authorised.
- [ ] Identify each semantic change needing owner acceptance: new temporal/source profiles, quote assembly policy/domain, direct grouping scope, public carrier/codec additions, new proof admission and any D145 time-basis revision. Obtain exact required approval and lawful ingress binding before dependent code.
- [ ] Obtain independent contract/oracle documentary review, commit and checkpoint. If required authority is absent, publish the blocked contract proposal and stop its dependent leaves; never label G1 accepted by reviewer judgement alone.

**Acceptance:** no implementation-relevant source/policy/interface ambiguity remains for commissioned leaves; normative approval and independent review are separately identified.

### G2 / L02 — additive M02 receipt/control input and durable lineage

**Files:** proposed additive public types/protocols in `src/nvda_desk/market_measurement_truth/api.py`; focused owner-local source/control helper and codec support only if L01 requires them; exact proof files/claim fixed by L01. Preserve `_selection.py` legacy numeric behaviour.

- [ ] Author the admitted module-local proof from L01 before production changes: separate control discovery, receipt-only input selection with null event cutoff, strict source isolation, deterministic pagination and typed durable lineage.
- [ ] Implement the approved public input protocol and bounded M02 interpretation of controls. Merge events under declared order; refuse ambiguous required transitions and incomplete generation restart state.
- [ ] Implement approved typed receipt basis without fabricating event datetimes. Preserve original projections in lineage and version changes; keep old persisted records readable under their original owner/profile.
- [ ] Prove public owner and fresh ordinary read-only SQLite readback for the exact new carriers and refusal outcomes. Exercise an independent literal omission/order/control sequence under the declared case allocation.
- [ ] Independent semantic review and only the admitted scoped strict proof; assess impacted existing claims; commit and checkpoint.

**Acceptance:** M02 has a lawful input/lineage capability for native-shaped receipt/control facts. No new M00 API or M00 proof run is presumed necessary. If common semantics require per-family carriers, keep them bounded and bind each dependent leaf explicitly.

### G2 / L03 — D087 asynchronous option quote selection

**Files:** `_option_scalars.py`, additive owner-local assembly/carriers/codec where L01 authorises them, `tests/product/market_measurement_d087/test_signal.py`, owning profile/claim.

- [ ] Preserve the old timestamped synthetic snapshot profile. Introduce only the separately authorised receipt-based option profile with explicit membership, right, request, generation, age/skew and cutoff policy.
- [ ] Select four-callback A2/A3 constituent identities as applicable without manufacturing a shared native occurrence. For coherent C1/A2 reference context, bid1.20 and ask1.40 give midpoint1.30 with both exact source lineages.
- [ ] Publish exact approved selection/oracle/refusal before code; author the two-case profile using the agreed missing/stale/mismatched constituent refusal. No assumed production authority for example250ms/1000ms thresholds.
- [ ] Preserve the full raw constituent identities and assembly policy/version in derived lineage and durable readback. Independently review/strict proof, commit/checkpoint; then unblock L04.

**Acceptance:** actual public D087 can supply the newly approved coherent option profile without inventing an event timestamp or atomic callback. If quote-policy authority is absent, L03 and L04 remain BLOCKED.

### G3 / L04 — D131 option depth band, after compatible D087

**Files:** `_book_depth.py`, relevant M02 public types/codec, `tests/product/market_measurement_d131/test_signal.py`, exact owning authority/admission/generation.

- [ ] After L03, materialise actual compatible public D087 for the selected coherent option profile; keep legacy midpoint100 separate from coherent midpoint1.30.
- [ ] Author the approved success/refusal pair: coherent C1 has midpoint1.30, inclusive half-dollar band0.80–1.80, sizes5+3=8 contracts; outside bid0.70 size7 is excluded. Oracle is independently specified, not a hard-coded calculation substitute.
- [ ] Reconcile side, receipt selection, separate controls and complete positional replay; refuse reset/discontinuity without required fresh warm-up. Preserve exact predecessor, raw and configuration lineage.
- [ ] Preserve still-valid legacy proof as separately scoped evidence; independently review, run only warranted strict proof, commit and checkpoint.

**Acceptance:** exact band depth and reached refusal supported by M02-local proof using actual compatible D087; no cross-scenario quote mixing or fabricated predecessor.

### G3 / L05 — D134 native-compatible SMART bid depth

**Files:** `_smart_depth.py`, relevant public types/codec, `tests/product/market_measurement_d134/test_signal.py`, owning profile/claim.

- [ ] Author the approved two-case profile using native bid side1 and ask side0, receipt-only fields and explicit source/generation. A4 bid sizes5/3 yield8 shares.
- [ ] Preserve four mandatory R roles; do not add price as a new mathematical dependency. Reconcile controls and positional warm-up through L02. Preserve/reach the missing-operation refusal with other fields visible.
- [ ] Implement minimal owner changes; independently review the source interpretation and strict pair with durable readback; commit and checkpoint.

**Acceptance:** native bid selection and exact result8, plus reached refusal, retain full typed source/time/control lineage.

### G3 / L06 — D135 native-compatible SMART ask profiles

**Files:** `_smart_ask.py` and its lawful shared owner-local helper, public types/codec, `tests/product/market_measurement_d135/test_signal.py`, owning profiles/claim.

- [ ] Reconcile approved top-two and top-one profiles without overwriting old definition/parameter/selection identities. Native ask side0 sizes2/4 yield top-two6 and top-one2 shares.
- [ ] Author the allocated success/refusal pair with a separate reset control after warm-up; no synthetic native operation317. Preserve any still-valid legacy cases within L01's approved count allocation.
- [ ] Reuse L05's accepted shared semantics and re-prove only materially affected obligations; independent review/strict proof/readback; commit and checkpoint.

**Acceptance:** both explicitly approved depth profiles preserve their exact meaning and reset refusal; shared-source changes do not silently invalidate L05.

### G3 / L07 — D136 compatible actual bid/ask predecessors

**Files:** `_smart_imbalance.py`, `tests/product/market_measurement_d136/test_signal.py`, owning profile/claim; code changes only if required by the revised predecessor contract.

- [ ] Materialise actual public compatible L05/L06 predecessors: bid8 and ask6 yield exact1/7. Preserve both identities and matching source/generation/time/level context.
- [ ] Preserve the reached refusal with actual top-one D135 ask2 against the unchanged common-top-two request. Do not fabricate a predecessor or change only the requested depth.
- [ ] Amend lineage/version checks only where their contract materially changed; keep the imbalance equation unchanged. Independent semantic/strict proof and readback, commit/checkpoint.

**Acceptance:** revised source meaning propagates correctly through actual predecessors; no stale inherited acceptance by numeric coincidence.

### G3 / L08 — D138 side-specific book slopes

**Files:** `_book_slope.py`, relevant public carriers/codec, `tests/product/market_measurement_d138/test_signal.py`, owning profile/claim and accepted D138 overlay.

- [ ] Define the approved receipt-only three-level source fixture and actual compatible public D011 midpoint. Preserve K06, P_REGRESSION, units and equation; source reconciliation is not mathematical redefinition.
- [ ] Use native side1 bids and side0 asks, correct ladders, complete pre-selection book and separate control invalidation. Independent oracle retains bid slope7/2 and ask slope5/2 for its explicitly bound controlled fixture.
- [ ] Author the allocated success and reset-without-warm-up refusal; preserve all five projected roles and typed provenance, independently review/strict proof/readback; commit/checkpoint.

**Acceptance:** bid/ask outputs cannot be silently swapped; actual midpoint and revised input/control semantics are proved.

### G3 / L09 — D139 collector-receipt insertion rate

**Files:** `_book_insert_rate.py`, relevant public request/lineage/codec, `tests/product/market_measurement_d139/test_signal.py`, owning profile/claim.

- [ ] Keep the accepted four-second R001 receipt bucket and bid positions1–2 policy unless separately amended. Specify native bid side1 and genuine collector-added R001 equal to envelope receipt, with absent provider event time.
- [ ] Author success: selected inserts sizes3/5 yield count1/2 events/s and size2 shares/s. Preserve the visible missing-operation refusal and exact pre-window warm-up.
- [ ] Remove unsupported true-instant dependency only in the new approved profile; process separate controls through L02 and preserve the original raw metadata. Reuse M00's existing datetime persistence evidence rather than repairing its codec again.
- [ ] Independently review/strict proof and typed durable readback; commit/checkpoint.

**Acceptance:** rates depend on the declared receipt clock, never a fabricated source timestamp; original native and collector provenance remain distinct.

### G3 / L10 — D140 collector-receipt deletion rate

**Files:** `_book_delete_rate.py`, its lawful L09 source helper, public types/codec, `tests/product/market_measurement_d140/test_signal.py`, owning profile/claim.

- [ ] Preserve the two-second receipt bucket, bid positions1–2 and actual pre-delete size semantics under the native-compatible side/source contract.
- [ ] Author success: native deletion size0 removes actual standing size6, giving count1/2 events/s and removed size3 shares/s. The refusal addresses a nonexistent standing position; no invented zero removal.
- [ ] Preserve warm-up, separate controls, typed R001 provenance and exact fresh SQLite readback; independent semantic/strict proof; commit/checkpoint.

**Acceptance:** deletion consumes pre-delete standing state under the revised input contract, with no accidental reinterpretation of native zero size as removed quantity.

### G3 / L11 — D143 subscribed direct book and qualified concentration

**Files:** `_direct_venue.py`, direct request/row/lineage types in `api.py` and codec as required, `tests/product/market_measurement_d143/test_signal.py`, owning profile/claim.

- [ ] Reconstruct one selected subscribed book per side, applying positions across MPIDs; retain requested exchange independently from MPID, native side and per-callback occurrence.
- [ ] Group reconstructed rows only after positional replay, under L01's exact approved concentration scope. Do not treat MPID as an unqualified exchange or restart positions per MPID.
- [ ] Define the approved success fixture using C2-compatible rows: ALPHA4+2 and BETA1+1 give grouped quantities6/2; if the accepted scope includes those complete rows, independent shares3/4,1/4 and HHI5/8 follow. This scope must be authorised before changing legacy per-venue-top-one semantics.
- [ ] Preserve reached missing-MPID refusal with size still visible; include required cross-MPID position mutation evidence within the authorised pair rather than an unbounded scenario loop. C3 CALL remains a conditional source specimen, not a direct-feed entitlement or PUT coverage claim.
- [ ] Reconcile receipt/control inputs, independently review scoped strict proof and durable readback, commit/checkpoint.

**Acceptance:** subscribed-book addressing, qualified source identities and exact grouping scope are independently established; same HHI does not mask a different book model.

### G4 / L12 — D137 coherent quote domains and assembly

**Files:** `_microprice.py`, approved quote carriers/helper, `tests/product/market_measurement_d137/test_signal.py`, owning profile/claim.

- [ ] Preserve lawful atomic shares co-reference and original stock microprice201/2. The existing single-occurrence rule remains meaningful for that exact profile.
- [ ] For a separately authorised asynchronous option extension, use L03's approved assembly contract without adding D087 as a mathematical predecessor. Preserve four independent callback identities, receipt windows and complete lineage.
- [ ] Bind exact independent option microprice oracle and reached refusal to the approved fixture/case allocation before implementation; retain denominator-zero law and refuse incomplete/mismatched assembly without fusing raw observations.
- [ ] Independently review/strict proof and durable readback of authorised profiles; commit/checkpoint. If option-domain extension is not authorised, record its scoped blocker and retain atomic-only capability; do not claim the extension complete.

**Acceptance:** each authorised quote domain has correct co-reference or explicit derived assembly, mathematical output and absence semantics. A retained atomic stock proof does not certify asynchronous option consumption.

### G4 / L13 — D145 and held downstream work: documentary disposition

**Files:** create `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` and an explicit proposed paused-plan amendment; inspect the D138/D145 overlay and dependency traceability. No D145 product code/test/claim is created here.

- [ ] State the source conflict exactly: verified updateMktDepthL2 specimens lack provider event time; paused D145 requires an event-time one-second window with complete pre-window book and each intermediate transition.
- [ ] Recommend retaining that event-time profile as BLOCKED on a lawfully timestamped source, unless the owner explicitly approves a separately versioned receipt-clock synthetic profile. Do not silently change K17, collapse equal-time transitions or fabricate source time.
- [ ] Define the exact evidence and authority needed for any successor D145 plan: native sides, position-based mutations, control invalidation, warm-up, chosen clock/window and full intermediate best-book states. No automatic D145 implementation or old-plan resumption follows.
- [ ] Trace actual affected downstream contracts without promoting historical graph counts into newly proved executable dependants. Keep D120–D122, D141/D142/D144 and other existing holds explicit; source fidelity alone does not resolve their missing policies/prerequisites.
- [ ] Obtain independent documentary review and checkpoint. This leaf may be complete as a truthful disposition while D145 capability remains BLOCKED; do not describe the latter as accepted execution.

**Acceptance:** precise resumption condition, owner decision boundary and retained holds are recorded. No arbitrary replacement clock or new deferral-by-convenience.

### G5 / L14 — final independent disposition and cumulative handover

**Files:** create `handoff/downstream_reconciliation/FINAL_REPORT.md`, per-leaf evidence index and independent final review; update only this root plan's actual ledger/status.

- [ ] Map I01–I08 to exact source/profile/test deltas, accepted evidence, reviewed commits and checkpoint links. Distinguish full inspection, partial inspection, inference and unknown.
- [ ] Reconcile every shared helper/public carrier change against earlier accepted leaves. Re-prove only propositions precisely invalidated by later changes, through their owning claims; no final chain-wide or broad-suite run.
- [ ] Verify immutable M00 fixtures/outputs/history remain preserved and reuse their valid acceptance evidence. Record SQLite capability, PostgreSQL datetime gap/runtime deferral and live-provider exclusions separately.
- [ ] Independent final semantic review checks coverage, ownership, failure/repair lineage, per-profile case allocation, all required leaf checkpoints and remaining blockers. A required implementation leaf BLOCKED means partial delivery, not full reconciliation completion.
- [ ] Deliver final cumulative full-history checkpoint with reports, authority/profiles, schemas/oracles, code/tests, evidence and restore instructions. Keep D145/old schedule paused pending explicit subsequent commission.

**Acceptance:** every mandatory authorised implementation leaf is independently accepted, every conditional exclusion/blocker explicitly scoped, and final delivery is recoverable. No test success, reviewer receipt or archive hash substitutes for semantic acceptance.

## 5. Future execution and evidence discipline

After owner acceptance/commission only, first complete L00/L01 and bind exact implementation authority. Use the repository's existing isolation method; do not create extra worktrees or install an environment solely because a generic skill suggests it.

Each implementation leaf must identify its exact files, approved input/output interface, independent expected oracle, two physical cases, strict claim/immutable generation and affected predecessor contracts before coding. Do not infer claim names from directory names. Future strict command template:

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate <exact-admitted-owning-claim>
```

The placeholder must be resolved to the actual approved claim in the leaf evidence before execution. Record the candidate SHA, command, environment, full output, collection count, exit status and independent semantic disposition. Existing signal profile proof expects exactly its admitted success/refusal pair, exit0 and no skips; a helper-only contract claim follows its separately approved explicit family allocation. Do not reseal or overwrite old immutable generations.

Fresh reviewer judgement is independent of worker convenience fixtures. For ordering, omissions or transitions, the reviewer must inspect/decompose the relevant fixture and use the bounded authority-derived public sequence required by current AGENTS, within the approved case allocation. A new independent witness is not permission for unbounded extra product cases. Inspect relevant prior return/repair lineage; classify recurrent findings and close the common invariant. Missing class-level authority is a blocker, not an open-ended patch instruction.

Before accepting a leaf, assess whether its shared edits materially invalidate any accepted leaf or unchanged M00 proposition. Stop dependent advancement until that exact obligation is reaccepted. Do not repeat unrelated green proof because of a new session, packaging or a checkpoint restore.

## 6. Mandatory cumulative checkpoint after every accepted leaf

The checkpoint is part of leaf completion, not an optional final-task export.

1. Finish the semantic obligation, retain failures/repairs and obtain independent disposition. Commit exact source, tests, authority, evidence and actual plan progress. Do not rewrite/prune history or overwrite earlier proof generations.
2. Create `NVDA_DOWNSTREAM_RECONCILIATION_<LEAF>_<YYYYMMDD>_FULL_HISTORY.bundle` with `git bundle create ... --all`. Retain all starting refs/tips and new work. The checkpoint is cumulative: it contains all accepted earlier leaves, all preserved history and the current accepted leaf.
3. Verify bundle integrity, fresh-clone restoration, exact accepted HEAD, `git fsck --full`, L06/D143 ancestry and preservation of original ref-tip objects. This is packaging verification, not product testing. Record source SHA and verification outside the bundle to avoid self-reference.
4. Package `NVDA_DOWNSTREAM_RECONCILIATION_<LEAF>_CHECKPOINT_<YYYYMMDD>.tar.gz` containing the bundle, root plan, preserved plans, exact authority/oracle/input references or bytes, leaf evidence, complete prior checkpoint index, checksums and restore instructions. Hash archive and bundle separately; never include transient lockfiles or an archive inside itself.
5. Save the archive durably and expose its working downloadable link to the owner BEFORE beginning another leaf. A local scratch file or unsaved link alone does not satisfy this requirement. Record filename, accepted source SHA, hashes and returned durable file identity in the delivery ledger; include the receipt in the next cumulative checkpoint to avoid self-hash cycles.
6. Keep every earlier checkpoint. Once execution is commissioned, continue after each successful checkpoint without routine reapproval. If packaging/saving fails, preserve the accepted source and stop advancement until a downloadable cumulative checkpoint exists.
7. After sandbox loss, restore the latest durably saved checkpoint, verify its manifest/hash/HEAD/ancestry and resume at the first uncompleted obligation. Reuse valid proof; do not rerun tests solely to restore confidence after recovery.

A first reviewed planning delivery is documentary only and is not L00 execution acceptance. Every future leaf receipt must state ACCEPTED / BLOCKED / FAILED / NOT_ATTEMPTED accurately. If interrupted mid-leaf, an additional clearly labelled UNACCEPTED recovery snapshot may be saved without advancing that leaf.

## 7. Planning review, progress and completion ledger

- [x] Owner's planning-only instruction and no-test boundary recorded.
- [x] Completed M00 root plan preserved; D143 schedule and D145 pause retained.
- [x] Identified impact mapped to G0–G5 and individually reviewable leaves; module-local proof and cumulative checkpoint protocol specified.
- [x] Documentary self-review checked coverage, dependencies, authority boundaries, case allocation and absence of implicit execution approval.
- [ ] Independent documentary plan review, if commissioned, recorded with exact reviewed plan hash. No such approval is asserted by this draft.
- [x] Owner accepted the plan and commissioned completion on 28 October 2026; exact conditional mathematical/time decisions remain subject to the accepted boundaries.

Execution ledger: L00 independently accepted as documentary work; L01–L14 NOT_ATTEMPTED. No product tests or implementation have been run under this plan. Planning delivery location and hash are recorded by the accompanying saved-file receipt.

Final status may become COMPLETED only when §4 and §6 acceptance conditions are supported. Partial source compatibility, documentary dispositions, preserved legacy PASS evidence, numerical coincidence and archive creation alone cannot close the mandatory implementation gates.

## 8. Live execution ledger

Commission recorded at planning commit 2f93370. Ruling: correct mechanical historical-reference shifts introduced during leaf renumbering: the completed M00 anchor is L06, final review evidence/L06, outputs/L05_verified. Exact historical bytes and starting SHA remain unchanged. No product/proof change.

Preflight: L02 receipt/control types feed every native-compatible book profile; L03 quote assembly feeds actual D087 used by L04; L05/L06 feed actual D136; L09 source handling feeds L10. Shared edits require exact per-leaf invalidation assessment. Current branch is a task-private clone; no extra worktree or broad baseline run.

L00 ACCEPTED — documentary candidate c492bcba34ac8c9e3ece8631181e271f3fcd4736 independently passed spec/quality review d18a3a6de4daab3e6a9c913b35d7a43449972b41. I01–I08, source/profile versus regression distinction, exact callers/claims, shared-helper and proof-loader coupling, scoped descendant mapping and evidence reuse recorded in L00/BASELINE_AND_IMPACT.md. No tests/imports/runtime probes. Cumulative packaging/save/exposure receipt follows outside source commit.
