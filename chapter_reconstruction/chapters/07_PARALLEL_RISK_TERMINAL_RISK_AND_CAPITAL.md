# Chapter 7 — Parallel Risk, Terminal Risk and Capital

## Chapter role

This chapter separates three authorities that all constrain a trade but answer different questions:

- parallel risk independently evaluates the environment;
- terminal risk adjudicates the execution result before review;
- capital authority sizes a permitted downstream deployment from supplied capital state.

None may absorb the others for convenience.

**Primary propositions:** `P-RISK-001`, `P-RISK-002`, `P-RISK-003`, `P-PRISK-001`, `P-PRISK-002`, `P-PRISK-003`, `P-CAP-001`, `P-CAP-002`.

## 1. Original terminal authority: one final-risk join

After execution synthesis and before review, one authoritative final-risk join evaluates the admitted posture, modifier, execution and final-risk inputs. It returns exactly one of: (`P-RISK-001`)

- `allow`;
- `derisk`;
- `block`.

The join preserves the pre-final-risk execution snapshot, its own structured lineage and the reasons for its disposition. It then applies that disposition to the execution shape and exposes the result to review. Final risk is part of the runtime authority chain; it is not a detached advisory service that may be ignored by execution.

There is no second terminal-risk authority. Missing or invalid required inputs cannot be bypassed by an informal parallel calculation. The exact overlay formula and default failure outcome are not restated in the admitted corpus.

## 2. Final risk is decomposed into overlay evaluation and terminal application

The design later makes the terminal-risk reasoning inspectable without changing its final results. The raw market/portfolio overlay decision is preserved separately from the posture-aware terminal application. (`P-RISK-002`)

The second step records whether posture aligned with, further derisked or escalated the overlay through these explicit overlap classes:

- `overlay_allow_no_terminal_override`;
- `overlay_derisk_no_terminal_override`;
- `overlay_block_no_terminal_override`;
- `posture_derisk_supersedes_overlay_allow`;
- `posture_block_supersedes_overlay_allow`;
- `posture_block_supersedes_overlay_derisk`;
- `posture_block_aligns_with_overlay_block`.

A compatibility wrapper may still return only the final `allow`/`derisk`/`block` result. That wrapper is not the explanatory authority. Review must retain the separate overlay and terminal-application surfaces. Exposing the decomposition may not change execution effects, stage order or DMP packet order.

## 3. Parallel risk is introduced as a sibling, not a replacement

Independent parallel risk had previously been deferred. The successor authority then admits it as a deterministic, non-mutating sibling lane co-resident with the governed runtime. (`P-PRISK-001`)

It may produce:

- a typed environment assessment;
- candidate-audit material;
- a lane evaluation;
- deterministic packets and supporting receipts.

It cannot mutate any serial-stage output. Identical inputs must reproduce the same lane packets and supporting receipts. The lane does not become the serial candidate generator, the final arbiter, a portfolio replacement or a hidden policy source for the serial spine.

## 4. Parallel-risk ingress becomes packet-based and bounded

The admitted live ingress boundary is later narrowed. Parallel risk consumes the temporal packet plus selected bounded stage packets from the serial runtime's admitted DMPV3 packet set. It does not read serial native internals and does not receive one oversized everything-packet. (`P-PRISK-002`)

The lane remains packet-in/packet-out. Its proof path must preserve:

- native typed carriage upstream of the deliberate DMPV3 boundary;
- the exact point where DMPV3 begins;
- lawful temporal semantics;
- selected packet identity and lineage;
- the absence of direct serial-internal reads.

This amendment does not authorise terminal risk, capital allocation, trade placement or broader parallel-risk stages. The exact selected packet subset and evaluation formula remain incomplete.

## 5. Current admitted parallel-risk path: Stage A only

The current mandatory lane is Stage A. It: (`P-PRISK-003`)

1. receives one lawful bootstrap DMPV3 input packet;
2. preserves invariant reads, stage-read state and dependency packet identity;
3. preserves trace, run, scenario and lineage identity;
4. evaluates the present environment;
5. emits one lawful parallel-risk DMPV3 output packet.

Where a lawful upstream packet already exists, Stage A consumes it. Where it does not, a bounded parallel-risk-owned adapter may wrap truth already admitted elsewhere. The adapter cannot fabricate an upstream packet, force serial stages to emit new families or create a larger packet ecosystem for visual symmetry.

Stage A's answer is the independent lane's bounded conclusion about the present environment. It does not become serial candidate formation, fresh-capital decision, final risk, downstream position management, exit or close logic.

Stage B market-translation enrichment and Stage C candidate-semantics enrichment remain conditional. Without lawful owned inputs, they stay reserved. Temporary contracts or borrowed fields cannot be used to pretend they have been admitted.

## 6. Capital remains strictly downstream of terminal risk

Capital deployment consumes the admitted final-risk result through a typed or otherwise constrained seam. It does not consume a free string and cannot read arbitrary upstream cognition fields. Negative validation must make unauthorised upstream-field consumption observable. (`P-RISK-003`)

Capital policy may not leak backwards into the serial spine. Posture hard invariants remain posture-owned. Capital receives posture permission only through bounded serial-candidate material or a downstream pre-deployment result.

The capital contract may carry bounded capital values, but the downstream opening-authorisation result remains a distinct shell. Absorbing the opening result into the capital contract would blur sizing with permission to proceed. (`P-CAP-001`)

This boundary does not grant broker placement authority and does not make thin placeholder sizing semantics complete.

## 7. A bounded authorised-notional formula is admitted

The successor hardening tranche resolves one narrow sizing rule. Capital deployment requires explicit supplied capital state and bounded policy inputs. The admitted formula is: (`P-CAP-002`)

`authorised_notional = available_capital_usd × min(requested_deployable_pct, max_deployable_pct)`

A hard-coded notional base is not authoritative. The result is bounded by the tighter of the requested and maximum deployment percentages.

This amendment resolves only that calculation. It does **not** define:

- whether percentages are fractions, whole percentages or another admitted representation;
- permitted ranges or validation rules;
- missing or invalid input behaviour;
- portfolio aggregation;
- exposure netting;
- concentration or liquidity policy;
- instrument limits;
- final trade quantity;
- broker placement.

Those remain unresolved and cannot be inferred from the algebra alone.

## 8. Current authoritative position

The risk-and-capital chain is now:

1. the serial spine forms an execution candidate without parallel-risk mutation;
2. the serial runtime emits the admitted selected DMPV3 packet set;
3. parallel-risk Stage A evaluates the present environment independently and deterministically;
4. Stage B and C remain reserved until lawful inputs exist;
5. execution reaches one terminal-risk join;
6. review preserves both raw overlay evaluation and posture-aware terminal application;
7. terminal risk returns `allow`, `derisk` or `block` and reshapes execution accordingly;
8. capital receives typed terminal-risk truth and bounded permission material;
9. authorised notional uses supplied capital and the tighter deployment percentage;
10. opening authorisation and broker placement remain separate downstream concerns.

## 9. Unresolved matters

The admitted corpus leaves open:

- the detailed parallel-risk Stage-A calculation;
- the exact selected serial packet subset;
- admission and contracts for Stage B and Stage C;
- the final-risk overlay formula and failure default;
- percentage representation and validation for capital sizing;
- all broader portfolio, liquidity, concentration, quantity and placement policy.

These gaps do not permit parallel risk to mutate the serial spine, capital to consume arbitrary cognition fields or a hard-coded notional base to reappear.

## Cross-references

- Posture partitions and stage-local handoff: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Candidate formation and modifier consequences: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- DMPV3 downstream boundary and packet ownership: [Chapter 6](06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md).
- Parallel-risk observation persistence: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Review of overlay and terminal seams: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- Coefficient and compatibility governance: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
