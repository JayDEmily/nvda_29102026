# Programme Owner Direction — Lineage-Aware Review and U03 Blocker Correction

**Date:** 2026-09-24
**Scope:** reusable VI-13R review routing plus current `IWO-U03` blocker handling
**Supersedes:** the process allocation in `VI13R_U03_NATIVE_RETRY_ROOT_CAUSE_DIRECTION.md` that made the next Worker responsible for discovering whether the recurrent class was actually an authority gap

## 1. Process correction

Fresh Tester/Reviewer instances are stateless in conversation context but the Git repository is not. A fresh review must therefore use the preserved Git lineage before routing another failure. Independence means an independent judgement on the candidate, not ignoring predecessor findings and repairs.

Before `FAIL / RETURN_TO_WORKER`, inspect the relevant semantic-unit lineage as far back as required to identify materially related reviewer findings and corresponding Worker repairs. Do not use a fixed `last N commits` rule. After a second successive materially related failure in the same semantic unit, classify explicitly whether the new defect is `ISOLATED` or `RECURRENT_CLASS`.

For `RECURRENT_CLASS`, the Tester owns recurrence detection and handoff synthesis. The Tester must identify the common mechanism/invariant and the class-level proposition that must become true. The Worker owns the technical implementation and may choose the smallest complete design that satisfies that proposition. If current authority cannot define class-level closure, the Tester returns `BLOCKED` rather than delegating an open-ended or impossible patch sequence.

## 2. Assessment of the externally reported U03 Worker result

The Programme Owner supplied a Worker response reporting:

- status `BLOCKED — U03 NATIVE VALUE DOMAIN / EXACT-CONTENT AUTHORITY GAP`;
- reported commit `85738686e5ee41d2e6f638c1ca890d15e555a0f0`, parent `2439688f254d0bb7fc856e5e770fa1e5ae293b4a`;
- no production or U03 proof/test mutation; and
- diagnosis that `Mapping[str, object]` admits arbitrary deepcopy-able objects whose object-defined equality can collapse changed content or reject reconstructed identical state.

The reported commit/archive bytes were not supplied to this repository and are therefore **not independently verified or incorporated into ancestry here**. The underlying technical proposition was independently challenged on the governed parent state. Two mechanically admitted custom value classes were passed through the public U03 seam:

- one class whose `__eq__` always returns true caused changed same-ID native state to be accepted;
- one class whose `__eq__` always returns false caused independently reconstructed identical state to be rejected.

This establishes that the reported blocker is substantively real on the current candidate/API surface.

## 3. What actually went wrong

The Worker did not fail to execute its brief. The previous Programme Owner root-cause handoff explicitly permitted exactly two outcomes: class-level repair or this authority blocker. Given the open `Mapping[str, object]` surface, returning the blocker was a lawful completion.

The process defect was the allocation of recurrence synthesis. Reviewer 025 through Reviewer 029 had already produced enough preserved evidence for the Tester side to recognise a common equality mechanism before routing another narrow repair. The root-cause correction then overcompensated by asking the Worker to decide whether the open class could be closed from authority. This direction corrects that allocation for future cycles.

## 4. Current U03 state

U03 is now blocked on a genuine Programme Owner/domain-authority decision, not on another implementation patch. BC-005 requires native provider field/value preservation, BC-009 requires conflicting same-ID payload rejection, and BC-010 permits same-ID retry only for identical content. The realised public field remains `native_record: Mapping[str, object]`; current accepted authority does not define a closed value universe or a universal exact-content relation for arbitrary Python objects.

Do not send the unchanged U03 problem to another Worker. That would reproduce the same blocker under the corrected process. The minimum next authority decision is to define either:

1. the complete admitted `native_record` value model, including recursive container rules and the exact-content relation for every admitted category; or
2. an alternative authoritative representation/fingerprint carried at ingress that makes same-occurrence exact-content comparison decidable without inferring provider semantics.

No U04 work is authorised while this remains unresolved.
