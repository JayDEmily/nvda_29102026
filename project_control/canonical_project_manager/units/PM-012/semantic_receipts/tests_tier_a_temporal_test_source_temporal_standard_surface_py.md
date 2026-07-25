# Semantic receipt — `tests/tier_a/temporal/test_source_temporal_standard_surface.py`

## Process and restatement
- Sequence/unit `025` / `PM-012`; SHA-256 `b24d7f351839aa5eeea4b1eaae8713566a558edeb77b39c30713a3164094991a`.
- Read full test `1-55`, full temporal contract implementation, authority and current routes. Targeted pytest: `4 passed in 0.17s`.
- The file checks date-level truth without an invented timestamp, rejects capture/persistence clocks as source-time substitutes, verifies date/timestamp granularity inference, and rejects an undeclared trade-authority field.

## Relationships
1. **`10-22`; `N04-003`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:44-72`.** Date source truth remains date-only while capture and persistence clocks remain distinct. Falsifier: populate `source_time_utc` or alter stored dates; `19-22` fails. Does not prove provider/version/lineage truth. `bounded_separable_clause` / `boundary`; admit.
2. **`25-33`; `N04-003`, same locator.** Capture/persistence timestamps cannot substitute for missing source observation truth. Falsifier: accept the model; expected exception fails. Does not test every invalid combination. `exact_full_proof` / `boundary`; admit.
3. **`36-47`; `N04-003`; `N09-009`, `docs/09.1_DMPV3_PROTOCOL_WORKING.md:63-79`.** Helper infers only date versus timestamp kind/granularity and does not invent the alternative precision. Falsifier: emit wrong kind/granularity or populate alternate field; `42-47` fails. Does not validate timezone conversion/consistency. `bounded_separable_clause` / `behavioural`; admit.
4. **`50-55`; `N04-003` plus separation from decision authority in `docs/04.1...:74-84`.** Closed temporal carrier rejects an undeclared `trade_allowed` field. Falsifier: accept it; expected exception fails. Authority could still be encoded inside declared strings. `bounded_separable_clause` / `boundary`; admit narrow schema closure.

## File-level disposition
- Groups/relationships `4` / `4`; final disposition `ADMIT_TIER_A_CURRENT`.
- Admission is limited to source/capture/persistence temporal separation, precision non-invention and closed top-level carrier shape. No claim of timezone validation, source identity/version/lineage, event-window correctness, packet emission or replay.
- No implementation or test mutation executed.
