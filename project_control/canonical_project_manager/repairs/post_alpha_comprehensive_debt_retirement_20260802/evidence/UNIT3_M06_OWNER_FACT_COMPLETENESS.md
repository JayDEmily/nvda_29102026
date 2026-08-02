# Unit 3 — M06 owner-fact completeness

## Outcome

PASS. M06 now consumes exact owner-issued concentration, inventory and liquidity facts when supplied. Missing, future-dated or stale facts remain explicit `unknown` observations; no safe default or fabricated fact was introduced.

## Implemented

- Added immutable concentration, inventory-stress and liquidity owner-fact contracts with deterministic identity, owner policy/version, UTC validity, exact authority references and copied-model revalidation.
- Added an M11 `PortfolioRiskFactIssuer` binding concentration and inventory measurements to one exact `PortfolioSnapshot` and position lineage.
- Added a read-only `LiquidityFactProvider` protocol that returns one exact M01-admitted fact or `None`.
- Added optional `ParallelRiskOwnerFacts` to `ParallelRiskInput`; existing callers without facts preserve the accepted explicit-unknown behaviour.
- M06 mechanically maps owner conditions to `observe`, `caution` or `block`; it does not recalculate or replace owner limits.
- Added M13 `StateReadPort`/`TransactionalStatePort` and made the in-memory state kernel implement the combined read/transaction boundary, allowing M11 owner reads to be replaced by the durable implementation in Unit 4.

## Expected-red proof

The new Tier A file initially failed during collection because the new owner-fact exports did not exist. It then exposed and drove the exact implementation surface. No xfail, skip or assertion weakening was used.

## Validation

- `tests/tier_a/m06_k10/test_m06_owner_fact_completeness.py`: 6 passed.
- Affected M06/M09/M11/M13/M00 Tier A set: 247 passed.
- Proof-control tests: 30 passed.
- Proof authority: 198 families, 200 physical tests, 70 blocks.
- Black/Ruff on changed Python and proof-control files: passed.

## Remaining truth

Complete owner facts are now representable and evaluable. Their availability is still provider/repository dependent. Unit 4 supplies durable owner state; Unit 5 supplies the concrete operational provider boundary. Absence remains a truthful unknown, not a defect concealment.
