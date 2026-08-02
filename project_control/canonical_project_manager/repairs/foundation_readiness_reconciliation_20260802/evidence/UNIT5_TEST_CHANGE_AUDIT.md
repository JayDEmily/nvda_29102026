# Unit 5 Test-Change Authority Audit

## Scope

- Accepted base audited: `11699fed3838049722a16eedeb68a3ebe5f94b49`.
- Every one of the 46 Unit 4 red node IDs is recorded individually in `UNIT5_TEST_CHANGE_AUTHORITY_REGISTER.tsv`.
- Every additional changed test node and the shared test-only authority helper is also recorded.
- Unit 4 red evidence: `UNIT4_PHYSICAL_TIER_A_JUNIT.xml`.
- Post-audit focused green evidence: `UNIT5_46_NODE_AUTHORITY_AUDIT_JUNIT.xml` (46 passed).

## Audit outcome

- No skip, xfail, pytestmark suppression, weakened validation or broad retirement was introduced.
- One dropped fingerprint assertion was detected during the audit and restored.
- C046 no-reconstruction assertions were strengthened to require absent reproduced-output identity and fingerprint.
- The capital-decision test retains its original decision action, input-trace and receipt propositions before proving that the unadmitted packet role fails closed.
- Exact test changes are allowed only where the register cites governing authority that supersedes the old seam or field location; all other assertions are unchanged or strengthened.

## Disposition counts

| Disposition | Records |
|---|---:|
| `assertion_strengthening` | 10 |
| `current_owner_rebind_proposition_preserved` | 3 |
| `current_owner_rebind_proposition_preserved_and_strengthened` | 3 |
| `fixture_authority_completion` | 3 |
| `fixture_authority_completion_assertions_unchanged` | 25 |
| `fixture_authority_completion_original_assertion_restored` | 1 |
| `normative_field_relocation_proposition_preserved` | 1 |
| `normative_role_supersession_carriage_preserved` | 1 |
| `normative_state_scope_adjustment_proposition_preserved` | 1 |
| `normative_supersession` | 3 |
| `normative_supersession_with_preserved_domain_assertions` | 1 |
| `owner_repair_assertions_unchanged` | 6 |
| `test_support_only` | 1 |

## Remaining gate

This audit does not by itself accept Unit 5. The exact post-audit tree must still pass the complete physical Tier A/B/C, signed promotion, proof-control, vocabulary and Git-integrity gates before the provisional acceptance commit can be replaced.
