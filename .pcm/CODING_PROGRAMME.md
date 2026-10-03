# PCM V5 Coding Programme

Status: governing PCM V5 coding profile. This profile sits over the existing PCM control substrate; it does not create a second project hierarchy.

## 1. Coding Gate contract

A coding Gate is a bounded unit of product meaning executed through one or more stages and closed only when its declared whole-Gate proposition is supported by admissible evidence.

For every coding Gate, the project contract MUST identify:

- the requirement IDs the Gate is intended to realise;
- the stage propositions that divide the work into bounded responsibilities;
- one explicit whole-Gate proposition describing the integrated meaning that must be true at promotion;
- the permitted write scope for each stage and for the Gate as a whole;
- the stop conditions that prevent autonomous continuation;
- the reviewer challenges selected for this Gate;
- the required evidence classes and verification propositions;
- the repair disposition rules;
- the promotion boundary; and
- the accepted recovery base from which lawful append-only recovery would begin.

Stage completion and whole-Gate completion are separate claims. Passing a stage does not establish the whole-Gate proposition.

## 2. Stage proposition

Each executable coding stage MUST state one proposition that the active actor is responsible for making true.

The stage record MUST expose, without requiring unrelated historical leaves:

- stable stage/task ID and human label;
- mapped requirement IDs;
- proposition to be established;
- owning semantic authority;
- permitted write scope;
- required evidence and applicable selected reviewer challenges;
- stop condition;
- dependencies required for execution ordering; and
- semantic route records required for meaning.

The actor MAY choose implementation details inside this envelope. The actor MUST stop rather than silently change the requirement, semantic authority, actor class, write scope, acceptance law or route meaning.

### Test/proof before production implementation

When the consuming project enables `test_first_policy=required`, any task that changes executable production behaviour MUST be represented as `work_type=implementation` and cannot become executable until one of these admitted boundaries is satisfied:

1. a governing `work_type=test_proof` predecessor is accepted; and, where the behaviour is not already satisfied, its declared expected-RED verification has a current admissible receipt whose explicitly allowed exit code is non-zero; or
2. an explicit exception predecessor delegated to `PROGRAMME_OWNER` is accepted through its programme-owner review contract.

The test/proof and implementation responsibilities may be grouped at whatever bounded granularity the accepted brief and architecture justify; PCM does not require a universal one-test-leaf-per-implementation-leaf topology. The invariant is ordering and evidence: production implementation does not begin before its governing proof boundary. A project manager may not collapse or bypass that boundary conversationally.

## 3. Whole-Gate proposition

Every coding Gate MUST declare exactly one integrated proposition for promotion. It states the product meaning that the completed stages, taken together, are intended to establish.

Promotion requires evidence for this whole-Gate proposition in addition to any stage-level evidence. A green worker test, stage PASS, review PASS, verification receipt, acceptance tag and promotion commit remain distinct claims and MUST NOT be treated as interchangeable.

## 4. Requirement mapping and write scope

Every stage and whole Gate MUST map to explicit requirement IDs. A task with no mapped governing requirement is not executable.

Write scope is an authority boundary, not merely a convenience list. An actor may modify only the declared paths for the active responsibility. A required change outside that scope returns `BLOCKED` unless a lawful programme-owner transition widens the scope.

Changing the meaning of an accepted requirement is not a repair within implementation discretion; it requires the `CHANGE_MEANING` route and the applicable owner authority.

## 5. Stop conditions

Execution MUST stop when any of the following applies:

- required authority is absent, stale, contradictory or cannot be uniquely identified;
- a required semantic owner record is unavailable or its identity/hash cannot be established;
- the required change exceeds declared write scope or changes an accepted requirement;
- the actor class required by governance is stronger than the current actor;
- a required check is missing, incomplete or cannot lawfully be classified as PASS;
- a route has an unresolved stop or an unexplained exclusion;
- evidence needed to distinguish product failure from environment/control failure is unavailable; or
- continuation would rewrite accepted history instead of creating lawful append-only recovery.

A stop caused by unresolved authority or unavailable required evidence is `BLOCKED`, not `FAIL` and not `PASS`.

## 6. Reviewer challenge selection

Reviewer challenges are selected per Gate according to the semantic risks of that Gate. PCM does not impose a universal challenge count or require every challenge on every Gate.

The available challenge classes retained for PCM V5 are:

- **Public seam / source trace** — establish that the exercised behaviour reaches the admitted product seam rather than only a fixture, surrogate or test-only path.
- **Optionality / ordering** — exercise optional, absent, reordered or partial materialisation where those states can alter semantics.
- **Identity** — challenge candidate/source/configuration identity and stale or mismatched evidence where identity affects the proposition.
- **Adverse environment / configuration** — exercise relevant configuration or runtime conditions that can expose false-green behaviour or separate environment limitations from product behaviour.

The Gate contract MUST name the selected challenges and why they are relevant. A reviewer may identify a newly evidenced challenge need, but expanding the governing challenge contract beyond the admitted Gate envelope follows the applicable authority route.

## 7. Evidence classes and disposition

Evidence is proposition-scoped. Each material proposition MUST be classified using one of these result dispositions:

- `PASS` — admissible current evidence establishes the proposition under its declared scope.
- `FAIL` — admissible evidence establishes that the proposition is false under its declared scope.
- `UNKNOWN` — available evidence does not establish whether the proposition is true or false.
- `BLOCKED` — a required operation, authority decision or evidence acquisition cannot lawfully proceed.

Evidence classes may include, as applicable to the proposition:

- product/runtime test evidence;
- source/configuration trace evidence;
- verification receipts bound to the current inputs and governing contract;
- independent review evidence bound to the exact candidate and review material;
- Git candidate, acceptance and promotion identity; and
- programme-owner decisions where the boundary requires owner authority.

Environment capability and product correctness are separate axes. Timeout, unavailable tooling, incomplete execution or unsupported environment capability MUST NOT be promoted to PASS.

## 8. Repair disposition

A review or verification result returns `REPAIR` when the governing meaning remains accepted and the defect can be corrected within the admitted requirement, semantic authority, write scope and actor-class envelope.

A result returns `BLOCKED` rather than `REPAIR` when correction would require any of the following:

- changing accepted requirement meaning;
- widening write scope or semantic authority;
- changing the delegated actor class or acceptance law;
- resolving an authority conflict for which the current actor is not the owner; or
- proceeding without required evidence or an admissible recovery base.

A repeated defect mechanism is routed with the relevant prior findings needed to classify recurrence. PCM MUST NOT use a fixed retry count or fixed last-N history window as a substitute for that judgement.

For a lawful in-envelope `REPAIR`, the independent reviewer returns the finding directly to the owning autonomous worker. The PM/orchestrator is not a transport or approval hop for that retry. The worker and reviewer may remain the paired execution contexts across repeated in-envelope corrections: each changed candidate requires a fresh review packet/result, but not a new PM-mediated dispatch and not a new reviewer thread merely because candidate bytes changed. `PASS` returns control to the PM/orchestrator for the next governed transition. Any correction that would change the admitted envelope, or cannot lawfully establish the next bounded refinement, is `BLOCKED` back to governance.

### 8.1 Bounded refinement contract

A repair may be represented as a new task without programme-owner escalation only when it declares a `refinement` contract against an already-admitted root task and stays inside that root task's approved envelope. The repair task MUST use a new stable task ID; reopening or rewriting the prior stable ID is not refinement.

The refinement envelope is unchanged only when all of the following remain identical to the admitted root task:

- requirement IDs;
- semantic routes, including owner identity and every authority hash;
- write scope and applicable authority-section references;
- acceptance and verification law;
- independent/programme-owner review contract, where present; and
- delegated actor class.

A bounded repair declares a stable defect `mechanism_id`, requires fresh independent review for changed candidate bytes, and carries every prior repair task for the same root-envelope/mechanism pair in `prior_repair_task_ids`. When that list is non-empty, recurrence classification is an independent-review responsibility. The controller may identify the repeated mechanism and route the complete same-mechanism lineage; it MUST NOT decide semantic recurrence by counting attempts.

A proposed repair is `BLOCKED` for autonomous refinement and must use the programme-owner route if it changes requirements, semantic owner/authority hashes, write scope, authority references, delegation, acceptance/verification law or review contract. No retry counter, maximum attempt count or fixed last-N repair window is part of the refinement contract.

Fresh review means a new review packet/result bound to the changed candidate bytes and current governing hashes. A prior PASS does not carry over to changed candidate bytes.

## 9. Promotion boundary

Promotion is a separate boundary after stage completion and review. The exact candidate being promoted MUST be identified in Git and bound to the governing requirement, Gate proposition, selected review material and required verification evidence.

Promotion is lawful only when:

- all required stage responsibilities for the Gate are complete;
- the whole-Gate proposition has admissible evidence;
- required independent review, where declared, is current for the exact candidate;
- every declared required verification item has a current successful admissible receipt under the governing acceptance rules; and
- no unresolved `UNKNOWN` or `BLOCKED` claim is being silently treated as PASS for a required proposition.

Promotion does not by itself erase or rewrite earlier accepted states.

## 10. Recovery base

The recovery base is the last admitted accepted product/Gate point from which new work may lawfully proceed after downstream work is abandoned or invalidated.

Recovery is append-only:

- preserve prior accepted tags and Git ancestry;
- preserve failed, abandoned and superseded evidence as history;
- create a new lawful lineage/ID where recovery requires new work; and
- never reset or rewrite accepted history merely to make downstream state appear clean.

A durability bundle or `flush` is transport/recoverability evidence only; it is not a semantic recovery base or acceptance claim.

## 11. Semantic route modes

Execution dependencies determine readiness/order. Semantic routes determine what meaning must be loaded or consulted. They are separate graphs.

### `CONSUME_ADMITTED`

Use when the active responsibility consumes meaning that is already admitted and is not being changed or adjudicated.

The route MUST identify the exact bounded admitted records needed for the active proposition. It MUST NOT require a full historical owner record merely because that record is an execution predecessor.

If the admitted record is missing, stale, hash-mismatched, semantically insufficient or becomes disputed, the route cannot remain `CONSUME_ADMITTED`; execution stops until a lawful route is established.

### `CHANGE_MEANING`

Use when the active responsibility changes, adjudicates or redefines semantic meaning.

The route MUST provide the complete owner record plus every dependency whose trigger is active for that change. Untriggered or unrelated records remain excluded rather than being loaded by default.

`CHANGE_MEANING` does not grant authority to change meaning; it identifies the semantic context required when the governing actor is already authorised to do so.

## 12. Required route-record contract

Every semantic route record MUST contain enough durable identity to reconstruct why each authority unit was or was not supplied. The schema implemented in the successor controller/task contract MUST represent:

- **owner record** — identity and content/hash reference for the semantic authority that owns the meaning;
- **route mode** — exactly `CONSUME_ADMITTED` or `CHANGE_MEANING`;
- **complete-context records** — records that must be supplied in full when their meaning is being changed/adjudicated;
- **bounded records** — exact admitted records sufficient for unchanged consumption;
- **conditional trigger results** — each conditional dependency, its trigger result and the evidence/source used to resolve it;
- **exclusions with reasons** — each otherwise relevant candidate record excluded from the packet and the explicit reason for exclusion; and
- **unresolved stops** — any unresolved authority, provenance, trigger or semantic condition that prevents lawful continuation.

Every referenced authority/record identity MUST be hash-bindable by the Task 2 implementation. Missing owner identity, unexplained exclusion, asserted-but-untriggered dependency, unresolved stop or source/hash drift MUST fail closed.

## 13. Fresh-actor operating view

For any active coding responsibility, the bounded execution packet must let a fresh actor answer four questions without reading unrelated historical leaves:

1. What proposition am I responsible for establishing?
2. What governing authority and semantic records do I need for that proposition?
3. What may I change and what evidence/challenges must I produce?
4. What condition requires me to stop rather than continue?

For review, the corresponding packet must make the selected challenges and the `REPAIR` versus `BLOCKED` boundary explicit.
