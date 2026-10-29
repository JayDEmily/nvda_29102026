# M01 F2a — temporal trade-sign checkpoint (worker evidence)

## Authority and exact disposition

Starting Git HEAD `d86f764eed1003e10de4b3aca2cbc45dcf180175` contains reviewer F2 `REPAIR / RECURRENT_CLASS` at `5e210f096b6220182a3a1d575020364fd92909c4` and the 2026-10-09 programme-owner F2a→F2b internal-checkpoint amendment in `EXEC_PLAN.md`. This is an **F2a engineering checkpoint**, not F2 acceptance, Stage-1 acceptance or F3 authorisation.

## Reproduced reviewer failure

The unmodified `handoff/m01_completion/review/proof/test_f2_late_quote_sign_20261009.py` originally failed: after a quote-only T+10 update, prior T+5 sell was reclassified from -1 to +1; D016/D120 became absent. Independently authored F2a proof tests originally failed 3 additional cases. Proof-first test commit `5cb82f7` preceded production repair `ab7ba10`. The intermediate test-only correction `5d08b9e` adjusts an incorrect assertion about recalculation-derived IDs; the reviewer expectation and original arithmetic were not weakened. Subsequent test formatting is commit `0303592`.

## Production repair and established outcome

`api.py` `_materialise` scopes the `D015 -> D011` predecessor request to the **selected native R120 trade's UTC source instant**, keeping the parent's knowledge cutoff so a later quote event is ineligible. It refuses missing/non-instant and tied multiple latest-trade records rather than inventing a timestamp or selecting one arbitrarily. Temporal scoping is deliberately separate from existing D109/D170 contract-scoped child selection.

The public-seam proof now obtains D015(T0)=+1, D015(T+5)=-1 and D015(T+10)=-1 after quote-only update; D016(T+10)=-1 and D120(T+10)=(signed_contracts=-1, signed_premium_notional=0). It verifies that the later quote does not enter D015's raw predecessor lineage, and verifies contributing D015 derived identities, retry and quote-only refusal. The unchanged earlier reviewer canonical positive witness is also included.

## Executed verification

Environment: Python 3.13.5, pinned pytest 9.0.3, Ruff 0.15.11, mypy 1.20.1, restored from supplied offline U05 proof bundle. Logs: `handoff/m01_completion/proof/f2a_temporal_sign_20261009/`.

- `PYTHONPATH=src python -m pytest -q tests/product/derived_signal handoff/m01_completion/review/proof/test_f2_late_quote_sign_20261009.py handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py`: **136 passed**.
- `ruff check src tests tools`: passed.
- `python -m mypy src/nvda_desk/derived_signal_calculation_truth/api.py`: passed.
- `python -m compileall -q src/nvda_desk/derived_signal_calculation_truth`: passed.
- Full-repository mypy: not passed in clean pinned venv due missing `types-PyYAML` stubs in five unrelated architecture files. No source or test was weakened to overcome it.
- PostgreSQL M00 durability, M01 persistence and the combined architecture/bootstrap regression: **not rerun** during this F2a-only checkpoint. They are not claimed passed.

## Routing

Proceed only to the mandated F2b *authority/capability examination*. F2b production repair, F2 consolidated review, F3, F4 and Stage 2 are not implied by this checkpoint.
