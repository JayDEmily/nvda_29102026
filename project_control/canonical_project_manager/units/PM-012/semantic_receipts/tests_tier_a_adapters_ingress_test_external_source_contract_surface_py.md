# Semantic receipt — `tests/tier_a/adapters_ingress/test_external_source_contract_surface.py`

## 1. Process record

- Sequence: `001`
- Unit: `PM-012`
- Test SHA-256: `c671d5f0efc1472f886ec2246290509a880e446947f49f40ec9f0addb43c4482`
- Test lines read: `1-86` in full.
- Exercised implementation read in full: `src/nvda_desk/contracts/external_source.py` lines `1-179`.
- Local helper read: `_operator_bundle_spec`, test lines `15-21`.
- Fixtures/parametrisation/setup/teardown/monkeypatch: none.
- Current route observed, not inherited as authority: retained registry family and proof block `external_source_contract_surface`.
- Validation command: `PYTHONPATH=src python -m pytest tests/tier_a/adapters_ingress/test_external_source_contract_surface.py -q`.
- Validation result: `4 passed in 0.24s`, exit `0`.
- Metadata repair: the first authored receipt carried an incorrect copied test hash; the ledger was reset to `NO`, the complete 86-line test was reread, and this hash was recomputed before re-closing the row.

## 2. Complete file restatement

### 2.1 Starting state and inputs

The file constructs a frozen `ExternalSourceInterfaceSpec` for an operator-provided bundle. It then exercises the interface and carrier models with: the current ingress-mode enumeration; a requested live-network flag; declared credential fields; a nested payload containing `api_key` and `order_qty`; and a recorded payload containing symbol and metadata.

### 2.2 Actions

The tests instantiate Pydantic contract models, expect validation failures for closed authority, call `validate_external_payload_boundary`, construct an `ExternalPayloadCarrier`, mutate the caller-owned input after construction, obtain a detached payload copy, and mutate that copy.

### 2.3 Exact observed surfaces

The file observes only:

1. `ExternalIngressMode` enumeration values;
2. Pydantic validation of `ExternalSourceInterfaceSpec.network_enabled`;
3. Pydantic validation of `ExternalSourceInterfaceSpec.credential_fields`;
4. recursive key scanning performed while constructing `ExternalPayloadCarrier`;
5. the returned `ExternalSourceValidationResult` fields `accepted` and `rejected_keys`; and
6. deep-copy isolation of `ExternalPayloadCarrier.payload` and `payload_copy()`.

### 2.4 Exact asserted results or failures

1. The mode enumeration equals five recorded/offline modes.
2. `network_enabled=True` raises a validation error containing `external_network_clients_not_admitted`.
3. non-empty credential fields raise a validation error containing `external_credentials_not_admitted`.
4. nested `api_key` and `order_qty` keys cause construction to fail with the sorted key list.
5. a payload without tested forbidden keys is accepted, reports no rejected keys, and remains unchanged after caller-input and returned-copy mutation.

### 2.5 Surfaces never observed

The file does not observe any adapter implementation, source reader, live network stack, dependency, credential store, provider protocol, API composition, broker client, registry-based provider selection, actual source/capture identity preservation, schema/version carriage, source observation time, repository capture identity, immutable fingerprint, downstream preparation, cognition bypass, persistence, replay, or trading decision. It does not exercise `ExternalSourceValidationResult` on a rejected payload, every key in `_FORBIDDEN_PAYLOAD_KEYS`, every nested Python container type, fabricated source identity, or whether another module performs live network activity while these models remain unchanged.

## 3. Authority context

- Proposition `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`, requires explicit external adapters/source readers and typed native ingress carriers, source-shape validation, termination of provider semantics at the adapter boundary, and exclusion of domain/trading/state authority.
- Gate-C requirement `C-001`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:2`, requires admitted external families to enter through this or another explicit source-owned contract, preservation of owner-issued identity on the nominal path, and recursive rejection of fabricated identity and forbidden authority. It explicitly rejects model-validation-only proof of the whole requirement.
- Current architecture truth, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:135-150` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:39-45`, fixes surface 5.1 at `thin_seam`; lawful outputs include typed carriers and source validation results, but this is not an `implemented` claim.
- The bounded programme record, `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353`, limits the relevant work to authority-readiness for recorded/offline carriers, source-shape and boundary rejection, including explicit rejection of credential/network/client/runtime-decision smuggling. It forbids a live external-source/API implementation claim.

No relationship below is treated as full proof of `N04-002` or `C-001`.

## 4. Assertion group 1 — admitted ingress-mode enumeration

1. **Test locator:** lines `24-31`, set equality over `ExternalIngressMode`.
2. **Authority locator:** `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`; bounded current scope at `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353`.
3. **Test behaviour:** enumerates the current interface modes and requires exactly operator bundle, checked-in reference, recorded API response, recorded broker response and offline fixture.
4. **Authority meaning:** current surface 5.1 is confined to typed recorded/offline ingress readiness and does not admit live network/client authority.
5. **Match analysis:** owner and boundary match the external-ingress contract. The assertion is narrower and more representation-specific than the proposition: the exact enum tokens are implementation grammar, while the lawful semantic clause is the absence of a live/client mode in this interface.
6. **Proved:** the inspected enum exposes only the five named non-live modes at this revision.
7. **Not proved:** no network activity elsewhere; adapter composition; completeness of all lawful future recorded/offline modes; provider substitution; source identity/temporal carriage.
8. **Falsifier:** add `LIVE_API = "live_api"` to `ExternalIngressMode` while leaving all unobserved adapters and services unchanged.
9. **Required failing assertion:** lines `25-31` fail because the actual set gains `live_api`.
10. **Semantic relation:** `bounded_separable_clause`.
11. **Proof strength:** `boundary`.
12. **Disposition / return gate:** `ADMIT_TIER_A_CURRENT`; no P3 repair required for this bounded clause. Any claim of actual network absence remains blocked.

## 5. Assertion group 2 — interface-level live-network rejection

1. **Test locator:** lines `33-40`, expected `ValidationError` for `network_enabled=True`.
2. **Authority locator:** bounded authority-readiness clause at `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353`, consistent with `N04-002` and surface 5.1 `thin_seam` at `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:135-150`.
3. **Test behaviour:** attempts to create an external-source interface that declares live network authority and expects deterministic rejection.
4. **Authority meaning:** the current boundary may prove recorded/offline contract readiness but may not admit concrete network clients or live external integration.
5. **Match analysis:** the asserted field is owned by the external-source boundary and the lifecycle is the current authority-readiness seam. It is not evidence about other modules.
6. **Proved:** this model rejects the explicit `network_enabled=True` representation.
7. **Not proved:** absence of network calls, clients, credentials or dependencies outside this field; adapter import boundaries; actual external-source execution.
8. **Falsifier:** change `_network_must_remain_closed` to return `True` without raising.
9. **Required failing assertion:** the `pytest.raises` block at lines `33-40` fails because no `ValidationError` is raised.
10. **Semantic relation:** `bounded_separable_clause`.
11. **Proof strength:** `boundary`.
12. **Disposition / return gate:** `ADMIT_TIER_A_CURRENT`; broader live-network prohibition still requires composition/import proof elsewhere.

## 6. Assertion group 3 — credential-field rejection

1. **Test locator:** lines `43-51`.
2. **Authority locator:** `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353`; related external-boundary proposition `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`.
3. **Test behaviour:** supplies `("api_key", "secret")` as interface credential fields and expects deterministic rejection.
4. **Authority meaning:** credentials and concrete client authority are outside the currently opened external-ingress seam.
5. **Match analysis:** the test addresses the correct owner and boundary. It checks one explicit contract field, not repository-wide credential absence.
6. **Proved:** non-empty `credential_fields` are rejected by `ExternalSourceInterfaceSpec`.
7. **Not proved:** secrets cannot appear under other field names, in environment/configuration, or in adapter/service code; no credential handling exists elsewhere.
8. **Falsifier:** remove the non-empty check in `_credentials_must_remain_closed`.
9. **Required failing assertion:** lines `44-51` fail because model construction succeeds.
10. **Semantic relation:** `bounded_separable_clause`.
11. **Proof strength:** `boundary`.
12. **Disposition / return gate:** `ADMIT_TIER_A_CURRENT`; repository-wide credential exclusion is not claimed.

## 7. Assertion group 4 — recursive rejection of tested nested authority keys

1. **Test locator:** lines `54-65`.
2. **Authority locator:** Gate-C requirement `C-001`, `GATE_C_TEST_REQUIREMENTS.tsv:2`, specifically the separable recursive forbidden-authority rejection clause; supporting owner boundary `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`.
3. **Test behaviour:** constructs a carrier with `api_key` nested inside a mapping and `order_qty` nested inside a list of mappings, expecting both keys in the sorted rejection message.
4. **Authority meaning:** external material must not smuggle authority across the ingress boundary, including in nested payload structure.
5. **Match analysis:** owner, stage and boundary match. The test is a concrete recursive sample, not exhaustive proof of every forbidden key/container or fabricated identity.
6. **Proved:** the current recursive scanner reaches the tested mapping/list paths and rejects the two tested authority keys before carrier construction completes.
7. **Not proved:** all 20 forbidden keys, arbitrary custom containers, cycles, aliases, values that encode authority without a forbidden key, or fabricated source identity.
8. **Falsifier:** stop recursion into list elements, or remove `order_qty` from `_FORBIDDEN_PAYLOAD_KEYS`, while keeping top-level validation unchanged.
9. **Required failing assertion:** lines `55-65` fail because construction either succeeds or the error no longer contains `api_key,order_qty` exactly.
10. **Semantic relation:** `bounded_separable_clause`.
11. **Proof strength:** `boundary`.
12. **Disposition / return gate:** `ADMIT_TIER_A_CURRENT`; full `C-001` remains unproved and must be supplied by other tests or P3 repair.

## 8. Assertion group 5 — nominal acceptance and copy isolation

1. **Test locator:** lines `68-86`.
2. **Authority locator:** `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`, requiring a typed native ingress carrier and source validation result; surface 5.1 lawful outputs at `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:143-149`.
3. **Test behaviour:** validates and carries a recorded payload, mutates the original nested mapping and a returned detached copy, then checks acceptance, empty rejected keys and preserved internal value `7`.
4. **Authority meaning:** admitted outer material crosses the seam through a typed carrier and validation result without hidden mutation of the carried evidence.
5. **Match analysis:** the carrier/result owner and boundary match. The assertion covers local copy isolation only; it does not establish complete carrier identity, schema version, source time or adapter composition.
6. **Proved:** this payload is accepted; `rejected_keys` is empty; constructor and `payload_copy()` perform sufficient deep copying for the tested nested mapping.
7. **Not proved:** all payload types are copy-safe; original captured evidence is durably immutable; owner-issued identity or source-time fields are present; an adapter actually creates this carrier.
8. **Falsifier:** replace the carrier validator's `deepcopy` with a shallow `dict(value)` and return `dict(self.payload)` from `payload_copy()`.
9. **Required failing assertion:** line `86` fails because nested sequence becomes `99` or `100`; alternatively changing the nominal result to rejected fails lines `84-85`.
10. **Semantic relation:** `bounded_separable_clause`.
11. **Proof strength:** `behavioural`.
12. **Disposition / return gate:** `ADMIT_TIER_A_CURRENT`; complete nominal `C-001` identity/composition proof remains outside this file.

## 9. Adversarial whole-file challenge

A violating implementation could keep these models and all five observed behaviours unchanged while an adapter directly instantiates a live provider client, fabricates `source_id`, omits capture identity and source time, bypasses the typed carrier for another external family, or sends the payload directly into cognition. This file would still pass. Therefore it cannot prove the whole external-adapter proposition or Gate-C requirement. Its lawful role is the five bounded contract/boundary clauses above.

## 10. Final file disposition

`ADMIT_TIER_A_CURRENT`

Reason: the file contains current behavioural and boundary proof for exact separable clauses of the external-ingress authority-readiness seam. Admission is limited to those clauses. The file must not be cited as proof of complete adapter composition, external-family coverage, source identity/temporal lineage, provider substitution, live-network absence across the repository, or implementation maturity beyond `thin_seam`.

- Assertion-group count: `5`
- Relationship count: `5`
- P3 return gate: none for this file's bounded admitted clauses; broader C-001 completion remains a separate coverage question.
