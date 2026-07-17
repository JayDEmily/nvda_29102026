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
