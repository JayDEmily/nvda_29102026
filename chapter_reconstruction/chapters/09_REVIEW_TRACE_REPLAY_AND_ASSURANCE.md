# Chapter 9 — Review, Trace, Replay and Assurance

## Chapter role

This chapter defines the evidence surfaces by which a decision can be inspected, reproduced and challenged without creating a second decision system. It develops from exact coefficient lineage, through bounded sibling traces and replay, to native-path workbook specimens and preserved behavioural invariants.

**Primary propositions:** `P-TRACE-003`, `P-TRACE-004`, `P-TRACE-005`, `P-TRACE-007`, `P-REV-003`, `P-REV-004`, `P-REPLAY-001`, `P-TEST-001`.

## 1. Review must expose the coefficient chain actually used

Review does not narrate policy from free text after the event. It carries the same resolved-surface chain consumed by runtime policy: (`P-REV-003`)

- baseline reference;
- baseline value;
- effective value;
- clamp state;
- precedence band;
- source policy IDs;
- authority version.

Raw and prepared paths must preserve identical coefficient lineage. A second coefficient story reconstructed in review would sever the evidence from the decision it purports to explain and is therefore invalid.

## 2. Replay inherits the same governed coefficient identity

Replay and calibration extend that requirement through a deterministic coefficient-snapshot identifier derived from the same resolved-surface evidence used by runtime and review. (`P-TRACE-003`)

The snapshot identity is attached to audit packets, replay runs and comparisons by coefficient set. Identical governed evidence must produce the same snapshot identity. Replay cannot privately reload, reinterpret or reconstruct coefficients under a separate authority.

The admitted corpus does not define the snapshot-hash algorithm or retention policy. Those omissions do not weaken the identity requirement.

## 3. Bounded sibling scenarios are explicit evidence objects

A semantic scenario pack is anchored to one admitted prepared-runtime path. Its sibling scenarios must be materially distinct, non-absurd and different only through named perturbations. The admitted Gate-132 pack contains five scenarios. (`P-TRACE-004`)

The bounded pack is evidence for how the governed path responds to controlled changes. It does not admit a native scenario engine, an open-ended catalogue or hidden perturbation machinery. An unanchored scenario, an unstated change or an absurd input does not satisfy the proposition.

## 4. Trace review is semantic proof, not trading optimisation

The five siblings are then run through the declared live decision path and assessed against broad human-sanity expectations. This is a late-phase semantic proof: it asks whether the system's meaning remains coherent under bounded variation. (`P-TRACE-005`)

It does **not**:

- tune alpha;
- optimise coefficients;
- establish profitability;
- authorise calibration changes;
- prove a general scenario facility.

The deliberately broad sanity criteria therefore remain bounded review judgement, not a numerical trading-performance claim.

## 5. Replay and specimen harnesses remain outside live authority

The successor corpus formalises replay/evaluation as an analysis-only consumer of prepared, runtime or fixture-backed artefacts. It may compare outputs and append research/evaluation evidence, but it may not decode raw ingress, place orders, mutate live core state or imply a scenario engine. (`P-REPLAY-001`)

Research/evaluation persistence remains append-only and separate from live execution, opening-policy and market-observation persistence. A canonical specimen-path harness may assemble admitted fixtures and contracts, but it is test-only. It cannot become a concealed runtime orchestrator or require live API or broker execution.

Replay comparison metrics and retention remain unspecified.

## 6. Workbook specimens are governed promotions, not invented runtime truth

A workbook-derived packet specimen is a bounded promotion from a governed reference ledger. It is neither a live admitted raw bundle nor direct runtime authority. (`P-TRACE-007`)

The promotion must:

1. map only fields lawfully supported by typed contracts;
2. keep missing truth explicit;
3. record workbook origin at field, row and cell level;
4. carry that origin through native packet lineage or bounded extension metadata plus a specimen receipt;
5. emit the bootstrap input packet, Stage A output packet and append-only observation record through the existing native builder/service path.

Hand-written JSON and parallel specimen packet paths are prohibited. Unsupported fields remain absent; fabricated UTC values are not permissible. The workbook anchor-row date and individual field source dates remain distinct, so mixed-date evidence is preserved rather than normalised away. Earlier `observed_at` and `next_event_at` specimen examples are superseded.

The exact workbook mapping and complete extension schema remain external and unresolved.

## 7. Preserved decision seams are first-class review outputs

Review packets and bounded trace reports expose the actual decision seams directly: (`P-REV-004`)

- Stage-5 admissibility;
- Stage-6 lead-candidate ownership;
- overlay decision;
- terminal application;
- nested stage-local handoff;
- `final_risk_join` compatibility outcome.

Human trace reports compare those seams in order. They must agree with the final compatibility outcome and must reflect the same run. Review can detect disagreement; it cannot repair or alter the runtime decision after the fact.

## 8. Assurance preserves bounded high-risk behavioural laws

Three high-risk invariant families remain binding: (`P-TEST-001`)

1. modifier kill switches and deployable-capital caps remain stable under combined high-risk inputs;
2. playbook eligibility preserves no-trade outcomes across permission, event and options combinations;
3. ordered event queries advance monotonically and never move the next-event cursor backwards.

These laws justify bounded property and stateful testing of the high-risk services that own them. They do not authorise indiscriminate property-test expansion across the repository. The specific generators and numerical domains remain unstated, but violation of any named invariant is still failure.

## 9. Current authoritative position

The review, trace and replay design is now:

1. review exposes the exact coefficient chain used by runtime;
2. replay uses a deterministic snapshot ID derived from that same evidence;
3. five bounded sibling scenarios remain anchored and explicitly perturbed;
4. sibling review is semantic proof, not alpha tuning or profitability evidence;
5. replay/evaluation remains analysis-only and append-only;
6. specimen harnesses remain test-only and cannot orchestrate runtime;
7. workbook specimens travel through native builders with exact field/row/cell lineage and explicit missing truth;
8. admission, candidate ownership, overlay and terminal seams are first-class review outputs;
9. high-risk modifier, eligibility and temporal invariants remain binding and bounded.

## 10. Unresolved matters

The admitted corpus leaves open:

- the coefficient snapshot-hash algorithm and retention policy;
- the reproduced contents of the five Gate-132 sibling scenarios;
- numerical completion of the human-sanity criteria;
- replay comparison metrics and research-evidence retention;
- the exact governed-workbook mapping and complete lineage-extension schema;
- report formatting and property-test generator domains.

None of these gaps permits a second coefficient authority, a hidden scenario engine, live replay mutation, a bespoke specimen path or backward-moving event state.

## Cross-references

- Advisory authority and unresolved scenario/observability reservation: [Chapter 1](01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md).
- Raw/prepared evidence and workbook-source truth: [Chapter 2](02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md).
- Temporal monotonicity and mixed-date provenance: [Chapter 3](03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md).
- Serial stages and preserved handoffs: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Playbook eligibility and modifiers: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- Packet lineage and native DMPV3 carriage: [Chapter 6](06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md).
- Parallel-risk Stage A and terminal application: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Append-only observations and preview lifecycle: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Coefficient authority, compatibility and public boundaries: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
