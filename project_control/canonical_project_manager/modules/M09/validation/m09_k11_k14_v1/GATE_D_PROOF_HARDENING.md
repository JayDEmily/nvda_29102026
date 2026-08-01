# M09 Gate D Proof Hardening

## Trigger

The first production-facing integration attempt showed that the original clear-branch fixture did not contain matching M05/M06 prepared lineage and that the current M06 evaluator truthfully emitted three unknown families. The fixture was corrected to use one exact matching M05 candidate and one fully typed, contract-valid M06 assessment rather than caller summaries.

A semantic reread of section 7.13.4 also showed that the original seven public-seam assertions did not prove policy-value identity, contradictory aggregate-state rejection, exact branch lineage in the K14 receipt, decision-to-input recomputation, or copied-model revalidation.

## Admitted hardening

Five additional production-facing cases now require:

1. join-policy values and capital-policy values to participate in semantic identity;
2. contradictory M06 aggregate state/evidence summaries to be rejected;
3. receipt construction to recompute the decision against the exact K11, capital-state, M07 and policy inputs;
4. K14 receipts to preserve exact M05/M06 lineage and explicit false execution authority; and
5. forged Pydantic copies of K11/K14 contracts to be revalidated at public boundaries.

The compatibility C-036 route remains bounded and separate from the canonical typed M09 seam; it must not fabricate canonical M05/M06 lineage.

## Expected-red result before production restoration

- reference/mutant proof: 16 passed;
- canonical production-facing proof: 12 failed solely because `nvda_desk.m09_capital_authority` was absent;
- retained C-036 compatibility proof: 3 failed solely because the bounded branch compatibility contracts were absent;
- canonical M09 or compatibility production source present during this check: none.

Gate D remains open under the separately reviewed proof, but implementation acceptance now requires all 15 production-facing nodes above to resolve without new affected-suite failures.
