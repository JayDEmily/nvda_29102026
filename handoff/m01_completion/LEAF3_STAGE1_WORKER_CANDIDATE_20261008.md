# M01 Stage 1 — Leaf 3 Worker Candidate Handoff (2026-10-08)

## Scope, authority and acceptance boundary

- Current user instruction: **complete Leaf 3 only** from the frozen Leaf-2 full-Git checkpoint; return a single full-Git Stage-1 candidate to the independent Reviewer, then stop.
- Governing sources: root `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, accepted `EXEC_PLAN.md` §4 Leaf 3, and the exact M01 accepted authority indexed in `handoff/m01_completion/AUTHORITY_INDEX.md`.
- The accepted brief digest is `603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c`; the normative catalogue digest is `63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5` (rechecked during this pass).
- **This is a Worker-submitted candidate, not a Stage-1 Reviewer PASS, M01 completion, promotion or authorisation to start Stage 2.**

## Provenance, chronological proof and implementation history

Input Leaf-2 full-Git HEAD: `42092dc156ed5b43b8169f32ef2f46c94f61994d`. The following Git commits exist on `work/m01-completion`, in chronological order:

1. `455b2ead953976a8488a8860bc6d16b9ec38e485` — initial authority-catalogue census and *failing* proof for D008, D145, D155 and D173.
2. `41396b6ca77c1b50b2578e6c0db235284f9a741d` — corrected/strengthened proof fixtures: complete D155 component schema and public R187–R190 OFI inputs. This precedes the production repair.
3. `e1e7664ce12481440040042a9a7686056ed6a4f9` — production repair for D008 structured quality output, exact D173 candidate neighbours, canonical D155 metadata-carrying assembly and D145 event-derived best-book OFI.
4. `cfb3331cc22c1942a157bd66eca1e89adabaedbe` — *failing* adversarial proof for D082 zero-variance regression, D191 absent liquidation quantity/multiplier, D176 missing risk multipliers and D139/D140 missing rate windows.
5. `e3fafcc88cb541c8bae5f358114bd958eb4722e1` — production refusal repairs for those missing numeric prerequisites and D141 replenishment window.
6. `1de84e62fb6612bd6eb66be7862eb0f1e3dc6280` — final all-row kernel dispatch and static branch-marker proof. This adds no production code.

At the end of entry 6, only these previously existing files differ from the Leaf-2 code/test tree: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py`, `tests/product/derived_signal/test_m01_stage1_semantics.py`; additionally `tests/product/derived_signal/test_m01_stage1_leaf3_catalogue_kernels.py` is new. This handoff is the only new control document.

## Complete population and kernel-proof boundaries

- Exact accepted catalogue: **209 rows**, of which **174 Stage-1 rows** belong to ten Stage-1 families; the other **35 rows are not implemented by this Stage-1 dispatch**.
- Breakdown: K01 10, K02 57, K03 33, K04 9, K05 8, K06 7, K07 24, K08 24, K16 1, K17 1.
- The Leaf-3 tests assert catalogue-order identity, exactly one authorised parameter profile, mandatory typed profile conjunction, absence for unauthorised profiles, explicit Stage-1 dispatch exactly once for each of 174 rows, and static row-handler markers for row-specific branches. These are *binding and routing proofs*, not 174 independently proven numerical calculations.
- Representative numerical and adversarial kernel proofs are in `tests/product/derived_signal/test_m01_stage1_semantics.py`, `tests/product/derived_signal/test_m01_stage1_leaf3_catalogue_kernels.py`, and the preceding selection and graph suites.
- D145 proof exercises authorised raw catalogue inputs R187/R188/R189/R190 rather than synthetic internal `__book_states__`. D155 proof requires all nine declared dependencies, fixed order, units/quality/freshness preservation and occurrence identity. D173 proof restricts comparisons to directed declared neighbour identities. D008 proof checks structured output/coverage/skew.
- Regressions additionally check absent windows, invalid/degenerate model quantities, and refusal of fabricated default multipliers.
- The existing public materialiser refuses Stage-2 calculation of K09–K15. Stage-1 kernel-side D173 testing uses explicitly supplied predecessor values because its normative D165 predecessor is K13 (Stage 2). This pass does **not** claim to demonstrate a full public D173 materialisation with a Stage-2 D165 predecessor; such an integration proof cannot be substituted by a pure-kernel positive test and remains an explicit independent-review/future-stage evidence boundary.

## Executed validation (at the Leaf-3 code/test HEAD prior to this handoff commit)

Tools: Python 3.13, pytest 9.0.3, Ruff 0.15.11, mypy 1.20.1 from an out-of-tree recovered virtual environment; PyYAML 6.0.3 supplied by `/opt/pyvenv/lib/python3.13/site-packages`, via `PYTHONPATH=src:/opt/pyvenv/lib/python3.13/site-packages`. No proof-environment binaries enter Git.

- `python -m pytest -q tests/product/derived_signal`: **108 passed**.
- `python -m pytest -q tests/architecture tests/bootstrap`: **74 passed** with PyYAML available.
- `python -m pytest -q tests/product tests/architecture tests/bootstrap --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`: **606 passed**.
- `ruff check src tests tools`: **all checks passed**.
- `python -m mypy src/nvda_desk/derived_signal_calculation_truth`: **no issues in 5 files**.
- `python -m mypy src`: **no issues in 21 source files** with the above PyYAML available.
- `make validate PYTHON=/mnt/data/leaf2_workspace/proof_env/bin/python`: **structural architecture PASS**; **zero dependency/public-seam violations**.
- `git diff 42092dc --check`: passed.

These results establish precisely the exercised suites/validations; they do not constitute independent semantic acceptance. The M00 PostgreSQL durability suite requires `NVDA_TEST_POSTGRES_DSN` and is excluded from the reported 606-test run. No claim is made about that suite in this pass. A first architecture collection without PyYAML errored at import; that environment blocker was resolved for the subsequent successful run, not by changing source or tests.

## Constraints and reviewer action

- The Stage-1 candidate introduces no `K09`–`K15` implementation, external action, trading function, `.pcm/` recreation, version bump, M00 production edit or Financial Calendar work.
- This Worker has not run an independent Reviewer, has not issued a Stage-1 PASS and has not started Stage 2.
- The independent Reviewer must evaluate the accepted Stage-1 proposition against this **exact Git candidate**, including whether row semantics, lineage and public reachability are genuinely demonstrated; static routing and a passing suite alone do not satisfy the broad proposition.
- If the Reviewer returns `REPAIR`, return the specific defect/class to a new Worker pass. Stage 2 is unauthorised until the independent Reviewer returns `PASS`.
