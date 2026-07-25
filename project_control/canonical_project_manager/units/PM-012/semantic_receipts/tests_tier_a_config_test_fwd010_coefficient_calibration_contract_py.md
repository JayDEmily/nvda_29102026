# Semantic receipt — `tests/tier_a/config/test_fwd010_coefficient_calibration_contract.py`

## 1. Process record

- Sequence: `008`
- Unit: `PM-012`
- Test SHA-256: `d39945382db55121d0d78b3f0b03199fd78bab216e36557d27d510121e01a526`
- Test read in full: lines `1-48`.
- Exercised implementation read in full: `src/nvda_desk/config/coefficient_authority.py` lines `1-250`, `src/nvda_desk/contracts/modifiers.py` lines `1-120`, `src/nvda_desk/contracts/coefficient_authority.py` lines `1-213`, and `config/coefficient_authority.v1.yaml` lines `1-82`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/config/test_fwd010_coefficient_calibration_contract.py -q` returned `1 passed in 0.26s`, exit `0`.

## 2. Complete file restatement

The test constructs one calibration proposal containing one override, embeds it in an audit packet alongside a replay receipt, and separately builds a replay fixture pack. It checks calibration and target identifiers, packet/calibration linkage, active modifier identity, two Boolean permission fields, fixture-pack type and one path-stem lineage string.

The file does not inspect the proposed value or evidence reference, does not compare authority/config state before and after, does not hash the config file, does not prove no file mutation, does not reject out-of-bound proposed values, does not test promotion, review horizon, champion/challenger separation, historical/live-paper separation, owner-stage mismatch, unknown targets, modifier/config versions, complete fixture lineage or actual capital-deployment isolation.

## 3. Authority context

- Accepted `Coefficient Authority` and `Modifier Authority` permit runtime changes only through promoted typed authority; tests, workbook material and evaluation evidence cannot directly update live authority: `project_control/canonical_project_manager/units/PM-004/COEFFICIENT_MODIFIER_EVALUATION_ADJUDICATION_REGISTER.tsv`, `CME-001` and `CME-002`.
- Accepted `Champion/Challenger Evaluation` is non-deploying and promotion-gated; `Review Horizon` and live-paper/historical evidence remain promotion evidence only: the same register `CME-008` through `CME-010`.
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:271-286` prohibits unbounded mutation, hidden strategy changes, capital decisions and source ingestion at row 5.9.
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:179-184` requires deterministic semantic receipts with authority/version, owner, active modifier identity/version, resolved snapshots, closed classes and fingerprint.
- Testing law requires direct proof of the claimed state/non-interference behaviour; labels and schema construction alone are insufficient: `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:38-59`.

## 4. Assertion group 1 — calibration and target identifiers are carried (`40-41`)

1. **Behaviour:** verifies the calibration ID and first override target ID.
2. **Authority meaning:** a non-deploying coefficient candidate/evaluation artefact must remain explicitly identified and promotion-gated.
3. **Mismatch:** the assertions prove two strings only. They do not establish a governed evaluation class, review horizon, promotion gate, evidence-mode separation or valid proposal content.
4. **Proved:** the constructed model preserves `calibration-1` and `max_risk_per_trade`.
5. **Not proved:** proposed value, evidence reference, bounds, owner, target mutability, version, uniqueness or non-deployment.
6. **Falsifier:** rewrite either identifier during model/service construction.
7. **Required failure:** assertions `40-41`.
8. **Authority-violating implementation that passes:** accept an out-of-bounds or auto-promoted override while preserving both strings.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `identity_lineage` limited to two identifiers.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`.

## 5. Assertion group 2 — audit packet links calibration and active policy IDs (`42-44`)

1. **Behaviour:** checks packet ID, embedded calibration ID and replay-receipt active policy list.
2. **Authority meaning:** evaluation/audit evidence must preserve proposal and result-changing modifier/config identity without granting live authority.
3. **Fit:** this is a bounded identity-carriage specimen, but it omits all material versions and does not prove the packet's audit-only role.
4. **Proved:** the three tested identifiers are present in the returned packet graph.
5. **Not proved:** authority/schema/modifier versions, resolved snapshot correctness, evidence linkage, deterministic fingerprint, promotion state or consumer behaviour.
6. **Falsifier:** detach/replace the calibration or active policy identity.
7. **Required failure:** assertions `42-44`.
8. **Authority-violating implementation that passes:** attach the identifiers while applying the calibration live or omitting material versions.
9. **Semantic relation:** `bounded_separable_clause` for identifier carriage only.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** valid narrow evidence, insufficient to admit the file's no-live-mutation claim.

## 6. Assertion group 3 — audit packet declares live update disallowed (`45`)

1. **Behaviour:** checks a Boolean field is `False`.
2. **Authority meaning:** evaluation evidence must not directly mutate promoted live coefficient/modifier authority.
3. **Mismatch:** a declarative flag is not proof that the service did not mutate config, authority state or downstream values.
4. **Proved:** the returned audit model carries `live_update_allowed=False`.
5. **Not proved:** no live mutation, no auto-promotion, no file write, no runtime-state update or enforcement by consumers.
6. **Falsifier:** return the flag as true.
7. **Required failure:** assertion `45`.
8. **Authority-violating implementation that passes:** mutate the YAML or in-memory authority before returning a packet whose flag remains false.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `boundary` as declared metadata only.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`; add before/after state/file proof and a negative mutation path.

## 7. Assertion group 4 — fixture-pack type and first lineage token (`46-47`)

1. **Behaviour:** verifies model type and that the first lineage item equals the authority file stem.
2. **Authority meaning:** replay/evaluation evidence must identify retrievable, versioned material authority and deterministic dependencies.
3. **Mismatch:** a path stem is not authority content identity, version, fingerprint or retrievable verified evidence. Type construction is not replay adequacy.
4. **Proved:** the service returns the named model and inserts `coefficient_authority.v1` as the first lineage string.
5. **Not proved:** file content hash, schema/config/modifier versions, complete fixture lineage, replay class, source retrievability or deterministic result equivalence.
6. **Falsifier:** return another type or change the first lineage string.
7. **Required failure:** assertions `46-47`.
8. **Authority-violating implementation that passes:** use any file contents under the same stem, or omit all result-changing version evidence.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `specimen_only`.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`.

## 8. Assertion group 5 — fixture pack declares capital deployment disallowed (`48`)

1. **Behaviour:** checks a Boolean field is false.
2. **Authority meaning:** row 5.9 must not originate capital-deployment authority.
3. **Mismatch:** the assertion proves only a label on one fixture object, not absence of capital decision behaviour or downstream enforcement.
4. **Proved:** this fixture pack carries `capital_deployment_allowed=False`.
5. **Not proved:** no capital calculation, no capital receipt creation, no hidden capital field, no consumer override or system-level separation.
6. **Falsifier:** return the field as true.
7. **Required failure:** assertion `48`.
8. **Authority-violating implementation that passes:** perform or expose capital deployment elsewhere while leaving the fixture flag false.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `boundary` as declared metadata only.
11. **Disposition/gate:** `BLOCKED_P3_REPAIR`.

## 9. Final file disposition

`BLOCKED_P3_REPAIR`

The test carries several useful identifiers, but its title claims construction “without live mutation” while no assertion observes authority/config state or file writes. A mutating implementation can preserve every asserted value. The calibration proposal also lacks tested bound validation, promotion-gate status and material version evidence.

- Assertion-group count: `5`
- Relationship count: `5`
- Return gate: P3 must prove before/after authority immutability, reject unlawful calibration values/owners, and replace path-stem lineage with material version/fingerprint evidence before Tier-A admission.
