# NVDA10 Atlas-to-active-codebase migration methodology — standalone cold-start handoff

## 0. Purpose

This document tells a future thread how to continue the Atlas migration without inheriting the earlier terminology confusion.

The task is to move Atlas ideas into the **active codebase**, one service at a time, using the project hierarchy:

```text
normative documents
→ Tier A/B/C tests
→ active-codebase source/YAML/config/schema/fixture implementation
→ proof receipts and ledger/report update
```

This document is deliberately written so a future thread can start from the source tarball and know where to look first.

---

## 1. Locked terminology

Use these terms only.

| Term | Meaning |
|---|---|
| **active codebase** | The current runnable codebase. It contains the **18 services**. |
| **18 services** | The service surfaces inside the active codebase. |
| **Atlas** | The original donor idea corpus containing **1,716 Atlas ideas**. |
| **Atlas idea** | One donor idea from Atlas. It must be handled as a row-level item. |
| **Atlas Bridge** | The mapping layer that assigns each Atlas idea to one of the active codebase’s 18 services. |
| **included in active-codebase source behaviour** | The behaviour exists in source/YAML/config/schema/fixture/runtime artefacts with evidence. |
| **not yet migrated** | The Atlas idea is mapped to one of the 18 services, but source behaviour has not yet been included in the active codebase by the evidence rule. |
| **receipt** | A project artefact that may record work or proof. A receipt is not source-code implementation by itself. |
| **proof** | Command output, diff, file/line evidence, test result, or another concrete artefact showing what happened. |

Do **not** use these old labels as status terms:

```text
open
closed
reopened
non-310
non-audit
non310
row closure
```

Those labels caused the confusion. They may appear in old artefact filenames or historical notes, but they are not migration-status language.

---

## 2. Current clean state

The current clean understanding is:

| Item | Count |
|---|---:|
| Atlas ideas total | 1,716 |
| Atlas ideas mapped by the Atlas Bridge to the active codebase’s 18 services | 1,716 |
| Atlas ideas already included in existing active-codebase source behaviour | 508 |
| Atlas ideas added or modified in active-codebase source behaviour | 80 |
| Atlas ideas with tests but missing/incomplete source behaviour | 0 |
| Atlas ideas not yet migrated into active-codebase source behaviour | 1,128 |
| Atlas ideas not traceable | 0 |

Clean operating sentence:

> The active codebase has 18 services. Atlas has 1,716 ideas. The Atlas Bridge maps all 1,716 Atlas ideas to those 18 services. The current forensic classification records 588 Atlas ideas as included in active-codebase source behaviour and 1,128 Atlas ideas as not yet migrated. The next phase is to migrate the remaining 1,128 Atlas ideas one service at a time.

Important limitation:

> Do not say all 1,716 Atlas ideas are implemented as source code. They are not. The correct current statement is that 1,128 Atlas ideas remain to be migrated into active-codebase source behaviour.

---

## 3. Expected cold-start input

The source tarball expected for this handoff is:

```text
fwd014-final-non310-clean-handoff.tar.gz
```

Expected repo root after extraction:

```text
MVD-A10_1704_V1/
```

Expected inspected git state from the previous forensic pass:

```text
branch: work/fwd014-final-non310-sweep
HEAD:   1f417b39ddd75312f92670d7f0927813a5dffe8c
git status --short: clean
```

A future thread must re-check these. If the tarball differs, stop and report the mismatch before continuing.

---

## 4. First inspection sequence for a future thread

Do this before any migration work.

### 4.1 Unpack and identify the repo

```bash
tar -xzf fwd014-final-non310-clean-handoff.tar.gz
cd MVD-A10_1704_V1
pwd
git branch --show-current
git rev-parse HEAD
git status --short
```

Pass condition:

- repo root is `MVD-A10_1704_V1/`;
- branch and HEAD match the expected values, or the mismatch is reported;
- working tree state is known.

Stop condition:

- tarball cannot be unpacked;
- repo root is missing;
- `.git` is missing;
- working tree is dirty before work starts;
- branch/HEAD mismatch is not understood.

### 4.2 Read the live authority files in full

Read these files in full before deciding what to do:

```text
AGENTS.md
PLANS.md
ROADMAP_LEDGER.md
```

Then read the route-specific authority files that apply to the selected migration surface. Likely candidates include:

```text
intent_migration/AGENTS.override.md
intent_migration/native_intent_implementation/AGENTS.override.md
intent_migration/native_intent_satisfaction/AGENTS.override.md
intent_migration/testing_governance_reconciliation/AGENTS.override.md
intent_migration/active_codebase_alignment_repair/AGENTS.override.md
tests/AGENTS.override.md
```

Do not rely on snippets. These authority files must be read in full.

### 4.3 Read the core normative documents in full

Minimum normative read set:

```text
docs/00_CONTROL_SURFACE_ROUTING_INDEX.md
docs/01_NORMATIVE_CORE.md
docs/01.1_NORMATIVE_WORKING.md
docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md
docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md
docs/03_DOMAIN_MODEL_CORE.md
docs/03.1_DOMAIN_MODEL_WORKING.md
docs/04_TECHNICAL_ARCHITECTURE_CORE.md
docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md
docs/05_GUARDRAILS_CORE.md
docs/05.1_GUARDRAILS_WORKING.md
docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md
docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md
docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md
docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md
docs/08_TESTING_AND_PROMOTION_CORE.md
docs/08.1_TESTING_AND_PROMOTION_WORKING.md
docs/09_DMPV3_PROTOCOL_CORE.md
docs/09.1_DMPV3_PROTOCOL_WORKING.md
docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md
docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md
docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md
```

Also read vocabulary workflow material before admitting new names, aliases, signal labels, statuses, or schema terms:

```text
docs/vocabulary/CONSOLIDATION_WORKFLOW.md
docs/vocabulary/vocabulary_registry.md
data/vocabulary/canonical_vocabulary.json
```

Pass condition:

- a read manifest records every authority and normative file read;
- any missing file is recorded explicitly;
- no implementation decision is made before this read is complete.

Stop condition:

- authority forbids the intended service migration;
- a controlling normative document is missing;
- the service boundary is unclear.

---

## 5. Where to look for Atlas, Bridge, and prior process evidence

A future thread should inspect these paths before building the new queue.

### 5.1 Atlas and Bridge mapping evidence

```text
var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json
var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json
var/audit/atlas_surface_slices/atlas_surface_slice.schema.json
var/audit/atlas_surface_slices/
```

These are the main places to confirm:

- 1,716 Atlas ideas;
- 18 service slices;
- mapping of each Atlas idea to one of the active codebase’s 18 services.

### 5.2 Active-codebase inventory evidence

```text
var/audit/active_code_atlas_001/active_code_atlas.json
var/audit/active_code_atlas_001/primary_active_code_atlas.json
var/audit/active_code_atlas_001/active_code_atlas_surface_inventory.json
var/audit/active_code_atlas_001/active_code_atlas_surface_metadata.json
var/audit/active_code_atlas_001/active_code_atlas_validation_report.json
```

These files help show what the active codebase already contained at the time of that inventory.

### 5.3 Old Atlas-to-active-codebase migration process evidence

```text
var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_SUMMARY.md
var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_TEST_FIRST_QUEUE.md
var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md
var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json
var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_queue.json
var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_execution_queue.json
var/audit/active_code_atlas_bridge_comparison_001/receipts/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_RECEIPT.md
```

These files are method evidence. They show the older intended pattern:

```text
Atlas idea
→ Bridge-mapped service
→ compare against active-codebase evidence
→ write test-first queue
→ tests before source changes
→ source/YAML/config implementation
→ proof and receipt
```

Do not reuse the old queue as the current worklist without rechecking it against the current 1,128 not-yet-migrated Atlas ideas.

### 5.4 Final package and confusing historical audit evidence

These paths explain why old status words must not be reused:

```text
var/audit/fwd014_final_non310_sweep_20260519/FINAL_CLOSEOUT.md
var/audit/fwd014_final_non310_sweep_20260519/FINAL_PACKAGE_CLEAN_HANDOFF.md
var/audit/fwd014_final_non310_sweep_20260519/NON310_FINAL_SURFACE_SWEEP.csv
var/audit/fwd014_final_non310_sweep_20260519/FWD014_EXISTING_SATISFACTION_LEDGER.csv
ROADMAP_LEDGER.md
```

These are useful as history and audit evidence. They are not enough to prove all Atlas ideas have source-code implementation.

---

## 6. Service migration queue starter

The current migration queue must be built from the Atlas ideas classified as **not yet migrated**.

Per-service starting counts:

| # | Service | Already included in existing active-codebase source behaviour | Added/modified in active-codebase source behaviour | Not yet migrated | Total Atlas ideas mapped to service |
|---:|---|---:|---:|---:|---:|
| 1 | DMPV3 packet carriage | 68 | 5 | 0 | 73 |
| 2 | Downstream capital deployment authority | 2 | 0 | 0 | 2 |
| 3 | Dynamic coefficient and modifier authority | 0 | 0 | 193 | 193 |
| 4 | Exit and close architecture | 0 | 0 | 90 | 90 |
| 5 | External source interfaces and API ingress | 8 | 0 | 226 | 234 |
| 6 | Financial and event calendar architecture | 2 | 0 | 115 | 117 |
| 7 | Live position and inventory architecture | 2 | 17 | 19 | 38 |
| 8 | Opening architecture and placement readiness | 0 | 23 | 51 | 74 |
| 9 | Parallel risk lane | 0 | 0 | 57 | 57 |
| 10 | Persistence, ledgers, and receipts | 23 | 15 | 59 | 97 |
| 11 | Playbook library architecture | 75 | 20 | 0 | 95 |
| 12 | Prepared ingress and runtime context preparation | 51 | 0 | 0 | 51 |
| 13 | Raw capture and source temporal law | 108 | 0 | 0 | 108 |
| 14 | Raw signal families | 0 | 0 | 123 | 123 |
| 15 | Review and explanation layer | 1 | 0 | 142 | 143 |
| 16 | Serial desk-cognition spine | 139 | 0 | 0 | 139 |
| 17 | Testing, proof, and checkpoint surfaces | 19 | 0 | 53 | 72 |
| 18 | Vocabulary governance interface | 10 | 0 | 0 | 10 |

Services with `0` not-yet-migrated items do not need feature migration work unless a new forensic pass changes the classification.

The services with remaining migration work are:

```text
Dynamic coefficient and modifier authority — 193
Exit and close architecture — 90
External source interfaces and API ingress — 226
Financial and event calendar architecture — 115
Live position and inventory architecture — 19
Opening architecture and placement readiness — 51
Parallel risk lane — 57
Persistence, ledgers, and receipts — 59
Raw signal families — 123
Review and explanation layer — 142
Testing, proof, and checkpoint surfaces — 53
```

The count across these services is 1,128.

---

## 7. Canonical per-Atlas record

Every Atlas idea must be tracked with these fields.

```json
{
  "atlas_id": "stable Atlas identifier",
  "atlas_idea_text": "original Atlas idea text or stable excerpt",
  "mapped_service": "one of the active codebase's 18 services",
  "bridge_mapping_status": "mapped_to_one_of_18_services | mapping_conflict | mapping_missing",
  "source_code_status": "existing_behaviour_found | implementation_added_or_modified | missing_or_incomplete | not_yet_checked",
  "test_status": "tier_tests_present | tier_tests_added | tier_tests_need_update | no_tests_yet | not_yet_checked",
  "classification": "already_included | migrated_this_pass | not_yet_migrated | blocked_by_authority_or_conflict",
  "evidence": [
    {
      "type": "normative | test | source | yaml | config | schema | fixture | receipt | command_output | diff",
      "path": "repo-relative path",
      "line_range": "start-end where applicable",
      "summary": "plain-English evidence note"
    }
  ],
  "notes": "plain-English caveats, especially where prior receipts could be misleading"
}
```

The record may also add these workflow fields during service execution:

```text
normative_status
vocabulary_status
intended_test_tier
proof_commands
stop_conditions
changed_files
```

But the core report fields above must not be removed or renamed.

---

## 8. Classification rules

Every Atlas idea must end a service pass in exactly one classification.

| Classification | Meaning |
|---|---|
| `already_included` | The Atlas idea was already present in active-codebase source behaviour before this pass. |
| `migrated_this_pass` | Tests and implementation were added or amended in this pass. |
| `not_yet_migrated` | The idea remains mapped to the service but active-codebase source behaviour has not been added. |
| `blocked_by_authority_or_conflict` | The idea cannot proceed because authority, vocabulary, mapping, or service-boundary evidence blocks it. |

For headline reporting:

```text
included in active-codebase source behaviour = already_included + migrated_this_pass
not yet migrated = not_yet_migrated + blocked_by_authority_or_conflict
```

Do not report receipt status as implementation status.

---

## 9. Canonical service-by-service workflow

### Step 0 — Select exactly one service

Select one of the active codebase’s 18 services.

Pass condition:

- one service is named;
- the Atlas IDs mapped to that service are loaded;
- the service has a known not-yet-migrated count.

Stop condition:

- the selected service cannot be matched to the Atlas Bridge mapping;
- multiple services would need to be changed at once.

### Step 1 — Authority and normative full read

Read in full:

- `AGENTS.md`;
- relevant `AGENTS.override.md` files;
- `PLANS.md`;
- `ROADMAP_LEDGER.md`;
- all relevant normative documents;
- vocabulary governance material;
- `tests/AGENTS.override.md`;
- proof-block and retained-test registry material if tests are touched.

Pass condition:

- full-read manifest exists;
- authority allows the selected service pass.

Stop condition:

- authority forbids the work;
- the route is unclear;
- a controlling document is missing.

### Step 2 — Build the service evidence inventory

For every Atlas idea mapped to the selected service, record:

- Atlas ID;
- Atlas idea text;
- Atlas Bridge service mapping;
- existing normative evidence;
- existing tests;
- existing source/YAML/config/schema/fixture evidence;
- old receipts that may be relevant;
- vocabulary impacts.

Pass condition:

- every selected Atlas idea has an inventory row.

Stop condition:

- an Atlas idea cannot be traced to original Atlas text and Bridge mapping.

### Step 3 — Check service mapping semantics

The Atlas Bridge says where each idea was mapped. This step checks whether that mapping makes sense before implementation.

For each Atlas idea:

1. read the idea text;
2. read the mapped service definition;
3. confirm the idea belongs in that service;
4. record `bridge_mapping_status`.

Pass condition:

- each idea is accepted as mapped to the selected service or marked as a mapping conflict.

Stop condition:

- the idea belongs to another service and would force cross-service work.

### Step 4 — Reconcile against normative documents

For each Atlas idea, compare intended behaviour to the governing documents.

Record one of:

```text
present_in_normative_docs
normative_update_required
conflict_with_normative_docs
not_yet_checked
```

If normative documents need updating, do that before tests or source changes, but only if authority allows it.

Pass condition:

- every Atlas idea has normative status and evidence.

Stop condition:

- the idea conflicts with the governing documents;
- required normative changes are outside authority.

### Step 5 — Apply vocabulary governance

Before tests or implementation, check whether the idea introduces or relies on:

- governed terms;
- synonyms;
- signal names;
- status words;
- schema labels;
- service names;
- aliases.

Pass condition:

- vocabulary impact is recorded for every Atlas idea.

Stop condition:

- a new or conflicting term requires admission outside the current service authority.

### Step 6 — Write the test-first plan

Before changing source/YAML/config, write the test plan.

The plan must identify:

- Atlas IDs covered;
- normative clauses covered;
- intended Tier A tests;
- intended Tier B tests;
- intended Tier C tests;
- false-positive resistance checks;
- expected source/YAML/config/schema/fixture changes;
- proof commands.

Pass condition:

- every selected Atlas idea is assigned to a test obligation or proven already included.

Stop condition:

- the idea cannot be expressed as testable behaviour.

### Step 7 — Write or amend tests first

Tests must be written or amended before implementation changes.

Rules:

- If a test passes before implementation changes, the idea may already be included; prove it with source/YAML/config/schema/fixture evidence.
- If a test fails before implementation changes, keep the failure as red-first proof of the missing behaviour.
- If a test passes trivially, it is not evidence. Add false-positive resistance.

Pass condition:

- meaningful Tier A/B/C tests exist for every idea being migrated.

Stop condition:

- tests cannot be written without violating authority, service boundary, or vocabulary rules.

### Step 8 — Implement only after tests define the behaviour

After tests define the expected behaviour, amend only the required files for the selected service.

Allowed targets when in scope:

```text
Python source
YAML
configuration
schemas
fixtures
registry files
proof-block files
retained-test registry entries
service-specific documentation required by the hierarchy
```

Do not mutate:

```text
original Atlas JSON
original Atlas Bridge JSON
generated Atlas slices
unrelated services
broker/live trading paths
dependency files
VENV files
unrelated vocabulary data
frozen normative documents unless authority explicitly allows it
```

Pass condition:

- implementation is bounded to the selected service;
- every change traces to Atlas ID, normative rule, and test.

Stop condition:

- implementation requires touching another service or forbidden artefact.

### Step 9 — Run targeted proof

Run the smallest meaningful proof first.

Proof must show:

- relevant tests fail before implementation if behaviour was missing;
- relevant tests pass after implementation;
- false-positive resistance is active;
- the proof actually exercises the migrated behaviour.

Pass condition:

- targeted proof passes and output is captured.

Stop condition:

- targeted proof fails;
- proof does not exercise the migrated behaviour.

### Step 10 — Run broader retained proof

Run the broader proof required by authority and testing governance.

Likely checks:

```text
Tier A pack
Tier B pack
Tier C pack
retained-test registry validator
proof-block validator
vocabulary checks
schema checks
JSON/YAML parse checks
formatting/linting if required
```

Pass condition:

- required broader proof passes and output is captured.

Stop condition:

- broader proof fails;
- environment cannot run the required checks.

### Step 11 — Update per-Atlas evidence records

For each Atlas idea handled in the service pass, update:

- classification;
- normative evidence;
- test evidence;
- source/YAML/config/schema/fixture evidence;
- proof output;
- changed files;
- remaining gaps;
- caveats about old receipt confusion.

Pass condition:

- every selected Atlas idea has an updated record.

Stop condition:

- changed behaviour cannot be traced back to Atlas ID, normative clause, test, and implementation evidence.

### Step 12 — Produce service closeout package

Each service pass must produce a closeout package containing:

1. service name;
2. Atlas IDs attempted;
3. Atlas IDs already included;
4. Atlas IDs migrated in this pass;
5. Atlas IDs blocked;
6. Atlas IDs remaining;
7. files changed;
8. tests changed;
9. source/YAML/config/schema/fixture files changed;
10. proof commands and outputs;
11. retained-test registry/proof-block changes, if any;
12. final per-Atlas migration records;
13. updated queue for the next pass.

Pass condition:

- counts reconcile to the service’s selected Atlas ID set;
- no status depends on receipt wording alone.

Stop condition:

- counts do not reconcile;
- evidence is missing for a claimed migration.

---

## 10. Required output files for the new queue

A future thread should create these files before starting implementation:

```text
NVDA10_ATLAS_MIGRATION_QUEUE.md
NVDA10_ATLAS_MIGRATION_QUEUE.json
NVDA10_ATLAS_MIGRATION_QUEUE_BY_SERVICE.csv
NVDA10_ATLAS_MIGRATION_SERVICE_CLOSEOUT_TEMPLATE.md
```

The queue must preserve one row per Atlas idea.

Required queue fields:

```text
queue_id
atlas_id
atlas_idea_text
mapped_service
bridge_mapping_status
source_code_status
test_status
classification
normative_status
vocabulary_status
intended_test_tier
required_files_to_read
expected_files_to_change
proof_commands
stop_conditions
evidence
notes
```

---

## 11. Definition of done for the overall remaining migration

The remaining migration is done only when:

1. all 1,128 currently not-yet-migrated Atlas ideas have been processed through service passes;
2. every Atlas idea has one final classification;
3. every `migrated_this_pass` idea has normative, test, implementation, and proof evidence;
4. every `already_included` idea has source/YAML/config/schema/fixture evidence and test evidence, or a documented reason why existing proof is sufficient;
5. every blocked idea has a concrete blocker and next required authority action;
6. final counts reconcile back to 1,716 Atlas ideas;
7. no claim relies on receipt wording alone.

---

## 12. First recommended executable worker brief

Use this as the opening brief for the next worker thread.

```text
Task: build the new service-by-service Atlas migration queue from the source tarball.

Input source of truth:
fwd014-final-non310-clean-handoff.tar.gz

Use only locked terminology:
active codebase, 18 services, Atlas, Atlas idea, Atlas Bridge, included in active-codebase source behaviour, not yet migrated.

Do not use old status labels such as open, closed, reopened, non-310, non-audit, or row closure.

Work in gates.

Gate 1 — Cold-start authority
Unpack the tarball, verify repo root, branch, HEAD, and clean status.
Read AGENTS.md, PLANS.md, ROADMAP_LEDGER.md, route-specific AGENTS.override.md files, tests/AGENTS.override.md, and all in-scope normative documents in full.
Pass only if the read set is recorded.

Gate 2 — Rebuild Atlas/Bridge inventory
Identify the 1,716 Atlas ideas and their Atlas Bridge mapping to the active codebase’s 18 services.
Pass only if counts reconcile to 1,716 total and 18 mapped services.

Gate 3 — Rebuild migration classification
For every Atlas idea, classify source-code inclusion using the agreed fields:
atlas_id, atlas_idea_text, mapped_service, bridge_mapping_status, source_code_status, test_status, classification, evidence, notes.
Pass only if there is one row per Atlas idea and classifications reconcile to 1,716.

Gate 4 — Create the not-yet-migrated service queue
Extract the Atlas ideas not yet migrated into active-codebase source behaviour.
Group by mapped service.
Pass only if the queue count reconciles to the not-yet-migrated total.

Gate 5 — Prepare the first service migration brief
Open exactly one service.
Do not implement yet.
Create the service-specific brief using the hierarchy:
normative documents → Tier A/B/C tests → source/YAML/config/schema/fixture implementation → proof receipts and queue update.

Stop if any authority, mapping, vocabulary, or count conflict appears.
```

---

## 13. What this document is and is not

This document is:

- a cold-start methodology;
- a terminology lock;
- a pointer map for where a future thread should inspect;
- a service-by-service migration process.

This document is not:

- proof that any specific Atlas idea is implemented;
- a substitute for reading the tarball;
- permission to skip authority files;
- permission to implement multiple services at once;
- permission to treat old receipts as source-code evidence.

The future thread must read the repo evidence directly and produce proof before making implementation claims.
