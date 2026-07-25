# PM-010 Reopened P1 Integration and Deterministic Projection Receipt

`unit_result: pass`

This is a worker validation result only. **Project-manager acceptance remains pending; P1 acceptance is not claimed. P2 was not begun.**

## Control

- Branch: `work/NVIDIA_2026_pm001_pm010_restart_20260721`
- HEAD: `21c1e5eccfbb818bdd422afd42117f23b1f74f26`
- Commit created: none.
- P2/P3/P4/Gate D work: none.
- Tests, current contracts and implementation remained read-only observation/diagnostic evidence.

## Reopened semantic decisions

### PM-007 serial cognition

- The exact PM-007 fixed label `Serial Desk-cognition` is explicitly represented by `SSC-010`.
- `SSC-010` is a lawful alias-only decision targeting canonical `SSC-015 Serial Desk-cognition Spine`.
- The human registry contains one canonical Spine record, carries `Serial Desk-cognition` as a lawful alias, and cites both semantic decisions.
- The fixed label was not silently replaced by the later canonical Spine label.

### PM-008 downstream state reader

- `OPC-010 Downstream State-reader Layer` is admitted from `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195`.
- The exact `state-read` occurrence at line 195 is owned by PM-008 and preserved as contextual-only occurrence evidence.
- PM-009 has no ownership of this occurrence.

### PM-009 Stage-read State

- `PRP-004 Stage-read State` is quarantined.
- The cited Parallel Risk input-trace and replay-envelope propositions do not establish a distinct per-stage read-status record.
- Current contracts, implementation and tests remain observation evidence and do not admit the concept.
- Deleted Stage-read registry occurrences are removed from the PM-009 occurrence register.

## Rebuilt integrated result

- P1 semantic decisions: **129**
- Canonical human records/generated entries: **117**
- Alias-only decisions: **3**
- Quarantined decisions: **9**
- Projected semantic-decision references: **120**, each represented exactly once
- Exact candidate-occurrence dispositions: **499**
- Candidate paths: **130**
- Normalised candidate phrases: **88**
- Governing-normative candidate occurrences in the integrated audit register: **59**, all resolved inside P1
- Additional preserved PM-008 downstream `state-read` normative occurrence: **1**
- Non-governing observation occurrences: **440**
- Unresolved audit candidates: **0**

Counts were rebuilt from the corrected decisions and were not held to earlier arithmetic.

## Exact fixed-label coverage

`FINAL_ACCEPTANCE_VALIDATOR.py` parses the fixed-list paragraphs directly from each PM-003–PM-009 brief and requires every exact fixed label to occur exactly once in its owning adjudication register:

- PM-003: 32
- PM-004: 10
- PM-005: 30
- PM-006: 21
- PM-007: 13
- PM-008: 9
- PM-009: 10

The validator therefore fails if a fixed label is silently renamed or replaced even when total row counts remain unchanged.

## Occurrence-scoped audit behaviour

`src/nvda_desk/vocabulary_synonym_audit.py` recognises only canonical labels and lawful aliases as phrase-global exact tokens. A disposition suppresses only the exact path, line, column, normalised phrase and unchanged source-context SHA-256 occurrence.

`OCCURRENCE_LEVEL_AUDIT_PROBE.py` introduces a previously dispositioned phrase with identical context at a new path and records:

- `occurrence_level_audit_probe=PASS`
- `new_occurrence_reported=true`

## Locator and revision integrity

`VALIDATE_SOURCE_LOCATORS.py` records:

- `source_locator_validation=PASS`
- adjudication locators: **297**
- occurrence locators: **559**
- preserved source-revision evidence rows: **2**

No locator extends beyond the declared source revision.

## Deterministic projection and audit

- Human registry version: `2026-07-21-p1-corrected-v4`
- Generated entries: **117**
- Generated JSON SHA-256: `00ec2ebcc4660ba82bd3c526958599fcff53252bc6eee21d1cd4b2d6492d0d6e`
- Final audit fingerprint: `29de4fb5c7a1be0d95e62778f1f071a4ccf12a4cb369c2ad398d403d81962ad5`
- Fresh builder payloads are byte-identical to the tracked JSON.
- The tracked audit report is reproducible, has zero candidates, records 499 resolved occurrences and has `vocabulary_touched=false`.
- The touch stamp equals the final audit fingerprint.

## Validation

- Reopened semantic/projection validator: **PASS**
- Exact fixed-label coverage: **PASS**
- Source-locator validator: **PASS**
- New-occurrence audit probe: **PASS**
- Generated JSON determinism/parity: **PASS**
- Audit/stamp parity: **PASS**
- `git diff --check`: **PASS**

## Read-only diagnostic tests

Command:

`UV_CACHE_DIR=/tmp/uv-cache UV_PROJECT_ENVIRONMENT=/tmp/nvda-2026-venv UV_PYTHON_INSTALL_DIR=/tmp/uv-python uv run --python 3.13.5 --frozen pytest tests/tier_a/vocabulary -q`

Result: **83 passed, 18 failed in 17.24s**.

The failures are retained diagnostic evidence. Four assert unsupported or superseded expectations: canonical Candidate Audit/Stage-read State, Mutable Runtime Surface, audit categories dependent on rejected records, or a separate `Serial Desk-cognition` human heading rather than its lawful alias relationship. Fourteen audit tests use the former tuple fixture protocol; one also expects phrase-global disallowed-phrase suppression. No test was edited or suppressed.

## Bounded changed surfaces

Tracked changes remain confined to vocabulary doctrine/registry/projection artefacts and the two vocabulary implementation surfaces authorised by the governing restart handoff. Untracked evidence remains under `project_control/canonical_project_manager/units/`.

No test, configuration, root control, roadmap, ExecPlan, production/trading, P2, P3, P4 or Gate D surface changed.
