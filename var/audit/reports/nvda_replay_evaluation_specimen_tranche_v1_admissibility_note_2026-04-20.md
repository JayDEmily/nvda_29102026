# Replay/evaluation + specimen-path tranche v1 admissibility note

Date: 2026-04-20
Branch: `work/replay-evaluation-specimen-tranche-v1-20260420`
Baseline after required promotion: `main` at `3556388e0b76bc90676a48a5539906b491aeeb7a`

## Decision

No governance blocker was proved.

This tranche owns exactly these benchmark targets:

- `nvda_desk.analysis.replay`
- `nvda_desk.testing.harnesses`
- `nvda_desk.persistence.research_logs`

## Evidence

Workbook authority:

- `Target_Structure!A23:G27` locks `nvda_desk.analysis.replay`, keeps `nvda_desk.analysis.scenarios` provisional, and keeps `nvda_desk.testing` locked.
- `Component_Skeleton!A46:I46` locks replay/comparison services at `analysis/replay/*.py`.
- `Component_Skeleton!A51:I51` locks the canonical specimen-path harness at `testing/harnesses/canonical_runtime.py`.
- `Seam_Contracts!A23:M23` keeps replay/scenario outputs bounded to research/evaluation persistence rather than live trading state.
- `Test_Architecture!A19:H20` keeps replay/scenario containment and canonical specimen path as distinct benchmark proof families.
- `Reservations!A8:H10` leaves the broader analysis subsystem provisional except where a locked owner is already named.

Live repo evidence before this tranche:

- `src/nvda_desk/analysis/` does not exist.
- `src/nvda_desk/testing/harnesses/` does not exist.
- `src/nvda_desk/persistence/research_logs.py` does not exist.
- `src/nvda_desk/repositories/research_logs.py` exists only as current evidence of research/evaluation persistence behaviour.
- Existing bounded support already exists at `src/nvda_desk/contracts/replay.py`, `src/nvda_desk/contracts/trace_review.py`, `src/nvda_desk/testing/bounded_trace_review.py`, and the fixture roots under `fixtures/replay/`, `fixtures/trace_review/`, and `fixtures/dmp_v3/`.

## Boundaries kept

This tranche does not admit:

- `nvda_desk.analysis.scenarios`
- `nvda_desk.observability`
- `nvda_desk.legacy.imported`
- replay/eval API routes
- broad CLI expansion
