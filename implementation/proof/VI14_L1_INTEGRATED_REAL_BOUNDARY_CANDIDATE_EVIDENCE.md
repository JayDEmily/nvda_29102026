# VI-14-L1 — Integrated Material Interaction / Direct-Boundary Worker Candidate Evidence

## Status

`WORKER CANDIDATE — PENDING FRESH INDEPENDENT TESTER REVIEW`

This record closes only the Worker side of VI-14-L1 under the accepted root `EXEC_PLAN.md`.
It does not claim VI-14 acceptance, promotion, VI-15 authority, package finality, broader NVDA
completion, production commissioning, provider integration, replay, recovery SLA, RTO/RPO, or
cross-kind atomicity.

## Governing boundary

- active plan: root `EXEC_PLAN.md`, Programme Owner accepted 2026-09-28;
- accepted BICP JSON SHA-256:
  `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- accepted BICP Markdown SHA-256:
  `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`;
- accepted IWO JSON SHA-256:
  `a673ff05bc58870fdfca49167482aabe4647889d7750fd1b49805c7064ef7eed`;
- accepted IWO Markdown SHA-256:
  `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e`;
- accepted/promoted U06 close-out predecessor: `ed94f745effd65050f03d921ad0ae30769877206`;
- independently accepted U06 candidate: `8462630277b04d431ad393e2b73039cacb5d6247` /
  tree `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`;
- independent U06 Tester PASS / review identity:
  `562767529235cedff77d3e740a259fab9d88716e`;
- VI-14/VI-18 accepted plan integration: `6d1420b6e0245fc3f61bda8aaa5510ff3c7afae2`;
- VI-14-L1 routed branch base / Worker handoff: `00ca26815bc217b7fd4bb98a73eb2089caf94919` /
  tree `cb5bf7a00b58ac25ce36be2957c7cf5069164ff0`;
- branch: `work/vi14-l1-integrated-real-boundary-closure`.

The routed state descends from the exact accepted U06 candidate and independent U06 Tester PASS.
There is no substantive `src/**`, `tests/**`, `config/**`, or `pyproject.toml` drift between the
accepted U06 candidate `8462630...` and the routed VI-14-L1 state.

## Historical VI-14 proposition and current classification

The historical VI-14 authority required material/heavyweight real-boundary closure for A00/M00,
PostgreSQL durability/restart/readback and the admitted sequential composition. The accepted current
ExecPlan requires each proposition to be classified before executing only the smallest genuinely
missing integrated proof.

| VI-14 proposition | Classification before current execution | Primary accepted evidence | Current integrated closure |
| --- | --- | --- | --- |
| A00 production construction/injection | `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE` | U06 Stage 4 candidate + Stage 5 Tester PASS | Re-exercised by U06 product proof and real PostgreSQL Stage-3 composition test |
| declared runtime dependency exactly `A00 -> M00` | `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE` | architecture registry + U06 independent review | Revalidated by architecture/dependency tools and U06 proof |
| typed M-owned command/read public boundary | `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE` | accepted U01 seam + U06 review | Public-seam validator PASS; U06 proof exercised only M00 command/read facets |
| no reverse `M00 -> A00` dependency | `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE` | U06 Stage 4 source trace + Tester trace | Current source search found no `nvda_desk.composition` import under M00; dependency validator PASS |
| PostgreSQL remains non-owning mechanism behind M-owned persistence authority | `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE` | U05 durability family + U06 Stage 4/5 object-graph review | Revalidated by U05 real-PostgreSQL durability family and current source/architecture trace |
| real transaction/readback/failure semantics | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | accepted U05 55-case real-PostgreSQL family | Re-run in current integrated 66-case VI-14 set; green |
| restart reconciliation from committed durable state | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | accepted U05 restart/whole-restart evidence | Re-run via U05 product durability family and Stage-5 whole-restart discriminator; green |
| referential readback | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | U05 durability/restart + U06 production composition evidence | Re-run through U05/U06 current integrated set; green |
| required sequential/end-to-end A00 -> M composition | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | U06 Stage 3 real PostgreSQL composition + independent Stage 5 challenge | Re-run production A00 -> PostgreSQL-backed M00 sequence; green |
| process/namespace/isolation propositions bearing on realised durability | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | admitted U05 family process/chroot/fresh-process cases | Entire admitted U05 durability family re-run; green |
| no overclaim of cross-kind atomicity, SLA, RTO/RPO, recovery or replay | `REQUIRES_CURRENT_INTEGRATED_REVALIDATION` | IWO-U05 nonclaims + admitted U05 prohibited-false-positive case | Current U05 family re-run includes the explicit non-overclaim discriminator; architecture exclusions remain unchanged |

No VI-14 proposition remained `UNPROVED` or `BLOCKED` after the current integrated execution recorded
below.

## Realised source / architecture trace

The Worker traced the current accepted source rather than relying only on historical receipts.

### A00 -> M00 construction and public-seam path

Current `src/nvda_desk/composition/__init__.py`:

1. imports the M00 semantic contracts and `create_owner` from the declared public seam
   `nvda_desk.raw_signal_occurrence_truth.api`;
2. uses exactly one private/technical exception,
   `nvda_desk.raw_signal_occurrence_truth._postgres.create_postgres_persistence`, matching the
   declared architecture public-seam exception;
3. production construction rejects caller owner-factory substitution when a PostgreSQL DSN is
   supplied;
4. constructs the technical persistence mechanism and injects it into M00 `create_owner`;
5. stores only the M00 owner on the A00 application object;
6. orchestrates the accepted policy -> capture -> observation -> optional relation -> assessment ->
   referential-read sequence through M00 `commands` and `reads`;
7. returns the exact semantic objects returned by M00 and contains no Raw Signal assessment outcome
   selection logic.

### Architecture state

Current architecture configuration declares:

- active semantic owner: `M00` / `nvda_desk.raw_signal_occurrence_truth`;
- public seam: `nvda_desk.raw_signal_occurrence_truth.api`;
- A00 permitted dependency: `M00`;
- declared owner edge exactly `A00 -> M00`;
- one A00->M00 private import exception only for
  `nvda_desk.raw_signal_occurrence_truth._postgres.create_postgres_persistence`;
- M00 state-writer boundary: M00 command/service boundary through the M00 persistence port;
- A00 and PostgreSQL/SQL/driver/adapter are prohibited semantic state writers;
- P01/DMPV3, K01, provider/network integration, authoritative replay, downstream consumers and
  recovery/SLA/performance semantics remain excluded/inactive.

A current source search found no import of `nvda_desk.composition` under
`src/nvda_desk/raw_signal_occurrence_truth/**`.

## Exact current integrated proof environment

The preserved U05 proof-environment bootstrap and separately preserved PostgreSQL runtime were
verified and reconstructed fresh for this VI-14 Worker execution.

Observed live identities/settings:

- CPython `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`;
- server encoding `UTF8`;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- `listen_addresses` empty — Unix-domain socket proof transport;
- current proof session `TimeZone=Etc/UTC`.

The preserved proof bootstrap deliberately omits PyYAML. For U06/architecture collection, the
execution kept the exact proof virtualenv site-packages first and exposed the already-present
PyYAML `6.0.3` installation as the missing dependency. This did not change repository bytes or the
pinned pytest/Psycopg/Ruff/mypy identities.

## Current integrated VI-14 execution

The proposition-bearing current integrated set was executed against the routed VI-14-L1 branch:

```text
pytest -q \
  tests/product/raw_signal/test_u05_postgresql_durability.py \
  tests/product/raw_signal/test_u06_a00_composition.py \
  tests/implementation/raw_signal/test_u05_stage5_whole_restart.py \
  tests/implementation/raw_signal/test_u06_stage3_postgresql_composition.py
```

Observed result:

- **66 passed**;
- one Python multiprocessing/fork deprecation warning;
- no assertion failure, skip, xfail or degraded substitute was used for the required axes.

This execution combines the admitted U05 heavyweight real-PostgreSQL/process boundary family with
current A00/M00 public-seam composition and the whole-restart / real-production-composition
regressions. It directly exercises the current accepted source bytes rather than treating historical
PASS receipts as sufficient by themselves.

## Current structural/static validation

Observed current results:

- product-proof control validation: **PASS**, six admitted physical product families, 13/13 product
  obligations covered;
- architecture structural validation: **PASS**;
- dependency direction/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- architecture/bootstrap: **74/74 passed**;
- mypy over `src`: **success, 16 source files**;
- Ruff over `src tests tools`: **PASS**;
- `git diff --check`: **PASS** before candidate evidence authoring.

The first architecture/bootstrap attempt reached one environment-only failure because Git rejected
the extracted repository path as dubious ownership inside a subprocess. After adding this exact
extracted path to Git's safe-directory configuration, the unchanged repository reran at 74/74. No
repository test/assertion was changed or weakened in response.

The first combined U05/U06 run likewise stopped during collection because the proof bootstrap omits
PyYAML. It was rerun with the exact proof venv retained first and PyYAML 6.0.3 exposed as the missing
runtime dependency; the unchanged repository then passed 66/66. No semantic result is claimed from
the failed collection attempt.

## Nonclaims / boundedness

VI-14-L1 does not establish or claim:

- cross-kind transaction atomicity;
- exactly-once provider semantics;
- authoritative replay or replay equivalence;
- retention/deletion/recovery policy;
- bounded raw-loss recovery;
- availability, latency, throughput or operational fitness;
- SLA, RTO or RPO;
- provider/network integration or external effects/accounts;
- P01/DMPV3 or K01 activation;
- downstream consumer semantics;
- final package distribution name/version;
- production PostgreSQL version requirement (17.9 is the proof environment only).

These remain excluded, inactive, unresolved or deferred according to the accepted BICP/IWO and
current ExecPlan.

## Worker disposition

**VERIFIED:** the current accepted U01-U06 implementation and architecture state satisfies the
Worker-side VI-14-L1 integrated material interaction/direct-boundary proposition under the evidence
recorded above, with no current production/source repair required.

**UNPROVED:** independent VI-14-L1 Tester acceptance. The Worker does not self-award VI-14 PASS.

**BLOCKED:** none identified for VI-14-L1 Worker closure.

**NOT_IN_SCOPE:** VI-15 and all downstream leaves.

The lawful next action after candidate freeze is a fresh independent Tester review of the exact
VI-14-L1 candidate under `EXEC_PLAN.md` section 6. On Tester PASS only, the accepted VI-14 lineage
may be promoted to `main` and VI-15-L1 may begin.
