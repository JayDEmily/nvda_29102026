# Gate 50 — Vocabulary Governance Rebase

Status: complete on `main`

## Purpose

Rebase the vocabulary-consolidation workflow onto the current live architecture so one term means one thing, aliases are governed, and stale labels cannot creep back into the runtime and planning stack.

## Why this gate exists

The harvested vocabulary workflow is good, but its payload snapshot is stale. The audit now defines the architecture surfaces that vocabulary governance must follow.

## Leaves in Gate 50

1. `LEAF-G50-001` — import the vocabulary workflow into the authoritative repo as feeder process only, not as blind payload truth.
2. `LEAF-G50-002` — regenerate the canonical vocabulary from the current repo surfaces after Gates 47–49 are pinned.
3. `LEAF-G50-003` — extend the vocabulary schema with `family`, `setup_variant`, `execution_expression`, `horizon`, `raw_or_derived`, `stage_owner`, and contract-linkage fields.
4. `LEAF-G50-004` — reconcile duplicate labels, aliases, and stale `session_clock`-era terms against the live architecture.
5. `LEAF-G50-005` — add enforcement tests that block duplicate conflicting labels, undefined aliases, and runtime surfaces missing canonical vocabulary entries.

## Entry rule

Gates 47 through 49 must be structurally pinned first.

## Exit rule

The vocabulary workflow is rebased onto current truth, duplicate labels are governed, and enforcement tests prevent silent language drift.

## Non-goals

- no blind merge of the stale vocabulary workspace;
- no free-form glossary disconnected from typed contracts;
- no vocabulary-first redesign of the runtime.

## Exit evidence

- Vocabulary workflow docs, canonical vocabulary schema/file, build script, and enforcement tests are in place.
