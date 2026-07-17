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
