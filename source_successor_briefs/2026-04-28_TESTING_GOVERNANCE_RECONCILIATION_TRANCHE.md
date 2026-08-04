# Testing Governance Reconciliation Tranche

Status: pending explicit user acceptance
Promotion readiness: false
Runtime code changed: false
Pytest files changed: false
Atlas implementation opened: false

## Purpose

Repair stale or ambiguous testing-governance language before further Atlas implementation work.

This tranche reconciles the test override, test README surfaces, and retained-test registry governance rules with the current authority hierarchy:

1. official source material when external language, API, package, platform, or tool behaviour is in scope
2. repo-root `AGENTS.md` and the numbered normative/control stack
3. vocabulary governance, including `docs/vocabulary/vocabulary_registry.md`
4. testing and promotion law in `docs/08_TESTING_AND_PROMOTION_CORE.md`
5. retained-test registry and proof-block authority
6. admitted tests and governed proof artefacts
7. runtime code as observed implementation
8. docstrings as explanatory surfaces

## Scope

In scope:

- `AGENTS.md` route truth
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` route truth
- `intent_migration/testing_governance_reconciliation/AGENTS.override.md`
- `tests/AGENTS.override.md`
- `tests/README.md`
- `tests/tier_a/README.md`
- `tests/tier_b/README.md`
- `tests/tier_c/README.md`
- `config/retained_test_registry.yaml` governance rules
- tranche brief and ledger receipts

Out of scope:

- runtime code changes
- pytest implementation changes
- Atlas implementation tranche work
- promotion or demotion of individual test files
- behavioural hardening of presence-only tests

## Acceptance state

The leaf execution recorded below is mechanically reconciled but remains pending explicit user acceptance.

Current retained-test registry inventory:

```text
tier_a_test_count: 67
registered_retained_seed_tier_a: 67
tier_a_file_registered_outside_retained_seed_tier_a: 0
pending_explicit_registry_record: 0
```

Semantic retained-family trust is not claimed by this tranche without the runtime-code and docstring rereads required by registry law.

## Leaf execution

| Leaf | Status | Result |
|---|---|---|
| TGR-L01 route and active-pack plan | closed | Active route now points to this pack and retained roadmap/slice-pack evidence remains recorded. |
| TGR-L02 testing-governance text reconciliation | closed | Test override and README surfaces now state that folder location is not authority and that normative/vocabulary/test law outranks observed code. |
| TGR-L03 retained-test registry rule reconciliation | closed | Registry rules now bound code-vs-docstring divergence beneath doctrine, vocabulary, tests, and registry authority. |
| TGR-L04 mandatory closeout | pending_user_acceptance | Scope, verification, and packaging receipts are recorded, but tranche closeout remains pending explicit user acceptance. |

## Verification

Passed:

- `ruby -e 'require "yaml"; YAML.load_file("config/retained_test_registry.yaml")'`
- `jq empty var/audit/ledgers/testing_governance_reconciliation_tranche_ledger.json`
- `jq empty var/audit/ledgers/testing_governance_reconciliation_tranche_ledger.schema.json`
- `git diff --check`
- no `src/**` files changed
- no `tests/**/*.py` files changed

Not run:

- full pytest, because this tranche changed governance Markdown/YAML surfaces only and did not change runtime code or pytest implementation.

## Carry-forward

- Presence-only and zero-assert proof files remain inventoried concerns and must be handled in later bounded proof-hardening tranches.
- User acceptance remains required before this tranche may be described as closed.
- Atlas implementation remains blocked until the active route moves to a lawful Atlas implementation pack.
