# Remaining preparation gaps and exact receivers (P3.2)

**Pinned source scope:** `19c14ee` full archive + `27abad7` task branch. The concurrent worker's live branch, new D014 state and any subsequent M02 family acceptance are **UNKNOWN**. This document does not request retroactive approval, provider integration or execution tests.

## Audit coverage

- Exact foundation census: **126 unique Annex-B D IDs**; downstream: **83 unique Annex-C IDs / 26 proposed peers**; disjoint union **209**. This is membership reconciliation only.
- **8 IDs** have documentary family packets with M01 source/test pointers, explicit math witnesses and fixture/source holds: D035/D036/D037, D042/D043/D047, D094/D095. These eight have **no M02 implementation/proof acceptance in inspected snapshot**.
- **118 IDs** retain `P0_2_CENSUS_ONLY`, **including D011/D012/D013 bounded accepted and D014 partial at that snapshot**. Their membership and snapshot readiness are known, but **this preparation tranche did not re-audit their individual M01 logic/fixture semantics**. Do not equate this documentary status with lack of existing M02 implementation or with no tests.
- `M01_STATIC_LITERAL_LOCATORS.csv` is an exhaustive 126-ID *lexical navigation index* to current M01 source/test lines. Zero-hit IDs: D102, D111, D112, D113. A literal match proves neither a valid implementation nor a usable test, and is not substituted for missing semantic audit.

## Required source/provider answers — do not commission broad rediscovery

| Affected IDs | Receiver | Precise unresolved question | Blocking scope |
| --- | --- | --- | --- |
| D042/D043/D047 | FRED/native publisher research → M00 projection owner → M02 calculation owner | For R246/R247/R249/R256/R257 give actual series-specific native `value` field, Percent/decimal unit codec, missing sentinel, release/effective/receipt time, revision/vintage precedence and series alignment/selection version. | Native source-certified publication, **not controlled mathematical difference**. |
| D035–D037 | IBKR historical-bar/official-calendar researcher → M00/source/calendar custodian | For R151 give admitted native bar close field, interval/session identity, receipt/effective time, exchange timezone/holiday/early-close and revision handling; exact 5/10/20 trading-session grid and trading-year fractions. | Native calendar/historical-source validity; controlled synthetic formulas remain usable. |
| D094/D095 | IBKR options/IV API research → M00 projection owner | Map R111, R183 to actual native option IV fields, right/strike/expiry/contract identity, callback/reporting/receipt timestamps, unit scale, missing state and any historical source availability. Resolve D095's 1-*trading-day* versus code's 1-calendar-day anchor and role of R183. | Native option-history/source-time admission, not numerical subtraction. |
| All eight | M02 contract/proof owner | Confirm a typed M02 result/parameter/history contract, exact Decimal precision/rounding or exact-ratio output where necessary, SQLite independent first-write/read isolation, immutable history, proof admission and rejection conditions. | New M02 family implementation/acceptance, separately governed. |

## Unresolved elsewhere: no speculative auto-closure

The other **118** have not had equation-specific expected witness construction or test/history cardinality review in this tranche. Future sequence must be dependency-closed and ranked by accepted need, not merely numerical order. G6.2 option interpolation/model/surface/density and G6.3 book state/sequence/reset families need dedicated source/mathematical contracts; do **not** reduce them to scalar or rate-family proofs. Accepted global holds remain `SRC-CALENDAR`, `SRC-MACRO`, `SRC-OI`, `SRC-VOLUME`, `SRC-BOOK`, `RAW-PROJECTION`, `CALC-PROFILE`, `MODEL-PROFILE`, applied per impacted signal.

## Integration/authority

- Root `EXEC_PLAN.md` is the single active programme plan; this task-local proposed plan is not a competing source of authority. The handoff is **proposal material**, not approved source-contract changes.
- Do not merge preparation directly into the active worker's branch without reconciling its later HEAD and dispositions. No GA acceptance, native provider acquisition, main merge, tests, admitted proof amendment, M01 retirement or SQLite schema changes were part of this work.
- Separate independent proof reviewer assessment and owner/delegated adoption remain external to this documentary extraction; no new acceptance is manufactured by a commit.
