# M00 Brief 2 — baseline and bounded admission scope

Independent L00 inspection by `/root/l00_authority_review`, 27 October 2026. Source baseline: `bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc`. This document records source/evidence inspection, not new M00 runtime correctness.

## Authority and lineage

Read full root GUARDRAILS, AGENTS, EXEC_PLAN, tests/AGENTS.override; original Brief 2; Implementation Authority Ingress; Ownership and Component Law; IRB BC-001–016; original M00 SQLite proof contract and SQLite proof-admission addendum; M00 SQLite proof review; G5.1 final review, closeout and owner acceptance. Read full affected current source `api.py` (2042 lines), `_sqlite.py` (513), `_native_codec.py` (179). Other source and old test inspection is partial; no claim of exhaustive historical product review is made.

Original Brief 2 remains SHA-256 `0d5ee211c1285b31834062ab2d871670ed2f318cbb955e7df95f80067d562007`. Current execution reference is `owner-chat/20261027/M00-Brief2-execute-all-leaves`, recorded in EXECUTION_COMMISSION.md and the separate M00/G01 binding. Binding mechanics establish byte/target association; the user's commission supplies authority.

Original SQLite admission history is `895d8f8` → `37e3cec` → `5de245d`; current generation3 SHA-256 is `51e87129c2a31c71599b7a01beb8ba39717ed5118a4d5c849bcb2015b6c80c6f`. Its original brief/binding/contract hashes are respectively `3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233`, `7c7fa7df69e75825853bf7b355343d9b6f793beab247b37223bfa71737248b87`, and `70a6a0e0d216ef3b6eb3b600b72880dc8dd159215ec761e391eeaf2c1148706f`.

Proof adequacy lineage includes 819b49f after recurrent signature/commit-correspondence repairs, generation2 driver review at64b292e, and generation3 integer witnesses at2902c1d. G5.1 owner acceptance identifies delivered candidate `68d3c2fbb263403a36f215696e45872505b2a340`, reference `owner-chat/20261019T202718/G5.1-accept-G5.2-only`. Its independent final review expressly did not independently re-review the integer implementation repair; separate changed-proof adequacy and author verification are retained. Do not enlarge that historical acceptance.

Current M00 source differs from that accepted G5.1 candidate by six api.py additions at D139 (`6d6654e`): datetime native carrier, UTC snapshot validation and exact equality. SQLite/codec bytes are unchanged in that comparison. Neither D143 nor bc02a472 is the original M00 freeze. Old baseline evidence remains historical scoped evidence, not native Brief 2 certification.

## Current source observations and proof boundary

Observation admission retains immutable identity/full-content retry and rejects strictly decreasing per-scope sequence; equal sequence is allowed. Receipt-only rejects non-null source timestamp. Native facts remain distinct from receipt/order metadata. Projection needs exactly one matching provider/variant/R mapping and projects missing paths as absence. History filters receipt/event cutoffs and sorts `(receipt,scope,sequence,occurrence ID)` with offset pagination. Its built-in selectors do not replace the explicit selection-identity checks required by this brief.

Public reads expose known-ID observations and projected R history. They expose no general observation/control enumeration. Private transaction received-between enumeration exists; it cannot substitute for public control proof. L04 must reach the direct discovery witness and independently approve any additive read contract before implementation.

SQLite commands commit their own technical transactions; ordinary reads use `mode=ro` and `query_only=ON`. `create=False` construction still validates the store using a write-capable `mode=rw` connection before closing it; distinguish that constructor step from the subsequent read-only transactions. Fresh-process/public-read persistence proof remains future work.

Static compatibility risk: api.py admits UTC datetime native values, while `_native_codec.py` contains no datetime encode/decode tag. This is a source observation, not an executed failure. L02's valid R001 collector-receipt carrier must establish the public SQLite witness before any repair. Existing positive native price/size specimens do not themselves establish datetime persistence.

No supplemental direct-PUT mandate was found in full IRB or original generic SQLite contract. Brief ten-scenario scope therefore remains 36/155, with PUT in A3/A6 and direct CALL in C3; no full per-right direct-depth claim follows.

## Separate proof admission

The original raw SQLite claim owns `tests/product/raw_signal_sqlite`; unchanged partition law forbids overlapping claim roots. New families use sibling `tests/product/m00_brief2`. The fixed separate `m00_brief2` extension retains existing target/generation/partition/outcome/runner algorithms, exact original-brief SHA, separate M00/G01 binding, and exact existing M00 target. Original catalogue, authority, admissions, generation bytes, schemas and product tests are preserved.

Initial contract owns only the native family; pointer is null and no physical product family or generation is admitted at L00. Later history/control/export families extend the contract in declared order with independent source adequacy review and a new immutable generation/predecessor link before execution. Required fixture/oracle/mapping/schema/export support must be explicitly hash-bound as it materialises. No absent future family, stale source or borrowed generation can certify this work.

Runtime evidence in `../evidence/L00/environment.log` records CPython3.12.14, SQLite3.53.1, pytest9.0.3, mypy1.20.1, Ruff0.15.11 and PyYAML6.0.3; these are inspected worker observations, not independently rerun product evidence. Dependencies were reconstructed offline by the worker. PostgreSQL runtime remains deferred; live IBKR remains unverified. No product execution or production changes occurred in this independent review.
