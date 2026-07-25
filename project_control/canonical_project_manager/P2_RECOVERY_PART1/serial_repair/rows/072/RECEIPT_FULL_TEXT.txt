# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py`

## File evidence

- Sequence `072`, unit `PM-014`; test SHA-256 `ffd8934f8f549f54e71048ea26a03ea6210491dcb1f3bd3402846560a507c07b`.
- Full reads: test `1-91`; profile assembler `src/nvda_desk/domain/parallel_risk/minute_profile_assembly.py:1-158`; lane service `src/nvda_desk/services/parallel_risk_lane_service.py:1-229`; directly exercised Parallel Risk contracts; DMPV3 lineage law `docs/09_DMPV3_PROTOCOL_CORE.md:95-113`; Parallel Risk allocation `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; P1 decisions `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:121-122`.
- Raw test result: `2 passed in 0.15s`.

## G1 — `test_minute_profile_lineage_preserves_packet_ids_source_refs_and_forbidden_authority_trace`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:13-67`; assertions at lines `48-66` cover profile lineage, three admitted input labels, source-reference propagation and non-empty family atom lists.
- Authority locator: `docs/09_DMPV3_PROTOCOL_CORE.md:95-113` for packet lineage; `NO_VALID_AUTHORITY_RELATIONSHIP` for the separate Minute Profile, Freshness Register, Event Proximity Register, Risk Atom and Risk Family carriers.
- Authority match: parent/dependency/source identity carriage is consistent with DMPV3 lineage law, but the test locates that evidence inside an unadmitted profile and nested semantic surfaces.
- Behaviour proved: the exercised assembly copies supplied packet IDs, source artefacts, fingerprint and register references into the asserted profile fields and generated atom collections.
- Limitation: `forbidden_authority_keys_consumed == []` is a value emitted by the implementation rather than an instrumented observation of all reads; the exact admitted-input labels and nested carriers lack proposition-level ownership.
- Adversarial challenge: the assembler could consult hidden global state, consume an unrecorded authority key or mis-handle another register entry while preserving every asserted lineage value.
- Exact-surface falsifier: remove an asserted parent/dependency/source ID or source reference so an assertion at lines `48-65` fails; this falsifies the bounded carriage only, not the missing carrier authority.
- Assertion that must fail and why: lines `48-53` fail if any supplied bootstrap, parent, dependency, source-artifact or fingerprint value is not copied into the profile; lines `59-65` fail if the asserted source references are not propagated into snapshots/atoms or if a family loses every dominant atom. Line `53` merely reads the assembler's declared empty forbidden-key list and does not instrument hidden consumption.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after the profile and nested carriers are proposition-level and vocabulary admitted, or relocate the lineage proof to canonical DMP/lane surfaces.

## G2 — `test_service_optional_profile_carries_lineage_without_hidden_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lineage_completeness.py:69-91`; assertions at lines `87-91` check source artefact, fingerprint, an empty forbidden-key list and two false authority flags.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for an optional Minute Profile output and its authority-flag schema.
- Authority match: the asserted no-capital intent aligns with the Parallel Risk boundary, but false labels on an unadmitted optional product do not establish behavioural non-interference.
- Behaviour proved: one optional service invocation emits a profile carrying the supplied source artefact and fingerprint and serialises the asserted false flags.
- Limitation: the test does not compare service outputs with and without the option, instrument side effects, reject forbidden authority payloads or prove that the empty forbidden-key list is complete.
- Adversarial challenge: enabling the profile could mutate the lane packet, call a capital service or read a hidden workbook while preserving the asserted fields.
- Exact-surface falsifier: change the profile’s asserted source artefact or fingerprint so an assertion at lines `87-88` fails; the false-flag assertions at lines `90-91` remain only declarative evidence.
- Assertion that must fail and why: line `87` fails if the optional profile loses the supplied source artefact and line `88` fails if its fingerprint changes. Lines `89-91` fail only when the profile's own trace/flag values change; they would stay green if enabling the option caused an external capital call or mutated an unasserted lane field.
- Semantic relation: `authority_missing`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact ownership of the optional product and behavioural non-authority proof, including before/after lane equivalence and side-effect rejection.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the observed packet/source lineage carriage as implementation evidence; current Tier A placement is not admitted for the unowned Minute Profile and nested register/atom/family semantics.
