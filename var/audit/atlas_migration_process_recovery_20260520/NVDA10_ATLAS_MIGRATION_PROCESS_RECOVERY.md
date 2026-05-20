# NVDA10 Atlas-to-active-codebase migration process recovery

## Scope and status

This report answers one question only: **how Atlas ideas used to be brought into the active codebase**.

It does **not** implement anything. It does **not** decide that any of the remaining 1,128 Atlas ideas are implemented. It recovers the prior working method from repo evidence.

Repo inspected: `/mnt/data/process_recovery/MVD-A10_1704_V1`  
Branch inspected: `work/fwd014-final-non310-sweep`  
HEAD inspected: `1f417b39ddd75312f92670d7f0927813a5dffe8c`

Read in full for this process recovery:

- `/mnt/data/PROJECT_EXECUTION_METHOD.md`
- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- relevant `intent_migration/**/AGENTS.override.md` files
- `tests/AGENTS.override.md`
- the numbered governing docs listed in the process evidence below
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`
- all 44 retained `ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_*_RECEIPT.md` files under `var/audit/active_code_atlas_001/**/receipts/`
- the comparison plan, comparison receipt, and test-first execution queue files listed below

No tests were run in this pass.

---

## Direct answer

Yes — the old method exists in the repo.

It is not a single neat script. It is a **controlled migration workflow** spread across:

1. root authority: `AGENTS.md`;
2. active-code Atlas plan: `PLANS.md`;
3. live execution ledger: `ROADMAP_LEDGER.md`;
4. intent-migration route overrides;
5. testing and vocabulary governance documents;
6. the active-code Atlas comparison artefacts and test-first queue;
7. row-specific receipts from prior successful execution.

The method was:

```text
Atlas idea / Bridge row
→ map to one of the 18 services
→ compare against active-code evidence
→ classify the gap
→ full-read the governing docs/source/tests for that service
→ define tests first
→ write or extend Tier A/B/C tests
→ run red-first proof where a gap exists
→ change source/config/YAML only after tests define the invariant
→ run targeted proof and broader retained proof
→ update proof blocks, retained-test registry, receipts, manifests, and ledger
→ move to the next row/service
```

The important bit: **receipts were not the method. They were the proof trail after the method was executed.**

---

## Evidence: authority and migration order

`AGENTS.md` defines the hierarchy and Atlas migration order:

- Authority order is direct user instruction, `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, governing normative docs, route overrides, tests, implementation code, then comments/docstrings: `AGENTS.md:109-119`.
- Runtime behaviour must follow `normative intent → tests → implementation → documentation`: `AGENTS.md:123-130`.
- Atlas material is only candidate intent until lawfully admitted: `AGENTS.md:132-133`.
- Required Atlas migration order is `normative intent → tests → implementation → evidence → ledger update`: `AGENTS.md:135-140`.
- Runtime behaviour must not be directly mutated from Atlas outside the lawful migration flow: `AGENTS.md:142-147`.

`intent_migration/AGENTS.override.md` gives the earlier implementation rule:

- It requires the intent-migration authority read order: `intent_migration/AGENTS.override.md:21-35`.
- It says to plan and execute rebuild work by **atomic intent unit**, not by file: `intent_migration/AGENTS.override.md:43-49`.
- It says not to touch runtime code, tests, doctrine files, donor files, or receipts outside the admitted bounded scope: `intent_migration/AGENTS.override.md:51-55`.

`intent_migration/native_intent_implementation/AGENTS.override.md` shows the pilot-tranche version of the method:

- It required reading the normative stack, blueprint, vocabulary workflow, pilot brief, tranche ledger, Bridge validation, selected Bridge records, retained-test registry, proof blocks, and test override before test work: `intent_migration/native_intent_implementation/AGENTS.override.md:20-42`.
- It explicitly did **not** process the full Atlas in one pass: `intent_migration/native_intent_implementation/AGENTS.override.md:44-50`.
- It kept runtime code/tests read-only during tranche creation, with later leaf execution needing reopened scope before touching runtime code or tests: `intent_migration/native_intent_implementation/AGENTS.override.md:52-65`.

---

## Evidence: tests and vocabulary gates

`tests/AGENTS.override.md` confirms the testing side of the old method:

- Before touching tests, read root controls, routing docs, normative docs, vocabulary governance where durable terms are touched, testing/promotion docs, retained-test registry, proof blocks, then the specific test/source/fixture surfaces: `tests/AGENTS.override.md:11-23`.
- Runtime code is only the observed implementation surface and cannot override normative doctrine, vocabulary governance, admitted proof, or retained-test registry authority: `tests/AGENTS.override.md:25-38`.
- A pytest file is not admitted merely because it sits under `tests/tier_a`, `tests/tier_b`, or `tests/tier_c`; registry/proof-block/active-pack authority is required: `tests/AGENTS.override.md:40-47`.
- Before changing a test, the invariant must be identified and classified as live/defer/archive/demote/promote/block: `tests/AGENTS.override.md:48-54`.
- Before relying on a native test family, reread runtime code and docstrings and record divergence: `tests/AGENTS.override.md:62-76`.

`docs/08_TESTING_AND_PROMOTION_CORE.md` defines the tier law and proof closeout:

- Tier A is blocking governed proof; Tier B is bounded shadow proof; Tier C is historical/observational/non-blocking proof: `docs/08_TESTING_AND_PROMOTION_CORE.md:29-61`.
- Proof artefacts cannot change tier by habit or convenience: `docs/08_TESTING_AND_PROMOTION_CORE.md:37-39`.
- Durable proof language must obey vocabulary governance and cannot become a back door for vocabulary drift: `docs/08_TESTING_AND_PROMOTION_CORE.md:121-133`.
- Proof-backed branch truth must update required proof receipts, retained-test registry, proof manifests, and affected control-surface receipts: `docs/08_TESTING_AND_PROMOTION_CORE.md:159-169`.
- Silent promotion/demotion is prohibited and a persuasive narrative does not make insufficient proof sufficient: `docs/08_TESTING_AND_PROMOTION_CORE.md:171-192`.

`docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` define the vocabulary gate:

- One durable term must map to one governed meaning; aliases must be explicit; durable terms cannot enter docs/schemas/manifests/receipts/code unless governed or admitted in the same bounded gate: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:6-12`.
- Candidate terms are classified only as `enrich_existing`, `add_new`, `alias_only`, or `quarantine`: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:23-33`.
- The vocabulary workflow harvests terms, reconciles against the canonical file, classifies candidates, regenerates the canonical vocabulary, and runs enforcement tests: `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:5-15`.
- Synonym-candidate audit must run when governed vocabulary surfaces change and unresolved candidates must escalate rather than be hand-suppressed: `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:45-51`.

---

## Evidence: the old active-code Atlas comparison method

`PLANS.md` gives the method for creating active-code evidence and comparing it to Atlas/Bridge:

- The objective was to create a primary active-code Atlas mapping current active source, tests, configs, data, contracts, schemas, receipts, and docstrings into the same 18 surfaces used by the Atlas Bridge: `PLANS.md:42-51`.
- The generated all-surface artefact was later reclassified as structural inventory only; it could help navigation but did not prove implementation, test pass, or semantic correctness: `PLANS.md:56-75`.
- The preserved repo hierarchy was `normative documents → tests → code → code docstrings`: `PLANS.md:132-146`.
- The active-code record shape deliberately separated runtime behaviour, tests, configs, receipts, data, schemas, and docstrings: `PLANS.md:241-307`.
- Gate 3 required records to have path/line evidence and to keep runtime, tests, config, receipts, data, schemas, and docstrings separate: `PLANS.md:489-513`.
- Gate 5 defined statuses for `already_satisfied`, `partially_satisfied`, `missing`, `transform_required`, `blocked`, and `conflict`, and required future Tier A/B/C test work to be queued from normative gaps, not current-code output: `PLANS.md:540-562`.

The comparison plan then reduced the 1,716 raw rows into execution groups:

- It compared the recovered Atlas intent corpus, the Atlas Bridge/native satisfaction ledger, and the active-code structural inventory scaffold: `var/audit/active_code_atlas_001/ACTIVE_CODE_ATLAS_001_THREE_WAY_COMPARISON_PLAN.md:5-13`.
- It defined comparison statuses and later actions, including “write or update tests before code changes” for partially satisfied rows and “create tests first, then implement only if authorised” for missing rows: `var/audit/active_code_atlas_001/ACTIVE_CODE_ATLAS_001_THREE_WAY_COMPARISON_PLAN.md:27-36`.
- It explicitly forbade treating donor Atlas as runtime authority, active code as correctness authority, docstrings as implementation proof, or static inventory as test-pass evidence: `var/audit/active_code_atlas_001/ACTIVE_CODE_ATLAS_001_THREE_WAY_COMPARISON_PLAN.md:38-45`.
- Its mechanical method grouped Bridge records by surface/owner/proof/leaf type, detected active evidence classes, assigned provisional comparison status, emitted one row per Bridge group, then required human review before tests/code: `var/audit/active_code_atlas_001/ACTIVE_CODE_ATLAS_001_THREE_WAY_COMPARISON_PLAN.md:47-55`.

The comparison receipt proves the queue that resulted:

- The comparison accounted for 1,716 Bridge records, joined 1,716 Atlas records, emitted 1,716 record-level join rows, and produced 46 test-first queue records: `var/audit/active_code_atlas_bridge_comparison_001/receipts/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_RECEIPT.md:39-47`.
- Group statuses were `already_satisfied=2`, `partially_satisfied=28`, `transform_required=18`: `var/audit/active_code_atlas_bridge_comparison_001/receipts/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_RECEIPT.md:49-55`.
- Test-first action counts were `confirm_existing_proof_only_no_refactor=2`, `extend_existing_test_family_before_code=17`, and `write_new_test_family_before_code=29`: `var/audit/active_code_atlas_bridge_comparison_001/receipts/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_RECEIPT.md:65-71`.
- The next engineering stage was test-first execution, starting with vocabulary governance; it would mutate test files first and source only if new/extended tests proved a legitimate gap: `var/audit/active_code_atlas_bridge_comparison_001/receipts/ACTIVE_CODE_ATLAS_BRIDGE_COMPARISON_001_RECEIPT.md:150-158`.

---

## Evidence: the old execution queue

The old queue file is:

`var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md`

It states:

- The queue was the deterministic execution order from Atlas + Bridge + active-code structural inventory comparison and did not itself write tests or refactor source: `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md:1-5`.
- The recommended first tranche was vocabulary governance because it was the smallest non-runtime governance surface with Tier A queue rows: `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md:7-11`.
- The queue held 46 rows across the 18 services, with actions such as `extend_existing_test_family_before_code` and `write_new_test_family_before_code`: `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md:13-62`.
- The queue guardrail was: tests first, no mutation of source/vocabulary/dependencies/original Atlas/Bridge/generated slices, and runtime trading/capital/broker/API/refactor work closed unless explicitly opened: `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md:64-69`.

---

## Evidence: the later service-row execution method

`ROADMAP_LEDGER.md` later turned the process into a service-by-service forward programme:

- It says Atlas, Bridge, active-code Atlas, receipts, manifests, and historical pass records are evidence only, not direct runtime authority: `ROADMAP_LEDGER.md:593-602`.
- Prior `acted_on_bounded` history meant only bounded work had happened; it did not mean complete/mature/implemented/reconciled/promoted/closed for all future work: `ROADMAP_LEDGER.md:603-620`.
- Each surface row from `FWD-001` to `FWD-018` used gates `.0` to `.9`: surface open, authority full read, evidence inventory, three-way comparison, test-first plan, test mutation, source/config mutation, targeted proof, broader proof, receipt/ledger close: `ROADMAP_LEDGER.md:642-657`.
- The global read set for every surface includes root controls, all numbered core/working docs, blueprint, current-state map, test override if tests are touched, retained-test registry/proof blocks if proof tiers are touched, and surface-specific active-code Atlas/Atlas/Bridge/source/test/config/fixture/docstring evidence: `ROADMAP_LEDGER.md:661-677`.
- The forward service order is foundation first, then upstream runtime, preparation, cross-cutting runtime, candidate formation, parallel risk, downstream authority/opening/state/close, and review: `ROADMAP_LEDGER.md:679-702`.

This is the clean service-by-service version of the old method.

---

## Evidence: successful prior execution examples

### Example 1 — vocabulary governance, tests passed without source repair

Receipt: `var/audit/active_code_atlas_001/vocabulary_governance_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_001_VOCABULARY_GOVERNANCE_SURFACE_RECEIPT.md`

Evidence:

- Scope was surface `5.18 Vocabulary governance interface`, queue rows `ACATQ-0046`, `ACATQ-0045`, and `ACATQ-0044`: lines `19-29`.
- It read root controls, tests override, PLANS, ROADMAP, routing docs, testing docs, vocabulary docs, blueprint, current-state map, vocabulary source, vocabulary tests, proof blocks, and retained-test registry: lines `31-83`.
- It wrote 10 surface records linked to 10 Atlas records and 10 Bridge records, with validation `PASS`: lines `85-105`.
- It added a Tier A test before any source change: lines `106-117`.
- Validation included targeted pytest, vocabulary proof command, synonym clean check, diff check, and JSON parse checks; observed outputs included `16 passed`, `114 passed`, and `vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False`: lines `118-147`.
- No source implementation file, dependency file, original Atlas JSON, Bridge JSON, generated Atlas slice, vocabulary data file, runtime trading path, or refactor work changed: lines `156-163`.

### Example 2 — DMPV3 packet carriage, red-first test then source repair

Receipt: `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE_RECEIPT.md`

Evidence:

- Surface was `5.6 DMPV3 packet carriage`, queue row `ACATQ-0017 / ACABC-0017`, action class `extend_existing_test_family_before_code`: lines `3-9`.
- It created a full-read manifest, wrote surface records, extended a Tier A test before source repair, repaired only `src/nvda_desk/contracts/packets.py`, and advanced the pointer: lines `10-17`.
- The reason came from DMPV3 protocol law; the new Tier A test exposed a concrete gap where caller-supplied extensions could overwrite canonical schema identifiers: lines `18-20`.
- Full-read manifest evidence was recorded before substantive work and regenerated after mutations: lines `22-39`.
- Pre-repair targeted pytest failed `1 failed, 5 passed`; post-repair pytest passed `6 passed`; support-spine proof block passed `34 passed`; proof-block manifest check passed; surface-record/registry validator passed; full-read manifest validator passed; diff check passed: lines `51-59`.
- Original Atlas/Bridge JSON, generated Atlas slices, vocabulary data, dependency files, VENV, runtime trading, broker/API execution, capital/risk policy, financial policy, and refactor work remained unchanged: lines `61-68`.

### Example 3 — DMPV3 new test family, red-first test then source repair plus registry/proof-block updates

Receipt: `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface_new_test_family/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_008_DMPV3_PACKET_CARRIAGE_SURFACE_NEW_TEST_FAMILY_RECEIPT.md`

Evidence:

- Action class was `write_new_test_family_before_code`: lines `3-9`.
- It added a retained Tier A family, proof block, retained-test registry admission, Tier A inventory entry, surface-specific record file, then repaired only `src/nvda_desk/contracts/packets.py`: lines `10-18`.
- The new Tier A family exposed a source gap; validation records pre-repair failure and post-repair pass: lines `20-22` and `43-51`.
- Original Atlas/Bridge JSON, generated Atlas slices, vocabulary data, dependencies, VENV, runtime trading, broker/API execution, capital/risk policy, financial policy, and refactor work remained unchanged: lines `53-60`.

---

## Recovered process in plain English

For the remaining Atlas ideas, the old method should be recovered as follows:

1. **Select one service.**  
   Use the 18 services of the active codebase. Do not process the whole Atlas at once.

2. **Load only that service’s mapped Atlas ideas.**  
   Use the Atlas Bridge mapping as routing evidence, not proof of implementation.

3. **Read the authority stack in full.**  
   Minimum: `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, all relevant numbered normative docs, the service’s blueprint/current-map material, relevant route overrides, `tests/AGENTS.override.md` if tests are touched, `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` if proof tiers are touched, plus service-specific source/test/config/YAML/fixture/docstring files.

4. **Build the evidence inventory.**  
   List source, tests, config/YAML, fixtures, receipts, active-code Atlas records, Atlas intent slice, Bridge rows, and current map rows for that service.

5. **Compare three things.**  
   Compare: intended behaviour, Bridge target service, and active-code evidence. Classify each idea or group as already satisfied, partial, missing, transform-required, blocked, or conflict.

6. **Write the test-first plan.**  
   Identify Tier A/B/C proof obligations and false-positive resistance before any source/config/YAML mutation.

7. **Write or extend tests first.**  
   Do not touch source until the test states the invariant. If the test already passes, record that the source already satisfied it. If it fails, that is the red-first proof of the gap.

8. **Only then modify source/config/YAML/fixtures.**  
   Keep mutation inside the selected service boundary. Do not mutate original Atlas JSON, Bridge JSON, generated slices, vocabulary data, dependencies, broker/live trading paths, or unrelated services unless explicitly opened.

9. **Run proof.**  
   Run targeted tests, named proof blocks, retained-test registry/proof-block validation, manifest validation, diff checks, and broader Tier A/B proof required by the touched files.

10. **Record the truth.**  
   Update the service record file, retained-test registry/proof blocks if changed, receipt, full-read manifest, and `ROADMAP_LEDGER.md`. Include known true, ruled out, next row/service, and remaining Atlas IDs.

---

## What this means for the current 1,128 not-yet-included Atlas ideas

The recovered method supports your proposed next phase.

The clean operational statement is:

```text
The 1,128 Atlas ideas are mapped by the Atlas Bridge to the 18 services of the active codebase, but they are not yet included in active-codebase source behaviour by the current evidence rule. The migration should proceed one service at a time. For each service, read the governing documents in full, compare that service's mapped Atlas ideas against active-codebase evidence, write or extend Tier A/B/C tests first, then amend source/config/YAML/fixtures only inside the opened service boundary, and close with proof receipts, full-read manifests, registry/proof-block updates, and ledger updates.
```

Do not use the old 46-row queue as the current execution queue for the 1,128. Use it as **method evidence**. The new queue should be regenerated from the V2 forensic report and the current Atlas Bridge mapping, then executed service by service.

---

## Known true

- The old method exists and is evidenced in repo files.
- The old method was test-first, not receipt-first.
- Atlas/Bridge evidence was routing evidence, not runtime authority.
- Source/config/YAML changes happened only after test-first proof opened a specific gap.
- The old method used vocabulary governance before durable terms could enter tests, proof artefacts, receipts, schemas, or code.
- Prior successful examples include both “test passed without source repair” and “test failed first, then source repaired”.

## Ruled out

- A receipt alone is not proof that an Atlas idea is implemented.
- The active-code structural inventory is not proof that an Atlas idea is implemented.
- The old method did not process all 1,716 ideas as one giant implementation batch.
- The old queue artefact did not itself mutate tests or source.

## Next gate

Create a new **service-by-service Atlas migration plan** from the V2 forensic report:

1. group the 1,128 not-yet-included Atlas ideas by the 18 services;
2. choose the first service by dependency order, starting with vocabulary/testing/proof foundations if any not-yet-included ideas remain there;
3. create the service-specific read set;
4. create the service-specific test-first queue;
5. execute one service only.
