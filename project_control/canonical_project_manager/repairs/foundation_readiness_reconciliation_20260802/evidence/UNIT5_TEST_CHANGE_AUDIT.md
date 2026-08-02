# Unit 5 Test-Change Authority Audit

## Scope

- Accepted base audited: `11699fed3838049722a16eedeb68a3ebe5f94b49`.
- Every one of the 46 Unit 4 red propositions is recorded individually in `UNIT5_TEST_CHANGE_AUTHORITY_REGISTER.tsv`.
- Every additional changed test node and the shared test-only authority helper is also recorded.
- AST comparison against `11699fed` finds 43 changed old test functions and 43 changed current test functions; every one is present in the register.
- Unit 4 red evidence: `UNIT4_PHYSICAL_TIER_A_JUNIT.xml`.
- Post-audit focused green evidence: `UNIT5_46_NODE_AUTHORITY_AUDIT_JUNIT.xml` (46 passed: 45 original node IDs plus one authority-mapped replacement).

## Audit outcome

- No skip, xfail, pytestmark suppression, weakened validation or broad retirement was introduced.
- One dropped fingerprint assertion was detected during the audit and restored.
- C046 no-reconstruction assertions were strengthened to require absent reproduced-output identity and fingerprint.
- The capital-decision test retains its original decision action, input-trace and receipt propositions before proving that the unadmitted packet role fails closed.
- Exact test changes are allowed only where the register cites governing authority that supersedes the old seam or field location; all other assertions are unchanged or strengthened.
- The physical test count is unchanged at 1,990. Three node-name replacements are explicitly mapped and there are zero unmapped node removals or additions.

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

## Acceptance follow-through

The audited executable tree is commit `35ebb93`. Signed `alpha_current` passes
19/19 blocks and 811/811 tests at that clean commit. The reconciled tree passes
physical Tier A 1,990/1,990, Tier B 91/91 and Tier C 5/5, with JUnit evidence
for all three physical tiers; proof authority and all 73 block definitions pass;
all 13 vocabulary namespaces are candidate-clean.
The provisional acceptance commit was removed and is not part of branch history.
