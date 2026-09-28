# VI-16-L1 — Independent whole-BICP Tester disposition

## Disposition

**PASS**

## Exact reviewed state

- candidate commit: `9248f3b1788f8e99e59a0482c4cc393c27942715`;
- candidate tree: `5560c97ad83a05190603c323eb4fbfa0c21d983d`;
- Tester cycle: `TESTER_VI16_L1_1790592833`;
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- wheel SHA-256: `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist SHA-256: `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`;
- received Tester handoff SHA-256: `f1e4e0d8e8099f7f6b9dfd82481c8086c4d7132e08ebc0544caed8188c7c0abb`.

Testing and source/semantic review were performed against a detached worktree at the exact candidate rather than the
later routing tip. There is no `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift from the accepted VI-15-L2
package candidate to the VI-16 candidate.

## Whole-BICP semantic result

The Tester rebound the exact accepted BICP, IRB, IWO, VI-04 authority and VI-15 distribution authority and challenged
the realised implementation/package against the complete VI-16 proposition.

All twelve named Raw Signal propositions passed independent semantic challenge:

1. `M16-RSOT-001` bounded ownership;
2. `M16-RSOT-002` configured schedule truth;
3. `M16-RSOT-003` occurrence admission;
4. `M16-RSOT-004` native fidelity;
5. `M16-RSOT-005` temporal-kind law;
6. `M16-RSOT-006` receipt-evidence law;
7. `M16-RSOT-007` assessment law;
8. `M16-RSOT-008` identity and retry law;
9. `M16-RSOT-009` persistence/failure law;
10. `M16-RSOT-010` referential replay/readback law;
11. `M16-RSOT-011` public governance law; and
12. `M16-RSOT-012` compatibility law.

BC-001 composition/ownership remains exact: A00 owns construction/translation/top-level lifecycle; M00 owns Raw Signal
semantic state/time/persistence meaning and the typed command/read boundary; PostgreSQL/Psycopg/SQL/schema/repository
remain non-owning mechanisms. The runtime owner direction remains `A00 -> M00`, with no reverse semantic dependency.

All nineteen current proof obligations were challenged: the thirteen current product obligations plus
`IA17-ARCH-001..006`. The persistence/restart obligation is repaired successor `IA22R01-PROD-009`; predecessor
`IA17-PROD-009` remains explicitly forbidden/non-current.

## Independent execution and direct challenge

- complete product population: **479/479 PASS**;
- product proof control: six admitted families / **13/13** current product obligations;
- architecture/bootstrap: **74/74 PASS**;
- structural architecture, dependency and public-seam checks: PASS;
- mypy: PASS across 16 source files;
- Ruff: PASS.

A fresh external install of the accepted wheel, without repository path injection, exposed only `architecture`,
`composition` and `raw_signal_occurrence_truth`. No P01, K01, provider/network, downstream-consumer, DMPV3 or replay
runtime package was importable.

A Tester-authored direct installed A00 -> PostgreSQL-backed M00 sequence established exact receipt-evidence/readback,
durable idempotent retry, fail-closed policy mismatch, append-only late-evidence supersession, identity conflict law,
restart `unknown_not_established`, absent-eligibility fail-closed behaviour, temporal-kind preservation and typed
identity separation. The fresh database ended with policy/capture/observation/assessment row counts `4/4/6/4`.

## Remaining Unknowns and bounded claims

No hidden implementation default was established for concrete provider eligibility/mappings, provider revision or
duplicate equivalence, clocks/finality/exact counts, production opaque-ID generation, retention/replay, provider/network
integration, validation/quarantine, D001+, downstream consumers or SLA/RTO/RPO/performance behaviour. Final package
name/version is separately resolved by accepted VI-15 authority only.

The previously challenged `evidence_as_of_ts_utc` case does not establish a current defect: accepted U04 review records
that current authority provides no historical query/commit clock and forbids use of receipt time as a system-knowledge
visibility surrogate. The current implementation uses committed evidence visible to the assessment transaction rather
than inventing an unauthorised receipt-time cutoff.

## Package relevance and repository integrity

The accepted wheel contains exactly the 16 tracked runtime Python files and those bytes match the final source state.
The wheel/sdist hashes remain exact. The candidate worktree remained clean, `git diff --check` passed and
`git fsck --full --no-dangling` returned success.

The preserved proof bootstrap did not contain a PyYAML wheel; exact locally installed PyYAML 6.0.3 was supplied to the
fresh Tester environments. This changed no candidate/package bytes and matches the accepted package's pinned dependency.

## Acceptance boundary

No material VI-16-L1 finding was established. Exact candidate
`9248f3b1788f8e99e59a0482c4cc393c27942715` is accepted for subsequent preserved-ancestry VI-16 promotion/close-out
only. VI-17 remains prohibited until that promotion succeeds and the current state is lawfully advanced.
