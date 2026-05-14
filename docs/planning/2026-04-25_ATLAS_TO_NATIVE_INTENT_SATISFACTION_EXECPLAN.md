# Atlas-to-Native Intent Satisfaction ExecPlan v0.5.1

Date: 2026-04-26  
Status: Terminology-normalised revision aligned to the post-Gate-3 Bridge baseline  
Scope: Completed Atlas satisfaction audit against an accepted native architecture blueprint  
Relationship: This brief executes only after `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` exists, is vocabulary-lawful, and is accepted by the control stack.  
Alignment baseline: `repo_bridge_post_gate3_pass_2026-04-26.zip`  
Alignment branch: `work/bridge-gate3-blueprint-authority-20260426`  
Alignment commit: `a8a3ceaf53079a3fefddb1fd3e321a1f64384c0f`  
Alignment note: This revision normalises Bridge terminology only. It does not change Bridge scope, authority, pass criteria, or the validity of already-completed Gates 1-3.  

---

## 1. Purpose

This ExecPlan controls the Bridge step after the Legacy Intent Atlas is complete and after the Native Blueprint Stabilisation tranche is complete.

The Bridge compares recovered legacy intent against the accepted native architecture blueprint.

The Bridge produces a native intent satisfaction ledger.

The first Bridge run is ledger-only.

The Bridge does not implement runtime behaviour.  
The Bridge does not modify feature tests.  
The Bridge does not modify runtime code.  
The Bridge does not modify config, schema, database, packet, or docstring surfaces for feature work.  
The Bridge does not copy legacy files.  
The Bridge does not treat Atlas owner candidates as native authority.  
The Bridge does not use user vernacular as normative language.

---

## 2. Binary execution rule

Every instruction in this brief is binary.

A required action must be performed.  
A prohibited action must not be performed.  
A blocker stops completion.  
A completed item must carry evidence.  
An unevidenced item remains incomplete.

Loose permission wording is prohibited in outputs created under this Bridge.

---

## 3. Required prior state

The Bridge cannot start until all prior-state conditions are true.

Required prior state:

1. `docs/planning/2026-04-25_NATIVE_BLUEPRINT_STABILISATION_EXECPLAN.md` exists.
2. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` exists.
3. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` is accepted by the control stack.
4. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` follows the required sequential architecture order.
5. Every architecture surface in `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` has an implementation-truth status.
6. Durable terms in `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` are vocabulary-lawful or explicitly blocked.
7. The Native Blueprint Stabilisation provenance register exists.
8. The Native Blueprint Stabilisation planning carry-forward register exists.
9. The Native Blueprint Stabilisation normative reconciliation report exists.
10. The Native Blueprint Stabilisation vocabulary admission report exists.
11. The completed Atlas artefacts exist.
12. The completed Atlas coverage view records no uncovered donor ranges for accepted Atlas scope.
13. The completed Atlas has passed granularity review.

If any prior-state condition fails, stop. Do not run the Bridge.

---

## 4. Authority model

The Bridge separates five authority surfaces.

### 4.1 Native authority

Native authority is the accepted control stack.

The target architecture authority for this Bridge is:

```text
docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md
```

Target-owner mapping must pass through `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

### 4.2 Atlas evidence

The Legacy Intent Atlas is descriptive evidence.

It records observed legacy behaviour, recovered intent, provenance, owner candidates, caveats, coverage, exclusions, and rebuild-readiness state.

The Atlas does not override native authority.

### 4.3 Vocabulary authority

Vocabulary governance is a blocking semantic admission system.

No implementation-bound Bridge record can proceed unless all durable native language is admitted, reused, enriched, aliased, quarantined, or blocked under vocabulary law.

### 4.4 Test and proof authority

Tier A, Tier B, Tier C, retained-test registry, proof blocks, checkpoint declarations, and docstring declarations remain governed by the accepted testing and promotion law.

The Bridge records proof requirements. It does not execute feature implementation proof.

### 4.5 Vernacular Bridge status

The Vernacular Bridge is a translation aid only.

It can help translate user language into repo handles during analysis.

It cannot be cited as native authority.

It cannot introduce durable terminology into normative docs, ledgers, tests, code, schemas, configs, packets, or docstrings.

---

## 5. Required baselines

Every Bridge run must bind to exact baselines.

The satisfaction ledger must record:

- native repo branch
- native repo commit
- active bounded pack path
- accepted blueprint document path
- accepted blueprint commit
- accepted vocabulary commit
- accepted normative stack commit
- completed Atlas bundle manifest checksum
- Atlas closeout report checksum
- Atlas intent atlas checksum
- Atlas coverage view checksum
- Atlas owner map checksum
- Atlas rebuild queue checksum
- Atlas exclusion register checksum
- Bridge ExecPlan version
- ledger schema version

A satisfaction claim without these baselines is invalid.

If the native repo, blueprint, vocabulary, or Atlas changes, the satisfaction ledger must be superseded or revalidated under a new Bridge run.

---

## 6. Inputs

### 6.1 Required Bridge inputs

The Bridge must read in full:

1. `AGENTS.md`
2. active bounded pack for this Bridge
3. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
4. `docs/01_NORMATIVE_CORE.md`
5. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
6. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
7. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
8. `config/retained_test_registry.yaml`
9. `config/proof_blocks.yaml`
10. `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`
11. `var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json`
12. `var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json`
13. `var/audit/imports/atlas_bridge_inputs/legacy_rebuild_queue_view.json`
14. `var/audit/imports/atlas_bridge_inputs/legacy_exclusion_register.json`
15. `var/audit/imports/atlas_bridge_inputs/NVDA6_intent_atlas_salvage_closeout_report.md`
16. `var/audit/imports/atlas_bridge_inputs/atlas_bridge_input_manifest.json`
17. Native Blueprint Stabilisation provenance register
18. Native Blueprint Stabilisation planning carry-forward register
19. Native Blueprint Stabilisation normative reconciliation report
20. Native Blueprint Stabilisation vocabulary admission report

### 6.2 Native evidence inputs

For each Atlas intent unit, the Bridge must read the native surfaces required to classify satisfaction:

- target architecture surface in `docs/11`
- native code surface for the target owner
- native tests for the target owner
- retained-test registry entries for the proof family
- proof block entries for the proof family
- config/schema/packet surfaces connected to the target owner
- docstrings on the owned native surface
- vocabulary entries used by the target owner

---

## 7. Full-read rule

Every in-scope source must be read in full before it is used as evidence.

Filename lists, grep hits, summaries, snippets, headings, extracted symbols, and embeddings do not satisfy this requirement.

A claim that a source was reviewed is prohibited unless that source was read in full.

Every material claim in the satisfaction ledger must carry file path and line evidence, sheet and row evidence, checksum evidence, or exact tool output.

---

## 8. Authorised touched surfaces

The first Bridge run is ledger-only.

Authorised touched surfaces:

- `docs/planning/2026-04-25_ATLAS_TO_NATIVE_INTENT_SATISFACTION_EXECPLAN.md`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_validation_report.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_provenance_register.json`

No runtime source, feature test, config, schema, packet contract, database, proof block, retained-test registry, vocabulary surface, or docstring surface is authorised for feature implementation change during the first Bridge run.

Vocabulary surfaces are read-only in the first Bridge run.

A vocabulary issue produces a blocked Bridge record, not a vocabulary edit.

---

## 9. Prohibited work

The Bridge must not:

- implement native behaviour
- modify runtime source
- modify feature tests
- modify config for feature behaviour
- modify schemas for feature behaviour
- modify packet contracts for feature behaviour
- modify database or persistence surfaces for feature behaviour
- modify docstrings for feature behaviour
- modify retained-test registry for feature behaviour
- modify proof blocks for feature behaviour
- modify vocabulary surfaces in the first Bridge run
- copy legacy code
- create file-to-file migration instructions
- use Atlas owner candidates as native authority
- use the Vernacular Bridge as authority
- use user vernacular in durable native language
- classify a coarse Atlas record as accepted when the record boundary loses one lawful owner, one bounded behavioural job, or one bounded proof family
- convert `thin_seam`, `placeholder`, `reserved`, or `future_only` blueprint architecture surfaces into implementation work automatically
- call missing behaviour implemented
- call a docstring match satisfaction when runtime code differs
- call a name match satisfaction without behavioural evidence

---

## 10. Atlas input contract

The completed Atlas must provide enough granularity to adjudicate native satisfaction.

Each accepted Atlas record must provide:

- Atlas record ID
- intent unit ID
- donor source path
- donor line start
- donor line end
- record type
- construct type
- symbol name
- evidence status
- observed behaviour
- intended behaviour
- inputs
- outputs
- state reads
- state writes
- external dependencies
- packet effects
- schema effects
- config effects
- coefficient effects
- thresholds and literals
- branch conditions
- null semantics
- empty semantics
- error semantics
- side effects
- known defects
- caveats
- owner candidate
- owner confidence
- proof family state
- rebuild-readiness state
- exclusion reason where applicable

If the Atlas does not provide enough information for one lawful owner, one bounded behavioural job, and one bounded proof family, the Bridge record must be blocked for Atlas granularity.

---

## 11. Native satisfaction statuses

Each Bridge record must classify native satisfaction as exactly one of:

| Status | Meaning |
|---|---|
| `pending_gate6` | Atlas-to-blueprint mapping is recorded, but Gate 6 native satisfaction adjudication has not yet been executed. |
| `already_satisfied` | Native code/config/schema/test/proof evidence satisfies the accepted intent under `docs/11`. |
| `partially_satisfied` | Native owner and seam exist, but recovered lawful behaviour is incomplete. |
| `missing` | Accepted lawful intent has no satisfying native implementation. |
| `transform_required` | Legacy intent is useful but must move to a different lawful native owner or be expressed under different vocabulary. |
| `excluded` | Legacy intent is not part of native architecture. |
| `blocked_blueprint` | `docs/11` lacks a sufficient architecture surface, owner, seam, or truth status. |
| `blocked_vocabulary` | Durable native language is not vocabulary-lawful. |
| `blocked_atlas_granularity` | Atlas record boundary is too coarse for satisfaction adjudication. |
| `blocked_evidence` | Required native or Atlas evidence is missing. |
| `blocked_conflict` | Native authority surfaces conflict. |

During Gate 4 mapping and Gate 5 vocabulary adjudication, use `pending_gate6` until Gate 6 native satisfaction adjudication is executed.

---

## 12. Blueprint architecture-surface status handling

Every Atlas intent mapped to `docs/11` must preserve the target architecture-surface implementation-truth status.

Allowed blueprint architecture-surface implementation-truth statuses:

- `implemented`
- `thin_seam`
- `placeholder`
- `reserved`
- `future_only`
- `legacy_only`
- `rejected`

Rules:

1. `implemented` requires native code and proof evidence.
2. `thin_seam` can support `partially_satisfied` or `missing` classification.
3. `placeholder` can support `partially_satisfied` or `missing` classification.
4. `reserved` blocks implementation work until a later implementation tranche admits work for that architecture surface.
5. `future_only` blocks implementation work until a later implementation tranche admits work for that architecture surface.
6. `legacy_only` cannot become native work through this Bridge.
7. `rejected` produces `excluded` unless current authority conflict is found.

---

## 13. Target-owner mapping rule

Target-owner mapping must use this order:

1. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
2. accepted normative docs referenced by `docs/11`
3. native code owner evidence
4. native tests and proof evidence
5. Atlas owner candidate as descriptive evidence only
6. Vernacular Bridge as translation aid only

A target owner must not be assigned directly from the Atlas owner candidate.

A target owner must not be assigned from vernacular wording.

A target owner must not be assigned from filename similarity alone.

---

## 14. Vocabulary gate

Every Bridge record must include a vocabulary gate.

The vocabulary gate must classify all durable native language connected to the record.

Durable language includes:

- architecture surface names
- owner names
- class names
- public function names
- packet fields
- schema keys
- config keys
- ledger keys
- enum values
- proof block IDs
- retained-test family IDs
- checkpoint surface names
- docstring-declared concepts
- durable planning terms

Allowed vocabulary gate statuses:

- `pending_gate5`
- `not_required`
- `passed_reuse_existing`
- `passed_new_terms_already_admitted`
- `blocked_admission_required`
- `blocked_synonym_collision`
- `blocked_disallowed_phrase`
- `blocked_overloaded_term`
- `blocked_unchecked`

If the gate status starts with `blocked_`, the Bridge record cannot become implementation-bound.

During Gate 4 mapping, use `pending_gate5` when vocabulary adjudication has not yet been executed.

The first Bridge run records vocabulary blockers. It does not perform vocabulary admission.

---

## 15. Proof-family resolution

Every Bridge record must record proof posture.

Allowed proof tiers:

- `pending_gate7`
- `Tier A`
- `Tier B`
- `Tier C`
- `none`
- `blocked_unresolved`

A Tier A claim is blocking governed proof.

A Tier B claim is bounded shadow proof.

A Tier C claim is historical, observational, or non-blocking proof.

During Gate 4 mapping and Gate 6 satisfaction audit, use `pending_gate7` until Gate 7 resolves proof posture.

Proof-family resolution must cite:

- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`
- native test files where relevant

The Bridge does not create or modify tests.

The Bridge records whether a later implementation leaf must reuse an existing test family, extend an existing family, admit a new family, or perform no test work.

---

## 16. Existing-test decision rule

Every missing or partial accepted intent must record one existing-test decision:

- `pending_gate7`
- `reuse_existing_same_invariant`
- `extend_existing_same_invariant`
- `new_test_family_required`
- `no_test_change_required`
- `blocked_unresolved`

Before Gate 7, use `pending_gate7` when existing-test adjudication has not yet been executed.

An existing test can be extended only when the recovered obligation strengthens the same invariant already owned by that test.

If the recovered obligation is adjacent, distinct, or broader than the existing invariant, a new test family is required.

The Bridge records the decision. It does not edit tests.

---

## 17. Checkpoint and docstring decision rule

Every missing or partial accepted intent must record:

- checkpoint declaration required: true, false, or null before Gate 7
- docstring declaration required: true, false, or null before Gate 7
- rationale evidence

Checkpoint declaration decisions must cite testing and promotion law, checkpoint helper surfaces, and owned test proof where relevant.

Docstring declaration decisions must cite runtime code first and docstrings second.

Runtime code is the truth surface when runtime code and docstrings diverge.

---

## 17.1 Gate-scoped staged placeholder rule

The first Bridge run is sequential across Gates 1-9.

A Bridge record may therefore exist before all later-gate decisions are available.

When a record is created during Gate 4 mapping:

- `vocabulary_gate.status` must be `pending_gate5` unless Gate 5 has already executed for that record
- `native_satisfaction_status` must be `pending_gate6` unless Gate 6 has already executed for that record
- `proof_resolution.tier`, `proof_resolution.test_family_action`, and `proof_resolution.proof_block_action` must be `pending_gate7` unless Gate 7 has already executed for that record
- `existing_test_decision` must be `pending_gate7` unless Gate 7 has already executed for that record
- `checkpoint_declaration_required` may be `null` until Gate 7 executes
- `docstring_declaration_required` may be `null` until Gate 7 executes
- `implementation_leaf_required` may be `null` until Gate 7 executes
- `implementation_leaf_type` must be `pending_gate7` until Gate 7 executes

A staged placeholder is lawful only when the later gate that owns the field has not yet executed.

---

## 18. Required ledger artefacts

Create:

```text
var/audit/ledgers/intent_migration/native_intent_satisfaction_provenance_register.json
var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json
var/audit/ledgers/intent_migration/native_intent_satisfaction_validation_report.json
```

The provenance register records baselines and sources.

The satisfaction ledger records every Atlas intent adjudication.

The validation report records schema validation, duplicate-ID validation, blocked-record counts, evidence checks, and final git diff surface checks.

---

## 19. Native intent satisfaction ledger schema

The satisfaction ledger must conform to this schema or a stricter repo-admitted successor.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://nvda6.local/schemas/native_intent_satisfaction_ledger.v1.schema.json",
  "title": "NativeIntentSatisfactionLedgerV1",
  "type": "object",
  "required": [
    "ledger_name",
    "schema_version",
    "status",
    "bridge_execplan_path",
    "baselines",
    "records"
  ],
  "additionalProperties": false,
  "properties": {
    "ledger_name": {"const": "native_intent_satisfaction_ledger"},
    "schema_version": {"const": "v1"},
    "status": {"enum": ["draft", "in_progress", "complete", "blocked", "superseded"]},
    "bridge_execplan_path": {"const": "docs/planning/2026-04-25_ATLAS_TO_NATIVE_INTENT_SATISFACTION_EXECPLAN.md"},
    "baselines": {
      "type": "object",
      "required": [
        "native_repo_branch",
        "native_repo_commit",
        "active_bounded_pack_path",
        "accepted_blueprint_path",
        "accepted_blueprint_baseline_branch",
        "accepted_blueprint_baseline_commit",
        "accepted_vocabulary_commit",
        "accepted_normative_stack_commit",
        "completed_atlas_bundle_manifest_checksum",
        "atlas_closeout_report_checksum",
        "atlas_intent_atlas_checksum",
        "atlas_coverage_view_checksum",
        "atlas_owner_map_checksum",
        "atlas_rebuild_queue_checksum",
        "atlas_exclusion_register_checksum",
        "bridge_execplan_version",
        "ledger_schema_version"
      ],
      "additionalProperties": false,
      "properties": {
        "native_repo_branch": {"type": "string", "minLength": 1},
        "native_repo_commit": {"type": "string", "pattern": "^[0-9a-f]{7,40}$"},
        "active_bounded_pack_path": {"const": "intent_migration/native_intent_satisfaction/AGENTS.override.md"},
        "accepted_blueprint_path": {"const": "docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md"},
        "accepted_blueprint_baseline_branch": {"type": "string", "minLength": 1},
        "accepted_blueprint_baseline_commit": {"type": "string", "pattern": "^[0-9a-f]{7,40}$"},
        "accepted_vocabulary_commit": {"type": "string", "pattern": "^[0-9a-f]{7,40}$"},
        "accepted_normative_stack_commit": {"type": "string", "pattern": "^[0-9a-f]{7,40}$"},
        "completed_atlas_bundle_manifest_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_closeout_report_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_intent_atlas_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_coverage_view_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_owner_map_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_rebuild_queue_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "atlas_exclusion_register_checksum": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "bridge_execplan_version": {"const": "v0.5.1"},
        "ledger_schema_version": {"const": "v1"}
      }
    },
    "records": {
      "type": "array",
      "items": {"$ref": "#/$defs/satisfaction_record"}
    },
    "gate2_state": {"$ref": "#/$defs/gate_state"},
    "gate3_state": {"$ref": "#/$defs/gate_state"},
    "gate4_state": {"$ref": "#/$defs/gate_state"},
    "gate5_state": {"$ref": "#/$defs/gate_state"},
    "gate6_state": {"$ref": "#/$defs/gate_state"},
    "gate7_state": {"$ref": "#/$defs/gate_state"},
    "gate8_state": {"$ref": "#/$defs/gate_state"},
    "gate9_state": {"$ref": "#/$defs/gate_state"}
  },
  "$defs": {
    "gate_state": {
      "type": "object",
      "required": ["result"],
      "additionalProperties": true,
      "properties": {
        "result": {"enum": ["pass", "fail", "blocked"]}
      }
    },
    "evidence_pointer": {
      "type": "object",
      "required": ["path", "line_start", "line_end", "evidence_type"],
      "additionalProperties": false,
      "properties": {
        "path": {"type": "string", "minLength": 1},
        "line_start": {"type": "integer", "minimum": 1},
        "line_end": {"type": "integer", "minimum": 1},
        "evidence_type": {"enum": ["atlas", "blueprint", "normative", "vocabulary", "test", "proof_block", "code", "config", "schema", "packet", "docstring", "ledger", "tool_output"]}
      }
    },
    "term_check": {
      "type": "object",
      "required": ["term", "term_kind", "result"],
      "additionalProperties": false,
      "properties": {
        "term": {"type": "string", "minLength": 1},
        "term_kind": {"enum": ["architecture_surface", "owner_name", "class_name", "function_name", "packet_field", "schema_key", "config_key", "ledger_key", "enum_value", "proof_block_id", "test_family_id", "checkpoint_surface", "docstring_concept", "planning_term"]},
        "result": {"enum": ["reused_existing", "already_admitted", "blocked_admission_required", "blocked_synonym_collision", "blocked_disallowed_phrase", "blocked_overloaded_term", "unchecked"]}
      }
    },
    "vocabulary_gate": {
      "type": "object",
      "required": ["status", "terms"],
      "additionalProperties": false,
      "properties": {
        "status": {"enum": ["pending_gate5", "not_required", "passed_reuse_existing", "passed_new_terms_already_admitted", "blocked_admission_required", "blocked_synonym_collision", "blocked_disallowed_phrase", "blocked_overloaded_term", "blocked_unchecked"]},
        "terms": {"type": "array", "items": {"$ref": "#/$defs/term_check"}}
      }
    },
    "proof_resolution": {
      "type": "object",
      "required": ["tier", "test_family_action", "proof_block_action"],
      "additionalProperties": false,
      "properties": {
        "tier": {"enum": ["pending_gate7", "Tier A", "Tier B", "Tier C", "none", "blocked_unresolved"]},
        "test_family_action": {"enum": ["pending_gate7", "reuse_existing", "extend_existing", "admit_new", "none", "blocked_unresolved"]},
        "proof_block_action": {"enum": ["pending_gate7", "reuse_existing", "extend_existing", "admit_new", "none", "blocked_unresolved"]}
      }
    },
    "satisfaction_record": {
      "type": "object",
      "required": [
        "satisfaction_record_id",
        "atlas_record_id",
        "intent_unit_id",
        "donor_provenance",
        "blueprint_surface",
        "blueprint_surface_status",
        "target_owner",
        "target_owner_evidence",
        "vocabulary_gate",
        "native_satisfaction_status",
        "native_evidence",
        "proof_resolution",
        "existing_test_decision",
        "checkpoint_declaration_required",
        "docstring_declaration_required",
        "implementation_leaf_required",
        "implementation_leaf_type",
        "blocked_reason",
        "decision_notes"
      ],
      "additionalProperties": false,
      "properties": {
        "satisfaction_record_id": {"type": "string", "pattern": "^NIS-[0-9]{4}$"},
        "atlas_record_id": {"type": "string", "minLength": 1},
        "intent_unit_id": {"type": "string", "minLength": 1},
        "donor_provenance": {"$ref": "#/$defs/evidence_pointer"},
        "blueprint_surface": {"type": "string", "minLength": 1},
        "blueprint_surface_status": {"enum": ["implemented", "thin_seam", "placeholder", "reserved", "future_only", "legacy_only", "rejected"]},
        "target_owner": {"type": "string", "minLength": 1},
        "target_owner_evidence": {"type": "array", "items": {"$ref": "#/$defs/evidence_pointer"}},
        "vocabulary_gate": {"$ref": "#/$defs/vocabulary_gate"},
        "native_satisfaction_status": {"enum": ["pending_gate6", "already_satisfied", "partially_satisfied", "missing", "transform_required", "excluded", "blocked_blueprint", "blocked_vocabulary", "blocked_atlas_granularity", "blocked_evidence", "blocked_conflict"]},
        "native_evidence": {"type": "array", "items": {"$ref": "#/$defs/evidence_pointer"}},
        "proof_resolution": {"$ref": "#/$defs/proof_resolution"},
        "existing_test_decision": {"enum": ["pending_gate7", "reuse_existing_same_invariant", "extend_existing_same_invariant", "new_test_family_required", "no_test_change_required", "blocked_unresolved"]},
        "checkpoint_declaration_required": {"type": ["boolean", "null"]},
        "docstring_declaration_required": {"type": ["boolean", "null"]},
        "implementation_leaf_required": {"type": ["boolean", "null"]},
        "implementation_leaf_type": {"enum": ["pending_gate7", "none", "later_test_first_leaf", "later_vocabulary_leaf", "later_blueprint_leaf", "blocked"]},
        "blocked_reason": {"type": ["string", "null"]},
        "decision_notes": {"type": "string", "minLength": 1}
      }
    }
  }
}
```

---

## 20. Semantic validation rules

Schema validation is required and insufficient.

The validation report must also prove:

1. every `satisfaction_record_id` is unique
2. every `atlas_record_id` exists in the completed Atlas
3. every `intent_unit_id` exists in the completed Atlas
4. every donor provenance range exists in the Atlas coverage view
5. every blueprint architecture surface exists in `docs/11`
6. every blueprint architecture-surface status matches `docs/11`
7. every target owner is supported by `docs/11`
8. every vocabulary blocker prevents implementation-leaf status
9. every `reserved`, `future_only`, `legacy_only`, or `rejected` architecture surface prevents direct implementation-leaf status
10. every `already_satisfied` record has native code/config/schema evidence and proof evidence unless proof tier is `none`
11. every `partially_satisfied` or `missing` record has a later leaf type or blocker
12. every `excluded` record has exclusion evidence
13. every record with `blocked_` status has a blocked reason
14. no record cites the Vernacular Bridge as native authority
15. no record uses Atlas owner candidate as final owner without `docs/11` evidence

---

## 21. Ordered gates

### Gate 1 — Route and prior-state verification

Verify branch, commit, git status, active route, accepted `docs/11`, accepted vocabulary baseline, and completed Atlas baseline.

Pass condition:

- all required prior-state conditions are true
- provenance register exists and validates
- no dirty git state exists unless the dirty state is the authorised Bridge work

### Gate 2 — Completed Atlas acceptance check

Read the repo-local Atlas evidence bundle in full.

Pass condition:

- imported Atlas evidence artefacts validate against the manifest
- coverage view has no uncovered accepted donor ranges
- record boundaries are granular enough for Bridge adjudication
- exclusions are explicit
- the imported closeout report is consistent with the imported Atlas artefacts

### Gate 3 — Blueprint authority read

Read `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` in full.

Pass condition:

- every architecture surface is understood
- architecture-surface order is sequential
- implementation-truth statuses are recorded
- target-owner mapping rules are clear

### Gate 4 — Atlas intent to blueprint architecture-surface mapping

For each Atlas intent unit, map to a `docs/11` architecture surface or record `blocked_blueprint`.

Pass condition:

- every mapped record cites `docs/11` evidence
- no record maps directly from Atlas owner candidate
- no record maps from vernacular wording
- later-gate fields use only the staged placeholder values defined in this ExecPlan

### Gate 5 — Vocabulary gate

Run vocabulary classification for all durable native language tied to each record.

Pass condition:

- every record has a vocabulary gate result
- vocabulary blockers are recorded
- no vocabulary blocker proceeds to implementation-bound status

### Gate 6 — Native satisfaction audit

Read native code, tests, config, schema, packets, and docstrings required by the target owner.

Pass condition:

- every status has evidence
- name matches alone are rejected
- docstring-only matches are rejected
- runtime behaviour is truth surface when docstrings diverge

### Gate 7 — Proof and checkpoint resolution

Resolve test tier, retained-test action, proof-block action, checkpoint declaration requirement, and docstring declaration requirement.

Pass condition:

- every missing or partial accepted intent has proof posture
- every proof decision cites governing proof surfaces

### Gate 8 — Ledger validation

Validate ledger schema and semantic rules.

Pass condition:

- schema validation passes
- duplicate-ID validation passes
- semantic validation passes
- validation report exists

### Gate 9 — Closeout

Close the ledger-only Bridge run.

Pass condition:

- only authorised surfaces changed
- all records are complete or truthfully blocked
- implementation leaves are not executed
- git diff surface check passes
- working tree is clean after commit

---

## 22. Implementation leaf generation rule

Implementation leaves are created after the first Bridge ledger is accepted.

Each later implementation leaf must reference:

- satisfaction record ID
- Atlas record IDs
- blueprint surface
- blueprint surface status
- target owner
- native baseline commit
- blueprint baseline commit
- vocabulary baseline commit
- normative basis
- vocabulary gate result
- exact missing obligation
- proof tier
- test-family action
- proof-block action
- checkpoint declaration requirement
- docstring declaration requirement
- allowed implementation surfaces
- stop conditions
- closeout proof commands

The Bridge does not execute those leaves.

---

## 23. Stop conditions

Stop if any condition occurs:

1. prior-state condition fails
2. source provenance is unclear
3. completed Atlas is not granular enough
4. `docs/11` is missing
5. `docs/11` is not accepted
6. `docs/11` lacks the required target architecture surface
7. target-owner mapping cannot be supported by `docs/11`
8. vocabulary gate blocks the durable native language
9. native evidence is insufficient for satisfaction classification
10. native authority surfaces conflict
11. proof tier cannot be resolved
12. required evidence file is missing
13. further progress requires runtime implementation
14. further progress requires feature-test modification
15. further progress requires vocabulary admission work
16. further progress requires changing `docs/11`

---

## 24. Completion criteria

The Bridge run is complete only when:

- provenance register exists and validates
- native intent satisfaction ledger exists and validates
- validation report exists
- all baselines are pinned
- completed Atlas input has been accepted as granular or the run is blocked
- every accepted Atlas intent unit has a satisfaction record or a recorded blocker
- every record maps through `docs/11` or records a blueprint blocker
- every record has vocabulary gate status
- every record has proof resolution
- every missing or partial accepted intent has later leaf type or blocker
- no runtime implementation occurred
- no feature-test modification occurred
- no vocabulary admission work occurred
- no direct legacy code migration occurred
- no Vernacular Bridge authority citation exists
- only authorised surfaces changed
- git status is clean after commit

---

## 25. Canonical Bridge sentence

Recover legacy intent as evidence; adjudicate it against the accepted native architecture blueprint and governed vocabulary; credit already satisfied native behaviour; classify missing lawful obligations for later bounded, vocabulary-lawful, test-first implementation leaves.
