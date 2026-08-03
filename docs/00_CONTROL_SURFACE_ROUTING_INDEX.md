# 00_CONTROL_SURFACE_ROUTING_INDEX

## Purpose

This file is a document-level directory for LLM plan construction. It does not define normative meaning, precedence, execution scope or mutation authority.

The active ExecPlan must name the exact normative document families governing its bounded work. Read every prose document in each selected family in full, in the listed order. Do not use search results, excerpts, headings or summaries as substitutes for the complete read.

For cross-cutting work, select the union of all applicable families. If execution reveals an additional material family, amend the ExecPlan before relying on or changing that family.

## Normative document families

| Family | Route when the work concerns | Read in full, in order |
|---|---|---|
| `01` — normative authority | authority hierarchy, frozen repo invariants, runtime-sequence boundaries, controlled normative amendment or semantic reconciliation | `docs/01_NORMATIVE_CORE.md`; `docs/01.1_NORMATIVE_WORKING.md` |
| `02` — operating model | desk operating behaviour, runtime progression, serial cognition, parallel risk, downstream operating flow or signal-informed intraday phase | `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`; `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md`; `docs/02.2_SIGNAL_INFORMED_INTRADAY_PHASE_WORKING.md` |
| `03` — domain model | domain entities, contracts and meanings, typed inputs, options data, source identity, calendar or temporal domain truth | `docs/03_DOMAIN_MODEL_CORE.md`; `docs/03.1_DOMAIN_MODEL_WORKING.md`; `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md` |
| `04` — technical architecture | technical components, seams, data preparation, prepared envelopes, merge policy, stage carriers or structural integration | `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`; `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` |
| `05` — guardrails | prohibited shortcuts, architectural drift, authority leakage, unsafe substitutions or anti-patterns | `docs/05_GUARDRAILS_CORE.md`; `docs/05.1_GUARDRAILS_WORKING.md` |
| `06` — process and tranche law | planning, active-plan selection, read/write scope, semantic gates, execution sequencing, evidence, receipts or closeout | `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`; `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` |
| `07` — ownership, state and replay | runtime ownership, producers and consumers, module contracts, state, persistence, transaction boundaries, risk joins or authoritative replay | `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`; `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` |
| `08` — testing and promotion | test authority, proof tiers, normative lineage, test preservation, environment provenance, promotion, receipts or operational assurance | `docs/08_TESTING_AND_PROMOTION_CORE.md`; `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` |
| `09` — DMPV3 protocol | packet envelope, packet roles, producer identity, lineage, validation, degraded states, carriage or protocol extension | `docs/09_DMPV3_PROTOCOL_CORE.md`; `docs/09.1_DMPV3_PROTOCOL_WORKING.md` |
| `10` — vocabulary governance | durable-term admission, canonical IDs, namespaces, aliases, prohibited phrases, semantic decisions or vocabulary generation | `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`; `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`; `docs/vocabulary/README.md`; `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` |
| `11` — native architecture blueprint | native package placement, module allocation, component form, seams, persistence placement, dependency planes, test-family mapping or architecture traceability | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` |

## Structured vocabulary lookup

For read-only lookup of an already admitted term, query `data/vocabulary/canonical_vocabulary.json` by exact canonical ID or namespace. This is the machine-readable projection of the existing vocabulary system.

Any change to vocabulary meaning, admission, namespace, aliasing, prohibited usage, schema or generation must route through family `10` and its complete prose read set. A JSON record lookup does not replace vocabulary-governance reading for semantic change.

## Execution-state route

Read `ROADMAP_LEDGER.md` for current state. Read `EXEC_PLAN.md` only when the roadmap names it as active. Historical plans, receipts, handovers and programme records do not become current authority because they retain active-sounding language.
