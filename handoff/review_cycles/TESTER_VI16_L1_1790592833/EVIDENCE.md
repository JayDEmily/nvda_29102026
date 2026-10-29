# Tester evidence

**Status:** `COMPLETE`

## Binding

- cycle: `TESTER_VI16_L1_1790592833`
- role: fresh independent `TESTER`
- leaf: `VI-16-L1 — whole-BICP semantic closure`
- received handoff SHA-256: `f1e4e0d8e8099f7f6b9dfd82481c8086c4d7132e08ebc0544caed8188c7c0abb`
- exact candidate: `9248f3b1788f8e99e59a0482c4cc393c27942715`
- candidate tree: `5560c97ad83a05190603c323eb4fbfa0c21d983d`
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`
- accepted wheel SHA-256: `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- accepted sdist SHA-256: `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`

The review used a detached worktree at the exact candidate. The later handoff/routing commit was not treated as
candidate implementation. There is no `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift from the accepted
VI-15-L2 package candidate to the VI-16 candidate.

## Authority rebinding and lineage

The exact BICP, IRB and IWO hashes match the accepted identities in the active ExecPlan. VI-04 still fixes the M00
package/public seam, Psycopg 3.3.4 and bounded PostgreSQL implementation delegation; VI-15 fixes final distribution
metadata exactly to `nvda-architecture-kernel==1.0.0` and does not close other Remaining Unknowns.

The recorded accepted U01-U06 implementation/review lineage, VI-14 candidate lineage and VI-15 candidate/review/
promotion lineage were independently checked as ancestors of the VI-16 exact candidate.

## Twelve named propositions

| Proposition | Independent VI-16 challenge | Result |
| --- | --- | --- |
| `M16-RSOT-001` Bounded ownership | source/config/public seam show M00 owns Raw Signal decisions; A00 composes; PostgreSQL is mechanism | PASS |
| `M16-RSOT-002` Configured schedule truth | immutable policy/version and exact `:00/:30` half-open slot law remain realised and proved | PASS |
| `M16-RSOT-003` Occurrence admission | one actually received provider-logical record per observation; capture/observation independence retained | PASS |
| `M16-RSOT-004` Native fidelity | native values/nulls/provenance preserve admitted form through PostgreSQL and installed readback | PASS |
| `M16-RSOT-005` Temporal-kind law | exact `true_instant|date_only|receipt_only`; no fabricated `event_ts_utc` or timezone | PASS |
| `M16-RSOT-006` Receipt-evidence law | exact active-policy/eligibility/in-slot derivation; constant role; no membership/count semantics | PASS |
| `M16-RSOT-007` Assessment law | exact three states, owner-derived outcome, append-only immediate-predecessor supersession, no finality | PASS |
| `M16-RSOT-008` Identity/retry law | typed layers remain distinct; same-ID identical retry/id conflict/new retransmission distinction hold | PASS |
| `M16-RSOT-009` Persistence/failure law | real PostgreSQL own-transaction durability/restart/failure family passes; no cross-kind atomicity/SLA claim | PASS |
| `M16-RSOT-010` Referential replay law | original domain facts remain referentially readable; no authoritative replay capability activated | PASS |
| `M16-RSOT-011` Public governance law | typed M00 seam remains sole admitted semantic boundary; A00/private PG constructor exception adds no meaning | PASS |
| `M16-RSOT-012` Compatibility law | `.v1` requiredness/discriminants/identity/time/null semantics remain exact; no silent version reuse found | PASS |

BC-001 composition/ownership was challenged separately through source/config trace and a direct installed
A00 -> M00 -> PostgreSQL path. The realised boundary remains `A00 -> M00`; M00 owns semantic state/time/persistence
meaning and PostgreSQL/Psycopg/SQL/repository remain non-owning mechanisms.

## Nineteen proof obligations

All 13 current product obligations are present in the product-proof authority and covered across six admitted families:
`IA17-PROD-001..008`, repaired successor `IA22R01-PROD-009`, and `IA17-PROD-010..013`. The predecessor
`IA17-PROD-009` is explicitly forbidden/non-current. `tools/validate_product_proof.py` independently reports six
families, 13/13 obligations and `READY_FOR_PROOF`.

The six architecture obligations `IA17-ARCH-001..006` remain represented by the architecture/bootstrap proof and
current registries. The separately governed `architecture_kernel` promotion set passed **74/74**, with one active
runtime module, one implementation allocation and zero dependency/public-seam violations.

## Independent execution

On the exact candidate in the fresh pinned proof environment:

- complete admitted product population: **479/479 PASS**;
- non-U05 families: **424/424 PASS**;
- U05 real-PostgreSQL family: **55/55 PASS**;
- architecture/bootstrap: **74/74 PASS**;
- mypy: PASS across 16 source files;
- Ruff: PASS;
- product/architecture/dependency/public-seam validators: PASS.

One intermediate U05 bounded batch exceeded the command-wrapper time before a terminal pytest result and was not
counted. Every affected case was rerun to explicit terminal PASS. A first validator invocation without `PYTHONPATH=src`
failed import collection and was likewise not counted; the Tester corrected only its invocation.

The preserved proof bootstrap did not include a PyYAML wheel. Exact locally installed PyYAML 6.0.3 was supplied to the
fresh proof/install venvs; this changed no candidate or package bytes, and the accepted package metadata itself pins
`PyYAML==6.0.3`.

## Fixture-independent installed semantic challenge

A fresh external Python 3.13.5 environment loaded only the accepted wheel from `site-packages`, with `PYTHONPATH`
unset and no repository path on `sys.path`. Installed top-level runtime modules were exactly `architecture`,
`composition` and `raw_signal_occurrence_truth`; no P01, K01, provider/network, downstream-consumer, DMPV3 or replay
runtime module was importable.

A Tester-authored direct sequence against a fresh PostgreSQL 17.9 database established:

- A00 -> PostgreSQL-backed M00 composition and typed public boundary;
- exact receipt-evidence role, `one_or_more_received` and native Decimal/null readback;
- fresh-application durable idempotent retry and fail-closed policy-reference mismatch;
- append-only `zero_received -> one_or_more_received` immediate-predecessor supersession;
- same-ID retry/conflict law and distinct newly received retransmission identity;
- restart missing-slot `unknown_not_established` rather than inferred zero;
- no hidden eligibility default;
- date-only/receipt-only preservation and no fabricated event UTC;
- runtime identity-layer separation.

The resulting semantic row counts were policy/capture/observation/assessment `4/4/6/4`.

## Remaining Unknowns and boundedness

No evidence was found that the realised/package state silently selects concrete provider mappings, provider duplicate
or revision equivalence, clock/finality/count semantics, production opaque-ID generation, authoritative replay,
retention/deletion, provider/network integration, validation/quarantine, D001+, downstream business semantics or
performance/SLA/RTO/RPO behaviour. VI-15 resolved only final distribution metadata as authorised.

The assessment `evidence_as_of_ts_utc` boundary was specifically challenged. The accepted U04 review already records
that current law provides no historical query/commit clock and forbids using observation receipt time as its surrogate.
The current implementation therefore evaluates evidence visible to the assessment transaction without inventing a
receipt-time cutoff; no new temporal rule was inferred and no current-authority contradiction was established.

## Candidate/package relevance and integrity

The supplied wheel hashes to `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127` and
contains exactly the 16 tracked runtime Python files, byte-equal to the candidate source state. The accepted sdist hash
is `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

The exact candidate worktree remained clean; `git diff --check` passed; `git fsck --full --no-dangling` passed.

## Disposition

`PASS`.

No material VI-16-L1 semantic finding was established. This disposition permits only a subsequent Worker
preserved-ancestry VI-16 promotion/close-out. VI-17 remains prohibited until that promotion succeeds and current-state
routing is advanced under the accepted ExecPlan.
