# M01 Stage 1 — Leaf 2 Worker Git Checkpoint (2026-10-08)

## Authority and stop boundary

- Current explicit Programme Owner/user instruction: **execute Leaf 2 only**.
- Governing files: `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, accepted `EXEC_PLAN.md` §4 Leaf 2, and the indexed accepted Derived Signal brief, especially §§5 K03–K06 and 8–14.
- This is an engineering checkpoint **not** an independent review, Stage-1 acceptance, M01 completion or module activation.
- The next worker/reviewer must not infer that Leaf 3 has been executed. No Leaf-3 code, proof or acceptance was undertaken in this pass.

## Source provenance and proof-first history

- Input full-Git Leaf-1 checkpoint HEAD: `208606b1ea19eeb91e8c39d5f36bc57bbb6369f7`.
- Leaf-2 initial authority-derived proof commit: `4e3687ce8a03c2a9d0dcf65bf16fa45a85d261ab`.
- Leaf-2 additional temporal, context and public predecessor proof commit: `eec0612aa7267263ab9ea440d2f0e368d6c9d6d5`.
- Leaf-2 non-positive ATR window proof commit: `f1d92792433b59babcb45f4c0a04b619e81d105f`.
- Leaf-2 production repair commit: `273d6f238d98bd16597f06a3d69037898f0334c6`.
- All listed proof commits precede the production-behaviour commit. This file is a subsequent evidence-only checkpoint record.

## Changed production and proof surfaces

- `src/nvda_desk/derived_signal_calculation_truth/api.py`: constrain stored predecessor reuse by requesting calculation-definition and required predecessor typed-context versions, exact raw projection-mapping/unit-convention versions, and previously admitted selection/parameter references; apply latest-per-member/direct-raw and current-predecessor skew checks and current-predecessor freshness refusal.
- `src/nvda_desk/derived_signal_calculation_truth/_stage1.py`: require an explicit sufficient `P_BASELINE` count/minimum rather than shrinking the requested historical baseline to whatever was retrieved; for the realised-risk D032–D038 path, require the exact versioned sample schedule and reject missing or substituted sample instants; reject non-positive ATR bar counts on D039.
- `tests/product/derived_signal/test_m01_stage1_leaf2_temporal_graph.py`: public cutoff/event-time/basis/freshness/skew refusal, direct-raw absence, retry/append-only lineage, incompatible predecessor context/definition/mapping/unit versions, strict historical anchor, baseline sufficiency, exact volatility sample schedule, stale stored Stage-2 predecessor on public Stage-1 path with positive control, and ATR invalid-window refusal.
- `tests/product/derived_signal/test_m01_stage1_semantics.py`: bind the existing positive D035 sample-window test to an explicit schedule without changing its accepted numerical assertion.

## Actual validation performed

The runtime proof tools were recovered **outside this Git tree** from the previously supplied `NVDA_U05_PROOF_ENV_BOOTSTRAP_PY313_PG17_9_20260926` wheelhouse. Versions: Python 3.13, Ruff 0.15.11, mypy 1.20.1, pytest 9.0.3, psycopg 3.3.4. The proof environment is not part of the candidate source tree or handoff archive.

- `python -m pytest -q tests/product/derived_signal`: **96 passed**.
- `python -m pytest -q tests/architecture tests/bootstrap` with the recovered dependencies and system-provided PyYAML: **74 passed**.
- `python -m pytest -q tests/product tests/architecture tests/bootstrap --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` with the same environment: **594 passed**.
- `ruff check src tests tools`: **all checks passed**.
- `python -m mypy src/nvda_desk/derived_signal_calculation_truth`: **no issues in five source files**.
- `PYTHONPATH=src make validate`: **structural architecture validation passed, zero dependency/public-seam violations**.
- `python -m compileall -q src/nvda_desk/derived_signal_calculation_truth tests/product/derived_signal`: **passed**.
- `git diff --check`: **passed**.

## Unresolved verification boundaries (do not promote to PASS)

1. The whole-product run including M00's `tests/product/raw_signal/test_u05_postgresql_durability.py` was attempted and produced **55 setup errors**, all because `NVDA_TEST_POSTGRES_DSN` was unset. The 594 passing non-PostgreSQL tests are not equivalent to real PostgreSQL durability proof. The M00 PostgreSQL proof environment has not been established in this Leaf-2 pass.
2. Full `python -m mypy src` was attempted: **five `import-untyped` errors in architecture sources** due to missing `types-PyYAML`. The focused changed-package mypy run passed. Do not present that focused result as a full-tree type-check PASS.
3. Stage-1 catalogue-row mathematical closure, complete kernel-family coverage, and Stage-1 acceptance are **Leaf 3 / independent-review boundaries**, not established by this Leaf-2 proof subset.
4. No independent reviewer has accepted this checkpoint. Do not claim M01/Stage-1 admission or complete implementation on the basis of this package.

## Continuation

The present user's scope ends with this Leaf-2 checkpoint. Preserve the full Git ancestry, direct proof-first ordering and every stated validation limitation. Do not proceed into Leaf 3 without a new direct user instruction.
