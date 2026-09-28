# VI-14-L1 — Independent Tester disposition

**Date:** 2026-09-28
**Role:** fresh independent `TESTER`
**Reviewed candidate:** `076f1e979474babbb8985dc87d3b2d4d62ec0b4c`
**Candidate tree:** `45aec5c01ae8a35fa8879fab978c6fb0f0082140`
**Disposition:** `PASS`

## 1. Exact review boundary

The Tester reviewed the exact VI-14-L1 Worker candidate, not the later handoff branch tip.
The candidate parent/routed source is `00ca26815bc217b7fd4bb98a73eb2089caf94919`.
The candidate changes exactly one path:

- `implementation/proof/VI14_L1_INTEGRATED_REAL_BOUNDARY_CANDIDATE_EVIDENCE.md`.

No `src/**`, `tests/**`, `config/**` or `pyproject.toml` bytes changed in the candidate. No substantive
post-candidate drift exists through the received branch tip.

Git ancestry independently established that the accepted U06 candidate `8462630...`, U06 Tester PASS
`5627675...`, U06 close-out `ed94f74...` and VI-14 routed parent `00ca268...` are ancestors of the exact
VI-14 candidate.

## 2. Governing authority and source trace

The Tester read the mandatory governance/routing material, accepted BICP/IRB/IWO, Worker VI-14 evidence,
accepted U05/U06 Tester evidence, and the realised A00/M00/PostgreSQL source and proposition-bearing proof.
The recorded BICP/IWO SHA-256 identities match the Worker evidence exactly.

Independent source/configuration trace established:

- production A00 construction uses the M00 public seam and the one declared private technical PostgreSQL
  constructor exception;
- A00 holds the M00 owner and delegates the Raw Signal sequence through M00 command/read facets;
- A00 contains no Raw Signal assessment outcome selection and no SQL/table/repository write path;
- no reverse `M00 -> A00` source dependency was found;
- PostgreSQL remains a technical persistence mechanism behind the M-owned persistence port;
- configured runtime owner edge remains exactly `A00 -> M00`;
- P01/DMPV3, K01, authoritative replay, provider/network integration and downstream consumers remain
  excluded/inactive rather than silently activated.

## 3. Independent proof environment

A fresh proof environment was reconstructed from the preserved offline bootstrap and PostgreSQL runtime and
verified as:

- CPython `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PostgreSQL `17.9`, UTF8;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- Unix-domain-socket transport with empty `listen_addresses`.

The bootstrap intentionally omits PyYAML. PyYAML `6.0.3` from the already-present Python 3.13 installation
was exposed only as the missing runtime dependency while the preserved proof virtualenv remained first.
Repository bytes were unchanged.

## 4. Independent executable evidence

The Worker's single 66-case command exceeded the available command window during this review without
emitting an assertion failure. It is not counted as a completed pass. The Tester collected the exact U05
node set and executed it in bounded groups, then executed the remaining VI-14 integration files.

Observed exact-candidate results:

- heavyweight real-PostgreSQL U05 product family: **55/55 passed**;
- remaining U06 A00 composition + U05 whole-restart + U06 real-PostgreSQL composition: **11/11 passed**;
- total VI-14 proposition-bearing integrated set: **66/66 passed**;
- product-proof control: **PASS**, six admitted physical product families, **13/13** product obligations;
- architecture/bootstrap: **74/74 passed**;
- architecture structural validation: **PASS**;
- dependency direction/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- mypy: **success, 16 source files**;
- Ruff: **PASS**;
- candidate diff check: **PASS**;
- `git fsck --full`: exit `0`; seven dangling blobs were diagnostic only and no integrity failure occurred.

The U05 execution included the admitted process/filesystem boundary, PostgreSQL database-clone transfer,
public-return commit acknowledgement, kill-immediately-after-success durability, fresh-process readback,
restart reconciliation, persistence-capability-bypass and boundedness discriminators. None was skipped or
xfail in the completed 55-node run.

## 5. Fixture-independent production public-seam challenge

The Tester constructed policy and observation values directly from the public API without using the Worker
support fixture, created A00 through `create_application(postgres_dsn=...)`, and exercised the production
policy -> capture -> observation -> relation -> assessment -> referential-read sequence.

Observed:

- assessment outcome: `one_or_more_received`;
- referential observation readback exactly matched the submitted observation;
- durable row counts after the first sequence: `(1, 1, 1, 1)`;
- a fresh production application repeated the same sequence with identical semantic result and no duplicate
  durable rows;
- conflicting reuse of the durable observation identity failed closed with
  `observation occurrence identity is already admitted with different content` and row counts remained
  `(1, 1, 1, 1)`;
- a mismatched caller policy reference failed before capture progression with
  `scope_policy_ref must identify the policy accepted for this sequence`, with durable row counts unchanged.

This independently bears on production composition, committed durable identity, fresh-owner readback,
idempotent retry, conflicting-content failure and caller-policy binding.

## 6. Boundedness

No evidence or source trace established any claim of cross-kind atomicity, exactly-once provider semantics,
authoritative replay/equivalence, retention/deletion/recovery policy, bounded raw-loss recovery,
availability/latency/throughput, SLA, RTO/RPO, provider/network integration, external effects/accounts,
P01/DMPV3, K01, downstream consumer semantics or final package identity/version.

The current implementation/proof explicitly keeps those claims absent, excluded, inactive or deferred.

## 7. Disposition

`PASS`.

No material VI-14-L1 defect was established. No recurrence classification is opened because there is no
Tester finding to return.

The exact candidate `076f1e979474babbb8985dc87d3b2d4d62ec0b4c` / tree
`45aec5c01ae8a35fa8879fab978c6fb0f0082140` is independently accepted for preserved-ancestry VI-14-L1
promotion/close-out only. VI-15 remains prohibited until that promotion/close-out succeeds and current-state
routing explicitly advances.
