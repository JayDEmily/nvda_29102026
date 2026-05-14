# Sequence 9 HOLD repair authority reconciliation report

The expanded read-set pass covers candidate-source governing docs, Atlas surface slices, prior Sequence 1–7 source-tree ledgers/reports, Sequence 8 external aggregate artefacts/reports/proofs, downstream/capital authority evidence surfaces, DMP packet surfaces, coefficient/modifier surfaces, temporal/context surfaces, parallel/final risk surfaces, tests/specimens, and present legacy downstream/capital surfaces.

Exact Sequence 8 ledgers/reports are not present under `var/audit/ledgers/sequence8*` or `var/audit/reports/sequence8*` inside the Sequence 9 candidate source tree. They are hard-missing from the source tree but satisfied by the authoritative external Sequence 8 aggregate pack included in the read ledger.

## Reconciliation result

The existing Sequence 9 implementation remains lawful after the completed read-set pass:

1. `CapitalDeploymentAuthority` remains downstream/pre-deployment and does not rewrite the serial cognition spine.
2. It consumes serial candidate metadata, parallel/final risk envelope state, coefficient/modifier floor information, and temporal context.
3. Parallel/final risk block dominance remains first in decision precedence.
4. Serial confidence remains auditable metadata and is not used as position size.
5. DMPV3 integration remains a downstream packet emission with `packetrole=capital_deployment_decision` and `dataschema=urn:nvda:schema:capital_deployment_authority.decision:1.0.0`.
6. No brokerage execution was added.
7. No Sequence 10 work was opened.

## Coefficient-floor proof

The HOLD repair adds a reachable branch test using `requested_deployable_pct=1.0`, `coefficient_min_deployable_floor_pct=2.0`, and `max_deployable_pct=10.0`. This preserves the validator constraint while proving the `coefficient_floor_not_satisfied` reduction branch.
