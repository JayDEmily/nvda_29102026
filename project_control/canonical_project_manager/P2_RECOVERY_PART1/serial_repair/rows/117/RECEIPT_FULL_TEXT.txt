# Semantic receipt — `tests/tier_a/persistence/test_append_only_repository_surfaces.py`

## File evidence

- Sequence `117`, unit `PM-015`; test SHA-256 `94b0936c5ed3f1e172076285740476069ca6f6861e01668dc1b097a4d2e3aca1`.
- Full reads: test `1-64`; complete execution-event and market-observation repositories; persistence authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:390-405`; ownership supplement `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-113`; transaction/replay law `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76`.
- Raw test result: `3 passed in 0.04s`.

## G1 — `test_execution_event_repository_preserves_append_order_and_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:7-20`; two execution-event mappings are appended and write/read alias mutations are tested.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-113`, especially lines `109-110`.
- Authority match: append-only record repositories must preserve insertion order and return copies; this test directly exercises both clauses for the current in-memory execution-event adapter.
- Behaviour proved: the two records remain in insertion order and nested caller/readback mutations do not alter stored values.
- Limitation: records are arbitrary mappings; event IDs are neither required nor duplicate-protected; no authorised writer, sequence/version, transaction, durability, restart readback or replay envelope is proved.
- Adversarial challenge: append duplicate event IDs or malformed events; the tested order/copy assertions still pass.
- Exact-surface falsifier: reorder records or retain either nested input/readback mapping by reference; the equality assertion at lines `17-20` must fail.
- Assertion that must fail and why: The equality at lines `17-20` must fail if execution events are returned out of insertion order, if the first stored stage follows the caller mutation to `mutated`, or if mutating the listed copy to `listed-mutated` changes repository state. The test does not fail for duplicate IDs, malformed events, missing authorised-writer evidence, non-durable storage or absent transaction sequencing.
- Semantic relation: `exact_full_proof`.
- Proof strength: `substitution`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain this exact in-process order/copy regression while keeping durability and record semantics explicitly unclaimed.

## G2 — `test_market_observation_repository_preserves_append_order_and_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:23-36`; two market-observation mappings are appended and write/read alias mutations are tested.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-113`, especially lines `109-110`.
- Authority match: the test directly exercises the admitted insertion-order and copy-readback rules for the current in-memory observation adapter.
- Behaviour proved: the two observations retain insertion order and nested caller/readback mutations do not alter stored values.
- Limitation: observations are arbitrary mappings; IDs, source/time identity, schema, duplicates, authorised writer, sequence, durability and replay are unproved.
- Adversarial challenge: append duplicate observation IDs or fabricated market payloads; the order/copy assertions remain green.
- Exact-surface falsifier: reorder observations or retain either nested input/readback mapping by reference; the equality assertion at lines `33-36` must fail.
- Assertion that must fail and why: The equality at lines `33-36` must fail if observations are reordered, if the first stored spot follows the caller mutation to `999.0`, or if mutating the listed copy to `0.0` changes internal state. It remains green for duplicate or fabricated observations, missing source/time identity and the absence of durable sequencing or replay evidence.
- Semantic relation: `exact_full_proof`.
- Proof strength: `substitution`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain this exact non-durable adapter regression without promoting record authority.

## G3 — `test_append_only_observation_repositories_do_not_expose_keyed_mutators`

- Test locator: `tests/tier_a/persistence/test_append_only_repository_surfaces.py:39-64`; public method names are compared with a thirteen-name prohibited set.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:106-110`; keyed overwrite/upsert methods are prohibited absent later reconciliation policy.
- Authority match: the test covers several obvious exact names, but the authority is semantic and not limited to this finite naming catalogue.
- Behaviour proved: neither current repository exposes a public callable with one of the thirteen listed names.
- Limitation: aliases such as `amend`, `set`, `save`, `update_event`, generic mutation callables, property-based writers and direct mutable storage can pass; keyed identity is not implemented at all.
- Adversarial challenge: add `amend_event(event_id, payload)` or `set_observation`; the assertion remains green despite equivalent keyed overwrite authority.
- Exact-surface falsifier: add any one exact prohibited public method; the assertion at line `64` must fail.
- Assertion that must fail and why: The disjointness assertion at line `64` must fail if either repository exposes a public callable with one of the thirteen exact prohibited names collected at lines `42-55`. An equivalent keyed overwrite named `amend_event`, `set_observation` or another alias remains outside the finite set, so the group cannot prove behavioural append-only authority.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace finite method-name exclusion with behavioural immutability and authorised-writer tests over typed record identities.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Two strong local order/copy regressions satisfy bounded alpha rules, but a finite mutator-name blacklist plus untyped, non-durable records does not prove append-only authority.
