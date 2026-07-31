# Chat audit and selected-handoff repair — review and disposition

## Scope

Canonical base: `55e3b0b154bcd1829de133222f1c5ce0a13a1361`.

The user supplied the novel audit and M05 selected handoff as consideration, not authority. This repair admits only propositions supported by the live normative contracts.

## Admitted audit findings

- M03 must reconcile source validation/limitations, multi-source payload fields, field-resolution selected values and derivation outputs against the emitted typed payload.
- M05 `StageContext` must use the exact M03 validation/completeness domains and enforce their state/gap consistency.
- M05 non-formed terminal results must preserve the actual failed-stage output; an empty output prefix cannot claim a failed stage.
- M06 VIX thresholds must be non-negative and ordered.
- M06 v1 evaluator and aggregation logic must reject unsupported policy/version labels rather than execute fixed logic under arbitrary names.
- Positive metamorphic properties from the audit are admitted as regression checks where they exercise the public seam.

## Admitted handoff proposition

Every M05 terminal serial result has a deterministic `serial_result_id` derived from its semantic fingerprint. Only a formed result additionally has a distinct `candidate_id`. Identity-role substitution must fail closed.

This proposition is consistent with the minimum replay-envelope requirement for a bounded output identity and strengthens terminal-result traceability without changing stage ownership or execution order.

## Dismissed handoff material

The following are not integrated:

- cumulative stage dependencies;
- six separate stage contexts;
- generated `not_evaluated` stage outputs;
- generic registered payload carriers;
- Worker A control receipts and raw validation logs.

They conflict with the accepted common-context/selective-dependency architecture, replace the bounded carrier model, or require a separate normative decision.
