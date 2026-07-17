# External Source Decisions

No external-source decision has yet been admitted.

## Decision 01-001 — Record architecture changes as explicit linked decisions

Status: accepted for normative unit `01/01.1`

Reviewed: 2026-07-17

Sources:
- Microsoft Azure Well-Architected Framework, “Maintain an architecture decision record (ADR)”: https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- IBM Cloud Architecture Framework, “Documenting your architecture decisions”: https://cloud.ibm.com/docs/architecture-framework?topic=architecture-framework-decision-template

Project-specific adaptation:
- Preserve numbered core documents as frozen baselines.
- Record admitted changes in numbered working overlays.
- Require explicit status, context, rationale, affected proposition, implications, and supersession.
- Do not treat external guidance as direct runtime authority.

Rejected interpretation:
- Rewriting accepted normative history in place, because it destroys why and when the architecture changed.

## Decision 01-002 — Use modular boundaries at known volatility points

Status: accepted as a top-level architecture principle; detailed application remains for later normative units

Reviewed: 2026-07-17

Source:
- Google Cloud Architecture Framework, “Promote modular design”: https://docs.cloud.google.com/architecture/framework/performance-optimization/promote-modular-design

Project-specific adaptation:
- Use bounded owners, explicit carriers, and clear interfaces so future input types, playbooks, policies, adapters, and persistence implementations can change without unrelated rewrites.
- Do not infer that this alpha system needs microservices or production distributed infrastructure.

## Decision 02-001 — Keep the runtime sequence stable while implementations remain replaceable

Status: accepted for normative unit `02/02.1`

Reviewed: 2026-07-17

Sources:
- Google Cloud Architecture Framework, “Promote modular design”: https://docs.cloud.google.com/architecture/framework/performance-optimization/promote-modular-design
- Microsoft Learn, “Common web application architectures”: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures

Project-specific adaptation:
- Keep the fourteen-step behavioural sequence fixed.
- Isolate variable inputs, playbooks, policies, adapters, and persistence implementations behind bounded contracts.
- Permit a modular monolith; do not infer microservices or cloud deployment.

## Decision 02-002 — Keep playbook decision logic independent from orchestration

Status: accepted for normative unit `02/02.1`

Reviewed: 2026-07-17

Source:
- IBM documentation, “Business rules”: https://www.ibm.com/docs/en/baw/25.0.x?topic=types-business-rules

Project-specific adaptation:
- Playbook definitions and selection rules are governed by the playbook library/registry boundary.
- Serial orchestration invokes that boundary and must not hard-code every playbook or a fixed playbook count.

## Decision 03-001 — Preserve identifier ownership and scope

Status: accepted for normative unit `03/03.1`

Reviewed: 2026-07-17

Sources:
- Google API Improvement Proposal AIP-122, “Resource names”: https://google.aip.dev/122
- IBM documentation, “Preparing data for data lineage”: https://www.ibm.com/docs/en/ws-and-kc?topic=lineage-preparing-data-data
- IBM documentation, “Data lineage”: https://www.ibm.com/docs/en/ws-and-kc?topic=governance-data-lineage

Project-specific adaptation:
- Each material identifier has an explicit originating owner, scope, uniqueness rule, stability rule, generation rule, and lawful absence rule.
- Source-issued identifiers remain source-issued truth.
- Repository capture identifiers name captured evidence and must not be presented as source-issued identifiers.
- Downstream packet, trace, run, correlation, hash, timestamp, filename, or array-position values cannot substitute for a missing authoritative identity.

Rejected interpretations:
- Requiring every source to provide a globally unique identifier when the source contract does not make that guarantee.
- Treating one UUID-shaped field as sufficient lineage regardless of its owner and meaning.

## Decision 03-002 — Isolate external-source semantics at explicit adapters

Status: accepted for normative unit `03/03.1`

Reviewed: 2026-07-17

Source:
- Microsoft Azure Architecture Center, “Anti-Corruption Layer pattern”: https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer

Project-specific adaptation:
- Provider-specific protocols, field names, omissions, and semantics are translated at an explicit ingress adapter or source reader.
- The internal domain consumes typed native carriers rather than provider-native dictionaries or hidden source assumptions.
- The adapter performs translation and validation; it does not acquire candidate, risk, capital, broker, exit, close, or review authority.

Rejected interpretation:
- Creating a separate service or microservice solely because the cited pattern can be deployed that way. A component inside the modular monolith is lawful.

## Decision 03-003 — Version input contracts and preserve captured evidence without adopting blanket event sourcing

Status: accepted for normative unit `03/03.1`

Reviewed: 2026-07-17

Sources:
- Microsoft Azure Architecture Center, “Event-Driven Architecture Style”: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven
- Microsoft Azure Architecture Center, “Event Sourcing pattern”: https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing

Project-specific adaptation:
- Input-family contracts carry an explicit schema/contract version.
- Captured source evidence and its identity remain traceable when later typed or derived representations evolve.
- Consumers must not infer a different input family from payload shape merely to continue processing.

Rejected interpretations:
- Adopting event sourcing, distributed messaging, append-only production stores, or event-driven deployment as a repository-wide requirement. The source explicitly warns that event sourcing adds material complexity and should be adopted only where its benefits justify it.

## Decision 04-001 — Invert infrastructure dependencies at explicit assembly boundaries

Status: accepted for normative unit `04/04.1`

Reviewed: 2026-07-17

Sources:
- Google Cloud Architecture Framework, “Promote modular design”: https://docs.cloud.google.com/architecture/framework/performance-optimization/promote-modular-design
- Microsoft Learn, “Common web application architectures”: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
- Microsoft Azure Architecture Center, “Anti-Corruption Layer pattern”: https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer

Project-specific adaptation:
- Domain/application behaviour depends on explicit contracts for external sources, persistence, clocks, identifiers and configuration.
- Concrete implementations are selected at one explicit application assembly boundary rather than instantiated inside domain decisions or held in module-global mutable state.
- Provider semantics terminate at the adapter boundary and become typed native carriers.

Rejected interpretations:
- Requiring microservices, separate deployables, a dynamic plugin system, or a specific dependency-injection framework.
- Splitting every small component merely to maximise interface count; modularity is applied at known volatility and authority boundaries.

## Decision 04-002 — Separate state-boundary contracts from concrete alpha durability

Status: accepted for normative unit `04/04.1`

Reviewed: 2026-07-17

Sources:
- Microsoft Learn, “Common web application architectures”: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
- Google Cloud Well-Architected Framework: https://docs.cloud.google.com/architecture/framework

Project-specific adaptation:
- Repository/store contracts isolate state ownership from concrete infrastructure.
- In-memory implementations are lawful for alpha tests and incomplete flows only when labelled volatile and non-durable behind the bounded contract.
- A database dependency or ORM is implementation availability, not proof of active persistence or an architecture lock.
- Production persistence requirements remain undecided until actual operating evidence exists.

Rejected interpretations:
- Building production storage, availability, backup, retention or recovery machinery before requirements exist.
- Calling an implementation durable because its class is named repository or store.

## Decision 04-003 — Distinguish deterministic domain re-execution from original packet preservation

Status: accepted for normative unit `04/04.1`

Reviewed: 2026-07-17

Sources:
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- CloudEvents primer: https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md
- Microsoft Azure Architecture Center, “Event Sourcing pattern”: https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing

Project-specific adaptation:
- DMP packet context metadata and module payload meaning remain separate.
- Deterministic re-execution compares domain result and semantic fingerprint under identical authoritative inputs and material versions.
- Exact original-envelope proof requires preserving and reading the original envelope; a newly emitted replay result is not represented as the original packet.
- Current emission metadata is excluded from the semantic result fingerprint, while all material source, contract, configuration, policy, dependency and algorithm versions are included.

Rejected interpretations:
- Using DMP packet `id` as a source/domain identifier.
- Requiring event sourcing or a production event store to prove alpha-stage deterministic algorithms.
- Claiming byte-identical replay while regenerating wall-clock emission fields.
