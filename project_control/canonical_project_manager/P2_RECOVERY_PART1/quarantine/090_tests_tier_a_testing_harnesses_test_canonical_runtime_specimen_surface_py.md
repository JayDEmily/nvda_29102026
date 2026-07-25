# Reconstructed semantic receipt — `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py`

- Sequence `090`, PM-014; test SHA-256 `a698381377a9785a6748fc183bc860f5abddfc35df8765f80f6e858e8af6746e`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: repository paths, fixtures and standard-library helpers referenced directly by the test.
- Surviving decision summary: The test proves a test-harness shell, path basenames and copied IDs. It neither reads/validates fixtures nor proves replay meaning or isolation; no-entry/no-API is only two source-string absences. Retain as tooling evidence, not Tier-A production authority.

## Complete test restatement

- Lines `22-31` `test_canonical_runtime_specimen_surface_is_present`: executes the named specimen/boundary and observes checks at lines `24, 26, 28, 29, 30, 31`. The exact assertions are enumerated in the relationship sections below.
- Lines `34-58` `test_canonical_runtime_specimen_surface_stays_test_only_and_fixture_backed`: executes the named specimen/boundary and observes checks at lines `36, 38, 52, 53, 54, 55, 56, 57, 58`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_canonical_runtime_specimen_surface_is_present`

- Test locator: `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py:22-31`. Checks: L24 assert `package_module.__name__ == "nvda_desk.testing.harnesses"`; L26 assert `harness_module.__name__ == "nvda_desk.testing.harnesses.canonical_runtime"`; L28 assert `_require_attr(package_module, "CanonicalRuntimeHarness") is getattr(package_module, "CanonicalRuntimeHarness")`; L29 assert `_require_attr(package_module, "CanonicalRuntimeSpecimen") is getattr(package_module, "CanonicalRuntimeSpecimen")`; L30 assert `_require_attr(package_module, "build_canonical_runtime_specimen") is getattr(package_module, "build_canonical_runtime_specimen")`; L31 assert `_require_attr(harness_module, "CanonicalRuntimeHarnessPaths") is getattr(harness_module, "CanonicalRuntimeHarnessPaths")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: The test proves a test-harness shell, path basenames and copied IDs. It neither reads/validates fixtures nor proves replay meaning or isolation; no-entry/no-API is only two source-string absences. Retain as tooling evidence, not Tier-A production authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## G2 — `test_canonical_runtime_specimen_surface_stays_test_only_and_fixture_backed`

- Test locator: `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py:34-58`. Checks: L36 assert `harness_module.__name__ == "nvda_desk.testing.harnesses.canonical_runtime"`; L38 assert `build_specimen is getattr(harness_module, "build_canonical_runtime_specimen")`; L52 assert `specimen.fixture_paths.replay_root.name == "replay"`; L53 assert `specimen.fixture_paths.trace_review_root.name == "trace_review"`; L54 assert `getattr(specimen.fixture_paths, "dmp" "_v3_root").name == "dmp_v3"`; L55 assert `getattr(specimen.replay_lineage, dependency_key) == ["pkt-1", "pkt-2"]`; L56 assert `specimen.trace_review_pack.scenario_ids == ["scenario-a"]`; L57 assert `"nvda_desk.entry" not in source_text`; L58 assert `"nvda_desk.api" not in source_text`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: the group is useful regression/structure evidence, but it does not exercise enough governed semantics to become an authoritative proof relationship.
- What is not proved: The test proves a test-harness shell, path basenames and copied IDs. It neither reads/validates fixtures nor proves replay meaning or isolation; no-entry/no-API is only two source-string absences. Retain as tooling evidence, not Tier-A production authority.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `token_only`; file disposition `NON_AUTHORITATIVE_OBSERVATIONAL`.

## File decision

- Assertion groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
