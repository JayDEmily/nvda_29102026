# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_1790138454`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U02_R024_1790131803`
- **Reviewer-024 disposition commit:** `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c`
- **Reviewer-024 disposition tree:** `bcca17d646b67c27e76197c486324e69c688c648`
- **Reviewer-024 disposition:** `PASS`
- **Accepted repaired U02 candidate:** `5c62ec5147da718297b251b5a287405ebf3b4755`
- **Accepted repaired U02 tree:** `dc1293d2c3d7e234e53a8d663f25eac51f7086ab`
- **Current forward `main` before U02 promotion:** `b806447eb440a016826728af075e714beee23d31`

## Authorised task

Follow root governance and the current `EXEC_PLAN.md` exactly. Execute the next lawful Worker
sequence without widening scope:

1. **Promote accepted U02 first.** Preserve ancestry; do not squash, rebase or rewrite history.
   Promote the accepted repaired U02 candidate together with Reviewer-024 PASS/evidence to forward
   `main`, then verify that both `5c62ec5147da718297b251b5a287405ebf3b4755` and `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c` are ancestors of the resulting
   `main` and that the repository is clean/integrity-valid.
2. **Only after that promotion succeeds, begin IWO-U03.** Create one fresh U03 work branch from that
   accepted forward `main`. Implement only **IWO-U03 — Raw observation admission, native fidelity
   and temporal-kind truth** under VI-12R, preserving accepted U01/U02 meaning.
3. U03 scope is exactly the accepted current IWO section: one actually received provider logical
   record becomes one RawObservation occurrence; separable records remain separate observations
   sharing delivery reference; independent no-scope observation validity; required receipt UTC and
   local sequence/scope; optional genuine nanosecond receipt evidence only; exact
   `true_instant|date_only|receipt_only` law; no inferred provider timezone/event UTC;
   same-occurrence retry versus newly received retransmission identity; and no equal-value/provider-ID
   deduplication. Primary proof obligations are `IA17-PROD-003`, `IA17-PROD-004`, `IA17-PROD-005`
   plus the observation/identity portions of `IA17-PROD-008`.
4. Do **not** begin IWO-U04 or later units, weaken accepted U01/U02 proof, invent provider mappings,
   select unresolved authority values, add persistence/replay/downstream behaviour, or move semantic
   ownership.
5. Run proposition-bearing U03 validation required by the governing plan on committed candidate
   state, freeze exact commit/tree/changed paths/evidence, then create the next opposite-role
   `TESTER_...` cycle for fresh VI-13R review of U03 only.

## Fail-closed conditions

- If accepted U02 candidate or Reviewer-024 PASS cannot be promoted with preserved ancestry, stop
  `BLOCKED`; do not start U03.
- If forward `main` after promotion is not clean/integrity-valid, stop `BLOCKED`; do not start U03.
- If U03 requires an unresolved authority value or a semantic change outside the accepted IWO,
  stop and report the exact blocker rather than selecting a value.
- If `CURRENT_STATE.md`, this cycle prefix, or this request disagree about actor or bound state,
  stop `BLOCKED` rather than guessing.

## Required cycle output

Record Worker results in this cycle's `RESPONSE.md`, `RESULT.json`, `EVIDENCE.md`, `COMMANDS.txt`
and `SOURCE_PACKET.sha256`. Preserve exact promotion and U03 candidate identities. Before stopping,
create the next `TESTER_<...timestamp>/` cycle for fresh U03 review if and only if a lawful U03
candidate has been frozen.
