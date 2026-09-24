# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R029_REPAIR_1790219280`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R029_1790214675`
- **Reviewer-029 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-029 disposition commit:** `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`
- **Rejected repaired U03 candidate:** `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`
- **Rejected repaired U03 candidate tree:** `21eb6bd2ba53b29ea6d80f90c01af40668f56955`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Reviewer-028 finding status:** `R028-U03-F001` — `CLOSED`
- **Open Reviewer-029 finding:** `R029-U03-F001`

## Authorised task

Execute the smallest bounded IWO-U03 repair required to close **only `R029-U03-F001`**. Do not
begin or assess U04.

Reviewer 029 independently established that `R028-U03-F001` is closed: both required `array.array`
and `range` same-ID conflicts reject, the first admitted record remains intact, and the complete U03
proof is 47/47 green including all earlier numeric/NaN/complex/bytes/mapping exactness cases.

The new defect is confined to native retry equality for admitted aware `datetime` values. The
current generic fallback uses ordinary Python equality after runtime-type matching. Python aware
`datetime` equality compares represented instants, so the following changed provider-native content
is wrongly accepted as idempotent under the same observation occurrence ID:

- first: `2026-09-20T12:00:00+00:00`;
- retry: `2026-09-20T13:00:00+01:00`.

The two values have the same runtime type and denote the same instant, but their provider-native
wall-clock/offset representation differs. Reviewer 029's public-seam canary required rejection and
failed with `DID NOT RAISE <class 'ValueError'>`. The first record remained stored; the defect is
failure to reject changed same-ID native content.

Required repair outcome:

1. preserve accepted U01/U02/U03 public semantics and the bounded owner boundary;
2. retain every already-closed retry behaviour, including int/float, Decimal scale, reconstructed
   NaN, complex signed zero, bytes/bytearray, nested mapping-key type, `array.array` typecode/content
   and `range` bounds;
3. make admitted same-type native `datetime` retry comparison representation-sensitive enough that
   the verified `12:00+00:00` -> `13:00+01:00` change rejects rather than being normalised by instant
   equality;
4. prove the rejected retry does not mutate or replace the first admitted record;
5. preserve idempotency for an independently reconstructed native `datetime` with genuinely
   identical representation;
6. preserve existing non-native observation-field equality semantics;
7. add only the smallest implementation-coupled U03 regressions needed for the verified finding;
8. do not invent provider validity, duplicate/retransmission equivalence, broaden U04 behaviour,
   add persistence/replay or activate downstream capability.

Relevant authority remains IRB BC-005, BC-006, BC-009 and BC-010 plus IWO-U03 and
IA17-PROD-003/004/005 and the observation/identity portion of IA17-PROD-008.

Do not close the finding by excluding `datetime` from `native_record` unless new accepted authority
expressly requires such a restriction; the realised contract currently admits `Mapping[str, object]`.
Do not broaden the repair into a speculative universal object-identity framework.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-029 FAIL continuity state; do
not squash, rebase or rewrite history. Keep physical repair bounded to the U03 owner/proof paths
required by `R029-U03-F001`.

## Required validation and handoff

Run the proposition-bearing U01+U02+U03 proof plus current architecture/static controls on the frozen
repaired candidate. Preserve exact commit/tree/changed paths and focused regression results. Then
create a fresh `TESTER_...` cycle for independent U03 re-review. U04 remains prohibited until repaired
U03 receives PASS and is lawfully promoted to forward `main`.
