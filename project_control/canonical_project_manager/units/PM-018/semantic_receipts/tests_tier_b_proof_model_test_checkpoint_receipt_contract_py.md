# Semantic receipt — `tests/tier_b/proof_model/test_checkpoint_receipt_contract.py`

- Sequence `169`, PM-018; SHA-256 `f4604f4df6374d9e99a2457baca853a908c18ab73300ea2bcd3ccf5a26d4ec2e`.
- Read full test `1-65`, full prepared-ingress checkpoint, prepared runtime snapshot and context-payload implementation, support-spine authority in `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:328-336`, and receipt ownership limits in `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:102-115`. Targeted run: `2 passed in 0.13s`.
- Current historical routing to Gate-C item C-024 is not semantically exact: this file does not exercise idempotency keys, atomic state/receipt commit, duplicate conflict or rollback.

## G1 — valid detached prepared-ingress checkpoint receipt

- Test locator `31-51`; authority support-spine line `336` requires copy-safe prepared-context handoff and checkpoint receipt payloads.
- The assertions prove the tested valid-status rule, checkpoint/snapshot identity, alignment/source-section carriage, optional/failed enrichment carriage, prepared-context values and copy detachment from the source snapshot.
- They do not prove deterministic fingerprinting, canonical DMPV3 carriage, JSON persistence, receipt-ledger append, transaction atomicity or replay completeness.
- Falsifier: mark the clean snapshot degraded, omit/mis-map a tested field, or return a live alias to the payload; lines `37-51` fail.
- Relation `bounded_separable_clause`; strength `behavioural`; disposition `retain_shadow`.

## G2 — failed enrichment degrades checkpoint receipt

- Test locator `54-65`; authority support-spine line `336` and explicit missing-material visibility requirement.
- The assertions prove that the tested failed-enrichment list changes status to `degraded` and remains visible both at receipt top level and inside prepared context.
- They do not prove all degradation causes, aggregation precedence, durable storage or no invented lineage.
- Falsifier: keep status valid or drop the failure list; lines `60-65` fail.
- Relation `bounded_separable_clause`; strength `state_transition`; disposition `retain_shadow`.

## File decision

- Groups/relationships `2/2`; final `ADMIT_TIER_B_SHADOW`.
- Admit only as shadow proof for the prepared-ingress checkpoint receipt boundary. Remove its current C-024 transaction/idempotency mapping during PM-019; this file cannot support that proposition.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
