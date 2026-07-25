# Semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`

## File evidence

- Sequence `096`, unit `PM-015`; test SHA-256 `05c0d0c76deedd93be4e28ef5580beee9e2c0e333f8a2fa4cdaf255915a3ad23`.
- Full reads: test lines `1-361`; `src/nvda_desk/contracts/downstream.py` lines `1-205`; `src/nvda_desk/downstream/live_inventory.py` lines `1-295`; workbook wrapper lines `1-27`; receipt ledger lines `1-76`; capital repository lines `1-51`; position repository lines `1-61`; downstream operating model; live-inventory ownership; architecture allocation; and N-06 transaction/idempotency authority.
- Targeted rerun: `15 passed in 0.17s`, exit `0`; raw output is under `P2_RECOVERY_PART1/test_outputs/096_AUDITOR_REPAIR_TARGETED_TEST.txt`.
- Fresh adversarial probe: `P2_RECOVERY_PART1/validation/096_AUDITOR_REPAIR_ADVERSARIAL_PROBE.txt` reproduces duplicate requested-ID exposure inflation, nested placement-authority acceptance, cross-position fill replay and position mutation surviving receipt failure.

## G1 — service module and class presence

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:31-34`; lines `33-34` assert the module identity and class attribute.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`.
- Authority match: the blueprint assigns live position and inventory behaviour to a live-inventory owner, but import and class-name presence prove only that a shell exists.
- Behaviour proved: the named module imports and exposes `DownstreamLiveInventoryService` at the tested attribute.
- Limitation: no lawful input, output, state-read, reconciliation, receipt or authority boundary is exercised.
- Adversarial challenge: replace the implementation with an empty class retaining the same name; lines `33-34` remain green, so meaningful behaviour is a material false positive outside this group.
- Exact-surface falsifier: rename the module or remove the class attribute while leaving the test unchanged; line `33` or `34` must fail immediately.
- Assertion that must fail and why: assertions at lines `33-34` must fail because they directly compare the imported module name and require the exact class attribute; a green result after either symbol is absent would mean the presence detector is broken.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; presence remains supporting inventory evidence until behavioural and boundary proof is admitted.

## G2 — repository snapshot readback and copy isolation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:37-67`; lines `51-60` assert position, capital, exposure and receipt readback, and lines `62-67` assert repository copy isolation.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`.
- Authority match: reading repo-native position and capital state into a bounded live-inventory snapshot is a lawful separable clause, provided the output does not become an opening or capital decision.
- Behaviour proved: the service reads the inserted position and capital records, derives the asserted exposure and receipt identifiers, and returns a deep-copied position payload that cannot mutate repository state through the snapshot.
- Limitation: the arbitrary in-memory mappings are not typed execution truth, carry no state version, and do not prove missing-record semantics, cross-record consistency, durability or restart readback.
- Adversarial challenge: return stale or fabricated mappings containing the expected values; all current assertions remain green, so source authenticity is unproved.
- Exact-surface falsifier: return a shared position payload reference or omit/change any asserted position, capital, exposure or receipt value; an assertion at lines `51-67` must fail.
- Assertion that must fail and why: assertions at lines `51-60` must fail when readback values diverge, and the equality at lines `63-67` must fail when snapshot mutation leaks into the repository; these are the direct detectors for value carriage and copy safety.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain the bounded regressions while adding typed source truth, state-version and durability proof.

## G3 — explicit append-only snapshot receipt

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:70-86`; lines `81-84` assert the stored receipt and lines `85-86` require duplicate-ID rejection.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:21-56`.
- Authority match: explicit receipt append and duplicate rejection are lawful bounded clauses, but N-06 also requires atomic binding, idempotency input fingerprint and deterministic sequence where the receipt attests material state.
- Behaviour proved: one snapshot receipt is explicitly appended with the asserted kind and payload, and reusing the same receipt ID raises in the same in-memory ledger.
- Limitation: no input fingerprint, committed state version, sequence, duplicate replay result, conflict classification, durability or restart recovery is proved.
- Adversarial challenge: append a receipt independently of material state or lose the ledger on restart; lines `81-86` remain green.
- Exact-surface falsifier: suppress the append, alter the stored kind/payload, or permit the second identical receipt ID; an assertion at lines `81-86` must fail.
- Assertion that must fail and why: lines `81-84` must fail if the receipt is absent or semantically altered, while the `pytest.raises` block at lines `85-86` must fail if duplicate protection disappears; together they detect only this local append contract.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; admission requires the N-06 transaction, idempotency, sequencing and restart contract.

## G4 — no exposure invented from quantity

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:89-96`; line `95` preserves the open position ID and line `96` requires an empty declared-exposure map.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-181`.
- Authority match: live inventory may report preserved state but must not invent valuation, capital or risk authority from an unrelated quantity field.
- Behaviour proved: a quantity-only position remains visible while the current aggregation emits no `declared_exposure` value.
- Limitation: caller-supplied `declared_exposure` is accepted without type, valuation source, version, capital consistency or risk-limit reconciliation.
- Adversarial challenge: provide a fabricated numeric `declared_exposure`; the test reports it without challenging its authority, so exposure authenticity remains green.
- Exact-surface falsifier: derive any declared exposure from the quantity-only fixture or drop the position identity; line `96` or `95` must fail.
- Assertion that must fail and why: line `96` must fail if quantity is converted into undeclared exposure, because it directly requires the empty map; line `95` must fail if non-invention is achieved by silently dropping the position.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; preserve non-invention while governing exposure source, valuation and consistency.

## G5 — finite direct-import authority boundary

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:99-119`; lines `109-119` compare AST imports with four forbidden roots.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353` and `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:95-103`.
- Authority match: candidate formation, raw ingress and broker placement are prohibited live-inventory decisions, but absence of four direct imports is not executable authority isolation.
- Behaviour proved: the scanned source file contains no direct import equal to or beneath the four named module roots.
- Limitation: aliases, indirect imports, dependency injection, open dictionaries, re-exported symbols and delegated side effects remain outside the scan.
- Adversarial challenge: inject broker authority through a collaborator or nested payload without adding a forbidden direct import; lines `115-119` remain green.
- Exact-surface falsifier: add `from nvda_desk.adapters.egress import ...` to the scanned file; the boolean assertion at lines `115-119` must fail.
- Assertion that must fail and why: the assertion spanning lines `115-119` must fail because its generator explicitly matches every collected module against the four forbidden roots; if that direct import survives green, the token boundary check is defective.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace finite import scanning with executable collaborator and payload authority-boundary tests.

## G6 — blank live-inventory identifier rejection

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:122-132`; three `pytest.raises` blocks cover blank live ID, inventory ID and receipt ID.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-38,50-56`.
- Authority match: stable non-empty command, state and receipt identities are necessary bounded transaction clauses.
- Behaviour proved: the three exact whitespace-only identifiers are rejected with their named error messages.
- Limitation: uniqueness, collision scope, canonical character policy, identity lineage and cross-object consistency are not exercised.
- Adversarial challenge: submit duplicate but individually non-empty IDs; all three blank-ID assertions remain green.
- Exact-surface falsifier: trim a whitespace-only identifier to an accepted empty token or stop raising the named `ValueError`; the corresponding block at lines `125-132` must fail.
- Assertion that must fail and why: each `pytest.raises` context at lines `125-132` must fail when its blank identifier is accepted or emits the wrong error, because those contexts are the exact negative-boundary detectors for the three fields.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain blank rejection while adding governed uniqueness, lineage and collision rules.

## G7 — requested position-ID normalisation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:135-145`; lines `143-145` assert trimmed ID carriage and one exposure read.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-38,50-56`.
- Authority match: canonical identity normalisation is a necessary clause, but N-06 also requires deterministic duplicate and conflict treatment within the consistency unit.
- Behaviour proved: surrounding whitespace is removed from one requested position ID before repository readback and output carriage.
- Limitation: duplicate requested IDs are neither rejected nor deduplicated; the fresh probe shows `['pos-1', ' pos-1 ']` produces duplicate live IDs and doubles exposure from `2.5` to `5.0`.
- Adversarial challenge: repeat the same normalised ID twice; lines `143-145` are not exercised by that case and remain green.
- Exact-surface falsifier: stop trimming the single requested ID; line `143` or `144` must fail. The material duplicate-ID exposure inflation has no current assertion and therefore remains a known false positive.
- Assertion that must fail and why: lines `143-145` must fail if the single requested ID is not normalised or its bounded readback changes; no current assertion fails for duplicate normalised IDs, so the named `BLOCKED_P3_REPAIR` return gate requires an assertion that rejects or deduplicates collisions before exposure aggregation.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; add collision and uniqueness invariants before aggregation.

## G8 — explicitly requested capital snapshot

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:148-162`; lines `160-162` require `cap-1` and its payload rather than the later inserted `cap-2`.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`.
- Authority match: a downstream state reader may read the named repo-native capital surface without converting that read into capital authority.
- Behaviour proved: a whitespace-padded requested snapshot ID is normalised and the matching repository record is returned instead of the latest record.
- Limitation: unknown requested IDs silently yield no capital state, and no version, effective time, source truth or position-capital consistency is asserted.
- Adversarial challenge: return a stale but correctly identified `cap-1` mapping; lines `160-162` remain green.
- Exact-surface falsifier: ignore `capital_snapshot_id` and return `cap-2`, or alter the selected payload; an assertion at lines `160-162` must fail.
- Assertion that must fail and why: line `161` must fail when the wrong snapshot identity is selected, and line `162` must fail when its payload changes; these assertions directly distinguish the requested record from insertion-order fallback.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; add missing-record, version, temporal and cross-state consistency semantics.

## G9 — workbook wrapper preserves bounded inputs

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:165-194`; lines `184-194` assert wrapper-normalised inventory, position, capital and receipt values plus stored payload equality.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354` and `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:169-195`.
- Authority match: a compatibility wrapper may preserve the lawful live-inventory service seam without taking over its decisions.
- Behaviour proved: the wrapper delegates the supplied bounded identifiers, preserves the selected capital snapshot, emits the asserted receipt, and stores a payload equal to the returned receipt model.
- Limitation: subclass inheritance is not a stable explicit contract, and the test does not prove substitution across alternative implementations, state versions, failures or durability.
- Adversarial challenge: add hidden wrapper side effects that do not alter the asserted output values; lines `184-194` remain green.
- Exact-surface falsifier: drop or alter any supplied identifier during wrapper delegation, select `cap-older`, or store a different payload; an assertion at lines `184-194` must fail.
- Assertion that must fail and why: lines `184-191` must fail on lost or altered delegated values, and line `194` must fail on payload divergence; they are the direct detectors for this wrapper’s bounded preservation contract.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain as compatibility evidence while governing an explicit substitutable service contract.

## G10 — nominal fill-evidence reconciliation

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:197-263`; lines `229-263` assert normalised position state, summed declared exposure, stored fill mappings and reconciliation receipt fields.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:339-354`, `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:95-103`, and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-44`.
- Authority match: admitted execution/fill updates may lawfully change live inventory, but one inventory reconciliation and its position-state/receipt changes form an N-06 consistency unit.
- Behaviour proved: two supplied mappings are normalised, their declared-exposure deltas are summed into one in-memory position, their payloads are retained, and the asserted reconciliation receipt is appended.
- Limitation: arbitrary caller dictionaries stand in for admitted execution truth; fill economics, source identity, expected prior version, idempotency binding and atomic state/receipt commit are absent.
- Adversarial challenge: label fabricated or economically nonsensical caller data as execution evidence; lines `229-263` accept it when the asserted values match.
- Exact-surface falsifier: change normalisation, exposure sum, stored fill order/content or reconciliation receipt values; an assertion at lines `229-263` must fail. Fabricated-source acceptance has no current assertion.
- Assertion that must fail and why: assertions at lines `229-263` must fail when the exact nominal state or receipt values diverge; no current assertion fails for unauthenticated fill origin, so the `BLOCKED_P3_REPAIR` return gate requires typed admitted execution evidence and source-fingerprint checks.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require typed admitted execution evidence and the N-06 consistency-unit contract.

## G11 — fill-evidence negative input boundary

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:266-301`; lines `269-301` cover blank fill identity, blank position identity, one top-level broker key and empty event input.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:347-353` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:29-44`.
- Authority match: non-empty identities, non-empty commands and exclusion of placement authority are lawful bounded clauses for live-inventory reconciliation.
- Behaviour proved: the four exact invalid input forms raise before the nominal state-write loop.
- Limitation: the forbidden-key check is top-level and finite; the fresh probe persists `metadata.broker_order_id`, while aliases and semantic placement instructions remain untested.
- Adversarial challenge: nest or rename a placement-authority field; every current negative assertion remains green.
- Exact-surface falsifier: accept a tested blank/empty input or top-level `broker_order_id`, or emit a different error; the corresponding `pytest.raises` block at lines `269-301` must fail. Nested authority has no current assertion.
- Assertion that must fail and why: the `pytest.raises` contexts at lines `269-301` must fail when any named invalid case is accepted; no current assertion fails for nested placement authority, so `BLOCKED_P3_REPAIR` requires typed evidence or recursive semantic rejection at this boundary.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; replace open mappings with typed fill evidence and executable authority rejection.

## G12 — duplicate fill identity and transaction failure truth

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py:304-361`; lines `308-327` require same-request duplicate rejection before mutation and lines `343-361` require same-position replay rejection without changing stored state.
- Authority locator: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:21-76`.
- Authority match: duplicate replay must not repeat mutation, and all position-state changes plus the attesting receipt must become visible atomically within the named inventory-reconciliation consistency unit.
- Behaviour proved: duplicate fill IDs within one request and replay against the same stored position are rejected before the asserted `pos-1` state changes.
- Limitation: duplicate identity is not consistency-unit-wide, and state/receipt writes are not atomic. The fresh probe accepts the same fill ID on another position and leaves `pos-atomic` mutated after duplicate receipt append fails.
- Adversarial challenge: replay one fill ID on a different position or force receipt failure after position writes; all current duplicate tests remain green.
- Exact-surface falsifier: allow either tested duplicate to mutate `pos-1`; an assertion at lines `308-327` or `343-361` must fail. Cross-position replay and receipt-failure rollback have no current assertion.
- Assertion that must fail and why: lines `308-327` and `343-361` must fail when the two expressly tested duplicates are accepted or alter `pos-1`; no current assertion fails for cross-position duplicate identity or non-atomic receipt failure, so `BLOCKED_P3_REPAIR` requires consistency-unit-scoped idempotency and rollback/commit assertions.
- Semantic relation: `authority_contradictory`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; require consistency-unit idempotency, conflicting-key treatment and atomic state/receipt visibility before Tier A admission.

## File decision

- Groups/relationships: `12/12`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Bounded readback, copy isolation, non-invention, requested-state selection and local duplicate guards are useful regression evidence. They do not cure the reproduced identity-collision, source-authority and transaction-atomicity defects.
