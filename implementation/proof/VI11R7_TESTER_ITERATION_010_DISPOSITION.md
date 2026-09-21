# VI-11R7 Tester Iteration 010 disposition

## Binding

Fresh independent Tester Iteration 010 reviewed:

- submitted source packet SHA-256 `20d5d9ec8eeb604a576291679fcebd9773aae6f4f308884376d41ab3254c1f92`;
- wrapper `d1b59a898f07c21a2faeca03aae5122f78649dd7` / tree `a70d1f71ce3a2c57e8d8b2040e1626f20ab25d6a`;
- physical proof `816696590912bfac22d9397bef19dc1eb5315f17` / tree `561d8610e98c965d43aac02f296b8cee39f02129`;
- repair/disposition parent `52f6b77bfb96bd72971bbdf83c6b2c731c329271`;
- Tester Iteration 010 response SHA-256 `5e85f8c38f81e59802b31d5bae25180ba5ad46a3d1ab7db48828ef73f4857220`;
- Tester Iteration 010 response-package SHA-256 `587543244b10c4012f30d7722e1352298887b2995b31428592649b56be5b1864`.

The independent verdict is `FAIL / RETURN_TO_WORKER`. VI-12R remains prohibited.

## Prior-finding status

Tester Iteration 010 records:

- `T009-F001` — `PARTIALLY_CLOSED`;
- `T009-F002` — `PARTIALLY_CLOSED`;
- `T009-F003` — `CLOSED`;
- `T009-F004` — `CLOSED`.

The closed typing and Decimal-fidelity discriminators remain part of the active proof and must not be weakened.

## Findings routed to VI-10R8

### T010-F001 — Critical — server COMMIT-ack discriminator is incomplete across durable-success commands

The submitted SyncRep discriminator proves PostgreSQL COMMIT acknowledgement causally precedes public success return only for the raw-observation command. Policy registration, scheduled-capture realisation and assessment append paths are still covered only by the client-tree freeze/kill/readback control. A command-specific implementation could therefore await server acknowledgement for observations while returning early after sending/flushing COMMIT on another durable-success command and still satisfy the existing proof.

### T010-F002 — Critical — record-only graph rewrite misses nested ordinary-container capability capture

The submitted graph rewrite rejects a private adapter method cached directly on an owner attribute but does not descend from an owner attribute into an ordinary container unless that container was already entered by another path. A private bound adapter method cached inside a list/dict or equivalent nested caching form can therefore survive while the direct persistence-port attribute is replaced by the record-only proxy.

## Owning-layer disposition

Both findings are proof-layer defects under `EXEC_PLAN.md` section 6.7. They do not authorise production implementation or any change to IRB/BICP/IWO/METHOD-006 meaning, product obligations, architecture proof configuration or `src/**` production source.

The next lawful action is a genuinely new VI-10R8 physical proof successor that:

1. applies the server-side COMMIT-ack discriminator to every public command path that claims durable success under the current BC-011 proof surface, including both assessment outcomes where execution can differ; and
2. structurally rejects or rewrites concrete/private adapter capability capture through ordinary nested containers and admitted caching forms, with implementation-independent canaries.

Fresh independent Tester Iteration 011 review is required before VI-12R may begin.
