# Semantic receipt — `tests/tier_a/downstream_runtime/test_exit_close_transform_boundary_surface.py`

## File evidence

- Sequence `101`, unit `PM-015`; test SHA-256 `c8e4e3459a19b4f6cff6529008cb81d7d8db0ca77c6a919f6f812ab096ed7c14`.
- Full reads: test `1-83`; complete exit/close contracts and service; row-5.14 authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:356-371`; P1 `P1-117`/`P1-118` in `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv`.
- Raw test result: `45 passed in 0.15s`.

## G1 — `test_exit_close_handoff_rejects_transform_required_donor_payloads`

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_transform_boundary_surface.py:11-69`; 44 exact dictionary-key strings are parametrically rejected from one nested handoff preview.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:364-370` and P1 `P1-118`.
- Authority match: donor runtime, broker execution, raw ingress, capital sizing and hidden inventory writes are prohibited at the close handoff, but a finite key blacklist is only a narrow lexical clause.
- Behaviour proved: each exact listed key is found and rejected when nested in the tested dictionary shape.
- Limitation: aliases, transformed names, values carrying the same semantics, objects/collaborators, indirect imports and executable side effects remain untested.
- Adversarial challenge: rename `position_repository_write` to `persist_position` or pass a repository collaborator; the parameter set remains green.
- Exact-surface falsifier: remove one listed key from the contract guard; the `pytest.raises` assertion at lines `63-69` must fail.
- Assertion that must fail and why: at test lines `59-69`, ceasing to recognise any one parametrised exact key in the nested preview makes that case construct successfully and fails `pytest.raises(ValidationError)`. A renamed key, collaborator object or equivalent side effect is not represented by the parameter list.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain as supplemental lexical regression only after typed/executable transform-boundary tests exist.

## G2 — `test_exit_close_transform_boundary_does_not_import_donor_runtime_modules`

- Test locator: `tests/tier_a/downstream_runtime/test_exit_close_transform_boundary_surface.py:72-83`; one source file is AST-scanned for `legacy_import` and two raw substrings.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:364-370`.
- Authority match: direct donor/broker/repository-write coupling is prohibited, but one-file import/string absence cannot prove transformation or behavioural isolation.
- Behaviour proved: the scanned file contains none of the three exact lexical patterns.
- Limitation: aliases, re-exports, dependency injection, calls through imported contracts/services and equivalent side effects remain green.
- Adversarial challenge: import a helper that performs the prohibited write or use a different symbol name; all assertions remain green.
- Exact-surface falsifier: insert one exact scanned token/import pattern; an assertion at lines `81-83` must fail.
- Assertion that must fail and why: at test lines `72-83`, adding an `ImportFrom` module containing `legacy_import`, or inserting either exact source substring, breaks one of the three assertions. Re-exported helpers, aliases and behaviour reached through another dependency remain outside the scan.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace lexical absence with executable forbidden-authority and transformation proof.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Exact-key and one-file lexical checks are supplemental only and do not prove the governed exit/close transform boundary.
