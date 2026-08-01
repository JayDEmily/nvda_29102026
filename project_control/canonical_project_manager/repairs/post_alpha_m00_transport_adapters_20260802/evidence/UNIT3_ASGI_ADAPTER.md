# Unit 3 ASGI Adapter Evidence

- Date: 2026-08-02
- Parent commit: `5c4d931`
- Changed production surface: `src/nvda_desk/entry/asgi.py`.
- Command: `python -m pytest -q tests/tier_a/entry/test_entry_boundary_surface.py`
- Outcome: `15 passed`.
- Established routes: mechanical `GET /health`; `POST /commands/run`; `POST /queries/review`.
- Failure behaviour: malformed JSON `400`; invalid M00 command/query `422`; wrong method `405`; unknown path `404`.
- Injection: `create_app` requires keyword-only `RunCoordinator`; no service locator or default graph.
- Known Unit 4 fallout: the existing M00 static quarantine test fails only because it still prohibits every import of M00 outside the package, including the newly authorised entry adapters.
