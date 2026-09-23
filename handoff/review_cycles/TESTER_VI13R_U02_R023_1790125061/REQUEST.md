# Review-cycle request

## Cycle identity

- **Cycle:** `TESTER_VI13R_U02_R023_1790125061`
- **Current actor:** `TESTER`
- **Predecessor Worker cycle:** `WORKER_VI12R_U02_1790119179`
- **Accepted/promoted U01 main:** `b806447eb440a016826728af075e714beee23d31`
- **U02 candidate:** `a77dc596b7cbc3f248097df94d8dd0bef4491bec`
- **U02 candidate tree:** `1b8672a851f63c1bab8da02fb75de8357e4fad3c`
- **Worker branch:** `work/vi12r-u02-capture-policy-owed-slot`

## Authorised task

Act as fresh independent Reviewer 023 under VI-13R. Review **IWO-U02 only** against the accepted
IRB/IWO, bounded U02 proof, accepted U01 public contract and the actual committed implementation.
Do not begin or assess U03.

Independently determine whether the candidate conserves:

- immutable capture-scope policy-version meaning;
- exact UTC `:00` / `:30` activation/deactivation/slot alignment;
- at most one active policy version at an instant in this slice;
- exact 30-second `[start,end)` owed-slot truth;
- no owed slot before activation or at/after deactivation;
- stable `(scope_policy_ref, slot_start_utc)` retry identity distinct from opaque capture ID;
- same-identity idempotency versus conflicting reuse failure;
- referential U02 reads and preservation of accepted U01 identity/seam law.

Challenge the realised implementation for concrete U02 defects under the current bounded-proof
methodology. Do not reopen an implementation-independent hypothetical proof-hardening loop. Do not
weaken accepted tests or semantics to obtain green.

Return exactly one disposition: `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

If PASS, record that U02 may be promoted and that U03 becomes authorised **only after** lawful U02
promotion to forward `main`; create the next `WORKER_...` cycle accordingly. If FAIL, identify the
exact defeated accepted proposition and smallest owning-layer repair, keep U03 prohibited, and
create the appropriate Worker repair cycle.

Preserve disposition/evidence in this cycle and Git. Return a full-Git TAR.
