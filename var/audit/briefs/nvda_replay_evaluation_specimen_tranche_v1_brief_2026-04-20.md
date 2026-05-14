# NVDA replay-evaluation and specimen-path tranche v1 — executable brief

Date: 2026-04-20
Repo baseline used to write this brief: `work/persistence-migration-lifecycle-tranche-v1-20260420` at `3556388e0b76bc90676a48a5539906b491aeeb7a`
Current `main` observed while writing: `167fd520321ce3925ae9ebd96abe508d9af377e5`

---

## 1. Direct answer

Yes. The next bounded tranche is the replay/evaluation and specimen-path tranche.

This tranche exists to close the next highest-confidence benchmark drift after the accepted persistence tranche:

- admit the locked `nvda_desk.analysis.replay` home
- admit the locked specimen-path harness home under `nvda_desk.testing.harnesses`
- converge the locked research/evaluation persistence module cut to `src/nvda_desk/persistence/research_logs.py`
- add only the minimum truthful proof mirror required for those bounded surfaces

This tranche must **not** promote:

- `nvda_desk.analysis.scenarios`
- `nvda_desk.observability`
- `nvda_desk.legacy.imported`
- API DTO or broker-boundary reservation work
- replay/eval API routes or broad CLI expansion

This brief is executable. It is not an audit-only brief.

---

## 2. Mandatory execution setup

### 2.1 Promotion precondition before the tranche branch exists

The repo supplied with this brief is expected to be the accepted persistence tranche state on:

- `work/persistence-migration-lifecycle-tranche-v1-20260420`
- `HEAD = 3556388e0b76bc90676a48a5539906b491aeeb7a`
- `main = 167fd520321ce3925ae9ebd96abe508d9af377e5`

Before starting tranche work:

1. confirm the supplied repo still matches that accepted state
2. promote the accepted persistence tranche into `main`
3. confirm `main` now points to `3556388e0b76bc90676a48a5539906b491aeeb7a`
4. only then create the new tranche branch from that promoted `main`

Do not start the next tranche from stale `main`.

### 2.2 Work branch for this tranche

Create and use exactly this work branch:

`work/replay-evaluation-specimen-tranche-v1-20260420`

All leaves in this brief belong on that one tranche branch.

### 2.3 Mandatory reread before touching code or tests

Read, in order:

1. `AGENTS.md`
2. `migration_prebuild/AGENTS.override.md`
3. the ordered `migration_prebuild/` pack through `14_frozen_authority_and_mutability_law_2026-04-20.md`
4. `var/audit/README.md`
5. `var/audit/nvda_running_audit_log.xlsx`
6. `var/audit/briefs/nvda_persistence_migration_lifecycle_tranche_v1_brief_2026-04-20.md`
7. `var/audit/reports/nvda_persistence_migration_lifecycle_tranche_v1_report_2026-04-20.md`
8. `config/retained_test_registry.yaml`

Do not rely on memory of the prior tranche.

### 2.4 Workbook basis for this tranche

This tranche is grounded on the locked workbook by lineage, specifically:

- `Target_Structure!A23:G27`
- `Component_Skeleton!A42:H46`
- `Test_Architecture!A19:H20`
- `Reservations!A8:H10`

Interpretation fixed for this tranche:

- `nvda_desk.analysis.replay` is a **locked** target home
- `nvda_desk.testing` is already physically present, but the specimen-path harness cut under `testing/harnesses/canonical_runtime.py` is still missing
- `persistence/research_logs.py` is a locked module cut supporting replay/evaluation artefacts
- `analysis.scenarios` remains **provisional** and is **not** promoted in this tranche

---

## 3. Tranche objective

Converge the minimum truthful replay/evaluation and specimen-path architecture without widening into scenario execution, observability, API DTO work, or imported-module disposition.

At tranche closeout, the repo should truthfully contain:

- `src/nvda_desk/analysis/replay/`
- `src/nvda_desk/testing/harnesses/`
- `src/nvda_desk/testing/harnesses/canonical_runtime.py`
- `src/nvda_desk/persistence/research_logs.py`

And the proof mirror should make these bounded surfaces visible without pretending that scenario flows or observability are already admitted.

---

## 4. Current repo facts that this tranche must respect

Observed directly while writing this brief:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` is green at **90 passed**
- `python3 -m compileall src tests/tier_a tests/tier_b` is clean
- the accepted persistence tranche has **not yet** been promoted to `main` in the supplied repo state
- `src/nvda_desk/analysis/` does not exist
- `src/nvda_desk/testing/harnesses/` does not exist
- `src/nvda_desk/persistence/research_logs.py` does not exist
- `src/nvda_desk/repositories/research_logs.py` does exist and is the nearest current research/evaluation persistence surface
- replay-adjacent support already exists in:
  - `src/nvda_desk/contracts/replay.py`
  - `src/nvda_desk/contracts/trace_review.py`
  - `src/nvda_desk/testing/bounded_trace_review.py`
  - `fixtures/replay/`
  - `fixtures/trace_review/`
  - `fixtures/dmp_v3/`
- `src/nvda_desk/entry/cli.py` is intentionally still bounded to `inspect-config` and `run-once`

This tranche must build on those facts.

---

## 5. Ordered leaves inside this tranche

### Leaf 1 — Admitted owner audit for replay/evaluation and specimen-path surfaces

#### Objective

Confirm the truthful owner set for this tranche before moving code:

- replay/comparison service home
- specimen-path harness home
- research/evaluation persistence owner

#### Required outcome

The leaf must close with an explicit admissibility decision that this tranche owns exactly these benchmark targets:

- `nvda_desk.analysis.replay`
- `nvda_desk.testing.harnesses`
- `nvda_desk.persistence.research_logs`

#### Rules

- use the workbook rows named above as the benchmark source
- use the current native surfaces only as evidence for the truthful minimum cut
- treat `src/nvda_desk/repositories/research_logs.py` as current evidence, not as the benchmark-frozen owner
- keep `analysis.scenarios` outside scope even though the workbook reservation discusses replay/scenario split

#### Hard stop inside the leaf

If this leaf proves that one of those three targets is benchmark-wrong at the ownership level, stop the tranche and convert the tranche into a governance-blocker report rather than silently inventing a different architecture.

### Leaf 2 — Replay home convergence

#### Objective

Create the minimum truthful `src/nvda_desk/analysis/replay/` home and bind it to the already-admitted replay contracts without widening into scenario flows.

#### Required outcome

At minimum, this leaf must leave the repo with a physical replay home that exposes bounded replay/comparison services or functions consistent with the workbook benchmark.

The replay home must support the current bounded native meaning:

- replay of prepared/runtime artefacts or fixture-backed artefacts
- comparison of replay outputs
- no live order placement
- no raw ingress decode
- no scenario-family promotion

#### Rules

- keep the replay home analysis-only
- reuse existing bounded contracts where truthful, especially `src/nvda_desk/contracts/replay.py`
- do not use this leaf to redesign `entry`, `api`, `downstream`, or runtime orchestration
- if compatibility wrappers are required for existing callers, they must stay thin and honest

#### Hard stop inside the leaf

Do not create `src/nvda_desk/analysis/scenarios/` in this tranche.

### Leaf 3 — Research/evaluation persistence module-cut convergence

#### Objective

Move the research/evaluation persistence owner to the benchmark-shaped home under `src/nvda_desk/persistence/research_logs.py`.

#### Required outcome

At minimum, this leaf must leave the repo with a truthful persistence owner for replay/evaluation artefacts under the benchmark home.

If compatibility for current imports is still required, `src/nvda_desk/repositories/research_logs.py` may remain only as a thin wrapper or re-export.

#### Rules

- do not widen persistence business logic
- keep this module append-only and bounded to research/evaluation artefacts
- do not blend live execution state, opening policy, or observation persistence into this module

#### Hard stop inside the leaf

Do not redesign the wider `repositories/` package in this tranche.

### Leaf 4 — Canonical specimen-path harness convergence

#### Objective

Create the minimum truthful specimen-path harness under `src/nvda_desk/testing/harnesses/canonical_runtime.py`.

#### Required outcome

At minimum, this leaf must leave the repo with a bounded harness surface that can assemble or describe the admitted specimen-path inputs from existing fixture roots and bounded support contracts.

The specimen-path harness must stay honest about what it does and does not do.

It may use existing roots such as:

- `fixtures/dmp_v3/`
- `fixtures/replay/`
- `fixtures/trace_review/`

#### Rules

- keep the harness test-only
- do not make the harness a secret runtime orchestrator
- do not let scenario flows masquerade as replay or specimen-path truth
- do not require live brokers, live APIs, or full serial runtime execution merely to build the bounded harness surface

#### Hard stop inside the leaf

Do not widen `src/nvda_desk/entry/cli.py` or API routes in this tranche unless a minimal compatibility shim is the only truthful way to keep the specimen-path harness honest. Any such shim must remain boundary-only and must not become a feature expansion.

### Leaf 5 — Minimum truthful proof mirror for analysis subsystem and specimen path

#### Objective

Add only the minimum proof required to make the admitted replay/evaluation and specimen-path surfaces visible.

#### Required outcome

At tranche closeout, proof must cover the bounded surfaces touched in Leaves 2-4, including:

- replay home presence and bounded surface shape
- research/evaluation persistence owner presence
- specimen-path harness presence and boundedness
- continued separation from scenario promotion and live-core mutation where applicable

#### Rules

- keep proof families bounded to the touched domains
- prefer minimum truthful Tier A and Tier B additions rather than a broad new proof bundle
- update `config/retained_test_registry.yaml` only for the families actually admitted or revised in this tranche
- do not backfit tests to hide architecture drift

#### Expected proof floor at tranche closeout

Run exactly:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python3 -m compileall src tests/tier_a tests/tier_b`

#### Hard stop inside the leaf

Do not create scenario-only tests, observability tests, or imported-module tests in this tranche.

### Leaf 6 — Tranche closeout

#### Objective

Close the tranche truthfully and prepare the repo for audit.

#### Required outcome

The tranche report must truthfully record:

- the promotion of the accepted persistence tranche into `main`
- the new tranche branch name
- each closed leaf and its closing commit
- the proof commands and exact results
- any compatibility wrapper retained on purpose
- the post-tranche benchmark-home count and the remaining absent benchmark homes

#### Report content must include

At minimum, name whether these remain absent after this tranche:

- `src/nvda_desk/legacy/imported`
- `src/nvda_desk/analysis/scenarios`
- `src/nvda_desk/observability`

If `analysis.replay` closed successfully, it must no longer appear on the absent-home list.

---

## 6. Touched, read-only, and prohibited surfaces

### 6.1 Touched surfaces allowed in this tranche

Runtime / test surfaces that may be touched if required by the leaf queue:

- `src/nvda_desk/analysis/replay/**`
- `src/nvda_desk/persistence/research_logs.py`
- `src/nvda_desk/persistence/__init__.py`
- `src/nvda_desk/testing/harnesses/**`
- `src/nvda_desk/testing/__init__.py`
- `src/nvda_desk/repositories/research_logs.py` only as a thin compatibility surface if required
- `src/nvda_desk/contracts/replay.py` only if a bounded replay contract refinement is strictly required
- `src/nvda_desk/contracts/trace_review.py` only if a bounded harness contract refinement is strictly required
- bounded new test files under `tests/tier_a/**` and `tests/tier_b/**` that mirror the admitted families touched here
- `config/retained_test_registry.yaml`
- `var/audit/briefs/**`
- `var/audit/reports/**`
- `var/audit/nvda_running_audit_log.xlsx`

### 6.2 Read-only surfaces

These surfaces remain authority and must not be rewritten for convenience:

- the full frozen `migration_prebuild/` pack
- `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
- `docs/planning/2026-04-02_GATE159_WORKBOOK_LINEAGE_AND_CONSOLIDATION_AUDIT.md`
- `docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md`
- existing accepted tranche reports and briefs except for adding the new brief/report pair
- fixture roots under `fixtures/` unless a bounded harness leaf requires adding truthful non-runtime support content

### 6.3 Prohibited surfaces in this tranche

Do not touch these surfaces in this tranche:

- `src/nvda_desk/analysis/scenarios/**`
- `src/nvda_desk/observability/**`
- `src/nvda_desk/legacy/imported/**`
- `src/nvda_desk/api/**` except a boundary-only shim if Leaf 4 proves it is strictly unavoidable
- `src/nvda_desk/entry/**` except a boundary-only shim if Leaf 4 proves it is strictly unavoidable
- `src/nvda_desk/adapters/egress/api_dto_adapter.py`
- `src/nvda_desk/adapters/egress/broker_protocol.py`
- `src/nvda_desk/downstream/**`
- `src/nvda_desk/cognition/**`
- packaging, offline bundle, or `.venv` method surfaces
- governance-document rewrites inside `migration_prebuild/`

If a prohibited surface becomes necessary, stop and record the blocker rather than widening the tranche silently.

---

## 7. Proof and acceptance standard

This tranche is accepted only if all of the following are true:

1. the accepted persistence tranche was first promoted to `main`
2. the tranche branch is exactly `work/replay-evaluation-specimen-tranche-v1-20260420`
3. each closed leaf has its own closing commit
4. the replay home exists truthfully and remains analysis-only
5. the specimen-path harness exists truthfully and remains test-only
6. the research/evaluation persistence owner exists under `src/nvda_desk/persistence/research_logs.py`
7. scenario, observability, imported-module, DTO, and broker-boundary work did not leak into this tranche
8. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` is green
9. `python3 -m compileall src tests/tier_a tests/tier_b` is clean
10. the ledger and tranche report record the tranche truthfully

---

## 8. Definition of done

### Outcome A — direct code convergence succeeded

Use this outcome only if:

- the persistence tranche was promoted to `main`
- the replay/evaluation/specimen-path tranche completed on the named branch
- all required proofs passed
- the tranche report and live ledger were updated truthfully

### Outcome B — governance blocker proved first

Use this outcome only if Leaf 1 proves that one of the benchmark targets for this tranche is wrong at the ownership level and the proof is documented explicitly.

A vague feeling that the architecture is messy is not a governance blocker.
