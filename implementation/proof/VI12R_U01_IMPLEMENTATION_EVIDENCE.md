# VI-12R U01 implementation evidence

## Status

**WORKER CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

This evidence records the first bounded production implementation unit after the independent
Tester Iteration 014 VI-11 `PASS`. It does not accept the unit, authorise U02, or convert either
of the two observed proof-harness discrepancies below into a proof-layer disposition. Fresh
VI-13R review is required before the next dependent IWO unit.

## Exact lineage

- accepted forward `main` after Tester Iteration 014 merge:
  `95c0aea` (`merge: accept Tester Iteration 014 bounded VI-11 pass`);
- Worker branch: `work/vi12r-u01-contract-owner-boundary`;
- U01 production commit: `d14190cdfe845fdd60629ca9b1eed8d1d2704d44`;
- U01 production tree: `00f036fcd22a6e3ec6f79c5ddfeb9d210d1418b9`;
- changed production path: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only;
- production diff: 461 insertions / 1 deletion;
- no test, proof-control, architecture-registry, dependency, PostgreSQL, packaging or governance
  file was changed by the U01 production commit.

The exact fixed authority remains:

- `handoff/authority/BICP_CANDIDATE_005.json` SHA-256
  `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- `handoff/authority/BICP_CANDIDATE_005.md` SHA-256
  `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`;
- `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` SHA-256
  `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`;
- `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md` SHA-256
  `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e`.

## Implemented proposition

IWO-U01 only: typed contracts, identity layers and owner boundary.

The candidate implements:

- the five canonical `.v1` payload contract classes;
- exact concept/contract identities for those payloads;
- runtime-distinct identity layers for concept, contract, scope policy, eligibility policy,
  scope-policy reference, capture occurrence, observation occurrence, assessment occurrence,
  provider, delivery artefact and ingestion-sequence scope;
- canonical `R001`-`R323` Raw Signal catalogue identities;
- exact finite temporal, relation-role and assessment-outcome discriminants;
- structural optional absence represented separately from provider-native null retained inside
  `native_record`;
- the accepted BC-005 source-timestamp law: `true_instant` / `date_only` require supplied
  `source_timestamp_raw`; `receipt_only` requires it absent; optional
  `source_timezone_native` is preserved rather than inferred;
- immutable/frozen slotted public payload objects;
- separate typed command and read facets exposed through `create_owner()`;
- final typed method shapes for later units, with every U02-U05 behaviour deliberately raising
  `NotImplementedError` rather than being implemented early.

The candidate deliberately does **not** implement schedule generation, provider mapping/admission,
receipt-evidence derivation, assessment state transitions, persistence, PostgreSQL, reconciliation,
packet carriage, replay, A00 composition or downstream consumers. Those remain later IWO units.

## Environment preflight

Exact runtime/tool versions used for the committed candidate validation:

```text
Python 3.13.5
pytest 9.0.3
mypy 1.20.1
Ruff 0.15.11
PyYAML 6.0.3
```

The exact Python runtime is native to this sandbox. The pinned Python-only validation tooling was
recovered from preserved project artefacts into `/mnt/data/nvda_tooling_exact` and injected only
through `PYTHONPATH`; it was not installed into or committed with the repository. PostgreSQL is not
required to decide IWO-U01 and was not started for this unit.

## Validation on exact committed U01 state

Validation was run with `HEAD=d14190cdfe845fdd60629ca9b1eed8d1d2704d44` and
`tree=00f036fcd22a6e3ec6f79c5ddfeb9d210d1418b9`.

### U01 bounded product proof

Command:

```text
PYTHONPATH=/mnt/data/nvda_tooling_exact:src \
python -m pytest -q tests/product/raw_signal/test_u01_contract_owner_boundary.py
```

Observed result:

```text
293 passed, 2 failed
```

The two failures are preserved as Worker-observed candidate proof-harness findings below. The
Worker did not change the tests to obtain green.

A diagnostic run excluding only the two implicated test functions produced:

```text
283 passed, 12 deselected
```

This diagnostic result is **not** claimed as U01 acceptance or as a substitute for the complete
U01 proof.

### Direct public-seam type proof

The positive specimen was run directly with exact mypy 1.20.1, `--strict`,
`--disallow-any-expr`, and `--show-error-codes` and returned rc 0.

The negative specimen returned rc 1 and emitted exactly 15 type errors at the 15 source lines
marked `STATIC_NEGATIVE`. The diagnostics covered all command/read cross-layer substitutions,
including occurrence-identity, scope-policy, datetime/integer and list-element substitutions.

Full source typecheck:

```text
Success: no issues found in 15 source files
```

### Product-proof and architecture controls

Observed:

```text
product-proof control: PASS; 6 families; 13/13 obligations; aggregate READY_FOR_PROOF
structural architecture validation: PASS
architecture/bootstrap promotion: 74 passed
Ruff: All checks passed!
dependency-direction validation: PASS
public-seam validation: PASS
git diff --check: PASS (no output)
```

The architecture promotion reported one active runtime module, one implementation allocation,
11 admitted test families and zero dependency/public-seam violations.

## Worker-observed proof-harness findings for VI-13R

These are **observations requiring independent VI-13R disposition**. The Worker does not self-accept
them, weaken tests, or treat them as authority over the IRB.

### W-U01-F001 — receipt-only discriminant specimen conflicts with accepted timestamp law

The parametrised test
`test_every_allowed_v1_discriminant_value_is_accepted` changes only
`source_temporal_kind` on the default RawObservation specimen. That default carries
`source_timestamp_raw="2026-09-20T12:00:04.900000Z"`. Therefore its `receipt_only` case expects a
receipt-only observation retaining a source timestamp to construct successfully.

The same proof file separately requires
`test_temporal_discriminant_controls_source_timestamp_null_law` to reject
`receipt_only` whenever `source_timestamp_raw` is present.

IRB BC-005 states that `source_timestamp_raw` is supplied for `true_instant`/`date_only` and
**absent for `receipt_only`**. BC-009 independently states `receipt-only without provider timestamp`.
The candidate follows that authority and therefore rejects the contradictory parametrised specimen.

**Worker classification proposal:** proof-harness defect exposed by the real implementation;
VI-13R must independently confirm and route the smallest proof-layer repair. Do not change the
BC-005 implementation to make the contradictory specimen pass.

### W-U01-F002 — negative mypy proof parser rejects genuine diagnostics because of path form

`test_every_public_facet_rejects_cross_layer_static_type_substitution` constructs an absolute
`TYPECHECK_NEGATIVE` path, then accepts diagnostics only when each line starts with that absolute
path string. With exact mypy 1.20.1 invoked under the test's repository `cwd`, mypy emits the
repository-relative path:

```text
tests/product/raw_signal/typecheck/public_seam_negative.py:<line>: error: ...
```

The parser therefore records no diagnostic line numbers and fails, despite direct execution
emitting all 15 intended errors at all 15 `STATIC_NEGATIVE` sites. The positive specimen returns
success.

**Worker classification proposal:** proof-harness diagnostic-path parsing defect exposed under the
pinned typechecker; VI-13R must independently reproduce it and determine the smallest proof-layer
repair without weakening the requirement that every negative substitution produce a type error.

## Acceptance boundary / next lawful step

This Worker candidate is **not U01 accepted**. U02 remains prohibited until fresh VI-13R review
compares the exact authority, bounded proof, this committed production candidate, the two observed
proof-harness discrepancies and the mechanical results, and returns its disposition. Any repair is
owned by the layer identified under ExecPlan section 6.7 and must be re-reviewed before U02.
