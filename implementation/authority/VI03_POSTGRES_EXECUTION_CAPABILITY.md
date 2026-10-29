# VI-03 — PostgreSQL execution-capability evidence

## Scope

This record establishes only that the current VI execution environment can run a real PostgreSQL server and a Python PostgreSQL client from already-preserved project artefacts. It does **not** select those artefacts as current implementation authority, does not discharge BC-011 / IA22R01-PROD-009, and is not product proof.

## Preserved artefacts

The project attachment consolidation supplied exact preserved runtime/build artefacts including:

- PostgreSQL 17.9 source archive SHA-256 `3b9a62538a8da151e807a3ddb1198e8605f2032544d78f403ae883d27ecf1ee4`;
- `psycopg-3.3.4-py3-none-any.whl` SHA-256 `b6bbc25ccf05c8fad3b061d9db2ef0909a555171b84b07f29458a447253d679a`;
- `psycopg_binary-3.3.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` SHA-256 `c677c4ad433cb7150c8cd304a0769ae3bcfbe5ea0676eb53faa7b1443b16d0d3`;
- preserved Bison/Flex build packages used only to satisfy the PostgreSQL source-build toolchain.

A dated 2026-08-07 historical dependency acquisition pack describes `psycopg[binary]==3.3.4` as the canonical project dependency and contains a snippet saying it was the exact runtime dependency pin approved for the then-current Raw Signal persistence capability. That pack is historical evidence only: the later accepted BICP explicitly preserves PostgreSQL driver selection as a Remaining Unknown, so the pack does not by itself supply current driver authority.

## Build and executable verification

Using the preserved PostgreSQL source plus the available GCC/Make/Perl toolchain and preserved Bison/Flex build artefacts, PostgreSQL was configured locally with:

```text
./configure --prefix=/mnt/data/vi04_pg17 --without-readline --without-zlib --without-icu
```

Targeted build/install produced working binaries:

| binary | observed version | SHA-256 |
| --- | --- | --- |
| `postgres` | PostgreSQL 17.9 | `95feec3bdf06cdb716a5e01f7b53509eb6ce46a59fd76e864bfe52e83d2e60a3` |
| `initdb` | PostgreSQL 17.9 | `ae36abb0570bee42121946b34ae16694bf96c6d7f6e0aa48a460b7117b91d6fa` |
| `pg_ctl` | PostgreSQL 17.9 | `2a4080f9b0c34c7b89eb1a5da28f60a79bd445c3b92f1e2ab995ea14f330a14f` |
| `psql` | PostgreSQL 17.9 | `df9f987565478d767166e5c6d39cfd5aa91c8f0445524587200c20ed6ba17b92` |

The preserved Psycopg wheels were installed into an isolated temporary virtual environment without changing repository dependencies. Observed client state:

```text
psycopg 3.3.4
pq implementation: binary
libpq version reported by client: 180000
```

## Normal local-cluster execution probe

A fresh isolated cluster was initialised outside the repository and started as the non-root `oai` user on a Unix socket only, port `55433`. The probe did not disable PostgreSQL durability settings.

Observed through `psql`:

```text
PostgreSQL 17.9 on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
fsync = on
synchronous_commit = on
full_page_writes = on
current_user = oai
```

Observed through Psycopg 3.3.4:

```text
('17.9', 'on', 'on', 'on', 'oai')
```

The cluster then stopped cleanly and `pg_ctl status` reported no server running.

## Disposition

**VERIFIED:** real PostgreSQL execution is technically available in this environment from preserved project artefacts; lack of a pre-installed system `postgres` binary is not an execution-capability blocker.

**NOT ESTABLISHED / NOT CLAIMED:** PostgreSQL 17.9, Psycopg 3.3.4, any physical schema/type mapping, or any repository/store implementation is current authorised product realisation. Those remain governed by the accepted BICP and VI-04 authority closure.

**NOT PRODUCT PROOF:** this probe establishes executable availability only. Later BC-011 proof must use the exact authorised mechanism and prove the actual transaction/readback/failure/restart propositions against the committed implementation.
