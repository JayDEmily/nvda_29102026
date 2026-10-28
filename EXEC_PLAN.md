# M00 downstream contract reconciliation — ExecPlan

Date: 28 October 2026, Australia/Melbourne. Plan ID `M00-DOWNSTREAM-RECONCILIATION-PLAN-1`, accepted revision `R2-DEFERRED-TESTING-ADDITIVE-BUNDLES`.

**Status: OWNER-AUTHORISED AND EXECUTION COMMISSIONED — 28 October 2026.** On 28 October 2026 the owner directed (i) deferral of all product/runtime/static test execution until implementation is complete and (ii) manual iPhone transfer of the latest **cumulative additive Git bundle** between implementation and independent tester threads, with GitHub/Codex excluded. This revision is installed after restoring and inspecting the accepted L00 full-history checkpoint, at `97f944d51ab9e403250fe76910e2754b50425c73`. The current owner explicitly commissioned execution. Only prospective testing sequence and transfer method change; earlier L00 review remains historical evidence and no L01 or later implementation is implied by plan installation.

**Goal:** Reconcile the identified downstream source contracts, owning code and module-scoped tests with the completed M00 native-shaped synthetic output, while preserving prior controlled evidence and every unrelated hold.

**Architecture:** M00 owns immutable raw observations, projections and control discoverability. M02 owns neutral calculation input selection, book reconstruction, quote assembly, derived results and their durable lineage. Each module is proved within its own span against an explicit public input contract. There is no proposed M00→M01→M02 end-to-end test suite, automatic M01 activation or application composition.

**Tech stack:** Retain the accepted CPython 3.12.14 environment and pinned dependencies: pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11, PyYAML 6.0.3; accepted prior SQLite evidence records 3.53.1. Execution must record its actual environment rather than infer it from this plan. Do not substitute Python 3.13 or install PostgreSQL.

**Specification and authority:** Current owner request to write this plan, the preceding static impact review, frozen `GUARDRAILS.md`, applicable agent instructions, architecture ownership/dependency law, the preserved M00 Brief2 and existing accepted calculation authority. The static review identifies reconciliation work; it does not supply new mathematical definitions, numeric policies or implementation authority. Exact changes to source profiles, temporal bases, public carriers and acceptance cases must be resolved in G1 before their implementation.

**Revised execution method:** one dependency-ordered implementation leaf at a time; author but **do not execute** its bounded module-local proof cases. Deliver a verified, cumulative **post-baseline additive** bundle after every leaf, not a repeated full-history bundle or tarball. A separate independent tester runs the relevant authorised module-scoped strict proofs, scoped static checks and review **only at L14**, after L02–L13 are implementation-complete or explicitly blocked. No early leaf can acquire test-backed acceptance under this amendment. The owner-approved change alters scheduling and transfer only, not source mathematics, proof content or required coverage.

## 1. Starting state, preserved plans and commission boundary

Starting accepted M00 checkpoint: `9b400183f275c3147b568d21b995b4aebd2af3c3` (completed M00 Brief2 L06). Previous signal anchor: D143 `17d7553cf3ad92700f849f696134de67b64b0dfa`.

The supplied full-history L00 checkpoint was restored and inspected: branch `work/downstream-reconciliation-20261028`, commit `97f944d51ab9e403250fe76910e2754b50425c73`; L00 independent review is recorded in `handoff/downstream_reconciliation/L00/INDEPENDENT_REVIEW.md` and the root plan history. No accepted L01 or later checkpoint was observed in the available primary Git state. The candidate fixed additive baseline is this exact L00 commit. Its full-history archive, bundle digest and ref inventory are recorded in `handoff/downstream_reconciliation/TRANSFER_BASELINE.md`. **Independent tester possession of the same baseline has not yet been observed;** the one-time baseline archive must be transferred and checked there before treating any additive bundle as usable. This is an explicit pending transfer invariant, not a code/proof failure.

The completed M00 root plan is preserved byte-identically at `handoff/planning/m00_downstream_reconciliation_20261028/COMPLETED_M00_BRIEF2_EXEC_PLAN.md` and in the starting commit. Its completion and evidence are retained. The earlier next-twenty plan remains PAUSED at `handoff/planning/m00_brief2_20261027/PAUSED_NEXT20_EXEC_PLAN_AT_D143.md`; D145 is its outstanding scheduled signal. Neither plan automatically resumes.

Root `EXEC_PLAN.md` is the single proposed successor planning entry point. Its execution role begins only after explicit owner acceptance and commissioning. The completed plan's active scheduling role is `DO_NOT_CARRY_FORWARD`; its bytes, source, fixtures, evidence and full Git history are retained. Earlier AGENTS/test-map execution wording describes prior commissions and does not authorise new implementation in this planning pass. At the inspected D143 anchor, root `AGENTS.md` and `tests/AGENTS.override.md` also contain prior per-leaf reviewer/full-history-checkpoint instructions; the newer **explicit owner instruction** governs the conflicting prospective test schedule and additive handover. Before installing this revision, inspect the *current* scoped AGENTS files and reconcile any live mismatch without weakening tests or making unauthorised governance edits.

The former documentary-only plan-amendment restriction applied to creation of the standalone draft, not the owner-commissioned execution that follows. During implementation L01–L13, apply §3.9 and §5: **do not execute product tests, replay, import/runtime probes or static analysis**. Git/hash/bundle verification remains permitted. L00's prior independent documentary review remains valid for its exact reviewed state; all newly authored code/proofs remain untested until L14.

D145 remains paused throughout this reconciliation plan. L13 produces an explicit source/time disposition and a bounded successor proposal, not a D145 implementation. Any implementation or changed mathematical/time policy needs its own accepted authority. All other holds, including D120–D122 and D141/D142/D144, remain in force.

## 2. Evidence basis and scope of the identified impact

The prior static pass compared D143 to L07 and inspected the relevant public contracts, consumer code, fixtures, paused plan and review records. The implementation delta in `src/` is confined to M00's `_native_codec.py` and `api.py`: additive UTC-datetime encoding and observation-history enumeration. M01/M02 production files and existing signal product tests were unchanged by Brief2. New M00 proof and shared proof-control support were also added.

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
9. **No tests during implementation leaves L02–L13:** no product proof gate, pytest, runtime readback, test execution, static analyser, replay, smoke test or unaffected regression. Workers may inspect/author versioned tests, fixtures, oracles and proof admissions under existing authority but must mark them **NOT_RUN**. They may perform documentary source review and Git/hash/bundle integrity operations, which are not claims of product correctness. At L14, a **separate independent tester** is the sole strict product-proof executor. Preserve existing valid cases, original evidence and immutable generations; avoid routine RED/duplicate GREEN, broad suites and unaffected regression. Failure repetitions follow documented material repairs only.
10. Reuse accepted M00 37-case, original SQLite compatibility and reproducibility evidence only where its source/proposition remains unchanged. This is prior evidence, not a new run. Source edits require a scoped invalidation assessment before proceeding.
11. Scoped static checks and all strict product gates occur **only in L14**, after implementation reaches a stable candidate HEAD and the tester restores it. No implementation checkpoint is represented as tested or accepted; retain the pinned environment. No PostgreSQL server, live IBKR calls, production entitlement claims, catalogue-wide rewrite, A00 composition or unrelated module work.
12. Stop dependent work at the first missing authority or failed invariant. A documentary blocker disposition is not an implemented capability or a completed mandatory runtime leaf.

Review focus allocated to future proof: side inversion and asymmetric expected results (L05–L10); receipt-only exclusion under event filtering (L02–L11); hidden reset/restart and incomplete re-warm-up (L02–L11); subscribed-book position shifts across MPIDs (L11); asynchronous quote identity/skew/age and missing constituents (L03/L12). Ambiguous receipt/sequence ties and generation boundaries belong in the accepted source contract and must not be hidden by convenient fixtures.

## 4. Gates, leaves and dependency order

Retain the established G0–G5 gates and L00–L14 semantic leaves, their owners and dependencies. **G0/G1 are authority/documentary readiness boundaries, not test gates. G2/G3/G4 are provisional implementation milestones only; formal product-proof acceptance is withheld until G5/L14.** A worker self-review or a valid additive bundle never promotes a provisional leaf. Leaf numbering is local to this plan and does not replace M00 Brief2's completed L00–L06.

| Gate | Acceptance boundary | Leaves |
| --- | --- | --- |
| G0 | Documentary evidence and impact inventory approved; no product tests | L00 |
| G1 | Required source contracts, authorisations, oracles and proof allocations fixed **before implementation**; no product tests | L01 |
| G2 | M02 receipt/control and option-quote implementations prepared, **UNTESTED** | L02–L03 |
| G3 | SMART/direct-book implementations prepared, **UNTESTED** | L04–L11 |
| G4 | Microprice implementation prepared, **UNTESTED**; D145 documentary disposition recorded | L12–L13 |
| G5 | Independent tester performs all applicable module-scoped strict proofs and static checks, repairs are verified, earlier provisional leaves are dispositioned, final cumulative additive bundle delivered | L14 |

Execution dependencies: L00 → L01 → L02 → L03. L04 requires L03's actual compatible D087; L05 → L06 → L07 covers bid/ask predecessors and imbalance. L08 requires actual compatible D011. L09 → L10 covers insertion/deletion source reuse. L11 requires L01/L02. L12 uses L03's approved quote assembly contract without adding D087 as a mathematical predecessor. L13 requires the resolved temporal/control contract. L14 requires all mandatory implementation leaves and the explicit L13 disposition.

Default traversal is L00→L13 for documentary contracts and implementation, followed by **all test execution and independent acceptance in L14**. Work one implementation leaf at a time; any order change must preserve actual dependencies and be documented. The next leaf may begin after (a) its authority and source prerequisites are established, (b) the preceding leaf's implementation is committed as **IMPLEMENTED_UNTESTED** or explicitly BLOCKED, and (c) its latest cumulative additive bundle is saved and downloadable. A later tester may return a finding affecting multiple earlier leaves; handle it as bounded repair with the same fixed baseline and a new additive bundle.

**Status vocabulary:** `AUTHORITY_READY`, `IMPLEMENTED_UNTESTED`, `DOCUMENTARY_DISPOSITION`, `BLOCKED`, `RETURNED_FOR_REPAIR`, `TESTED_ACCEPTED` and `NOT_ATTEMPTED`. Only L14 can confer `TESTED_ACCEPTED` on implementation leaves; no leaf is labelled independently accepted on the strength of coding or packaging alone. All tests remain prepared-but-unexecuted until L14. The §6 checkpoint protocol applies after each leaf, including documentary leaves and repair cycles.

### G0 / L00 — freeze the impact boundary and evidence reuse

**Files:** create `handoff/downstream_reconciliation/L00/BASELINE_AND_IMPACT.md`; read the primary paths in §2. No product change in this leaf.

- [x] Read governing files and relevant source/authority in full where conclusions depend on them; record exact starting commit and full/partial coverage.
- [x] Re-derive I01–I08 from source, including the purpose and authority of each legacy synthetic convention. Distinguish an old limited proof from an invalid claim of native compatibility.
- [x] Enumerate affected callers, public protocols, codecs, owning tests/claims, predecessors and direct dependants. Record D136's D134/D135 dependence and D131's D087 dependence. Trace further dependants only where an affected output contract actually propagates; no blanket invalidation.
- [x] Classify unchanged evidence and precisely invalidated propositions. Record that the datetime fix already exists and that PostgreSQL's separate codec is a deferred backend issue, not an instruction to repair it here.
- [x] Account for shared proof-loader M00-extension validation as a governance/build prerequisite. Preserve valid admissions; propose G01 changes only if an actual control defect is identified.
- [x] Preserve the original independently reviewed L00 inventory (candidate `c492bcba34ac8c9e3ece8631181e271f3fcd4736`, review `d18a3a6de4daab3e6a9c913b35d7a43449972b41`, baseline `97f944d51ab9e403250fe76910e2754b50425c73`); original full-history L00 checkpoint was already created and downloaded. Reserve all **new** implementation test acceptance for L14.

**Acceptance:** exact affected/unaffected/unknown inventory and reusable evidence ledger exist; no tests are run merely to establish the inventory.

### G1 / L01 — approve consumer source contracts and proof allocation

**Files:** create `handoff/downstream_reconciliation/authority/CONSUMER_SOURCE_CONTRACT_V1.md`, `PROFILE_AND_PROOF_ALLOCATION.md`, independently authored `fixtures/` and `expected/` under this handoff; proposed bindings/claim deltas remain documentary until authorised.

- [x] Specify exact per-profile provider/variant, subject/right, request/exchange, generation, mapping IDs/versions, units, side interpretation, receipt window, cutoff, completeness and identity eligibility. Treat M00's immutable A/B/C examples as separate source scenarios.
- [x] Specify an additive M02 raw/control reader contract using the existing public `list_projected_raw_history(...)` and `list_raw_observation_history(...)`. Copy exact signatures/types from M00 at the execution anchor; no imagined selector API or private database enumeration.
- [x] Specify ordered merging of projected mutations and separately discovered controls, G1 outgoing/G2 incoming restart discovery, invalidation policy for error/reset/gap/reconnect, explicit re-warm-up criteria, and refusal for unresolved causal ties. Control policy belongs to M02 and must identify its accepted authority.
- [x] Specify typed receipt/event basis in lineage and owner-local durable decoding. Preserve absent provider time and legacy carrier compatibility; do not weaken the original Decimal-only selector globally.
- [x] Specify direct positions per subscribed book side, source exchange distinct from MPID, and the exact grouping/depth scope for concentration. Specify asynchronous quote membership, selection time, skew/age bounds and lineage. The brief's 250 ms / 1000 ms examples are synthetic candidates, not approved production policy.
- [x] Publish independent numerical oracles and two-case allocations per affected D/profile. Resolve the six-case ceiling and legacy retention explicitly before implementation; retain the original top-one D135 incompatibility refusal for D136 unless an exact replacement is authorised.
- [x] Identify each semantic change needing owner acceptance: new temporal/source profiles, quote assembly policy/domain, direct grouping scope, public carrier/codec additions, new proof admission and any D145 time-basis revision. Obtain exact required approval and lawful ingress binding before dependent code.
- [ ] Obtain required **owner/normative** contract and oracle authorisation before code, document a self-audit, commit and export an additive checkpoint. Contract authorisation/self-audit are recorded; only controller export/save/exposure remains pending at this commit. Defer independent tester review to L14. If authority is absent, publish the blocked contract proposal and stop dependent leaves; neither self-review nor later tests may create missing owner authority.

**L01 current disposition: AUTHORITY_READY / NOT_RUN.** Current owner commission resolves bounded synthetic A01–A04 compatibility design; exact source/API/fixture/oracle/allocation/brief/binding components are committed under `handoff/downstream_reconciliation/authority/`. Independent meaning review and all proof execution remain L14. Checkpoint mechanics and exposure are recorded separately by controller; no test-backed acceptance is implied. D145 remains paused.

**G1 documentary readiness:** no implementation-relevant source/policy/interface ambiguity remains for work that proceeds; normative approval must precede code, while independent tester review is reserved for L14. No test-backed acceptance is asserted.

### G2 / L02 — additive M02 receipt/control input and durable lineage

**Files:** proposed additive public types/protocols in `src/nvda_desk/market_measurement_truth/api.py`; focused owner-local source/control helper and codec support only if L01 requires them; exact proof files/claim fixed by L01. Preserve `_selection.py` legacy numeric behaviour.

- [x] Author the admitted module-local proof from L01 before production changes: separate control discovery, receipt-only input selection with null event cutoff, strict source isolation, deterministic pagination and typed durable lineage.
- [x] Implement the approved public input protocol and bounded M02 interpretation of controls. Merge events under declared order; refuse ambiguous required transitions and incomplete generation restart state.
- [x] Implement approved typed receipt basis without fabricating event datetimes. Preserve original projections in lineage and version changes; keep old persisted records readable under their original owner/profile.
- [x] Implement the public owner/readback path and author its ordinary read-only SQLite and independent literal omission/order/control checks under the declared case allocation; **do not execute** them before L14.
- [ ] Document the affected claims and **NOT_RUN** proof obligations; commit as `IMPLEMENTED_UNTESTED` and publish the additive checkpoint. Source/claim/ledger are prepared; controller commit/export/save/exposure remain pending at this working-tree revision. Independent semantic review and scoped strict proof occur at L14.

**L02 implementation disposition: IMPLEMENTED_UNTESTED; all scoped source/static/runtime proofs NOT_RUN.** See `handoff/downstream_reconciliation/L02/STATUS.md` and next-export manifest. The export/save/exposure itself is controller-pending at this commit.

**Required L14 proof (not established by implementation checkpoint):** M02 has a lawful input/lineage capability for native-shaped receipt/control facts. No new M00 API or M00 proof run is presumed necessary. If common semantics require per-family carriers, keep them bounded and bind each dependent leaf explicitly.

### G2 / L03 — D087 asynchronous option quote selection

**Files:** `_option_scalars.py`, additive owner-local assembly/carriers/codec where L01 authorises them, `tests/product/market_measurement_d087/test_signal.py`, owning profile/claim.

- [ ] Preserve the old timestamped synthetic snapshot profile. Introduce only the separately authorised receipt-based option profile with explicit membership, right, request, generation, age/skew and cutoff policy.
- [ ] Select four-callback A2/A3 constituent identities as applicable without manufacturing a shared native occurrence. For coherent C1/A2 reference context, bid1.20 and ask1.40 give midpoint1.30 with both exact source lineages.
- [ ] Publish exact approved selection/oracle/refusal before code; author the two-case profile using the agreed missing/stale/mismatched constituent refusal. No assumed production authority for example250ms/1000ms thresholds.
- [ ] Implement full constituent identity/assembly policy/version and durable lineage/readback paths. Author but do not run proof. Commit `IMPLEMENTED_UNTESTED`, export the additive checkpoint, then permit L04 development; L14 tests both.

**Required L14 proof (not established by implementation checkpoint):** actual public D087 can supply the newly approved coherent option profile without inventing an event timestamp or atomic callback. If quote-policy authority is absent, L03 and L04 remain BLOCKED.

### G3 / L04 — D131 option depth band, after compatible D087

**Files:** `_book_depth.py`, relevant M02 public types/codec, `tests/product/market_measurement_d131/test_signal.py`, exact owning authority/admission/generation.

- [ ] After L03, materialise actual compatible public D087 for the selected coherent option profile; keep legacy midpoint100 separate from coherent midpoint1.30.
- [ ] Author the approved success/refusal pair: coherent C1 has midpoint1.30, inclusive half-dollar band0.80–1.80, sizes5+3=8 contracts; outside bid0.70 size7 is excluded. Oracle is independently specified, not a hard-coded calculation substitute.
- [ ] Reconcile side, receipt selection, separate controls and complete positional replay; refuse reset/discontinuity without required fresh warm-up. Preserve exact predecessor, raw and configuration lineage.
- [ ] Preserve still-valid legacy proof as separately scoped evidence; prepare changed proof `NOT_RUN`, commit `IMPLEMENTED_UNTESTED` and publish the additive checkpoint. Defer independent review and warranted strict execution to L14.

**Required L14 proof (not established by implementation checkpoint):** exact band depth and reached refusal supported by M02-local proof using actual compatible D087; no cross-scenario quote mixing or fabricated predecessor.

### G3 / L05 — D134 native-compatible SMART bid depth

**Files:** `_smart_depth.py`, relevant public types/codec, `tests/product/market_measurement_d134/test_signal.py`, owning profile/claim.

- [ ] Author the approved two-case profile using native bid side1 and ask side0, receipt-only fields and explicit source/generation. A4 bid sizes5/3 yield8 shares.
- [ ] Preserve four mandatory R roles; do not add price as a new mathematical dependency. Reconcile controls and positional warm-up through L02. Preserve/reach the missing-operation refusal with other fields visible.
- [ ] Implement minimal owner changes and prepare the strict success/refusal pair and durable readback assertions without executing them; commit `IMPLEMENTED_UNTESTED` and checkpoint. L14 performs independent review/proof.

**Required L14 proof (not established by implementation checkpoint):** native bid selection and exact result8, plus reached refusal, retain full typed source/time/control lineage.

### G3 / L06 — D135 native-compatible SMART ask profiles

**Files:** `_smart_ask.py` and its lawful shared owner-local helper, public types/codec, `tests/product/market_measurement_d135/test_signal.py`, owning profiles/claim.

- [ ] Reconcile approved top-two and top-one profiles without overwriting old definition/parameter/selection identities. Native ask side0 sizes2/4 yield top-two6 and top-one2 shares.
- [ ] Author the allocated success/refusal pair with a separate reset control after warm-up; no synthetic native operation317. Preserve any still-valid legacy cases within L01's approved count allocation.
- [ ] Reuse L05's versioned **implemented but untested** semantics as a development dependency; prepare the necessary affected readback/proof checks, without executing. Commit `IMPLEMENTED_UNTESTED`, checkpoint; L14 tests both L05/L06 and any interaction.

**Required L14 proof (not established by implementation checkpoint):** both explicitly approved depth profiles preserve their exact meaning and reset refusal; shared-source changes do not silently invalidate L05.

### G3 / L07 — D136 compatible actual bid/ask predecessors

**Files:** `_smart_imbalance.py`, `tests/product/market_measurement_d136/test_signal.py`, owning profile/claim; code changes only if required by the revised predecessor contract.

- [ ] Materialise actual public compatible L05/L06 predecessors: bid8 and ask6 yield exact1/7. Preserve both identities and matching source/generation/time/level context.
- [ ] Preserve the reached refusal with actual top-one D135 ask2 against the unchanged common-top-two request. Do not fabricate a predecessor or change only the requested depth.
- [ ] Amend lineage/version handling only where the contract changed; keep the equation unchanged. Prepare independent semantic/strict proof and readback for L14 without running them; commit `IMPLEMENTED_UNTESTED` and checkpoint.

**Required L14 proof (not established by implementation checkpoint):** revised source meaning propagates correctly through actual predecessors; no stale inherited acceptance by numeric coincidence.

### G3 / L08 — D138 side-specific book slopes

**Files:** `_book_slope.py`, relevant public carriers/codec, `tests/product/market_measurement_d138/test_signal.py`, owning profile/claim and accepted D138 overlay.

- [ ] Define the approved receipt-only three-level source fixture and actual compatible public D011 midpoint. Preserve K06, P_REGRESSION, units and equation; source reconciliation is not mathematical redefinition.
- [ ] Use native side1 bids and side0 asks, correct ladders, complete pre-selection book and separate control invalidation. Independent oracle retains bid slope7/2 and ask slope5/2 for its explicitly bound controlled fixture.
- [ ] Author the allocated success and reset-without-warm-up refusal; preserve all five projected roles and typed provenance. Commit `IMPLEMENTED_UNTESTED` and additive checkpoint; defer independent review, strict proof and readback execution to L14.

**Required L14 proof (not established by implementation checkpoint):** bid/ask outputs cannot be silently swapped; actual midpoint and revised input/control semantics are proved.

### G3 / L09 — D139 collector-receipt insertion rate

**Files:** `_book_insert_rate.py`, relevant public request/lineage/codec, `tests/product/market_measurement_d139/test_signal.py`, owning profile/claim.

- [ ] Keep the accepted four-second R001 receipt bucket and bid positions1–2 policy unless separately amended. Specify native bid side1 and genuine collector-added R001 equal to envelope receipt, with absent provider event time.
- [ ] Author success: selected inserts sizes3/5 yield count1/2 events/s and size2 shares/s. Preserve the visible missing-operation refusal and exact pre-window warm-up.
- [ ] Remove unsupported true-instant dependency only in the new approved profile; process separate controls through L02 and preserve the original raw metadata. Reuse M00's existing datetime persistence evidence rather than repairing its codec again.
- [ ] Prepare typed durable readback and strict case assertions `NOT_RUN`; commit `IMPLEMENTED_UNTESTED` and additive checkpoint. Independent review and execution are deferred to L14.

**Required L14 proof (not established by implementation checkpoint):** rates depend on the declared receipt clock, never a fabricated source timestamp; original native and collector provenance remain distinct.

### G3 / L10 — D140 collector-receipt deletion rate

**Files:** `_book_delete_rate.py`, its lawful L09 source helper, public types/codec, `tests/product/market_measurement_d140/test_signal.py`, owning profile/claim.

- [ ] Preserve the two-second receipt bucket, bid positions1–2 and actual pre-delete size semantics under the native-compatible side/source contract.
- [ ] Author success: native deletion size0 removes actual standing size6, giving count1/2 events/s and removed size3 shares/s. The refusal addresses a nonexistent standing position; no invented zero removal.
- [ ] Preserve warm-up, separate controls, typed R001 provenance and implement exact SQLite readback; author but do not run its proof. Commit `IMPLEMENTED_UNTESTED` and checkpoint; independent semantic/strict proof at L14.

**Required L14 proof (not established by implementation checkpoint):** deletion consumes pre-delete standing state under the revised input contract, with no accidental reinterpretation of native zero size as removed quantity.

### G3 / L11 — D143 subscribed direct book and qualified concentration

**Files:** `_direct_venue.py`, direct request/row/lineage types in `api.py` and codec as required, `tests/product/market_measurement_d143/test_signal.py`, owning profile/claim.

- [ ] Reconstruct one selected subscribed book per side, applying positions across MPIDs; retain requested exchange independently from MPID, native side and per-callback occurrence.
- [ ] Group reconstructed rows only after positional replay, under L01's exact approved concentration scope. Do not treat MPID as an unqualified exchange or restart positions per MPID.
- [ ] Define the approved success fixture using C2-compatible rows: ALPHA4+2 and BETA1+1 give grouped quantities6/2; if the accepted scope includes those complete rows, independent shares3/4,1/4 and HHI5/8 follow. This scope must be authorised before changing legacy per-venue-top-one semantics.
- [ ] Preserve reached missing-MPID refusal with size still visible; include required cross-MPID position mutation evidence within the authorised pair rather than an unbounded scenario loop. C3 CALL remains a conditional source specimen, not a direct-feed entitlement or PUT coverage claim.
- [ ] Reconcile receipt/control inputs and implement the durable readback/proof assertions without executing. Commit `IMPLEMENTED_UNTESTED` and checkpoint; L14 runs independent scoped proof.

**Required L14 proof (not established by implementation checkpoint):** subscribed-book addressing, qualified source identities and exact grouping scope are independently established; same HHI does not mask a different book model.

### G4 / L12 — D137 coherent quote domains and assembly

**Files:** `_microprice.py`, approved quote carriers/helper, `tests/product/market_measurement_d137/test_signal.py`, owning profile/claim.

- [ ] Preserve lawful atomic shares co-reference and original stock microprice201/2. The existing single-occurrence rule remains meaningful for that exact profile.
- [ ] For a separately authorised asynchronous option extension, use L03's approved assembly contract without adding D087 as a mathematical predecessor. Preserve four independent callback identities, receipt windows and complete lineage.
- [ ] Bind exact independent option microprice oracle and reached refusal to the approved fixture/case allocation before implementation; retain denominator-zero law and refuse incomplete/mismatched assembly without fusing raw observations.
- [ ] Prepare the approved profiles and durable readback assertions `NOT_RUN`; commit `IMPLEMENTED_UNTESTED` and checkpoint. If option-domain extension lacks authority, record `BLOCKED` without claiming completion. Independent review and strict proof occur in L14.

**Required L14 proof (not established by implementation checkpoint):** each authorised quote domain has correct co-reference or explicit derived assembly, mathematical output and absence semantics. A retained atomic stock proof does not certify asynchronous option consumption.

### G4 / L13 — D145 and held downstream work: documentary disposition

**Files:** create `handoff/downstream_reconciliation/L13/D145_RESUMPTION_DISPOSITION.md` and an explicit proposed paused-plan amendment; inspect the D138/D145 overlay and dependency traceability. No D145 product code/test/claim is created here.

- [ ] State the source conflict exactly: verified updateMktDepthL2 specimens lack provider event time; paused D145 requires an event-time one-second window with complete pre-window book and each intermediate transition.
- [ ] Recommend retaining that event-time profile as BLOCKED on a lawfully timestamped source, unless the owner explicitly approves a separately versioned receipt-clock synthetic profile. Do not silently change K17, collapse equal-time transitions or fabricate source time.
- [ ] Define the exact evidence and authority needed for any successor D145 plan: native sides, position-based mutations, control invalidation, warm-up, chosen clock/window and full intermediate best-book states. No automatic D145 implementation or old-plan resumption follows.
- [ ] Trace actual affected downstream contracts without promoting historical graph counts into newly proved executable dependants. Keep D120–D122, D141/D142/D144 and other existing holds explicit; source fidelity alone does not resolve their missing policies/prerequisites.
- [ ] Record the documentary D145 disposition and publish the additive checkpoint without product tests. L14 independently reviews the disposition. D145 capability remains BLOCKED; documentary disposition cannot be described as its accepted execution.

**Acceptance:** precise resumption condition, owner decision boundary and retained holds are recorded. No arbitrary replacement clock or new deferral-by-convenience.

### G5 / L14 — all independent testing, repair, retrospective acceptance and final additive handover

**Files:** `handoff/downstream_reconciliation/FINAL_REPORT.md`, final tester evidence/index, per-leaf and per-claim dispositions, original failure/repair lineage; update this root plan's verified ledger. **Implementation must have reached a stable candidate HEAD before any test is executed.**

- [ ] **Handover:** restore the fixed full-history baseline plus the most recent cumulative additive bundle in the independent tester thread. Confirm the baseline SHA, bundle prerequisite/base, source HEAD and complete changed-file/ref inventory by Git integrity/readback checks; hashes alone do not prove functionality. Identify any missing reference assets before the affected proofs.
- [ ] **Independent pre-test review:** inspect accepted authority, changed owning code, proof claims, exact source/profile/oracle allocation, fixtures and failure/refusal conditions for **every** mandatory L02–L12 leaf (including retained old cases and shared helpers). Review fixture independence for ordering, missing operations and state transitions; trace relevant historical return/repair lineage. Do not mistake the worker-authored test for an independent oracle.
- [ ] **Scoped static checks:** execute the necessary pinned mypy/Ruff and import/ingress/schema preflight checks for the actually affected modules and proof interfaces; preserve commands, input SHA, environment, output and status. Do not infer a clean system from absent checks.
- [ ] **Module-by-module strict proof:** run the approved aggregate for each affected owner/profile **only here**, with one independent tester acting as sole strict executor; do not create a new M00→M01→M02 end-to-end suite or run unrelated historical/broad regression. At minimum disposition L02 receipt/control, D087, D131, D134, D135, D136, D138, D139, D140, D143 and D137 and their required shared readback/source obligations. For ordinary signal profiles retain the exact approved success/refusal pair and existing six-case cap; helper-only claims obey their own authorised allocation. Record exact collected/passed/skipped counts, exit code, candidate SHA, source/proof generation and original output. Test actual public predecessors and ordinary read-only SQLite reopen where required.
- [ ] **Dependency-aware proof order:** start with L02's shared public source/control carrier; next D087→D131 and D134→D135→D136; then the other owners (D138, D139→D140, D143, D137). Re-evaluate shared-semantic invalidations across earlier leaves in this same final phase, without replacing owner-specific proofs with a cross-module smoke test. The order is subject to concrete approved dependency contracts rather than an unverified run schedule.
- [ ] **Failure/repair loop:** on any missing authority, failing invariant or test result, mark the affected leaf(s) `RETURNED_FOR_REPAIR` or `BLOCKED`, preserve failed output and exact candidate commit; stop dependent proofs, return a bounded defect/obligation to the implementation thread and receive a newly committed **cumulative additive** repair bundle against the unchanged baseline. Only rerun an unsuccessful proof after a documented material repair; rerun successful proofs only when a later repair materially invalidated them. Independent tester retains strict execution responsibility. Do not manufacture green by weakening, renaming, skipping, deleting or rewriting valid tests/claims or immutable generations.
- [ ] **Retrospective acceptance:** for **every** L02–L12 leaf, record `TESTED_ACCEPTED`, `RETURNED_FOR_REPAIR`, `BLOCKED`, or `NOT_ATTEMPTED` with claim-level evidence, source SHA, and final tester determination. G2/G3/G4 become formally accepted only if all their mandatory authorised obligations qualify. Independently review L00/L01 authority and L13's D145 documentary disposition without running D145 product tests or automatically lifting holds.
- [ ] **Final coverage:** reconcile I01–I08, old and new source profiles, valid prior evidence, M00 immutable artefacts, SQLite scope, PostgreSQL/backend deferral, original holds (including D120–D122, D141/D142/D144/D145) and any still-unresolved proof/invalidation. Explicitly identify incomplete items; a partial/test-failed outcome is not FULL COMPLETION.
- [ ] **Final handover:** commit actual reviewed evidence, tester disposition, repaired source and plan ledger. Export, verify and expose the latest **cumulative additive** bundle against the fixed baseline (not a full-history tarball). Include the handover/manifest **in Git**, with base/HEAD/ref inventory, SHA-256 sidecar reported alongside the downloadable bundle, restore command and complete status. No GitHub/Codex dependency.

**Final gate acceptance:** the independent tester has exercised and recorded the exact authorised owning module proofs and scoped checks for all required leaves; all mandatory obligations are `TESTED_ACCEPTED`; failures and invalidations are closed or explicitly left unresolved; documentary holds remain visible; and the final cumulative additive Git bundle restores correctly on the shared baseline. A clean Git bundle, a documentary review or an old proof is not a substitute for new execution where a changed contract invalidated it.

## 5. Revised two-thread execution and evidence discipline

**Execution split:**

1. **Implementation thread — L00–L13 only.** Read current authorities and active working state; obtain owner/normative approval at G1 where required. Implement each affected owning module and prepare its exact versioned tests, synthetic fixtures, independent literal expected values, proof claim/immutable generation and durable readback assertions, but **execute none of them**. No pytest, strict product gate, mypy, Ruff, product replay, runtime probe, smoke or regression during these leaves. Source/documentary inspection and Git/cryptographic transfer-integrity operations are permitted and are not described as correctness tests.
2. **Provisional handover per leaf.** Commit the source/proof/documentary delta, record `IMPLEMENTED_UNTESTED` or `BLOCKED`, generate a fresh cumulative additive bundle (fixed baseline → current HEAD), verify its mechanics and provide the downloadable path. The implementation thread continues dependency-order work after checkpoint availability, not after independent testing. If a semantic authority prerequisite is missing, dependent code remains blocked; postponing testing is not permission to invent authority.
3. **Independent tester thread — L14 only.** Receives the identical fixed baseline once and then only the newest cumulative additive bundle. Inspects/executes the scoped product proofs and checks in §4/L14, reviews meaning independently, reports defects and exact evidence. The implementation worker may repair and return a new cumulative additive bundle; the tester retains proof execution. Repeat until every mandatory obligation has a disposition, not merely until a selected sample passes.

**Bounded proof contract retained:** exactly the existing authorised physical success/refusal allocation per signal/profile (two cases unless separately approved; absolute ceiling six per ID), independent oracle, actual M00 public source and actual public derived predecessor, exact typed lineage, refusal without results/history, ordinary SQLite read-only reopen, and immutable claim/generation rules. Writing these checks before implementation is permitted; **running** them before L14 is not. Where a profile or case cap requires owner approval, resolve this before coding, not by adding tests at the end.

**Independent reviewer standard:** the tester must not rely solely on worker convenience fixtures for sequences, omission or absence, and must inspect applicable previous returns/repairs and classify recurrence. One independent final semantic reviewer is the sole strict executor for the entire final test phase; don't run duplicate GREEN or broad unrelated suites. Strict command, once the exact owner-approved claim and environment are resolved in L14:

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate <exact-admitted-owning-claim>
```

Record candidate Git SHA, invoked command, environment, raw outputs, collection/pass/skip counts, exit status, exact claim, source and final disposition. A check failing before collection is still a failure, not a pass or omitted test. Invalidation is assessed per changed interface/helper; fix and retest only materially affected claims and any dependent proofs.

## 6. Cumulative **additive** bundle after every leaf and repair

A cumulative incremental Git bundle is **not** a self-contained full repository: it is self-contained **relative to one immutable baseline** present in both threads. This distinction is a mandatory recovery invariant, not optional documentation.

1. **Pin transfer baseline once.** At intake, use the *actual latest accepted full-state checkpoint shared by worker and tester*, not an inferred later state or D143 merely because it is attached. Record its complete SHA (`BASE_SHA`), exact archive filename and SHA-256, Git refs/tips and accepted source identity in `handoff/downstream_reconciliation/TRANSFER_BASELINE.md`. The historical completed M00 L06 `9b400183...` and D143 `17d7553...` remain ancestry/evidence pins only. If the current worker baseline cannot be inspected and matched at both ends, **do not claim a usable transfer**. A locally created additive bundle is conditionally restorable only until the independent tester demonstrates possession of the identical L00 full-history baseline. Do not silently rebase the baseline after a leaf.
2. **Commit every leaf.** Include governing plan revision, applicable authority/profile/oracle/fixture source, code/test source (unexecuted), exact ledger and restore manifest in ordinary Git commits. Do not strip earlier leaf commits or rewrite immutable history. Keep the current working repository clean before export. Status is `IMPLEMENTED_UNTESTED` (or documentary/blocked), never `TESTED_ACCEPTED` before L14.
3. **Create cumulative additive, not full history.** From the first post-baseline commit through current `HEAD`, export the complete *reachable post-baseline commit/object closure* and all relevant newly created/updated refs needed by the handover; exclude baseline Git history only after confirming that those objects and relevant original refs exist in the shared baseline. The primary export is `NVDA_DOWNSTREAM_RECONCILIATION_<LEAF>_<YYYYMMDD>_ADDITIVE_FROM_<BASE12>.bundle`. A typical single-work-branch command is:

   ```bash
   git bundle create "$OUT_BUNDLE" HEAD "^$BASE_SHA"
   ```

   The command is conditional on `BASE_SHA` being an ancestor of the exported `HEAD`; no force-push, history rewrite or full-history fallback is implied. If new independent refs or side branches need preserving, enumerate and export them explicitly and verify every required ref; a `HEAD`-only command is insufficient for those refs. If the current full Git state cannot be encoded in one additive bundle under the shared baseline, mark `BLOCKED` and document the missing prerequisite rather than falsely claiming complete export.
4. **Integrity checks (not product tests):** verify bundle prerequisites against the real baseline, confirm restore of **baseline + additive bundle** in a fresh temporary Git repository, verify HEAD and required refs/tips, `git fsck --full`, ancestry and exact committed file/tree hashes, and compute SHA-256 of the bundle. A bundle verification that succeeds *only* against the producer's repository is insufficient. Run no Python tests, product gates or static analysers in this stage.
5. **Delivery:** expose the single latest `.bundle` as a working download from the conversation for the user's iPhone; report separately in the response its filename, SHA-256, baseline SHA, HEAD SHA, included ref list and status. The receipt/checksum cannot be embedded in a bundle that already includes itself; store manifest data describing the next export in Git and report the actual resulting bundle hash externally. Do not require a GitHub repo, Codex, a zip of the whole repository or all intermediate leaf files for normal handover.
6. **Recovery:** tester restores exactly the pinned baseline and applies only the latest cumulative additive bundle. Each newer bundle replaces the earlier *transfer payload* and covers all changes since the same baseline, including repairs; it must not require intermediate additive bundles. Both threads retain accepted original history and source packages required for lawful development. The owner may retain previous downloads for contingency but is not required to shuttle them sequentially. If restore, SHA or ref checks fail, stop; do not substitute an unverified patch/snapshot and claim equivalence.
7. **End-of-testing:** the final accepted (or truthful partial/blocked) state is also delivered as one cumulative additive bundle using the exact same baseline and protocol. Full-history checkpoints remain historical evidence and may be retained at their original locations, but **are no longer generated each leaf** under this revision.

**Non-Git assets:** only tracked repository content is carried by `git bundle`. Any external PDFs, workbooks, original full-history baselines, dependency wheelhouse, or untracked fixture assets remain separate prerequisites and must be enumerated with exact hashes. Do not imply the additive bundle contains files merely attached to the ChatGPT Project; an asset needed for test execution must either be committed or identically available in the tester environment. Ensure neither thread's sandbox is the sole copy of essential source assets.

**Interrupted leaf:** permit an optional clearly marked `UNACCEPTED_RECOVERY` cumulative additive snapshot, but it cannot advance semantic status or conceal unfinished work. Packaging/transfer failure stops further implementation until an independently restorable download is available.

## 7. Amendment review, progress and completion ledger

- [x] Original plan's I01–I08 and semantic leaf definitions retained as amendment base.
- [x] Owner's 28 October instruction to put **all testing at the end** and use iPhone-transferred cumulative additive bundles recorded.
- [x] G0–G5 and L00–L14 retained; G2–G4 implementation statuses separated from G5 proof acceptance.
- [x] Original module-local two-case/strict-proof coverage retained, but execution moved to final tester phase.
- [x] Full-history-per-leaf checkpoint requirement replaced prospectively by one latest cumulative additive bundle from a fixed shared baseline.
- [x] Inspected complete L00 full-history checkpoint `97f944d51ab9e403250fe76910e2754b50425c73`, its acceptance report and original root plan. L01–L14 not accepted at that checkpoint; no later primary Git checkpoint was located in the accessible sources. A concurrent external worker newer than this state remains **UNKNOWN**.
- [ ] Confirm independent tester receives and verifies the identical L00 baseline. Producer-side baseline SHA/archive checksum/ref inventory is recorded in `handoff/downstream_reconciliation/TRANSFER_BASELINE.md`; no assertion yet about the tester's environment.
- [x] Install this R2 amendment as root `EXEC_PLAN.md` in an ordinary post-L00 commit and reconcile current root/test AGENTS instructions with the higher-priority owner's testing/transfer amendment.
- [ ] Independent documentary audit of this revision and, later, all L14 module-scoped test dispositions; never report these as performed in this pass.

**Current execution status:** L00 documentary inventory is previously reviewed; L01–L14 have no verified acceptance in the restored L00 checkpoint. Future concurrent worker changes, if any, are **UNKNOWN**. This amendment changes prospective test/transfer rules but does not certify new implementation, test or gate acceptance. `TESTED_ACCEPTED` is reserved for L14 evidence. D145 and other stated holds remain paused/unchanged. Final `COMPLETED` requires all authorised mandatory L14 dispositions plus a verified final cumulative additive transfer; otherwise report exact partial/blocked coverage.


## 8. R2 execution intake — observed repository state

- Restored primary source: L00 full-history archive and contained Git bundle listed in `handoff/downstream_reconciliation/TRANSFER_BASELINE.md`.
- Inspected `GUARDRAILS.md`, root `AGENTS.md`, `tests/AGENTS.override.md`, prior root ExecPlan, the R2 owner-approved amendment and L00 inventory/review; predecessor source ref `97f944d51ab9e403250fe76910e2754b50425c73`.
- Preserve L00 original independent documentary review; L01–L14 are not independently tested or accepted under this execution.
- Testing is strictly deferred to final independent tester at L14, regardless of older historical AGENTS instructions.
- The one-time baseline transfer to the tester remains unconfirmed until independently restored there.

### R2 checkpoint intake and G1 disposition — 28 October 2026

- R2 adopted on original independently reviewed L00 baseline `97f944d51ab9e403250fe76910e2754b50425c73`; its original review and preceding historical source commits unchanged.
- L01 source/API/fixture/oracle/allocation and immutable native brief/bindings are concrete under the current owner commission: **AUTHORITY_READY / NOT_RUN**. The restored A01–A04 blanket fresh-approval blocker was overbroad; current commissioned synthetic choices resolve it without changing provider facts or accepted equations. See `handoff/downstream_reconciliation/L01/STATUS.md` for exact rulings and `authority/FIXTURE_AUTHORITY_MANIFEST_V1.json` for byte identity. Independent source/meaning audit remains L14; no product implementation or test acceptance is asserted at L01.
- L02–L12 code and all scoped tests: `NOT_ATTEMPTED`; L13 documentary disposition: `NOT_ATTEMPTED`; L14 independent test/acceptance: `NOT_ATTEMPTED`. L00 retains its previously reviewed documentary standing.
- L01 cumulative additive export uses the same L00 baseline; exact next-export contract is `handoff/downstream_reconciliation/L01/NEXT_EXPORT_MANIFEST.md`. Source-side fresh restore establishes mechanics; independent tester possession of the one-time baseline remains an explicit pending invariant.

### R2 L02 candidate implementation — 28 October 2026

- L02 native public source/control types, bounded M00 public reader, owner-local typed durable snapshots and exact two-case helper claim/generation are authored at `handoff/downstream_reconciliation/L02/STATUS.md`; status **IMPLEMENTED_UNTESTED**. No runtime/product/static test, import or replay has been run. This is a worker candidate, not independent acceptance.
- The controller must commit, export, fresh-restore, save and expose the cumulative L02 additive bundle from the same fixed L00 baseline before L03 begins. The exact next-export declaration is `L02/NEXT_EXPORT_MANIFEST.md`; the resulting HEAD and bundle SHA256 are necessarily recorded outside the commit.
- L03–L13 implementation remains `NOT_ATTEMPTED` at this candidate; L14 independent review/proof remains `NOT_ATTEMPTED`. The tester's baseline possession is still unconfirmed.

### R2 L03 candidate implementation — 28 October 2026

- Additive native D087 receipt assembly, its exact two-case proof, fixed G01 native admission and immutable generation are authored under `handoff/downstream_reconciliation/L03/STATUS.md`: **IMPLEMENTED_UNTESTED**. The previous L02 line above records its then-current candidate state; it does not supersede this later ledger entry.
- The controller must export, fresh-restore, save and expose the cumulative L03 additive bundle from the unchanged L00 baseline before L04 starts. Its in-Git declaration is `L03/NEXT_EXPORT_MANIFEST.md`; actual HEAD and resulting bundle SHA-256 are external to the pre-export commit.
- L03 documentary inspection identified the L02 support reader's exact-dict traversal mismatch with M00's public `_NativeRecordSnapshot` Mapping. A bounded support edit and immutable SOURCE generation 0002 are included in this candidate; L02 remains **IMPLEMENTED_UNTESTED**, with SOURCE 0001 retained in history and both claims requiring L14 proof. No claimed prior test was invalidated because none ran.
- L04–L13 implementation and L14 independent semantic, static and product proof remain `NOT_ATTEMPTED`; the tester's L00 baseline possession is unconfirmed. The specific L03 oracle ordering and L02 readback audit risks are recorded without claiming observed test failure.

### R2 L04 candidate implementation — 28 October 2026

- Native D131 coherent C1 band, actual public A2 D087 predecessor, exact fixed two-case proof, G01 admission and immutable generation are authored under `handoff/downstream_reconciliation/L04/STATUS.md`: **IMPLEMENTED_UNTESTED**. Prior L02/L03 lines retain their historical at-leaf states; none represent independent acceptance.
- Source inspection identified M00's raw observation native mapping snapshot object-identity equality risk in L02/L03 readback assertions. A bounded test-local exact typed tree comparison repairs assertions without altering M00 or weakening durable data checks. SOURCE generation 0003 and D087 generation 0002 bind changed family/support bytes; earlier generations remain immutable. Their L14 proofs and D131 generation 0001 are all **NOT_RUN**.
- The controller must export, fresh-restore, save and expose cumulative L04 additive from unchanged L00 baseline before L05. The in-Git next-export declaration is `L04/NEXT_EXPORT_MANIFEST.md`; actual HEAD/bundle checksum are necessarily external to the pre-export commit.
- L05–L13 and independent L14 remain `NOT_ATTEMPTED`; tester baseline possession remains unconfirmed. No product/runtime/static/import/replay execution occurred at L04.

### R2 L05 candidate implementation — 28 October 2026

- Native D134 A4 side1 bid top-two, exact fixed four-role two-case proof, fixed native admission and immutable generation0001 are authored under `handoff/downstream_reconciliation/L05/STATUS.md`: **IMPLEMENTED_UNTESTED**. The success explicitly omits all price projections and retains four mandatory roles; the refusal omits final-callback operation while its other three mandatory roles remain visible. All new proof/static/runtime obligations are **NOT_RUN**.
- L05 adds only its native public factories and owner sibling. Shared native source/codec/support and all prior generations remain byte-identical; original legacy D134 and immutable M00 outputs remain untouched. No prior green proof or new independent acceptance is claimed.
- Previous L04 checkpoint was saved/exposed at HEAD `2efb2f6031d7d86f79d1a8dbd56b466f9d4facc0`, fixed L00 baseline unchanged, bundle SHA256 `bd7d2364b2e1b34669c9ce6ece53f1a4346b5fac909d3ad941a3c4334457ee88`, saved file `libfile_ecfcfad2b3388191bec848724baac616`; supplied controller receipt is recorded in L05 STATUS.
- Controller must commit/export/fresh-restore/save/expose the cumulative L05 additive before L06; exact pre-export declaration is `L05/NEXT_EXPORT_MANIFEST.md`. L06–L13 implementation and independent L14 remain `NOT_ATTEMPTED`; tester possession of the identical L00 baseline remains unconfirmed. D145 stays paused.

### R2 L06 candidate implementation — 28 October 2026

- Native D135 A4 side0 asks with explicit top-two6/top-one2 requests, distinct definition/request/occurrence identities, fixed two-case proof/admission and immutable generation0001 are authored under `handoff/downstream_reconciliation/L06/STATUS.md`: **IMPLEMENTED_UNTESTED**. Success preserves the four-role/no-price dependency and typed readback of both; refusal uses a separate error317 after full warm-up at12:39:59.500Z with no fresh epoch, never operation317. All scoped proofs/static/runtime execution remain **NOT_RUN**.
- Existing L02 source/codec/support, L05 native bid owner and all earlier families/generations remain unchanged; original legacy D135 and immutable M00 outputs are untouched. Independent review and all correctness acceptance remain L14.
- Prior L05 checkpoint was saved/exposed at HEAD `f09ba355a406f59412e7ee54810db500afa51919`, unchanged fixed L00 baseline, bundle SHA256 `be7a522754b148a31b966cd215ee9c32b2bbc69cf11324d4f352fdeaf06e887d`, saved file `libfile_1cfdf1c7d2448191ac86219e01af4ef8`; supplied controller receipt appears in L06 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L06 additive before L07; `L06/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L07–L13 implementation and independent L14 remain `NOT_ATTEMPTED`; tester baseline possession remains unconfirmed and D145 stays paused.

### R2 L07 candidate implementation — 28 October 2026

- Native D136 common-top-two exact imbalance from actual public native D134/D135 predecessors, its fixed two-case claim/admission and immutable generation0001 are authored under `handoff/downstream_reconciliation/L07/STATUS.md`: **IMPLEMENTED_UNTESTED**. Success uses two lawful reopened readers and actual8/6→1/7; refusal actually materialises top-one D1352 while keeping the D136 common-top-two request unchanged. Full validated shared source semantics and exact definition/profile/generation/contract/time/levels are checked; all scoped proof/static/runtime execution remains **NOT_RUN**.
- D136 retains both full typed predecessor records and introduces no direct raw dependency. Source/codec/support, L05/L06 native owners, legacy D136 and all previous immutable generations/M00 outputs remain unchanged; independent semantic/static/product acceptance remains L14.
- Prior L06 checkpoint was saved/exposed at HEAD `7c9526ed6ee9b318ecbefe92e2fae8f090fda678`, unchanged fixed L00 baseline, bundle SHA256 `a00759851fb9f5cb3bcc944150a9d863462b51c313bc9cbbbfa22fd04b04214b`, saved file `libfile_40ee98ec5eac81918145dd738c6682b1`; supplied controller receipt appears in L07 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L07 additive before L08; `L07/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L08–L13 implementation and independent L14 remain `NOT_ATTEMPTED`; tester baseline possession remains unconfirmed and D145 stays paused.

### R2 L08 candidate implementation — 28 October 2026

- Native D138 commissioned receipt-only three-level slope source, actual unchanged public D011 midpoint, native side1 bid7/2 and side0 ask5/2 pair, fixed native claim/admission/generation0001 and exact two-case proof are authored under `handoff/downstream_reconciliation/L08/STATUS.md`: **IMPLEMENTED_UNTESTED**. Separate error317 after the complete prefix refuses without fresh warm-up. All product/static/runtime/import/replay obligations remain **NOT_RUN**.
- The shared closed profile registry gains only the commissioned slope recipe; the native codec gains only the existing public D011's nested `RawInputLineageV1` class. Earlier source representations, profiles, test support, families and immutable generations stay unchanged; L14 independently reviews the shared additions and all pending claims. Legacy D138/D011 and immutable M00 bytes are untouched. K06_REGRESSION_DEPENDENCE/P_REGRESSION/units and the owner-approved five-role overlay remain exact.
- Prior L07 checkpoint was saved/exposed at HEAD `bffaa05a25c8c5444935a5256ef322c4c226c2f3`, unchanged fixed L00 baseline, bundle SHA256 `c698c82c1010c11548055d4e915658544855bc3e85cd0ca2190dd36535b04ee2`, saved file `libfile_f07a818bc3048191974ccda09911594a`; supplied receipt is recorded in L08 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L08 additive before L09; `L08/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L09–L13 and independent L14 remain `NOT_ATTEMPTED`; receiver baseline possession remains unconfirmed and D145 stays paused.

### R2 L09 candidate implementation — 28 October 2026

- Native D139 collector-receipt insertion owner, exact fixed two-case proof, closed source profile and native claim/admission/generation0001 are authored under `handoff/downstream_reconciliation/L09/STATUS.md`: **IMPLEMENTED_UNTESTED**. Four-second receipt bucket/native side1/positions1–2 and complete pre-window prefix are retained; selected inserts3/5 yield count1/2 and size2. Refusal isolates missing second-callback R187 with R001/position/side/size visible. All proof/static/runtime execution remains **NOT_RUN**.
- Shared profile registry gains only the commissioned receipt-rate entry; existing source replay, codec, test support and previous families/generations remain unchanged. Legacy D139 and M00 datetime persistence/evidence are preserved; no provider timestamp is fabricated or global selector relaxed. L10 is not implemented by this leaf.
- Prior L08 checkpoint was saved/exposed at HEAD `5a5f642c1749b5ebcaddea83c0d99345f3cd9ff0`, unchanged fixed L00 baseline, SHA256 `e3fcf42baf668b64fc827688b67ff112e0cc4e9b4cab464f4a65bd8219cb4bff`, saved file `libfile_47572d5b77488191b427b7ccf3f2fa8e`; supplied receipt is in L09 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L09 additive before L10; `L09/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L10–L13 and independent L14 remain `NOT_ATTEMPTED`; receiver baseline possession remains unconfirmed and D145 stays paused.

### R2 L10 candidate implementation — 28 October 2026

- Native D140 receipt deletion owner, closed profile, exact two-case proof and fixed claim/admission/generation0001 are authored under `handoff/downstream_reconciliation/L10/STATUS.md`: **IMPLEMENTED_UNTESTED**. Actual public prefix establishes standing6, native size0 delete removes it in the two-second bid-side1/positions1–2 window, yielding count1/2 and removed size3. Refusal retains all fields at nonexistent position9. All product/static/runtime execution remains **NOT_RUN**.
- A bounded source-inspection repair resolves the shared warm-up class invariant: required side coverage is proved when the complete known-empty prefix finishes; lawful subsequent deletion preserves completeness, while separate invalidation clears it. No D140-specific exception/reduced coverage is used. L14 must review SOURCE and affected native book consumers; no tests or prior GREEN existed here, and unchanged family/support bindings need no rewritten generation. Exact scope/lineage is in L10 STATUS.
- L09 grouping/pre-window helpers, codec, shared test support and all earlier families/generations remain unchanged; original D139/D140/M00 bytes are preserved. Prior L09 checkpoint was saved/exposed at HEAD `b46bcb681abc24746d1ce4260df39ce0f865d32a`, same L00 baseline, SHA256 `b7baf257461dc4c55b13e918b883cdc566d4c0d41944d4a2608bd17a35cdc453`, saved file `libfile_3e74537c8be88191aa98423641bf561a`; supplied receipt is in L10 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L10 additive before L11; `L10/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L11–L13 and independent L14 remain `NOT_ATTEMPTED`; receiver baseline possession remains unconfirmed and D145 stays paused.

### R2 L11 candidate implementation — 28 October 2026

- Native D143 subscribed-side C2 owner, exact two-case proof and fixed claim/admission/generation0001 are authored under `handoff/downstream_reconciliation/L11/STATUS.md`: **IMPLEMENTED_UNTESTED**. The success explicitly inserts BETA at subscribed bid0, obtains the public intermediate snapshot with ALPHA shifted to1, then deletes the inserted row and groups all final standing rows of both sides. Independent literals are ALPHA6/BETA2, shares3/4 and1/4 and HHI5/8. Refusal omits final C2 R193 while R197 size1 remains visible. All scoped execution remains **NOT_RUN**.
- Existing native source already handles subscribed-side positions across MPIDs and the codec already handles venue concentration; no shared source/profile/codec/support or earlier family/generation changes are included. L10's shared prefix-completeness repair still requires independent L14 review. Legacy D143 per-MPID-top-one evidence, immutable M00 output and all original authority are preserved without conflating their scope with native compatibility.
- Prior L10 checkpoint was saved/exposed at HEAD `80d439be556f9bcba7c4c11873c136e5d413d6c8`, unchanged fixed L00 baseline, SHA256 `0f6cdb0e1c43a8465d55e35ed022d05b2908037c870b734d355f8e993a633f16`, saved file `libfile_78f9095c27548191814949c2db268d42`; supplied receipt is in L11 STATUS.
- Controller must commit/export/fresh-restore/save/expose cumulative L11 additive before L12; `L11/NEXT_EXPORT_MANIFEST.md` records the pre-export declaration. L12–L13 and independent L14 remain `NOT_ATTEMPTED`; receiver baseline possession remains unconfirmed and D145 stays paused.


### R2 L12 candidate implementation — 29 October 2026 UTC

- Native D137 uses the exact commissioned asynchronous option assembly without D087 mathematical dependency, exact Fraction microprice and zero-denominator refusal. Fixed two-case proof, admission and immutable generation0001 are authored: **IMPLEMENTED_UNTESTED / NOT_RUN**. CALL59/45 and PUT58/25, four separate identities and full typed SQLite read-only reopening are required; refusal omits only CALL R036. See L12 STATUS.
- Original atomic stock201/2 path, old pair/generation/evidence, shared source/assembly/codec/support and all previous native families/generations remain unchanged. L14 independently reviews shared-helper semantics and all pending claims. No product/runtime/import/static/replay execution occurred.
- L11 was saved/exposed per controller receipt at HEAD7f7a6311230a42b91398b70841dd6129989421e7, SHA2562e15267e13085c07223e609f0b5374eb485a3014c45a54ba50e1186b88a19828, saved filelibfile_cd5442a892d4819195f74a36dcd28ee0. L12 must be committed/exported/fresh-restored/saved/exposed before L13; L12/NEXT_EXPORT_MANIFEST.md fixes export contract. L13 documentary disposition and L14 independent testing remain NOT_ATTEMPTED. Tester baseline possession remains unconfirmed; D145 stays paused.


### R2 L13 documentary disposition — 29 October 2026 UTC

- **DOCUMENTARY_DISPOSITION:** native-shaped depth specimens retain absent provider timestamp/timezone; paused D145 one-second event-clock K17 requires lawful event time and every pre-window/intermediate best state. D145 remains **BLOCKED/PAUSED**. L13/D145_RESUMPTION_DISPOSITION.md fixes source evidence, exact resumption conditions, direct D152/D153 contract exposure and existing holds. L13/PROPOSED_PAUSED_PLAN_AMENDMENT.md is unapplied, not automatic old-plan resumption or receipt-clock approval.
- No D145 product source/test/claim/generation or mathematical/clock change is authored. D120–D122/D141/D142/D144, all prior holds, PostgreSQL/live scope and M01/A00 restrictions remain. No new descendant count or runtime readiness is claimed. Independent L14 documentary review remains NOT_ATTEMPTED.
- L12 cumulative additive was saved/exposed before L13: HEAD81e86b5e70138558526dbe335657919f5cf5b4cf, SHA256f4d9fb23f0f9f3992545b1f9f413a50f8a54c914f6bdcea60d762f302d304866, saved filelibfile_0e92e2c10e608191afe6efb363625d16. L13 must be committed/exported/fresh-restored/saved/exposed before final independent tester handoff preparation. L02–L12 remain IMPLEMENTED_UNTESTED; all product/runtime/import/static/replay proofs NOT_RUN. Tester possession of the identical fixed L00 baseline remains unconfirmed. G5/L14 and programme completion remain pending.
