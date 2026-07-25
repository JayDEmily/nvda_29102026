# Semantic receipt — `tests/tier_a/adapters_ingress/test_external_source_interface_boundary.py`

## 1. Process record

- Sequence: `002`
- Unit: `PM-012`
- Test SHA-256: `aac83ecb5364a3404be8235251cadb5d4a14dba17368e60709fd34c4b14f01c4`
- Test read in full: lines `1-210`.
- Exercised source read in full: `src/nvda_desk/contracts/external_source.py` lines `1-179`; all four current files under `src/nvda_desk/adapters/ingress` (`__init__.py`, `calendar_feed.py`, `market_snapshot_feed.py`, `options_surface_feed.py`); and `src/nvda_desk/adapters/egress/broker_protocol.py` lines `1-26`.
- Local helper read: `_market_spec`, lines `23-29`.
- No external fixture, parametrisation, setup/teardown or monkeypatch is used.
- Current registry/proof-block routes were read as observations only.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/adapters_ingress/test_external_source_interface_boundary.py -q` returned `12 passed in 0.19s`, exit `0`.

## 2. Complete file restatement

The file builds a recorded-market `ExternalSourceInterfaceSpec`, checks its closed-authority defaults and selected enum values, tests model rejection of explicit network and credential fields, checks deep-copy carrier isolation, checks deterministic rejection/acceptance results, parses the current ingress-adapter source tree for an exact file inventory and five forbidden import roots, scans the broker protocol source text for protocol and client tokens, checks non-empty interface identity fields, rejects undeclared carrier fields, samples ten critical forbidden payload keys, checks result immutability, and checks recursive nested-key rejection.

The exact surfaces observed are Pydantic model construction/validation, `_find_forbidden_payload_keys`, `validate_external_payload_boundary`, deep-copy behaviour, source-file names, Python AST import roots, and literal source text in one broker protocol file.

The file never executes an ingress adapter or broker gateway; never performs provider substitution; never proves controlled registration; never observes transitive/dynamic imports, runtime sockets or network side effects; never preserves source/capture identity, source time, schema version or fingerprint; never tests every forbidden key; never proves every external family uses this contract; and never observes persistence, cognition bypass, order lifecycle, replay or implementation maturity beyond the current seam.

## 3. Authority context

- `N04-002`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:21-42`: explicit adapters/source readers, typed native carriers, source-shape validation, provider-semantic termination and exclusion of downstream decision authority.
- `N03-004`, `docs/03.1_DOMAIN_MODEL_WORKING.md:57-75`: typed input extensibility through adapters, versioned carriers and controlled registration without unrelated rewrites.
- `C-001`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv:2`: source-owned contract coverage, owner-issued identity on the nominal path, and recursive forbidden-authority/fabricated-identity rejection; model validation alone cannot prove the whole requirement.
- `C-039`, the same register line `40`: protocol-only invariants and adapter replacement for downstream transaction boundaries; token presence alone cannot prove the whole requirement.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:135-150` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:39-45`: surface 5.1 remains `thin_seam`.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:348-353`: bounded authority-readiness permits recorded/offline carriers and import/boundary rejection proof, but not concrete live source/API implementation.

## 4. Assertion-group decisions

### Group 1 — recorded market spec defaults and selections (`32-38`)

- Behaviour: verifies network disabled, credentials empty, family `MARKET`, mode `RECORDED_API_RESPONSE`.
- Authority match: correct external-contract owner and current recorded/offline lifecycle; exact enum choices are implementation grammar.
- Proves: the helper-created spec has those four values.
- Does not prove: carrier identity completeness, provider source truth, adapter use or actual absence of network activity.
- Falsifier: default `network_enabled=True`, non-empty credentials, or substitute another enum value.
- Required failure: one of assertions `35-38`.
- Relation: `bounded_separable_clause`.
- Strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; no broader C-001 claim.

### Group 2 — explicit live-network rejection (`41-49`)

- Behaviour: `network_enabled=True` must raise the named validation error.
- Authority match: exact bounded closure required by the current authority-readiness seam.
- Proves: this interface representation rejects the explicit flag.
- Does not prove: repository-wide network absence or transitive client use.
- Falsifier: permit `True` in `_network_must_remain_closed`.
- Required failure: `pytest.raises` at `42-49`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; composition proof remains separate.

### Group 3 — explicit credential rejection (`51-58`)

- Behaviour: non-empty credential fields must raise the named validation error.
- Authority match: exact bounded credential closure at the external interface.
- Proves: the tested model field cannot carry one credential name.
- Does not prove: secrets cannot appear elsewhere or under other representations.
- Falsifier: accept non-empty `credential_fields`.
- Required failure: `pytest.raises` at `51-58`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`.

### Group 4 — carrier copy isolation (`61-71`)

- Behaviour: caller mutation and mutation of a detached copy do not change the carrier's nested payload.
- Authority match: typed carrier boundary and no hidden downstream mutation.
- Proves: deep-copy isolation for the tested mapping/nested mapping.
- Does not prove: durable captured-evidence immutability or every Python payload type.
- Falsifier: replace constructor or `payload_copy` deep copying with shallow copies.
- Required failure: assertions `70` or `71`.
- Relation: `bounded_separable_clause`; strength: `behavioural`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`.

### Group 5 — deterministic rejection result for three authority/secret keys (`74-87`)

- Behaviour: top-level `trade_allowed`, `order_qty` and `api_key` produce rejected result, fixed reason and sorted key tuple.
- Authority match: separable recursive-forbidden-authority clause of `C-001`; correct ingress owner.
- Proves: these three keys are found and represented deterministically.
- Does not prove: all forbidden keys, fabricated identity, or all nested/container shapes.
- Falsifier: remove any tested key from the forbidden set.
- Required failure: `85-87`, especially exact tuple at `87`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; full C-001 remains unproved.

### Group 6 — nominal recorded-shape validation result (`90-98`)

- Behaviour: a simple recorded market mapping returns accepted, no reason and no rejected keys.
- Authority match: source validation result is a lawful surface-5.1 output.
- Proves: the tested mapping is not rejected by the current forbidden-key boundary.
- Does not prove: source-shape correctness, source identity, version/time/fingerprint or adapter composition. The function performs no positive schema validation beyond absence of forbidden keys.
- Falsifier: return rejected for this mapping or add one present key to the forbidden set.
- Required failure: one of `96-98`.
- Relation: `bounded_separable_clause`; strength: `behavioural`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`, limited to nominal boundary acceptance, not authoritative source-shape proof.

### Group 7 — exact current ingress-adapter file inventory (`101-108`)

- Behaviour: requires exactly four current Python files.
- Authority match: it creates an explicit review gate around the current adapter seam, but exact filenames are not a normative provider-registration design.
- Proves: only those files exist at this path at test time.
- Does not prove: controlled registration, adapter correctness, provider substitution or lawful completeness. A lawful new adapter also causes failure until consciously reviewed.
- Falsifier: add `new_feed.py`.
- Required failure: list equality at `103-108`.
- Relation: `bounded_separable_clause` to the current review boundary, not full `N03-004`.
- Strength: `presence_only`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; must never be described as behavioural adapter proof.

### Group 8 — forbidden concrete-client import roots (`110-119`)

- Behaviour: AST-parses current ingress files and requires imports to exclude `openai`, `requests`, `httpx`, `aiohttp`, `websocket`.
- Authority match: bounded import-boundary check explicitly opened by process law.
- Proves: no static import/import-from root with those five names exists in the four parsed files.
- Does not prove: no `urllib`, `socket`, dynamic import, transitive network library, subprocess, runtime network call or concrete client elsewhere.
- Falsifier: add `import requests` to an adapter.
- Required failure: assertion `119`.
- Relation: `bounded_separable_clause`.
- Strength: `token_only`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; repository-wide network absence remains unproved.

### Group 9 — broker protocol source-token boundary (`122-130`)

- Behaviour: scans one egress source file for the protocol class and method token and absence of two client-library tokens.
- Authority match: bounded protocol-only clause of `C-039`; this is downstream egress adjacency, not external-ingress behavioural proof.
- Proves: the inspected text contains/omits the exact strings.
- Does not prove: valid Python semantics, Protocol conformance, no other client library, lifecycle idempotency, event ordering, adapter replacement or no broker side effect.
- Falsifier: rename/remove `BrokerGatewayProtocol` or add `import requests` text.
- Required failure: one of `127-130`.
- Relation: `bounded_separable_clause` only for the source-token protocol seam.
- Strength: `token_only`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; full C-039 requires other proof.

### Group 10 — non-empty source and carrier identity fields (`133-148`)

- Behaviour: empty `source_id` and empty `typed_carrier_name` each fail model validation.
- Authority match: bounded mandatory-field validity at the typed ingress contract.
- Proves: these two strings have minimum length one.
- Does not prove: owner, namespace, uniqueness, stability, actual source-issued identity, schema/contract version or carrier type existence.
- Falsifier: remove either `Field(min_length=1)` constraint.
- Required failure: corresponding `pytest.raises` block at `134-140` or `142-148`.
- Relation: `bounded_separable_clause`.
- Strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; identity-lineage proof is not claimed.

### Group 11 — undeclared client-state field rejection (`151-157`)

- Behaviour: adding `client_session` to carrier construction must fail.
- Authority match: typed carrier is closed against undeclared client state.
- Proves: Pydantic `extra="forbid"` rejects this tested field.
- Does not prove: no client/session state can be encoded inside `payload` under an unlisted key.
- Falsifier: set carrier extra handling to allow/ignore.
- Required failure: `pytest.raises` at `152-157`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`.

### Group 12 — ten critical keys individually rejected (`160-182`)

- Behaviour: loops over ten keys and requires a rejected result, fixed reason and exact one-key tuple for each.
- Authority match: direct sample of C-001 forbidden-authority rejection.
- Proves: those ten top-level keys are individually recognised at this revision.
- Does not prove: the remaining forbidden set, nesting for every key, aliases/encoded values or fabricated identity.
- Falsifier: remove any listed key from `_FORBIDDEN_PAYLOAD_KEYS`.
- Required failure: one of loop assertions `180-182`, labelled by key.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`.

### Group 13 — immutable validation result (`185-192`)

- Behaviour: assignment to `result.accepted` must fail.
- Authority match: validation result may be a stable carrier of one boundary decision; immutability is a local contract property.
- Proves: the Pydantic result model is frozen against the tested assignment.
- Does not prove: durable immutability, receipt lineage, replay or authoritative result correctness.
- Falsifier: remove `frozen=True`.
- Required failure: `pytest.raises` at `191-192`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`.

### Group 14 — nested authority/secret rejection (`195-210`)

- Behaviour: nested `api_key` and `trade_allowed` produce deterministic rejection and sorted tuple.
- Authority match: exact recursive forbidden-authority clause of C-001 for the tested nested mapping.
- Proves: mapping recursion finds those two keys.
- Does not prove: arbitrary containers, cycles, all keys or fabricated identity.
- Falsifier: stop recursion into nested mappings or remove a tested key.
- Required failure: one of `208-210`, especially tuple at `210`.
- Relation: `bounded_separable_clause`; strength: `boundary`.
- Disposition/gate: `ADMIT_TIER_A_CURRENT`; no full-C-001 claim.

## 5. Whole-file adversarial challenge

A violating system can preserve every assertion while another module dynamically imports a network client, a current adapter fabricates source identity, a new external family bypasses this contract, a payload lacks source time/version/fingerprint, or the broker implementation violates lifecycle/idempotency rules. The file would pass because it observes only local models, selected static imports, file names and source tokens. Therefore the file supplies bounded boundary and structural checks only.

## 6. Final file disposition

`ADMIT_TIER_A_CURRENT`

The file lawfully supports fourteen bounded current clauses. Its `presence_only` and `token_only` groups are not behavioural proof, and none of the groups proves complete external-source composition, source identity/temporal lineage, provider substitution, repository-wide network/credential absence, broker lifecycle, or implementation status beyond `thin_seam`.

- Assertion-group count: `14`
- Relationship count: `14`
- Return gate: none for the bounded clauses; broader C-001, N03-004 and C-039 completeness remains outside this file.
