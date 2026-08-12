# Raw Signal Data Universe Mapping

Status: **Gate 1 normative mapping** for `M00 raw_signal_persistence`.

## Purpose

This mapping demonstrates that the raw-data foundation is designed against the complete signal universe in the sole authorised workbook, not a sampled subset. The workbook was read sheet-by-sheet and row-by-row. The mapping preserves workbook terminology and dependencies while separating workbook aliases from stable data-concept identity.

Normative workbook: `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94(1).xlsx`, SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.

## Machine-readable normative tables

| File | Rows | Meaning |
|---|---:|---|
| `data/RAW_SIGNAL_CONCEPTS.tsv` | 323 + header | Every `R001`–`R323` raw definition, canonical concept identity, source-native semantics, time/revision handling and direct downstream derived references. |
| `data/DERIVED_SIGNAL_REQUIREMENTS.tsv` | 209 + header | Every `D001`–`D209` derived definition, direct dependencies, canonical dependency identities and ultimate raw-support status. |
| `data/SIGNAL_DEPENDENCY_EDGES.tsv` | 549 + header | Complete 292 raw→derived plus 257 derived→derived dependency edges. |

The TSV files are normative data tables, not generated implementation or test evidence.

## Raw universe — 323 rows

| Family | Count |
|---|---:|
| Time & provenance | 6 |
| IBKR contract metadata | 20 |
| IBKR option-chain definition | 6 |
| IBKR L1 / generic ticks | 50 |
| IBKR option analytics | 36 |
| IBKR tick-by-tick | 14 |
| IBKR RTVolume parsed fields | 6 |
| IBKR real-time bars | 8 |
| IBKR historical bars | 38 |
| IBKR Level II market depth | 15 |
| IBKR news | 5 |
| IBKR account/risk state | 6 |
| IBKR position state | 7 |
| IBKR order/execution state | 18 |
| External volatility indices | 7 |
| FRED macro / market series | 34 |
| FRED release/vintage metadata | 6 |
| Economic calendar / consensus | 7 |
| Nasdaq Data Link real-time/delayed | 34 |
| **Total** | **323** |

The foundation therefore covers not only market quotes but contract/reference data, option-chain definitions, option analytics/Greeks, trades, bars, depth, news metadata, account/position/execution state, volatility indices, macro/vintage data, event-calendar data and alternate/fallback real-time market data.

## Derived universe — 209 rows

| Family | Count |
|---|---:|
| Time & data quality | 10 |
| Market microstructure | 6 |
| Underlying/price path | 11 |
| Volume/activity | 4 |
| Volatility | 8 |
| Regime features | 2 |
| Macro/rates | 6 |
| Macro/FX | 4 |
| Volatility complex | 10 |
| Macro/events | 4 |
| International | 5 |
| US market | 4 |
| Sector | 5 |
| NVDA state | 5 |
| Options contract | 5 |
| Options liquidity | 4 |
| Options surface | 15 |
| Options relative value | 3 |
| Options distribution | 6 |
| Options activity | 6 |
| Options flow | 3 |
| Dealer positioning | 6 |
| Execution | 5 |
| L2 microstructure | 12 |
| State synthesis | 14 |
| Decision/scenarios | 8 |
| Structure selection | 6 |
| Risk/stress | 1 |
| Risk/sizing | 2 |
| Live risk | 5 |
| Live control | 7 |
| Post-trade | 9 |
| Learning | 7 |
| Control loop | 1 |
| **Total** | **209** |

`M00` does not calculate these rows. They are mapped so the persistence contract does not destroy information required by future owners.

## Dependency integrity

The workbook's relationship graph was mechanically checked after semantic review:

- every `Rxxx` reference in a derived row resolves to one of `R001`–`R323`;
- every `Dxxx` reference in a derived row resolves to one of `D001`–`D209`;
- every raw row's `Downstream derived IDs` agrees with the reverse raw-dependency references declared by the derived rows;
- the 209-node derived dependency graph contains no cycle;
- 206 derived rows have a direct or transitive path to at least one raw row;
- `D007`, `D204` and `D205` have no explicit signal dependency in the workbook and are preserved as such rather than repaired by assumption.

## Canonical identity mapping rule

Raw workbook IDs are preserved as historical aliases. Canonical raw concepts use semantic IDs of the form:

`raw.<family>.<semantic_concept>`

A canonical concept can legitimately have more than one source-native row. For example, the four Nasdaq Data Link endpoint rows carrying `Ticker symbol` share one canonical semantic concept while retaining distinct endpoint/source-variant identity. This prevents a source field name from becoming the system-wide concept identity.

Derived rows use required downstream semantic IDs of the form:

`signal.<semantic_concept>`

These derived IDs are **unadmitted requirements**, not ownership assignments. Their future semantic owner is `UNKNOWN_FUTURE_OWNER` until that capability is independently admitted.

## Time/provenance consequences of the mapping

The raw universe contains heterogeneous temporal semantics. The persistence design therefore must preserve, rather than flatten:

- true event instants;
- provider-native dates that are not instants;
- receipt-time-only callbacks;
- exchange/market timezone and local session context;
- live/frozen/delayed source state;
- source cadence/frequency and freshness basis;
- revision/vintage identity;
- collector receipt UTC and ingestion sequence.

This is required to support `D001`–`D010` and to prevent look-ahead or false simultaneity downstream.

## Source-variant consequences of the mapping

The raw table demonstrates that payload value alone is insufficient identity. Examples include:

- option computation fields repeated under bid, ask, last and model variants;
- SMART depth versus direct-exchange depth;
- historical-bar families differentiated by source/`whatToShow` semantics;
- alternate real-time/delayed Nasdaq endpoint variants;
- FRED observation values versus release/vintage metadata.

The persistence record therefore carries source-native endpoint/field/variant identity independently of canonical concept identity.

## Validation consequences of the evidence audit and addendum

The workbook's evidence audit establishes the data-foundation requirements used here:

- Step 1: preserve source, market and receipt timing, freshness/session and revisions;
- Step 2: align asynchronous streams without disguising stale observations;
- Step 3: reject or quarantine invalid raw state;
- Step 4: preserve levels and changes across horizons;
- Step 81: use UTC as the computational clock while retaining local market context;
- Step 82: extend validation to bad ticks, duplicates and cross-contract inconsistencies;
- Step 83: retain history sufficient to distinguish transient from persistent/re-emerging change.

The mapping also preserves the later steps' dependencies so this first capability does not preclude the options surface, distribution, state, decision, execution, live-control and governed-learning layers.

## Material unresolved items

The mapping exposes, rather than fills, these gaps:

- `R283`–`R289`: provider is pending/TBD in the workbook; provider-native schema is not invented.
- `D007`, `D204`, `D205`: no explicit signal dependencies are supplied; no dependencies are invented.
- semantic owners for all `D001`–`D209`: not yet admitted by the clean kernel.
- PostgreSQL is now selected by the Gate 1 amendment as the normative backing-store technology; physical schema/index/partition design remains unresolved implementation detail.

These are carried into the active ExecPlan as Gate 1 Unknowns.
