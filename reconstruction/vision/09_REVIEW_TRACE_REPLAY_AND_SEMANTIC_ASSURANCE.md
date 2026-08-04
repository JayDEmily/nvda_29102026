# Review, Trace, Replay and Semantic Assurance

## Authority propositions

`P-TRACE-003`, `P-TRACE-004`, `P-TRACE-005`, `P-TRACE-007`, `P-REV-003`, `P-REV-004`, `P-REPLAY-001`, `P-TEST-001`.

Exact lineage is retained in [`../propositions/A08.md`](../propositions/A08.md), [`../propositions/A12.md`](../propositions/A12.md), [`../propositions/A13.md`](../propositions/A13.md), [`../propositions/A15.md`](../propositions/A15.md), [`../propositions/B03.md`](../propositions/B03.md) and [`../propositions/B10.md`](../propositions/B10.md).

## 1. Review exposes the governing chain

Review must expose the exact resolved coefficient chain used by the runtime:

- baseline reference;
- baseline value;
- effective value;
- clamp state;
- precedence band;
- source policy IDs;
- authority version.

It cannot reconstruct a second coefficient story from free text. Raw and prepared paths preserve identical coefficient lineage.

Review and bounded-trace outputs expose these preserved seams directly:

- Stage-5 admissibility;
- Stage-6 candidate ownership;
- overlay risk decision;
- terminal-risk application;
- nested stage-local handoff;
- final-risk compatibility result.

The preserved seam must agree with the final allow/derisk/block outcome. Review does not alter runtime decisions.

## 2. Deterministic coefficient identity

Replay, calibration and comparison outputs carry a deterministic governed coefficient snapshot ID derived from the same resolved-surface evidence used by runtime and review. The identifier and admitted evidence appear on audit packets, replay runs and comparisons by coefficient set. Replay cannot privately reconstruct policy.

## 3. Replay and specimen boundary

Replay/evaluation replays prepared, runtime or fixture-backed artefacts and compares outputs. It is analysis-only. It does not decode raw ingress, place orders, mutate live core state or imply a scenario engine.

Research/evaluation persistence is append-only and separate from live execution, opening-policy and market-observation persistence. A specimen harness may assemble admitted fixtures and contracts, but remains test-only and cannot become a secret runtime orchestrator or require live API/broker execution.

## 4. Bounded sibling scenarios

A bounded semantic scenario pack contains materially distinct, non-absurd siblings anchored to an admitted prepared-runtime path. Every scenario names its perturbations. The admitted pack contains five scenarios.

Bounded sibling trace review is a late-phase semantic proof. It runs the scenarios through the decision path and applies broad human-sanity expectations. It does not tune alpha or establish profitability.

## 5. Workbook-derived packet specimens

A workbook-derived packet specimen is a bounded reference-ledger promotion, not a live raw bundle or direct runtime authority. It must:

- use only fields supported by admitted typed contracts;
- keep missing truth explicit;
- preserve exact workbook field/row/cell lineage;
- carry lineage through the native packet or bounded extension surface plus a specimen receipt;
- emit the bootstrap input, Stage-A output and append-only observation record through the existing native builder and service path;
- avoid handwritten JSON and parallel packet paths;
- keep anchor-row and field-level dates distinct.

Legacy specimen examples using `observed_at` or `next_event_at` are superseded at the remediated seams and are not active field authority.

## 6. High-risk behavioural laws

The following behaviours survive because the admitted property/stateful evidence states them as system law:

- modifier kill switches and deployable-capital caps remain stable under combined high-risk inputs;
- playbook eligibility preserves no-trade behaviour across permission, event and options combinations;
- ordered event queries advance monotonically and never move the next-event cursor backwards.

Property/stateful proof remains targeted to bounded high-risk services; its existence does not authorise indiscriminate test expansion.
