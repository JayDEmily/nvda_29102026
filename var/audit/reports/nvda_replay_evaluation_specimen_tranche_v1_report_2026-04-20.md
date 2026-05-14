# NVDA replay-evaluation and specimen-path tranche v1 report

Date: 2026-04-20
Branch: `work/replay-evaluation-specimen-tranche-v1-20260420`
Brief: `var/audit/briefs/nvda_replay_evaluation_specimen_tranche_v1_brief_2026-04-20.md`

## Outcome

This tranche completed the bounded replay/evaluation and specimen-path convergence requested by the brief.

Observed directly at closeout:

- `main` was first promoted from `167fd520321ce3925ae9ebd96abe508d9af377e5` to `3556388e0b76bc90676a48a5539906b491aeeb7a` before this branch was opened.
- `src/nvda_desk/analysis/replay/` now exists.
- `src/nvda_desk/testing/harnesses/` now exists and includes `canonical_runtime.py`.
- `src/nvda_desk/persistence/research_logs.py` now exists.
- `src/nvda_desk/repositories/research_logs.py` remains only as a thin compatibility wrapper.
- `src/nvda_desk/analysis/scenarios/` still does not exist.

This tranche did not widen into scenarios, observability, legacy imported-module work, DTO or broker-boundary work, API replay routes, or broad CLI expansion.

## Closed leaves and substantive commits

1. `L1-owner-audit-and-admissibility-decision` — `1b17bc7`
2. `L2-replay-home-convergence` — `8b09dce`
3. `L3-research-evaluation-persistence-owner-convergence` — `70d53fd`
4. `L4-canonical-specimen-path-harness-convergence` — `38d7829`
5. `L5-minimum-truthful-proof-mirror` — `42bbdf0`
6. `L6-tranche-closeout` — `3d5a8e5`

Receipt reconciliation commits on the same tranche branch:

- `7658777` — leaf 1 receipt reconciliation
- `d1f727d` — leaf 2 receipt reconciliation
- `3044f15` — leaf 3 receipt reconciliation
- `8df89c0` — leaf 4 receipt reconciliation
- `5dd7a22` — leaf 5 receipt reconciliation

## Runtime and proof surfaces admitted

### Replay analysis home

Added the benchmark-owned replay analysis home at:

- `src/nvda_desk/analysis/__init__.py`
- `src/nvda_desk/analysis/replay/__init__.py`
- `src/nvda_desk/analysis/replay/service.py`

The replay home remains analysis-only. It currently admits only:

- replay fixture-source description
- replay lineage construction
- deterministic comparison of prepared or fixture-backed artefacts

It does not admit scenario execution, live order placement, raw ingress decode, or boundary-stack expansion.

### Research/evaluation persistence owner

Added the benchmark-owned research/evaluation persistence owner at:

- `src/nvda_desk/persistence/research_logs.py`

Retained compatibility only at:

- `src/nvda_desk/repositories/research_logs.py`

The owner remains append-only and bounded to research/evaluation artefacts. This tranche did not widen into live execution-state persistence.

### Canonical specimen-path harness

Added the benchmark-owned specimen-path harness at:

- `src/nvda_desk/testing/harnesses/__init__.py`
- `src/nvda_desk/testing/harnesses/canonical_runtime.py`

The harness remains test-only and fixture-backed. It assembles only:

- replay fixture root
- trace-review fixture root
- DMP v3 fixture root
- replay lineage from admitted replay contracts
- bounded trace-review fixture packs from admitted support contracts

It does not invoke entry, API routes, live brokers, or full runtime orchestration.

### Proof mirror

Added the minimum truthful Tier A proof mirror at:

- `tests/tier_a/analysis/test_replay_evaluation_surface.py`
- `tests/tier_a/persistence/test_research_logs_owner_surface.py`
- `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py`

Updated retained-test authority at:

- `config/retained_test_registry.yaml`

The new proof families cover only the admitted replay analysis, research-log persistence owner, and specimen-path harness surfaces.

## Proof results

Targeted replay/specimen proof:

- `PYTHONPATH=src pytest -q tests/tier_a/analysis/test_replay_evaluation_surface.py tests/tier_a/persistence/test_research_logs_owner_surface.py tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py` → `6 passed`
- `python3 -m compileall src/nvda_desk/analysis src/nvda_desk/persistence/research_logs.py src/nvda_desk/testing/harnesses tests/tier_a/analysis tests/tier_a/persistence/test_research_logs_owner_surface.py tests/tier_a/testing_harnesses` → clean

Tranche proof floor:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `96 passed in 2.16s`
- `python3 -m compileall src tests/tier_a tests/tier_b` → clean

## Benchmark-home count after closeout

Observed directly after this tranche:

- benchmark target package families present: `21 / 24`
- remaining absent benchmark homes:
  - `src/nvda_desk/legacy/imported/`
  - `src/nvda_desk/analysis/scenarios/`
  - `src/nvda_desk/observability/`

`src/nvda_desk/analysis/replay/` is no longer absent.
