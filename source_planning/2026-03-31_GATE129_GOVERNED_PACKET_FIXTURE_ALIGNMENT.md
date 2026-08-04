Status: complete on `main`; Gate 130 is now the active gate
# Gate 129 — Governed Packet Fixture Alignment

## What closed

Gate 129 is complete on `main`. Governed resolved-surface fixtures now construct the current packet lawfully, and the dead private floor/cap leftovers from the pre-externalisation era have been removed so the Gate 124 receipt matches the live code.

## What changed

- updated the Gate 120 geometry cap test to construct `ResolvedRuntimeSurfaceValue` with the governed fields introduced in Gates 124-125;
- removed the unused `_SURFACE_FLOORS` and `_SURFACE_CAPS` private constants from `StateConditionedModifierService`;
- advanced the post-flight repo consistency pack honestly to Gate 130.

## Receipt

- branch: `work/gate-129-governed-packet-fixture-alignment-20260331`
- start commit: `d62720e`
- closing proof command: `PYTHONPATH=src pytest -q tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate120_execution_geometry.py tests/test_gate124_mutable_surface_authority.py tests/test_gate125_review_visible_lineage.py tests/test_financial_calendar_planning_v3.py tests/test_gate59_doctrine_rebase.py tests/test_gate80_corrective_pass_reset.py tests/test_gate95_phase0_closeout.py tests/test_successor_pack_anti_drift.py`
- observed result: `28 passed`

## Why this is honest

This gate did not change runtime behaviour. It repaired stale governed-packet fixtures and deleted dead private leftovers that were no longer authoritative after Gate 124. The code and the receipts now tell the same story.
