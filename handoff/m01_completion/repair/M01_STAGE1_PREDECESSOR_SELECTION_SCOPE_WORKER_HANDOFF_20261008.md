# M01 Stage-1 predecessor-selection scope — worker repair candidate

## Authority and reviewer disposition

- Governing files: root `GUARDRAILS.md`, root `AGENTS.md`, `tests/AGENTS.override.md`, accepted root `EXEC_PLAN.md` Stage 1, and exact accepted M01 brief/catalogue indexed by `handoff/m01_completion/AUTHORITY_INDEX.md`.
- Incoming independent review: `handoff/m01_completion/review/M01_STAGE1_REVIEW_RESULT_8446b5944a029cc944530588a6dcfcb9cf08bbfc.json`.
- Reviewer verdict: `REPAIR`, classification `RECURRENT_CLASS`, route `RETURN_TO_WORKER_STAGE1`; reviewed Worker HEAD `8446b5944a029cc944530588a6dcfcb9cf08bbfc`.
- Incoming repair-handoff commit: `0cbf318e575a2f36c30bd3947f54a58bcf0d68e2`.
- Repair scope: parent/child selection granularity for aggregate D109 and candidate D170 resolving exact contract predecessor D087 (and D109's exact D091 delta-bucket dependency) through the public M01 calculation seam. Stage 2 remains unauthorised.

## Observed failure and bounded repair

The rejected Stage-1 candidate recursively reused the parent's selection reference when evaluating narrower predecessor rows. A parent pair or candidate structure cannot be both a lawful aggregate selection and the exact per-contract D087 identity for two different legs. The reviewer demonstrated absence via the public calculation seam in both D109 and D170, despite supplied inputs.

The change introduces immutable, explicitly versioned `predecessor_selection_policy_refs` on `CalculationRequestV1`, derives distinct exact-contract child requests only on the admitted D109/D087, D109/D091 and D170/D087 edges, and validates each selected occurrence against all five exact option-contract join keys. It also permits different raw bindings for different exact contract identities and refuses absent, ambiguous, mismatched or non-exact selections. Selection versions must respect parent temporal/identity policy limits.

D109 now uses its D091 predecessor's delta bucket to verify the accepted ATM pairing. D170 retains distinct leg contract identities (and their independent strike values) rather than collapsing both legs onto the parent underlying instrument. Parent and child occurrence IDs, version references and raw observation lineage remain separate and recoverable.

No D identifiers, catalogue edges, M00 persistence ownership, Stage-2 implementations, package version or governing documents were changed. The API extension is additive; missing required scoped-child policy fails closed.

## Proof-before-implementation history

1. `92a552e256386133b42b6e038b59fb944133503c`: public-seam failing proofs for D109 and D170 pair-to-contract selection and lineage.
2. `45ed9bd4b07609687536188c486f35ac05dd12eb`: negative proofs and multi-strike candidate proof.
3. `eb6bc05515558814cfa0c3de5d60a522116f6c02`: production repair; no original proof test was removed or weakened.

## Validation actually obtained on the production-repair tree

- `PYTHONPATH=.:src pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal` with the PostgreSQL-dependent cases listed below excluded: **620 passed**, 9.21 seconds.
- Public seam: `pytest -q tests/product/derived_signal/test_m01_stage1_predecessor_scope.py`: **12 passed**. Includes positive D109 (separate call/put D087 and D091) and D170 (per-leg D087) numerical answers, lineage and deterministic retries; refusal of missing underlying input/quote/delta, missing child policy, mismatched strike or non-ATM selection; and distinct-strike candidate legs.
- `make lint`: **Ruff: all checks passed**.
- `make typecheck`: **mypy: success, no issues found in 21 source files**.
- `PYTHONPATH=src make validate`: **structural architecture validator PASS; zero dependency/public-seam violations**.

Explicit exclusions, NOT PASSES: `tests/product/raw_signal/test_u05_postgresql_durability.py` (requires PostgreSQL), and `tests/implementation/derived_signal/{test_ds_t01_persistence_isolation.py,test_ds_t01_r02_persistence_boundary_refinement.py,test_ds_t01_r03_postgres_privilege_boundary_refinement.py,test_ds_t01_r04_postgres_privilege_surface_refinement.py,test_ds_t01_r05_postgres_role_membership_refinement.py,test_ds_t01_selection_lineage_persistence.py}` (requires `NVDA_TEST_M00_POSTGRES_DSN`). Database-backed isolation and durability are therefore **not newly proved by this repair**.

## Freeze boundary and reviewer request

The Worker requests fresh **independent Stage-1 review** of this exact next full-Git checkpoint. Proofs establish the D109 and D170 public-seam witnesses and negative paths above; they are not an independent proof of the entire 144-row Stage-1-closed population. The reviewer must independently assess whether the *class-level* graph-selection invariant is closed for other aggregate/grouping parents as required by authority. In particular, the newly added tests do not independently exercise D121/D122 multi-contract grouping through the public seam; no claim of proof for those row graphs is made here.

No Stage-1 acceptance, Stage-2 authorisation, or whole-M01 completion is claimed. The independent reviewer must decide the disposition.
