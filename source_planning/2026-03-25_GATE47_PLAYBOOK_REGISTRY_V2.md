# Gate 47 — Playbook Registry v2

Status: complete on `main`

## Purpose

Replace the flat playbook registry with a hierarchy that can represent trader-real families, setup variants, execution expressions, and horizon constraints without breaking the deterministic runtime order.

## Why this gate exists

The current checked-in registry spec is flat and stale relative to runtime reality. The repo now has more named playbooks than the registry spec admits, and the next tranche needs a structure that can grow without taxonomy bloat.

## Leaves in Gate 47

1. `LEAF-G47-001` — define the typed registry-v2 schema with at least `family`, `setup_variant`, `execution_expression`, `horizon`, `priority`, `constraints`, and `risk_overrides`.
2. `LEAF-G47-002` — map the current seven live playbooks into registry-v2 family rows and define the compatibility bridge from the flat registry.
3. `LEAF-G47-003` — update checked-in config and replay fixtures to registry-v2 without inventing extra trader leaves.
4. `LEAF-G47-004` — update runtime readers and deterministic tests so playbook eligibility consumes registry-v2 without behaviour drift.
5. `LEAF-G47-005` — document the registry-v2 non-goals, including what remains an overlay, what remains an execution template, and what does not become a top-level family.

## Entry rule

Gate 46 must be complete and the audit finding about registry staleness must be frozen in the authoritative tree.

## Exit rule

A typed registry-v2 exists, current live playbooks are represented through the hierarchy, the compatibility bridge is explicit, and deterministic tests stay green.

## Non-goals

- no invention of every hypothetical trader play;
- no collapse of posture/risk and playbook layers into one object;
- no LLM-facing ontology work.

## Exit evidence

- Registry-v2 exists in typed schemas, checked-in config, replay fixtures, runtime readers, and deterministic tests.
