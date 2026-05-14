# NVDA rebuild — supplemental continuation brief
**Date:** 2026-04-19  
**Purpose:** continue the same line of work from `nvda_major_work_brief_next_queue_v2_2026-04-19.md`, carrying forward only the parts that are still incomplete or no longer truthful after direct repo verification.  
**State basis verified in repo:** branch `work/post-wave1-contract-truth-pass-20260419`, commit `3540521e3c0e35c2270e01daf77b91f97ea2ffa9`.

---

## 1. Direct answer

The earlier brief is **not fully completed**.

### Verified complete enough to close from the earlier brief
The repo now has:
- workbook-owned module-path coverage at `0 missing` in the current completeness checkpoint: `migration_prebuild/11_completeness_matrix_all_workbook_paths_present_2026-04-19.md:1-14`
- a green native blocker shell: `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `74 passed` (verified directly in this review session)
- successful source compilation over `src`, `tests/tier_a`, and `tests/tier_b` (verified directly in this review session)
- bounded native implementations for the packet/reference/preparation/ingress/runtime/repository/service waves that the earlier brief queued, for example:
  - packet envelope contracts at `src/nvda_desk/contracts/packets.py:11-20`
  - packet builders at `src/nvda_desk/packets/dmp_packets.py:11-74`
  - calendar import at `src/nvda_desk/reference/calendar_import.py:24-53,67-97`
  - calendar projection at `src/nvda_desk/reference/calendar_projection.py:55-166`
  - runtime preparation at `src/nvda_desk/preparation/runtime_preparer.py:9-24`
  - ingress translation at `src/nvda_desk/cognition/ingress/translator.py:12-25`
  - bounded runtime orchestration at `src/nvda_desk/runtime/orchestrator.py:8-35`
  - bounded review explanation at `src/nvda_desk/services/review_explanation_service.py:8-27`

### Verified incomplete and therefore carried forward
The earlier brief’s integrity/authority closure work is **not closed**:
1. There is **no durable workbook-to-native-test crosswalk artefact** in the repo. A repo-wide search for the workbook test-family labels returned no matches during this review.
2. `config/proof_blocks.yaml` is still an empty scaffold: `config/proof_blocks.yaml:1-5`.
3. `scripts/run_proof_block.py` still prints scaffold-only output instead of resolving admitted proof blocks: `scripts/run_proof_block.py:1-23`.
4. The retained-test registry is **not fully truthful against the active native test tree**:
   - active native test file missing from registry admission: `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py:1-24`
   - stale merged-path references still recorded against non-existent Tier A files:
     - `config/retained_test_registry.yaml:1535-1573`
     - `config/retained_test_registry.yaml:1612-1633`
     - `config/retained_test_registry.yaml:1699-1720`
5. Control-surface README text is stale relative to the actual repo state:
   - `src/README.md:1-5`
   - `tests/README.md:1-9`
   - `tests/tier_a/README.md:1-9`
   - `tests/tier_b/README.md:1-5`
   - `config/README.md:1-18`

So the correct continuation is **not another broad implementation wave first**. The next lawful work is to close authority truth, registry truth, proof truth, and control-surface truth around what already landed.

---

## 2. Verified completion state from the earlier brief

### 2.1 Workbook path completion wave landed
The repo now records complete workbook path presence at:
- `migration_prebuild/11_completeness_matrix_all_workbook_paths_present_2026-04-19.md:1-14`
- `var/reports/workbook_completeness_matrix_2026-04-19.csv:1-65`

That matrix records all `MA-001` through `MA-064` as present with `missing: 0` and `native_shell_only: 0` in the current checkpoint artefact.

### 2.2 Reference / packet / review surfaces landed
The earlier brief’s code-side queue around packet carriage, reference import/projection, and review helpers has direct file evidence:
- `src/nvda_desk/contracts/packets.py:11-20`
- `src/nvda_desk/packets/dmp_packets.py:11-74`
- `src/nvda_desk/reference/calendar_import.py:24-53,67-97`
- `src/nvda_desk/reference/calendar_projection.py:55-166`
- `src/nvda_desk/downstream/review_stage.py` is present in the tree and the review explanation helper is implemented at `src/nvda_desk/services/review_explanation_service.py:8-27`
- bounded trace review helper is implemented at `src/nvda_desk/testing/bounded_trace_review.py:10-22`

### 2.3 Preparation / ingress / orchestration / repository waves landed at bounded level
The queued bounded surfaces are present and importable:
- preparation: `src/nvda_desk/preparation/runtime_preparer.py:9-24`
- ingress mappers:  
  - `src/nvda_desk/cognition/ingress/temporal_mapper.py:11-28`  
  - `src/nvda_desk/cognition/ingress/regime_mapper.py:10-16`  
  - `src/nvda_desk/cognition/ingress/options_mapper.py:10-16`  
  - `src/nvda_desk/cognition/ingress/translator.py:12-25`
- runtime orchestrator: `src/nvda_desk/runtime/orchestrator.py:8-35`
- bounded repositories: for example `src/nvda_desk/repositories/reference_repository.py:18-39`
- minimal HTTP shell: `src/nvda_desk/api/http/app.py:10-20`

### 2.4 Native shell verification passed
Verified directly in this review session:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `74 passed`
- `python -m compileall src tests/tier_a tests/tier_b` completed without compile failure

---

## 3. Verified incomplete work that must migrate forward

### 3.1 Workbook-to-test authority closure is missing as a durable artefact
The earlier brief explicitly required:
- workbook-to-native-test crosswalk
- benchmark family matrix
- crosswalk vs registry reconciliation
- crosswalk vs actual native files reconciliation

I found **no durable artefact** in the repo that maps the workbook `Test_Architecture` benchmark families to native Tier A / Tier B families. The present durable artefact is a **module completeness** matrix only: `var/reports/workbook_completeness_matrix_2026-04-19.csv:1-65`.

That means the module-path completion wave landed, but the **benchmark-family-to-test-authority** closure did not land as a durable repo surface.

### 3.2 Proof-block closure is still scaffold-only
The earlier brief required proof-block alignment and a durable registry-integrity proof. That is not yet true:
- `config/proof_blocks.yaml:1-5` declares `proof_blocks: []`
- `scripts/run_proof_block.py:1-23` states there are no admitted proof blocks in this scaffold pass
- `Makefile:14-17` only wires the scaffold runner

So the manifest-scoped proof pattern exists only as a shell, not as an admitted integrity gate.

### 3.3 Retained-test registry truth is not fully closed
The earlier brief required every active Tier A/Tier B file to be admitted in the registry and mapped cleanly.

That is not fully true.

#### Active native test missing from authority file
This active Tier A test exists but is not admitted anywhere in `config/retained_test_registry.yaml`:
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py:1-24`

#### Stale merged-path references remain in the registry
The registry still points at non-existent Tier A file paths for merged shadow families instead of naming the actual host family path truthfully:
- `config/retained_test_registry.yaml:1535-1573`
- `config/retained_test_registry.yaml:1612-1633`
- `config/retained_test_registry.yaml:1699-1720`

This does not break the current green shell, but it means the registry is still partly a migration narrative rather than a fully truthful native authority surface.

### 3.4 Control-surface text drift remains
These files still describe the repo as if the native tests and runtime surfaces have not been admitted:
- `src/README.md:1-5`
- `tests/README.md:1-9`
- `tests/tier_a/README.md:1-9`
- `tests/tier_b/README.md:1-5`
- `config/README.md:1-18`

That is no longer truthful after the current native test tree and bounded code waves.

---

## 4. Correct ordered continuation queue

### Phase A — close authority truth before any wider implementation wave

#### 1. Create the missing workbook-to-native-test crosswalk artefact
Create one durable repo artefact that maps each workbook `Test_Architecture` benchmark family to exactly one of:
- active Tier A family/families
- active Tier B family/families
- lawful defer
- missing

Use workbook evidence from:
- `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx` → `Test_Architecture!A2:H20`

Do not use the module completeness matrix as a substitute for this test-authority crosswalk.

#### 2. Create the benchmark family matrix as a durable repo surface
For each workbook benchmark family, record:
- workbook family name
- required test family class
- native family id(s)
- native file path(s)
- status: covered / deferred / missing
- predecessor/successor note where applicable

This matrix must be durable and reviewable in-repo, not only an execution-thread claim.

#### 3. Repair retained-test registry truth against the active native tree
Update `config/retained_test_registry.yaml` so that:
- every active `tests/tier_a/**/test_*.py` and `tests/tier_b/**/test_*.py` file is admitted explicitly
- `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` is either lawfully admitted or explicitly removed from the active tree
- merged/shadow dispositions stop pointing at non-existent native Tier A files and instead record the actual host-family file truthfully

#### 4. Add the missing registry-integrity blocker
Author one native proof surface that fails when:
- an active Tier A/Tier B file is not admitted in `config/retained_test_registry.yaml`
- a registry path points at a non-existent native file when the entry claims native file ownership
- a workbook benchmark family has no mapped native family or lawful defer in the new crosswalk artefact

This is the missing durable integrity gate from the earlier brief.

#### 5. Promote the proof-block surface from scaffold to admitted integrity proof
Replace scaffold-only proof state with one admitted block in:
- `config/proof_blocks.yaml`
- `scripts/run_proof_block.py`
- `Makefile`

The first admitted block should execute the registry/crosswalk integrity gate only. Do not widen the proof model yet.

#### 6. Repair stale control-surface README text
Make these files truthful to current repo state:
- `src/README.md`
- `tests/README.md`
- `tests/tier_a/README.md`
- `tests/tier_b/README.md`
- `config/README.md`

The text must stop claiming that no native tests or runtime code are admitted when the native tree and bounded runtime surfaces are already present.

### Phase B — then continue the next bounded truth-pass wave

#### 7. Run a depth pass over the thinnest bounded runtime shells
After authority truth is closed, continue with a deeper truth-pass over the most obviously thin bounded modules, in this order:
- `src/nvda_desk/runtime/orchestrator.py`
- `src/nvda_desk/preparation/runtime_preparer.py`
- `src/nvda_desk/api/http/app.py`
- `src/nvda_desk/services/downstream_state_service.py`
- `src/nvda_desk/services/downstream_opening_service.py`
- `src/nvda_desk/services/downstream_live_inventory_service.py`

This wave is not about widening policy. It is about making the bounded native shells more truthful and less placeholder-like while preserving architecture boundaries.

#### 8. Re-run and record the same verification gates
After each bounded pass, rerun:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python -m compileall src tests/tier_a tests/tier_b`

Then update the new crosswalk artefact, retained-test registry, proof block, and checkpoint receipt together.

---

## 5. Execution rule

Use this stop/go rule for the continuation:
- **Do not open another broad implementation wave until authority truth is closed.**
- First make the registry, crosswalk, proof block, and control-surface text truthful to the repo that already exists.
- Then harden one bounded runtime shell family only.
- Then rerun the blocker shell and update the authority artefacts in the same change set.

That is the lawful continuation of the earlier brief after direct repo verification.
