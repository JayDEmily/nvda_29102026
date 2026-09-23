# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U02_R023_REPAIR_1790127347`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U02_R023_1790125061`
- **Reviewer-023 disposition:** `FAIL / RETURN_TO_WORKER`
- **Rejected U02 candidate:** `a77dc596b7cbc3f248097df94d8dd0bef4491bec`
- **Rejected U02 candidate tree:** `1b8672a851f63c1bab8da02fb75de8357e4fad3c`
- **Accepted/promoted U01 main:** `b806447eb440a016826728af075e714beee23d31`
- **Open finding:** `R023-U02-F001`

## Authorised task

Execute the smallest bounded IWO-U02 repair required to close **only `R023-U02-F001`**. Do not
begin or assess U03.

The observed defect is concrete: `create_owner()` returns public command/read facets carrying the
same ordinary reachable mutable semantic `_state`. Direct mutation can bypass the public overlap
check, forge a second simultaneously active policy, make a capture under it, and erase referential
policy truth.

Required repair outcome:

1. preserve all accepted U01/U02 public semantic behaviour and identity/time/null law;
2. remove ordinary caller-reachable mutable semantic-state capability from the public command/read
   facets so caller code cannot insert/replace/clear owner policy/capture truth outside M-owned
   commands through the observed object-graph path;
3. add bounded implementation-coupled U02 proof that closes the concrete Reviewer-023 bypass;
4. preserve existing overlap, slot, idempotency and referential-read semantics; do not weaken tests;
5. do not add U03 provider-observation behaviour, persistence, replay or downstream capability.

Exact internal decomposition remains implementation freedom. The repair need not claim prevention
of arbitrary metaprogramming, `eval`/`exec` or runtime monkey-patching; it must close the ordinary
mutable capability actually exposed by the rejected candidate and avoid an equivalent trivial
rename of that capability.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-023 FAIL continuity state;
do not squash, rebase or rewrite history. Keep the repair bounded to the owning implementation and
proof paths required by `R023-U02-F001`.

## Required validation and handoff

Run the proposition-bearing U01+U02 proof and current architecture/static controls on the frozen
repaired candidate. Preserve exact commit/tree/changed paths and the concrete bypass regression
result. Then create the next fresh `TESTER_...` cycle for independent U02 re-review. U03 remains
prohibited until repaired U02 receives PASS and is lawfully promoted.
