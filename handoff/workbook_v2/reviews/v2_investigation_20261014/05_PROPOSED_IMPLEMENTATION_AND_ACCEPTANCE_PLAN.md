# NVDA V2 — Proposed implementation, proof and acceptance ExecPlan

**Status:** **PROPOSAL ONLY — NOT INSTALLED AS ACTIVE `EXEC_PLAN.md`**. The original root `EXEC_PLAN.md` remains the sole active execution plan. All production changes below require current explicit acceptance of the exact new implementation-ready brief/scope and architecture ingress. The present commission expressly prohibits tests, app code, production edits and module construction; **this document is a plan, not execution approval**.

## P0. Authority and design transition — before any code

**Goal:** resolve the V2 meaning-to-architecture boundary without discarding the original 209-D history.

**Exact current sources:** `GUARDRAILS.md`; `AGENTS.md`; `EXEC_PLAN.md`; `handoff/m01_completion/AUTHORITY_INDEX.md`; `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`; the effective `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` digest `26c5486d...`; `handoff/workbook_v2/decisions/ADR_WBV2_001_...md`, `ADR_WBV2_002_...md` and Pass08; `docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md`, `OWNERSHIP_AND_COMPONENT_LAW.md`, `DEPENDENCY_LAWS.md`, `PUBLIC_SEAM_LAW.md`, `IMPLEMENTATION_AUTHORITY_INGRESS.md`, `EXTENSION_AND_RETIREMENT_RULES.md`, `TEST_AND_PROMOTION_KERNEL.md`.

**Recommended exact human approval package:**

1. **Accept the new module responsibilities** — M00 unchanged; `M01-1` as the V2 descriptive-market capability, **propose registration as the already-consumed architecture object `M01` with explicitly narrowed semantic responsibility**; M02–M31 as future separately admitted independent peers. The mixed original M01 graph is not silently relabelled as market truth.
2. **Accept the canonical D allocation register** as a proposed transfer target, with every D001–D209 still singular. The 114/95 workbook populations remain provisional until the authority-owned measurement/borderline questions are resolved. No D moves solely because of code placement or original kernel stage.
3. **Authorise a governed transition of the active ExecPlan**, preserving the original document verbatim in Git ancestry (the new active root plan must be explicit, not concurrently competing). The prior Stage-1 F1–F4 and Stage-2/Stage-3 work remains historical with exact evidenced completion/deferral disposition; **do not complete obsolete old M01 work merely for its former gate number**.
4. **Accept the immutable measurement-definition/version policy**, including proposed eligibility, source/selection definitions and resolution of the 65 convention flags; do not invent measurement coefficients where the original authority does not suffice.
5. **Accept a bounded compatibility/data migration policy** identifying source owner, old and new definition/version records, existing durable derived IDs, recalculation policy, lineage mapping and non-destructive rollback. Existing M01 persisted facts remain historical M01 facts unless exact semantic identity and compatibility are established.
6. **Admit exact implementation authority**, supplying an accepted byte-identical brief SHA-256 and human approval reference per `AK-INGRESS-001..005`. Runtime IDs are resolved by the legal architecture ingress, **not manually registered as `M01-1`**.

**Current hard decision:** accepted architecture identifier grammar forbids literal runtime ID `M01-1`. If owner rejects retaining/narrowing `M01` for the foundation, revised module allocation/working-number policy and explicit lifecycle transitions are needed before code. This is a planning-level production **BLOCKER**, not a reason to stop unrelated read-only inspection.

**Affected existing files / surfaces:** `config/architecture/modules.yaml`, `config/architecture/implementation_allocations.yaml`, current root `EXEC_PLAN.md`, exact ingress records under repository-native config/handoff processes, selected architecture proof configuration, existing public API. `GUARDRAILS.md` must remain unchanged. **Proposed new doc/file names are not authorised placements until the applicable ingress contract establishes them.**

**Proof proposition:** one registered semantic owner per output; valid reserved ID; new inputs/outputs/dependency/state/reader/writer law; full D identity coverage; exact original/proposed allocation comparison; no implicit second plan or peer edges. Separate independent governance/architecture review checkpoint before changing runtime behaviour.

## P1. Establish minimal M01-1 foundation boundary

**Reuse rather than wholesale rewrite** the present owner implementation only where its actual contracts fit. The following existing files are specific inspection/repair targets:

- `src/nvda_desk/derived_signal_calculation_truth/api.py` — typed projection ingress, public materialise/read seam, time/cutoff/selection/parameters, recursive graph evaluation, occurrence identity and lineage. Implement an **explicit authorised M01-1 D population and downstream-context refusal**, not a blanket K01–K08 dispatcher. Ensure no candidate, portfolio, live position or order-intent concepts leak through indirect configurations.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py` — preserve eligible kernel functions and helper algorithms as candidates; separate only after exact caller/dependency review. `_financial_policy.py` must not become an imported M01-1 dependency simply because it shares original M01.
- `src/nvda_desk/derived_signal_calculation_truth/_catalogue.py` and its hash-bound runtime CSV — preserve accepted 209-row historical definitions and canonical IDs; introduce only an approved precise owner/definition-version projection. Do not replace existing authority with a truncated or competing ad hoc 114-row normative catalogue.
- `src/nvda_desk/derived_signal_calculation_truth/_postgres.py` — current calculation-occurrence persistence and schema/role isolation; plan authorised table/reader/version separation and migration as required, not silent owner relabelling or destructive overwrite.
- `src/nvda_desk/raw_signal_occurrence_truth/api.py` and admitted projection mapping/contracts — M00 only provides raw identity/history/provenance; new provider mapping, if needed, belongs to M00-authorised interfaces, not private M00 database access.
- `config/architecture/modules.yaml` and composition/registry declarations — entry through public seams only; no runtime dependencies on future peers.

**Proposed boundary contract:** request a canonical D identity in the *accepted foundation set*, exact subject and source selection, as-of UTC and knowledge cutoff, immutable measurement-definition/profile versions and lawful M00 mapping/unit/convention refs. Emit either a fully typed durable result with exact R/previous-D occurrence lineage, definition/version identity, selected history and eventual `supersedes` relationship, or fail closed for an unsatisfied predicate. No parameter request may change the meaning of an existing definition. No actual account/order/provider mutation.

**Version and persistence transitions:** list old M01 consumer paths and durable data; use a version discriminator or separately admitted owner namespace for changed meaning rather than reusing historical occurrence IDs. Specify read-old/write-new behaviour and reversible current-tree Git checkpoint; no pruning or overwriting old Git/DB evidence. Old private code no longer in target active tree should be marked `DO_NOT_CARRY_FORWARD` where applicable (not destroyed from history).

**Proof before any production change:** governing ADR/ownership tests, allowed and forbidden D request matrix, raw-only legitimate ingress, forbidden candidate/portfolio/peer dependency matrix, graph predecessor selection/version/time cases, identity/lineage and persistent read-back. Then author implementation, focused source+architecture tests, narrow database integrity/permission tests and independent review on exact frozen candidate.

## P2. Resolve mathematical/source gaps by dependency — separately bounded work units

Every unit follows: establish exact accepted definition and source contract → write independently calculated expected-value positive/boundary/refusal tests **and commit them before production change** → implement narrow repair/new capability → run focused plus necessary regression/architecture/DB evidence → freeze recoverable exact Git checkpoint → independent reviewer evaluation. A new equation or native-provider mapping requires prior owner/source authority, not an improvised code fallback.

| Work unit | Exact proposition and code surface | Preconditions / refusal and independent proof | Recommended order |
|---|---|---|---|
| W-025 | D025 must use R040 session low and R039 session high in `.../_stage1.py:1354–1361` | Prove nonmidpoint cases e.g. high 110, low 90, last 95 gives 0.25; equal high/low and inconsistent/outside-session inputs have exact authority-derived refusal/handling; source-labelled test in `test_m01_f4_rc02_scalar_algebra_public.py` must no longer mask inversion | First numerical repair following P0/P1 |
| W-099/100 | D099/D100 exact 25/10-delta skew using R111 IV, R112 delta and R015 **right C/P**, not an invented strike; `_stage1.py:1430–1501` | Establish permitted canonical strike binding from exact option contract/source metadata; independently test native C/P, right/expiry/strike mismatch, ambiguous contract/source, correct IV difference and full lineage. Fix `test_m01_f4_rc14_skew_from_native_delta_public.py`'s synthetic R015=strike test input without weakening valid numerical assertions. | Early; D104 downstream historical skew depends on lawful skew inputs |
| W-009 | D009 outputs initial, revised and latest-visible macro vintages per accepted §5 K01; `_stage1.py:1188–1225` | Source period and visible historic vintage selection; independent 3-state cases, competing/partial revisions, cutoff, ambiguity, preserved identity, persistence and temporal refusal; do not invent missing FRED period semantics. | Early |
| W-096 | Implement only accepted D096 per-expiry, per-side 50-absolute-delta interpolation from R111/R112 and D085; present K09 dispatch excludes this row | Set/validate precise source contracts and frozen IV/expiry matching, duplicate 0.50 handling, bracketing, call/put averaging, single-side profile and unsupported extrapolation refusal. Test independently chosen exact interpolation numerics, source IDs, version/lineage. Introduce narrow lawful dispatch for *this* authorised row rather than all K09. | Before W-097/098/107/108 public acceptance |
| W-097/098/107/108 | Retain K02 existing calculations but integrate lawful new D096 values through original exact D predecessor meaning | Independently prove term-point selection and expiry spacing, original D035/D036 realised-volatility units, definition-version/time alignment and missing D096 refusal. | After W-096 |
| W-117 | Establish R075's accepted prerequisite/numeric or bucket role alongside R041; `_stage1.py:2270–2401` | **BLOCKED on missing authoritative role**; preserve both declared R inputs, no deletion. After resolution, prove matched historical contract/delta/expiry/time buckets, source identity, no-leakage cutoff, minimum sample and zero variance. | Authority-gated |
| W-123 | Preserve controlled two distinct official reporting periods and revision precedence, `_stage1.py:142–243`, `api.py:2485–2502` | Controlled provider-independent proof with explicit versioned projection and ambiguous-period/revision refusal. Separately obtain native IBKR/OCC or actual source mapping, if live-source operation is accepted scope; do not use receipt ordering as official period. | Controlled proof now in future authorised phase; live mapping separately gated |
| W-138 | Prove D138 inputs constitute a coherent book state (complete snapshots or reconstructed event history) before cumulative-depth OLS `_stage1.py:2603–2660` | **BLOCKED on admitted source semantics**; if only incremental R187 depth operations exist, establish lawful M00/consumer reconstruction boundary and replay/ordering rules, proof for inserts/updates/deletes vs full snapshot, missing rows, source/version mismatch, temporal and bid/ask separation. | Authority/source-gated |
| W-FREEZE | Individually resolve 65 V2 measurement-convention flags and other context/selection ambiguities | A stable, approved definition version and allowable non-strategy configurations for each row; lawfully refuse caller strategy overrides; no numerical inference from kernel family name. | Before admitting corresponding rows |
| W-OTHER | Re-examine all other 114 candidates, not only named failures, through full definitions, transitive R/D/context chain and public production selection/lineage/persistence | Indexed source paths are navigation only; independently expected arithmetic+temporal+boundary/refusal proof for each admitted calculation. Report any further genuine issue separately with source evidence. | Can be partitioned by independently proved semantic families, no blind all-rows-PASS |

**Subordinate source/contract decisions:** keep D117 R075 role and D138 book-state semantics separate from the independently proved D025/R015 source mismatches. D123 provider-independent proof cannot be called live provider support. D096 retains the original `D096` identity and accepted maths; no new D identity is needed.

## P3. Independent foundation acceptance and transition

Acceptance is not the number of dispatcher branches or green tests. Require **every finally admitted M01-1 D** to have:

1. Exact approved calculation definition/version, source and complete transitive eligibility (typed contexts and measurement conventions included).
2. Independently determined positive numeric/structural values, boundary/tie rules and invalid-input/refusal cases for required history, co-reference, native contracts and temporal/knowledge limits.
3. Correct definition/profile/convention versions, no implicit parameter mutation, deterministic retries, append-only successor calculation, lineage to original M00 and predecessor D occurrences, and durable read-back in bounded role/schema isolation.
4. Independent row-level calculation access (legitimate predecessor computations permitted), all public paths and accepted failure states; no dependency on downstream policy/strategy or another peer.
5. Relevant PostgreSQL, architecture/dependency/public seam, type/lint and application tests when authorised and available; specific controlled versus real/native source evidence accurately distinguished.
6. One frozen clean Git candidate with command/environment/results identities and a truly independent review accepting **that exact state**. Any missed mandatory check remains UNRUN/BLOCKED, not PASS.

Preserve historical tests only for the exact propositions they exercise; author fresh cases where meaning, R field identity or ownership changed. A controlled fixture is not source integration. Live validation is required only where an applicable accepted obligation explicitly demands it.

## P4. Thirty independently executable downstream peers

The 30-module recursive map in `04A_DOWNSTREAM_95_ROOT_CLOSURES.csv` and `04B_DOWNSTREAM_30_PEER_SUMMARY.csv` supplies **each module's exact declared canonical D outputs**, transitive historical D references, lawful M01-1 inputs, original M00 R field ingress, typed contexts and missing Stage-2 kernel labels.

For **each proposed module**, implement the following finite independent semantic unit only after its own bounded brief and authority:

- Define exact semantic responsibility/exclusions, D outputs, private intermediate labels, accepted equations, source and context contracts, time/knowledge and side-effect ownership.
- Trace each canonical D dependency recursively; consume only M00/M01-1 public results. Where historical D graph refers to a signal assigned to a different peer, reproduce the strategy-dependent **whole remaining chain** under module-private identity/config/lineage. Never import/call that peer or read its private state; do not introduce a common strategy calculation module. Local copies must preserve the accepted required mathematics or explicitly seek authority where adaptation affects meaning.
- Investigate and reuse appropriate old `_stage1.py`/`_financial_policy.py`/context/projection components only where source law and private independence are established. Existing Stage-2 nodes need new authorised implementation; a code locator or the source's family label does not supply that.
- Author peer-owned proof **first**, including independent standalone execution without any other M02–M31 running, forbidden peer import/state access, local config change isolation, stable canonical D ownership, local version/lineage, refusal/recalculation and database separation where applicable.
- Independently review and accept the exact admitted peer. Work order is by ready foundation inputs, approved source contracts and owner priorities **not** ascending working label or historical cross-group edge direction.

**Suggested initial peer planning cohort only**: identify those with no unresolved Stage-2 nodes and relatively short private chains from `04B`; this is a readiness screen, *not* an implementation mandate. Other peers cannot use a neighbour's completion as a runtime prerequisite. Financial-policy D175/D178/D189/D192 source repairs from the 13 October original-M01 line are reusable candidates for corresponding local peers, subject to exact ownership and independently accepted proof.

## P5. Composition, compatibility and release

1. Review application composition/registry through the architecture's lawful `A` layer, with **no inferred live trade scheduler, capital allocator, broker routing or trading permission**.
2. Verify separately: consumers use one lawful M00/M01-1 foundation; every peer runs without others; peer-private state and configuration are isolated; canonical D occurrence identity is singular.
3. Version/transition old persisted M01 results explicitly; preserve old lineage and old code in normal Git history; use `DO_NOT_CARRY_FORWARD` for retired active-tree code when appropriate, not destructive deletion/history rewriting. Recovery target is last independently accepted checkpoint.
4. Require architecture lifecycle/admission/promotion proof plus domain evidence for each exact module; externally connected activity needs a separate mandate and brief.

## P6. Explicit next executable unit after authority

**First pending approval:** resolve/accept the architecture identity and original-M01 responsibility migration in P0, including legal `M01`/`M01-1` mapping, accepted target D population and immutable measurement-profile policy, and install **one** newly approved ExecPlan via governed ordinary Git commit. Do **not** install this proposal without approval.

**First bounded proof/production unit after that boundary:** W-025, independently expected High/Low identity proof first, then minimal `_stage1.py` correction and public-seam source-labelled test update, with a distinct proof commit preceding code and a recoverable review checkpoint. In parallel at planning level, resolve source/authority prerequisites for W-117/W-138 and native W-123 without running or changing production until admitted.

## P7. Stop and review logic

Stop dependent changes at the first: conflicting source authority, absent native field/period/revision contract, unsatisfied immutable measurement meaning, invalid architecture ID, incompatible stored-state conversion, failed expected-value or lineage proof, unavailable required independent reviewer, or mandatory database integrity/proof check that cannot be executed. Retain exact source, failed result and preceding accepted checkpoint. Do not weaken a valid test, substitute a synthetic success for live evidence, or revive the original monolithic stage sequence because it is convenient.

**Current plan status:** investigatory document only. No tests or production modifications made.
