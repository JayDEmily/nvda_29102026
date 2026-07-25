# Automation boundary audit — P2 Recovery Part 1

Date: 2026-07-24 AEST

## Outcome

The prior batch-generated semantic insertion was disallowed and invalidated. It remains preserved only as historical audit evidence under `auditor_repair/`; it is not present in any current canonical receipt.

The replacement cycle used automation only for mechanical support. No automated process was authorised to decide or write authority matches, semantic relations, proof strengths, limitations, adversarial challenges, falsifiers, assertion-failure explanations or final dispositions.

## Mechanical automation used in the replacement cycle

| Operation | Purpose | Semantic judgement permitted | Result |
|---|---|---:|---|
| Ledger reset and count scripts | Reset affected flags and count current states | No | All 54 rows reset before replacement; current count 54 `YES` only after sequential closure |
| Hashing and path inventory | Preserve scope and detect mutation | No | 125 out-of-scope receipts and 724 protected paths unchanged |
| Exact text search | Find the invalid generated template and worker-specific paths | No | 0 template hits in current receipts; 0 worker-path hits |
| Per-file and aggregate pytest execution | Observe current test behaviour | No | 227 passed; exit 0 |
| Row validator | Enforce required receipt structure and controlled enums | No | 54/54 passed; validator explicitly does not establish semantic truth |
| Duplicate/generic detector | Surface repeated fields for human review | No | 30 schema/citation duplicates justified; 0 unresolved reasoning hits |
| Workbook generation and packaging | Present reproduced counts and create the handoff | No | Pending final extraction proof at package close |

## Human semantic work required and performed

For every sequence `067-120`, the replacement cycle required a fresh read of the complete test, the directly exercised runtime or specimen surface, the relevant governing propositions and the receipt. Each assertion group was then independently assessed for:

- the exact behaviour actually observed;
- whether governing authority owns that behaviour;
- the strongest lawful semantic relation and proof class;
- limitations and realistic false-positive paths;
- the exact assertion that would fail under the stated falsifier;
- the resulting file disposition and return gate.

The current receipts record those decisions group by group. Mechanical inventory of all 54 current receipt hashes is retained in `SELF_AUDIT_REPAIR_COMPLETION_INVENTORY.tsv`.

## Checks aimed specifically at disguised automation

- The exact invalid generated sentence frame has 0 occurrences in current canonical receipts.
- The detector examined 1,837 required semantic fields across 54 receipts.
- No exact duplicate was unresolved in the semantic reasoning fields.
- The 30 retained duplicate hits are controlled enum values or identical authority citations, each with occurrence-level review evidence.
- Historical files under `auditor_repair/` deliberately retain the rejected generated text so the failure is not erased.

## Limit of proof

A repository cannot cryptographically prove that prose was understood by a human rather than produced mechanically. The available evidence is the sequential reset/closure record, assertion-specific current text, absence of the rejected template, detector results, per-row validators, raw test outputs and preserved incident history. Independent Project Manager review remains necessary and is not pre-empted by this report.
