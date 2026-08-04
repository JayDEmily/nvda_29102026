# Chapter 5 — Playbooks, Posture Modifiers and Execution Choices

## Chapter role

This chapter follows the system from an admitted playbook idea to a selected execution expression. It separates catalogue structure, eligibility, candidate ownership, deterministic selection, execution geometry and modifier consequences so that no stage can quietly decide the whole trade.

**Primary propositions:** `P-PLAY-002`, `P-PLAY-003`, `P-PLAY-004`, `P-PLAY-005`, `P-PLAY-006`, `P-EXE-004`, `P-GOV-007`.

## 1. Original expansion: deterministic options-first playbooks

The design first adds three explicit options-led playbooks: (`P-PLAY-002`)

- `front_expiry_pin_pressure`;
- `term_structure_dislocation`;
- `skew_pressure_reversal`.

They qualify only in focused deterministic options states. They do not displace established baseline playbooks in cases where those baseline playbooks already apply. They cannot read ad hoc broker-interface or UI fields, silently redefine legacy playbooks or rename packet payload identity.

The exact qualification thresholds are not present in the admitted corpus. The settled rule is therefore one of authority and dependency: these playbooks must consume governed derived options truth and qualify deterministically; they cannot obtain apparent sophistication by bypassing the data and protocol boundaries.

## 2. The flat catalogue is replaced by a governed hierarchy

The next development replaces the flat registry as the design authority. The registry must represent: (`P-PLAY-003`)

- `family`;
- `setup_variant`;
- `execution_expression`;
- `horizon`;
- `priority`;
- `constraints`;
- `risk_overrides`.

Runtime order is deterministic. Legacy flat entries may be projected through an explicit compatibility bridge, but the bridge does not erase the hierarchy or become a second catalogue truth.

Overlays and execution templates do not automatically become top-level families. The registry is not intended to enumerate every hypothetical trade, absorb posture and risk policy, or become an unconstrained LLM ontology. Undefined aliases, ambiguous hierarchy and incompatible entries cannot be silently accepted.

The hierarchy then becomes native runtime structure: (`P-PLAY-004`)

`family -> setup_variant -> execution_expression`

Family and setup-variant candidates are emitted natively. Execution and review preserve the selected lineage. The former flat list survives only as an explicit tested compatibility projection. A missing native hierarchy cannot be hidden by attaching a flat label to the final output.

## 3. Eligibility and execution are separate decision owners

The later ownership repair makes the Stage-5/Stage-6 boundary explicit. (`P-PLAY-006`)

**Stage 5 owns admissibility.** Its answer includes:

- permission and no-trade reasons;
- admissible and watch family IDs;
- admissible and watch setup-variant IDs;
- admissible and watch playbook IDs.

**Stage 6 owns candidate execution and adjudication.** Its answer includes:

- the admitted playbook IDs it received;
- the IDs it actually adjudicated;
- the selected lead;
- contradiction-resolution lineage.

Stage 6 cannot invent admissibility. Stage 5 cannot select the final lead merely by emitting a candidate list. Historical Stage-5 lists such as `add_candidates`, `hold_candidates`, `trim_candidates`, `reduce_candidates`, `hedge_candidates` and `watch_only_candidates` may remain as compatibility surfaces. Stage-6 compatibility fields such as `candidate_adjudication`, `lead_selection_score` and `lead_selection_reasons` may also remain. None moves ownership across the boundary.

The ownership split must not change admissibility, lead selection, execution geometry, terminal-risk outcome or packet order. It exposes the existing decision chain rather than creating a new one.

## 4. Candidate selection becomes deterministic and review-visible

When several playbooks are eligible, execution ranks them by scored reasons. Registry priority is a tie-break, not the primary selector. (`P-PLAY-005`)

The output must expose:

- each candidate's adjudication record;
- the selected lead;
- the lead score;
- the reasons supporting that score;
- contradiction or tie-break state.

Registry order cannot silently decide the result. A tie without governed priority, or a candidate without the required scored evidence, cannot be converted into an opaque lead choice.

The score formula and any tie-break details beyond registry priority are not restated in the corpus. That gap does not authorise priority-first selection or unreported manual selection.

## 5. The selected execution expression resolves governed geometry

An execution expression becomes concrete through a template-backed geometry authority. (`P-EXE-004`)

The template owns bounded defaults for:

- directional bias;
- ladder spacing;
- chase distance;
- stop distance;
- take-profit distance;
- hedge ratio;
- base risk per slice.

Current context may shape those values, including event and gamma stress, but only through the selected template and governed transforms. Runtime context cannot create a second execution doctrine detached from the selected expression. Missing template authority cannot be replaced with private defaults.

The resulting geometry and explanatory notes remain visible to review. This is still execution formation, not broker placement authority. The admitted corpus does not state every template value, unit or stress transform.

## 6. Modifier authority becomes an emitted packet, not an implicit mutation

The modifier stage originally risked becoming difficult to inspect because downstream flat posture or execution fields could change without a first-class record of what policy authorised the change. The repair makes `ModifierRuntimePacket` the authoritative modifier decision. (`P-GOV-007`)

The packet carries the policy identity and operative consequences. Posture-owned fields remain intact. Where compatibility requires flat posture or execution changes, the bridge records:

- packet authority;
- applied policy IDs;
- which compatibility fields changed;
- deployable-capital consequences;
- whether execution already matched packet authority and required no additional override.

Modifier application occurs after posture and before terminal risk. Execution cannot invent its own private interpretation of the modifier. Any unlineaged flat mutation is invalid.

Historical surfaces such as `effective_policy`, `modifier_control_law` and review-lineage fields may remain as bounded projections of the same packet authority. They cannot become competing modifier truths. The modifier does not change stage order or bypass the final-risk join.

## 7. Current authoritative position

The complete playbook-to-expression chain is now:

1. governed derived context qualifies a native family and setup variant;
2. Stage 5 records admissibility, watch state and no-trade reasons;
3. Stage 6 receives the admitted IDs and adjudicates them deterministically;
4. one lead is selected with visible score, reasons and contradiction lineage;
5. the selected execution expression resolves template-backed geometry;
6. the modifier emits an authoritative packet with explicit policy lineage;
7. any flat mutation remains a bounded compatibility consequence;
8. terminal risk remains a separate downstream authority.

This sequence prevents the catalogue, eligibility stage, registry order, execution template or modifier from becoming a hidden all-purpose decision owner.

## 8. Unresolved matters

The admitted corpus does not specify:

- the exact thresholds for the three options-led playbooks;
- the retirement date for the flat registry bridge;
- the complete candidate score formula;
- every execution-template value, unit and stress transform;
- the retirement date for flat modifier compatibility fields.

Those gaps must remain explicit. They do not permit ad hoc broker inputs, priority-first selection, private geometry defaults or a second modifier interpretation.

## Cross-references

- Derived options truth and feature carriage: [Chapter 2](02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md).
- Posture ownership and serial stage order: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Packet identity and stage packetisation: [Chapter 6](06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md).
- Modifier consequences and terminal risk: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Execution lifecycle after candidate formation: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Review of candidate ownership and modifier lineage: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- Registry, coefficient and compatibility governance: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
