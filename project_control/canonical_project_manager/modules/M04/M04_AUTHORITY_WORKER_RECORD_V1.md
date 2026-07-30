# M04 Authority Worker Record V1

## Assignment

| Field | Value |
|---|---|
| Worker | `Lane 2AW` |
| Tester | `Lane 2AT` |
| Unit | `M04-PROOF-MLC-A-V1` |
| Module | `M04 packet_protocol` |
| Contract | `K07 DmpV3Packet` |
| Leaf | `MLC-A — Authority sufficiency` |
| Result label | `PROPOSED_M04_AUTHORITY_V1_AWAITING_LANE_2AT` |

## Result

`BLOCKED_MISSING_NORMATIVE_AUTHORITY:For every governed DMPV3 packetrole, which execution-context identities (traceid, runid, scenarioid), lineage fields (parentids, dependencyids, derivedfrom, replayref, sourceartifactids, inputfingerprint, reviewtraceid, replaytraceid, decisiontraceid) and validation checks are mandatory, conditionally required, optional or not applicable, and what exact rejection, stand-down, non-admission or diagnostic/degraded outcome applies when each is absent?`

Current numbered authority is sufficient for the common M04 invariants listed below. It is not sufficient for the assignment's complete role-specific contract because it expressly defers the mandatory/optional/conditional/not-applicable lineage matrix and exact per-role validation checks. The missing matrix is material: the retained D-010 evidence records an actual conflict over whether a reference packet may lawfully omit caller-owned runtime context.

This is an authority result only. It does not route or observe tests, specify proof, mutate normative meaning, or open implementation.

## Accepted owner, surface and contract

| Item | Accepted meaning | Locators |
|---|---|---|
| Architecture surface | `5.6 DMPV3 packet carriage`; structural status `Locked`; implementation truth `thin_seam`; deliberate inter-module carriage only | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:50`; workbook `Surface Map!A7:O7`; JSON selector `.surfaces[] | select(.surface_id=="5.6")` |
| Owner module | `M04 packet_protocol`; no runtime prerequisite; no owned state | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:150-173,184-202`; `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md:125-145,200-209`; workbook `Target Modules!A6:Q6`; JSON selector `.modules[] | select(.module_id=="M04")` |
| Owned authority | DMPV3 outer-envelope validation and deliberate packet carriage | `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:160`; workbook `Target Modules!E6`; JSON `.modules[] | select(.module_id=="M04") | .owns` |
| Prohibited authority | Raw-ingress carriage, domain decisions, identity fabrication, time fabrication, payload ownership and persistence truth by implication | `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`; `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:160`; `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md:133,206-207` |
| Public contract | `K07 DmpV3Packet`: one common outer envelope; role-specific IDs are supplied, not fabricated | workbook `Contracts!A8:E8`; JSON selector `.contracts[] | select(.contract_id=="K07")` |
| Historical obligations | `C-010 → D-010` and `C-016 → D-016` remain traceability obligations, not present implementation authority | `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:11,17`; `GATE_C2_PROOF_ENVELOPE_REGISTER.tsv:8,11`; `gate_c2_proof_envelopes/D-010.md:1-71`; `gate_c2_proof_envelopes/D-016.md:1-71` |

## Exact numbered authority propositions

### Common envelope and boundary

1. Every live packetised inter-module output uses one canonical DMPV3 outer envelope; the envelope normalises carriage without merging responsibility or meaning (`docs/01_NORMATIVE_CORE.md:81-85`; `docs/04_TECHNICAL_ARCHITECTURE_CORE.md:24-50`; `docs/09_DMPV3_PROTOCOL_CORE.md:19-29`).
2. The canonical shell carries the complete outer field set, including packet role, producer, lineage, validation, summary, typed data and bounded extensions (`docs/09_DMPV3_PROTOCOL_CORE.md:31-58`).
3. DMPV3 begins at deliberate live inter-module boundaries. It is not the universal raw-source, prepared-data or internal-stage carrier and does not replace typed domain contracts (`docs/03.1_DOMAIN_MODEL_WORKING.md:77-87`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:74-84`; `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-234`).
4. Readers use `packetrole`, `producer.grammar_role`, `producer.behaviour_class` and `dataschema`; payload shape alone does not establish carriage meaning (`docs/09_DMPV3_PROTOCOL_CORE.md:78-93`; `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:17-41`).

### Identity, lineage and time

5. M04 may create packet-occurrence identity and emission metadata only inside packet-carriage authority. It may not create source, domain, decision, state, policy, receipt, trace, run or scenario authority (`docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:74-84`; `docs/09.1_DMPV3_PROTOCOL_WORKING.md:11-23`).
6. `source + id` identifies a packet occurrence. It does not become an upstream source artefact, domain object, decision, position, execution, state, receipt or preserved-original identity (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:13-23`).
7. `traceid`, `runid` and `scenarioid` are distinct execution-context identities supplied by their owning boundary. A packet builder propagates them and must not derive trace/run from packet ID or silently default a generic scenario such as `live` (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:25-39`).
8. Lineage fields have separate declared meanings; immediate parents, material dependencies, principal domain derivation, replay reference, source artefacts, semantic input fingerprint and review/replay/decision traces are not interchangeable (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:41-59`).
9. Packet `time` is packet emission time, not source observation time. Source temporal truth remains separately carried at its lawful precision (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:63-79`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:43-72`).
10. A packet or execution-context identifier must not substitute for an absent source, capture, domain, decision, position, execution or state identifier (`docs/03.1_DOMAIN_MODEL_WORKING.md:41-55`; `docs/05.1_GUARDRAILS_WORKING.md:33-44`).

### Validation, reproduction and side effects

11. Validation records only the checks actually performed for the exact packet role and boundary. A mandatory structural, identity, lineage, semantic or authority failure rejects governed emission, stands down, remains non-admitted, or uses a separately admitted diagnostic/rejection contract (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:81-91`).
12. `degraded` is lawful only when the role contract permits limited non-binding carriage and names the limitation. Model construction, default `schema_validation=true` or an empty violation list is not proof of validity (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:83-91`).
13. The summary is a deterministic human-facing projection and cannot create or override domain authority; extensions cannot hide mandatory fields, lineage or authority (`docs/09.1_DMPV3_PROTOCOL_WORKING.md:93-119`).
14. Preserved-occurrence replay keeps the original envelope unchanged. Newly emitted replay output is a new occurrence. Domain-result equivalence uses the semantic result and material-version fingerprint, excluding regenerated packet identity/time and current wall-clock metadata (`docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:113-127`; `docs/09.1_DMPV3_PROTOCOL_WORKING.md:121-129`; `project_control/normative_authority_top_down_alignment/normative_completion_decisions/N-09_AUTHORITATIVE_REPLAY.md:21-44`).
15. M04 owns no domain state and no persistence side effect. Its bounded side effect is creation/emission of the validated packet occurrence; payload meaning, domain state and authoritative evidence remain with their owners (`docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:17-41`; `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:20-49`; accepted M04 architecture rows cited above).

## Input → validation/carriage → output

| Phase | Governed facts |
|---|---|
| Input | One strongly typed, module-owned payload contract; packet role; producer identity; packet source context; caller/owner-supplied execution context; owner-supplied source/domain/decision/state/dependency identities; exact material lineage; role-specific validation evidence; explicit packet emission metadata or an authorised packet-occurrence metadata source. |
| Validation and carriage | Validate the canonical shell, `source + id` occurrence identity, producer/role/schema declarations, exact role-required execution context, typed payload, lineage semantics, validation status and extension limits. Reject or withhold when a mandatory owner fact is absent. Do not carry pre-DMP raw/prepared inputs as though DMP were their native storage or input grammar. |
| Output | One DMPV3 packet occurrence with canonical envelope and typed payload. The packet carries the producing domain's result; it does not become that result's semantic owner. Domain reproduction compares governed semantic content/fingerprint, not current emission metadata. |

## Identity, lineage, time, state and side effects

| Concern | Owner and rule | M04 limit |
|---|---|---|
| Packet occurrence `source + id` | Packet-carriage authority creates or validates the occurrence identity within its declared source context | Must not reuse it as source/domain/state truth |
| Producer identity | Emitting module truth: module, version, instance, grammar role, behaviour class and narrower stage where one exists | Must not infer it from payload shape |
| `traceid`, `runid`, `scenarioid` | Boundary owning the execution, replay or scenario context | Propagate/validate only; no derivation or generic defaults |
| `parentids` / `dependencyids` | Producing domain and dependency owners identify actually consumed upstream material | Preserve exact causal versus non-parent dependency meaning |
| `derivedfrom` | Owner of the principal upstream domain output | No concatenated plural or invented substitute |
| `sourceartifactids` / `inputfingerprint` | Source/capture/preparation owners | Preserve declared evidence and semantic fingerprint; a hash alone is not retrievable evidence |
| Replay/review/decision trace IDs | Respective replay, review and decision owners | Carry only where their role contract requires them |
| `time` | Packet emission metadata | Never source observation time or deterministic domain-result authority |
| State | None owned by M04 | Packet carriage does not create persistence truth |
| Side effects | Bounded packet creation/emission | No domain decision, source admission, capital, execution, inventory, close, review or persistence mutation |

## N-package and C/D evidence reconciliation

| Evidence | Contribution to M04 | Limit |
|---|---|---|
| `N-03` | Defines mandatory prepared identity, source/capture references, versions, temporal facts, fingerprints, validation/completeness and source artefact lineage (`N-03...md:21-43`; `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:17-89`) | Does not allocate those facts into each DMP packet role |
| `N-05` | Defines immutable common context, narrow stage carriers, reference consistency and deterministic reconstruction inputs (`N-05...md:21-43`; `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:150-217`) | Does not define the K07 per-role mandatory lineage/validation profile |
| `N-09` | Defines preserved occurrence versus semantic re-execution, complete authoritative envelope, isolated/no-side-effect replay and emission-metadata exclusion (`N-09...md:21-44`; `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:145-217`) | Does not decide which K07 lineage fields are mandatory for each packet role |
| `C-010 / D-010` | Requires role-specific IDs, source artefact lineage, deterministic reproduction and pre-DMP separation (`B02_TEST_DESIGN.md:53-73`; `D-010.md:1-71`) | D-010 is closed because a reference-packet test permits missing runtime context while the proposed Gate C test rejects it; the exact exception boundary is unresolved |
| `C-016 / D-016` | Requires source artefact IDs, supplied context IDs, dependency semantics and domain output independent of emission time (`B04_TEST_DESIGN.md:53-73`; `D-016.md:1-71`) | D-016 remains dependent on D-010 and prepared-lineage proof; its historical readiness text does not supply missing normative meaning |

## Contradictions and missing meaning

### M04-AUTH-GAP-001 — role-specific identity and lineage matrix absent

`docs/09.1_DMPV3_PROTOCOL_WORKING.md:61` says every packet role must eventually declare its mandatory, optional, conditionally required and not-applicable lineage subset, and assigns that work to Gate B. `docs/09.1_DMPV3_PROTOCOL_WORKING.md:161` prohibits inference of those checks from defaults. `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:66-80` likewise leaves the exact per-boundary mandatory replay subset to the semantic walk.

This is missing normative meaning, not an implementation detail. Without the role matrix, M04 cannot determine whether an absent field is lawful absence, degradation, diagnostic carriage or a fail-closed error.

### M04-AUTH-GAP-002 — exact validation profile absent

`docs/09.1_DMPV3_PROTOCOL_WORKING.md:83-91` requires the producer to know the checks required for the exact role. No current numbered proposition enumerates those checks for all governed packet roles.

### M04-EVIDENCE-CONFLICT-001 — reference packet exception

`project_control/normative_authority_top_down_alignment/gate_c_test_design/B02_TEST_DESIGN.md:53-73` labels C-010 ready/admitted, but the later D-010 record closes proof authority because `test_reference_packet_builder_emits_canonical_shell_and_degraded_validation_without_runtime_context` permits trace/run defaulting while the proposed C-010 test rejects missing caller-owned context (`GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv:3`; `gate_c2_proof_envelopes/D-010.md:65-71`).

The current module-local protocol makes those historical statuses evidence rather than present scheduling authority. The conflict still demonstrates why the missing role-specific exception boundary cannot be guessed from old tests.

## Exact normative return question

The routed DMPV3 authority must add one role-by-role matrix covering every governed `packetrole`, including at minimum prepared-context, serial-stage, parallel-risk, financial-calendar/reference, review/explanation, replay and separately admitted diagnostic/rejection roles. For each role it must state:

1. required/conditional/optional/not-applicable execution-context and lineage fields;
2. field owner and lawful generation/propagation rule;
3. exact structural, identity, lineage, semantic and authority checks;
4. lawful absence outcome: reject, stand down, remain non-admitted, or expressly diagnostic/degraded carriage;
5. whether any role may omit caller-owned `traceid`, `runid` or `scenarioid`, and why;
6. the typed payload and source-artifact/replay evidence required for deterministic domain reproduction.

Until that numbered authority exists, `M04-PROOF-MLC-A-V1` is blocked at `MLC-A`.

## Project Manager normative return and MLC-A recheck — 2026-07-30

Source control checkpoint: `27fa427` on `control/atlas-current-path-rebase-gate-c-continuation-v1`.

Normative return unit: `M04-K07-NORMATIVE-AUTHORITY-V1`.

The missing authority is now supplied by `docs/09.1_DMPV3_PROTOCOL_WORKING.md`, section `9.10 K07 packet-role identity, lineage, validation and outcome authority`.

### Recheck disposition

`AUTHORITY_SUFFICIENT:M04_K07_CURRENT_PACKET_ROLE_MATRIX`

The new proposition:

1. admits ten exact current `packetrole` values and makes every unlisted code/test/Atlas role non-authoritative pending a bounded amendment;
2. requires owner-supplied `traceid`, `runid` and `scenarioid` for every governed emission, including `reference_packet`;
3. classifies all nine lineage fields as required, conditional, optional or not applicable for reference, prepared, serial-stage, parallel-risk, review, replay and diagnostic/rejection roles;
4. defines ten common validation checks and exact role-specific checks;
5. defines reject, stand-down, non-admission, diagnostic/rejection and `non_authoritative_incomplete` outcomes;
6. prohibits `degraded` from excusing missing identity, required lineage, source-artifact retrievability, fingerprints or authority-boundary checks;
7. preserves M04 as packet carriage and validation only.

### Historical conflict reconciliation

- D-010's reference-packet exception is resolved normatively: a reference artefact without governed execution context remains a typed reference artefact; a governed `reference_packet` requires explicit owner-supplied trace, run and scenario identity. Defaulting those values is non-conforming.
- D-016's role-authority dependency is satisfied for the current K07 roles. Its historical tests are not admitted by this result and its remaining proof dependencies are assessed in later MLC leaves.
- Existing code defaults and green tests remain implementation/test evidence. They did not select the rule.

### MLC-A required record

| Required concern | Current result |
|---|---|
| Exact proposition and locator | `docs/09.1_DMPV3_PROTOCOL_WORKING.md`, section 9.10 |
| Owner and surface | M04 `packet_protocol`; surface 5.6; K07 `DmpV3Packet` |
| Input → action → output | owner-supplied typed payload/context/lineage → exact role validation and canonical carriage → one governed DMPV3 occurrence or an exact fail-closed outcome |
| Identity, lineage and time | complete role matrix; packet time remains emission time; source temporal truth remains separate |
| State and side effects | M04 owns no domain state; bounded packet creation/emission only |
| Prohibited authority | no source/domain/decision/state/persistence ownership; no identity/time fabrication; no binding use of diagnostic carriage |
| Atlas and D obligations | accepted M04/K07 cohort allocation retained; D-010 conflict resolved; D-016 authority prerequisite supplied |
| Missing or contradictory meaning | none found inside the bounded current K07 role set |

### Claim boundary and next leaf

This PM recheck closes only M04 MLC-A for the current packet-role set. It does not admit a physical test, specify proof, mutate test code, change production implementation or open Gate D.

The next lawful leaf is `M04-PROOF-MLC-R-V1`: route the physical tests that claim authority over the exact section 9.10 roles and mark unrelated tests `LEGACY_SHADOW_UNADMITTED`.

### Vocabulary scope-reopen closure

The section 9.10 packet roles are durable protocol concepts under `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`. The existing registry governed none of the ten exact role values, including the two already named by the earlier DMP working overlay. The same bounded M04 leaf therefore reopened vocabulary scope before final MLC-A closure.

Ten `add_new` decisions are recorded in section 10.14 and in the existing human registry:

`reference_packet`, `prepared_context_packet`, `stage_packet`, `parallel_risk_packet`, `review_explanation_packet`, `replay_request_packet`, `replay_result_packet`, `replay_comparison_packet`, `diagnostic_packet`, and `rejection_packet`.

The unchanged deterministic builder projected registry version `2026-07-30-m04-k07-packet-roles-v1` with 147 entries. Each role slug occurs exactly once. A validated `/tmp` build, the committed JSON, and a second independent build were byte-identical. Direct native/wrapper builder parity passed, and the existing DMPV3 vocabulary test function passed.

The required synonym-candidate audit was then run against the current governed sources. It initially surfaced 134 unresolved occurrences: 50 already present at checkpoint `27fa427`, plus 89 newly visible because the admitted packet-role lexicon gave the scanner new comparison targets. Full occurrence contexts were reviewed and recorded in the existing PM-010 semantic-disposition register: 42 governed contextual/numbered references remain lawful only in their exact propositions, and 92 implementation, test, configuration or non-governing-document observations remain occurrence-scoped quarantined evidence. No phrase was admitted as a global alias. The regenerated existing candidate report contains zero unresolved candidates, the existing touch stamp was advanced through the guarded route, and a final read-only clean check returned `candidates=0`, `vocabulary_touched=False`, `resolved_occurrences=633`.

The primary runtime does not provide `pytest`, so the requested pytest command was `BLOCKED_ENVIRONMENT` rather than passed. The pre-existing required-baseline assertion for absent `mutable_runtime_surface` remains red in both source commit `27fa427` and the current projection; the M04 vocabulary change introduced no new occurrence of that known failure.

## Project Manager MLC-R routing — 2026-07-30

Source checkpoint: `12f8105` on `control/atlas-current-path-rebase-gate-c-continuation-v1`.

Unit: `M04-PROOF-MLC-R-V1`.

Result: `ROUTING_COMPLETE:M04_K07_25_PHYSICAL_TEST_FILES`.

This leaf mechanically joined the PM-011 physical/current-route census, retained-test and proof-block routes, C-010/D-010 and C-016/D-016 records, and exact occurrences of the ten admitted section 9.10 role values or the canonical DMPV3 contract name in physical Python tests. It did not read assertions semantically, run tests, select authority by filename, admit a test, or mutate a test.

Every file below claims or consumes at least one exact K07 role/contract token and is therefore routed into MLC-O for factual observation. Route inclusion is deliberately broader than eventual admission: domain-owned tests may use a packet token without proving M04 carriage law.

| Physical test file | Mechanical K07 claim token(s) | Existing route evidence | SHA-256 |
|---|---|---|---|
| `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` | `reference_packet` | PM-011 current route | `022203decd6eb9be1bafd3bc3a00d9ee3bba9a69e9262e11f3efea86526494f7` |
| `tests/tier_a/capital_deployment/test_capital_authority_service_surface.py` | `parallel_risk_packet` | PM-011 current route | `0081d39a103e2b92bca821e0a291fbad9d646d101fb14756829006c82a31d5b6` |
| `tests/tier_a/capital_deployment/test_capital_contract_models.py` | `parallel_risk_packet` | PM-011 current route | `9b5f0e2ad6285ecc166698777b1f88d3ee6cb917d6be02dff246919ab02ebed2` |
| `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py` | `parallel_risk_packet` | PM-011 current route | `befe79943fd9c6b83dff28cf79649772b016380935db4625dc104324ba60163d` |
| `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py` | `parallel_risk_packet`; `DMPV3` | PM-011 current route | `346f853263789c4d1011cff170832fe51fe4a284db4666fb8a63758286594f94` |
| `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py` | `parallel_risk_packet` | PM-011 current route | `5409d16b8c13017c2a333e006d0493a2d1f4e3998f12fe514b0b7a65c5f04d1f` |
| `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py` | `parallel_risk_packet` | PM-011 current route | `6eceb47ddfa298b45bb4121a3a2a65c77118a7b2aedf769fd3c09c65d40f65ba` |
| `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py` | `stage_packet` | D-010; D-016; PM-011 current route | `0e705c9a2dd5afea58e6c4414a78b98731685bfa8d8a8774c18683205391ac29` |
| `tests/tier_a/normative_authority/test_gate_c_remaining_normative_contracts.py` | `parallel_risk_packet` | PM-011 current route | `d1544b9fa8fd2c8339ed4cbc83694fb2cbfbbf93823d85c7d12fecd61029a98b` |
| `tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py` | `stage_packet` | D-010; PM-011 current route | `45dfe7e719fb31b6b8aae23b28cc0bd82d8cdcec3456f46acf9b48286ecd107d` |
| `tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py` | `DmpV3Packet` | D-010; PM-011 current route | `40acde2f80b7e2d69b3d5c62f65105e48fe1449eec92f2686c67f2b79a76b699` |
| `tests/tier_a/packets/test_fwd004_reopened_row_packet_carriage_proof.py` | `reference_packet`; `stage_packet`; `parallel_risk_packet` | D-010 | `d228f89d61b4844823c44f599f7274662355193b87e75a5d9dde867ae406f4b7` |
| `tests/tier_a/packets/test_reference_packet_carriage.py` | `reference_packet`; `prepared_context_packet`; `stage_packet`; `review_explanation_packet`; `DmpV3Packet` | D-010; PM-011 current route | `61a55a2caed8bb9e0497a8a980d413cb0790a8a3d1c3fa8afc07eed93b37ca41` |
| `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py` | `parallel_risk_packet` | PM-011 current route | `ec02a46e2c049f3b84c4b7dbb2cf1866bca026089aa5c650940cf8428fb1953e` |
| `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py` | `stage_packet` | PM-011 current route | `17c4061336d249f87b27a1fd21d33f656210c7d6a38482e9adf795773b68fedd` |
| `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py` | `stage_packet`; `parallel_risk_packet` | PM-011 current route | `8edcda5980a1d6a7466f612e7fd2fff25e3b118bf54620b9f127c528f7dd283c` |
| `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py` | `parallel_risk_packet` | PM-011 current route | `f037de5d9a1116e1e5cbe3ba0a8850c1be9281b003e0cb8a2d37e3884898fbe7` |
| `tests/tier_a/runtime/test_fwd012_reopened_row_serial_cognition_spine_proof.py` | `stage_packet` | D-016 | `4f7f9cf6627f8c00257cfbd65b45274b658aea50af2b9f9c3cc7e554242a4cfb` |
| `tests/tier_a/runtime/test_runtime_orchestrator_surface.py` | `stage_packet` | PM-011 current route | `64a770bb18e66fd93bc98fcd1cd26451eb7f8240f7bef1347d9d38a3e5ab6863` |
| `tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py` | `stage_packet` | D-016; PM-011 current route | `ee0a115da8c80b7b0764b92a2917033f960178f8ff23bdfc77b7244fe932debc` |
| `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py` | `stage_packet` | PM-011 current route | `f67b69999aace0eb663cb0c1793a5e64ec024f9a4aaa60972d110d8260a7ca60` |
| `tests/tier_a/upstream_cognition/test_fwd009_reopened_row_prepared_ingress_runtime_context_proof.py` | `prepared_context_packet` | exact K07 symbol; no pre-existing PM-011 current route | `a3300de568165f2609a7b7de5d6ae811bd932a0d24ccf381e08bc12deff0ebb9` |
| `tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py` | `prepared_context_packet` | PM-011 current route | `bb0d40859b133970d47d730d0061534fc6b7343cb955cf52b5649b9b216e39c8` |
| `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py` | `DmpV3Packet` | PM-011 current route | `48e171e51b6b03bd8fd2239817d12f3ae1d2d7f147a082b8393eef7b50999c89` |
| `tests/tier_b/capital_deployment/test_capital_deployment_transform_boundary_surface.py` | `parallel_risk_packet` | PM-011 current route | `252905dbfef7502920b58a9c74e049531e4f0894a23991b3efb2ed2f2aff28e7` |

No physical Python test contains the exact current values `replay_request_packet`, `replay_result_packet`, `replay_comparison_packet`, `diagnostic_packet` or `rejection_packet`. That is a routing fact only; it does not establish a proof gap until MLC-O and MLC-D determine what the routed tests actually cover.

The other 154 files in the accepted 179-test census remain `LEGACY_SHADOW_UNADMITTED` for this M04 leaf. This is a neutral routing status, not retirement or rejection.

### MLC-R claim boundary and next leaf

MLC-R is complete. No test was run, observed, admitted, rewritten or assigned a proof strength. No numbered authority, vocabulary, runtime configuration or production source changed.

The next lawful leaf is `M04-PROOF-MLC-O-V1`: read each of the 25 routed files in full and record starting input/state, action, exact assertion/absence/exception, public seam, unobserved surfaces and any scoped result actually run. Files may be grouped only when homogeneous, and each physical file must retain a distinct observation.

## Project Manager MLC-O factual observation — 2026-07-30

Source checkpoint: `6d3ec80` on `control/atlas-current-path-rebase-gate-c-continuation-v1`.

Unit: `M04-PROOF-MLC-O-V1`.

Result: `OBSERVATION_COMPLETE:M04_K07_25_PHYSICAL_TEST_FILES`.

All 25 routed files were read in full without mutation. Their source hashes are fixed in `raw_validation/mlc_o_v1/FULL_READ_MANIFEST.tsv`. The complete routed command under repository-pinned `pytest==9.0.3` collected 357 tests and returned 347 passed / 10 failed. The ten failures occur in two broad normative-authority files; only one failure directly exercises K07, while the other nine concern other Gate C propositions. Execution state is evidence only and does not admit or reject a test.

| Physical test file | Starting input/state and action | Exact observed assertion, exception or absence | Public seam exercised | Material K07 surface not observed | Scoped result |
|---|---|---|---|---|---|
| `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` | Imports calendar reference importer/projection and mutates returned crosswalk lists. | Requires the `build_reference_packet` symbol and detached crosswalk records; emits no packet. | Calendar reference import/projection. | All section 9.10 packet identity, context, lineage, validation and outcomes. | 4 passed |
| `tests/tier_a/capital_deployment/test_capital_authority_service_surface.py` | Supplies a `parallel_risk_packet_id` inside capital input and evaluates a capital receipt. | Asserts capital trace/receipt values and that placement authority remains closed; emits no risk packet. | Capital deployment service. | Parallel-risk packet producer, context, lineage and validation. | 2 passed |
| `tests/tier_a/capital_deployment/test_capital_contract_models.py` | Builds capital inputs/decisions/receipts, including a whitespace-padded risk packet identifier. | Normalises the identifier and proves capital bounds, blocks and hidden-field rejection; emits no DMPV3 packet. | Capital contracts and authority function. | All K07 emission obligations. | 13 passed |
| `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py` | Varies downstream/risk/capital conditions on one capital decision input. | Asserts block, no-trade, reduce and continue domain outcomes; the risk packet value is trace input only. | `evaluate_capital_deployment`. | All K07 envelope and validation behaviour. | 8 passed |
| `tests/tier_a/capital_deployment/test_sequence9_capital_deployment_dmp_packet.py` | Supplies explicit trace/run/scenario plus capital decision and lineage IDs to the capital packet builder. | Asserts DMPV3 shell, lineage and `packetrole=capital_deployment_decision`. | `build_capital_deployment_packet`. | The role is unlisted in section 9.10, so this is candidate implementation evidence; common/role-specific check recording and failure outcomes are absent. | 1 passed |
| `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py` | Uses a parallel-risk ID in exit/close trace and evaluates policy, handoff, receipt and replay fingerprint. | Asserts non-execution, forbidden-authority rejection and deterministic receipt replay; emits no K07 replay packet. | Exit/close contracts and service. | DMPV3 role, context, lineage and validation. | 16 passed |
| `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py` | Uses a parallel-risk ID in an exit trace and evaluates carry handoff, market decision and replay. | Asserts bounded carry actions and replay/service/API behaviour; emits no K07 packet. | Overnight-carry services. | All K07 packet and replay-role obligations. | 4 passed |
| `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py` | Calls the generic builder once without owned context/required lineage, then twice with explicit identity and lineage. | The K07 test expects missing context/lineage to raise; current code does not raise. The explicit calls assert stable source artefact lineage. Five other failures concern C001/C002/C003/C009/C012 rather than K07. | `build_dmp_v3_packet` plus ingress/preparation contracts. | Complete named validation result set, every role profile and lawful diagnostic outcome. | 1 passed / 6 failed; one failure is direct K07 expected-red evidence |
| `tests/tier_a/normative_authority/test_gate_c_remaining_normative_contracts.py` | Exercises several unrelated numbered contracts with a risk packet ID as capital trace data. | Seven propositions pass; four fail for C007, C034, C042 and C044. No K07 packet is emitted. | Raw signal, coefficient, capital, carry and review contracts. | All K07 emission behaviour. | 7 passed / 4 failed; none is direct K07 proof |
| `tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py` | Builds `stage_packet` values with explicit trace/run and extension/dependency inputs. | Preserves canonical extension leaves and prevents extensions replacing canonical dependencies. | Generic DMPV3 builder. | Owner-supplied scenario, required source artefacts/input fingerprint, full named validation profile and rejection outcomes. | 3 passed |
| `tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py` | Imports canonical and compatibility packet modules. | Asserts wrappers are object aliases and no duplicate grammar is declared; emits no packet. | Packet compatibility import surface. | All behavioural section 9.10 obligations. | 3 passed |
| `tests/tier_a/packets/test_fwd004_reopened_row_packet_carriage_proof.py` | Parameterised Atlas rows build stage, risk and reference packets using generic and role builders. | Asserts shell/role/selected lineage fields. One reference case explicitly accepts defaulted trace/run as `degraded`, contrary to sections 9.10.1 and 9.10.5. | `build_dmp_v3_packet` and `DmpPacketBuilder`. | Complete per-role R/C/N matrix, named validation results, source retrieval and failure outcomes. | 59 passed |
| `tests/tier_a/packets/test_reference_packet_carriage.py` | Builds a reference packet without runtime context; also builds explicit generic, prepared and review packets. | Explicitly accepts fabricated trace/run as `degraded`, contrary to sections 9.10.1 and 9.10.5; other cases assert selected shell, extension and lineage fields. | Reference/generic/role packet builders. | Complete role-specific checks, context ownership for prepared/review, failure rejection and diagnostic separation. | 6 passed |
| `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py` | Builds bootstrap input with explicit trace/run and evaluates allow/block risk cases. | Asserts `parallel_risk_packet`, immediate parent/dependency IDs and risk-domain outcomes. | Parallel-risk evaluation service. | Source artefact closure, exact risk input fingerprint, full named validation results and invalid-input outcomes. | 5 passed |
| `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py` | Runs the serial orchestrator and passes selected stage output through the lane service. | Asserts selected stage, bootstrap and risk packet lineage chain; does not assert packet context or validation. | Parallel-risk lane service. | Owned execution context, source artefacts/fingerprint, named validation and rejection outcomes. | 3 passed |
| `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py` | Builds stage and parallel-risk packets with explicit identity and selected lineage. | Asserts roles, producer fields, selected lineage and `validation.status=valid`. | Stage and risk role builders. | Full R/C/N matrix, common and role-specific named check results, and falsification/rejection paths. | 3 passed |
| `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py` | Loads a checked JSON specimen. | Asserts only envelope summary values including `packetrole=parallel_risk_packet`. | Fixture document. | Runtime builder, context ownership, lineage validation and outcomes. | 1 passed |
| `tests/tier_a/runtime/test_fwd012_reopened_row_serial_cognition_spine_proof.py` | Parameterised Atlas rows run the serial orchestrator and inspect generated stage packets. | Asserts generated `trace::serial_runtime::*`, `run::serial_runtime::*`, `scenarioid=live`, selected lineage and `valid` status. Acceptance of implementation-generated execution context conflicts with owner-supplied context law. | Runtime orchestrator. | External context ownership, source artefact closure, per-stage fingerprint meaning, named validation and rejection outcomes. | 139 passed |
| `tests/tier_a/runtime/test_runtime_orchestrator_surface.py` | Runs available and partial serial stages. | Asserts stage order, packet key order and state attachments; does not inspect K07 context or validation. | Runtime orchestrator. | Detailed section 9.10 identity, lineage, validation and outcomes. | 8 passed |
| `tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py` | Runs the serial spine with typed stage inputs and inspects every generated stage packet. | Asserts producer/order/dependency lineage and `valid`; the first temporal `stage_packet` has empty `parentids`, contrary to the section 9.10.3 required prepared/prior-stage parent. | Runtime orchestrator stage emission. | Owner-supplied execution context, required source artefacts, exact per-stage material fingerprint, named checks and rejection path. | 2 passed |
| `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py` | Builds and writes a serial-to-risk specimen. | Asserts the stage/bootstrap/risk lineage chain and bounded artefact paths. | Testing harness specimen. | Context ownership, source artefact/fingerprint completeness, named validation and failure outcomes. | 2 passed |
| `tests/tier_a/upstream_cognition/test_fwd009_reopened_row_prepared_ingress_runtime_context_proof.py` | Parameterised Atlas rows build prepared snapshots and an explicitly identified prepared packet. | Asserts exact trace/run/scenario/review trace and input fingerprint plus prepared-domain lineage facts. | Preparation service and prepared packet builder. | Complete source-artefact retrievability assertion, all named common/role checks and rejection/degraded falsification. | 49 passed |
| `tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py` | Builds prepared packets from complete and failed-enrichment snapshots. | Asserts explicit identity and selected lineage for the valid case; accepts one named enrichment limitation as `degraded`. | Prepared context packet builder. | Proof that all required checks passed before degradation, complete named check recording and rejection of required-fact absence. | 4 passed |
| `tests/tier_a/vocabulary/test_dmp_v3_vocabulary_terms.py` | Reads the canonical vocabulary JSON. | Asserts generic DMPV3 field terms map to contracts; emits no packet and asserts none of the ten namespaced role profiles. | Generated vocabulary projection. | All behavioural section 9.10 obligations. | 1 passed |
| `tests/tier_b/capital_deployment/test_capital_deployment_transform_boundary_surface.py` | Passes a risk packet ID through the capital boundary and checks prohibited donor authority. | Asserts capital block and absence of posture authority; emits no packet. | Capital transform boundary. | All K07 packet behaviour. | 3 passed |

### Aggregate factual findings

1. Five admitted roles have no exact physical-test occurrence: `replay_request_packet`, `replay_result_packet`, `replay_comparison_packet`, `diagnostic_packet` and `rejection_packet`.
2. `reference_packet`, `stage_packet`, `prepared_context_packet` and `parallel_risk_packet` have direct executable observations; `review_explanation_packet` appears only inside a broader builder test.
3. Three green surfaces preserve behaviour that conflicts with the accepted authority: missing-context reference packets accepted as degraded in two files; implementation-generated stage execution context accepted in one file; and the first stage packet accepted with empty required parentage in one file.
4. One direct expected-red test correctly demands rejection for missing owner context/lineage and currently fails.
5. Most routed green files are domain-owner or compatibility observations that merely consume a K07 token. Greenness does not establish M04 authority.
6. No routed file proves the complete common-check set, all role-specific named checks, R/C/N enforcement, degraded bounds, and separate diagnostic/rejection outcomes.

### MLC-O boundary and next leaf

MLC-O is complete. No physical test, fixture, runtime configuration, normative proposition or production source changed. No observation in this section is an admission decision.

The next lawful leaf is `M04-PROOF-MLC-D-V1`: disposition every observation against exact section 9.10 locators, retain only exact proposition proof candidates, classify contradictions and consumer-only observations without allowing green legacy behaviour to override authority, and identify the proof gaps that must feed MLC-P.
