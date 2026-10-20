# NVDA V2 — M01→M02 reuse and pre-test specification: task-local ExecPlan

**Status:** PROPOSED TASK PLAN — DOCUMENTARY PREPARATION ONLY; NOT THE ACTIVE ROOT `EXEC_PLAN.md`; NOT IMPLEMENTATION, PROOF OR PROGRAMME ACCEPTANCE.
**Date:** 20 October 2026 (Melbourne). **Branch:** `work/v2-g6-m01-m02-reuse-prep-20261020`.
**Pinned inspection base:** `19c14ee461140649110d5d1cc4c1d5d7f40123be` (tree `dc2b9fe81de02a5d2a381589f3947283d202e6ba`). This is the saved D014 generation-2 checkpoint, not the concurrent worker's live state. Recheck authority and ancestry on every resumed pass.

## Objective and decision boundary

Prepare an **evidence-linked, reuse-first specification** for the **126 conditionally eligible strategy-independent foundation D-signals**, so the Gate 6 implementer can reuse existing M01 mathematics, history/selection experience and proof lessons without re-deriving them or accepting legacy implementation assumptions. Preserve the **83 downstream D-signals** and all 209 canonical IDs. The immediate deliverable is a traceable 126-row crosswalk plus bounded, family-specific input/expected-value/history specifications and an explicit gap list. It is **not** 126 new executable tests, a new M02 implementation, or authorisation to enable any D-signal.

**Authority:** Current user commission permits preparation and local documentary commits on this isolated branch. Read `GUARDRAILS.md`, applicable `AGENTS.md` and the live root `EXEC_PLAN.md` before substantive work. Those govern over this draft. The root remains the **sole active programme ExecPlan**; a task-local plan cannot amend its G6 admission/acceptance boundaries or change any authority/contract. Review a latest worker snapshot at handoff; do not assume this saved base is current.

**Allowed writes:** Only `handoff/foundation_implementation/reuse_preparation/` on this isolated branch: this plan and subsequent crosswalk/packet/gap/handoff files. A separate output workbook may be produced only if useful, and must be supported by the same repository-linked crosswalk. Ordinary Git commits, a self-contained branch bundle and disposable recovery verification are allowed.

**Prohibited writes/actions:** No root `EXEC_PLAN.md`, `GUARDRAILS.md`, `AGENTS.md`, accepted brief/catalogue/workbook, original M01/M00/M02 implementation, tests, controls, admitted generations, manifests or native bindings; no provider integration/calls, DB migration, PostgreSQL removal, SQLite schema changes, source collection, strategy work, full G6 admission, M01 retirement, main merge or rewrite/prune of Git history. Existing tests are **evidence to inspect**, not accepted M02 proof or files to copy wholesale.

## Primary sources and interpretation

Read the actual bytes, not inherited completion labels. Resolve precedence and effective amendments before describing each ID:

1. Root `EXEC_PLAN.md` §7, accepted Gate 2–4 dispositions, `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annex B and incorporated effective calculations/overlays (historical suffix `PROPOSED` does not by itself decide current authority).
2. `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS08.xlsx`, original 209-row catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` and later accepted classification/contract corrections. The workbook is **source and identity evidence**, not automatic proof that a provider is integrated or that an old 114-row M01-1 proposal is still current.
3. Prior reuse audit `handoff/workbook_v2/reviews/m01_m011_semantic_audit_20261014/M01_TO_M01_1_SEMANTIC_REUSE_AUDIT.md` and `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md`, used as starting evidence to *recheck*, not as final authority.
4. M01 source `src/nvda_desk/derived_signal_calculation_truth/`, existing `tests/product/derived_signal/`; accepted M02 boundary `src/nvda_desk/market_measurement_truth/`, actual M00 public API and SQLite owner contracts. The legacy M01 PostgreSQL adaptor is historical engineering evidence only; do not transfer its isolation assumptions.
5. Relevant accepted source/field mappings; where IBKR/FRED/Cboe or other native-provider details are unresolved, identify an exact mapping question for the upstream research worker rather than assuming a native range or collecting fresh source data.

**Three separate statuses per row:** (a) accepted **mathematical law**; (b) **existing M01 engineering evidence** (source/tests); (c) **M02 production/source/proof readiness**. A path existing in M01, a passing legacy test, or a synthetic input is not M02 acceptance. `VERIFIED`, `INFERRED`, `UNKNOWN` and `BLOCKED` must be independently usable per field; don't collapse a row into one optimistic status.

## Execution method — one semantic preparation unit per pass

Work autonomously within the permitted documentary scope. Advance only after the prior leaf's concrete exit is evidenced. Prefer a compact family packet over per-ID receipts. Keep reports brief: exact leaf, changed files, new supported findings, first blocker and next leaf. Do not create redundant plans, ledgers, speculative control designs or repeated validation logs. Read authoritative source ranges in full when needed; preserve path, Git ref, symbol/line or workbook row for each substantive mapping. A bounded read-only extraction script is permitted **outside the repo** if it only indexes evidence; generated assertions must be checked against primary sources.

| Leaf | Work and dependencies | Exit criterion / evidence |
| --- | --- | --- |
| **P0.1 — Baseline** | Record branch/HEAD/tree/clean state; read governing files, current G6 acceptance and exact 126/83 identity authority. | One pinned source inventory, no governance conflict; D011–D014 state clearly labelled **snapshot-only**. Stop if authority set cannot be reconciled. |
| **P0.2 — Census** | Establish exact 126 foundation IDs from current Annex B/effective register; account for the complementary 83 downstream; reconcile old 114/95 and Stage-1/2 classifications as historical, not active owners. | `M01_M02_REUSE_CROSSWALK.csv` has **exactly 126 unique accepted IDs**, no missing/duplicate/unknown ownership, each with an authority reference. Separate 83 count cross-check; unresolved authority stops affected rows. |
| **P1.1 — Source/logic reuse** | For one dependency-closed mathematical family, trace each ID to original M01 source symbol/branch, existing public/fixture source, M00 raw inputs, predecessors and current M02 seam. Explicitly identify nonexistent Stage-2 logic and strategy-coupled code. | Family packet documents `REUSE_AS_SPEC` / `REEXPRESS` / `NOT_REUSABLE` / `UNKNOWN`, with exact locations and reasons. No private M01 runtime import is proposed. |
| **P1.2 — Historical/fixture reuse** | For the same family, extract existing M01 selection, window, session/calendar, timestamp, provenance, pagination, restart and negative-case preconditions. Separate legacy PostgreSQL-specific fixtures from backend-neutral mathematical propositions. | Every applicable historical scenario identifies input cardinality and ordering, trigger condition, selected output/refusal, and source evidence; explicit `UNKNOWN` where not defined. A fault fixture must be capable of reaching its intended fault without first exhausting the upstream history, learning from D014. |
| **P2.1 — Parameters and expected values** | For the audited family, specify exact accepted equation/units/representation, synthetic valid/invalid inputs, independently calculated expected results, exact boundaries and mismatch/refusal conditions. Use existing accepted mathematical work rather than inventing a new model. | Family packet contains individually attributable mathematical witnesses with calculations **independent of production implementation**. Do not invent typical provider ranges as rejection bounds. |
| **P2.2 — Native/source holds** | Distinguish controlled mathematical admissibility from provider-certified data. Reconcile provider field, units, temporal meaning, version, missing/sentinel and input-profile holds against accepted source mapping. | Each claim is `ESTABLISHED` with source reference or `UNKNOWN/BLOCKED` with a precise question/receiver. Historical fixture readiness does not promote native eligibility. |
| **P3.1 — Family review** | Repeat P1–P2 for further families in dependency order. Before calling a packet ready, independently challenge one direct mathematics witness and one source/history/negative witness without relying solely on the original M01 fixture helper. | One reviewed family packet per family, corrected crosswalk, explicit dependent holds; no unproved global statement that all signals in a family are test-ready. Independent reviewer judgement where required by current authority; this task plan does not manufacture independent acceptance. |
| **P3.2 — Handoff and reconciliation** | Reconcile all 126 rows and family packets to the accepted inventory; distinguish fully prepared, source-held, model/calendar-held and not-yet-audited. Identify reusable cross-family mechanisms separately from signal-specific equations and proof. | Bounded implementation-facing specification + `OPEN_GAPS.md` + `HANDOFF.md`, exact candidate/commit/tree; no synthetic source-certified claims, no omitted ID and no silent activation. |
| **P3.3 — Transfer** | Commit documentary output; verify changed paths/ancestry; create a Git bundle; import into a fresh disposable checkout and compare branch HEAD/tree/content. | Verified recovery, original history retained. Hand off the bundle as **proposal material** to the worker, who independently reconciles it against its live branch and accepted root plan before any use. |

### Crosswalk minimum columns

`D_id`; `accepted_name`; `authority_ref`; `family`; `neutral_eligibility_status`; `raw_R_refs`; `derived_D_predecessors`; `M01_source_path_symbol`; `M01_test_paths`; `existing_fixture_semantics`; `M02_current_seam`; `reuse_disposition`; `required_inputs_units_shapes`; `exact_equation_ref`; `history_window_time_rules`; `controlled_expected_witness_ref`; `native_mapping_status`; `hold_receiver`; `evidence_commit`; `readiness_status`.

A blank is not a successful unknown. Use `UNKNOWN` or `NOT_APPLICABLE` with a reason; a row's `M01_source_path_symbol` may legitimately be `NOT_IMPLEMENTED` and must not be backfilled from historical claims.

### Family packet: maximum useful content, no new proof bureaucracy

One compact Markdown packet per genuine compatible family (rather than one receipt per D): ID/dependency list; authority deltas versus M01; pointers to existing code and tests; reusable/non-reusable logic; explicit equation and independently evaluated witnesses; fixture cardinality/timing/history/fault prerequisites; provider/source holds; what a future independent M02 proof still must establish. Do **not** assume scalar shape or generic history for option surfaces/ordered book. Keep verified source observations separate from design proposals. A packet can be `PARTIAL/BLOCKED`; do not require the entire 126 census to be semantically closed before reporting honest partial progress.

### Stop conditions and changes of authority

At first missing or contradictory authority, hash/ancestry/integrity failure, or inability to establish the claimed semantic reuse: preserve the observed state, stop only dependent leaf work and name the precise unresolved proposition. Continue genuinely independent documentary families if their dependency closure is established. Do not patch production or write tests to fill an evidence gap. A future change to the active root plan, proof controls, source contracts, calculation shapes, acceptance batching or independent-review obligations requires its **own exact applicable authority** and is outside this preparation tranche.

## Completion definition and progress

A successful **preparation tranche** is a reproducible 126-row evidence crosswalk plus the audited family packets that can actually be established, with explicit uncovered/blocked material, reviewed independent expectations and an integrity-verified Git bundle. The goal is **reduced duplicate reasoning**, not a fabricated FULL126_COMPLETE or a numerical speed-up claim. Record for each family the time spent (measured where available), existing source/test references reused, genuinely new specifications, unresolved questions and review rework; the downstream worker can later compare actual implementation throughput. This plan neither discharges G6.1–G6.4 obligations nor retires M01.

**Progress at document creation:** PLAN DRAFTED ONLY. P0.1–P3.3 **NOT_EXECUTED UNDER THIS PLAN**. The earlier exploratory spreadsheet is candidate evidence, not an admitted output of these leaves.

## GPT-6 prompting basis (advisory, not repository authority)

OpenAI's current GPT-6 guidance favours direct outcomes and sufficient context, lean instructions, explicit autonomous-action/approval boundaries, calibrated verification and concise reporting. These practices inform the plan's one-family-per-pass structure and scoped exit criteria; they do not override project governance:

- https://developers.openai.com/api/docs/guides/latest-model
- https://openai.com/index/practical-guide-building-gpt-6/
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
