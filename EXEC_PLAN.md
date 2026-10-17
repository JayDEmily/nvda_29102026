# NVDA V2 — Active ExecPlan: Gates 3 and 4

Date: 17 October 2026 — Australia/Melbourne. Revision: 1.

**Status: ACTIVE. Gate3 IN_PROGRESS: G3.1 COMPLETED_SOURCE_INSPECTION; G3.2 COMPLETED_DOCUMENTARY_ASSESSMENT; G3.3 NOT_STARTED. Gate4 NOT_OPEN.**

**Activation,17October2026:** The owner stated “Okay, I approve the draft. Execute Leaf 3.1.” This accepts the draft at commit `be288c23327face2ef9c43472903c9e0d450593d`, tree `378cce1557c544c64a208c566ef04da216abb39a`, SHA-256 `5db52a2c86e370038158022fabbdba9b8fe0b8b1033b5e37b695378d5d168c89`. The single root plan is replaced on `work/v2-g3-1-shared-execution-assessment-20261017`. Its predecessor remains at `c88abc1367a6c4c755673c68e7f72536decc2c2f:EXEC_PLAN.md`. The proposed snapshot is unchanged. Draft/conditional activation language below is preserved from the approved text; this later explicit activation governs status. Current execution is limited to Leaf3.1; G3.2 is not authorised in this pass. No main merge, tests, application/provider execution or production change is authorised. Archive recovery/failure details are recorded in the cumulative assessment; the exact approved commit/tree and full Git object graph have been recovered and verified before activation.

**Goal:** Establish what existing engineering actually provides, what can serve the accepted future responsibilities, and the exact dependency-ordered route to implementation and acceptance.

**Basis:** Master ADR-WBV2-003, `handoff/workbook_v2/decisions/ADR_WBV2_003_V2_INVESTIGATION_COMMISSIONING_BRIEF_VERBATIM.md`, SHA-256 `7a05874fbd4971d03bcef47d5cdaf8020f533a10a6a73cf0ef276b8cb446f771`; its full intent/method/deliverable requirements remain applicable. Accepted Gate2 delivered baseline `a613ee497fe5d8b8bfbf8df9ba007a838a07f19b`, tree `6b1938348f1df29b33fca848406058404a701bda`. Owner acceptance is recorded at `c88abc1367a6c4c755673c68e7f72536decc2c2f:handoff/workbook_v2/gates_01_02/GATE_2_OWNER_ACCEPTANCE_20261017.md`.

This draft plans the **next two gates, G3 and G4**, rather than every eventual production gate. It completes the remaining investigation/planning commission; its G4 deliverable is the separate, repository-specific implementation/acceptance roadmap required by the master. Drafting that roadmap does not implement it.

## 1. The two decisions and why the leaves are grouped this way

| Gate | Decision at exit | Leaves | Master coverage |
| --- | --- | --- | --- |
| **G3 — Actual capability and foundation reuse assessment** | Is the account of original M01 progress and future foundation readiness reliable enough to design the transition? | G3.1 shared execution mechanisms; G3.2 all209 calculation paths/evidence; G3.3 foundation reuse and remaining work | §6.C–D, with §§1–5,7,9–12 |
| **G4 — Downstream self-sufficiency and implementation route** | Is there a concrete, lawful and executable route from that engineering to the future foundation and independent peers? | G4.1 peer-local computation designs; G4.2 implementation/acceptance roadmap | §6.E and all six §8 phases, with §§1–5,7,9–12 |

Shared infrastructure is inspected once before row conclusions; each original calculation is then assessed once and the same evidence feeds foundation and downstream reuse. G3 ends at a useful assessment decision. G4 ends at a useful design/roadmap decision. Five leaves are substantive outcomes, not five document-production steps. No separate gates are created for opening files, recording hashes, each D, each parameter flag, each peer or each future test suite.

## 2. Authority, entry and limits

Gate1 and Gate2 are accepted documentary investigations. The accepted future-design population is126conditional foundation families and83downstream canonical calculations in26proposed responsibilities. M00 remains the raw boundary; registered M01 remains transitional. M02/M03+ are working target labels, not admitted numeric identities. Preserve historical114/95,95members/30groups/107references and174/144/30stage populations as their own evidence; do not use them as current quotas.

Apply the full accepted authority chain: original calculation brief/catalogue, applicable owner amendments including D117, D123, D138/D145 and D028, accepted B1–B5/S1/N1–N10 package and bounded N6 closure. Original catalogue/readback and earlier After-L2 fields can be historical snapshots; use the effective accepted overlays when assessing current requirements. Do not revive removed R075/R044 dependencies or reopen accepted mathematics merely because source/runtime bytes lag the overlay. A newly evidenced semantic conflict requires a specific bounded decision, not silent amendment.

**Activation:** Present this draft first. If the owner explicitly accepts it as the successor active plan, preserve the previous root plan at `c88abc1367a6c4c755673c68e7f72536decc2c2f:EXEC_PLAN.md`, install the accepted successor as the single root `EXEC_PLAN.md` on a work branch, and record that exact activation. Change only draft-status/provenance metadata to ACTIVE, G3 NOT_STARTED, G4 NOT_OPEN; preserve the accepted substantive leaves and conditions. GUARDRAILS and all AGENTS remain frozen. Gate2 acceptance and this drafting instruction do not themselves activate G3. No main merge is implied. At activation, reconcile any intervening changes before relying on the accepted baseline. G3 starts only under the accepted successor; G4 entry requires owner G3 acceptance.

**Investigation scope throughout both gates:** read documents, complete relevant source functions/callers/helpers, test source, historical results/reviews and Git lineage. Standard read-only parsing and file/Git checks are allowed. Do not run application code, tests, lint/typecheck, repository runtime validators, databases or provider calls. Do not change code/tests/schemas/runtime configuration/catalogues/workbooks/registry or admit owners. The separate upstream IBKR acquisition module is outside implementation/integration scope; specify only its required delivery contracts, receiving responsibility and later proof obligations. No source/profile/runtime admission, state migration, live trading or M01 retirement occurs.

## 3. Gate 3 — Actual capability and foundation reuse assessment

**Entry:** Accepted Gate2 baseline and explicit successor-plan activation. **Outcome:** Separately evidenced original-M01 progress,126-family foundation readiness and a justified reuse/completion backlog, not accepted production readiness.

### G3.1 — Establish the shared public execution and state path

Read `src/nvda_desk/derived_signal_calculation_truth/api.py`, `_catalogue.py`, `_stage1.py`, `_financial_policy.py` and `_postgres.py` in their relevant complete contexts. Follow the actual public M00 projection/selection interfaces, predecessor evaluation, immutable parameters/contexts, result construction and persistence definitions they call. Inspect current `config/architecture/modules.yaml` and `implementation_allocations.yaml`, applicable seam/dependency/state/proof laws and relevant test/review source. A filename or dispatcher count is only navigation.

Establish which mechanism owns source selection, timestamp kinds, history sufficiency, cutoff/revision order, units, parameter/context versions, lineage, retry/recalculation, result identity, writer/read access and isolation. Identify where broad M01 or downstream assumptions enter otherwise reusable machinery. Record one shared mechanism map with exact public entry-to-helper-to-store paths and evidence limits; link it from rows rather than reproducing it209times. Do not infer actual populated stores, live consumers or native source capability from a schema or fixture.

**Leaf satisfied when:** the shared mechanisms needed to judge public calculation availability are traced sufficiently to support later row conclusions; each established gap has its location, required behaviour, actual source behaviour and consequence. Unknown runtime/data facts are distinguished from missing source inspection. Output: the shared-path section of the cumulative assessment.

### G3.2 — Establish actual original-M01 progress for every calculation

Against each D001–D209 effective accepted requirement, trace its actual own kernel and public request path, required predecessors/contexts/configuration, selection/history/refusal and result/persistence path, using G3.1 once for shared mechanisms. Record actual absence only after following dispatch, helpers and alternate public paths far enough to support it. Keep separate fields for own-kernel availability, public graph reachability, source-contract readiness, persistence/lineage support, test-source proposition, historical execution evidence and independent acceptance. A controlled synthetic fixture does not prove native-source supply; an old green log does not prove the current tree.

Read repair/reviewer lineage before declaring a defect current or resolved. In particular examine the master §7 leads, D009 revision handling, the alleged D096 absence and dependants, D117's accepted R041 history law, D123 official-period/revision selection, D028's accepted R041-only exact-fraction contract versus the previously observed fraction misuse, and L2 ordering/reset/readiness/numeric-enum handling. These are targeted leads, not substitutes for all209rows or a claim that every old diagnosis remains current. Reconcile F4-01–F4-07, R01/R02 and174/144/30 proof debt against the actual inspected candidate without rerunning tests or resuming the old repair sequence.

**Leaf satisfied when:** every canonical row has an inspected requirement-to-public-path/evidence disposition or an exact independently evidenced blocker; missing inspection is explicitly UNASSESSED. Report what remains against original M01 separately from what the new design needs. Output: enriched existing209-row register and original-progress section; no completion percentage derived from path counts.

### G3.3 — Determine foundation reuse, boundary changes and remaining obligations

For all126accepted foundation families, compare the effective meaning/full input family with the actual code and infrastructure from G3.1–2. Assess concrete existing profile domains, source bindings, public contracts, dependencies, lineage and storage separately from family eligibility. Specify the smallest justified separation: what mathematics can be retained, what embeds broad M01/strategy ownership, which public/state contracts must change, and where history/reader/identity compatibility needs further evidence. Route the83downstream calculations as preserved engineering for G4 rather than trying to finish them inside the foundation.

Use the master's exact reuse dispositions: `REUSE_AS_IS_CANDIDATE`, `REUSE_WITH_SEPARATION`, `REPAIR_REQUIRED`, `NEW_IMPLEMENTATION_REQUIRED`, `AUTHORITY_OR_SOURCE_CONTRACT_BLOCKED`, `DOWNSTREAM_PRESERVE`, `UNASSESSED`. Keep a numerical defect, source gap and evidence/admission debt as distinct linked work even when they affect one D. An as-is candidate is not admitted capability. Where accepted overlays need future catalogue/hash/code/fixture incorporation, state the exact affected surfaces and proof; do not perform the synchronisation here.

Reconcile every inherited M/G/R/A/T and F4-01–F4-07 obligation from Gate1. Preserve bounded accepted evidence with its original scope; assign every surviving obligation a current receiving responsibility/work item. Do not require completion of the obsolete monolithic schedule, silently drop its semantic/proof obligations or generate new receipts merely to repeat old acceptance. Carry B4 source/profile holds with exact consumer contract, missing fact, consequence, responsible role and pre-production hold point. Actual sources/profiles may remain unproved while the assessment of that gap is complete.

**Leaf satisfied when:** all126families have defensible row-level reuse/readiness dispositions, the shared boundary changes are explicit, all83downstream rows are retained for G4, and inherited/source/profile/evidence debt has an actionable receiver. Output: foundation assessment and initial implementation-work backlog linked to the same rows/issues.

### Gate 3 exit

Submit one assessment decision supported by: all209original-progress dispositions; shared-mechanism findings; all126foundation reuse/readiness dispositions; a complete inherited-obligation map; and precise unknowns/blocks with receiving actions. The owner may accept a complete, evidenced **assessment that capabilities are absent/unready**. Do not call inspection complete while material rows remain uninspected, or foundation production-ready while actual contracts/proofs remain unavailable. A genuine blocker to assessment yields PARTIAL/BLOCKED, with unaffected work preserved.

Owner ACCEPT means that assessment can ground G4; it does not admit M02, code reuse, source selection or implementation. Proposed readiness changes affecting Gate2 meaning/allocation must receive proper authority before relying on them. Otherwise continue routine in-scope investigation without per-row approval requests.

## 4. Gate 4 — Downstream self-sufficiency and implementation route

**Entry:** Owner-accepted G3 assessment. **Outcome:** Designs for all26proposed responsibilities and an exact implementation/acceptance roadmap covering the whole master commission.

### G4.1 — Design complete independent peer-local chains

For every one of the26accepted responsibility proposals, identify its purpose/canonical outputs, lawful M00/future-foundation public inputs and full recursive non-foundation computation chain. Start from the accepted Gate2 output/frontier table, then use G3's actual implementation evidence to trace each required path to lawful shared ingress or an explicit unresolved prerequisite. The Gate2 ancestor list is not itself a software design. Preserve the original95/30/107 sources as historical lineage; P04/P05/P06/P09 have no downstream canonical output under Gate2 and must not reappear as runtime allocations by default.

Map existing code that can supply each local chain and the required extraction, repair or new work. Specify private intermediate identities, definitions/configuration versions, source/predecessor lineage, state/time ownership, persistence/read boundaries and refusal. Distinguish these local nodes from the one canonical identity/owner proposal for each D. Demonstrate by inspected design paths how each peer can operate and be tested while every other peer is absent: no runtime call, shared strategy service, private import, private-state read or mutable model/configuration dependency on a peer. Equivalent downstream arithmetic is locally owned; lawful shared foundation calculations remain shared. No numeric module reservation, new equations or accepted implementation status arises from this map.

**Leaf satisfied when:** all26responsibilities have complete recursive designs and source-grounded reuse/gap actions;83canonical outputs remain unique; every boundary/private chain is explicit and every path terminates lawfully or at a named prerequisite. Output: one downstream self-sufficiency map linked to work items, not26approval packets.

### G4.2 — Produce the executable implementation and acceptance roadmap

Turn the G3 backlog and G4.1 designs into the separate proposed implementation plan required by master §8. Cover all six dependency phases: authority/boundaries; foundation separation; mathematical/source gaps; independent foundation acceptance; separately bounded peers; composition/transition/release. Phase4 consolidates acceptance; it is not the first time proof occurs. Do not force one future gate per phase or finalise detailed distant execution gates before their implementation scope is established.

Each coherent future work unit identifies: proposition and exact accepted authority; affected D/mechanisms and current/proposed responsibility; actual existing files/contracts plus justified proposed file changes; prerequisites including source/profile holds; intended change and refusal; independently derived positive/boundary/invalid-input proof; public/history/version/lineage/state compatibility evidence; required environment and relevant checks; independent review/owner acceptance boundary; and a recoverable checkpoint. Group work by a shared semantic invariant, not one item per source file/D or arbitrary batches. Do not fill unknown methods, signatures, provider fields or numerical expected values from invention: complete available investigation first; leave truly unavailable prerequisites explicit and prevent affected work from being scheduled as executable.

Plan proof-before-production for every future repair/implementation unit, targeted regression and supported-runtime/type/database proof as applicable. Preserve reusable historical witnesses with their exact limits. Separate controlled-input, native-source-contract and observed-source evidence; no blanket live-run demand. Choose implementation order from real prerequisites/owner priority, not module numbers or old Stage1/2 labels. The first executable unit after implementation authority must be exact; if it is blocked, name the precise decision/evidence unit required first.

Specify lawful exact-brief acceptance/ingress, unused-ID resolution and registry/admission decisions without performing them. Plan old-result writer attribution, identity collision/version compatibility, consumer inventory, reader/cutover/recalculation and recovery; unavailable actual database/consumer facts are named pre-migration prerequisites, not assumed empty stores. Plan M01 retirement separately after lawful successor coverage, state/consumer/proof compatibility and owner decision. `DO_NOT_CARRY_FORWARD` is a proposed target-tree disposition with preserved history, never deletion of mathematical obligations or automatic retirement. Identify any additional acquisition/composition/operational brief actually required; do not invent a trading orchestrator or order/account authority.

**Leaf satisfied when:** the roadmap covers all six §8 phases, all work items/peers and carried obligations with real dependency order, exact next unit, proof/review/approval boundaries and recovery. Material unresolved prerequisites remain visible and block affected execution. Output: the proposed implementation/acceptance plan, completion backlog and decision queue; no production execution.

### Gate 4 exit

Submit one decision on the coherent assessment/design/roadmap package. It must answer both master §1 questions, cover every D and proposed peer, support reuse conclusions from inspected paths, account for the full local chains, carry all material gaps, and identify exact future changes/acceptance conditions. A list of problems without executable sequencing does not pass. A concrete plan with explicit external prerequisites can pass **as planning**, but cannot call those blocked work units executable or claim full production readiness.

Owner ACCEPT closes this investigation/planning commission within its documented limits. Future implementation requires exact scope/brief/ingress and execution authority; it is not opened by a report, roadmap or Gate4 label.

## 5. Evidence and review without a receipt factory

Use one cumulative assessment report, `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md`, with sections for shared mechanisms, original progress, foundation readiness, carry-forward obligations and gate exits. Enrich the existing `gates_01_02/D001_D209_TRACEABILITY.csv` and linked `ISSUES.csv`/`ISSUE_D_LINKS.csv`; preserve canonical IDs, source/historical fields and accepted Gate2 baseline in Git. Add genuinely new material findings as linked issues;21/124are prior checkpoint counts, not a ceiling on actual findings. Reference shared evidence rather than repeating it in every cell.

Create only the master-required substantive companions when work reaches them: `IMPLEMENTATION_WORK_ITEMS.csv` (foundation and peer work in one dependency-linked backlog), `DOWNSTREAM_SELF_SUFFICIENCY.md` (all26designs in one map), and `IMPLEMENTATION_AND_ACCEPTANCE_ROADMAP_PROPOSED.md` (separate from the assessment). Keep material decisions in the existing issue register or one linked proposal where the exact decision needs prose. These are planned outputs, not artefacts falsely prepopulated by this draft. Do not make one findings document per leaf, one receipt per row or an empty template merely to satisfy a file count.

At leaf completion record outcome, exact evidence coverage and next unmet invariant briefly in the cumulative report/active plan ledger. Continue within accepted scope when the next leaf's inputs are established. No mandatory per-leaf reviewer round, owner signature, commit or archive; make recoverable commits at coherent checkpoints. At each gate exit present one exact reviewable candidate and its limits for owner ACCEPT/RETURN/BLOCK. Consolidate any applicable/requested independent review at that gate; this draft invents no additional investigation-review mandate or waiver of later production review. Previously accepted bounded evidence needs fresh review only when a changed proposition requires it. New delegation still requires applicable authority.

Stop dependent work at genuine authority, required-evidence or integrity failure; preserve the exact first failure and last proved checkpoint. Do not weaken a required check. Continue independently available authorised investigation; absence of a live provider/runtime is not a reason to halt source assessment. Missing inspection remains UNASSESSED, uncertainty UNKNOWN and an established prerequisite barrier BLOCKED. A receipt/hash/count never substitutes for semantic evidence.

## 6. Coverage and progress

| Master requirement / carried boundary | Receiving work |
| --- | --- |
| §§1–2 intent, foundation/peer independence and local duplication | G3.3 and G4.1; preserved from Gate2 rather than reapproved by default |
| §§3–5 source hierarchy, scope, actual-path reasoning | All leaves; G3.1 source mechanism map and G3.2 row evidence |
| §6.C original-M01 progress and separate proof states | G3.1–2 |
| §6.D all foundation rows and reusable infrastructure | G3.1 and G3.3 |
| §6.E every peer's full recursive chain | G4.1 |
| §7 audit leads, chronology and convention/source issues | G3.2–3 with exact Gate2 amendments, not stale raw lists |
| §8 phases1–6, proof first and transition/release limits | G3.3 supplies boundary/reuse facts; G4.2 produces the complete roadmap |
| §9 six deliverables | Cumulative report/register/backlog, peer map, separate roadmap and linked material decisions |
| §§10–12 stops, completeness, recoverable handoff and evidence limits | Both gate exits and section5 |
| Gate1 M/G/R/A/T ledger and F4-01–F4-07 | G3.2 historical/current evidence, G3.3 exhaustive receiving map, G4.1 local chains, G4.2 successor proof/migration/retirement |
| B4 SRC-CALENDAR, SRC-MACRO, SRC-OI, SRC-VOLUME, SRC-BOOK, RAW-PROJECTION, CALC-PROFILE, MODEL-PROFILE | G3.3 readiness/receiver, G4.1 consumer closure, G4.2 prerequisite/commissioning/acceptance hold |

**Current execution ledger:** G3.1 COMPLETED_SOURCE_INSPECTION; G3.2 COMPLETED_DOCUMENTARY_ASSESSMENT; G3.3 NOT_STARTED; G4.1–G4.2 NOT_OPEN. The latest owner instruction authorises G3.2. Its original209-row source/evidence census is recorded in section8; foundation reuse/downstream design remain later leaves.

**Authoring check:** The first structural check required every B4 hold's exact ID and failed on abbreviated IDs in the coverage table. After expanding the IDs, the same check passed, together with two-gate/five-leaf structure, C–E/six-phase coverage and unchanged master/governance/root/register/main checks. The plan was self-checked against the master and inherited obligations; no independent review of this new draft is claimed. This is a draft-document correction, not execution or failure of a planned gate.


## 7. Execution checkpoint — Leaf3.1 only,17October2026

G3.1 shared public execution/state-path source inspection is satisfied; see `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` for exact scope, source paths, shared-boundary findings SM-01–SM-06, historical-proof limits and the preserved failed-archive/recovery record. This is the worker's documentary finding, not independent review, implementation acceptance or Gate3 ACCEPT. The source/semantic baseline remains be288c2; no production/test/catalogue/registry/governance or209-row register change occurred. Tests/application/database/provider operations were not run.

G3.2–G3.3 remain NOT_STARTED and Gate4 NOT_OPEN. Current owner instruction ends at G3.1; next semantic unit is G3.2 when instructed. Gate3 exit remains pending the remaining leaves and the separate owner decision.


## 8. Execution checkpoint — Leaf3.2,17October2026

The owner instructed “Okay, complete the next leaf.” This authorises G3.2 after the completed G3.1 checkpoint and supersedes earlier Leaf3.1-only limits for this documentary pass. G3.2 is COMPLETED_DOCUMENTARY_ASSESSMENT: every209row has an effective-requirement, actual own behaviour/public path, missing-producer closure, separate source/persistence/test/historical/acceptance disposition. See cumulative assessment sections7–11 and enriched existing traceability/issue/link registers. The source assessment distinguishes174own paths,144structurally closed and30advanced-dependent paths,35absent producers, accepted overlay discrepancies and surviving F4/R01/R02 proof debt. No numerical completion percentage or implementation readiness is inferred.

Only documentary plan/report/register changes occur. Original Gate2 semantic/source fields and21issue/124link checkpoint records are preserved;14new material source findings give35issues/196direct links. G3.3 reuse dispositions remain UNASSESSED deliberately; all126foundation families,83downstream rows and26proposals retain accepted Gate2 classification. Production, tests, runtime/catalogue/profile, schemas, workbooks, registries, frozen guardrails/agents and main are unchanged. Application/tests/type/DB/provider operations were not run; no new independent implementation review is claimed. Gate3 remains IN_PROGRESS, G3.3 NOT_STARTED, Gate4 NOT_OPEN. Next semantic unit is G3.3; no implementation authority is created.
