# Semantic receipt — `tests/tier_a/adapters_ingress/test_external_source_transform_boundary_surface.py`

## 1. Process record

- Sequence: `003`
- Unit: `PM-012`
- Test SHA-256: `e3772b152d9c5aedd12a1ec3c19fbb68999524a4c1782402f683c8356d8606d7`
- Test read in full: lines `1-75`.
- Exercised files read in full: `src/nvda_desk/contracts/external_source.py`; `src/nvda_desk/adapters/ingress/calendar_feed.py`; `market_snapshot_feed.py`; `options_surface_feed.py`.
- Local helper `_imported_modules` and all AST traversal paths read in full.
- No fixtures, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/adapters_ingress/test_external_source_transform_boundary_surface.py -q` returned `3 passed in 0.05s`, exit `0`.

## 2. Complete file restatement

The file statically parses four selected row-5.1 files. It checks that their direct import roots exclude six named client libraries; that their direct imported module strings do not start with five named decision/persistence package prefixes; and that their defined class/function names exclude seven donor-style authority names.

It observes only current source text parsed by Python AST. It does not execute adapters, resolve transitive or dynamic imports, inspect calls or side effects, prove controlled registration, exercise provider substitution, preserve source identity/time, or detect unlawful authority under an unlisted import path or renamed symbol.

## 3. Authority context

- `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`, requires external adapter/source-reader ownership, typed native carriers, provider-semantic termination and exclusion of candidate/risk/capital/broker/state/review decisions.
- `N04-005`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:86-94`, requires replaceable infrastructure to be selected at an application assembly boundary rather than instantiated inside unrelated domain decisions.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353` explicitly permits bounded adapter-import checks and forbids live clients and downstream decision smuggling, while limiting claims to authority-readiness.
- `C-003`, `GATE_C_TEST_REQUIREMENTS.tsv:4`, requires actual adapter composition with the authoritative contract and identity/temporal lineage. This file does not prove that requirement.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:17,92,490-508` makes legacy structure non-authoritative and requires lawful target ownership before carry-forward. It does not normatively enumerate the seven forbidden donor symbol spellings used here.

## 4. Assertion group 1 — six forbidden client import roots (`50-55`)

1. **Behaviour:** AST-parses the four selected files and requires direct import roots to exclude `aiohttp`, `httpx`, `ibapi`, `openai`, `requests`, and `websocket`.
2. **Authority meaning:** live client implementation is outside the bounded 5.1 seam and concrete infrastructure should not be hidden in the transform boundary.
3. **Match:** correct boundary and lifecycle, but only a selected static-import blacklist is observed.
4. **Proved:** none of the six root names appears in a direct `import` or `from` statement in those files.
5. **Not proved:** no `urllib`, `socket`, dynamic import, transitive dependency, subprocess, runtime client or network side effect; no live client in another file.
6. **Falsifier:** add `import requests` to `market_snapshot_feed.py`.
7. **Required failure:** assertion line `55`.
8. **Relation:** `bounded_separable_clause`.
9. **Strength:** `token_only`.
10. **Disposition/gate:** bounded clause can remain current, but it cannot prove C-003 or repository-wide live-client absence.

## 5. Assertion group 2 — five forbidden domain import prefixes (`58-64`)

1. **Behaviour:** requires direct imported module strings not to start with capital, downstream, repositories, risk or runtime package prefixes.
2. **Authority meaning:** the external transform boundary must not own downstream decisions or persistence and must preserve dependency direction.
3. **Match:** owner and abstraction match `N04-002`/`N04-005`, but only direct imports under five current prefixes are checked.
4. **Proved:** the selected files have no direct import matching those prefixes.
5. **Not proved:** no indirect call, alias, relocated package, dynamic import, injected dependency or decision behaviour.
6. **Falsifier:** add `from nvda_desk.capital.service import allocate`.
7. **Required failure:** loop assertion line `64` with the offending module.
8. **Relation:** `bounded_separable_clause`.
9. **Strength:** `token_only`.
10. **Disposition/gate:** bounded clause is supportable, not behavioural architecture proof.

## 6. Assertion group 3 — seven forbidden donor-style defined names (`67-75`)

1. **Behaviour:** collects every class/function definition name and requires disjointness from seven hard-coded donor-style names.
2. **Authority meaning proposed by the test:** legacy/donor authority must not define the native external-ingress owner.
3. **Mismatch:** current authority prohibits legacy placement/meaning from becoming native authority without adjudication, but it does not prohibit these exact spellings. Name equality does not establish donor provenance, owner, behaviour or authority.
4. **Proved:** none of the seven literal names is currently defined in the selected files.
5. **Not proved:** no donor behaviour, allocation, execution, sizing or live gateway authority exists under another name; no harmless use of a listed name could be lawful.
6. **Adversarial violating implementation:** define `class CapitalChooser` that performs unlawful position sizing. The test still passes. Conversely, define a harmless parsing helper named `AllocationDecision`; the test fails without a normative violation.
7. **Required failing assertion for the actual authority violation:** none necessarily fails for the renamed unlawful class.
8. **Relation:** `related_but_not_proved`.
9. **Strength:** `token_only`.
10. **Disposition/gate:** `BLOCKED_P3_REPAIR`. P3 must either cite exact authority for a bounded reserved-name list or replace the assertion with proof of forbidden dependencies/behaviour/ownership.

## 7. Whole-file challenge and final disposition

A system can preserve all three assertions while using `socket`, dynamically importing a client, calling a downstream decision through a neutral package, or implementing allocation under a renamed class. Therefore the file is not full external-transform or composition proof. The third group has no exact normative relationship and is part of the file's pass condition.

`BLOCKED_P3_REPAIR`

- Assertion-group count: `3`
- Relationship count: `3`
- Return gate: P3 repair of the donor-name assertion; no source/test edit was performed in P2.
