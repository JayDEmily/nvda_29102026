# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U02_1790119179`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U01_R022_1790117393`
- **Reviewer-022 disposition commit:** `4db58e9091083500a2505023a302f36447185029`
- **Reviewer-022 disposition:** `PASS`
- **Accepted repaired U01 candidate:** `e8b659d7849d2f95b64ba32bed8090a8290358d4`
- **Accepted repaired U01 tree:** `62b074c0e94215a75fb64c5eb934af55be1ded3a`
- **Current forward `main` before U01 promotion:** `95c0aeabf3b76316bd32870ffe6c311be8ad1237`

## Authorised task

Follow root governance and the current `EXEC_PLAN.md` exactly. Execute the next lawful Worker sequence
without widening scope:

1. **Promote accepted U01 first.** Preserve ancestry; do not squash, rebase or rewrite history.
   Promote the accepted U01 candidate together with the Reviewer-022 PASS/evidence to forward
   `main`, then verify that both
   `e8b659d7849d2f95b64ba32bed8090a8290358d4` and
   `4db58e9091083500a2505023a302f36447185029` are ancestors of the resulting `main` and that the
   repository is clean/integrity-valid.
2. **Only after that promotion succeeds, begin IWO-U02.** Create one fresh U02 work branch from that
   accepted forward `main`. Implement only **IWO-U02 — Capture policy and owed-slot truth** under
   VI-12R, using the already-accepted U01 public contract and existing bounded product proof as
   authority/evidence rather than changing their meaning.
3. U02 scope is exactly the current IWO section: immutable policy versions; activation/deactivation
   alignment; at most one active policy version at an instant in this slice; exact `[start,end)`
   30-second slots at nominal `:00`/`:30` boundaries; no owed slot before activation or at/after
   deactivation; and stable `(scope_policy_ref, slot_start_utc)` retry reference distinct from the
   opaque capture occurrence ID. Primary proof obligations are `IA17-PROD-002` plus the identity
   portion of `IA17-PROD-008`.
4. Do **not** begin IWO-U03 or later units, select Remaining Unknowns, weaken existing proof, invent
   provider mappings, add persistence/replay/downstream behaviour, or move semantic ownership.
5. Run the proposition-bearing U02 validation required by the governing plan on committed candidate
   state, freeze exact commit/tree/changed paths/evidence, then create the next opposite-role
   `TESTER_...` cycle for fresh VI-13R review of U02 only.

## Fail-closed conditions

- If accepted U01 candidate or Reviewer-022 PASS cannot be promoted with preserved ancestry, stop
  `BLOCKED`; do not start U02.
- If forward `main` after promotion is not clean/integrity-valid, stop `BLOCKED`; do not start U02.
- If U02 requires an unresolved authority value or a semantic change outside the accepted IWO,
  stop and report the exact blocker rather than selecting a value.
- If `CURRENT_STATE.md`, this cycle prefix, or this request disagree about actor or bound state,
  stop `BLOCKED` rather than guessing.

## Required cycle output

Record Worker results in this cycle's `RESPONSE.md`, `RESULT.json`, `EVIDENCE.md`, `COMMANDS.txt`
and `SOURCE_PACKET.sha256`. Preserve exact promotion and U02 candidate identities. Before stopping,
create the next `TESTER_<...timestamp>/` cycle for fresh U02 review if and only if a lawful U02
candidate has been frozen.
