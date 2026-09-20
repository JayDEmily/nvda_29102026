# VI-11R4 Tester Iteration 007 Disposition

## Status

`FAIL / RETURN_TO_WORKER`

The independently reviewed candidate is preserved unchanged in Git history and must not be relabelled or resubmitted as a new iteration.

## Reviewed identity

- wrapper: `30db3d00f1b9f32215ce1f06b156647e92f1e505`
- wrapper tree: `d19d42277c8ed95b1b645edc973d6f0e51e6f629`
- physical proof: `0c626fb78fa7317fa265bd5ff871dd398c68404d`
- physical tree: `df10fd0e42178dfb7e6fabe0fd9a8e3a3a3249f6`
- repair baseline: `4aee3dfde5ff0c9f83a113e5f2fb792f53f22981`
- submitted archive SHA-256: `c320a72735dfa7b7e034b6cbed20372e03e4e97902868300517fb8560cf1ae73`

## Governing finding set

Tester Iteration 007 returned seven material proof-adequacy findings, six Critical and one Important:

1. `T007-F001` — the PostgreSQL proof process can still reach writable durable host paths, so PostgreSQL could remain only a gate/audit participant.
2. `T007-F002` — the durability timing probe observes post-return serialisation rather than the exact public-command return boundary.
3. `T007-F003` — syntactic scanning cannot prove that the technical persistence mechanism is semantically storage-only.
4. `T007-F004` — restart proof lacks same-assessment-ID conflict persistence and A→B→A per-scope ingestion high-water discrimination.
5. `T007-F005` — fail-before-commit non-fabrication does not cover scheduled capture occurrences.
6. `T007-F006` — the one-active-policy law is not challenged with overlapping distinct `scope_policy_id` values.
7. `T007-F007` — the eleven public command/read facets are callable but not physically static-typechecked against cross-layer substitution or `Any` collapse.

## Disposition

All seven findings are owned by successor VI-10R5 proof repair. No production implementation is authorised. IRB/BICP/IWO/METHOD-006 meaning, the six-family decomposition, thirteen current product obligations, architecture proof and tier treatment remain unchanged.
