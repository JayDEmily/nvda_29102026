# Unit 5 — Live Provider and Broker Operational Boundary

## Outcome

PASS for the repository-owned operational boundary. External commissioning remains unproven: no real credential, provider entitlement, broker account, network endpoint, order, fill or live-account state was used or claimed.

## Expected-red state

The admitted proof initially produced eight failures because the live-placement contracts and `nvda_desk.operational_boundaries` package did not exist. After the first implementation, two guardrail failures remained: raw source bytes were incorrectly passed into the semantic canonicaliser, and transport classification masked a missing-credential blocker. Both were corrected without weakening the proof.

## Implemented surfaces

- M10 now forms one `LivePlacementIntent` only from one exact revalidated paper `PlacementIntent` plus an explicit `LivePlacementPolicy`; it cannot change price, quantity, notional, order terms or M09-derived authority.
- `LiveMarketDataAdapter` and `LiveBrokerAdapter` require injected credential resolvers and transports; no default network implementation or service locator exists.
- Offline is the default and the kill switch defaults engaged. Validation accepts only hermetic transports; live mode accepts only network-marked injected transports.
- Missing credentials, provider/broker/account/environment/authorisation mismatch, transport mismatch, endpoint errors and invalid responses are terminal blockers with no retry or paper fallback.
- Secrets are resolved at call time and do not enter contracts, receipts, persistence or fingerprints. Provider raw material is retained and bound by SHA-256 without placing bytes in the semantic canonicaliser.
- Live mode alone does not prove a network effect. Explicit transport acknowledgement is required, and broker acknowledgement still cannot prove execution, fill, portfolio mutation, durable external effect or live-account truth.

## Admitted propositions

`M10-LIVE-001`, `M10-LIVE-002`, `OPS-LIVE-001` through `OPS-LIVE-006`, and `M01-LIVE-001` in `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`.

## Validation

- Unit 5 proof: `10 passed`.
- Affected M10/M00/entry and proof-control run: `138 passed`.
- Proof authority: `PASS families=200 tests=202 blocks=72`.
- Promotion membership check: `19` blocks, `19` families, `21` test paths.
- Black on changed Python: PASS after formatting three branch-owned files.
- Ruff on changed Python: PASS, zero findings.
- `git diff --check`: PASS.

## Ruled out

- M00 remains hermetic and paper-only and does not select the live boundary.
- No real provider or broker client was added.
- No credential value is stored in repository configuration or evidence.
- No validation submitted or attempted a real order.
- No broker acknowledgement is represented as a fill or successful live execution.
- No existing M09, M11 or M13 semantic ownership moved into the adapter package.

## Next gate

Unit 6: admit a separate Tier C route for slow installed, restart, provider-substitution, broker-safety and end-to-end operational assurance.
