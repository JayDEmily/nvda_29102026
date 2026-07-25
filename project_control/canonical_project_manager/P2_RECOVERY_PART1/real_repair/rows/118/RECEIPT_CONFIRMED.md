# Semantic receipt — `tests/tier_a/persistence/test_capital_state_repository_surface.py`

## File evidence

- Sequence `118`, unit `PM-015`; test SHA-256 `fe5dc41ad8069cdbfe0c511878c94588dc53b6965fedbad92de0a9d555cdaae1`.
- Full reads: test `1-68`; complete `src/nvda_desk/repositories/capital_state_repository.py:1-51`; persistence authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:390-405`; ownership supplement `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-113,146-153`; transaction/persistence consequence `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76`.
- Raw test result: `4 passed in 0.03s`.

## G1 — `test_capital_state_repository_rejects_duplicate_ids_and_preserves_copy_boundary`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:8-24`; one snapshot is written, input/readback aliases are mutated, and duplicate identity is rejected.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:106-110,146-153`.
- Authority match: identifier-keyed capital state must reject duplicate truth and return copies; this test directly proves those local process-memory clauses.
- Behaviour proved: write-time and read-time nested mappings are detached and a second write under the same normalised ID raises.
- Limitation: the snapshot is an arbitrary mapping; no typed capital owner, source lineage, state version, idempotency fingerprint, receipt, transaction or durable commit is exercised.
- Adversarial challenge: store malformed or contradictory capital values under a new ID; all assertions remain green.
- Exact-surface falsifier: silently overwrite the duplicate or retain either mutable mapping by reference; an assertion at lines `15-24` must fail.
- Assertion that must fail and why: The equality assertions at lines `15` and `19-22` must fail if the stored nested source follows either caller or readback mutation, and the `pytest.raises` block at lines `23-24` must fail if a duplicate normalised ID silently overwrites or is accepted. Arbitrary capital mappings under new IDs remain valid, so typed state, lineage, version and transaction truth are not established.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `substitution`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain as local adapter regression, not proof of authoritative capital-state persistence.

## G2 — `test_capital_state_repository_lists_snapshots_in_insertion_order`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:27-35`; two snapshots are listed in write order and list-read mutation is isolated.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:109-110`.
- Authority match: insertion order and copied list readback are explicitly required local repository behaviours.
- Behaviour proved: two process-memory snapshots retain insertion order and a modified returned mapping does not alter storage.
- Limitation: insertion order is not committed sequence authority under `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:50-56`; identifiers are omitted from this list surface and no gap/version semantics exist.
- Adversarial challenge: restart the process or request committed sequence identity; the test provides no evidence.
- Exact-surface falsifier: reorder records or return mutable internal dictionaries; the assertion at line `35` must fail.
- Assertion that must fail and why: The equality at line `35` must fail if the two snapshots are returned out of insertion order or if modifying the first listed mapping to `1.0` alters internal storage. This is volatile process order only; it carries no identifiers, committed sequence, gap detection or restart evidence.
- Semantic relation: `exact_full_proof`.
- Proof strength: `substitution`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; preserve as a volatile adapter regression without calling insertion order durable sequence.

## G3 — `test_capital_state_repository_reads_and_lists_identifier_records_copy_safely`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:38-55`; identifier-bearing record read/list output and nested copy isolation are asserted.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:108-110,146-153`.
- Authority match: identifier-keyed bounded state and copied readback are governed, and this test proves one local record-form clause.
- Behaviour proved: the repository returns the normalised snapshot ID alongside a detached nested snapshot in both read and list surfaces.
- Limitation: record schema and snapshot payload remain untyped; identity is not bound to semantic fingerprint, version, writer, receipt or transaction.
- Adversarial challenge: store any arbitrary mapping under a valid ID; the record assertions continue to pass.
- Exact-surface falsifier: omit/change the ID or retain the nested record by reference; an assertion at lines `43-55` must fail.
- Assertion that must fail and why: The record equality at lines `43-46` must fail if the read omits or changes `snapshot_id` or payload content, and the list equality at lines `50-55` must fail if mutating the returned nested record changes storage. The ID is still not bound to a typed capital-state fingerprint, writer, version, receipt or transaction.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; admit only after typed capital-state and version/receipt semantics are proved.

## G4 — `test_capital_state_repository_rejects_empty_id_and_duplicate_after_normalisation`

- Test locator: `tests/tier_a/persistence/test_capital_state_repository_surface.py:58-68`; blank IDs are rejected and surrounding whitespace normalises to the existing ID for duplicate/read behaviour.
- Authority locator: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:108-110,146-153`.
- Authority match: bounded identifier-keyed state requires stable non-empty identity; the exact trim/duplicate behaviour is a valid local boundary.
- Behaviour proved: all-whitespace identity is rejected, whitespace-normalised duplicate write fails, and normalised read returns the original snapshot.
- Limitation: other canonicalisation, case rules, namespace, identity provenance and cross-store uniqueness are not governed or tested.
- Adversarial challenge: use semantically duplicate IDs differing by case or Unicode form; this test does not establish conflict behaviour.
- Exact-surface falsifier: accept blank identity, permit the whitespace duplicate or fail the normalised read; an assertion at lines `61-68` must fail.
- Assertion that must fail and why: The first `pytest.raises` block at lines `61-62` must fail if an all-whitespace ID is accepted; the duplicate block at lines `65-66` must fail if trimming no longer maps ` cap-1 ` to the existing key; and line `68` must fail if normalised readback does not return the original snapshot. Case, Unicode and cross-store identity rules remain unspecified and untested.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain as local ID regression while broader identity and capital semantics remain unproved.

## File decision

- Groups/relationships: `4/4`.
- Final disposition: `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Strong local copy, insertion-order, duplicate and normalisation regressions exist, but arbitrary mappings and absent typed owner, durability, version, transaction, idempotency and receipt semantics prevent authoritative capital-state admission.
