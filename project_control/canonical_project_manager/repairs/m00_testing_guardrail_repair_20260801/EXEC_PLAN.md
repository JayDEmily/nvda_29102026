# NVDA M00 Testing Guardrail Repair ExecPlan

**Status:** `ACTIVE:CONTROL_REGISTRATION`
**Created:** 2026-08-01
**Owner:** User-authorised worker under the canonical Project Manager plan
**Canonical parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Baseline branch:** `work/signal-phase-dmpv3-repair-v1`
**Baseline commit:** `258470526c36da61b3ff4162f1d5ad9e512a8b54`
**Worker branch:** `work/m00-testing-guardrail-repair-v1`
**Current-target full-read manifest:** `project_control/canonical_project_manager/repairs/m00_testing_guardrail_repair_20260801/FULL_READ_MANIFEST.tsv`
**Accepted audit input:** `project_control/canonical_project_manager/repairs/m00_testing_guardrail_repair_20260801/PRE_EXECUTION_AUDIT.md`

## 1. Relationship to the canonical ExecPlan

This is a bounded subordinate repair plan. It does not replace, supersede or reinterpret the canonical alpha-delivery ExecPlan. The canonical plan remains the single live programme authority and opens this repair as a prerequisite to M00 final composition.

Accepted M01–M13 implementation history and the signal-phase/DMPV3 repair remain intact. M00 remains not started until this plan establishes a trustworthy current promotion gate and admits M00 normative/proof authority.

## 2. Objective

Before M00 production composition:

1. make test admission machine-readable and internally consistent;
2. establish one authoritative aggregate promotion route that resolves and executes the exact current blocking set;
3. make CI and the declared environment use that same route and authority;
4. produce reproducible evidence with Git, environment, membership and outcome identity;
5. admit M00 C-NORM and expected-red C-PROOF before implementing M00; and
6. implement M00 only against the admitted composition laws, without reopening accepted module meaning or promoting the quarantined legacy orchestrator.

## 3. Scope

### In scope

- `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` schema, lifecycle and reconciliation;
- repository-owned validators, resolvers, aggregate proof execution and receipts;
- relevant Make targets and GitHub workflows;
- locked-environment and installed-package smoke proof;
- the stale current-pack declaration in `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`;
- contradictory current/legacy API test lifecycle classification;
- exact normative proposition traceability for current blocking proof;
- M00 normative authority, expected-red proof, bounded implementation and final alpha composition validation;
- current-target manifests, concise validation summaries, canonical-plan/roadmap updates and Git checkpoints.

### Out of scope

- rewriting accepted M01–M13 domain semantics without a failing current proposition;
- live brokerage, live data, production durability, profitability or operational-readiness claims;
- blanket deletion, skipping, xfail, deselection or assertion weakening to create greenness;
- repository-history rewrite, rebase, squash, merge, push or publication;
- converting historical physical Tier A placement into authority by folder location alone.

## 4. Invariants

- Authority remains `user → canonical brief/plan → AGENTS/overrides → this subordinate plan → normative documents → admitted tests → implementation`.
- Normative meaning precedes proof; proof precedes implementation.
- One canonical admission model must determine current blocking, current nonblocking, next-gate expected-red, superseded compatibility and historical lifecycle.
- The aggregate gate must fail closed on invalid authority, unexplained membership, missing/red/skipped/collection-failed/timed-out blockers or dirty governed state.
- Fast module-local commands remain useful but cannot be represented as aggregate promotion proof.
- M00 owns translation, dependency composition and run lifecycle only; it must not own source truth, policy defaults, business decisions, fabricated identity or module-global mutable domain state.
- M03 remains the prepared-context parent; M05/M06 cross into M09 through validated DMPV3 carriage; M09 canonical ingress remains packet-only.
- The legacy `DeskRuntimeOrchestrator` remains noncanonical.

## 5. Acceptance units

### Unit 0 — Register the repair

**Pass:** clean baseline confirmed; worker branch created; this subordinate plan, audit input and current-target manifest committed; canonical ExecPlan and roadmap point to this repair without replacing the canonical plan.

**Fail:** competing live plan, branch ambiguity, dirty overlapping worktree or missing accepted audit evidence.

### Unit 1 — Repair and define admission authority

**Required reads:** both authority files in full, all current proof-model validators/tests, all physical test paths implicated by reconciliation.

**Pass:** registry and proof manifest parse; schemas reject duplicate IDs/paths, invalid tiers/lifecycles and invalid references; each current test has an explicit lifecycle; proof blocks resolve through admitted test-family IDs rather than independent unexplained path authority; exact proposition locators exist for blockers.

**Validation:** schema and reconciliation tests, malformed/duplicate fixtures, zero unexplained membership.

### Unit 2 — Reconcile current control and test authority

**Pass:** active pack/state agrees across canonical ExecPlan, roadmap and process overlay; legacy/current API assertions have explicit non-conflicting lifecycle; expected-red next-gate proof is visible but excluded from current green promotion until its gate opens.

**Validation:** active-control singleton proof and authority-precedence/conflict tests.

### Unit 3 — Implement the aggregate promotion gate and receipts

**Pass:** one repository command resolves the exact current blocking set, validates both authorities, executes every blocker, fails closed on all prohibited states, checks pre/post Git state and writes a sufficient receipt containing commit, branch, environment/lock identity, resolved membership, counts, duration, command and evidence hash.

**Validation:** resolver unit/property tests, broken-registry and omitted/stale/skipped/failing specimens, receipt-schema/tamper tests and an aggregate control test.

### Unit 4 — Make CI and environment authoritative

**Pass:** Make consumes the lock authority; one installed-package smoke route avoids source-tree import masking; workflows call repository-owned validation/promotion commands and do not duplicate retired schemas or hard-coded counts.

**Validation:** workflow/static contract tests, locked-install command validation where the configured index permits, installed-package smoke and explicit environment receipt. External index unavailability is recorded, not substituted.

### Unit 5 — Establish the current pre-M00 promotion baseline

**Pass:** the aggregate current blocking set is green and reproducible; all expected-red or historical tests are separately and explicitly classified; Git is clean after the gate.

**Validation:** authoritative aggregate command plus Tier B shadow proof and relevant module-local blocks.

### Unit 6 — M00 C-NORM and expected-red C-PROOF

**Pass:** M00 laws are explicit for dependency direction, translation-only ownership, injected run scope, fail-closed authority, canonical cognition path, hermetic paper integration, replay distinction and legacy quarantine; the smallest public-seam proof family fails for the intended missing implementation and is admitted with an explicit next-gate lifecycle.

**Validation:** proposition traceability, expected-red reason, positive/negative/false-positive challenges and proof-authority reconciliation.

### Unit 7 — M00 bounded Gate D implementation

**Pass:** one canonical application composition root uses only declared M01–M13 public seams; all time/identity/configuration/repositories/services are injected; no cross-run state leaks; missing authority fails closed; no synthetic defaults or hidden re-evaluation path; the legacy orchestrator cannot be selected canonically.

**Validation:** targeted M00 proof, affected module proof, DMPV3 lineage, state isolation, deterministic replay semantics, architecture/dependency and vocabulary checks.

### Unit 8 — Final validation and closeout

**Pass:** aggregate promotion gate and Tier B shadow pass; no unexplained new failure; canonical plan, roadmap, validation log and this plan record exact evidence; one bounded final checkpoint exists with a clean worktree.

**Artefacts:** concise validation summary, receipts, hashes, commits and full-history checkpoint when requested or required by closeout authority.

## 6. Prohibited shortcuts

Do not:

- treat `run_proof_block.py --check-all` as execution proof;
- make the physical `tests/tier_a` directory the blocking set by convenience;
- hard-code test counts in CI;
- weaken or suppress current red evidence;
- silently demote or promote tests;
- allow proof manifests or registries to create normative meaning;
- begin M00 code before C-NORM and expected-red C-PROOF pass;
- repair the legacy orchestrator piecemeal into a competing canonical owner.

## 7. Validation record

Record commands and observed outcomes under:

- `project_control/canonical_project_manager/repairs/m00_testing_guardrail_repair_20260801/VALIDATION_SUMMARY.md`
- repository-owned aggregate receipts under a path defined and tested in Unit 3.

Successful raw output is not committed by default. Novel failures, non-determinism and material environment failures are retained as evidence.

## 8. Progress

- 2026-08-01: user accepted the pre-execution audit and authorised worker execution.
- 2026-08-01: baseline `2584705` confirmed clean; branch `work/m00-testing-guardrail-repair-v1` created.
- 2026-08-01: Unit 0 opened.

## 9. Decisions

- The repair is subordinate to the canonical ExecPlan because it is a prerequisite control unit inside the same alpha-delivery programme, not a competing programme.
- M00 remains not started until Units 1–6 pass.
- Accepted M01–M13 local proof is retained; the repair targets admission, integration and promotion control before composition.

## 10. Roadblocks

None at plan creation.

## 11. Unknowns

- Whether the authorised package index can currently resolve every locked wheel remains Unknown until Unit 4 executes the canonical route.
- The final exact current blocking membership remains Unknown until Units 1–2 semantically classify and reconcile all differences.

## 12. Closeout

Open. No completion claim applies until Unit 8 passes.
