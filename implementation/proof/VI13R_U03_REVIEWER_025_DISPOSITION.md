# VI-13R U03 Reviewer 025 disposition

## Disposition

`FAIL / RETURN_TO_WORKER`

Fresh Reviewer 025 reviewed only IWO-U03 candidate
`7cf8936f854fbed952a468ce06c2f2a0320d9291` / tree
`b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`. U04 was not assessed.

The exact pinned bounded proof is green at U01+U02+U03 **366/366** and current static/Ruff/product/
architecture/dependency/public-seam controls remain green, including architecture promotion 74/74.
One material realised U03 implementation/proof defect remains.

## R025-U03-F001 — retry equality collapses exact native numeric content

**Status:** `OPEN` / Critical.

IRB BC-005 requires native content fidelity; BC-009 requires conflicting same-ID payload to fail
closed; BC-010 allows same occurrence identity to retry idempotently only for identical content.
The active U03 review contract also explicitly requires exact native numeric runtime-type fidelity.

The candidate implements retry conflict detection as ordinary dataclass equality (`existing != value`).
That equality uses Python numeric equality inside the native-record Mapping. Two public U03 canaries
therefore defeat the contract:

- same observation ID with native `int 1`, then native `float 1.0`: payloads compare equal; the
  conflicting retry is accepted and the first `int` is silently retained;
- same observation ID with `Decimal("1.0")`, then `Decimal("1.00")`: payloads compare equal despite
  distinct exact Decimal tuples/scales; the retry is accepted and the first representation is
  silently retained.

This collapses distinctions that U03 itself treats as fidelity-bearing and permits conflicting
content to masquerade as an idempotent retry.

**Owning layer:** U03 M-owner implementation plus bounded implementation-coupled U03 proof.

**Smallest repair:** make same-occurrence retry comparison preserve exact native numeric runtime type
and already-admitted representation distinctions (including Decimal tuple/scale), while retaining
idempotency for separately reconstructed genuinely identical payloads. Add a focused U03 regression
for the concrete escape. Do not invent provider duplicate semantics, broaden native validation,
begin U04, add persistence/replay, or weaken existing proof.

## Gate effect

U03 is not authorised for promotion. U04 remains prohibited pending a bounded repair of
`R025-U03-F001`, a frozen repaired U03 candidate and fresh independent U03 re-review.
