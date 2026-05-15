# Vocabulary Governance Remediation Receipt Before FWD-016

Status: `bounded_governance_remediation_recorded`

Scope:

- Resolved DEF-001 vocabulary governed source-hash coverage.
- Resolved DEF-002 durable row/architecture term governance through FWD-015 and the brief's high-risk term list.
- Resolved DEF-003 architecture-map freshness relative to ledger state after FWD-015.
- Did not open FWD-016 or any feature row.

## Fixed

- `src/nvda_desk/vocabulary_builder.py` `GOVERNED_SOURCE_PATHS` now includes authoritative vocabulary law/workflow/registry/builder/schema/audit/canonical artefacts.
- `data/vocabulary/canonical_vocabulary.json` was regenerated from the builder.
- `data/vocabulary/vocabulary_touch_stamp.json` was advanced only after the synonym audit had zero candidates.
- `docs/vocabulary/vocabulary_registry.md` now contains exact durable term registry headings for the admitted row/architecture terms.
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` now reflects FWD-010 through FWD-015 bounded-current ledger state and FWD-016 next/unopened status.

## Adjudicated

- Exact/new terms: event calendar, raw signal families, prepared ingress, runtime context, serial desk-cognition, serial candidate, capital deployment decision, opening architecture, downstream opening, placement readiness, placement handoff, broker protocol, live position, inventory architecture, exit architecture, close architecture, review layer, explanation layer, playbook library, modifier authority.
- Already governed exact: parallel risk lane.
- Alias-only/current entry enrichment: dynamic coefficient, DMPV3 packet.
- Near-match phrases from the remediation synonym audit were adjudicated into allowed aliases or disallowed non-term phrases in vocabulary artefacts; no scanner path exception or source-code suppression was added.

## Quarantined

None remaining after remediation; final synonym audit reported `candidates=0`.

## Blocked

None.

## Queued

FWD-016 remains the next roadmap row and remains unopened.

## Proof

See `VOCABULARY_GOVERNANCE_REMEDIATION_PROOF_SUMMARY.json` and `reports/` for command, stdout, stderr, and status evidence.
