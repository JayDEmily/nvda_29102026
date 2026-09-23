# Review-cycle response

**Status:** `COMPLETE`

**Disposition:** `FAIL / RETURN_TO_WORKER`

Fresh Reviewer 025 independently reviewed only frozen IWO-U03 candidate
`7cf8936f854fbed952a468ce06c2f2a0320d9291` / tree
`b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`.

The bounded U01+U02+U03 suite is independently green at **366/366**, and source/static/Ruff/product/
architecture/dependency/public-seam controls are green, including architecture promotion **74/74**.
Those results do not close one concrete realised U03 defect.

`R025-U03-F001`: same-occurrence retry equality uses ordinary Python/dataclass equality. That
collapses native numeric content that U03 must preserve exactly. With the same observation identity,
a first payload containing native `int(1)` and a retry containing native `float(1.0)` compare equal,
so the retry is accepted instead of rejected as conflicting content. The same failure occurs for
`Decimal("1.0")` versus `Decimal("1.00")`: the candidate accepts the retry and silently retains the
first Decimal representation even though the exact native Decimal tuple/scale differs.

This defeats IRB BC-005 native-value fidelity, BC-009 conflicting-payload rejection, BC-010
same-occurrence idempotency-only-for-identical-content, and the active U03 requirement to preserve
exact native numeric runtime type/representation.

**Smallest owning-layer repair:** U03 M-owner retry comparison plus one bounded U03 regression proof.
Make same-occurrence equality type-sensitive for native numeric content and preserve representation
distinctions already admitted by the U03 fidelity contract (including Decimal tuple/scale), while
retaining idempotency for genuinely identical reconstructed content. Do not add provider duplicate
semantics, U04 behaviour, persistence, replay or downstream capability.

U03 is not promotable. U04 remains prohibited pending a repaired U03 candidate and fresh independent
U03 re-review.
