# Semantic receipt — `tests/tier_a/config/test_config_authority_surface.py`

## 1. Process record

- Sequence: `007`
- Unit: `PM-012`
- Test SHA-256: `3daaba8ffabd5b362e5e105d5103ee5adf8cd7acc721b3d5e430d1f5be7ac2fc`
- Test read in full: lines `1-62`.
- Helpers `_require_module` and `_require_attr` read in full.
- Exercised implementation read in full: `src/nvda_desk/config/runtime_settings.py` lines `1-37`, `src/nvda_desk/config/bundle_loader.py` lines `1-54`, `src/nvda_desk/config/config_surface.py` lines `1-42`, `src/nvda_desk/config/coefficient_authority.py` lines `1-250`, `src/nvda_desk/config/playbook_registry.py` lines `1-155`, `src/nvda_desk/contracts/coefficient_authority.py` lines `1-213`, and `src/nvda_desk/contracts/playbook.py` lines `1-185`.
- Exercised config read in full: `config/runtime_settings.example.yaml`, `config/coefficient_authority.v1.yaml`, `config/playbook_registry.example.yaml`, `config/evaluation_config.example.yaml`, `config/coefficients_registry.example.yaml`, `config/strategy_variants.example.yaml`, and `config/README.md`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/config/test_config_authority_surface.py -q` returned `2 passed in 0.27s`, exit `0`.

## 2. Complete file restatement

The first test imports five config modules and verifies their module names plus the presence/identity of eleven current classes/functions. The second loads the default config bundle and a default `ConfigSurface`, obtains a coefficient-authority document through the surface, then compares separately loaded runtime settings, checks one authority ID, checks the declared source-workbook path suffix, checks one coefficient ID exists for posture ownership, and compares the playbook registry returned through the surface with the bundle copy.

The file observes importability, exact symbol names, equality between two access paths over the same default files, one coefficient authority identifier, one source-lineage path string, one record presence and one example playbook-registry equality. It does not observe filesystem access to the workbook, so the test named `...without_runtime_workbook_reads` does not prove that prohibition. It also never tests config substitution, missing or malformed files, schema versions, hard bounds, record contents, owner-stage rejection, duplicate keys, hidden authority, live-versus-example status, cache invalidation, downstream use or separation from unrelated domain decisions.

## 3. Authority context

- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:8-45` states that the workbook is governed reference evidence but never direct runtime authority; lawful lineage is workbook concept to typed config/contracts to runtime consumption, and direct runtime workbook reads are forbidden.
- Accepted `Coefficient Authority` owns typed coefficient identity, owner, baseline, surface class, hard bounds, promoted version and current authorised record: `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:35`.
- `docs/05.1_GUARDRAILS_WORKING.md:13-19` requires numeric/behavioural constraints to be owned by admitted domain policy/config authority, not structural convenience.
- `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:86-94` requires configuration and other replaceable infrastructure behind explicit contracts/interfaces and selected at an assembly boundary rather than hidden in unrelated domain decisions.
- `config/README.md:5-18` distinguishes live config surfaces from example-only files. Only `coefficient_authority.v1.yaml` is named live here; runtime settings, coefficient/evaluation/strategy examples and `playbook_registry.example.yaml` are explicitly not runtime authority until promoted.
- Current row 5.9 remains a `thin_seam`, with material version carriage and complete consumer integration incomplete: `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:53`.
- Testing law states that file presence, import success and schema construction are not semantic proof by themselves: `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:28-59`.

## 4. Assertion group 1 — five modules and eleven attributes are present (`21-42`)

1. **Behaviour:** imports five current config modules and requires exact classes/functions to exist under current names.
2. **Authority meaning:** governed configuration must have bounded owners/contracts, lawful live-versus-example status, replaceability and no direct workbook runtime authority.
3. **Mismatch:** module and symbol presence prove only current code shape. They do not prove ownership, live authority, substitution, validation or runtime use. Several named surfaces load files explicitly documented as example-only.
4. **Proved:** all five modules import and expose the eleven current objects.
5. **Not proved:** that any object is authoritative, correctly implemented, used at the assembly boundary, replaceable, isolated from domain decisions, schema-valid or free of workbook reads.
6. **Falsifier:** remove/rename one module or required object.
7. **Required failure:** module-name assertions `23`, `25`, `27`, `29`, `31` or `_require_attr` assertions `33-42`.
8. **Authority-violating implementation that passes:** keep empty shells under all names while reading the workbook directly or treating example YAML as live authority.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`; presence may remain as supplementary coverage but cannot carry the authority claim.

## 5. Assertion group 2 — runtime-settings access paths return equal example documents (`45-56`)

1. **Behaviour:** loads the default bundle and surface, then compares the runtime-settings model returned by each path.
2. **Authority meaning:** a governed runtime-settings authority would require admitted status, typed/versioned meaning and replaceable configuration access.
3. **Mismatch:** both paths read the same one-line placeholder example file. `config/README.md:11-18` explicitly says this file is example-only and not runtime authority. Equality therefore proves accessor consistency, not authority.
4. **Proved:** the two default access routes currently return equal `RuntimeSettingsDocument` model dumps.
5. **Not proved:** admitted runtime-settings authority, schema completeness, path values, substitution using a different config directory, cache behaviour, error handling or downstream dependence through an interface.
6. **Falsifier:** make the two routes return different model contents.
7. **Required failure:** equality assertion `56`.
8. **Authority-violating implementation that passes:** return the same empty/default model from both routes while ignoring the file or silently treating an unpromoted example as live runtime truth.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `behavioural` only for default accessor equivalence.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`; separate example-surface consistency from live authority proof.

## 6. Assertion group 3 — one coefficient-authority identity, lineage string and record are exposed (`53-61`)

1. **Behaviour:** obtains the typed coefficient-authority document and checks `authority_id`, source-workbook path suffix and presence of `max_risk_per_trade` in the posture record map.
2. **Authority meaning:** Coefficient Authority is promoted typed config/contract truth with explicit identity, owner and workbook-to-config lineage; runtime consumes the typed config rather than workbook cells.
3. **Fit:** the three assertions are a bounded positive specimen of current typed promotion identity/lineage and one owner-filtered record.
4. **Proved:** the default document identifies itself as `coefficient_authority_v1`, declares the canonical workbook path, and contains the named posture-owned record.
5. **Not proved:** schema/promoted version assertion, record baseline/class/bounds/transform/runtime mutability, workbook-ref cell lineage, config-file fingerprint, missing/malformed-file rejection, no direct workbook read, substitution, or complete coefficient membership.
6. **Falsifier:** change the authority ID/path or remove/reassign the named record.
7. **Required failure:** assertions `57`, `58-60` or `61`.
8. **Authority-violating implementation that passes:** read the workbook at runtime, then construct a document containing the same three observed values; all assertions still pass.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage` limited to the tested document/path/record facts.
11. **Disposition/gate:** the clause is useful, but the file remains `BLOCKED_P3_REPAIR` because its central direct-read prohibition is unobserved and mixed with example-only surfaces.

## 7. Assertion group 4 — playbook-registry access paths return equal example documents (`62`)

1. **Behaviour:** compares model dumps returned from the surface and the already loaded bundle.
2. **Authority meaning:** Playbook Library is a provisional thin-seam owner for governed definitions, constraints and metadata receipts, separated from eligibility, capital, broker and coefficient authority.
3. **Mismatch:** both values originate from `playbook_registry.example.yaml`, which `config/README.md:13-18` says is not runtime authority until promoted. Equality proves no definition semantics, hidden-authority rejection or owner boundary.
4. **Proved:** both current default access paths return equal playbook registry models.
5. **Not proved:** promoted registry status, registry identity/version correctness, definition/constraint content, duplicate rejection, hidden-authority exclusion, copy safety, eligibility separation, substitution or runtime composition.
6. **Falsifier:** make the two access paths return different model content.
7. **Required failure:** equality assertion `62`.
8. **Authority-violating implementation that passes:** return the same semantically invalid or unpromoted registry object from both paths.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `behavioural` only for accessor equivalence.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`; do not cite this assertion as Playbook Library authority.

## 8. Adversarial challenge — direct workbook reads

An implementation can open and parse the `.xlsx` workbook inside `coefficient_authority_document()`, then return a typed document with the same `authority_id`, `workbook_source_path`, posture record and playbook/runtime-setting outputs. Every assertion in this file still passes. Therefore the test does not prove the explicit direct-runtime-read prohibition despite its test name.

P3 repair requires a direct observation of filesystem/workbook access (for example an isolated config root plus a fail-on-`.xlsx` read boundary), and should split live coefficient-authority proof from example-only config-home smoke coverage.

## 9. Final file disposition

`BLOCKED_P3_REPAIR`

One bounded identity/lineage clause is valid, but the file's principal authority claim is false-positive prone: no assertion would fail if runtime code read the workbook directly. It also blends one live coefficient-authority file with multiple explicitly example-only surfaces under a single `config_authority` label.

- Assertion-group count: `4`
- Relationship count: `4`
- Return gate: P3 must add direct no-workbook-read proof and separate live authority from example-only accessor coverage before Tier-A readmission.
