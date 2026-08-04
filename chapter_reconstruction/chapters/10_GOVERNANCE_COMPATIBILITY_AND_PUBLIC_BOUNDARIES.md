# Chapter 10 — Governance, Compatibility and Public Boundaries

## Chapter role

This chapter closes the dependency chain by defining how names, mutable policy, coefficient authority, compatibility and public egress remain governed as the system evolves. It prevents configuration, migration and API convenience from silently changing semantic ownership.

**Primary propositions:** `P-GOV-001`, `P-GOV-002`, `P-GOV-003`, `P-GOV-004`, `P-GOV-005`, `P-GOV-006`, `P-ARCH-005`, `P-API-001`.

## 1. Vocabulary is a governed contract surface

Canonical vocabulary is regenerated from current governed surfaces rather than copied from a stale snapshot. It must govern aliases and duplicate labels and carry enough structure to identify: (`P-GOV-001`)

- playbook family;
- setup variant;
- execution expression;
- horizon;
- raw or derived status;
- stage owner;
- contract linkage.

Conflicting duplicate labels, undefined aliases and runtime surfaces without canonical entries are rejected. Historical vocabulary snapshots remain evidence, not current authority. The vocabulary cannot degrade into a free-form glossary or redesign runtime behaviour merely by renaming it.

The versioning and change-approval lifecycle remains incompletely specified.

## 2. Workflow-routing terms acquire explicit owners

The vocabulary boundary then expands to the system's routing language. It explicitly owns: (`P-GOV-002`)

- Step-0 calendar and horizon routing;
- candidate-family generation;
- generic playbook family, setup and expression labels;
- carry handoff;
- carry-horizon branch terms.

These terms regenerate deterministically from the governed builder. Naming alone does not establish ownership; an unowned or non-deterministically generated routing term is invalid.

## 3. Mutable runtime policy is limited to eight observable surfaces

The admitted mutable runtime surfaces are exactly: (`P-GOV-003`)

- `entry_gate_score_floor`;
- `zone_score_threshold`;
- `distance_to_vwap_soft_limit_pct`;
- `risk_vix_caution_threshold`;
- `risk_vix_hot_threshold`;
- `max_risk_per_trade`;
- `target_fresh_deployable_pct`;
- `hedge_required`.

The modifier packet resolves the operative values, execution output carries those values, and review exposes the same values. A consumer cannot depend on hidden side channels, implied policy state or an unadmitted ninth mutable surface.

## 4. Coefficient scope distinguishes behaviour from clock timing

Governance then freezes the broader coefficient universe. Every admitted entry identifies its owner stage, units, bound class, baseline and sane minimum/maximum envelope. (`P-GOV-004`)

The initial scope consists of:

- eight mutable runtime surfaces;
- sixteen behavioural temporal thresholds;
- two timing parameters.

Behavioural temporal thresholds and clock-timing parameters are distinct classes. A clock window cannot masquerade as an alpha coefficient, and neither a workbook nor implementation convenience may widen the admitted universe. The complete identifier list is not reproduced in this proposition, so it cannot be reconstructed by guesswork.

## 5. One typed authority validates the admitted coefficient universe

A single typed governed authority contract covers the admitted mutable surfaces, temporal thresholds and timing parameters. Each entry carries: (`P-GOV-005`)

- owner stage;
- units;
- baseline;
- minimum and maximum envelope;
- transform family;
- allowed upstream drivers.

Unknown surfaces, absurd ranges and illegal transforms fail deterministically. Legacy example registries remain reference-only and cannot act as private authority. Versioning, persistence and approval workflow remain only partially specified.

## 6. Runtime values load from authority and preserve ordered lineage

Mutable baselines, floors and caps are loaded from the governed authority rather than private class constants. Every resolved value carries owner stage, authority version, baseline reference and numeric envelope. (`P-GOV-006`)

The frozen specimen preserves two different stage outcomes in order:

1. modifier resolution produces `20.625`;
2. authoritative final-risk derisk then produces `13.4062`.

Collapsing those values, reversing their order or treating either as a private constant would erase the modifier-to-final-risk transition. Externalisation changes where authority is loaded from; it does not widen the admitted surface universe.

## 7. Compatibility persists until an explicit scoped retirement

Existing compatibility surfaces remain active until expressly retired. Historical seam work is retained as evidence, while corrective work must address field-level ownership, transitive consumers and overstated downstream claims without rewriting history. (`P-ARCH-005`)

At this corpus point, the following remain expressly deferred:

- an independent parallel-risk authority beyond the admitted bounded work;
- a new final arbiter;
- dynamic coefficient redesign;
- broader portfolio replacement.

Missing Gates 151–156 cannot be inferred as authority. Compatibility therefore survives absence of evidence; it does not disappear because a later architecture would be tidier without it.

## 8. Public DTO projection is explicit and broker authority remains reserved

Public API output crosses an explicit projection boundary. That boundary may be either a dedicated egress adapter or narrower route-local code, but the choice must be deliberate and bounded. (`P-API-001`)

The public DTO must not depend on arbitrary internal dictionary shape, and projection logic must not bleed into orchestration. The broker boundary remains an interface or protocol reservation unless later admitted authority establishes more. A structural gap cannot be closed by inventing:

- a live adapter;
- network behaviour;
- credentials;
- external order execution;
- a broker lifecycle.

The exact DTO schema and broker protocol remain unstated.

## 9. Current authoritative position

The governance and boundary model is now:

1. canonical vocabulary is contract-linked, deterministic and regenerated from current governed surfaces;
2. routing, playbook hierarchy and carry terms have explicit owners;
3. runtime mutation is confined to eight named observable surfaces;
4. the coefficient scope distinguishes eight mutable surfaces, sixteen behavioural temporal thresholds and two timing parameters;
5. one typed authority validates ownership, units, baselines, envelopes, transforms and drivers;
6. runtime values load from that authority and carry exact lineage;
7. the `20.625` modifier outcome precedes the `13.4062` final-risk result;
8. compatibility persists until explicit scoped retirement;
9. absent successor gates do not create authority;
10. public DTO projection is explicit and broker integration remains protocol-only unless separately admitted.

## 10. Unresolved matters

The admitted corpus leaves open:

- vocabulary versioning and change approval;
- the detailed vocabulary population;
- the full identifiers for the sixteen temporal thresholds and two timing parameters;
- coefficient-authority persistence and general precedence beyond admitted examples;
- the contents and authority effects, if any, of missing Gates 151–156;
- later compatibility-retirement decisions;
- the exact public DTO schema and broker protocol.

These gaps cannot authorise hidden policy, unregistered coefficients, inferred retirements, orchestration bleed or fabricated live broker behaviour.

## Cross-references

- Advisory authority and live-trading ceiling: [Chapter 1](01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md).
- Raw/derived identity and contract provenance: [Chapter 2](02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md).
- Temporal thresholds and timing semantics: [Chapter 3](03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md).
- Stage ownership and routing: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Playbook hierarchy and modifier packet: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- DMPV3 compatibility and packet boundary: [Chapter 6](06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md).
- Final-risk ordering and capital authority: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Preview state, carry and persistence boundaries: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Coefficient review, replay and trace assurance: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
