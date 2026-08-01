# M09 Authority Worker Record V1

## Assignment

- Programme mode: `MVP_FAST_TRACK`
- Owner module: `M09 capital_authority`
- Contract boundary: `K11 FinalRiskDecision; K14 CapitalDeploymentReceipt`
- Requirements: `N-08; C-034; C-036; OBL-M09-POSITIVE`
- Source checkpoint: `330becaa99e862f40ae4066d35e21ae9788ddcae`
- Active gate: `C-NORM`
- Gate D: `CLOSED`
- Branch: `work/m09-k11-k14-capital-authority-v1`

## Question

Can M09 lawfully close the only serial/parallel final-risk join and then make one deterministic bounded fresh-capital decision against exact M05, M06, M07 and explicit capital-state authority, while withholding broker/order, live-position, lifecycle, durable-state and replay authority?

## Pre-change finding

`AUTHORITY_DISTRIBUTED_POSITIVE_BOUNDARY_INCOMPLETE`

N-08 already defines the K11 categorical join. The accepted architecture also requires M09 to own capital state, bounded sizing, the fresh-capital decision and deployment receipt. Existing code provides useful calculations and compatibility contracts, but it accepts caller-assembled strings and scalars, does not consume exact M05/M06/M07 products, does not prove cross-branch identity/lineage consistency, and does not expose the accepted four-contract M09 public boundary.

## Atlas disposition summary

Only M09-relevant candidate behaviour consistent with numbered doctrine may be admitted. Generic risk blobs, module-weight allocation, confidence-sized capital, additive carry, live broker control, module allocators and caller-invented thresholds remain rejected or split to their accepted owners. The useful bounded propositions are retained: explicit terminal blocks, exact owner lineage, explicit capital snapshot, bounded policy, explainable receipt and no order-placement authority.

## Accepted C-NORM proposition

`M09-K11-K14-NORMATIVE-AUTHORITY-V1`

1. M09 owns exactly `FinalRiskDecision`, `CapitalState`, `CapitalDeploymentDecision` and `CapitalDeploymentReceipt` public-contract meaning.
2. K11 consumes exact revalidated M05 and M06 products, joins only matching prepared lineage, preserves complete reasons/limitations and treats missing, unknown, contradictory or hard-blocked authority as `stand_down`.
3. K11 grants neither capital nor execution authority.
4. K14 requires an eligible K11 result, explicit immutable capital state, one non-rejected M07 modifier receipt and implemented M09 policy authority.
5. Fresh-capital percentage is bounded only by M09 target/hard maximum and capital-state maximum; M07 posture coefficients and confidence are not capital percentages.
6. `block`, `no_trade`, `reduce` and `continue` remain the governed action vocabulary; zero-authority outcomes carry zero percentage and notional.
7. Decision and receipt identities are deterministic over exact logical inputs and policy versions; emission time does not alter semantic identity.
8. The current alpha seam does not reserve funds, place orders, mutate positions or prove durable state. Future state-plus-receipt mutation must use M13.

## Gate boundary

C-NORM is accepted. Production and tests remain unchanged. C-PROOF must admit exact reference/mutant/public-seam proof and pass a separate-worktree adversarial review before Gate D can open.

## C-PROOF boundary

Fourteen reference/mutant cases pass and seven production-facing assertions are exact red solely because the canonical M09 package is absent. Vocabulary parity admits namespace `m09`. No production source changed. Gate D remains closed pending the mandatory separate-worktree adversarial proof review.

## Separate-worktree proof challenge finding

The first detached review at C-PROOF commit `730c66c` found four omitted numeric-domain cases: zero available capital, negative reserved capital, percentages above 100 and a caution multiplier above 1. The numbered law already requires non-negative state and bounded sizing; section 7.13.3 is clarified before proof hardening. Gate D remains closed.

## Independent proof review gate

`PASS:SEPARATE_WORKTREE_REVIEW:GATE_D_OPEN` at hardened proof commit `8542846bbb3be926fc4b70ec386fbaf5390266a4`. The four novel numeric-domain cases now pass, the 16 admitted reference/mutant cases remain green, and seven production-facing assertions remain exact red solely because the canonical package is absent. Gate D is open only for the bounded M09 K11/K14 implementation.
