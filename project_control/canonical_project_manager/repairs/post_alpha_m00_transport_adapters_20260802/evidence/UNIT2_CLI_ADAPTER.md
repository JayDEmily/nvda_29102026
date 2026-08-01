# Unit 2 CLI Adapter Evidence

- Date: 2026-08-02
- Parent commit: `b1ca99d`
- Changed production surfaces: `src/nvda_desk/entry/cli.py`, `src/nvda_desk/entry/__init__.py`.
- Focused command: `python -m pytest -q tests/tier_a/entry/test_entry_boundary_surface.py -k 'cli_requires or cli_run or cli_query or cli_rejects'`
- Outcome: `4 passed, 11 deselected`.
- Known expected-red remainder: ASGI still selects the legacy app; M00 static quarantine still forbids the newly authorised entry import until Unit 4 narrows it.
- CLI properties established: explicit keyword-only coordinator injection; exact `ApplicationCommand`/`ApplicationQuery` validation; M00/M12 result serialisation without reinterpretation; no legacy app/config/orchestrator imports.
