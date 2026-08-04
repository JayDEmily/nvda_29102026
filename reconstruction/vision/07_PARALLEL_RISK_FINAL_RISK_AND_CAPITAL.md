# Parallel Risk, Final Risk and Capital

## Authority propositions

`P-RISK-001`, `P-RISK-002`, `P-RISK-003`, `P-PRISK-001`, `P-PRISK-002`, `P-PRISK-003`, `P-CAP-001`, `P-CAP-002`.

Exact lineage is retained in [`../propositions/A11.md`](../propositions/A11.md), [`../propositions/A15.md`](../propositions/A15.md), [`../propositions/B01.md`](../propositions/B01.md), [`../propositions/B04.md`](../propositions/B04.md), [`../propositions/B06.md`](../propositions/B06.md), [`../propositions/B07.md`](../propositions/B07.md) and [`../propositions/B10.md`](../propositions/B10.md).

## 1. Independent parallel-risk lane

Parallel risk is a deterministic, non-mutating sibling of the serial cognitive spine. It produces a bounded environment assessment, candidate-audit material and lane receipts. It cannot mutate serial-stage outputs, form the serial candidate, allocate capital, become final risk or own downstream position management.

Its ingress is packet-based. It consumes the temporal packet plus selected bounded packets from the admitted serial packet set. It cannot read serial native internals and cannot receive an oversized everything-packet.

## 2. Stage-A bootstrap path

The mandatory admitted path is parallel-risk Stage A:

- receive one lawful bootstrap DMPV3 input packet;
- preserve invariant reads, stage-read state, dependency identity and trace/run/scenario/lineage identity;
- emit one lawful parallel-risk DMPV3 output packet containing the lane's bounded conclusion about the present environment.

Where a lawful upstream packet already exists, consume it. Otherwise a parallel-risk-owned adapter may wrap already-admitted upstream truth. The adapter cannot force upstream stages to invent new packet families or create a richer packet ecosystem merely for symmetry.

Stage B market-translation enrichment and Stage C candidate-semantics enrichment remain conditional. They are not admitted through temporary contracts or forced upstream widening.

## 3. One terminal risk join

After execution synthesis and immediately before review, one final-risk join is authoritative. It can `allow`, `derisk` or `block`. It preserves the pre-final-risk execution snapshot, its own decision lineage and its application to the execution shape. Review shows whether the execution was allowed, derisked or veto-blocked.

The risk process has two inspectable parts:

1. the raw market/portfolio overlay decision;
2. posture-aware terminal application of that overlay.

The terminal application records one of these overlap classes:

- `overlay_allow_no_terminal_override`;
- `overlay_derisk_no_terminal_override`;
- `overlay_block_no_terminal_override`;
- `posture_derisk_supersedes_overlay_allow`;
- `posture_block_supersedes_overlay_allow`;
- `posture_block_supersedes_overlay_derisk`;
- `posture_block_aligns_with_overlay_block`.

A compatibility wrapper may return only the final decision, but the preserved overlay and terminal-application surfaces remain the explanatory authority. Final outcome and execution effects cannot change merely because the seam became visible.

## 4. Capital remains downstream

Capital deployment consumes typed final-risk truth rather than a free string. It cannot read arbitrary upstream cognition fields or leak capital policy back into the serial spine; prohibited upstream-field consumption must be directly observable in validation. Posture hard invariants remain owned by posture; capital receives posture permission only through bounded serial-candidate or downstream pre-deployment material.

The capital contract and the downstream opening-authorisation shell remain distinct. Capital fields cannot absorb the opening result merely to simplify the interface.

## 5. Bounded authorised-notional rule

Capital sizing requires supplied capital state. At the admitted seam:

`authorised_notional = available_capital_usd × min(requested_deployable_pct, max_deployable_pct)`

The percentage representation is whatever the consuming contract lawfully admits; the corpus does not resolve whether the values are fractions, whole percentages or another bounded representation. A hard-coded notional base is not authoritative.

The formula does not define portfolio aggregation, exposure netting, concentration, liquidity, instrument limits, final quantity, broker placement or missing/invalid-input behaviour. Those remain unresolved.
