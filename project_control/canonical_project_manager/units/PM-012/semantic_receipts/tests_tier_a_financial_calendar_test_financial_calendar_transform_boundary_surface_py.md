# Semantic receipt — `tests/tier_a/financial_calendar/test_financial_calendar_transform_boundary_surface.py`

## 1. Process record

- Sequence: `011`
- Unit: `PM-012`
- Test SHA-256: `c1cca4dfddcbaf757d1b150e261044c9103a3468b83d1ac9ffb48671e021c6e4`
- Test read in full: lines `1-61`.
- Exercised static-analysis targets read in full: `src/nvda_desk/contracts/reference_data.py` lines `1-75`, `src/nvda_desk/calendar/reference/importer.py` lines `1-135`, `src/nvda_desk/calendar/reference/projection.py` lines `1-253`, `src/nvda_desk/calendar/operational/events.py` lines `1-155`, and `src/nvda_desk/adapters/ingress/calendar_feed.py` lines `1-12`.
- Registry and proof-block routes inspected: `config/retained_test_registry.yaml:457-478` and `config/proof_blocks.yaml:515-530`.
- No fixture, parametrisation, setup/teardown, monkeypatch or runtime implementation call.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/financial_calendar/test_financial_calendar_transform_boundary_surface.py -q` returned `2 passed in 0.05s`, exit `0`.

## 2. Complete file restatement

The file parses five selected financial-calendar Python files into ASTs. It first rejects imports whose module names begin with one of eight hard-coded prefixes. It then collects every class and function name from those files and requires disjointness from six hard-coded donor-style symbol names.

The test does not execute calendar import, reference projection, operational query, adapter behaviour, candidate/capital non-interference, four-layer ownership, lineage, precedence, supersession, degradation, provider substitution or runtime composition. It can pass after an unlawful dependency or owner is renamed, dynamically imported, injected through a local wrapper, or placed in an unlisted financial-calendar file. It can also fail on a harmless helper that happens to reuse one blacklisted name.

## 3. Authority context

- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-119` establishes exactly four calendar business layers and their owners. Implementations, repositories and packet classes are carriers rather than additional business layers.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:160-170` permits provider replacement only behind the typed contract for the same layer and preserves calendar separation from candidate formation, risk ownership, capital, placement and execution.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:186-201` assigns the surface to financial-calendar authority, prohibits candidate formation, trading instruction, capital sizing and hidden online mutation, and retains `thin_seam` implementation status.
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-36,49-59` requires exact proposition traceability and says automated path/keyword similarity, file presence, import success and assertion counts are not semantic proof.
- The retained registry says this family proves absence of donor event-service/runtime owners and six donor service symbols (`config/retained_test_registry.yaml:457-478`), but registry admission is historical evidence and cannot supply missing normative authority.
- No exact normative proposition in the fully read authority corpus establishes these eight module-prefix spellings or six symbol spellings as the lawful complete transform-boundary definition.

## 4. Assertion group 1 — selected files avoid eight prohibited import prefixes (`39-51`)

1. **Behaviour:** AST-walks imports in five selected files and fails if an imported module starts with any hard-coded prefix.
2. **Authority meaning:** financial-calendar ownership must remain separate from candidate formation, risk, capital, placement and execution authority.
3. **Fit:** related boundary intent, but the exact module prefixes and selected-file set are implementation heuristics rather than a proposition-defined owner boundary.
4. **Proved:** none of the five current files contains a syntactic `import` or `from` statement beginning with the eight tested strings.
5. **Not proved:** absence of unlawful authority, dynamic imports, dependency injection, wrapper imports, imports in other calendar files, indirect dependencies, runtime calls, dataflow or output non-interference.
6. **Falsifier:** add a direct matching import to one selected file.
7. **Required failure:** `violations` becomes non-empty and assertion `51` fails.
8. **Authority-violating implementation that passes:** place candidate-formation or capital-sizing logic locally, import it through a renamed wrapper, or add it to an unlisted file.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `token_only`.
11. **Disposition/gate:** repair required; replace broad prefix heuristics with proposition-bound dependency and behavioural non-interference proof.

## 5. Assertion group 2 — selected files avoid six donor-style symbol names (`54-61`)

1. **Behaviour:** collects class/function names and requires them to be disjoint from six literals.
2. **Authority meaning:** donor service architecture must not be reintroduced as native calendar authority.
3. **Fit:** historical migration warning only; the six names are not an exact current normative proposition and cannot define semantic equivalence.
4. **Proved:** those six spellings are absent from class/function declarations in the selected files.
5. **Not proved:** absence of donor behaviour, renamed service architecture, local event-store ownership, hidden orchestration or unlawful calendar mutation.
6. **Falsifier:** declare any blacklisted name in one selected file.
7. **Required failure:** `observed_symbols.isdisjoint(...)` becomes false at `61`.
8. **Authority-violating implementation that passes:** recreate the same donor service under different names; conversely a harmless compatibility helper using one listed name fails.
9. **Semantic relation:** `no_semantic_fit` as current authority proof; `historical_observational` only as migration evidence.
10. **Proof strength:** `token_only`.
11. **Disposition/gate:** repair required; prove forbidden behaviour/ownership, not donor vocabulary.

## 6. File-level disposition

- Assertion groups: `2`.
- Explicit proposition relationships: `2`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Reason: both groups pass, but they prove only the absence of selected import/name tokens in five files. The authority requires semantic ownership and decision-boundary behaviour. Renaming, indirection or moving unlawful behaviour leaves this test green.
- P3 repair gate: derive a bounded dependency rule from exact owner propositions, cover the complete declared financial-calendar package or an authoritative allowlist, and add behavioural negative tests showing calendar inputs cannot originate candidate, capital, placement, execution or hidden mutation authority.
- No implementation or test mutation executed.
