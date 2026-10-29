# E0.1–E0.2 — re-pin and dependency-closed preparation queue

**Purpose:** documentary audit staging only. No M02 implementation/proof/provider admission; no root-plan change.

## E0.1 — observed baseline

- Preparation branch: `work/v2-g6-m01-m02-reuse-prep-20261020`; pre-work HEAD `b71e9d3bee3ede4e4aa7994dfd8ddc1e872fd072`; tree `4b19a8cb038220564a6bc508ba446c91f44f2ff7`; clean status observed.
- `git status --porcelain=v1` empty at baseline. The concurrently executing Gate 6 worker is not visible in this clone; its newer HEAD and D014 state are **UNKNOWN**.
- Authority read: full frozen guardrails, root and applicable agent instructions, task-local revision-2 plan and accepted Annex-B/C identity boundary. This plan remains subordinate to the single active root plan.
- Confirmed Annex B **126 unique** / Annex C **83 unique**, disjoint **209**, exactly equal to the effective catalogue identity set and 126 crosswalk IDs.
- Existing crosswalk: **8** `DOCUMENTARY_REUSE_PACKET_PREPARED_NATIVE_HOLD` and **118** `P0_2_CENSUS_ONLY`; the former require freshness review, latter full E1.1–E1.5.
- Accepted correction dependency rows D028, D117, D138 and D145 are retained in the existing `raw_R_refs`/`effective_R_basis`. No fallback to uncorrected original catalogue dependencies.

### Authority-byte comparison to original P0.1

| File | Current SHA256 | P0.1 comparison |
|---|---|---|
| `GUARDRAILS.md` | `585dc9b1a95719a7b60929b0d3ea64696fd6d52cd19b2b4a463c5bb9d34947b6` | UNCHANGED_FROM_P0_1 |
| `AGENTS.md` | `d431f1a0c139912606211474880d5ecf595549507eface0f4e5ae4b3f52b468d` | UNCHANGED_FROM_P0_1 |
| `EXEC_PLAN.md` | `69a10020d8f7219d790cb5f7d0ce209574578b4f91b5ba44b3a205e07d1afbbf` | UNCHANGED_FROM_P0_1 |
| `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` | `282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7` | UNCHANGED_FROM_P0_1 |
| `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` | `67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549` | UNCHANGED_FROM_P0_1 |
| `handoff/foundation_implementation/reuse_preparation/EXEC_PLAN_M01_M02_REUSE_PREPARATION_PROPOSED_20261020.md` | `e26cf4549ad0e8539781fceb052e22994446ecc8cd88050ab8e075099d675715` | PLAN_REVISION_OR_NOT_PINNED |

**Material holds:** Snapshot-only time; candidate vs accepted native source mapping remains separate; D014 status is not projected beyond archive; legacy PostgreSQL semantics are not accepted SQLite proof. E0.1 identifies no contradiction that prevents documentary family mapping.

## E0.2 — coverage and dependency graph

**Meaning of family:** a **preparation queue**, not a shared accepted semantic contract, generated tests, implementation batch or combined proof authority. Per-ID contracts remain separate. Mixed shapes/selection remain distinct within or across preparation families and may need further partition in E1.1.

| Queue | Gate envelope | Members | IDs | Cross-family D prerequisites | Scope and caution |
|---|---|---:|---|---|---|
| F01 | G6.1 | 7 | D001, D002, D003, D004, D005, D009, D010 | None | Canonical time, session and vintage |
| F02 | G6.1 | 4 | D011, D012, D013, D014 | None | Best quote algebra and size ratios |
| F03 | G6.1 | 2 | D015, D016 | F02 | Trade classification and signed volume |
| F04 | G6.1 | 2 | D017, D018 | None | Session VWAP construction/comparison |
| F05 | G6.1 | 9 | D019, D020, D021, D022, D023, D024, D025, D026, D027 | None | Underlying return/change and range |
| F06 | G6.1 | 4 | D028, D029, D030, D031 | None | Volume and activity baselines/z scores |
| F07 | G6.1 | 5 | D032, D033, D034, D038, D039 | None | Intraday realised risk/jump/ATR |
| F08 | G6.1 | 3 | D035, D036, D037 | None | Multi-session realised volatility |
| F09 | G6.1 | 3 | D042, D043, D047 | None | Rate spreads instantaneous |
| F10 | G6.1 | 3 | D044, D045, D046 | None | Rates historical change |
| F11 | G6.1 | 4 | D048, D049, D050, D051 | None | FX index/rate changes |
| F12 | G6.1 | 5 | D052, D053, D054, D055, D056 | None | Volatility index historical changes |
| F13 | G6.1 | 4 | D057, D058, D059, D060 | None | Volatility index term relationships |
| F14 | G6.1 | 2 | D062, D063 | F01 | Macro event/time/surprise |
| F15 | G6.1 | 4 | D066, D067, D068, D069 | None | International market returns |
| F16 | G6.1 | 5 | D071, D072, D073, D074, D075 | None | US/sector/NVDA underlying returns |
| F17 | G6.1 | 2 | D076, D077 | F16 | Relative sector strength |
| F18 | G6.1 | 5 | D078, D079, D080, D081, D082 | F16, F17 | Betas/residual/correlation |
| F19 | G6.1 | 1 | D083 | None | Market/sector dispersion |
| F20 | G6.2 | 2 | D085, D086 | F01 | Option contract calendar |
| F21 | G6.2 | 3 | D089, D090, D091 | None | Option moneyness and delta bucket |
| F22 | G6.2 | 4 | D087, D088, D092, D093 | None | Option quote liquidity and IV bid/ask |
| F23 | G6.2 | 2 | D094, D095 | None | Contract-matched IV history changes |
| F24 | G6.2 | 7 | D096, D097, D098, D099, D100, D101, D102 | F20 | IV term/smile/surface construction |
| F25 | G6.2 | 4 | D103, D104, D105, D106 | F24 | IV surface changes/ranks |
| F26 | G6.2 | 2 | D107, D108 | F08, F24 | IV vs realised volatility |
| F27 | G6.2 | 2 | D109, D110 | F21, F22 | ATM straddle and implied move |
| F28 | G6.2 | 3 | D111, D112, D113 | F20, F22, F24 | Risk-neutral density and tails |
| F29 | G6.2 | 5 | D116, D118, D119, D123, D124 | None | Option relative volumes and OI |
| F30 | G6.2 | 1 | D117 | None | Option unusual volume baseline |
| F31 | G6.2 | 3 | D120, D121, D122 | F03, F20, F21 | Option signed order-flow grouping |
| F32 | G6.3 | 1 | D131 | F22 | Option order-book cumulative depth |
| F33 | G6.3 | 7 | D134, D135, D136, D137, D138, D143, D144 | F02 | SMART/direct order-book snapshot metrics |
| F34 | G6.3 | 5 | D139, D140, D141, D142, D145 | None | Depth events, queue and order-flow imbalance |
| F35 | G6.1 | 1 | D151 | None | US breadth proxy |

**Order:** follow predecessor/DAG closure, not ID order. All cross-family predecessors are among the 126 and the preliminary family graph is acyclic. Membership is exact; a dependency on another family is an audit prerequisite, **not** authority to implement that predecessor.
**Source/test navigation:** each row in `E0_2_FAMILY_COVERAGE.csv` carries exact existing literal-index candidate paths/counts, canonical catalogue definition, accepted correction-adjusted raw dependencies, predecessor IDs and source-hold flags. A literal hit proves only a location candidate; zero hits do not establish missing implementation. The dynamic catalogue/dispatch boundary was inspected in `_stage1.py` and `api.py`.
**Zero literal-hit identities:** D102, D111, D112, D113 remain `NOT_ESTABLISHED_BY_LEXICAL_INDEX`. Their accepted surface/density role is recorded, but the dynamic dispatcher/indirection analysis and specialised mathematical closure belong to E1.1/E1.2; no `NOT_IMPLEMENTED` claim is made here.
**Mixed result shapes:** K09 surface/density and K17 event-state OFI are explicitly `UNCONFIRMED_FROM_CURRENT_AUTHORITY` pending per-ID contract inspection; no scalar assumption is made.
**Plan boundary:** All 118 remain un-audited; E0.2 is a coverage/queueing leaf, not completion of their mathematics/history/native-source assessments.

## Next leaf

Proceed with E1.1–E1.5 for one justified family, preferably `F01` time/quality (upstream dependency root) unless detailed authority/source inspection identifies a first-failure hold. Preserve the three prior packets and do not rerun their mathematics merely for checklist symmetry.
