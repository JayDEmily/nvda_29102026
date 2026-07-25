# Semantic receipt — `tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py`

## Process and restatement
- Sequence/unit `023` / `PM-012`; SHA-256 `0c7d660a4133af11cae4b65d99aca26739d1831e910b9b6025ec36622c36bed4`.
- Read full test `1-297`, all 108 parameter cases, and full directly exercised temporal, raw-bundle, upstream-signal and ingress modules. Current authority route is absent. Targeted pytest: `108 passed in 0.30s`.
- A 108-row table assigns Atlas/audit IDs to five canned behaviours. The test preserves selected raw-bundle temporal/provenance values, checks date-only replay carriage, constructs a temporal window, exercises a trace-only upstream ingress with key stripping/quarantine, and scans four source files for literal forbidden tokens/import substrings. It never reads the Atlas records or proves that any assigned behaviour represents their meaning.

## Assertion-group relationships

| G | Test locator | Proposition / source locator | Fit, exact proof and non-proof | Falsifier / failing assertion | Relation / strength | Disposition |
|---|---|---|---|---|---|---|
| 1 | `43-159` | `N08-011`, `docs/08_TESTING_AND_PROMOTION_CORE.md:69-101` | Only non-empty Atlas IDs are asserted; no row evidence or proposition mapping is read. | Empty one ID; `159` fails. Any wrong non-empty mapping passes. | `related_but_not_proved` / `token_only` | P3 row-level traceability. |
| 2 | `163-185` | `N03-002`, `docs/03.1_DOMAIN_MODEL_WORKING.md:21-39`; `N04-003`, `docs/04.1...:44-72` | API loader preserves selected source/capture/provenance values and payload sections. No contract/version/validation/fingerprint or source-identity truth is proved. | Change a carried value; `177-184` fails. Fabricated provenance passes. | `bounded_separable_clause` / `identity_lineage` | Preserve narrow carriage clause. |
| 3 | `187-203` | `N04-003`, `44-72`; `N09-009`, `docs/09.1...:63-79` | Date-only source truth remains `source_date`, with no invented UTC timestamp. Exact temporal-separation clause for this specimen. | Manufacture timestamp or lose date/kind; `197-202` fails. Replay determinism/source truth still unproved. | `bounded_separable_clause` / `boundary` | Preserve narrow date-granularity proof. |
| 4 | `205-233` | `N04-003`, `44-72` | Timestamp carrier/window fields are preserved; date helper labels granularity; carrier without source timestamp/date is rejected. Does not validate timezone conversion, interval order, provider truth or packet separation. | Remove rejection or alter asserted fields; `226-232` fails. Inconsistent raw/UTC values pass. | `bounded_separable_clause` / `boundary` | P3 for full temporal consistency. |
| 5 | `235-277` | `N04-002`, `docs/04.1...:21-42`; `N03-002`, `21-39` | Admitted family returns detached dataset copy, strips two name-listed decision keys, emits a trace and no side-effect-list entries; unadmitted family is quarantined. Does not observe real trade state or prove the key blacklist complete. | Retain observed key, mutate copied payload, or admit rejected family; `254-276` fails. Renamed authority/actual side effects pass. | `related_but_not_proved` / `behavioural` | P3: typed allow-list and observed non-interference. |
| 6 | `279-295` | `N04-002`, `21-42`; `N04-003`, `44-72` | Scans four files for seven donor tokens and five owner-import substrings, then checks missing source temporal truth is rejected. The rejection is direct; the text scans are non-exhaustive heuristics. | Add a listed token or accept missing truth; `283/285/286-294` fails. Renamed/dynamic forbidden ownership passes. | `related_but_not_proved` / `token_only` | P3: dependency/behaviour boundary; preserve missing-temporal rejection only. |

## File-level disposition
- Groups/relationships `6` / `6`; final disposition `BLOCKED_P3_REPAIR`.
- Decisive defects: 108 semantic row assignments are unsupported, and the transform/non-interference claims rely partly on literal blacklists and empty side-effect metadata rather than observed authority boundaries. Narrow temporal/provenance clauses remain useful.
- No implementation or test mutation executed.
