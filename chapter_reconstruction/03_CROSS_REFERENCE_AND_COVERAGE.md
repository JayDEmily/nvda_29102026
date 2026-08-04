# Cross-reference and proposition coverage

## Coverage result

The approved 83-proposition substrate is projected into ten chapters. Every proposition has exactly one primary chapter; secondary chapter references remain dependency pointers and do not create alternate canonical wording. This report is a mechanically generated coverage projection from `02_PROPOSITION_TO_CHAPTER_MAP.tsv`, supplemented by the explicit authority-state controls below.

| Chapter | Primary count | Primary propositions |
|---|---:|---|
| [01. System Purpose and Advisory Limits](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md) | 10 | `P-CTX-001`, `P-OPT-001`, `P-CTX-002`, `P-PLAY-001`, `P-EXE-001`, `P-DEC-001`, `P-REV-001`, `P-REV-002`, `P-RES-001`, `P-LEG-001` |
| [02. Data Truth from Source to Stage Inputs](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md) | 11 | `P-DAT-001`, `P-DAT-002`, `P-DAT-003`, `P-DAT-004`, `P-DAT-005`, `P-TRACE-001`, `P-TRACE-002`, `P-ARCH-002`, `P-ARCH-007`, `P-ARCH-009`, `P-ARCH-010` |
| [03. Temporal Truth, Calendars and Provenance](chapters/03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md) | 9 | `P-TMP-001`, `P-TMP-002`, `P-TMP-003`, `P-TMP-004`, `P-TMP-005`, `P-PROTO-004`, `P-TMP-006`, `P-TMP-007`, `P-TMP-008` |
| [04. Serial Cognition and Stage Ownership](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md) | 8 | `P-ARCH-001`, `P-ARCH-006`, `P-ARCH-008`, `P-SERIAL-001`, `P-CTX-003`, `P-ARCH-004`, `P-TRACE-006`, `P-DEC-002` |
| [05. Playbooks, Posture Modifiers and Execution Choices](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md) | 7 | `P-PLAY-002`, `P-PLAY-003`, `P-PLAY-004`, `P-PLAY-005`, `P-PLAY-006`, `P-EXE-004`, `P-GOV-007` |
| [06. DMP Protocol Evolution and Packet Carriage](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md) | 6 | `P-PROTO-001`, `P-PROTO-002`, `P-PROTO-003`, `P-PROTO-005`, `P-PROTO-006`, `P-ARCH-003` |
| [07. Parallel Risk, Terminal Risk and Capital](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md) | 8 | `P-RISK-001`, `P-RISK-002`, `P-RISK-003`, `P-PRISK-001`, `P-PRISK-002`, `P-PRISK-003`, `P-CAP-001`, `P-CAP-002` |
| [08. Execution Lifecycle, Carry, State and Persistence](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md) | 8 | `P-EXE-002`, `P-STATE-001`, `P-EXE-003`, `P-CARRY-001`, `P-CARRY-002`, `P-PERSIST-001`, `P-PERSIST-002`, `P-PERSIST-003` |
| [09. Review, Trace, Replay and Assurance](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md) | 8 | `P-TRACE-003`, `P-TRACE-004`, `P-TRACE-005`, `P-TRACE-007`, `P-REV-003`, `P-REV-004`, `P-REPLAY-001`, `P-TEST-001` |
| [10. Governance, Compatibility and Public Boundaries](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) | 8 | `P-GOV-001`, `P-GOV-002`, `P-GOV-003`, `P-GOV-004`, `P-GOV-005`, `P-GOV-006`, `P-ARCH-005`, `P-API-001` |

**Total primary assignments:** 83.

## Cross-reference flow

| Primary chapter | Referenced chapters |
|---|---|
| Ch. 01 | [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 02 | [Ch. 01](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md), [Ch. 03](chapters/03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 03 | [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 06](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 04 | [Ch. 01](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md), [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 06](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 05 | [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 06 | [Ch. 03](chapters/03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 07 | [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 06](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 08 | [Ch. 01](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 09 | [Ch. 01](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md), [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 03](chapters/03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 06](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 10](chapters/10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md) |
| Ch. 10 | [Ch. 02](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md), [Ch. 03](chapters/03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md), [Ch. 04](chapters/04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md), [Ch. 05](chapters/05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md), [Ch. 06](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md), [Ch. 07](chapters/07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md), [Ch. 08](chapters/08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md), [Ch. 09](chapters/09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md) |

## Authority-state visibility controls

- `P-RES-001` remains **unresolved** in [Chapter 1](chapters/01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md): bounded admission and reserved/containment remain conditional branches until external admissibility evidence is formally admitted.
- `P-ARCH-010` remains **unresolved** in [Chapter 2](chapters/02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md): the exact prepared-to-cognition translation location and owner are not selected by the admitted corpus.
- `P-PROTO-002` remains **partially superseded** in [Chapter 6](chapters/06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md): DMP v2 survives except at the explicitly replaced serial-runtime downstream boundary where DMPV3 becomes canonical.

## Dependency interpretation

1. Chapters 1–3 establish authority ceilings, data truth and temporal truth.
2. Chapters 4–6 establish ordered cognition, decision ownership and governed packet carriage.
3. Chapters 7–8 apply independent risk, capital, lifecycle and persistence constraints.
4. Chapter 9 exposes the resulting decision and authority chains for review, replay and assurance.
5. Chapter 10 governs vocabulary, mutable policy, compatibility and public boundaries across all earlier chapters.

## Validation boundary

The chapter validator checks unique assignment, references, file existence and explicit visibility of unresolved and partially superseded propositions. It cannot determine whether the prose has preserved every source qualification, threshold, branch or semantic consequence. That remains a proposition-by-proposition semantic review obligation against the approved reconstruction and cited immutable sources.
