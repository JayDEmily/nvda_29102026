# M08 K13 C-PROOF Validation Summary

## Scope

Accepted proposition: M08 section 7.8 playbook-definition, immutable-catalogue
and eligibility-decision authority only. The proof defines the target
`PlaybookDefinition`, `PlaybookCatalogue` and `EligibilityDecision` public seam
without creating production code.

## Results

| Check | Result |
|---|---|
| Reference and false-positive proof | PASS — 11 / 11 |
| Named mutants | PASS — caller order, missing-catalogue default, ignored posture block, catalogue-order tie and foreign-capital claim |
| Production seam | EXPECTED RED — 11 passed / 7 failed; all seven fail because the canonical package is absent |
| Vocabulary parity | PASS — 4 / 4; namespaces `global`, `m04`, `m07`, `m08` and exact M08 entries |
| Proof-block manifest | PASS — 56 / 56 |
| Proof-executor contract | PASS — 21 / 21 |
| M08 vocabulary audit | PASS — zero unresolved candidates across 22 scoped files; stamp current |
| Python compile, YAML parse and diff checks | PASS |
| Ruff | UNAVAILABLE — no installed Ruff module; no substitute used |
| Production/runtime configuration mutation | none |

## Sensitivity

The proof distinguishes missing authority from three valid stand-down states,
requires owner-issued lineage for each required eligibility fact, ignores
catalogue/container/caller order in favour of authority priority and the exact
identity/version tie-break, canonicalises catalogue fingerprint material,
rejects missing facts and invalid fact or catalogue authority, preserves an
occurrence-independent semantic decision fingerprint and prevents eligibility
metadata from claiming candidate-expression, capital, execution, lifecycle,
replay or transaction authority.

## Registry integrity repair

The retained-test registry contained one pre-existing unquoted M07 note with a
colon in its scalar value, which made the YAML invalid to a standard parser. The
same text is now quoted; no M07 status or meaning changed. Both proof registries
parse successfully.

## Gate

`PASS:C-PROOF:GATE_D_OPEN:M08_K13_PLAYBOOK_CATALOGUE_AUTHORITY`.
The expected-red production assertions must become green through the bounded
M08 implementation; they may not be skipped, xfailed or weakened.
