# Reconstructed semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py`

- Sequence `078`, PM-014; test SHA-256 `8edcda5980a1d6a7466f612e7fd2fff25e3b118bf54620b9f127c528f7dd283c`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.contracts.packets: DeskModulePacketV3; nvda_desk.packets.dmp_packets: DmpPacketBuilder, build_parallel_risk_packet, build_stage_packet.
- Surviving decision summary: Retained route proves field carriage and round-trip only; it promotes unvalidated plain-dict payloads and builder-invented live/module identities to valid, contrary to explicit DMPV3 validation and execution-context law.

## Complete test restatement

- Lines `13-16` `test_parallel_risk_packet_builder_surface_is_present`: executes the named specimen/boundary and observes checks at lines `14, 15, 16`. The exact assertions are enumerated in the relationship sections below.
- Lines `19-48` `test_stage_packet_builder_preserves_explicit_stage_carriage_metadata`: executes the named specimen/boundary and observes checks at lines `40, 41, 42, 43, 44, 45, 46, 47, 48`. The exact assertions are enumerated in the relationship sections below.
- Lines `51-72` `test_parallel_risk_packet_builder_emits_stable_parallel_risk_carriage`: executes the named specimen/boundary and observes checks at lines `63, 64, 65, 66, 67, 68, 69, 72`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_parallel_risk_packet_builder_surface_is_present`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py:13-16`. Checks: L14 assert `DmpPacketBuilder is not None`; L15 assert `build_stage_packet is not None`; L16 assert `build_parallel_risk_packet is not None`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Retained route proves field carriage and round-trip only; it promotes unvalidated plain-dict payloads and builder-invented live/module identities to valid, contrary to explicit DMPV3 validation and execution-context law.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_stage_packet_builder_preserves_explicit_stage_carriage_metadata`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py:19-48`. Checks: L40 assert `packet.packetrole == "stage_packet"`; L41 assert `packet.producer.module_id == "temporal_context"`; L42 assert `packet.producer.grammar_role == "temporal_context"`; L43 assert `packet.producer.stage_name == "temporal"`; L44 assert `packet.lineage.derivedfrom == "temporal_from_declared_stage_inputs"`; L45 assert `packet.lineage.sourceartifactids == ["bundle-input-1"]`; L46 assert `packet.lineage.inputfingerprint == "abc123"`; L47 assert `packet.summary.headline == "session_state=opening"`; L48 assert `packet.validation.status == "valid"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Retained route proves field carriage and round-trip only; it promotes unvalidated plain-dict payloads and builder-invented live/module identities to valid, contrary to explicit DMPV3 validation and execution-context law.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_parallel_risk_packet_builder_emits_stable_parallel_risk_carriage`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py:51-72`. Checks: L63 assert `packet.packetrole == "parallel_risk_packet"`; L64 assert `packet.producer.module_id == "parallel_risk_lane"`; L65 assert `packet.producer.grammar_role == "parallel_risk_lane"`; L66 assert `packet.producer.behaviour_class == "module_output"`; L67 assert `packet.lineage.dependencyids == ["stage-1", "stage-2"]`; L68 assert `packet.validation.status == "valid"`; L69 assert `packet.summary.headline == "parallel risk emitted"`; L72 assert `reparsed == packet`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Retained route proves field carriage and round-trip only; it promotes unvalidated plain-dict payloads and builder-invented live/module identities to valid, contrary to explicit DMPV3 validation and execution-context law.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
