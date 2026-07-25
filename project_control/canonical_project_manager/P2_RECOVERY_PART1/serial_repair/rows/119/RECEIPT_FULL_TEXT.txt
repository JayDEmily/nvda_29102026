# Semantic receipt — `tests/tier_a/persistence/test_execution_records_repository_surface.py`

## File evidence

- Sequence `119`, unit `PM-015`; test SHA-256 `9477312237d808da4c45a3717b416dcd44d70376c1e983a30a8ffc7223cc9b02`.
- Full reads: test `1-28`; complete `src/nvda_desk/persistence/execution_records.py:1-21`; persistence supplement `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-113`; transaction and current-alpha consequence `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76`.
- Raw test result: `2 passed in 0.03s`.

## G1 — `test_execution_records_repository_preserves_append_order_and_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_execution_records_repository_surface.py:6-19`; two execution-record mappings are appended and write/read alias mutations are tested.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:106-110`; current alpha consequence `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:72-75`.
- Authority match: insertion order and copied readback are admitted bounded alpha behaviours, and the normative consequence specifically recognises current execution-record stores as append-oriented and copy-safe in places.
- Behaviour proved: the two mappings remain in insertion order and nested caller/readback mutations do not change stored values.
- Limitation: records are arbitrary mappings; execution identity is not required or duplicate-protected; no typed state, authorised writer, idempotency, sequence/version, transaction, receipt binding, durability or restart replay is proved.
- Adversarial challenge: append duplicate execution IDs or contradictory execution records; the equality assertion remains green.
- Exact-surface falsifier: reorder records or retain either nested input/readback mapping by reference; the assertion at lines `16-19` must fail.
- Assertion that must fail and why: The equality at lines `16-19` must fail if records are reordered, if the first stored side follows the caller mutation to `mutated`, or if mutating the listed copy to `listed-mutated` changes internal state. Duplicate execution IDs, contradictory records and the absence of idempotency, sequence, receipt binding or durability do not affect this assertion.
- Semantic relation: `exact_full_proof`.
- Proof strength: `substitution`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain this exact local order/copy regression while explicitly withholding execution-record authority and durability.

## G2 — `test_execution_records_repository_exposes_no_keyed_overwrite_method`

- Test locator: `tests/tier_a/persistence/test_execution_records_repository_surface.py:22-28`; two expected method names are present and two exact overwrite names are absent.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:106-110`; keyed overwrite/upsert methods are prohibited absent reconciliation policy.
- Authority match: the exact absent names are compatible with append-only ownership, but the semantic prohibition is not limited to `write_record` and `upsert_record`.
- Behaviour proved: the current object exposes `append_record` and `list_records` and lacks the two exact checked names.
- Limitation: aliases such as `replace_record`, `update_record`, `set_record`, generic mutation methods or direct mutable access pass; there is no keyed identity to protect.
- Adversarial challenge: add `replace_record(execution_id, payload)`; every assertion remains green.
- Exact-surface falsifier: remove either expected method or add either exact prohibited method; an assertion at lines `25-28` must fail.
- Assertion that must fail and why: Lines `25-26` must fail if either expected append/list method disappears, while line `27` or `28` must fail if the exact `write_record` or `upsert_record` name is added. Equivalent keyed mutation through `replace_record`, `update_record`, another alias or direct storage access remains green, so the group does not establish behavioural immutability.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace two-name absence with behavioural immutable identity, authorised-writer and duplicate/idempotency tests over typed records.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Local order/copy behaviour is valid, but arbitrary mappings and a two-name mutator blacklist do not prove typed append-only execution-record persistence or transaction/idempotency semantics.
