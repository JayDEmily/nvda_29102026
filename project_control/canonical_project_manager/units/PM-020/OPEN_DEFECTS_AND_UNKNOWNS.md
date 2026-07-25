# Open defects and Unknowns

## Failed integration evidence

1. PM-019 projects all 179 files and 777 assertion groups but fails its validator:
   - 99 groups do not project one allowed semantic-relation enum;
   - 123 groups do not project one allowed proof-strength enum;
   - 214 admitted group relationships lack an exact group-level authority locator; and
   - six non-admitted file-decision excerpts lack a mechanically detectable explicit return-gate phrase.
2. Complete Tier A is red: `61 failed, 1097 passed`.
   - 42 failures exactly match the frozen Gate C expected-red nodes from the sequence-160 checkpoint.
   - 19 additional failures remain: one Parallel Risk policy-ID mismatch; four other vocabulary/projection failures; and fourteen obsolete tuple-fixture failures in the synonym-candidate audit.
3. Active `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` were not updated. The ExecPlan permits that mechanical promotion only after PM-019 registers agree; they do not.

## Provenance qualification

- The repository contains 66 preserved original receipts through sequence 066 and 54 explicitly reconstructed replacement receipts for sequences 067-120. The reconstructed receipts preserve surviving ledger decisions and fresh file-read evidence but are not claimed byte-identical to the lost originals.
- Sequences 121-179 were authored in the current continuation run and are present at their ledger-recorded paths.

## Unknown

- None caused by unavailable dependency, credential or external package gateway in this run.
- Semantic correctness of the 99/123/214 failed PM-019 relationships remains Unknown pending authorised one-file-at-a-time repair and independent Project Manager audit.
