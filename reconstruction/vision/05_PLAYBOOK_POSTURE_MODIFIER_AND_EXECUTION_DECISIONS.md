# Playbook, Modifier and Execution Decisions

## Authority propositions

`P-PLAY-002`, `P-PLAY-003`, `P-PLAY-004`, `P-PLAY-005`, `P-PLAY-006`, `P-EXE-004`, `P-GOV-007`.

Exact lineage is retained in [`../propositions/A04.md`](../propositions/A04.md), [`../propositions/A05.md`](../propositions/A05.md), [`../propositions/A06.md`](../propositions/A06.md), [`../propositions/A10.md`](../propositions/A10.md) and [`../propositions/A15.md`](../propositions/A15.md).

## 1. Native playbook hierarchy

The playbook model is native:

`family -> setup_variant -> execution_expression`

The registry carries at least `family`, `setup_variant`, `execution_expression`, `horizon`, `priority`, `constraints` and `risk_overrides`. Family and variant candidates are emitted natively, and execution and review preserve their lineage. The old flat registry or flat list may survive only as an explicit compatibility bridge.

Overlays and execution templates do not automatically become top-level families. The catalogue does not enumerate every hypothetical trade, collapse posture/risk into playbooks or become an LLM ontology.

## 2. Options-first additions

The admitted deterministic options-led playbooks are:

- `front_expiry_pin_pressure`;
- `term_structure_dislocation`;
- `skew_pressure_reversal`.

They qualify only in focused options states and must not displace established baseline playbooks in their existing cases. They cannot read ad hoc broker-interface fields, silently redefine legacy playbooks or rename packet identity.

## 3. Stage-5 admission versus Stage-6 ownership

Stage 5 owns admissibility. Its answer includes:

- permission and no-trade reasons;
- admissible and watch family IDs;
- admissible and watch setup-variant IDs;
- admissible and watch playbook IDs.

Stage 6 owns candidate execution and adjudication. Its answer includes:

- the admitted playbook IDs it received;
- the IDs it actually adjudicated;
- the selected lead playbook;
- contradiction-resolution lineage.

The historical Stage-5 compatibility lists `add_candidates`, `hold_candidates`, `trim_candidates`, `reduce_candidates`, `hedge_candidates` and `watch_only_candidates` may remain. Stage-6 compatibility fields such as `candidate_adjudication`, `lead_selection_score` and `lead_selection_reasons` may also remain. None moves candidate ownership back into Stage 5 or overrides the admitted ownership surfaces.

## 4. Candidate adjudication

When multiple candidates are eligible, selection is score-driven and deterministic. Registry priority is a tie-break, not the primary selector. The output exposes each candidate's adjudication record, the selected lead, its score and reasons, and contradiction or tie-break handling. Registry order must not silently decide the result.

## 5. Execution geometry

Execution expression carries governed, template-backed geometry:

- bias;
- ladder spacing;
- chase distance;
- stop distance;
- take-profit distance;
- hedge ratio;
- base risk per slice.

Current runtime context may shape these values, including event and gamma stress, but it cannot create a second execution doctrine detached from the selected template. Geometry remains review-visible.

## 6. Modifier authority

`ModifierRuntimePacket` is the authoritative modifier decision. It carries policy identity and the operative consequences. Posture-owned fields remain intact. Any mutation of flat posture or execution fields is a bounded compatibility bridge that records:

- packet authority;
- applied policy IDs;
- which compatibility fields changed;
- deployable-capital consequences;
- whether execution already matched packet authority and required no extra override.

Execution cannot invent a private modifier interpretation. Existing `effective_policy`, `modifier_control_law` and review-lineage surfaces may remain as bounded compatibility/lineage views of the same packet authority. Modifier application must not change stage order or bypass terminal-risk authority.
