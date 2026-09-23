# Review-cycle request

## Cycle identity

- **Cycle:** `WORKER_VI12R_U03_R025_REPAIR_1790140749`
- **Current actor:** `WORKER`
- **Predecessor review cycle:** `TESTER_VI13R_U03_R025_1790139709`
- **Reviewer-025 disposition:** `FAIL / RETURN_TO_WORKER`
- **Reviewer-025 disposition commit:** `04daa3c20773680bfab97a747e88778f276e188e`
- **Rejected U03 candidate:** `7cf8936f854fbed952a468ce06c2f2a0320d9291`
- **Rejected U03 candidate tree:** `b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`
- **Accepted/promoted U02 main:** `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- **Open finding:** `R025-U03-F001`

## Authorised task

Execute the smallest bounded IWO-U03 repair required to close **only `R025-U03-F001`**. Do not
begin or assess U04.

The concrete defect is in same-occurrence retry comparison. The rejected candidate uses ordinary
Python/dataclass equality, which treats native numeric content such as `int 1` and `float 1.0` as
equal and also treats `Decimal("1.0")` and `Decimal("1.00")` as equal. Under the same observation
identity, those changed native payloads are therefore accepted as idempotent rather than rejected
as conflicting content, and the first representation is silently retained.

Required repair outcome:

1. preserve accepted U01/U02/U03 public semantics and the bounded owner boundary;
2. make same-occurrence retry equality preserve exact native numeric runtime type and the native
   representation distinctions already admitted by U03, including Decimal tuple/scale;
3. retain idempotency for separately reconstructed genuinely identical content;
4. add the smallest implementation-coupled U03 regression that closes the concrete Reviewer-025
   escape without opening speculative proof growth;
5. do not invent provider duplicate/retransmission equivalence, broaden provider validity rules,
   implement U04, add persistence/replay or activate downstream capability.

## Branch / history law

Preserve Git ancestry. Create a fresh repair branch from the Reviewer-025 FAIL continuity state;
do not squash, rebase or rewrite history. Keep the repair bounded to the U03 owner/proof paths
required by `R025-U03-F001`.

## Required validation and handoff

Run the proposition-bearing U01+U02+U03 proof plus current architecture/static controls on the
frozen repaired candidate. Preserve exact commit/tree/changed paths and focused regression result.
Then create a fresh `TESTER_...` cycle for independent U03 re-review. U04 remains prohibited until
repaired U03 receives PASS and is lawfully promoted.
