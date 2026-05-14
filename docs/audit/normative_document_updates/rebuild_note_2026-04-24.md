# Normative document rebuild note — 2026-04-24

## Scope

This rebuild reconstructs the later normative-control cleanup from conversation history on top of the recoverable repo state at `15db522`.

The rebuild does not claim byte-for-byte recovery of the lost transient commit `75eea7efb83814ba1f3a54b52b7f4388b313cad0`.

It creates a new verified reconstruction on `work/rebuild-final-normative-docs` and then merges that reconstruction to `main`.

## Rebuilt content

The rebuild reapplies the documented final control-doc state:

- `01` owns authority hierarchy, frozen repo invariants, the governed runtime sequence, serial/parallel boundaries, DMPV3 top-level packet-carriage law, and owner routing for lower control documents.
- `00` is the routing-only control-surface index.
- Core docs `02` through `10` remove verbose `Purpose` and `Change discipline` framing while retaining operative law.
- Working companions use `Local supplement` and `Rules` structure.
- `04.1` preserves the repo-wide source temporal standard and named temporal field set.
- `05.1` preserves temporal anti-drift guardrails.
- `09.1` preserves the DMPV3 temporal mapping subset.

## Validation gates rerun

The rebuild reran these checks:

- `git diff --check`
- grep for prohibited `may` and `should` wording across the amended control set
- grep for stale or ambiguous phrases removed during the cleanup pass
- direct checks for restored temporal fields: `captured_at_utc`, `persisted_at_utc`, `source_provider`, and `source_channel`
- direct checks for restored `01` authority hierarchy and binary done criteria
- direct check that `00` routes `01` as authority hierarchy, frozen repo invariants, and governed runtime sequence

## Status

The rebuild is a verified equivalent reconstruction, not a byte-identical recovery of the lost transient commit.

## Blueprint Alignment

This document is subordinate to `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

- All structures, stages, and components MUST align to architecture surfaces in `docs/11`.
- All terms MUST be defined in `docs/vocabulary/vocabulary_registry.md`.
- No definitions in this document may contradict `docs/11`.
