# Pass 05 — Excluded 95 D-signal purpose, academic provenance and responsibility audit

**Status:** COMPLETE AS ROW-LEVEL REVIEW EVIDENCE; PROPOSED GROUPINGS ONLY. Not programme-owner approval, software-module allocation, proof of academic derivation or amendment of M01 authority.

## 1. Governing boundary

- User authority: examine the 95 D-signals excluded from the proposed M01-1 boundary; establish their declared purpose, original academic basis and natural reuse/shared-calculation grouping before module allocation.
- Starting Git checkpoint: `6bd46758800065fb46f8a4fb39239056da6fb418` on `work/workbook-v2-pass01-guardrails-method-20261014`.
- Read in full: root `GUARDRAILS.md`, root `AGENTS.md`, active root `EXEC_PLAN.md`, accepted M01 calculation brief, current effective D catalogue; inspected original research workbook source worksheets, current Pass04 audit and earlier non-binding family/class audit.
- This audit changes **no** accepted `Dxxx` definitions, accepted architecture, source, tests, original workbook, M00 or M01 code.

## 2. Verification and principal observations

| Check | Observed |
|---|---|
| Previous NO D-signals individually reconciled | 95 / 95 |
| Source D-to-framework-step citations | 810 |
| Distinct framework propositions linked | 71 of 80 original steps |
| Registered academic sources reached by those steps | 54 of 62 |
| Direct required-step citations to Addendum 81–94 | 0 |
| Independently proved paper-to-specific-D-equation derivations | **0 established in this audit** |
| Proposed functional responsibility groupings | **30** (including 4 one-D groups) |
| Direct D-dependency edges between proposed groups | 67 |
| Cycles in 30-group dependency graph | 0 |
| Excluded signals with at least one direct downstream D-signal consumer | 73 |
| Excluded signals with two or more direct downstream D-signal consumers | 39 |

**Interpretation:** The workbook says *why an output was listed* in its `Primary purpose / output`, what computation it was intended to perform in `Calculation concept (no equation)`, and what framework `Required steps` it supports. Its research evidence audit attaches papers to those **framework propositions**, not to D-identifiers. Consequently, a D-to-paper connection in these artefacts is always `D -> required framework step -> source supporting the step`; it is **not** evidence that a specific paper fixes the D-signal equation, exact coefficients, fitted model, backtest performance or warranted software ownership. The original `Method & Legend` expressly states that step support does not prove NVDA implementation or alpha.

**No complete-paper methodological reading or external bibliographic re-verification was performed in this pass.** The source titles, publication information, links and evidence grades were read as documented in the original workbook. Thus 54 is the number of source-register entries linked by the audited step references, not the number of independently validated D-level academic methods.

## 3. Proposed responsibility groupings (not modules)

Grouping is based on effective calculation semantics, typed contexts, dependency direction, reusable intermediate results and change responsibility. **Same-family** or **same-paper** alone is insufficient to merge rows. A proposed grouping neither asserts one code package nor assigns a numbered module.

| Group | D-signals | Proposed responsibility | Why these belong together |
|---|---|---|---|
| P01 | D006, D007, D008, D158 | Data-quality scoring and completeness | Scores, mandatory-input completeness and composite data quality are grouped because they govern admissibility and confidence in received information. |
| P02 | D040, D041, D061, D070, D084, D132, D151 | Configured market-condition composites | Scores/weighted or selectable baskets describing price trend, volatility, international spillover, sector, liquidity and breadth; reusable market context. |
| P03 | D062, D064, D065 | Scheduled event relevance and gating | Event countdown, importance weighting and active-window predicate share event identity and horizon assumptions. |
| P04 | D091, D121 | Delta bucket and market-flow grouping | Configured absolute-delta taxonomy and flow aggregation by that taxonomy share bucket identity. |
| P05 | D109, D110 | ATM straddle implied-move proxy | Straddle premium and scaled implied move are consecutive calculations sharing the chosen ATM option identity. |
| P06 | D102, D111, D112, D113 | Volatility-surface fit and risk-neutral tails | Arbitrage-aware surface fit, implied density, and density-integrated tail probabilities share option-pricing assumptions. |
| P07 | D114, D115 | Physical-return forecast and probability comparison | Physical return distribution and its comparison with implied risk-neutral distribution depend on explicit model identity. |
| P08 | D125, D126, D127, D128, D129, D130 | Dealer positioning and hedge-pressure inference | Dealer-side position assumptions unify inferred Greek exposures, concentration, gamma-flip and scenario hedge pressure. |
| P09 | D141, D142 | Limit-order-book resilience assumptions | Threshold-defined replenishment and liquidity resilience use reconstructed order-book events and explicit shock/recovery conditions. |
| P10 | D146, D147, D148, D149, D150 | Macro latent factor construction | Configured growth, inflation, policy, funding and composite risk factors share a market-state factor specification. |
| P11 | D152, D153, D154 | Market and options regime probabilities | Probability-vector estimates describe macro, underlying and options/dealer regimes under fixed model versions. |
| P12 | D155 | State-vector assembly | Ordered state vector preserving component identity, provenance and compatibility. |
| P13 | D156, D157 | Cross-signal dependence and disagreement | Aligned signal dependence and conflict logic discounts redundant evidence before decision gating. |
| P14 | D159 | State identifiability/tradeability scoring | Composite readiness judgement from model/state quality and probability-vector inputs. |
| P15 | D160 | Conditional scenario generation | Generates coherent joint market paths/scenario weights from selected state and model version. |
| P16 | D161, D162, D168, D169, D170, D174 | Candidate payoff, exposure and stress measurement | Compute candidate-specific P&L, tail exposure, structure Greeks, bounded losses, roots and stress scenarios. |
| P17 | D133, D164 | Prospective execution costs | Expected slippage and prospective commissions/fees share intended order and immutable fee-schedule context. |
| P18 | D163, D165, D166, D167 | Candidate utility and exposure decisions | Uncertainty penalty, risk-adjusted utility, tradeable predicate and exposure selection form a defined decision pipeline. |
| P19 | D171, D172, D173 | Expiry, strike and neighbour suitability | Configured scoring of option expiry/strike and declared neighbouring candidate structures. |
| P20 | D175, D176 | Risk limits and position sizing | Active permissible capital/tail/stress/liquidity limits and bounded recommended quantity form a risk policy/sizing boundary. |
| P21 | D177, D178 | Pre-submission entry edge and order-pricing policy | Fresh executable entry edge is calculated after candidate utility and costs; limit price is subsequently chosen under urgency and retained-edge policy. |
| P22 | D179, D180, D193 | Fill and realised transaction measurement | Execution slippage, quantity completion and realised costs follow matched order/fill records. |
| P23 | D181, D182, D183, D184, D185 | Live portfolio Greeks and P&L state | Live exposure aggregation and P&L preservation share position context. |
| P24 | D186, D187 | Live thesis continuity and invalidation | Entry-state similarity and policy-weighted thesis invalidation share stored entry-state semantics. |
| P25 | D188, D190, D191 | Live continuation, modification and exit valuation | Prospective utilities and executable liquidation/modification values share current live position/candidate context. |
| P26 | D189, D192 | Hedge adjustment and live action policy | Greek-band hedge exposure and hold/hedge/modify/exit precedence are coordinated live policies. |
| P27 | D194, D195, D196, D197, D198, D199 | Realised Greek/path P&L attribution | One attribution path decomposes realised/marked P&L and convention-consistent residual. |
| P28 | D200, D201 | Decision process and counterfactual review | Evaluate decision justification and reconstruct alternative outcomes using locked decision information and realised path. |
| P29 | D202, D203, D204, D205, D206, D207, D208 | Forecast/model/signal evaluation and disposition | Incremental information, calibration, proper scores, out-of-sample tests, drift and signal disposition share locked evaluation sets. |
| P30 | D209 | Observation/recalculation scheduling | Determines next governed observation/update trigger from an explicit schedule. |

## 4. Observed reusable intermediate calculations

The current **effective normative D dependency graph** supports actual shared use of the following calculated outputs (direct D consumers only; no unnamed playbook is asserted):

| D-ID | Declared output | Direct downstream D consumers |
|---|---|---|
| D132 | Composite option liquidity score | D133, D154, D155, D159, D171, D172, D176, D187 |
| D165 | Net expected utility by candidate | D166, D167, D173, D176, D177, D190, D200 |
| D155 | Canonical market-state vector | D156, D157, D160, D186, D202 |
| D160 | Conditional joint scenario set | D161, D162, D174, D188, D201 |
| D111 | Risk-neutral terminal density | D112, D113, D115, D160, D172 |
| D061 | Composite US volatility regime score | D114, D149, D152, D153, D155 |
| D102 | Volatility-surface fit error | D111, D158, D163, D172 |
| D091 | Delta bucket | D109, D121, D172 |
| D164 | Total expected execution cost | D165, D177, D188, D191 |

These shared consumers are a reason **not** to identify all 95 signals as independent playbooks. The future boundaries should keep genuinely reusable state, valuation, measurement and evaluation responsibilities independent of strategies that consume them.

## 5. Academic source reuse does not define software ownership

The original source register is a bibliography for the 80 research propositions. Sources S38 and S41 each appear through step-based references for **49** of the 95 excluded signals, spanning **17** proposed groups. Those are step-evidence links, not 49 direct endorsements of particular D equations. A single academic citation therefore cannot be treated as one module, and multiple citations do not require separate modules.

Some signals reference only one distinct research source **via their steps**, but that still does not demonstrate the source individually specified their calculation or requires those signals to be grouped together. Per-row source and step chains appear in `NVDA_EXCLUDED_95_STEP_SOURCE_EDGES.csv` and the Excel review workbook.

## 6. Illustrative distinctions and unresolved authority

- `D062` is a time-to-event measurement but was excluded because its current relevant-event selection depends on a separately supplied relevance convention. This is **possible future M01-1 reassessment**, not proof of inherent strategy content.
- `D091` is delta-bucket classification; `D109`, `D110` and `D121` fail Pass04 eligibility transitively due to that unfixed bucket convention. These are not necessarily playbooks.
- `D141`/`D142` have threshold-defined limit-order-book events and shock recovery; their exclusion involves definition/parameter rigidity, not a demonstrated trading playbook.
- `D125`–`D130` depend on inferred dealer position/sign; they are not facts about actual dealer holdings. Their common assumptions support one **proposed inference group**, not a proven one-to-one academic method.
- `D160` generates conditional joint scenarios; `D161`, `D162` and `D174` then measure *candidate* economics against those scenarios. This creates a useful boundary between scenario generation and candidate valuation.
- `D175` sets permissible limits, whereas `D162`/`D174` measure candidate risk; this mathematical/policy separation must remain explicit.
- `D179`/`D180`/`D193` measure realised execution; `D133`/`D164` predict intended-order cost; `D178` calculates a permitted limit-price policy. They cannot be collapsed into one semantic responsibility merely because all concern execution.
- `D202`–`D208` require forecast/decision evaluation sets. The Brier/log-score arithmetic is deterministic, but the data under evaluation are not solely raw market signals.

## 7. Important caveats

- **NO is provisional:** semantic NO in Pass04 does not imply a permanently strategy-dependent calculation. Some rows may qualify for M01-1 after exact measurement definitions and context separation are authorised and proved. This pass does not change their NO status.
- **Grouping is provisional:** 30 is a proposal of research responsibilities, not an optimal number of modules, strategies, code packages or tests. Four groups contain one D-signal, and are deliberately *not* labelled modules.
- **Source claims are bounded:** the source register and step evidence establish workbook-declared research support for propositions only; no independent full-text examination, paper replication or independent strategy performance study was undertaken.
- **Actual playbook consumers remain unknown:** a direct downstream D consumer is established from the normative graph; application/playbook usage is not.
- **Accepted M01 is unchanged:** the current active ExecPlan owns 209 D-signals for implementation; this V2 audit remains subordinate review evidence, not a new architecture allocation.
- **Individual source/test proof was not repeated:** current per-D implementation/test independence remains outside this audit.

## 8. Deliverables and recommended decision sequence

1. Review this 95-row crosswalk and the 30 responsibility-group proposals. Accept, merge, split or challenge them based on their actual definitions.
2. For calculations with uncertain M01-1 exclusion (for example D062/D091/D141/D142), perform focused definition/scope review before final downstream allocation.
3. For each group retained for architecture consideration, prove shared meaning, typed input/output contracts, independent tests and legitimate downstream consumers. Do not allocate module numbers merely from this grouping count.
4. Preserve existing D identities and current code/tests until a separately authorised ownership/migration plan exists.

## 9. Primary evidence and exact locators

- Source workbook: `handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`; `Derived Signals!A5:O213`, `Evidence Audit!A2:N81`, `Source Register!A2:J63`, `Method & Legend`.
- Effective implementation authority: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`; full brief `NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`.
- Pass04 proposed classification: `handoff/workbook_v2/reviews/m01_1_boundary_20261014/M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv`, SHA-256 `e336e4090a65a6ab1558c956826ec9b5f889348e76ca186965f203cbcb757900`.
- This audit: `NVDA_EXCLUDED_95_PROVENANCE_RESPONSIBILITY_AUDIT.csv` records exact D, workbook, normative and consumers; `NVDA_EXCLUDED_95_STEP_SOURCE_EDGES.csv` records exact D→step→paper with DOI and cell locators; `NVDA_EXCLUDED_95_PROPOSED_GROUPS.csv` contains grouping boundaries; the Excel audit workbook presents the same evidence in filterable tabs.

## 10. Acceptance boundary

**Verified review accounting:** 95/95 rows; their source-to-step references, all matched registered paper records, and acyclic proposed intergroup dependency graph.

**Not established:** accepted 30-group ownership; assignment of playbooks; exact one-paper-to-one-calculation derivation; academic model validity; independently verified production code/tests for every signal; M01 completion or new module admission.
