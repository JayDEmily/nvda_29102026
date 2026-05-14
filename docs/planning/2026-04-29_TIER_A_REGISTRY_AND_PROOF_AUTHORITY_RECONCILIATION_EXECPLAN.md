# Tier A Registry and Proof Authority Reconciliation — Execution Plan

Status: current continuation harmonised for control-surface truth; pending explicit user acceptance
Date: 2026-04-29
Current work branch: `work/agents-md-bootloader-20260430`
Original full-readiness branch target: `work/tier-a-registry-and-proof-authority-reconciliation`
Current continuation source lock: rolling cumulative patch applied on `work/agents-md-bootloader-20260430`
Current decision: `READY_TO_CONSIDER_ATLAS = false`
Current continuation objective: accept, reject, or repair the mechanically reconciled testing-governance state

This plan exists to get the repo from the current native-codebase confidence state to the point where Atlas ideas may be considered for admission.

This is not an Atlas import plan.
This is not an Atlas selection plan.
This is not a runtime feature plan.
This is not a speed-run.

---

## 1. Objective

Historical original objective: reach a truthful, evidence-backed decision on whether the active native repo is ready to consider Atlas ideas.

Current continuation objective: decide whether the mechanically reconciled testing-governance state can be accepted, rejected, or needs a further bounded repair gate.

The original target state was:

```text
READY_TO_CONSIDER_ATLAS = true
```

That original Atlas-consideration state is not reached by the current continuation. It is lawful only when:

1. repo authority documents align;
2. vocabulary governance is satisfied before durable test/code/docstring language changes;
3. the retained-test registry agrees with actual Tier A/B/C test authority;
4. Tier A tests are explicitly admitted, demoted, retired, replaced, or lawfully carried pending;
5. code aligns to the normative stack, Native Architecture Blueprint, and admitted tests;
6. DMPV3 is proven at the seams where the architecture requires packetised carriage;
7. dynamic coefficient authority is bounded, governed, and separated from playbook blobs;
8. thin/future surfaces remain visible and truthfully labelled;
9. docstrings explain settled code and do not create authority;
10. authorised proof is run and recorded truthfully;
11. a thin receipt records the result;
12. the tranche is committed on a work branch.

---

## 2. Non-negotiable execution posture

This tranche must not optimise for speed.

The operator must not:

- skip routed files for efficiency;
- replace full reading with grep, AST analysis, line counts, docstring counts, dependency maps, or keyword ledgers;
- claim a file was reviewed or understood unless the relevant file was read in full;
- bypass vocabulary governance to save time;
- bypass `tests/AGENTS.override.md`;
- treat test folder location as authority;
- treat docstrings as doctrine;
- treat Atlas or legacy donor material as live authority;
- use broad end-to-end tests as a substitute for seam/module proof;
- create bloated ledgers when Git history and a thin receipt are sufficient;
- create packages/tarballs unless explicitly requested;
- import Atlas ideas during this tranche.

Programmatic parsing, grep, AST analysis, dependency maps, line counts, and docstring counts may be used only as structural triage after the relevant files have been read in full.

If the work cannot be done properly inside one model pass, the operator must stop at a lawful gate and report exact state. The operator must not compress the work into a shallow answer.

---

## 3. Authority order

Read `PROJECT_EXECUTION_METHOD.md` first when it is present in the task surface.

After `PROJECT_EXECUTION_METHOD.md` has been read where required, this tranche must follow the execution read sequence owned by `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`:

1. `AGENTS.md`;
2. the active bounded pack surface in scope;
3. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
4. `docs/01_NORMATIVE_CORE.md`;
5. the numbered live authority documents that own the active question, in the order required by the active bounded pack where that order does not contradict higher-priority live law;
6. `PLANS.md` when the active bounded pack routes it as the repo-level plan standard;
7. the active bounded pack execution-plan surfaces that define the current gate;
8. retained evidence only after all live authority above has been read.

For this route, the active bounded pack surface is `intent_migration/testing_governance_reconciliation/AGENTS.override.md`.

For this route, route-specific authority may include testing/proof law, DMPV3 law, vocabulary governance, Native Blueprint law, test-surface routing, retained-test registry surfaces, proof artefacts, admitted tests, runtime code as observed implementation, and docstrings as explanatory surfaces only.

No lower-precedence surface may weaken or reinterpret a higher-precedence surface.

---

## 4. Required change order

If this tranche discovers required repo changes, apply them in this order:

```text
vocabulary
→ retained-test registry / test authority
→ tests
→ code only if doctrine/test authority exposes a code conflict
→ docstrings
→ proof
→ thin receipt
→ commit
```

Code-first repair is prohibited when vocabulary or test authority must change first.

Docstrings are last because they explain settled code truth.

---

## 5. Git discipline

Current work branch:

```text
work/agents-md-bootloader-20260430
```

Original full-readiness branch target recorded by the first version of this plan:

```text
work/tier-a-registry-and-proof-authority-reconciliation
```

The current branch owns the authorised control-surface repair and acceptance-state harmonisation sequence opened in this conversation. Do not silently move this work to a different branch; open a new branch only if the user explicitly authorises a new route or branch handoff.

Commit discipline:

- one bounded work branch;
- one tranche objective;
- small coherent commits where useful;
- no sprawling artefact pack;
- thin ledgers only where they preserve decisions not already visible in Git;
- Git history is the durable ledger;
- final commit only after proof state is recorded truthfully.

Expected patch surface for the current plan-vs-current-state harmonisation step:

```text
docs/planning/2026-04-29_TIER_A_REGISTRY_AND_PROOF_AUTHORITY_RECONCILIATION_EXECPLAN.md
```

Completed prior control-surface harmonisation in this conversation also touched:

```text
AGENTS.md
PLANS.md
var/audit/briefs/2026-04-28_TESTING_GOVERNANCE_RECONCILIATION_TRANCHE.md
var/audit/ledgers/testing_governance_reconciliation_tranche_ledger.json
docs/planning/2026-04-29_TIER_A_REGISTRY_AND_PROOF_AUTHORITY_RECONCILIATION_EXECPLAN.md
```

No runtime code changes are authorised by this plan unless a later gate proves they are required.

---

## 6. Current registry state

`config/retained_test_registry.yaml` now records the following Tier A inventory state:

```text
tier_a_test_count: 67
registered_retained_seed_tier_a: 67
tier_a_file_registered_outside_retained_seed_tier_a: 0
pending_explicit_registry_record: 0
```

This records mechanical registry reconciliation only.

It does not by itself establish semantic retained-family trust, because registry law still requires runtime-code and docstring rereads before any retained or materially relied-upon test family is trusted.

The reconciliation pack therefore remains pending explicit user acceptance before closeout or next-route promotion.

---

## 7. DMPV3 boundary discipline

DMPV3 must not be treated as universal data transfer.

The tranche must distinguish:

1. non-DMP preparatory/raw/reference flows;
2. early ingress, temporal, and calendar/reference surfaces where DMPV3 may not be the lawful carrier;
3. cognition-stack seams where DMPV3 is required or emerges as a packet boundary;
4. parallel-risk gateway/output seams where DMPV3 may be required at specific boundaries rather than everywhere;
5. downstream handoff seams where DMPV3 carries candidate/risk/capital/review material;
6. review/replay/proof surfaces that consume DMPV3 lineage.

The DMPV3 audit must answer seam by seam:

- is DMPV3 required here?
- if yes, who is the producer?
- who is the consumer?
- what packet family is carried?
- what lineage is preserved?
- what validation happens?
- what state semantics apply to omission, null, and explicit values?
- what must not be smuggled through the packet?

Do not write “all module transfers use DMPV3”.

---

## 8. Modular architecture doctrine

The repo is a modular trading-system chassis.

The tranche must preserve the ability to:

- add, remove, demote, or replace options playbooks;
- add later NVDA shares/futures/instrument surfaces without contaminating options-specific logic;
- keep playbook logic separate from coefficient authority;
- keep dynamic coefficients bounded, governed, and lineage-visible;
- keep serial cognition separate from parallel risk;
- keep capital deployment downstream of candidate formation and risk assessment;
- keep API/broker/opening/inventory/close/review surfaces visible even where thin or future;
- test seams and module-to-module contracts instead of relying on premature end-to-end tests.

A strategy may fail. A playbook may be retired. A coefficient family may be replaced. The chassis must survive that.

---

## 9. Gate sequence

### Gate 0 — Branch and source lock

Pass when:

- branch is `work/agents-md-bootloader-20260430`;
- source state and commit are recorded;
- no unplanned dirty files exist.

Current source lock for this continuation:

```text
branch: work/agents-md-bootloader-20260430
source commit at Gate 5 intake: 0f738d5
```

This replaces the stale original branch-target requirement for the current control-surface repair sequence. It does not mark the full Tier A registry/proof plan complete and does not allow Atlas consideration.

### Gate 1 — Authority read

Read in full:

- `PROJECT_EXECUTION_METHOD.md` when present in the task surface
- `AGENTS.md`
- `intent_migration/testing_governance_reconciliation/AGENTS.override.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
- `docs/09_DMPV3_PROTOCOL_CORE.md`
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `PLANS.md`
- this execution-plan surface

Pass when authority order, process law, testing law, DMPV3 law, vocabulary law, and native blueprint law are understood without contradiction.

### Gate 2 — Test authority read

Read in full:

- `tests/AGENTS.override.md`
- `tests/README.md`
- `tests/tier_a/README.md`
- `tests/tier_b/README.md`
- `tests/tier_c/README.md`
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`

Pass when the tranche has exact test-authority law before changing registry/tests.

### Gate 3 — Vocabulary pre-check

Read in full:

- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`
- `src/nvda_desk/schemas/vocabulary.py`
- `scripts/build_canonical_vocabulary.py`

Pass when any durable terms required by the reconciliation are admitted, aliased, or quarantined.

### Gate 4 — Tier A registry reconciliation

For each non-clean Tier A record:

1. read the registry entry in full;
2. read the test file in full;
3. read any directly referenced source file in full;
4. classify the test as one of:
   - admit;
   - demote;
   - retire;
   - replace;
   - carry pending with explicit lawful reason;
5. record the reason in the thinnest durable surface required.

Pass when no Tier A file remains ambiguous by registry/test authority.

### Gate 5 — Test update gate

Only if Gate 4 proves a test-authority change is required:

1. update registry/test authority first;
2. update tests only when required;
3. do not update runtime code yet unless a test/code doctrine conflict is proven.

Pass when test authority and actual tests agree.

### Gate 6 — Code conflict gate

Only if Gate 5 proves code violates admitted authority:

1. read the affected source file in full;
2. read the owning blueprint surface in full;
3. repair code within the lawful architecture home;
4. preserve modularity and DMPV3 seam discipline; keep `coefficient_authority` governance intact.

Pass when code obeys docs/tests without introducing new architecture drift.

### Gate 7 — Docstring gate

Only after code truth is settled:

1. read touched source file docstrings;
2. update docstrings only to explain observed bounded behaviour;
3. do not let docstrings claim mature behaviour for thin seams, placeholders, reserved surfaces, or future-only surfaces.

Pass when docstrings are truthful and subordinate.

### Gate 8 — Proof gate

Run proof from the lawful local environment.

At minimum:

```text
python --version
cat .python-version
make scaffold-check
make format-check
make lint
make test
```

If dependency execution is unavailable, record exact failure and do not claim tests passed.

Run `make proof-block BLOCK=<name>` only where proof-block authority admits the block.

### Gate 9 — Thin receipt and commit

Write a thin receipt only if needed.

The receipt must say:

- branch;
- files changed;
- registry/test decisions;
- proof commands and outputs;
- unresolved blockers, if any;
- whether Atlas consideration is now allowed.

Commit the tranche.

---

## 10. Exit criteria

`READY_TO_CONSIDER_ATLAS = true` only if all are true:

1. non-clean Tier A registry statuses are resolved or lawfully carried;
2. test authority and registry agree;
3. no Tier A file relies only on folder location for authority;
4. vocabulary governance is satisfied;
5. DMPV3 seam obligations are not overclaimed;
6. dynamic coefficient authority remains governed and bounded;
7. modular replaceability is preserved;
8. thin/future surfaces are accounted for;
9. proof is run and recorded truthfully;
10. docstrings are truthful if touched;
11. final state is committed on the work branch.

If any item fails:

```text
READY_TO_CONSIDER_ATLAS = false
```

and the tranche must name the next repair gate.

---

## 11. Files read in full before this plan was written (historical receipt)

The following files were read in full to write this plan:

| File | Lines | SHA-256 |
|---|---:|---|
| `AGENTS.md` | 31 | `35081c8f9ce50d73ce9ad9036693c3ab4159c6cdab4a1ed4c98757f6f37ab57e` |
| `PLANS.md` | 189 | `5e4e56f4fd39dd8188c4410922baedfd058bd1f6458e0480984ed53099a3217c` |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | 84 | `27bbac5208a68a9dee832b652d47ec0cce0d96ae1720cdd957c0c23b34418e86` |
| `docs/01_NORMATIVE_CORE.md` | 117 | `32d26e8b67a5308291e61294cbc511d6bf51dccc5f961c11798714b249d813ee` |
| `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` | 147 | `dd2afe14ccc7e2dc1083495d619557fc405d19042cff1055014c8c2e3a293f07` |
| `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` | 32 | `471b70203d98348672c4012cb301eb8a4a270a2c405f753342107d59a9ea7ed3` |
| `docs/08_TESTING_AND_PROMOTION_CORE.md` | 202 | `c3409910fd27d5452304469584179fb0c421ba82ee7903b95f9e0415b395e944` |
| `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` | 13 | `c9b8c96deef18fc1b2b3c069c935216f1f5ff8bb363da02570710b6b56d691c1` |
| `docs/09_DMPV3_PROTOCOL_CORE.md` | 187 | `816ecb0b5e2bc76437920982e8eb37b4118f348a4aba8606806c45eb0ddf4abe` |
| `docs/09.1_DMPV3_PROTOCOL_WORKING.md` | 31 | `8e1c4e69cd799b860c5e0747f4f053c62106e8149340fdc050ec7f5b019a69f0` |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` | 50 | `2d365d1f7bb7a765731a5234c2e4deb8cad3a2dff2963fbbe942711329192fa8` |
| `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` | 23 | `620323b5f3e8b31fd47a68ef3e80fa4c4cb683c7a4be0785343fd534d98b3ae8` |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | 758 | `8f3de1fe9cac41c4b36c35c78a1acadb4d60b39e2f82a56f8ad134ed3c94f563` |
| `docs/vocabulary/README.md` | 23 | `e76cc9c284641d194283f0a3194d0b81d2a603fd5f5c01b042f3b0fbe0e74439` |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | 51 | `1e2643dcd604c193b7e019b23e39d64a966c58d8facf93fd41229246636fd24a` |
| `docs/vocabulary/vocabulary_registry.md` | 60 | `776c1e390edfb95adefe03cf67b438b345b0bb676f0367578e3aeef7521ad14c` |
| `tests/AGENTS.override.md` | 76 | `35db7663eccdcf5e8104c170bdc4f057411ceedc61ca87050b3f2810238c1900` |
| `tests/README.md` | 11 | `c85d58cece621a044186f8aa88ad01a0ad2c90b7f54085f116520e16970522af` |
| `tests/tier_a/README.md` | 7 | `e32a0e2677131dc0f330093f14fd3c588c5d85f4067f2bb74a8651f9f7eb2ca1` |
| `tests/tier_b/README.md` | 7 | `d30e54959d88a7309081f70243e5376983fff2217e5b13230825b7aae13cf2fa` |
| `tests/tier_c/README.md` | 7 | `4d1a32dc7d7bd159f06867a22b17d20edc49eda39effce494e4e5fb51f718477` |
| `config/retained_test_registry.yaml` | 2173 | `09e2fbd52228ebbd420d7f3ac286561bd2b42f2826907d3446f7130e4bcd206e` |
| `config/proof_blocks.yaml` | 5 | `5afb6c44800baf89cf87eafdd91ba7faee3365bd7a992a325876dee04e1ff9af` |

---

## 12. Current planning decision

The testing-governance reconciliation route remains pending explicit user acceptance.

Current objective:

```text
Decide whether to accept the mechanically reconciled retained-test registry state, reject it, or open a further bounded repair gate.
```

Current authorised change surface for plan-vs-current-state harmonisation:

```text
docs/planning/2026-04-29_TIER_A_REGISTRY_AND_PROOF_AUTHORITY_RECONCILIATION_EXECPLAN.md
```

Previously completed control-surface harmonisation in this conversation touched:

```text
AGENTS.md
PLANS.md
var/audit/briefs/2026-04-28_TESTING_GOVERNANCE_RECONCILIATION_TRANCHE.md
var/audit/ledgers/testing_governance_reconciliation_tranche_ledger.json
docs/planning/2026-04-29_TIER_A_REGISTRY_AND_PROOF_AUTHORITY_RECONCILIATION_EXECPLAN.md
```

Atlas remains out of scope until this route exits cleanly and the user explicitly opens a lawful Atlas route.

---

## 13. Gate 6 plan-vs-current-state review

Gate 6 found that the original Atlas-readiness objective in this plan could be misread as the current continuation objective.

Current truth:

```text
The original full Atlas-readiness gate sequence is not complete.
The current route remains testing-governance reconciliation only.
The mechanically reconciled registry state remains pending explicit user acceptance.
READY_TO_CONSIDER_ATLAS remains false.
```

Remaining original readiness gates are not closed by the control-surface harmonisation sequence. The next lawful execution gate, if the user wants to continue the original readiness plan, is Gate 1 Authority read using the full file list in section 9.

No runtime code or pytest implementation change is authorised by this review.

---

## 14. Gate 3 vocabulary pre-check continuation

Gate 3 found that the control-surface harmonisation sequence relies on durable process terms that must be vocabulary-governed before closeout claims.

The bounded local vocabulary supplement in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` now admits or enriches the required process terms for this route:

- `authority intake gate`
- `execution read sequence`
- `active bounded pack`
- `active bounded pack surface`

This records vocabulary admission for the control-surface repair sequence only. It does not authorise Atlas, runtime work, pytest implementation changes, or promotion readiness.

---

## 15. Gate 7 through Gate 8 continuation receipt

Gate 7 authority-read repair:

- `AGENTS.md`, `PLANS.md`, and this execution-plan surface now defer to the execution read sequence owned by `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`.
- Gate 1 now explicitly includes `PROJECT_EXECUTION_METHOD.md` when present, the active bounded pack surface, `PLANS.md` after the numbered live authority documents, and this execution-plan surface.
- The previous contradiction between `AGENTS.md` / `PLANS.md` and `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` is resolved for this route.

Gate 2 test-authority read:

- `tests/AGENTS.override.md`, tier README surfaces, `config/proof_blocks.yaml`, and `config/retained_test_registry.yaml` were read for the current route.
- `config/retained_test_registry.yaml` parsed successfully.
- Current Tier A inventory remains `67 / 67 / 0 / 0`.

Gate 3 vocabulary pre-check:

- Control-surface process terms required by the current repair route are admitted or enriched in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`.
- This vocabulary admission is bounded to the current control-surface repair sequence and does not authorise Atlas, runtime work, pytest implementation changes, or promotion readiness.

Gate 4 Tier A registry reconciliation:

- No non-clean Tier A inventory row remains to classify in the current registry inventory.
- This is a mechanical registry-state observation only. It does not claim semantic retained-family trust beyond the registry's own recorded reread fields.

Gate 8 proof attempt:

```text
python --version -> Python 3.13.5
cat .python-version -> 3.13.5
make scaffold-check -> repo scaffold present; status 0
make format-check -> failed: .venv/bin/python not found; make Error 127; wrapper status 2
make lint -> failed: .venv/bin/python not found; make Error 127; wrapper status 2
make test -> failed: .venv/bin/python not found; make Error 127; wrapper status 2
```

Proof state:

```text
READY_TO_CONSIDER_ATLAS remains false.
Testing-governance closeout is not claimed.
The next repair gate is environment/proof-run availability, unless the user explicitly narrows the objective back to governance-only acceptance of the mechanically reconciled registry state.
```
