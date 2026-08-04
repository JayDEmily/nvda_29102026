Status: Gate 102 complete on `main`; Gate 103 is the next active gate in the successor testing pack

# 2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md

## Purpose

Freeze one lawful raw-path harness from the admitted canonical raw bundle without bypassing the checked-in preparation path.

## Gate 102 result

- Verdict: `complete_raw_path_proven`
- Source raw artefact: `fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json`
- Downstream permission: Gate 103 may begin

## Proven path

The Gate 102 harness proves the following checked-in path end to end:

`raw bundle -> prepared runtime dataset -> cognition inputs -> review outputs`

The raw bundle is loaded as `RealDataBundle`, prepared by `RealDataLoaderService.prepare_runtime_dataset(...)`, converted by `ChainToCognitionService.convert_snapshot(...)`, and executed by `DeskCognitionRuntime.run(...)`.

No prepared snapshot was injected by hand and no prepared fixture pack was used as the primary ingress artefact.

The canonical sanity report remains honest: aligned chain coverage is `100.0`, aligned bar coverage is `75.0`, and one orphan bar remains visible rather than being hidden.

## Canonical raw-path harness freeze

- harness helper: `src/nvda_desk/testing/canonical_raw_runtime_harness.py`
- proof test: `tests/test_gate102_raw_runtime_harness.py`
- canonical dataset id: `gate102_canonical_raw_runtime`
- prepared snapshot count: `3`
- first sequence id: `seq-opening-balance`
- first spot price: `116.0`

## Deterministic runtime freeze

Using the canonical raw-path harness with the bounded supportive regime/inventory companion fixture yields:

- event window state: `same_session_event_window`
- options behavior cluster: `balanced_options_state`
- permission state: `allow`
- target fresh deployable pct: `30.25`
- add candidates: `['continuation_ladder']`
- active playbooks: `['continuation_ladder']`

The stage packet ids, packet lineage, and review packet are stable across repeated runs of the same inputs.

## What Gate 102 does not claim

- It does not claim broader raw-ingress coverage than the admitted canonical bundle.
- It does not claim raw/prepared parity beyond the one canonical run.
- It does not claim invariant extension, property testing, or DB/API seam coverage; those remain for later successor gates.
