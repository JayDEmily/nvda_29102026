# ACTIVE_CODE_ATLAS_001 three-way comparison plan

Status: `prepared_after_static_active_code_atlas_extraction`

## Purpose

Define the later comparison between:

1. recovered Atlas intent corpus: `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`;
2. Atlas Bridge/native satisfaction ledger: `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`;
3. static structural-inventory scaffold: `var/audit/active_code_atlas_001/active_code_atlas.json`.

This plan does not authorise source-code refactor, test implementation, vocabulary mutation, original Atlas/Bridge mutation, generated slice rebuild, or runtime/dependency changes.

## Comparison keys

| Key | Source | Role |
|---|---|---|
| `blueprint_surface` | Bridge and structural inventory scaffold | Primary architecture-surface join. |
| `target_owner` | Bridge and structural inventory scaffold | Owner-level join and conflict detector. |
| `lawful_owner_candidate` | Atlas and structural inventory scaffold | Candidate owner/path comparison. |
| `proof_family` | Atlas, Bridge, structural inventory scaffold | Test/proof work queue grouping. |
| `record_type` / `construct_type` | Atlas and structural inventory scaffold | Separates runtime, schema, config, test, receipt, and docstring evidence. |
| `source_file` / `source_line_*` | Atlas and structural inventory scaffold | Evidence audit trail only; donor and active source paths are not equivalent. |
| `observed_behaviour` | Atlas and structural inventory scaffold | Human review input; not a trusted semantic join by itself. |

## Comparison statuses

| Status | Meaning | Later action |
|---|---|---|
| `already_satisfied` | Structural inventory scaffold has native code/proof evidence that appears to satisfy the Bridge-mapped intent. | Confirm with targeted Tier A/B/C proof before any claim. |
| `partially_satisfied` | Active-code evidence exists but proof, seam, owner, status, or behaviour is incomplete. | Write or update tests before code changes. |
| `missing` | Bridge intent maps to a surface with no matching active-code record family. | Create tests first, then implement only if authorised. |
| `transform_required` | Donor idea exists but active architecture requires reshaping or owner migration. | Write migration brief and tests before code. |
| `blocked` | Vocabulary, owner, authority, or reserved-surface gate blocks migration. | Resolve authority blocker first. |
| `conflict` | Donor intent, Bridge owner, active code, or normative docs disagree. | Stop and adjudicate before tests or code. |

## Required comparison guardrails

- Do not treat the donor Atlas as runtime authority.
- Do not treat the active code as correctness authority.
- Do not treat docstrings as implementation proof.
- Do not treat static structural inventory scaffold records as test pass evidence.
- Queue Tier A/B/C proof from normative and Bridge gaps, not from convenience of existing code.
- Implementation/refactor remains closed until comparison output has a test-first work queue.

## Initial mechanical comparison method

1. Group Bridge records by `blueprint_surface`, `target_owner`, `proof_resolution`, and `implementation_leaf_type`.
2. Group structural inventory scaffold records by `blueprint_surface`, `target_owner`, `record_type`, `construct_type`, and `proof_family`.
3. For each Bridge group, detect active evidence classes present: runtime, schema/contract, config/data, test/proof, receipt/ledger, docstring.
4. Assign provisional comparison status using evidence class coverage and blockers.
5. Emit a comparison ledger with one row per Bridge group, not one row per donor record, to avoid 1,716-line noise before human adjudication.
6. Human-review unresolved/conflict/blocked rows before any tests or code are opened.

## Output target for the next authorised comparison pass

```text
var/audit/active_code_atlas_001/active_code_atlas_bridge_comparison.json
```

The comparison output must include counts by surface and by status, and must preserve links back to Atlas, Bridge, structural inventory scaffold, and normative evidence.


## External audit correction

The current artefact is classified as `ACTIVE_CODE_ATLAS_STRUCTURAL_INVENTORY_001` / static structural inventory scaffold only. It is useful navigation evidence, not the completed primary active-code Atlas.

Required limitation:

```text
This is static structural evidence only. It does not prove semantic correctness, native satisfaction, implementation maturity, or test pass status.
```

Selected contributing files must still be read in full surface-by-surface before records can be accepted as primary active-code Atlas records.
