Status: complete on `main`; signal-coefficient authority pack is now closed through Gate 127
# Gate 127 — Replay Coefficient Visibility and Pack Closeout

## What closed

Gate 127 is complete on `main`. Replay runs and comparison reports now surface a stable governed coefficient snapshot id plus the admitted resolved-surface evidence that produced each replay decision. The signal-coefficient authority pack is closed honestly across the planning quartet.

## What changed

- added `GovernedCoefficientSnapshot` to replay/calibration contracts;
- added deterministic snapshot hashing from the governed resolved-surface evidence already carried by review-visible coefficient lineage;
- surfaced snapshot ids on `CoefficientAuditPacket`, replay run outputs, and comparison reports by coefficient set;
- refreshed the checked-in replay comparison report to current runtime truth after the Gate 126 temporal-authority change;
- updated router surfaces so no active pack is currently routed.

## Receipt

- branch: `work/gate-127-replay-coefficient-visibility-20260331`
- start commit: `ca3c674`
- closing proof command: `PYTHONPATH=src pytest -q tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate122_signal_coefficient_authority_closeout.py tests/test_gate123_coefficient_authority.py tests/test_gate124_mutable_surface_authority.py tests/test_gate125_review_visible_lineage.py tests/test_gate126_temporal_threshold_authority.py tests/test_gate127_replay_coefficient_visibility.py tests/test_replay_compare_runtime.py tests/test_gate98_threshold_edges.py tests/test_gate96_canonical_runtime_harness.py tests/test_gate102_raw_runtime_harness.py tests/test_gate103_raw_prepared_parity.py tests/test_gate121_historical_evaluation_readiness_closeout.py tests/test_document_hygiene.py`
- observed result: `45 passed`

## Why this is honest

This gate did not invent a new coefficient world. It reused the governed effective-surface evidence already produced by runtime and review, then carried that same evidence into replay outputs and horizon reports so replay no longer depends on private reconstruction. The pack is closed, and `PLANS.md` now routes no active pack until a later planning pass creates one explicitly.
