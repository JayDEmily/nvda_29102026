# Cognition Context and Serial Workflow

## Authority propositions

`P-ARCH-001`, `P-ARCH-006`, `P-ARCH-008`, `P-SERIAL-001`, `P-CTX-003`, `P-ARCH-004`, `P-TRACE-006`, `P-DEC-002`.

Exact lineage is retained in [`../propositions/A06.md`](../propositions/A06.md), [`../propositions/A10.md`](../propositions/A10.md), [`../propositions/A14.md`](../propositions/A14.md), [`../propositions/B01.md`](../propositions/B01.md), [`../propositions/B08.md`](../propositions/B08.md) and [`../propositions/B09.md`](../propositions/B09.md).

## 1. Ordered cognitive questions

The serial cognitive spine answers six questions in this order:

1. temporal state;
2. market regime;
3. options and flow;
4. posture and risk permission;
5. playbook eligibility;
6. expression and execution candidate formation.

Each stage owns only its bounded answer and emits a typed, inspectable output. Stages must not collapse into one opaque object. Parallel risk, terminal risk, capital and downstream operations cannot absorb serial meaning for convenience.

Step-0 calendar and horizon routing, candidate-family generation, execution-expression ownership and carry-branch boundaries must be assigned explicitly. An ambiguity in ownership is not resolved by whichever component happens to have the data.

## 2. Stateless serial spine

The serial spine is stateless. State, observation history and persistence belong to explicit downstream or side-lane surfaces. Temporal remediation, packetisation or orchestration cannot create hidden memory in a serial stage.

The runtime orchestrator validates and sequences typed stage contracts. It coordinates; it does not become a policy owner. Execution lifecycle, execution coordination, final-risk overlay, parallel-risk assessment and outbound projection cross their admitted boundaries through typed contracts rather than arbitrary dictionaries. Outbound shapes derive from admitted contracts rather than incidental mapping keys.

## 3. Precursor economics

Precursor context carries both raw-field presence and derived economic meaning. Calendar availability alone is insufficient. Supportive, contradictory and hostile precursor states must remain distinguishable so posture and review can show different downstream consequences.

## 4. Posture ownership

Posture exposes three distinct surfaces:

- `hard_invariants`: posture-owned hard-block truth;
- `local_envelope`: base permission, base posture label, deployable-capital envelope and posture-owned derisk reasons;
- `downstream_annotations`: selector citations, modifier notes and other non-posture-owned annotations.

Non-posture notes must not contaminate posture-owned truth. Flat posture fields and the historical reasons list may remain only as compatibility representations.

## 5. Preserved stage-local seams

Review and trace must preserve the decision chain before later mutation. The inspectable sequence is:

- cited posture before modifier mutation;
- cited eligibility before execution;
- execution before modifier mutation;
- execution after modifier mutation but before terminal-risk application;
- the terminal-risk decision before final execution reshaping.

`StageLocalHandoffSurface` carries these exact artefacts additively as:

- `cited_posture_pre_modifier`;
- `cited_eligibility`;
- `execution_pre_modifier`;
- `execution_post_modifier_pre_final_risk`;
- `final_risk_decision`.

This preservation must not change final allow/derisk/block outcomes, serial order, review order or packet lineage order. It exists to make ownership inspectable, not to create a second decision path.
