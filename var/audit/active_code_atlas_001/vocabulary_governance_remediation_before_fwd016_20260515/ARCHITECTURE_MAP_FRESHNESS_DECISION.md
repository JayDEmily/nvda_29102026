# Architecture Map Freshness Decision

Decision: `refresh_map_now`.

Reason: the global PM acceptance audit found `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` stale relative to ledger state after FWD-010 through FWD-015. The current authority permits updating the non-frozen architecture map but forbids modifying frozen `*_CORE.md` authority.

Changes made:

- Updated map status header to `RECONSTRUCTED_REPLACEMENT_REFRESHED_AFTER_FWD015` with a 2026-05-15 refresh note.
- Refreshed rows `5.9` through `5.12` to point at FWD-010 through FWD-015 bounded ordered-replay evidence and proof artefacts.
- Refreshed row `5.13` to state FWD-016 remains the next ordered row and unopened.

DEF-003 status: `fixed`.

Boundary: this did not open FWD-016, did not alter runtime source behaviour, and did not modify frozen normative docs.
