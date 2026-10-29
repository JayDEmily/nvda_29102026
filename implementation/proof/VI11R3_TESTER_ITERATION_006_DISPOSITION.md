# VI-11R3 Tester Iteration 006 Disposition

## Status

`FAIL / RETURN_TO_WORKER`

The independently reviewed candidate is preserved unchanged in Git history and must not be relabelled or resubmitted as a new iteration.

## Reviewed identity

- wrapper: `d50bc2393078b584b722fb2bf4ba692f055c40ad`
- wrapper tree: `212f739dcb218611c89e010a9966b201beb880f1`
- physical proof: `ffcbc64b77b66f96c91926b423622281f125d757`
- physical tree: `7884c38a5edf6a3538bc2acc6a3bc57a079ea888`
- submitted archive SHA-256: `9340562c57ba7fb156676835740ea48195a880d0579604daf7ba55458c05ce0d`

## Governing finding set

Tester Iteration 006 returned nine material proof-adequacy findings, five Critical and four Important:

1. `T006-F001` — PostgreSQL exclusivity: the proof still permits PostgreSQL to act only as a gate/audit participant while semantic durable truth is reconstructed or sourced elsewhere.
2. `T006-F002` — success-after-commit timing: the proof does not yet discriminate API success that becomes externally visible before the command's own durable transaction has committed.
3. `T006-F003` — persistence semantic ownership: semantic decisions can still hide in a technical persistence path not reached by the existing static mechanism-closure proof.
4. `T006-F004` — `.v1` compatibility `**kwargs` bypass: a constructor can accept unproved extra material through a variadic keyword boundary while the shape checks still pass.
5. `T006-F005` — missing observation authority: the relation proof lacks the typed-but-nonexistent observation-reference negative corresponding to the existing capture-reference check.
6. `T006-F006` — capture-local assessment evidence: evidence attached to one capture can still be allowed to influence the assessment of a different capture.
7. `T006-F007` — restart-persistent invariants: restart proof does not yet jointly establish persisted policy/capture/assessment constraints and per-scope ingestion high-water behaviour across fresh processes.
8. `T006-F008` — restart assessment readback: the recovered assessment is not compared as a complete exact record after restart.
9. `T006-F009` — exact half-open/time-grid boundaries: the physical surface is incomplete at exact slot start, one-microsecond-before-end, and microsecond grid-edge cases.

These labels and summaries are the controlling repair set for VI-10R4. The proof Worker must repair the physical discriminator, not reinterpret product authority.

## Disposition

All nine findings are owned by VI-10R4 proof repair. No production implementation is authorised. IRB/BICP/IWO/METHOD-006 meaning, product obligations, architecture proof and tier treatment remain unchanged.
