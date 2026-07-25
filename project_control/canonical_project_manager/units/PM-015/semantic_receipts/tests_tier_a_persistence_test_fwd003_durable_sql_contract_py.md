# Semantic receipt — `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py`

## File evidence

- Sequence `120`, unit `PM-015`; test SHA-256 `a5c7357b7a5010de176623578f2e1a8851c7d1b681086dba2d30d88c4a2248a3`.
- Full reads: test `1-35`; complete `src/nvda_desk/persistence/durable_sql.py:1-101`; bounded alpha persistence direction `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:104-115`; storage-versus-semantic-layer boundary `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:100-107,158-162`; persistence contract `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:390-405`; Gate C authority row `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv:23` and its disposition/conformance rows.
- Raw test result: `2 passed in 0.05s`.

## G1 — `test_durable_sql_store_creates_schema_and_seeds_bounded_dev_rows`

- Test locator: `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py:12-28`; a temporary file-backed store is initialised, seeded for one session and queried through three list methods.
- Authority locator: `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv:23`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:104-115`; `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:158-162`.
- Authority match: Gate C permits proof only of the intended bounded SQL contract, and the architecture permits a bounded SQLite seam without promoting it to production durability or material-state ownership.
- Behaviour proved: for the exercised one-session seed, a file-backed SQLite database returns an NVDA bar with positive close drift, an NVDA option snapshot and one regular-session row.
- Limitation: the test does not prove complete schema constraints, authorised writers, typed repository ports, duplicate/reconciliation law, atomic multi-table failure behaviour, version/lineage, restart replay, material-state ownership, production retention or replacement equivalence; `INSERT OR REPLACE` overwrite semantics are not challenged.
- Adversarial challenge: seed the same session twice with a different symbol or fail the third insert after earlier mutations; the asserted happy-path rows do not establish the required reconciliation or transaction meaning.
- Exact-surface falsifier: return a first bar with a different symbol or non-positive drift, a first option snapshot with a different underlying symbol, or a different session list; an assertion at lines `23-28` must fail.
- Assertion that must fail and why: Lines `23-28` must fail when any queried specimen differs from the seeded NVDA bar, option snapshot or exact session row, because those assertions are the direct read-after-write detectors. Their failure would show the bounded demo path changed; greenness still says nothing about overwrite, rollback, ownership or production durability.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain as bounded implementation regression, with Tier A return requiring typed owning repository contracts and the omitted identity, transaction, reconciliation, durability and replay proofs.

## G2 — `test_durable_seed_helpers_are_deterministic`

- Test locator: `tests/tier_a/persistence/test_fwd003_durable_sql_contract.py:31-35`; four helper outputs are compared with exact constants.
- Authority locator: Gate C bounded-demo row `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv:23`; current-alpha SQLite direction `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:104-113`.
- Authority match: deterministic demo seeding is compatible with a bounded development seam, but no governing proposition owns these four numerical constants as business or persistence semantics.
- Behaviour proved: the current helper implementation returns `0.25`, `0.75`, `0.45` and `1200` for the four selected indices.
- Limitation: no invariant over all indices, economic meaning, range, monotonicity, schema consequence, replay identity or normative ownership of the constants is proved.
- Adversarial challenge: change untested indices, introduce negative or economically invalid values outside the four examples, or preserve the outputs through unrelated implementation logic; every assertion remains green.
- Exact-surface falsifier: change any of the four selected helper outputs; its corresponding assertion at lines `32-35` must fail.
- Assertion that must fail and why: Each equality at lines `32-35` must fail when its selected helper output changes, because the test fixes four concrete implementation constants. The assertions do not constrain any untested index or confer economic or normative meaning on those values.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain only as an implementation-specific demo fixture regression unless governing authority defines the seed semantics.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `NON_AUTHORITATIVE_OBSERVATIONAL`.
- The file proves a narrow file-backed demo path and four selected helper values, while Gate C expressly withholds material ownership and wider durability authority.
