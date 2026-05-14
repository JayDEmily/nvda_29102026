# Testing Governance Reconciliation Pack

## Status

Active bounded pack for testing governance reconciliation, pending user acceptance of the prior-thread registry reconciliation evidence.

## Scope

This pack owns reconciliation of:

- `tests/AGENTS.override.md`
- `tests/README.md`
- `tests/tier_a/README.md`
- `tests/tier_b/README.md`
- `tests/tier_c/README.md`
- `config/retained_test_registry.yaml` governance rules and candidate live inventory reconciliation
- `AGENTS.md` placeholder routing only where explicitly authorised by the user

## Authority rule

The order of authority for testing work is:

1. official source material when external language, API, package, platform, or tool behaviour is in scope
2. repo-root `AGENTS.md` and the numbered normative/control stack
3. vocabulary governance, including `docs/vocabulary/vocabulary_registry.md`
4. testing and promotion law in `docs/08_TESTING_AND_PROMOTION_CORE.md`
5. retained-test registry and proof-block authority
6. admitted tests and governed proof artefacts
7. runtime code as observed implementation
8. docstrings as explanatory surfaces

## Prohibitions

This pack does not open a new Atlas implementation tranche.

This pack does not open a new Atlas roadmap tranche.

This pack does not make an Atlas-readiness decision.

This pack does not change runtime code.

This pack does not change pytest implementation files.

This pack may clarify the governance rules that control retained-test classification operations.

This pack may add or amend retained-test registry family records for already-existing native tests when that work is required to reconcile candidate live tier status inside `config/retained_test_registry.yaml`, provided the decision is backed by authority reads and no `src/**` or `tests/**/*.py` files change.

This pack must not fabricate a new proof family, widen runtime scope, or silently promote/demote a test without updating the governing receipt surfaces it owns.

## Acceptance requirement

User acceptance requires:

- testing governance text reconciled
- retained-test registry governance rules reconciled
- current live Tier A inventory rows either matched to explicit family records or truthfully carried with an active blocker
- no `src/**` or `tests/**/*.py` changes
- syntax/format checks over changed JSON/YAML/Markdown surfaces where available
- a final user-approved route decision outside this placeholder pack
