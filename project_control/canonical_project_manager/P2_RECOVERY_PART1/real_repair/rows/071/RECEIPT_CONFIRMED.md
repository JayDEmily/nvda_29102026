# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`

## File evidence

- Sequence `071`, unit `PM-014`; test SHA-256 `17c4061336d249f87b27a1fd21d33f656210c7d6a38482e9adf795773b68fedd`.
- Full reads: test `1-106`; lane service `src/nvda_desk/services/parallel_risk_lane_service.py:1-229`; directly exercised runtime packet and Parallel Risk contracts; serial/parallel allocation `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:37-66`; DMPV3 identity and lineage law `docs/09_DMPV3_PROTOCOL_CORE.md:31-58,60-123`; native DMPV3 and Parallel Risk seams `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-269`; P1 decisions `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:121-122`.
- Raw test result: `3 passed in 0.19s`.

## G1 — `test_parallel_risk_lane_service_runs_serial_runtime_boundary_path_without_hidden_state`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:42-80`; assertions at lines `51-80` verify exact return surfaces, temporal-packet selection, bootstrap and lane packet identities, lineage, source, event carriage and service instance state.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:37-66`, `docs/09_DMPV3_PROTOCOL_CORE.md:60-123` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-269`.
- Authority match: the exercised path is the declared serial-stage-packet to independent Parallel Risk boundary, and the assertions directly exercise truthful packet role, source, lineage and bounded output carriage.
- Behaviour proved: one lawful serial runtime receipt selects only its temporal stage packet, creates a separately identified bootstrap packet, emits a separately identified Parallel Risk packet and retains explicit parent/dependency lineage without additional service state.
- Limitation: the specimen does not prove all malformed receipt shapes, all serial stages, optional Minute Profile semantics, repository-wide hidden-read absence, persistence, candidate audit, capital non-interference or arbitrary downstream consumers.
- Adversarial challenge: a later implementation could read regime or options packets through a new global dependency, mutate capital state or alter unasserted DMP fields while all current assertions remain green.
- Exact-surface falsifier: select the regime packet, change either asserted packet ID or drop the asserted parent/dependency identity so an assertion at lines `52-79` fails; this falsifies the admitted boundary behaviour for the exercised receipt.
- Assertion that must fail and why: line `52` fails if a non-temporal stage is selected; lines `54-63` fail if the bootstrap identity or lineage no longer names the selected temporal packet; and lines `72-79` fail if the lane packet identity, lineage or bounded service state changes. These assertions establish the exercised packet path, but the `service.__dict__` check cannot exclude hidden reads performed through module globals or imported services.
- Semantic relation: `exact_full_proof`.
- Proof strength: `behavioural`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain while the serial-to-Parallel-Risk packet seam and asserted DMPV3 identities remain normatively unchanged.

## G2 — `test_parallel_risk_lane_service_fails_closed_on_temporal_packet_id_contract_mismatch`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:83-89`; assertion at lines `88-89` requires the exact fail-closed error after substituting a regime-prefixed ID into the temporal slot.
- Authority locator: `docs/09_DMPV3_PROTOCOL_CORE.md:60-93,115-123` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:237-269`.
- Authority match: producer/stage identity must be truthful and packet meaning must not be inferred from payload shape; the substituted identifier is therefore an exact negative boundary case.
- Behaviour proved: the service rejects a temporal-slot packet whose ID declares the regime stage rather than accepting or reinterpreting it.
- Limitation: only one identifier substitution is challenged; wrong producer fields, schema, role, time token, extra stage keys and malformed nested data require separate proof.
- Adversarial challenge: the service could accept a correctly prefixed temporal ID carrying a regime producer or wrong schema, and this test would remain green.
- Exact-surface falsifier: remove the prefix check or accept the substituted regime ID so the `pytest.raises` assertion at line `88` fails.
- Assertion that must fail and why: the context manager at lines `88-89` fails if the service accepts the substituted regime-prefixed packet ID, raises no exception, or raises a `ValueError` whose message does not match the declared temporal-ID contract. It proves that one identifier substitution is rejected, not that every producer/schema mismatch is rejected.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `substitution`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain as the exact packet-identity substitution proof and return for review if the stage-ID grammar changes.

## G3 — `test_parallel_risk_lane_service_records_serial_temporal_input_trace`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py:92-106`; assertions at lines `100-106` fix bootstrap source, admitted semantic input, selected packet, bootstrap packet and parent packet identities.
- Authority locator: `docs/09_DMPV3_PROTOCOL_CORE.md:95-113` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:220-269`.
- Authority match: explicit upstream packet identities and derivation references are required at deliberate packet boundaries; these fields are the exercised Parallel Risk input-trace implementation of that law.
- Behaviour proved: the emitted lane payload records the exact temporal source and packet identities used by the bootstrap path.
- Limitation: the group proves only the asserted trace fields and does not instrument every possible hidden authority key or prove that no other process/global input was consulted.
- Adversarial challenge: an implementation could consult a hidden module-level signal while still recording the same five trace fields.
- Exact-surface falsifier: change or omit any asserted source or packet identity so an assertion at lines `100-106` fails.
- Assertion that must fail and why: lines `100-106` each bind one trace field to the selected temporal packet or generated bootstrap packet; changing the source label, admitted-input list, selected ID, bootstrap ID or parent list makes the corresponding equality false. The group would still pass if an additional unrecorded dependency were consulted elsewhere.
- Semantic relation: `exact_full_proof`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `ADMIT_TIER_A_CURRENT`; retain as bounded DMP/input-trace evidence, not as repository-wide proof of hidden-read absence.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `ADMIT_TIER_A_CURRENT`.
- Admit the three bounded relationships for lawful temporal-stage selection, packet-identity fail closure and explicit serial-to-Parallel-Risk lineage. No source, test, config or authority mutation is authorised.
