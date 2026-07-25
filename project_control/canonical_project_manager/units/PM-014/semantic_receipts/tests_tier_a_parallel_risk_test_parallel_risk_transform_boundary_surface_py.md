# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py`

## File evidence

- Sequence `083`, unit `PM-014`; test SHA-256 `dd4a7fcbb935ddcf763e8f8dd77dbc0d5d2180c57be3a5f4f636c6acdf717546`.
- Full reads: test `1-94`; all five files enumerated by `ACTIVE_PARALLEL_RISK_FILES`; directly inspected `ParallelRiskEnvelope` and `ParallelRiskLanePacket` contracts; donor-evidence vocabulary `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:144-149`; native carry-forward law `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:508`; Parallel Risk prohibitions `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Raw test result: `3 passed in 0.14s`.

## G1 — `test_active_parallel_risk_files_do_not_import_donor_risk_lane_stack`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py:61-74`; assertion at lines `72-74` requires no import matching four forbidden prefixes across five enumerated files.
- Authority locator: `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:144-149` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:508`.
- Authority match: donor source must not become live native authority, but the test scans only five files and four historical import prefixes.
- Behaviour proved: those exact files contain no direct AST import matching the listed prefixes.
- Limitation: renamed modules, relative/dynamic imports, transitive dependencies and other active Parallel Risk files remain unobserved.
- Adversarial challenge: move donor logic into `nvda_desk.compat.risk` or import it through a helper; every assertion remains green.
- Exact-surface falsifier: add a direct import matching one listed prefix to one enumerated file so the assertion at lines `72-74` fails.
- Assertion that must fail and why: The import assertion at lines `72-74` is the only detector for this group: adding one forbidden direct import changes `forbidden` from empty to non-empty. Its failure would prove the finite prefix scan noticed that exact dependency, while leaving renamed, dynamic and transitive donor paths outside the proof.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; return with a complete governed active-surface inventory and dependency/behavioural proof rather than a finite prefix blacklist.

## G2 — `test_active_parallel_risk_files_do_not_redeclare_transform_required_donor_symbols`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py:77-85`; assertion at lines `83-85` requires no top-level definition matching four forbidden symbol names in the same five files.
- Authority locator: `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md:144-149` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:508`.
- Authority match: the no-live-donor intent is relevant, but exact symbol-name absence is not proof that donor behaviour was transformed or excluded.
- Behaviour proved: the four listed top-level names are absent from the enumerated files.
- Limitation: aliases, nested definitions, equivalent renamed classes/functions and copied logic are not detected.
- Adversarial challenge: reproduce the donor implementation under `NativeRiskEvaluator` and preserve all assertions.
- Exact-surface falsifier: add one exact prohibited top-level name so the assertion at lines `83-85` fails.
- Assertion that must fail and why: The set-intersection assertion at lines `83-85` must fail when one listed donor symbol is declared because that name enters both `declared` and `PROHIBITED_DONOR_SYMBOLS`. Failure would validate only the exact-name detector; semantically equivalent renamed code would still escape.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; return with semantic provenance/transform evidence for all active surfaces.

## G3 — `test_parallel_risk_envelope_and_lane_packet_remain_risk_only_carriers`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_transform_boundary_surface.py:88-94`; assertions check disjointness from five field names and one default decision-authority string.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Authority match: independent-risk/no-capital boundaries are authoritative, but five field names plus a declaration string under-observe the behavioural boundary.
- Behaviour proved: the two current model signatures omit the listed fields and the envelope defaults to the asserted string.
- Limitation: synonymous/nested authority fields, methods, callbacks, consumers and side effects remain possible; a label does not enforce non-authority.
- Adversarial challenge: add `deployable_fraction`, a broker callback or downstream mutation without any prohibited field name.
- Exact-surface falsifier: add one listed field to either model or change the default authority string so an assertion at lines `92-94` fails.
- Assertion that must fail and why: The disjoint-field assertions at lines `92-93` must fail if either carrier acquires one listed downstream field, and line `94` must fail if the declared authority label changes. Those assertions detect the named schema/default mutations only; they do not detect aliases, methods or side effects.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `signature_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; return with structural schema rejection, side-effect instrumentation and complete active-path coverage.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The governing no-donor and no-capital boundaries exist, but this file reduces them to incomplete path, prefix, symbol and field-name blacklists. Repair the proof family before Tier A admission.
