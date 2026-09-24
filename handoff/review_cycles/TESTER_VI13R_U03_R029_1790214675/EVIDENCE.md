# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 029 / TESTER
- authorised scope: repaired IWO-U03 only; U04 not assessed
- source transport SHA-256: `de9c6dcbe8cef3fcb31ab2c9141ed949f8bc0ba2349d794917085272ffc5739e`
- exact source transport filename: `NVDA_G03_WORKER_VI12R_U03_R028_REPAIR_R029_HANDOFF_FULL_GIT_20260924.tar(2).gz`
- transported repository HEAD before review: `dd0188aa44c595e51c78f4019122d4a96f272982`
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- Reviewer-027 FAIL: `31b76489b1ec32fa38921bd3f5e97e40f544e23e`
- Worker Reviewer-027 repair: `06735b3682d79387ebaa4da70002e6685d52740a`
- Reviewer-028 FAIL: `d6d58c0a45b439c262cc135b961e9c67b98ac0a8`
- Worker Reviewer-028 repaired candidate under review: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- repaired candidate tree: `21eb6bd2ba53b29ea6d80f90c01af40668f56955`
- candidate-to-handoff material diff over `src tests config tools pyproject.toml`: none

## Governing material inspected

Read before substantive disposition: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, complete
current `EXEC_PLAN.md`, `tests/AGENTS.override.md`, `handoff/control/CURRENT_STATE.md`, active
Reviewer-029 `REQUEST.md`, accepted IRB, complete IWO, Reviewer-028 disposition, Reviewer-028 Worker
repair record, exact repaired diff, repaired `api.py`, complete U03 proof and its public support.
Relevant accepted clauses are BC-005, BC-006, BC-009 and BC-010; primary proof obligations are
IA17-PROD-003, IA17-PROD-004, IA17-PROD-005 and the observation/identity portion of
IA17-PROD-008.

Role consistency is established: `CURRENT_STATE.md`, the active-cycle prefix and active request all
route Reviewer 029 to exact candidate `d25aede...`. The Git sequence independently establishes
`d6d58c0...` as an ancestor of `d25aede...`, and `d25aede...` as an ancestor of handoff
`dd0188a...`.

## Reviewer-028 closure

`R028-U03-F001` is **CLOSED** on the exact candidate.

The repaired comparator now treats `array.array` by exact typecode plus raw element bytes and treats
`range` by exact start/stop/step. The two required public-proof regressions independently pass
**2/2**. The complete U03 proof passes **47/47**, including the earlier int/float, Decimal-scale,
reconstructed NaN idempotency, complex signed-zero, bytes/bytearray and nested mapping-key
int/float cases. Both Reviewer-028 conflict regressions assert that the first admitted record is not
replaced. The Reviewer-028 source diff does not change the separate non-native observation equality
block.

This closes the prior finding; Reviewer 029 does not route the repository back on Reviewer 028's
failure.

## Exact review environment and controls

Validation ran in a detached clean worktree at exact candidate
`d25aedeed5de65d0a241bdce6eae22671ef2ddf8` / tree
`21eb6bd2ba53b29ea6d80f90c01af40668f56955` using:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

Observed controls before the new invariant failure:

- Reviewer-028 focused regressions: **2 passed**;
- complete U03 proof: **47 passed**;
- strict Git integrity: `git fsck --full --strict` exit 0;
- detached candidate worktree: clean.

Per the repository failure-stop law, downstream acceptance/promotion validation was not continued
after the first new material U03 invariant failed. U04 was not executed, assessed or implemented.

## R029-U03-F001 — native datetime representation collapses to instant equality

**Status:** `OPEN` / material U03 implementation defect / Critical.

### Accepted proposition defeated

BC-005 requires provider-native field values to be preserved unchanged. BC-010 and IA17-PROD-008
permit same-occurrence retry reuse only for identical content and require conflicting same-ID content
to reject. The IWO-U03 boundary also forbids inferred source-time normalisation.

The realised `native_record` contract is `Mapping[str, object]` and does not exclude `datetime`
values. `_NativeRecordSnapshot` admits and deep-copies such values. The comparator first enforces
same runtime type but, after its explicit special cases, falls back to ordinary `left == right`.
Python aware-datetime equality compares instants, so two different provider-native timestamp
representations can compare equal.

### Independently reproduced public-seam witness

Reviewer 029 admitted:

- first native value: `2026-09-20T12:00:00+00:00`;
- same-ID retry native value: `2026-09-20T13:00:00+01:00`.

The values have the same runtime type and Python reports them equal, but their native wall-clock and
offset representations differ. The external public-seam canary requires `ValueError` for changed
same-ID content. Observed result:

`Failed: DID NOT RAISE <class 'ValueError'>`.

The candidate therefore accepts the changed retry as idempotent. Readback remains the first
admitted `12:00+00:00` record, so the store is not replaced; the defect is specifically failure to
reject changed native content.

This is a concrete realised U03 defect, not an invented provider-validity or duplicate-equivalence
rule.

## Owning layer and smallest bounded repair

Owning layer: U03 M-owner native retry comparison in
`src/nvda_desk/raw_signal_occurrence_truth/api.py`, plus the implementation-coupled U03 proof.

Smallest bounded repair:

1. make same-type native `datetime` comparison representation-sensitive before the ordinary-equality
   fallback, so wall-clock fields and represented UTC offset/timezone state are not normalised to
   instant equality;
2. add a regression proving same-ID `12:00+00:00` -> `13:00+01:00` rejects and leaves the first
   record unchanged;
3. add or retain a positive reconstruction case proving genuinely identical datetime representation
   remains idempotent;
4. preserve every already-closed numeric/NaN/complex/bytes/mapping/array/range behaviour and the
   existing non-native observation equality semantics.

Do not broaden this repair into provider validity, provider duplicate/retransmission equivalence,
persistence/replay or U04 behaviour.

## Disposition

`FAIL / RETURN_TO_WORKER`.

U03 is not promotable. U04 remains prohibited pending this bounded repair and a fresh independent
U03 re-review.
