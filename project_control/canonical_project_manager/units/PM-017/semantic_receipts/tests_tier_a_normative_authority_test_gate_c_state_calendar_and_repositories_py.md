# Semantic receipt — `tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py`

- Sequence `149`, PM-017; SHA-256 `1de43f825655da5e88ff455c1aeaef496e78f11ec2debb9875c02aab66352a66`.
- Read full test `1-75`, directly exercised calendar importer/projection/operational repository and two memory repositories, propositions `C-006;C-019;C-023`, and Gate C admission evidence. Targeted run: `1 passed, 1 failed`, within the expected-red pack.

## G1 — one explicit reference-to-operational composition

- Locator `12-45` builds a versioned reference bundle and projected context, then requires an explicit `ingest_precursor_context` boundary to produce one operational event.
- This proves one owned composition specimen; it does not establish all four calendar layers, every conflict rule or persistence durability.
- Relation `bounded_separable_clause`; strength `state_transition`.

## G2 — shared memory repositories are copy-safe and instance-isolated

- Locator `48-75` appends nested data to execution and observation repositories, mutates caller/listed copies, and requires stored data to remain original while second instances stay empty.
- It proves process-memory copy and instance boundaries only, not durable append semantics or typed ownership.
- Relation `bounded_separable_clause`; strength `state_transition`.

## File decision

- Groups/relationships `2/2`; final `ADMIT_TIER_A_CURRENT` under the Gate C admission receipt.
- The failed calendar composition remains a Gate D implementation obligation; the green memory-repository clause is not a durability claim.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
