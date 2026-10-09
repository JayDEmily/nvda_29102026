# M01 F3 — contract/grouped predecessor closure and Stage-1 F4 entry boundary

Date: 2026-10-09. Governing authority: root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`; independent F2 `F2_ACCEPTED` at `30945dd` and `handoff/m01_completion/repair/M01_F3_AFTER_F2_ACCEPTANCE_WORKER_HANDOFF_20261009.md`. This is a **worker proof checkpoint**, not independent F3/Stage-1 acceptance.

## F3a — exact predecessor contracts

`b63978c` added adversarial public M00/M01 proofs for D109 separate call/put and D170 candidate-leg contracts. Both reused the prior versioned exact child policy mechanism rather than broadening selection or changing normative contracts. No F3a production change was required. Run log: `F3A_CONTRACT_GRAPH.log` (19 cases, including retained predecessor-scope cases). Inheritance of raw and direct-D lineage is asserted by the public results, including incompatible, incomplete and cutoff refusals.

## F3b — grouped D120

`6607996` and `c9ffe7c` commit the new red multi-contract public witnesses **before** the production repair; logs `F3B_GROUPED_PUBLIC_RED.log` and `F3B_GROUPED_BOTH_SIGNED_MEASURES_RED.log`. The pre-repair code selected unrelated derived occurrences by equal UUID and lost contract group membership.

`83bcc1a` repairs the admitted public recursive resolver and K08 grouping. D121 resolves each contract's D120 plus D091 with complete versioned exact-contract identity and computes signed contracts **and** signed premium notional by expiry, right and configured delta bucket. D122 similarly pairs each D120 to the same contract's D085 and groups by expiry and configured DTE band. Different contract inputs are not collapsed by equal derived IDs; no independent contract is inferred from a group label. Missing/mismatched child member, conflicting selection identities or policy versions, and invalid bucket definitions refuse a result. Per-contract raw and direct-D predecessor identities remain reconstructable in lineage. Run log `F3B_GROUPED_PUBLIC.log` (16 tests). The final invalid-DTE-bucket negative is additional post-repair regression evidence, not incorrectly characterised as an earlier red proof.

## F3c — bounded F1 reconciliation

Run `python handoff/m01_completion/proof/f3_20261009/f3_reconcile.py` from the repository (or any CWD). It rereads and checks exact F1 edge IDs/classes, previously accepted 18 F2 edges and nine F3 edges. Output: `F3_ALL_EDGES_RECONCILIATION.csv` (488 actual dependencies and one D007 zero-edge census sentinel), `F3_CLASS_COVERAGE.json` (all 21 classes) and `F3_CENSUS_READBACK.log`.

- RC10: 4 exact D109/D170 edges have bounded F3a public evidence.
- RC11: 5 D091/D121/D122 edges have bounded F3b public evidence. D124's two R edges **are not** F3b grouped proofs; D128's two D dependencies require Stage 2 and remain deferred.
- Previously F2-accepted scoped evidence: 18 independent edges. No F2/F3 edge overlap.
- The remaining 354 Stage-1-closed direct edges are **not individually reconciled to a public positive/adversarial proof by F3c**; this is an evidence status, **not** a claim their implementations are defective or that no tests exist elsewhere.
- The 107 cross-stage-classified dependency edges in the 488-edge census are not permission to implement Stage-2; Stage-1 has exactly 30 cross-stage rows (25 direct and five transitive only), which still require their own Stage-1 kernel/refusal evidence at F4.

## Executed checks and limitations

- `F3_FULL_REGRESSION.log`: 716 passed; `PYTHONPATH=.:src pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` with isolated M00/M01 PostgreSQL roles under pinned Python 3.13.5 and PostgreSQL 17.9. The first test collection attempt used `PYTHONPATH=src` and failed to resolve `tests.*`; adding the repo root corrected the *environment invocation*, not source or tests.
- `F3_M00_DURABILITY_*`: all 55 cases passed **in bounded groups**, not one uninterrupted suite. The initial 26–29 group printed three dots then timed out without a test result; it was discarded as proof, and cases 26–28 and case 29 were subsequently re-executed and all passed. The timed-out initial log is retained separately.
- `F3_RUFF_CHECK.log`, `F3_MYPY_ALL.log`, `F3_ARCHITECTURE.log`, `F3_FORMAT_CHECK.log`: repository-wide Ruff, 21-file source mypy, structural architecture (zero violations), and focused format checks pass.
- No M00 code, live economic-calendar provider adapters, strategy controls, normative CSV/brief, `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md` or package version were modified.

## F4 entry / non-acceptance

The next authorised unit is F4 reconciliation and complete Stage-1 revalidation, with **144 closed rows publicly reachable**, and **30 cross-stage rows** carrying own-kernel and fail-closed proof. Existing row dispatch/catalogue and selected K01–K17/controlled predecessor tests do not alone establish **every** required public graph through all 21 classes. In particular, the F1 proof matrix still identifies additional representative/public edge reconciliation obligations for RC03–RC06, RC12–RC17 and RC20–RC21. The 354 still-unreconciled Stage-1-closed edges **must not be marked PASS** merely on this F3 evidence. For F4, associate concrete positive and adversarial public tests with the applicable mechanisms/edges and demonstrate all 144 closed row reachability, including exact parameters, versions, context, cutoff, refusal and persisted lineage. Preserve the 30 deferred Stage-2 edges and independently prove their own Stage-1 behaviour. Only then freeze one Stage-1 F4 candidate for independent review. No F3-only reviewer gate is created; this checkpoint is an implementation recovery handoff, not Stage-1 acceptance.
