# NVDA rebuild — corrected continuation brief
**Date:** 2026-04-19  
**Purpose:** correct the next-work queue so it follows the workbook benchmark, the prebuild pack, and the retained-test authority without drifting across sessions.  
**State basis:** accessible checkpoint only — branch `work/post-wave1-contract-truth-pass-20260419` at `3540521e3c0e35c2270e01daf77b91f97ea2ffa9`.

---

## 1. Direct answer

The earlier brief was **directionally aligned but not fully in the natural order**.

It was correct that these are real outstanding areas:
- packet / DMP truth,
- vocabulary reconciliation,
- thin repository/runtime surfaces,
- deferred replay/review and upstream-support families.

But it was **too code-first**.

The workbook and prebuild pack make the next lawful priority:
1. **finish the benchmark-to-test authority mapping**,
2. **finish Tier A/Tier B family normalisation and registry truth**,
3. **prove the blocking test shell matches workbook-owned bounded families**,
4. **only then continue code migration/hardening family by family**.

That ordering is required by:
- hierarchy: `migration_prebuild/00_hierarchical_order.md:3-21`
- test migration authority: `migration_prebuild/03_nvda_test_ordering_review_2026-04-18.md:5-56`
- rebuild execution order: `migration_prebuild/04_rebuild_execution_order.md:20-27`
- family-split constraints: `migration_prebuild/06_tier_family_normalisation.md:36-53`
- workbook test architecture: `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`, `Test_Architecture!A2:H20`
- retained-test authority rules: `config/retained_test_registry.yaml:5-10`

---

## 2. Why this is the natural continuation

### 2.1 The workbook is the architecture benchmark, not the migration sequence
The prebuild pack states explicitly that the workbook owns:
- package structure,
- module ownership,
- seam contracts,
- persistence ownership,
- shell policy,
- test architecture,
- reservations,

but **does not own migration sequencing or general governance process**: `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md:26-40`.

So the next queue must combine:
- workbook benchmark truth,
- retained test ordering,
- family-normalisation rules,
- and rebuild execution order.

### 2.2 The workbook says every benchmark family must map to an explicit test family
The workbook is explicit:
- “Every benchmark family must map to an explicit test family” — `Test_Architecture!A2`
- packet carriage, persistence domain ownership, downstream shell honesty, calendar projection vs CRUD split, replay/scenario containment, and specimen-path harness are all separate benchmark families — `Test_Architecture!A10:H20`

That means the test shell must be benchmark-shaped **before** code migration can be trusted.

### 2.3 The retained-test authority already moved from broad blockers to bounded successors
The retained registry shows exactly the pattern you described:
- broad predecessors are marked `split_replaced`,
- successor blocker families are listed explicitly,
- the split is lawful only if the full predecessor envelope is preserved.

Example: the old broad financial-calendar blocker was retired only after four successor families existed:
- `reference_data_contract`
- `calendar_reference_projection_crosswalk`
- `reference_packet_carriage`
- `financial_calendar_vocabulary_terms`

Evidence: `config/retained_test_registry.yaml:29-54`.

This is the same bounded-family doctrine you were describing in plain language.

### 2.4 The family-normalisation pack confirms the split rule
The split rule is explicit:
- split only when it aligns successor artefacts to workbook-owned bounded families,
- the predecessor envelope remains covered as a group,
- every successor blocker exists before the predecessor retires,
- DMP and vocabulary obligations remain covered,
- the retained registry records the mapping truthfully.

Evidence: `migration_prebuild/06_tier_family_normalisation.md:36-44`.

So yes: your description is correct. The repo moved away from “one test file covering too much” toward bounded blocker families aligned to workbook-owned ownership boundaries.

---

## 3. What is already true in the accessible checkpoint

### 3.1 Tier A was already split into bounded families
Visible directly in the tree:
- `tests/tier_a/reference_data/test_reference_data_contract.py`
- `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py`
- `tests/tier_a/packets/test_reference_packet_carriage.py`
- `tests/tier_a/review_runtime/test_review_stage_surface.py`
- `tests/tier_a/review_runtime/test_review_explanation_service_surface.py`
- `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py`
- `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/vocabulary/test_vocabulary_schema_contract.py`
- `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`

This matches the bounded-family split doctrine.

### 3.2 The retained registry is now the native test authority
The registry says:
- it is the active retained-test authority,
- no pytest file enters Tier A/B/C unless admitted there,
- runtime code and docstrings must be reread before trusting a family.

Evidence: `config/retained_test_registry.yaml:1-10`.

### 3.3 Some Tier B families are still deliberately deferred
Visible directly in the registry:
- `upstream_non_interference_and_sanity_traces` is deferred pending upstream-signal family admission — `config/retained_test_registry.yaml:1410-1428`
- `upstream_signal_coverage_map_and_scope_lock` is deferred pending upstream-signal family admission — `config/retained_test_registry.yaml:1429-1446`
- `tranche_a_review_replay` is deferred pending runtime-family admission — `config/retained_test_registry.yaml:1447-1464`

So the test architecture is **partly normalised, not fully closed**.

---

## 4. Correction to the earlier brief

The earlier brief should be read as:
- **good on outstanding technical themes**,
- **wrong on immediate sequencing**.

### What remains good in the earlier brief
Keep these as real outstanding themes:
1. vocabulary reconciliation
2. replay/review lineage family
3. upstream non-interference / sanity-trace family
4. dataset-packet / raw-signal coverage family remains blocked
5. DMP shell thinness
6. thin repository/runtime surfaces

### What must change
Do **not** lead with packet/code hardening.

Lead with:
1. workbook-to-test-family coverage truth,
2. retained-test registry integrity,
3. proof-block alignment,
4. then code migration/hardening in workbook order.

---

## 5. Corrected ordered queue — next 15 bounded steps

### Phase A — close test authority against the workbook benchmark

#### 1. Re-anchor the bounded pack
Read in order:
- `AGENTS.md`
- `migration_prebuild/AGENTS.override.md`
- `migration_prebuild/00_hierarchical_order.md`
- workbook `01_nvda_best_practice_blueprint_v3_final.xlsx`
- `migration_prebuild/03_nvda_test_ordering_review_2026-04-18.md`
- `migration_prebuild/04_rebuild_execution_order.md`
- `migration_prebuild/06_tier_family_normalisation.md`
- `migration_prebuild/07` through `11`

#### 2. Build a workbook-to-native-test crosswalk
Use these workbook sheets as the benchmark:
- `Target_Structure`
- `Ownership_Matrix`
- `Seam_Contracts`
- `Persistence`
- `Test_Architecture`
- `Reservations`

For each workbook benchmark family, classify:
- covered by Tier A
- covered by Tier B
- deferred lawfully
- missing
- present but too broad

#### 3. Produce the benchmark family matrix
The matrix must cover at least the workbook benchmark families in `Test_Architecture!A4:H20`, including:
- schema/contract tests
- reference containment tests
- seam tests
- mapper tests
- deterministic function tests
- packet construction tests
- modifier tests
- parallel-lane tests
- capital authority tests
- persistence tests
- migration tests
- shell honesty tests
- bridge containment tests
- calendar subsystem tests
- analysis subsystem tests
- specimen-path harness tests

#### 4. Reconcile the crosswalk against `config/retained_test_registry.yaml`
Check whether every workbook family is represented by:
- one or more admitted native families,
- or an explicit deferred disposition.

#### 5. Reconcile the crosswalk against actual test files
Check that every active test file under:
- `tests/tier_a/`
- `tests/tier_b/`

is admitted in the registry and mapped to a workbook benchmark family.

#### 6. Identify unresolved predecessor/successor truth
Find any remaining case where:
- a broad predecessor still exists without full successor coverage,
- or a successor exists without explicit predecessor retirement truth,
- or workbook coverage is only implied rather than explicit.

#### 7. Reconcile proof-block execution with admitted families
Check `config/proof_blocks.yaml` so proof execution only points at admitted blocker families and does not silently rely on stale mixed predecessors.

#### 8. Add a durable registry-integrity proof
Create or tighten a proof that fails if:
- a Tier A/Tier B file is not admitted in the registry,
- a workbook benchmark family has no mapped native family or lawful defer,
- a predecessor is retired without successor coverage.

### Phase B — only then continue code migration/hardening

#### 9. Contracts/schema truth pass in workbook order
Follow workbook benchmark and rebuild order:
- `contracts/common.py`
- `contracts/temporal.py`
- `contracts/regime.py`
- `contracts/options_flow.py`
- `contracts/posture.py`
- `contracts/eligibility.py`
- `contracts/execution.py`
- `contracts/risk.py`
- `contracts/parallel_risk.py`
- `contracts/capital.py`
- `contracts/downstream.py`
- `contracts/review.py`
- `contracts/reference_data.py`
- `contracts/packets.py`

#### 10. DMP packet-carriage tranche
Only after the contract/blocker families are stable:
- reconcile `contracts/packets.py`
- reconcile `packets/dmp_packets.py`
- decide whether `schemas/dmp.py` and `schemas/dmp_envelope.py` are the next lawful native admission or still blocked by test-architecture gaps

#### 11. Reference containment and calendar projection tranche
Then truth-pass:
- `reference/calendar_import.py`
- `reference/calendar_projection.py`

against workbook seams:
- `Calendar reference bundle -> calendar runtime context` — `Seam_Contracts!A7:N7`
- calendar subsystem benchmark family — `Test_Architecture!A18:H18`

#### 12. Preparation seam tranche
Truth-pass:
- `preparation/runtime_preparer.py`

against workbook seam:
- `Raw bundle -> prepared runtime substrate` — `Seam_Contracts!A8:N8`
- preparation seam benchmark family — `Test_Architecture!A7:H7`

#### 13. Ingress mapper tranche
Truth-pass:
- `cognition/ingress/temporal_mapper.py`
- `cognition/ingress/regime_mapper.py`
- `cognition/ingress/options_mapper.py`
- `cognition/ingress/translator.py`

against benchmark families:
- ingress translation — `Test_Architecture!A8:H8`
- regime completeness reservation — `Reservations!A4:I4`

#### 14. Deterministic serial/runtime tranche
Truth-pass serial deterministic owners in workbook order before widening services:
- temporal
- regime
- options flow
- posture
- eligibility
- execution expression
- modifier lane
- parallel risk
- final risk join
- capital authority

#### 15. Persistence/downstream/deferred-family tranche
Then continue with:
- persistence domain ownership proof from `Persistence!A4:K15`
- downstream shell honesty from `Bridge_Shell_Policy!A8:H10` and `Test_Architecture!A16:H16`
- replay/scenario containment from `Test_Architecture!A19:H19`
- re-evaluate the deferred Tier B families only if their native architecture has been lawfully admitted

---

## 6. Outstanding items that still carry forward

These remain the top carried-forward outstanding items:
1. **Vocabulary reconciliation** — still required before admitting new durable runtime terms; see `migration_prebuild/02_vocabulary_dictionary_system_audit.md:22-47`
2. **Replay/review lineage family** — still outstanding, but only lawful once the owning native review/replay surfaces are admitted
3. **Upstream non-interference / sanity-trace family** — still outstanding, but still architecture-dependent
4. **Upstream coverage-map / dataset-packet family** — still blocked until the native raw-signal coverage and dataset-packet architecture exists

---

## 7. Practical rule for future execution

Use this stop/go rule:
- **Do not migrate or rewrite more code just because the workbook names a target module.**
- First prove that the workbook benchmark family is protected by an admitted native test family or an explicit lawful defer.
- Then move one bounded code family only.
- Then rerun the blocker shell and update the retained registry / receipts.

That is the natural continuation of the rebuild.
